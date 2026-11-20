# KISS TNC over TCP (receive only)

HermitSDR can act as the receive half of a packet TNC. Settings › Station ›
**KISS TNC** runs a packet demodulator on the receiver's audio and offers
every AX.25 frame with a good checksum to other programs over TCP in KISS
framing — the interface APRS and packet software already uses with
sound-card TNCs, on the conventional port 8001. Off by default. Source
issue 417.

**Transmit is not available through this TCP service.** Programs can connect and read frames. Frames
they send (packets to transmit, TXDELAY and the other KISS settings) are
read, counted and discarded; nothing is keyed, queued or modulated, and no
code path leads from these ports to the transmitter. An APRS program will
plot what the receiver hears but its beacons and messages go nowhere, and
connected-mode software (Winlink packet, BBS, chat) cannot complete a
session, because a connection needs replies sent on the air. Packet
transmit through these TCP ports remains unavailable. The development
TH-D75 native packet console is a separate operator-armed USB TNC session;
it does not forward these clients or change their receive-only boundary.
See [TH-D75 USB data](KenwoodD75.md).

## Settings

| Field | Default | Meaning |
| --- | --- | --- |
| KISS TNC, 1200 Bd packet | off | Bell 202 AFSK, 1200 / 2200 Hz: VHF/UHF APRS and packet (FM), 6 m APRS on 50.620 MHz. |
| KISS TNC, 300 Bd packet | off | 200 Hz-shift AFSK, 1600 / 1800 Hz: HF packet and 30 m APRS (10.1476 MHz LSB). |
| Port | `8001` (1200 Bd), `8002` (300 Bd) | TCP port of that speed's listener, 1024–65535. The two must differ. |
| Centre | `1700` Hz | Audio frequency midway between the two tones, 800–2600 Hz. |
| Allow KISS clients from other machines | off | Listen on every network interface instead of `127.0.0.1`. |

Both speeds can run at once; each has its own port, so a program connects to
the speed it wants. The two demodulators listen to whatever the main
receiver is demodulating, so in practice one of them has something to hear
at a time: FM on a VHF channel for 1200 Bd, LSB or USB on HF for 300 Bd.
They are separate from the Digital Modes window's Packet decoder — that
window need not be open, and its speed picker does not affect these ports.
A demodulator runs only while its switch is on.

Each KISS frame is `C0 00 <AX.25 frame> C0` with the usual escapes
(`C0` → `DB DC`, `DB` → `DB DD`). The AX.25 bytes are exactly what was
received, address field to the last information byte, without flags or
checksum; frames that fail the checksum are never passed on. The KISS port
number in the type byte is always 0.

### Other machines on the network

With **Allow KISS clients from other machines** on, a program on another
computer connects to this Mac's address and the port. KISS has no password
and no encryption: anyone on the network who can reach the port sees every
frame the receiver decodes. They cannot tune the radio or make it transmit.
macOS may ask whether HermitSDR may accept incoming connections, and the
macOS firewall, if enabled, must allow it. A program on *this* Mac needs none
of that; leave the switch off and use `127.0.0.1`.

## Monitor

Under each switch, while it is listening:

- the address and port in use, or why it failed (most often: another
  program — Direwolf, for instance — already has the port);
- connected clients, frames decoded, and frame deliveries;
- one line per client: its address, frames sent to it, frames waiting;
- **Ignored: transmit not available** — how many frames clients sent us.
  They were discarded;
- clients closed for not reading.

Up to 8 clients per port. Each has its own queue of 256 frames with one
frame on the wire at a time. A client that stops reading is closed when its
queue fills; the others are not held up. TCP keepalive closes a client that
vanished without disconnecting (after about two minutes).

## Recipes

> **Not yet tried.** The three recipes below were written from each
> program's public documentation and from published how-to pages for
> Direwolf's port 8001, which this interface imitates. None has been run
> against YAAC, Xastir or Pat. Menu and field names may differ in your
> version. Corrections are welcome.

### YAAC as an APRS display

YAAC connects to a KISS-over-TCP server directly and expects port 8001.

1. In HermitSDR, turn on **KISS TNC, 1200 Bd packet** (or 300 Bd for 30 m)
   and tune to an APRS channel.
