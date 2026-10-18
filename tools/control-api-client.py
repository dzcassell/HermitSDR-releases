#!/usr/bin/env python3
"""HermitSDR Control API reference client (issue #122, docs/ControlAPI.md).

Python 3 standard library only: a minimal RFC 6455 WebSocket client over
`ssl`, certificate-fingerprint pinning, the pairing-code HMAC handshake,
state/meter printing, tuning, and an RX-audio dump to WAV. Written from the
protocol document alone — if this file and docs/ControlAPI.md disagree, the
document wins and this file has a bug.

  # first contact: shows the fingerprint, asks, remembers it
  tools/control-api-client.py shack.local --code AMFB-CGA7-…-VAMI

  # tune, change mode, record ten seconds of receiver audio
  tools/control-api-client.py shack.local --code … --tune 7074000 --mode USB \
      --audio 10 --wav rx.wav

  # watch state, meters and spectrum rows for 30 s
  tools/control-api-client.py shack.local --code … --watch 30 --spectrum 256

This client cannot transmit and neither can the server: `--probe-tx` sends a
reserved `ptt` message only to show the typed `tx_disabled` refusal.
"""
import argparse
import base64
import hashlib
import hmac
import json
import os
import socket
import ssl
import struct
import sys
import time
import uuid
import wave

SUBPROTOCOL = "hermitsdr-control.v1"
PATH = "/control/v1"
API_VERSION = 1
WS_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
PIN_FILE = os.path.expanduser("~/.hermitsdr-control-api.json")


class ProtocolError(Exception):
    pass


class WebSocket:
    """Just enough RFC 6455: client handshake, masked sends, fragmented
    receives, ping/pong and close. No extensions, no compression."""

    def __init__(self, sock):
        self.sock = sock
        self.buffer = b""
        self.closed = False

    def handshake(self, host, port):
        key = base64.b64encode(os.urandom(16)).decode()
        request = (
            f"GET {PATH} HTTP/1.1\r\nHost: {host}:{port}\r\nUpgrade: websocket\r\n"
            f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\n"
            f"Sec-WebSocket-Version: 13\r\nSec-WebSocket-Protocol: {SUBPROTOCOL}\r\n\r\n")
        self.sock.sendall(request.encode())
        while b"\r\n\r\n" not in self.buffer:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise ProtocolError("server closed during the WebSocket handshake")
            self.buffer += chunk
            if len(self.buffer) > 16384:
                raise ProtocolError("oversize HTTP response")
        head, self.buffer = self.buffer.split(b"\r\n\r\n", 1)
        lines = head.decode("latin-1").split("\r\n")
        if " 101 " not in lines[0] + " ":
            raise ProtocolError(f"WebSocket upgrade refused: {lines[0]}")
        headers = {k.strip().lower(): v.strip() for k, v in
                   (line.split(":", 1) for line in lines[1:] if ":" in line)}
        expected = base64.b64encode(hashlib.sha1((key + WS_GUID).encode()).digest()).decode()
        if headers.get("sec-websocket-accept") != expected:
            raise ProtocolError("bad Sec-WebSocket-Accept")
        if headers.get("sec-websocket-protocol") != SUBPROTOCOL:
            raise ProtocolError("server did not select " + SUBPROTOCOL)

    def _send(self, opcode, payload):
        header = bytes([0x80 | opcode])
        n = len(payload)
        if n < 126:
            header += bytes([0x80 | n])
        elif n < 65536:
            header += bytes([0x80 | 126]) + struct.pack(">H", n)
        else:
            header += bytes([0x80 | 127]) + struct.pack(">Q", n)
        mask = os.urandom(4)
        masked = bytes(b ^ mask[i & 3] for i, b in enumerate(payload))
        self.sock.sendall(header + mask + masked)

    def send_text(self, text):
        self._send(0x1, text.encode())

    def send_binary(self, data):
        self._send(0x2, data)

    def close(self, code=1000):
        if not self.closed:
            self.closed = True
            try:
                self._send(0x8, struct.pack(">H", code))
            except OSError:
                pass

    def _read(self, n):
        while len(self.buffer) < n:
            chunk = self.sock.recv(65536)
            if not chunk:
                raise EOFError
            self.buffer += chunk
        out, self.buffer = self.buffer[:n], self.buffer[n:]
        return out

    def receive(self):
        """Returns ("text", str) | ("binary", bytes) | ("close", code)."""
        message, kind = b"", None
        while True:
            b0, b1 = self._read(2)
            fin, opcode, n = b0 & 0x80, b0 & 0x0F, b1 & 0x7F
            if n == 126:
                n = struct.unpack(">H", self._read(2))[0]
            elif n == 127:
                n = struct.unpack(">Q", self._read(8))[0]
            if n > (1 << 20):
                raise ProtocolError("oversize frame")
            mask = self._read(4) if b1 & 0x80 else None
            payload = self._read(n)
            if mask:
                payload = bytes(b ^ mask[i & 3] for i, b in enumerate(payload))
            if opcode == 0x9:
                self._send(0xA, payload)
                continue
            if opcode == 0xA:
                continue
            if opcode == 0x8:
                code = struct.unpack(">H", payload[:2])[0] if len(payload) >= 2 else 1005
                self.close(code)
                return "close", code
            if opcode in (0x1, 0x2):
                kind = "text" if opcode == 0x1 else "binary"
            message += payload
            if fin:
                return (kind, message.decode()) if kind == "text" else (kind, message)


