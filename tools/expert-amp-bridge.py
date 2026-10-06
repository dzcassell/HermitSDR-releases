#!/usr/bin/env python3
"""HermitSDR reference-amplifier bridge for Expert Amp Server (issue #190).

Lets HermitSDR's "Reference amplifier (line protocol)" driver (Station ->
Control Devices -> Station Devices) show an SPE Expert amplifier that is
already managed by Expert Amp Server (github.com/w9fyi/expert-amp-server,
a fork of FtlC-ian/expert-amp-server). The bridge listens on a TCP port,
speaks the reference line protocol documented in
docs/ReferenceAmplifierProtocol.md, and answers from what it reads at the
server's GET /api/v1/status. Python 3 standard library only (3.7 or newer).

  # on the Raspberry Pi, beside Expert Amp Server (HermitSDR on another Mac)
  python3 expert-amp-bridge.py --listen 0.0.0.0 --amp-url http://127.0.0.1:8088

  # on the Mac that runs HermitSDR (the default listen address is loopback)
  python3 expert-amp-bridge.py --amp-url http://amp-pi.local:8088

  # no amplifier, no HermitSDR: check the bridge against built-in fakes
  python3 expert-amp-bridge.py --selftest

Then add a device in HermitSDR with link TCP, the bridge's host, port 4001.

Monitor-only by default: the only request this program makes is
GET <amp-url>/api/v1/status, and the protocol's OPER, STBY, TUNE and BAND
commands are answered "ERR READONLY".

With --allow-control, OPER and STBY are honoured through Expert Amp Server's
OPERATE key (POST /api/v1/actions/button {"name":"operate"}). That key
*toggles*, and the server has no separate standby action, so the bridge
turns the absolute command into a verified toggle: read the amplifier's
state fresh (never from the poll cache); if it already matches, answer OK
without pressing; otherwise press once, wait --control-settle seconds, read
again, and answer OK only when the amplifier reports the requested state.
One retry if the state did not change at all; never more than two presses
per command; any other outcome is "ERR STATE …" with what the amplifier
reports, and nothing further is pressed. OPER is refused while the amplifier
reports an alarm. TUNE and BAND stay refused (the server offers no absolute
action for them). The residual risk is a hand on the front panel in the
second between the read and the press — the verification reports it.

Honest readings: a value the server does not report is sent as "-" (shown
as a dash in HermitSDR), never as a number. When the server is unreachable,
serves fixture data, or reports no recent contact with the amplifier, every
value is "-" and the bridge raises the protocol's ALM line. By default that
is code WLINK, a warning: HermitSDR does not stop transmitting when its own
link to a device drops, so the bridge does not either, and an amplifier that
is switched off does not block barefoot operation. --link-loss fault raises
LINK instead, a fault that inhibits transmit in HermitSDR while it lasts.
An alarm reported by the amplifier is always ALM AMPALARM, a fault (inhibit);
amplifier warnings become ALM WAMP (warning only).

Nothing here can key a radio. Tested against the built-in fakes only; see
the document for what has and has not been checked on real hardware.
"""
import argparse
import contextlib
import http.client
import io
import json
import math
import re
import signal
import socket
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

BRIDGE_VERSION = "1.1"
BUTTON_PATH = "/api/v1/actions/button"
STATUS_PATH = "/api/v1/status"
DEFAULT_PORT = 4001            # the port HermitSDR's "Add..." sheet pre-fills
MAX_COMMAND_BYTES = 256        # longest unterminated command we will buffer
MAX_HTTP_BYTES = 262144        # largest status reply we will read
SOCKET_TICK = 1.0              # upper bound on any single client socket wait

# Alarm codes this bridge can raise. The set is fixed so that a new
# connection can clear every code that is not active: HermitSDR keeps alarms
# across reconnects until it hears "CLR <code>". HermitSDR treats a code that
# starts with W as a warning and every other code as a fault (TX inhibit).
ALARM_AMP = "AMPALARM"         # the amplifier reports an alarm       (fault)
ALARM_AMP_WARNING = "WAMP"     # the amplifier reports a warning      (warning)
ALARM_LINK_WARNING = "WLINK"   # no fresh amplifier status, default   (warning)
ALARM_LINK = "LINK"            # same, with --link-loss fault         (fault)
ALARM_NO_STATUS = "WNOSTATUS"  # display-derived data only            (warning)
ALARM_UNIVERSE = (ALARM_AMP, ALARM_AMP_WARNING, ALARM_LINK, ALARM_LINK_WARNING,
                  ALARM_NO_STATUS)

TEMPERATURE_KEYS = ("temperatureC", "temperatureLowerC", "temperatureCombinerC")

_LOG_LOCK = threading.Lock()
_QUIET = False


def log(message):
    if _QUIET:
        return
    with _LOG_LOCK:
        sys.stderr.write("%s %s\n" % (time.strftime("%H:%M:%S"), message))
        sys.stderr.flush()


# --- Expert Amp Server side (HTTP GET only) -----------------------------------

class UpstreamError(Exception):
    pass


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None            # a status endpoint has no business redirecting


# No proxy (this is a station LAN) and no redirects.
_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}), _NoRedirect())


def status_url(base):
    """Validate --amp-url and return the one URL this program ever requests."""
    parts = urllib.parse.urlsplit(base.strip())
    if parts.scheme not in ("http", "https") or not parts.netloc:
        raise ValueError("--amp-url must look like http://host:8088")
    if parts.query or parts.fragment:
        raise ValueError("--amp-url must not carry a query or fragment")
    return urllib.parse.urlunsplit(
        (parts.scheme, parts.netloc, parts.path.rstrip("/") + STATUS_PATH, "", ""))