2. In YAAC: File → Configure → Expert Mode, **Ports** tab, **Add**, port
   type **KISS-over-TCP**.
3. Host `127.0.0.1`, port `8001` (`8002` for the 300 Bd port), KISS device
   ID 0. YAAC wants a callsign on the port before it will connect.
4. Leave the port's transmit option off. If it is on, YAAC will show its
   beacons as sent; HermitSDR discards them and counts them under
   "Ignored".

Stations should appear on YAAC's map as HermitSDR's "decoded" count rises.

### Xastir as an APRS display

Xastir's documented network TNC interface is AGWPE, which HermitSDR does not
offer. Its KISS interface expects a serial device, so the published approach
for a TCP KISS port is a virtual serial port made with `socat`:

```
socat pty,link=/tmp/hermit-kiss,raw tcp:127.0.0.1:8001 &
```

Then in Xastir: Interface → Interface Control → Add → **Serial KISS TNC**,
device `/tmp/hermit-kiss`, leave transmitting disallowed, and Start the
interface. If Xastir runs on another machine, use this Mac's address in the
`socat` line and turn on **Allow KISS clients from other machines**.

### Pat (Winlink) listening

Pat has no KISS-over-TCP engine of its own. Its packet support on Linux goes
through the kernel's AX.25 stack, which takes a KISS serial device, so the
same `socat` bridge applies, on a Linux machine, with **Allow KISS clients
from other machines** on in HermitSDR:

```
socat pty,link=/tmp/hermit-kiss,raw tcp:<this Mac's address>:8001 &
sudo kissattach /tmp/hermit-kiss wl2k
sudo axlisten -cart            # watch the frames HermitSDR decodes
pat --listen ax25 http         # Pat waiting for packet connections
```

`wl2k` is the port name from `/etc/ax25/axports` that Pat's `ax25` settings
refer to. What this gives you is monitoring: `axlisten` prints the traffic,
and Pat's listener is handed any connection request addressed to your call —
but it cannot answer, because the answer would have to be transmitted.
**No Winlink session can complete through HermitSDR in this build**, in
either direction.

## What was tested

- Framing against the KISS paper (Chepponis and Karn,
  <https://www.ka9q.net/papers/kiss.html>), including the escapes.
- Audio to bytes: AX.25 frames with known bytes, built in the test target
  from the AX.25 v2.2 specification (UI, UI response, SABM, an I frame with
  binary data), modulated at −80 dBFS by a test-only AFSK generator,
  demodulated by the app and read back by two TCP clients per port, both
  speeds running at once. The bytes read equal the frames built. The issue
  asked for a comparison with another TNC's decode of the same recording;
  none was available, so this stands in for it. There is no off-air
  recording in the tests.
- Two clients receive the same stream; a client that never reads is closed
  at its queue limit while the other receives every frame in order.
- 300 Bd in white noise, 100 different 95-byte APRS frames per level,
  S/N as signal power over noise power in 2.5 kHz: 100 of 100 at 10 dB and
  6 dB, 94 at 4 dB, 73 at 3 dB. The tests require 100, at least 98 and at
  least 90 for the first three. White noise only — no fading, multipath or
  mistuning, all of which a real HF channel adds.
- Frames sent by a client are counted and reach neither another client nor
  the decoded-frame count.

Not tested: any real packet program (see the recipes), any off-air signal
through these ports, a client on another machine, behaviour when macOS
denies incoming connections.

## Implementation

`Integration/KISS/KISSProtocol.swift` (framing, the inbound counter),
`Integration/KISS/KISSServer.swift` (the listener actor, the frame router
and `KISSTNCCenter`), `DSP/Digital/PacketTNCModems.swift` (the two
demodulators, fed from `DecoderEngineService.feed`),
`App/RadioState+KISS.swift` (wiring), `Views/KISSTNCSettingsRows.swift`.
Defaults keys: `kissTNC1200On`, `kissTNC300On`, `kissTNC1200Port`,
`kissTNC300Port`, `kissTNC1200CenterHz`, `kissTNC300CenterHz`,
`kissTNCAllowLAN`. Tests: `KISSProtocolTests`, `KISSServerTests`.