def decode_pairing_code(code):
    clean = code.upper().replace("-", "").replace(" ", "")
    if len(clean) != 32:
        raise SystemExit("the pairing code is 32 base32 characters (8 groups of 4)")
    return base64.b32decode(clean)


def fingerprint_of(der):
    return ":".join(f"{b:02X}" for b in hashlib.sha256(der).digest())


def load_pins():
    try:
        with open(PIN_FILE) as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return {}


def save_pin(key, fingerprint):
    pins = load_pins()
    pins[key] = fingerprint
    with open(PIN_FILE, "w") as handle:
        json.dump(pins, handle, indent=1)
    os.chmod(PIN_FILE, 0o600)


def connect(args):
    raw = socket.create_connection((args.host, args.port), timeout=10)
    raw.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    if args.insecure_plaintext:
        if args.host not in ("127.0.0.1", "::1", "localhost"):
            raise SystemExit("--insecure-plaintext is for the loopback conformance smoke only")
        return raw
    # The certificate is self-signed on purpose: trust comes from the pinned
    # SHA-256 fingerprint, never from a CA or the certificate's names.
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    tls = context.wrap_socket(raw, server_hostname=args.host)
    seen = fingerprint_of(tls.getpeercert(binary_form=True))
    key = f"{args.host}:{args.port}"
    pinned = args.fingerprint.upper() if args.fingerprint else load_pins().get(key)
    if pinned is None:
        print(f"Server certificate fingerprint (compare with Settings ▸ Control API):\n  {seen}")
        if args.trust_first_use or input("Trust and remember it? [y/N] ").strip().lower() == "y":
            save_pin(key, seen)
        else:
            raise SystemExit(3)
    elif pinned != seen:
        print(f"CERTIFICATE MISMATCH for {key}\n  pinned {pinned}\n  seen   {seen}\n"
              "Refusing to continue. If the shack really rotated its identity, remove the pin.",
              file=sys.stderr)
        raise SystemExit(3)
    return tls