def fetch_status(url, timeout):
    """GET the status document and return its `data` object.

    Every socket operation is bounded by `timeout`; the whole exchange is
    bounded by roughly three times that. Raises UpstreamError otherwise.
    """
    request = urllib.request.Request(url, method="GET", headers={
        "Accept": "application/json",
        "User-Agent": "hermitsdr-expert-amp-bridge/" + BRIDGE_VERSION,
    })
    deadline = time.monotonic() + 2.0 * timeout
    body = bytearray()
    try:
        with _OPENER.open(request, timeout=timeout) as response:
            if response.status != 200:
                raise UpstreamError("HTTP %d" % response.status)
            while True:
                chunk = response.read1(65536)
                if not chunk:
                    break
                body += chunk
                if len(body) > MAX_HTTP_BYTES:
                    raise UpstreamError("status reply too large")
                if time.monotonic() > deadline:
                    raise UpstreamError("status reply too slow")
    except UpstreamError:
        raise
    except urllib.error.HTTPError as error:
        raise UpstreamError("HTTP %d" % error.code)
    except urllib.error.URLError as error:
        raise UpstreamError(clean_text(getattr(error, "reason", error), 80))
    except (OSError, ValueError, http.client.HTTPException) as error:
        raise UpstreamError(clean_text(error, 80) or error.__class__.__name__)
    try:
        document = json.loads(body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        raise UpstreamError("status reply is not JSON")
    if not isinstance(document, dict) or document.get("success") is not True \
            or not isinstance(document.get("data"), dict):
        raise UpstreamError("status reply has no success/data")
    return document["data"]


def press_button(base, name, timeout):
    """POST the front-panel key `name` (Expert Amp Server's actions API).

    Raises UpstreamError unless the server answers 2xx with a JSON document
    whose `success` is not false.
    """
    body = json.dumps({"name": name}).encode("utf-8")
    request = urllib.request.Request(base.rstrip("/") + BUTTON_PATH, data=body, method="POST",
                                     headers={"Accept": "application/json",
                                              "Content-Type": "application/json",
                                              "User-Agent": "hermitsdr-expert-amp-bridge/"
                                              + BRIDGE_VERSION})
    try:
        with _OPENER.open(request, timeout=timeout) as response:
            if not 200 <= response.status < 300:
                raise UpstreamError("HTTP %d" % response.status)
            reply = response.read(MAX_HTTP_BYTES)
    except UpstreamError:
        raise
    except urllib.error.HTTPError as error:
        raise UpstreamError("HTTP %d" % error.code)
    except urllib.error.URLError as error:
        raise UpstreamError(clean_text(getattr(error, "reason", error), 80))
    except (OSError, ValueError, http.client.HTTPException) as error:
        raise UpstreamError(clean_text(error, 80) or error.__class__.__name__)
    try:
        document = json.loads(reply.decode("utf-8")) if reply.strip() else {}
    except (ValueError, UnicodeDecodeError):
        raise UpstreamError("button reply is not JSON")
    if isinstance(document, dict) and document.get("success") is False:
        raise UpstreamError("server refused: " + clean_text(document.get("error", "no reason"), 80))


class Snapshot(object):
    """What the poller knows: the last good status and the last error."""

    def __init__(self, status=None, status_at=0.0, error=None, model=None):
        self.status = status          # dict from the last successful GET
        self.status_at = status_at    # time.monotonic() of that GET
        self.error = error            # text of the most recent failure, or None
        self.model = model            # last model name the server reported


class StatusPoller(threading.Thread):
    def __init__(self, url, interval, http_timeout):
        threading.Thread.__init__(self, name="amp-status-poll", daemon=True)
        self.url = url
        self.interval = interval
        self.http_timeout = http_timeout
        self.first_result = threading.Event()
        self._halt = threading.Event()
        self._lock = threading.Lock()
        self._snapshot = Snapshot()

    def snapshot(self):
        with self._lock:
            return self._snapshot

    def halt(self):
        self._halt.set()

    def run(self):
        while not self._halt.is_set():
            started = time.monotonic()
            previous = self.snapshot()
            try:
                status = fetch_status(self.url, self.http_timeout)
                model = model_token(status.get("modelName")) or previous.model
                fresh = Snapshot(status, time.monotonic(), None, model)
                if previous.error is not None or previous.status is None:
                    log("amp server: status OK (%s)" % (model or "model not reported"))
            except UpstreamError as error:
                text = str(error)
                fresh = Snapshot(previous.status, previous.status_at, text, previous.model)
                if previous.error != text:
                    log("amp server: %s" % text)
            with self._lock:
                self._snapshot = fresh
            self.first_result.set()
            self._halt.wait(max(0.0, self.interval - (time.monotonic() - started)))


# --- Mapping Expert Amp Server status onto the reference protocol ------------

def clean_text(value, limit=120):
    """Printable ASCII, single spaces, bounded: safe inside one protocol line."""
    text = "".join(ch if 32 <= ord(ch) < 127 else " " for ch in str(value))
    return " ".join(text.split())[:limit]


def model_token(name):
    """'EXPERT 2K-FA' -> 'EXPERT-2K-FA' (the ID line's model is one word)."""
    if not isinstance(name, str):
        return None
    token = re.sub(r"[^A-Z0-9.]+", "-", name.upper()).strip("-")[:32]
    return token or None


def number(status, key):
    value = status.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    value = float(value)
    return value if math.isfinite(value) else None


def band_meters(text):
    """'20m' / '80 m' -> 20 / 80. Anything else is unknown."""
    if not isinstance(text, str):
        return None
    match = re.match(r"^\s*(\d{1,4})\s*m\s*$", text, re.IGNORECASE)
    return int(match.group(1)) if match else None


def describe(code, *lists):
    """One line of text for an alarm/warning code plus the server's wording."""
    code = clean_text(code or "", 8)
    if code.upper() == "N":
        code = ""
    words = []
    for items in lists:
        if isinstance(items, list) and items:
            words = [clean_text(item, 60) for item in items if isinstance(item, str)]
            break
    text = (code + " " + "; ".join(word for word in words if word)).strip()
    return clean_text(text) or None


def link_problem(snapshot, now, stale_after):
    """Why the amplifier status cannot be trusted right now, or None."""
    if snapshot.status is None:
        return "no status from Expert Amp Server" + \
            (": " + snapshot.error if snapshot.error else " yet")
    if now - snapshot.status_at > stale_after:
        return "no status from Expert Amp Server" + \
            (": " + snapshot.error if snapshot.error else " (stalled)")
    status = snapshot.status
    confidence = str(status.get("confidence", "")).lower()
    source = str(status.get("source", "")).lower()
    if confidence.startswith("fixture") or source.startswith(("fixture", "demo")):
        return "Expert Amp Server is serving fixture data, not a live amplifier"
    if status.get("recentContact") is not True:
        return "Expert Amp Server reports no recent contact with the amplifier"
    return None


def _format(value, pattern):
    if value is None:
        return "-"
    text = pattern % value
    return text.rstrip("0").rstrip(".") if pattern == "%.1f" else text


def build_view(snapshot, now, stale_after, link_code):
    """Return (ST line, {alarm code: text}) for the current knowledge."""
    problem = link_problem(snapshot, now, stale_after)
    if problem is not None:
        fault = "UNKNOWN" if link_code.startswith("W") else link_code
        return "ST PWR - SWR - TEMP - BAND - FLT " + fault, {link_code: clean_text(problem)}

    status = snapshot.status
    alarms = {}
    native = status.get("provenance") == "status-poll"
    state = {"operate": "OPER", "standby": "STBY"}.get(
        str(status.get("operatingState", "")).strip().lower())
    power = number(status, "powerWatts")
    if power is not None and power < 0:
        power = None
    swr = number(status, "swr")
    if swr is not None and swr < 1.0:
        swr = None                    # the amplifier sends 0.00 when not measuring
    temperatures = [t for t in (number(status, key) for key in TEMPERATURE_KEYS)
                    if t is not None]
    temperature = max(temperatures) if temperatures else None
    band = band_meters(status.get("bandText"))
    if band is None:
        band = band_meters(status.get("band"))

    amp_alarm = describe(status.get("alarmCode"), status.get("alarmsText"),
                         status.get("activeAlarms"))
    amp_warning = describe(status.get("warningCode"), status.get("warningsText"),
                           status.get("warnings"))
    if amp_alarm:
        alarms[ALARM_AMP] = amp_alarm
    if amp_warning:
        alarms[ALARM_AMP_WARNING] = amp_warning
    if not native:
        alarms[ALARM_NO_STATUS] = ("display-derived data only: power and amplifier "
                                   "alarm codes are not available")
    fault = ALARM_AMP if amp_alarm else ("NONE" if native else "UNKNOWN")

    parts = ["ST"]
    if state:
        parts.append(state)           # omitted when unknown: never guessed
    parts += ["PWR", _format(power, "%.0f"), "SWR", _format(swr, "%.2f"),
              "TEMP", _format(temperature, "%.1f"),
              "BAND", "-" if band is None else str(band), "FLT", fault]
    return " ".join(parts), alarms


# --- HermitSDR side (the reference line protocol over TCP) --------------------

class Config(object):
    def __init__(self, amp_url="http://127.0.0.1:8088", listen="127.0.0.1",
                 port=DEFAULT_PORT, poll=1.0, stale_after=3.0, http_timeout=2.0,
                 link_loss="warning", max_clients=4, client_idle=90.0, model=None,
                 verbose=False, allow_control=False, control_settle=1.0):
        self.amp_url = amp_url
        self.allow_control = allow_control
        self.control_settle = control_settle
        self.listen = listen
        self.port = port
        self.poll = poll
        self.stale_after = stale_after
        self.http_timeout = http_timeout
        self.link_loss = link_loss
        self.max_clients = max_clients
        self.client_idle = client_idle
        self.model = model
        self.verbose = verbose


class ClientSession(object):
    """One HermitSDR connection. Owns its socket and its alarm bookkeeping."""

    def __init__(self, bridge, sock, peer):
        self.bridge = bridge
        self.sock = sock
        self.peer = peer
        self.synced = False           # has this connection had its alarm sync?
        self.sent_alarms = {}         # code -> text as last told to this peer

    def run(self):
        cfg = self.bridge.cfg
        tick = min(SOCKET_TICK, max(0.05, cfg.client_idle / 2.0))
        buffered = b""
        last_command = time.monotonic()
        try:
            self.sock.settimeout(tick)    # bounds every recv and every sendall
            while not self.bridge.stopping.is_set():
                try:
                    chunk = self.sock.recv(4096)
                except socket.timeout:
                    chunk = None
                if chunk == b"":
                    break                 # peer closed
                if chunk:
                    buffered += chunk
                    parts = re.split(b"[\r\n]", buffered)
                    buffered = parts.pop()
                    for raw in parts:
                        if not raw:
                            continue      # CR LF pairs and blank lines
                        last_command = time.monotonic()
                        replies = self.handle(raw.decode("ascii", "replace"))
                        self.send(replies)
                    if len(buffered) > MAX_COMMAND_BYTES:
                        buffered = b""    # discard, exactly as the app's driver does
                        self.send(["ERR LINE too long"])
                if time.monotonic() - last_command > cfg.client_idle:
                    log("client %s: idle for %.0f s, closing" % (self.peer, cfg.client_idle))
                    break
        except OSError as error:
            log("client %s: %s" % (self.peer, clean_text(error, 80)))
        finally:
            try:
                self.sock.close()
            except OSError:
                pass

    def send(self, lines):
        if lines:
            self.sock.sendall(("\r\n".join(lines) + "\r\n").encode("ascii", "replace"))

    def handle(self, line):
        fields = line.split()
        if not fields:
            return []
        head = fields[0].upper()
        if self.bridge.cfg.verbose and head != "LOGIN":
            log("client %s: %s" % (self.peer, clean_text(line, 60)))
        if head == "ID?":
            return ["ID %s FW bridge-%s SN -" % (self.bridge.model(), BRIDGE_VERSION)]
        if head == "ST?":
            st_line, alarms = self.bridge.view()
            return [st_line] + self.alarm_lines(alarms)
        if head in ("OPER", "STBY"):
            if not self.bridge.cfg.allow_control:
                return ["ERR READONLY bridge started without --allow-control, %s not sent" % head]
            return [self.bridge.set_operating(head == "OPER")]
        if head in ("TUNE", "BAND"):
            return ["ERR READONLY Expert Amp Server offers no absolute %s action; use the "
                    "amplifier's panel" % head]
        if head == "LOGIN":
            return ["OK"]                 # no secret is configured or checked
        return ["ERR UNKNOWN " + clean_text(head, 16)]

    def alarm_lines(self, alarms):
        lines = []
        if not self.synced:
            # HermitSDR keeps alarms across reconnects; start from a known state.
            lines += ["CLR " + code for code in ALARM_UNIVERSE if code not in alarms]
            self.synced = True
        lines += ["CLR " + code for code in sorted(self.sent_alarms) if code not in alarms]
        lines += ["ALM %s %s" % (code, text) for code, text in sorted(alarms.items())
                  if self.sent_alarms.get(code) != text]
        self.sent_alarms = dict(alarms)
        return lines


class Bridge(object):
    def __init__(self, cfg):
        self.cfg = cfg
        self.stopping = threading.Event()
        self.poller = StatusPoller(status_url(cfg.amp_url), cfg.poll, cfg.http_timeout)
        self.link_code = ALARM_LINK if cfg.link_loss == "fault" else ALARM_LINK_WARNING
        self._clients = 0
        self._clients_lock = threading.Lock()
        self._control_lock = threading.Lock()
        family = socket.AF_INET6 if ":" in cfg.listen else socket.AF_INET
        self.listener = socket.socket(family, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind((cfg.listen, cfg.port))
        self.listener.listen(8)
        self.listener.settimeout(0.25)
        self.port = self.listener.getsockname()[1]
        self._accept_thread = threading.Thread(target=self._accept_loop,
                                               name="bridge-accept", daemon=True)

    def start(self):
        self.poller.start()
        self._accept_thread.start()

    def stop(self):
        self.stopping.set()
        self.poller.halt()
        self._accept_thread.join(2.0)
        try:
            self.listener.close()
        except OSError:
            pass

    def client_count(self):
        with self._clients_lock:
            return self._clients

    def view(self):
        return build_view(self.poller.snapshot(), time.monotonic(),
                          self.cfg.stale_after, self.link_code)

    def set_operating(self, want_operate):
        """Honour OPER/STBY through the OPERATE toggle key, verified. One
        command at a time; returns the protocol reply line."""
        wanted = "operate" if want_operate else "standby"
        with self._control_lock:
            try:
                status = fetch_status(self.poller.url, self.cfg.http_timeout)
            except UpstreamError as error:
                return "ERR LINK cannot read the amplifier before %s: %s" % (wanted.upper(), error)
            if status.get("provenance") != "status-poll" or status.get("recentContact") is False:
                return "ERR LINK amplifier status is not live; %s not pressed" % wanted.upper()
            state = str(status.get("operatingState", "")).strip().lower()
            if state not in ("operate", "standby"):
                return "ERR STATE amplifier state unknown (%s); nothing pressed" % clean_text(state or "-", 20)
            if state == wanted:
                return "OK already in %s" % wanted.upper()
            if want_operate and describe(status.get("alarmCode"), status.get("alarmsText"),
                                         status.get("activeAlarms")):
                return "ERR ALARM amplifier reports an alarm; clear it before OPERATE"
            presses = 0
            for attempt in (1, 2):
                try:
                    press_button(self.cfg.amp_url, "operate", self.cfg.http_timeout)
                except UpstreamError as error:
                    log("control: OPERATE key press failed: %s" % error)
                    return "ERR LINK OPERATE key press failed: %s" % error
                presses += 1
                time.sleep(self.cfg.control_settle)
                try:
                    status = fetch_status(self.poller.url, self.cfg.http_timeout)
                except UpstreamError as error:
                    return ("ERR LINK pressed OPERATE once but could not read the result: %s; "
                            "check the amplifier" % error)
                now = str(status.get("operatingState", "")).strip().lower()
                if now == wanted:
                    log("control: amplifier now in %s (%d press%s)"
                        % (wanted.upper(), presses, "" if presses == 1 else "es"))
                    return "OK %s" % wanted.upper()
                if now != state:
                    # It moved, but not where we asked: someone else is on the
                    # panel or the server's state is behind. Do not fight it.
                    break
                # Unchanged after the press: one retry only.
            log("control: amplifier reports %s after %d press%s, wanted %s"
                % (now.upper() or "-", presses, "" if presses == 1 else "es", wanted.upper()))
            return ("ERR STATE amplifier reports %s after %d press%s; check the front panel"
                    % (now.upper() or "-", presses, "" if presses == 1 else "es"))

    def model(self):
        if self.cfg.model:
            return model_token(self.cfg.model) or "UNKNOWN"
        # Give the first status request a bounded chance to name the amplifier.
        self.poller.first_result.wait(self.cfg.http_timeout + 0.5)
        return self.poller.snapshot().model or "UNKNOWN"

    def _accept_loop(self):
        while not self.stopping.is_set():
            try:
                sock, address = self.listener.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            peer = "%s:%s" % (address[0], address[1])
            with self._clients_lock:
                admitted = self._clients < self.cfg.max_clients
                if admitted:
                    self._clients += 1
            if not admitted:
                log("client %s: refused, %d clients already connected"
                    % (peer, self.cfg.max_clients))
                try:
                    sock.settimeout(SOCKET_TICK)
                    sock.sendall(b"ERR BUSY too many clients\r\n")
                except OSError:
                    pass
                finally:
                    sock.close()
                continue
            try:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            except OSError:
                pass
            log("client %s: connected" % peer)
            threading.Thread(target=self._serve, args=(sock, peer),
                             name="client-" + peer, daemon=True).start()

    def _serve(self, sock, peer):
        try:
            ClientSession(self, sock, peer).run()
        finally:
            with self._clients_lock:
                self._clients -= 1
            log("client %s: disconnected" % peer)


# --- Self-test: fake Expert Amp Server + fake HermitSDR driver ----------------
#
# The fake server's JSON follows Expert Amp Server v0.4.8 (internal/api/types.go
# and internal/protocol/status.go); the standby payload is what that code
# produces for its own captured 2K-FA status frame
# (internal/protocol/testdata/status_response_example.bin). The fake client
# sends the byte sequences HermitSDR's driver sends and judges every reply with
# a line-for-line port of FakeAmplifierDriver.parse and LineFrameAssembler.

def canned_status(mode):
    live = {
        "modelName": "EXPERT 2K-FA", "operatingState": "standby", "mode": "standby",
        "tx": False, "input": "1", "antenna": "1", "outputLevel": "LOW",
        "swr": 0, "swrDisplay": "0.00", "antennaSwr": 0, "antennaSwrDisplay": "0.00",
        "paSupplyVoltage": 0, "paSupplyVoltageDisplay": "0.0",
        "paCurrent": 0, "paCurrentDisplay": "0.0",
        "temperatureC": 33, "temperatureUnit": "C", "temperatureDisplay": "33 C",
        "temperatureLowerC": 0, "temperatureLowerDisplay": "0 C",
        "temperatureCombinerC": 0, "temperatureCombinerDisplay": "0 C",
        "powerWatts": 0, "source": "serial", "confidence": "protocol-native",
        "provenance": "status-poll", "recentContact": True,
        "lastContactAt": "2026-10-05T12:00:00Z", "bandCode": "00", "bandText": "160m",
        "atuStatusCode": "a",
    }
    if mode == "standby":
        return live
    if mode in ("operate", "alarm", "warning"):
        live.update({
            "operatingState": "operate", "mode": "operate", "tx": True,
            "outputLevel": "HIGH", "swr": 1.25, "swrDisplay": "1.25",
            "antennaSwr": 1.4, "antennaSwrDisplay": "1.40",
            "paSupplyVoltage": 48.5, "paCurrent": 31.2, "powerWatts": 1200,
            "temperatureC": 58, "temperatureLowerC": 61, "temperatureCombinerC": 49,
            "bandCode": "05", "bandText": "20m",
        })
        if mode == "alarm":
            live.update({"alarmCode": "S", "alarmsText": ["swr exceeding limits"],
                         "activeAlarms": ["swr exceeding limits"]})
        if mode == "warning":
            live.update({"warningCode": "K", "warningsText": ["atu bypassed"],
                         "warnings": ["atu bypassed"]})
        return live
    if mode == "display-only":      # status poll never answered: display fallback
        return {
            "modelName": "EXPERT 2K-FA", "operatingState": "standby", "mode": "standby",
            "tx": False, "band": "40m", "input": "1", "antenna": "1",
            "outputLevel": "LOW", "swrDisplay": "-.--", "temperatureC": 30,
            "temperatureUnit": "C", "temperatureDisplay": "30 C", "source": "serial",
            "confidence": "display-derived", "provenance": "display-frame",
            "notes": ["powerWatts not exposed in current captured home display frame"],
            "recentContact": True, "lastContactAt": "2026-10-05T12:00:00Z",
        }
    if mode == "no-contact":        # server up, amplifier silent: recentContact omitted
        live.pop("recentContact")
        return live
    if mode == "fixture":           # server started without a serial port
        return {"modelName": "EXPERT 1.3K-FA", "operatingState": "standby",
                "band": "40m", "temperatureC": 22, "source": "fixture:home",
                "confidence": "fixture-derived", "provenance": "display-frame",
                "recentContact": True, "lastContactAt": "2026-10-05T12:00:00Z"}
    raise ValueError(mode)


class _ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


class FakeAmpServer(object):
    def __init__(self, port=0, control=False):
        self.mode = "standby"
        self.control = control        # answer the OPERATE key like Expert Amp Server
        self.press_effect = "toggle"  # "toggle" | "ignore" | "fail"
        self.presses = 0
        self.requests = []            # (method, path) of everything received
        fake = self

        class Handler(BaseHTTPRequestHandler):
            def _reply(self, code, body, kind="application/json"):
                self.send_response(code)
                self.send_header("Content-Type", kind)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self):
                fake.requests.append(("GET", self.path))
                if self.path != STATUS_PATH:
                    self._reply(404, b'{"success":false,"error":"not found"}')
                elif fake.mode == "http-500":
                    self._reply(500, b'{"success":false,"error":"boom"}')
                elif fake.mode == "garbage":
                    self._reply(200, b"<html>not json</html>", "text/html")
                elif fake.mode == "unsuccessful":
                    self._reply(200, b'{"success":false,"error":"nope"}')
                else:
                    document = {"success": True, "data": canned_status(fake.mode)}
                    self._reply(200, json.dumps(document).encode("utf-8"))

            def _state_changing(self):
                fake.requests.append((self.command, self.path))
                self._reply(405, b'{"success":false,"error":"selftest: write refused"}')

            def do_POST(self):
                if not fake.control or self.path != BUTTON_PATH:
                    return self._state_changing()
                fake.requests.append(("POST", self.path))
                length = int(self.headers.get("Content-Length") or 0)
                try:
                    body = json.loads(self.rfile.read(length).decode("utf-8"))
                except ValueError:
                    body = {}
                if body.get("name") != "operate":
                    return self._reply(400, b'{"success":false,"error":"unknown button"}')
                fake.presses += 1
                if fake.press_effect == "fail":
                    return self._reply(500, b'{"success":false,"error":"serial write failed"}')
                if fake.press_effect == "toggle":
                    fake.mode = "operate" if fake.mode == "standby" else "standby"
                self._reply(200, b'{"success":true,"data":{"pressed":"operate"}}')

            do_PUT = do_PATCH = do_DELETE = _state_changing

            def log_message(self, *_):
                pass

        self.httpd = _ThreadingHTTPServer(("127.0.0.1", port), Handler)
        self.port = self.httpd.server_address[1]
        self.url = "http://127.0.0.1:%d" % self.port
        self._thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self._thread.start()

    def stop(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self._thread.join(2.0)


_DECIMAL = re.compile(r"^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?$")
_SPECIAL = re.compile(r"^[+-]?(nan|inf|infinity|0x[0-9a-f.p+-]+)$", re.IGNORECASE)


def swift_double(text):
    """Swift's Double(String): a number, 'non-finite' for nan/inf/hex, or None."""
    if _DECIMAL.match(text):
        return float(text)
    if _SPECIAL.match(text):
        return "non-finite"
    return None


def swift_int(text):
    return int(text) if re.match(r"^[+-]?\d+$", text) else None


def driver_parse(line):
    """Port of FakeAmplifierDriver.parse(line:). Returns (kind, payload)."""
    fields = [field for field in line.split(" ") if field]
    if not fields:
        return None
    head = fields[0].upper()
    if head == "ID":
        model = firmware = serial = ""
        index = 1
        if index < len(fields) and fields[index] != "FW":
            model = fields[index]
            index += 1
        while index + 1 < len(fields):
            key = fields[index].upper()
            if key == "FW":
                firmware = fields[index + 1]
            elif key == "SN":
                serial = fields[index + 1]
            index += 2
        if not model:
            return ("rejected", "malformed ID")
        return ("identity", {"model": model, "firmware": firmware, "serial": serial})
    if head == "ST":
        telemetry = {"operating": None, "tuning": False, "power": None, "swr": None,
                     "temperature": None, "band": None, "fault": None, "keys": []}
        index = 1
        if index < len(fields):
            token = fields[index].upper()
            if token == "OPER":
                telemetry["operating"] = True
                index += 1
            elif token == "STBY":
                telemetry["operating"] = False
                index += 1
            elif token == "TUNING":
                telemetry["operating"] = True
                telemetry["tuning"] = True
                index += 1
        while index + 1 < len(fields):
            key, value = fields[index].upper(), fields[index + 1]
            telemetry["keys"].append(key)
            if key == "PWR":
                telemetry["power"] = swift_double(value)
            elif key == "SWR":
                telemetry["swr"] = swift_double(value)
            elif key == "TEMP":
                telemetry["temperature"] = swift_double(value)
            elif key == "BAND":
                telemetry["band"] = swift_int(value)
            elif key == "FLT":
                telemetry["fault"] = None if value.upper() == "NONE" else value
            index += 2
        return ("telemetry", telemetry)
    if head == "ALM":
        if len(fields) < 2:
            return ("rejected", "malformed ALM")
        code = fields[1].upper()
        return ("alarm", {"code": code, "text": " ".join(fields[2:]) or code,
                          "severity": "warning" if code.startswith("W") else "fault"})
    if head == "CLR":
        if len(fields) < 2:
            return ("rejected", "malformed CLR")
        return ("cleared", fields[1].upper())
    if head == "OK":
        return ("ack", None)
    if head == "ERR":
        return ("rejected", " ".join(fields[1:]))
    return ("log", "unrecognized line: " + line[:80])


class DriverClient(object):
    """Stands in for HermitSDR: sends its bytes, applies its parsing rules."""

    violations = []                   # shared across every client in the run
    lines_checked = 0

    def __init__(self, port):
        self.sock = socket.create_connection(("127.0.0.1", port), timeout=2.0)
        self.buffer = b""             # LineFrameAssembler(limit: 1024)
        self.raw = b""
        self.alarms = {}              # code -> (severity, text), as the session keeps
        self.identity = None

    def close(self):
        try:
            self.sock.close()
        except OSError:
            pass

    def send(self, text):
        self.sock.sendall(text.encode("ascii"))

    def _push(self, data):
        events = []
        self.raw += data
        self.buffer += data
        while True:
            match = re.search(b"[\r\n]", self.buffer)
            if not match:
                break
            raw, self.buffer = self.buffer[:match.start()], self.buffer[match.end():]
            if not raw:
                continue
            line = raw.decode("utf-8", "replace")
            event = driver_parse(line)
            DriverClient.lines_checked += 1
            if len(raw) > 1024:
                DriverClient.violations.append("line over 1024 bytes: " + line[:60])
            if event is None or event[0] == "log":
                DriverClient.violations.append("driver would not recognize: " + line)
            elif event[0] == "rejected" and event[1].startswith("malformed"):
                DriverClient.violations.append("driver calls it malformed: " + line)
            elif event[0] == "telemetry":
                payload = event[1]
                if payload["keys"] != ["PWR", "SWR", "TEMP", "BAND", "FLT"]:
                    DriverClient.violations.append("ST keys misaligned: " + line)
                if "non-finite" in (payload["power"], payload["swr"], payload["temperature"]):
                    DriverClient.violations.append("non-finite number: " + line)
            if event is not None:
                if event[0] == "alarm":
                    self.alarms[event[1]["code"]] = (event[1]["severity"], event[1]["text"])
                elif event[0] == "cleared":
                    self.alarms.pop(event[1], None)
                elif event[0] == "identity":
                    self.identity = event[1]
                events.append(event)
        if len(self.buffer) > 1024:
            DriverClient.violations.append("unterminated reply over 1024 bytes")
            self.buffer = b""
        return events

    def read(self, want=1, timeout=2.0, quiet=0.08):
        """Collect events until `want` arrived and the line went quiet."""
        events = []
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            self.sock.settimeout(quiet if len(events) >= want else 0.25)
            try:
                data = self.sock.recv(4096)
            except socket.timeout:
                if len(events) >= want:
                    break
                continue
            if not data:
                events.append(("closed", None))
                break
            events += self._push(data)
        return events

    def command(self, text, want=1):
        self.send(text)
        return self.read(want)

    def poll(self):
        events = self.command("ST?\r\n")
        telemetry = [payload for kind, payload in events if kind == "telemetry"]
        return (telemetry[-1] if telemetry else None), events

    def poll_until(self, predicate, timeout=5.0):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            telemetry, _ = self.poll()
            if telemetry is not None and predicate(telemetry):
                return telemetry
            time.sleep(0.05)
        return None


def selftest():
    global _QUIET
    _QUIET = True
    results = {"pass": 0, "fail": 0}

    def check(name, condition, detail=""):
        results["pass" if condition else "fail"] += 1
        print("%s  %s%s" % ("PASS" if condition else "FAIL", name,
                             "" if condition or not detail else "  [%s]" % detail))
        return condition

    # 1. Pure mapping, no sockets.
    def view(mode, age=0.0, error=None, link_code=ALARM_LINK_WARNING):
        status = canned_status(mode) if mode else None
        snapshot = Snapshot(status, 100.0, error, None)
        return build_view(snapshot, 100.0 + age, 3.0, link_code)

    line, alarms = view("standby")
    check("map: standby frame -> STBY, 0 W, SWR unavailable, 33 C, 160 m",
          line == "ST STBY PWR 0 SWR - TEMP 33 BAND 160 FLT NONE" and alarms == {}, line)
    line, alarms = view("operate")
    check("map: operate -> OPER, 1200 W, 1.25, hottest sensor 61 C, 20 m",
          line == "ST OPER PWR 1200 SWR 1.25 TEMP 61 BAND 20 FLT NONE" and alarms == {}, line)
    line, alarms = view("alarm")
    check("map: amplifier alarm -> FLT AMPALARM + fault alarm text",
          line.endswith("FLT AMPALARM") and alarms == {ALARM_AMP: "S swr exceeding limits"},
          "%s %s" % (line, alarms))
    line, alarms = view("warning")
    check("map: amplifier warning -> warning-severity code only",
          line.endswith("FLT NONE") and alarms == {ALARM_AMP_WARNING: "K atu bypassed"},
          "%s %s" % (line, alarms))
    line, alarms = view("display-only")
    check("map: display-derived -> no power, no SWR, FLT UNKNOWN, WNOSTATUS warning",
          line == "ST STBY PWR - SWR - TEMP 30 BAND 40 FLT UNKNOWN"
          and list(alarms) == [ALARM_NO_STATUS], line)
    for mode, label in (("no-contact", "no recent amplifier contact"),
                        ("fixture", "fixture data")):
        line, alarms = view(mode)
        check("map: %s -> every value unavailable + WLINK warning (default)" % label,
              line == "ST PWR - SWR - TEMP - BAND - FLT UNKNOWN"
              and list(alarms) == [ALARM_LINK_WARNING], line)
        line, alarms = view(mode, link_code=ALARM_LINK)
        check("map: %s -> every value unavailable + LINK fault (--link-loss fault)" % label,
              line == "ST PWR - SWR - TEMP - BAND - FLT LINK" and list(alarms) == [ALARM_LINK],
              line)
    for link_code in (ALARM_LINK_WARNING, ALARM_LINK):
        line, alarms = view("operate", age=3.5, error="timed out", link_code=link_code)
        check("map: status older than --stale-after -> unavailable, never the old "
              "numbers (%s)" % link_code,
              line.startswith("ST PWR - SWR - TEMP - BAND - FLT ")
              and list(alarms) == [link_code] and "timed out" in alarms[link_code], line)
        line, alarms = view(None, error="Connection refused", link_code=link_code)
        check("map: never reached the server -> unavailable + %s" % link_code,
              line.startswith("ST PWR - SWR - TEMP - BAND - FLT ")
              and list(alarms) == [link_code], line)
        line, alarms = view("alarm", link_code=link_code)
        check("map: a real amplifier alarm is a fault whatever --link-loss says (%s)"
              % link_code, list(alarms) == [ALARM_AMP] and line.endswith("FLT AMPALARM"), line)
    severities = [driver_parse("ALM %s x" % code)[1]["severity"] for code in ALARM_UNIVERSE]
    check("map: driver's first-letter rule: WLINK/WAMP/WNOSTATUS warn, LINK/AMPALARM fault",
          dict(zip(ALARM_UNIVERSE, severities)) == {
              ALARM_AMP: "fault", ALARM_AMP_WARNING: "warning", ALARM_LINK: "fault",
              ALARM_LINK_WARNING: "warning", ALARM_NO_STATUS: "warning"}, str(severities))
    hostile = dict(canned_status("operate"), powerWatts=float("nan"), swr=True,
                   temperatureC="hot", temperatureLowerC=None, temperatureCombinerC=None,
                   bandText="20m\r\nALM X", operatingState="tuning?",
                   alarmsText=["bad\r\nOK line"], alarmCode="Z")
    line, alarms = build_view(Snapshot(hostile, 100.0), 100.0, 3.0, ALARM_LINK)
    check("map: malformed fields become unavailable and cannot inject a line",
          line == "ST PWR - SWR - TEMP - BAND - FLT AMPALARM"
          and alarms == {ALARM_AMP: "Z bad OK line"}, "%s %s" % (line, alarms))
    check("map: model name becomes one word", model_token("EXPERT 2K-FA") == "EXPERT-2K-FA")
    try:
        status_url("ftp://amp")
        refused = False
    except ValueError:
        refused = True
    check("config: --amp-url must be http(s); request path is fixed",
          refused and status_url("http://pi:8088/") == "http://pi:8088/api/v1/status")
    check("config: default listen address is loopback", Config().listen == "127.0.0.1")
    check("config: control is off unless --allow-control", Config().allow_control is False)
    check("config: lost amplifier status is a warning by default, a fault on request",
          Config().link_loss == "warning"
          and parse_arguments([]).link_loss == "warning"
          and parse_arguments(["--link-loss", "fault"]).link_loss == "fault")
    args = parse_arguments(["--allow-control", "--control-settle", "0.5"])
    check("config: --allow-control is accepted and off by default",
          args.allow_control is True and args.control_settle == 0.5
          and parse_arguments([]).allow_control is False)
    with contextlib.redirect_stderr(io.StringIO()) as captured:
        try:
            parse_arguments(["--control-settle", "0"])
            code = 0
        except SystemExit as stop:
            code = stop.code
    check("config: a zero or negative --control-settle is refused",
          code == 2 and "control-settle" in captured.getvalue())

    # 2. End to end over real sockets.
    fake = FakeAmpServer()
    bridge = Bridge(Config(amp_url=fake.url, port=0, poll=0.05, stale_after=0.5,
                           http_timeout=0.5, max_clients=3, client_idle=2.0))
    bridge.start()
    clients = []

    def connect():
        client = DriverClient(bridge.port)
        clients.append(client)
        return client

    try:
        radio = connect()
        # Exactly what StationDeviceSession sends when the link opens: ID?, then
        # ST? as soon as the first write completes, without waiting for a reply.
        radio.send("ID?\r\n")
        radio.send("ST?\r\n")
        events = radio.read(want=2 + len(ALARM_UNIVERSE))
        kinds = [kind for kind, _ in events]
        telemetry = [payload for kind, payload in events if kind == "telemetry"]
        check("handshake: ID? answered with a model the driver accepts",
              radio.identity is not None and radio.identity["model"] == "EXPERT-2K-FA",
              str(radio.identity))
        check("handshake: first ST? answered with telemetry",
              len(telemetry) == 1 and telemetry[0]["operating"] is False
              and telemetry[0]["power"] == 0.0 and telemetry[0]["swr"] is None
              and telemetry[0]["temperature"] == 33.0 and telemetry[0]["band"] == 160,
              str(telemetry))
        check("handshake: first ST? clears every alarm code the bridge can raise",
              kinds.count("cleared") == len(ALARM_UNIVERSE) and radio.alarms == {}, str(kinds))

        started = time.monotonic()
        steady = [radio.poll() for _ in range(5)]
        check("poll: each ST? gets exactly one ST line and nothing else",
              all(tel is not None and len(ev) == 1 for tel, ev in steady)
              and time.monotonic() - started < 5.0)

        fake.mode = "operate"
        telemetry = radio.poll_until(lambda t: t["operating"] is True)
        check("poll: operate/transmit status follows the amplifier",
              telemetry is not None and telemetry["power"] == 1200.0
              and telemetry["swr"] == 1.25 and telemetry["temperature"] == 61.0
              and telemetry["band"] == 20, str(telemetry))

        replies = []
        for text in ("OPER\r\n", "STBY\r\n", "TUNE\r\n", "BAND 20\r\n"):
            replies += radio.command(text)
        check("read-only: OPER, STBY, TUNE and BAND are each refused with ERR",
              len(replies) == 4 and all(kind == "rejected" and payload.startswith("READONLY")
                                        for kind, payload in replies), str(replies))
        check("protocol: LOGIN is acknowledged, an unknown word is rejected",
              radio.command("LOGIN not-a-real-secret\r\n") == [("ack", None)]
              and radio.command("FROB\r\n") == [("rejected", "UNKNOWN FROB")])

        fake.mode = "alarm"
        radio.poll_until(lambda t: ALARM_AMP in radio.alarms)
        check("fault: amplifier alarm arrives as a fault-severity ALM",
              radio.alarms.get(ALARM_AMP) == ("fault", "S swr exceeding limits"),
              str(radio.alarms))
        second = connect()
        second.command("ID?\r\n")
        second.poll()
        check("reconnect: a new connection is told the active alarm and nothing stale",
              second.alarms == radio.alarms, str(second.alarms))
        second.close()
        fake.mode = "warning"
        radio.poll_until(lambda t: ALARM_AMP_WARNING in radio.alarms and ALARM_AMP not in radio.alarms)
        check("fault: alarm clears with CLR; an amplifier warning is warning severity",
              radio.alarms == {ALARM_AMP_WARNING: ("warning", "K atu bypassed")},
              str(radio.alarms))

        fake.mode = "display-only"
        telemetry = radio.poll_until(lambda t: ALARM_NO_STATUS in radio.alarms)
        check("degraded: display-derived data shows what exists and flags the rest",
              telemetry is not None and telemetry["power"] is None and telemetry["band"] == 40
              and telemetry["temperature"] == 30.0
              and radio.alarms == {ALARM_NO_STATUS: radio.alarms[ALARM_NO_STATUS]}
              and radio.alarms[ALARM_NO_STATUS][0] == "warning", str(telemetry))

        def unavailable(t):
            return (t["operating"] is None and t["power"] is None and t["swr"] is None
                    and t["temperature"] is None and t["band"] is None)

        for mode in ("no-contact", "fixture", "http-500", "garbage", "unsuccessful"):
            fake.mode = "operate"
            radio.poll_until(lambda t: t["power"] == 1200.0 and not radio.alarms)
            fake.mode = mode
            telemetry = radio.poll_until(
                lambda t: unavailable(t) and ALARM_LINK_WARNING in radio.alarms)
            check("stale: server mode '%s' -> all values unavailable + WLINK warning" % mode,
                  telemetry is not None and list(radio.alarms) == [ALARM_LINK_WARNING]
                  and radio.alarms[ALARM_LINK_WARNING][0] == "warning",
                  "%s %s" % (telemetry, radio.alarms))

        # The opt-in: a second bridge started with --link-loss fault.
        strict = Bridge(Config(amp_url=fake.url, port=0, poll=0.05, stale_after=0.5,
                               http_timeout=0.5, client_idle=2.0, link_loss="fault"))
        strict.start()
        try:
            careful = DriverClient(strict.port)
            clients.append(careful)
            telemetry = careful.poll_until(
                lambda t: unavailable(t) and ALARM_LINK in careful.alarms)
            check("--link-loss fault: lost amplifier status is a fault-severity LINK",
                  telemetry is not None and list(careful.alarms) == [ALARM_LINK]
                  and careful.alarms[ALARM_LINK][0] == "fault", str(careful.alarms))
            radio.poll()
            fake.mode = "alarm"
            careful.poll_until(lambda t: list(careful.alarms) == [ALARM_AMP])
            radio.poll_until(lambda t: list(radio.alarms) == [ALARM_AMP])
            check("both settings: LINK clears and a real amplifier alarm is a fault",
                  careful.alarms.get(ALARM_AMP, ("",))[0] == "fault"
                  and radio.alarms.get(ALARM_AMP, ("",))[0] == "fault"
                  and len(careful.alarms) == 1 and len(radio.alarms) == 1,
                  "%s %s" % (careful.alarms, radio.alarms))
            careful.close()
        finally:
            strict.stop()

        fake.mode = "operate"
        radio.poll_until(lambda t: t["power"] == 1200.0 and not radio.alarms)
        port = fake.port
        fake.stop()
        telemetry = radio.poll_until(
            lambda t: unavailable(t) and ALARM_LINK_WARNING in radio.alarms)
        check("stale: amp server gone (connection refused) -> unavailable + WLINK warning",
              telemetry is not None and radio.alarms[ALARM_LINK_WARNING][0] == "warning",
              "%s %s" % (telemetry, radio.alarms))
        before = fake.requests
        fake = FakeAmpServer(port)
        fake.mode = "operate"
        telemetry = radio.poll_until(lambda t: t["power"] == 1200.0 and not radio.alarms)
        check("recover: amp server back -> values return and WLINK is cleared",
              telemetry is not None and radio.alarms == {}, str(radio.alarms))

        radio.send("S")
        time.sleep(0.03)
        radio.send("T?")
        time.sleep(0.03)
        radio.send("\r")
        time.sleep(0.03)
        radio.send("\n")
        check("framing: a command split across segments is answered once",
              [kind for kind, _ in radio.read()] == ["telemetry"])
        check("framing: LF-only and CR-only terminators are accepted",
              [kind for kind, _ in radio.command("ST?\n")] == ["telemetry"]
              and [kind for kind, _ in radio.command("ST?\r")] == ["telemetry"])
        check("framing: two commands in one segment get two replies in order",
              [kind for kind, _ in radio.command("ID?\r\nST?\r\n", want=2)]
              == ["identity", "telemetry"])
        overflow = radio.command("X" * 300)
        check("framing: an over-long unterminated command is dropped, link survives",
              len(overflow) == 1 and overflow[0][0] == "rejected"
              and radio.poll()[0] is not None, str(overflow))

        # `radio` keeps polling through this section, as HermitSDR would.
        extra = [connect(), connect()]
        check("clients: three connections are served side by side",
              all(client.poll()[0] is not None for client in extra + [radio])
              and bridge.client_count() == 3, str(bridge.client_count()))
        fourth = connect()
        kinds = [kind for kind, _ in fourth.read(want=2)]
        check("clients: beyond --max-clients the bridge says ERR BUSY and closes",
              kinds == ["rejected", "closed"], str(kinds))
        for client in extra:
            client.close()
        deadline = time.monotonic() + 3.0
        while bridge.client_count() > 1 and time.monotonic() < deadline:
            radio.poll()
            time.sleep(0.05)
        check("clients: closed connections are released", bridge.client_count() == 1,
              str(bridge.client_count()))
        silent = connect()
        silent.send("ST")                       # connects, half a command, goes quiet
        kinds = []
        deadline = time.monotonic() + 3.0 * bridge.cfg.client_idle
        while not kinds and time.monotonic() < deadline:
            radio.poll()
            kinds = [kind for kind, _ in silent.read(want=1, timeout=0.2)]
        check("clients: an abandoned connection is closed after --client-idle",
              kinds == ["closed"] and bridge.client_count() == 1, str(kinds))
        check("clients: the live connection is unaffected", radio.poll()[0] is not None)

        # --allow-control: a separate fake with the OPERATE key, a separate bridge.
        ctrl_fake = FakeAmpServer(control=True)
        ctrl = Bridge(Config(amp_url=ctrl_fake.url, port=0, poll=0.05, stale_after=0.5,
                             http_timeout=0.5, client_idle=2.0, allow_control=True,
                             control_settle=0.05))
        ctrl.start()
        try:
            panel = DriverClient(ctrl.port)
            clients.append(panel)
            panel.command("ID?\r\n")
            panel.poll_until(lambda t: t["operating"] is False)
            reply = panel.command("OPER\r\n")
            check("control: OPER from standby presses the key once and verifies OPERATE",
                  reply == [("ack", None)] and ctrl_fake.presses == 1 and ctrl_fake.mode == "operate",
                  "%s presses=%d" % (reply, ctrl_fake.presses))
            reply = panel.command("OPER\r\n")
            check("control: OPER while already operating presses nothing",
                  reply == [("ack", None)] and ctrl_fake.presses == 1, str(reply))
            reply = panel.command("STBY\r\n")
            check("control: STBY from operate presses once and verifies STANDBY",
                  reply == [("ack", None)] and ctrl_fake.presses == 2 and ctrl_fake.mode == "standby",
                  "%s presses=%d" % (reply, ctrl_fake.presses))
            ctrl_fake.press_effect = "ignore"
            reply = panel.command("OPER\r\n")
            check("control: a key the amplifier ignores -> one retry, then ERR STATE, two presses",
                  len(reply) == 1 and reply[0][0] == "rejected" and reply[0][1].startswith("STATE")
                  and ctrl_fake.presses == 4 and ctrl_fake.mode == "standby", "%s presses=%d" % (reply, ctrl_fake.presses))
            ctrl_fake.press_effect = "fail"
            reply = panel.command("OPER\r\n")
            check("control: a failed press is ERR LINK and is not retried",
                  len(reply) == 1 and reply[0][0] == "rejected" and reply[0][1].startswith("LINK")
                  and ctrl_fake.presses == 5, "%s presses=%d" % (reply, ctrl_fake.presses))
            ctrl_fake.press_effect = "toggle"
            ctrl_fake.mode = "alarm"
            reply = panel.command("STBY\r\n")
            check("control: STBY is honoured while the amplifier alarms",
                  reply == [("ack", None)] and ctrl_fake.presses == 6 and ctrl_fake.mode == "standby", str(reply))
            ctrl_fake.mode = "alarm"          # alarm reported in operate state
            ctrl_fake.mode = "standby"
            ctrl_fake_alarm_standby = dict(canned_status("standby"))
            # An alarm while in standby: OPER must be refused without a press.
            saved = canned_status
            def alarmed_standby(mode, _saved=saved):
                live = _saved(mode)
                if mode == "standby":
                    live.update({"alarmCode": "S", "alarmsText": ["swr exceeding limits"],
                                 "activeAlarms": ["swr exceeding limits"]})
                return live
            globals()["canned_status"] = alarmed_standby
            try:
                reply = panel.command("OPER\r\n")
            finally:
                globals()["canned_status"] = saved
            check("control: OPER is refused while the amplifier reports an alarm",
                  len(reply) == 1 and reply[0][0] == "rejected" and reply[0][1].startswith("ALARM")
                  and ctrl_fake.presses == 6, "%s presses=%d" % (reply, ctrl_fake.presses))
            reply = panel.command("TUNE\r\n") + panel.command("BAND 20\r\n")
            check("control: TUNE and BAND stay refused with --allow-control",
                  len(reply) == 2 and all(k == "rejected" and p.startswith("READONLY") for k, p in reply),
                  str(reply))
            ctrl_fake.stop()
            reply = panel.command("OPER\r\n")
            check("control: with the amp server gone, OPER is ERR LINK and nothing is pressed",
                  len(reply) == 1 and reply[0][0] == "rejected" and reply[0][1].startswith("LINK"),
                  str(reply))
            panel.close()
        finally:
            ctrl.stop()

        seen = before + fake.requests
        check("read-only: the amp server saw only GET %s (%d requests)"
              % (STATUS_PATH, len(seen)),
              len(seen) > 20 and all(request == ("GET", STATUS_PATH) for request in seen),
              str(sorted(set(seen))))
        raw_ok = all(re.match(b"^([^\r\n]+\r\n)*$", client.raw) for client in clients)
        check("framing: every reply line ends with CR LF", raw_ok)
        check("driver: all %d reply lines parse under the Swift driver's rules"
              % DriverClient.lines_checked,
              DriverClient.lines_checked > 50 and not DriverClient.violations,
              "; ".join(DriverClient.violations[:3]))
    finally:
        for client in clients:
            client.close()
        bridge.stop()
        fake.stop()

    print("selftest: %d checks passed, %d failed" % (results["pass"], results["fail"]))
    return 0 if results["fail"] == 0 else 1


# --- Command line -------------------------------------------------------------

def parse_arguments(argv):
    parser = argparse.ArgumentParser(
        prog="expert-amp-bridge.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(
            "Present an SPE Expert amplifier, as seen by Expert Amp Server, to HermitSDR's\n"
            "\"Reference amplifier (line protocol)\" driver. Monitor-only by default: the\n"
            "bridge issues GET /api/v1/status and answers OPER/STBY/TUNE/BAND with ERR\n"
            "READONLY. With --allow-control, OPER and STBY press the amplifier's OPERATE\n"
            "key through the server and verify the result. It can never key a radio."),
        epilog=(
            "In HermitSDR: Station -> Control Devices -> Station Devices -> Add...,\n"
            "driver \"Reference amplifier (line protocol)\", link TCP, host = the machine\n"
            "running this bridge, port = --port, expected model blank.\n\n"
            "Values the server does not report are sent as \"-\". Lost or stale amplifier\n"
            "status raises the warning WLINK; it does not stop HermitSDR transmitting\n"
            "unless you start the bridge with --link-loss fault. An alarm reported by\n"
            "the amplifier itself always inhibits transmit in HermitSDR until it clears.\n"
            "Full protocol: docs/ReferenceAmplifierProtocol.md"))
    parser.add_argument("--amp-url", default="http://127.0.0.1:8088", metavar="URL",
                        help="Expert Amp Server base URL (default %(default)s)")
    parser.add_argument("--listen", default="127.0.0.1", metavar="ADDR",
                        help="address to listen on; use 0.0.0.0 when HermitSDR runs on "
                             "another machine (default %(default)s)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT,
                        help="TCP port for HermitSDR (default %(default)s)")
    parser.add_argument("--poll", type=float, default=1.0, metavar="SECONDS",
                        help="how often to read the amp server (default %(default)s)")
    parser.add_argument("--stale-after", type=float, default=3.0, metavar="SECONDS",
                        help="report values as unavailable when the last good status is "
                             "older than this (default %(default)s)")
    parser.add_argument("--http-timeout", type=float, default=2.0, metavar="SECONDS",
                        help="timeout for each amp-server socket operation (default %(default)s)")
    parser.add_argument("--link-loss", choices=("warning", "fault"), default="warning",
                        help="what to tell HermitSDR when amplifier status is lost (server "
                             "unreachable, amplifier off or silent): warning only warns, "
                             "fault also inhibits transmit while it lasts (default "
                             "%(default)s). Amplifier alarms are faults either way")
    parser.add_argument("--max-clients", type=int, default=4,
                        help="simultaneous HermitSDR connections (default %(default)s)")
    parser.add_argument("--client-idle", type=float, default=90.0, metavar="SECONDS",
                        help="close a connection that sends no command for this long "
                             "(default %(default)s; HermitSDR polls at least every 60 s)")
    parser.add_argument("--model", default=None,
                        help="model word to report in the ID line instead of the one "
                             "the amp server names")
    parser.add_argument("--verbose", action="store_true", help="log every command received")
    parser.add_argument("--selftest", action="store_true",
                        help="run against a built-in fake amp server and fake HermitSDR "
                             "driver, then exit (touches no real device)")
    parser.add_argument("--allow-control", action="store_true",
                        help="honour OPER and STBY from HermitSDR through Expert Amp Server's "
                             "OPERATE key as a verified toggle (read, press once if needed, "
                             "wait --control-settle, read again; one retry; ERR otherwise). "
                             "Off by default: the bridge then only watches")
    parser.add_argument("--control-settle", type=float, default=1.0, metavar="SECONDS",
                        help="how long to wait after pressing OPERATE before reading the "
                             "amplifier's state back (default %(default)s)")
    args = parser.parse_args(argv)
    if not (math.isfinite(args.control_settle) and 0 < args.control_settle <= 10):
        parser.error("--control-settle must be between 0 and 10 seconds")
    for name in ("poll", "stale_after", "http_timeout", "client_idle"):
        value = getattr(args, name)
        if not (math.isfinite(value) and value > 0):
            parser.error("--%s must be a positive number" % name.replace("_", "-"))
    if not 0 <= args.port <= 65535:
        parser.error("--port must be 0-65535")
    if args.max_clients < 1:
        parser.error("--max-clients must be at least 1")
    try:
        status_url(args.amp_url)
    except ValueError as error:
        parser.error(str(error))
    return args


def main(argv=None):
    args = parse_arguments(sys.argv[1:] if argv is None else argv)
    if args.selftest:
        return selftest()
    cfg = Config(amp_url=args.amp_url, listen=args.listen, port=args.port, poll=args.poll,
                 stale_after=args.stale_after, http_timeout=args.http_timeout,
                 link_loss=args.link_loss, max_clients=args.max_clients,
                 client_idle=args.client_idle, model=args.model, verbose=args.verbose,
                 allow_control=args.allow_control, control_settle=args.control_settle)
    try:
        bridge = Bridge(cfg)
    except OSError as error:
        sys.stderr.write("cannot listen on %s:%d: %s\n" % (cfg.listen, cfg.port, error))
        return 1
    stop = threading.Event()
    for name in ("SIGINT", "SIGTERM"):
        signal.signal(getattr(signal, name), lambda *_: stop.set())
    bridge.start()
    log("listening on %s:%d for HermitSDR; reading %s every %.1f s (%s)"
        % (cfg.listen, bridge.port, bridge.poller.url, cfg.poll,
           "OPER/STBY control enabled, verified toggle" if cfg.allow_control else "monitor-only"))
    if cfg.listen not in ("127.0.0.1", "::1", "localhost"):
        log("note: no authentication or encryption; keep this port on a trusted station LAN")
    try:
        while not stop.wait(0.5):
            pass
    finally:
        bridge.stop()
        log("stopped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