class Session:
    def __init__(self, ws, token, args):
        self.ws = ws
        self.token = token
        self.args = args
        self.state = {}
        self.welcome = None
        self.next_id = 1
        self.meters = 0
        self.audio = bytearray()
        self.audio_frames = 0
        self.audio_gaps = 0
        self.last_audio_seq = None
        self.spectrum_rows = 0
        self.last_meter = None
        self.errors = []

    def send(self, message):
        message = dict(message)
        message["id"] = self.next_id
        self.next_id += 1
        self.ws.send_text(json.dumps(message, separators=(",", ":")))
        return message["id"]

    def pair(self):
        hello = json.dumps({
            "t": "hello", "apiVersion": API_VERSION, "clientId": self.args.client_id,
            "name": self.args.name, "platform": self.args.platform,
            "features": ["control", "audio", "spectrum"]}, separators=(",", ":"))
        self.ws.send_text(hello)
        kind, challenge = self.ws.receive()
        if kind != "text":
            raise ProtocolError("expected a challenge")
        body = json.loads(challenge)
        if body.get("t") == "denied":
            raise SystemExit(f"denied: {body.get('code')} — {body.get('message')}")
        if body.get("t") != "challenge":
            raise ProtocolError(f"expected challenge, got {body.get('t')}")
        nonce = base64.b64decode(body["nonce"])
        # The exact bytes that crossed the wire, joined by one LF.
        transcript = hashlib.sha256(hello.encode() + b"\n" + challenge.encode()).digest()
        answer = hmac.new(self.token, nonce + transcript, hashlib.sha256).digest()
        self.ws.send_text(json.dumps({"t": "auth", "answer": base64.b64encode(answer).decode()}))
        kind, reply = self.ws.receive()
        body = json.loads(reply) if kind == "text" else {}
        if body.get("t") == "denied":
            print(f"denied: {body.get('code')} — {body.get('message')}", file=sys.stderr)
            raise SystemExit(2)
        if body.get("t") != "welcome":
            raise ProtocolError(f"expected welcome, got {body.get('t')}")
        self.welcome = body
        return body

    def handle(self, kind, payload, verbose=False):
        if kind == "close":
            return False
        if kind == "binary":
            self.handle_binary(payload)
            return True
        body = json.loads(payload)
        t = body.get("t")
        if t == "state":
            if body.get("full"):
                self.state = {}
            for key, value in body["s"].items():
                if value is None:
                    self.state.pop(key, None)
                else:
                    self.state[key] = value
            if verbose and not body.get("full"):
                print("  state Δ " + json.dumps(body["s"], sort_keys=True))
        elif t == "meter":
            self.meters += 1
            self.last_meter = body
        elif t == "error":
            self.errors.append(body)
            print(f"  error {body.get('code')}: {body.get('message')}")
        elif t == "bye":
            print(f"  bye {body.get('code', '')}: {body.get('message')}", flush=True)
            return False
        elif verbose and t in ("ack", "subscribed", "pong"):
            print("  " + json.dumps(body, sort_keys=True))
        return True

    def handle_binary(self, data):
        if not data:
            return
        if data[0] == 0x01 and len(data) >= 16:
            codec, flags, seq, rate, channels, count = struct.unpack_from("<xBHIIHH", data, 0)
            if codec != 0 or len(data) != 16 + 2 * count:
                return
            if self.last_audio_seq is not None and seq != (self.last_audio_seq + 1) & 0xFFFFFFFF:
                self.audio_gaps += 1
            self.last_audio_seq = seq
            self.audio_frames += 1
            self.audio_rate = rate
            self.audio += data[16:]            # already int16 little-endian: WAV-ready
        elif data[0] == 0x02 and len(data) >= 40:
            _fmt, _flags, _seq, center, span, bins, _r, min_db, step_db, dbm_offset = \
                struct.unpack_from("<xBHIddHHfff", data, 0)
            values = data[40:40 + bins]
            self.spectrum_rows += 1
            if self.args.verbose and values:
                peak = max(range(len(values)), key=values.__getitem__)
                hz = center - span / 2 + (peak + 0.5) * span / len(values)
                print(f"  spectrum {len(values)} bins, {center/1e6:.4f} MHz ±{span/2e3:.0f} kHz, "
                      f"peak {min_db + values[peak] * step_db + dbm_offset:.0f} dBm at {hz/1e6:.4f} MHz")
        # Unknown frame types are ignored (docs § 6).

    def pump(self, seconds, verbose=False):
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            self.ws.sock.settimeout(max(0.05, deadline - time.monotonic()))
            try:
                kind, payload = self.ws.receive()
            except (socket.timeout, TimeoutError):
                break
            except EOFError:
                return False
            if not self.handle(kind, payload, verbose):
                return False
        return True


def describe(state):
    if not state.get("connected"):
        return "no radio session"
    flags = [name.upper() for name in ("nr", "nb", "anf", "split", "muted") if state.get(name)]
    return (f"{state.get('rfHz', 0) / 1e6:.6f} MHz {state.get('mode')} "
            f"filter {state.get('filterWidthHz')} Hz  AGC {state.get('agc')}  "
            f"RF {state.get('rfGainDb')} dB  ATT {state.get('attDb')} dB  "
            f"vol {state.get('volume')}  band {state.get('band')}  {' '.join(flags)}".rstrip())


def main():
    parser = argparse.ArgumentParser(description="HermitSDR Control API reference client")
    parser.add_argument("host")
    parser.add_argument("--port", type=int, default=4996)
    parser.add_argument("--code", required=True, help="pairing code from Settings ▸ Control API")
    parser.add_argument("--fingerprint", help="pin this certificate fingerprint (AA:BB:…)")
    parser.add_argument("--trust-first-use", action="store_true",
                        help="remember the certificate without asking (first contact only)")
    parser.add_argument("--client-id", default=None)
    parser.add_argument("--name", default=f"control-api-client.py on {socket.gethostname()}"[:64])
    parser.add_argument("--platform", default=sys.platform,
                        help="hello.platform (\"browser\" is what the web console sends and what its session policy keys on)")
    parser.add_argument("--tune", type=float, metavar="HZ")
    parser.add_argument("--step", type=int, metavar="STEPS")
    parser.add_argument("--band")
    parser.add_argument("--mode")
    parser.add_argument("--filter", type=float, metavar="HZ")
    parser.add_argument("--filter-preset", type=int, metavar="INDEX",
                        help="pick the Nth width the mode offers (radio.filters, revision 1)")
    parser.add_argument("--vfo-b", type=float, metavar="HZ", help="set VFO B (revision 1)")
    parser.add_argument("--rf-gain", type=float, metavar="DB")
    parser.add_argument("--audio", type=float, metavar="SECONDS", help="record receiver audio")
    parser.add_argument("--wav", default="hermitsdr-rx.wav")
    parser.add_argument("--spectrum", type=int, metavar="BINS", help="subscribe to spectrum rows")
    parser.add_argument("--watch", type=float, metavar="SECONDS", default=0)
    parser.add_argument("--probe-tx", action="store_true",
                        help="send the always-refused arm message to show tx_disabled")
    parser.add_argument("--json", action="store_true", help="print the final state as JSON")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--insecure-plaintext", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.client_id is None:
        pins = load_pins()
        args.client_id = pins.get("clientId") or str(uuid.uuid4())
        if "clientId" not in pins and not args.insecure_plaintext:
            save_pin("clientId", args.client_id)

    token = decode_pairing_code(args.code)
    ws = WebSocket(connect(args))
    ws.handshake(args.host, args.port)
    session = Session(ws, token, args)
    welcome = session.pair()
    radio = welcome["radio"]
    print(f"paired with {welcome['server']['app']} {welcome['server']['version']} — "
          f"{radio['name']} ({radio['link']}, {radio['sampleRateHz']} Hz), "
          f"granted: {', '.join(welcome['granted'])}")
    revision = welcome.get("apiRevision", 0)
    session.pump(0.5)
    print("state: " + describe(session.state))
    presets = radio.get("filters", {}).get(session.state.get("mode", ""), {}).get("presetsHz")
    if presets:
        chosen = session.state.get("filterPreset")
        print(f"filter presets for {session.state.get('mode')}: "
              + ", ".join(f"[{i}] {hz} Hz" + (" *" if i == chosen else "") for i, hz in enumerate(presets)))
    if revision < 1 and (args.vfo_b is not None or args.filter_preset is not None):
        print(f"this server is revision {revision}: it will answer --vfo-b / --filter-preset "
              "with unknown_message", file=sys.stderr)

    commands = []
    if args.band:
        commands.append({"t": "setBand", "band": args.band})
    if args.mode:
        commands.append({"t": "setMode", "mode": args.mode})
    if args.tune is not None:
        commands.append({"t": "tune", "hz": args.tune})
    if args.step:
        commands.append({"t": "tuneStep", "steps": args.step})
    if args.filter:
        commands.append({"t": "setFilter", "widthHz": args.filter})
    if args.filter_preset is not None:
        commands.append({"t": "setFilterPreset", "index": args.filter_preset})
    if args.vfo_b is not None:
        commands.append({"t": "setVFOB", "hz": args.vfo_b})
    if args.rf_gain is not None:
        commands.append({"t": "setRFGain", "db": args.rf_gain})
    for command in commands:
        session.send(command)
    if args.probe_tx:
        session.send({"t": "arm", "on": True})
    if commands or args.probe_tx:
        session.pump(0.6, verbose=True)
        print("state: " + describe(session.state))

    subscription = {"t": "subscribe"}
    if args.audio:
        subscription["audio"] = True
    if args.spectrum:
        subscription["spectrum"] = {"enabled": True, "bins": args.spectrum, "rowsPerSec": 5}
    duration = max(args.audio or 0, args.watch)
    if len(subscription) > 1:
        session.send(subscription)
    if duration > 0:
        alive = session.pump(duration, verbose=args.verbose)
        if session.last_meter:
            print(f"meter: {session.last_meter['sMeterDbm']} dBm ({session.last_meter['sUnits']}), "
                  f"{session.meters} meter messages")
        if args.spectrum:
            print(f"spectrum: {session.spectrum_rows} rows")
        if args.audio:
            with wave.open(args.wav, "wb") as out:
                out.setnchannels(1)
                out.setsampwidth(2)
                out.setframerate(getattr(session, "audio_rate", 12000))
                out.writeframes(bytes(session.audio))
            print(f"audio: {session.audio_frames} frames, {len(session.audio) // 2} samples, "
                  f"{session.audio_gaps} gaps → {args.wav}")
        if not alive:
            print("server closed the session")
    if args.json:
        print(json.dumps(session.state, indent=1, sort_keys=True))
    if not ws.closed:
        ws.send_text('{"t":"bye"}')
        ws.close(1000)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ProtocolError as error:
        print(f"protocol error: {error}", file=sys.stderr)
        sys.exit(1)
    except (OSError, EOFError) as error:
        print(f"connection failed: {error}", file=sys.stderr)
        sys.exit(1)
