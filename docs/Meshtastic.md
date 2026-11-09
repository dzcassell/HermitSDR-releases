# Meshtastic receive integration

HermitSDR requests a snapshot from a selected TCP or USB Meshtastic node. The
default TCP port is 4403. For a USB device exposing the Meshtastic Protobuf
Client API, select its macOS callout port. The USB client uses 115200 baud,
allows the link to settle and sends the serial wake marker before the snapshot
request. It opens only the selected port.

A snapshot contains the local node number, discovered nodes, and decoded text
received before the matching snapshot-complete response. The node records
include names, position, battery level, voltage, signal-to-noise ratio and
hops when supplied. Received telemetry can add temperature, relative
humidity, pressure and hourly rainfall to the node record. Dated readings are ordered by the node's timestamps, separately for power
and environment. An older or undated packet cannot replace a dated reading.
JSON includes the reported Unix timestamps when known. Telemetry does not
drive station controls or TX interlocks. A battery value above 100 denotes external power in the
Meshtastic schema. Text is preserved as UTF-8. Encrypted payloads are skipped.

The client sends a local snapshot request and, on USB, the serial wake marker.
An open monitor sends a local Client API heartbeat after the snapshot and
every five minutes. That heartbeat is not a mesh packet.
Each received text offers **Copy to MAGNET Draft**. It preserves the mesh
sender ID, starts with Routine precedence, and leaves an existing draft
untouched. The operator reviews and sends from MAGNET through the existing
controls. Automatic forwarding, sensor actions, and mesh radio commands
are still tracked in issue #156. The current fixture exercises the protocol and timeout cleanup.
Run the command against a selected node:

```sh
/Applications/HermitSDR.app/Contents/MacOS/HermitSDR \
  --hermit-meshtastic-snapshot <node-host> [port]

/Applications/HermitSDR.app/Contents/MacOS/HermitSDR \
  --hermit-meshtastic-snapshot --usb /dev/cu.usbmodem123
```

The command prints the snapshot as JSON and closes the connection.
In the app, open **Station → Control Devices → Meshtastic Receive**. Choose
**TCP** and enter the node address, or choose **USB** and select the port.
Select **Read Snapshot** for one read or **Monitor** to keep the connection
open. **Nodes** shows current records, **Map** plots
reported positions with bundled artwork, including decoded position packets
that arrive while monitoring, and **Messages** retains the latest
128 decoded messages. Disconnect or close the window to
stop a monitor. Physical-node validation is pending.

## Alerts to the mesh

Issue #156, phase 1. With **Send alerts to mesh** on, HermitSDR hands short
texts to the connected node over the same Client API link the monitor uses,
and the node transmits them on its LoRa channel (an ISM band — 915 MHz in
Region 2, 868 MHz in Region 1 — under the node's own regional settings and
duty-cycle rules, not under the amateur licence that covers the HF side).
An operator in the field reads them in the Meshtastic phone app.

What is sent: one `ToRadio.packet` per alert — a `MeshPacket` to the
broadcast address or one node chosen from the snapshot, with the chosen
channel index, an optional ACK request, a random non-zero id and a
`Data { portnum TEXT_MESSAGE_APP, payload }`. The payload is one UTF-8 line
of at most 200 bytes, cut on a character boundary with "…", opening with a
tag and the UTC time, for example `SF 14:32 W1AW 7.074 FT8 POTA K-1234`.

Events that can become a text, each with its own toggle:

| Tag | Event |
| --- | --- |
| `NB` | The receiver's lightning-static warning (sustained broadband impulse crashes) |
| `CRAB` | A crab watch fires (callsign on the cluster, broadcaster on air, Kp, flare, scale, proton, SELCAL) |
| `WATCH` | A Receive Watch recipe detection: watch number, RF MHz and peak dBFS |
| `SF` | A SignalFind spot whose callsign, park/summit reference or program tag is on the **watch list** (`W1AW, K-1234, POTA, VK2*`; a trailing `*` matches a prefix) |
| `DX` | A Needed DX alert (a fresh opportunity reaching the board's alert threshold) |

Defaults and limits: the master toggle and every event are **off**. The
first time it is switched on a sheet says that the texts will be
transmitted by the node on the mesh; that acceptance is stored once, and
the master toggle is never restored as on across launches without it.
Alerts leave only while a **Monitor** session is open and has received
the snapshot; with the link closed they are dropped and counted, never
queued for a later reconnect. A token bucket allows one message per 30 s
with a burst of three; overflow is dropped and counted. A session cap
(200) stops sending with a visible notice until the next monitor session.
The window shows sent and dropped counters and the last line sent.

Airtime: every alert is one LoRa frame on the shared channel. At the
default LongFast preset a 200-byte text costs on the order of a second of
air time plus the rebroadcasts of every hop, so leave the rate limit alone
on a busy mesh, keep lines short, and prefer a directed destination with
no ACK when only one phone needs them.

Settings (destination, channel, ACK, events, watch list) persist per
station profile beside the other receive settings, with a shared copy for
stations without a profile. Nothing here touches the HF transmitter, the TX
coordinator or PTT. Inbound texts become commands only under the separate
**Mesh commands** toggle below.

## Commands from the mesh

Issue #156, phase 2. With **Mesh commands** on, a text that starts with `!`
from a node on the operator's **allowlist** is parsed by the viewer-chat
command gate (#151, `ViewerCommandParser`) and carried out through the
same receive-only executor the chat platforms use: tuning goes through
`setVFO(_, source: .remoteClient)` — the Control API's remote tuning
source — so dial lock, tuning history and CAT echo behave exactly as for
a deliberate remote request. The reply goes back to the sender node (never
to broadcast) on the channel index the command arrived on, through the
alerts link.

What is accepted:

| Text | Effect | Reply |
| --- | --- | --- |
| `!freq 7.074 [lsb]` (`!f`, `!qsy`, `!tune 7.074`) | Tune, optional mode | `Tuned to 7.074 MHz LSB` |
| `!mode USB` (`!m`) | Demodulator | `Mode USB at 7.074 MHz` |
| `!band 20m` (`!b`) | Band preset | `20 m → 14.200 MHz USB` |
| `!zoom 8` (`!z`) | Spectrum zoom, 1–32 | `Zoom ×8` |
| `!smeter` (`!s`) | Read only | `S9+10 (-63 dBm) at 7.074 MHz LSB` |
| `!status` (`!st`) | Read only | `7.074 MHz LSB · S9 · RX` |
| `!decodes` (`!dec`) | Read only: last five FT8/FT4 decodes | `Decodes: W1AW -3 7.074 \| …` |
| `!help` (`!h`, `!commands`) | — | the command list |

What is refused **with a reply**, by construction: every transmit word —
`!ptt`, `!tx`, `!transmit`, `!key`, `!unkey`, `!mox`, `!vox`, `!arm`,
`!disarm`, `!drive`, `!power`, `!cq`, `!send`, `!beacon` and a bare
`!tune` (the TUNE carrier; `!tune 7.074` is receiver tuning) — answers
`Refused: transmit controls are not available over the mesh (receive
only)`. The action vocabulary (`ViewerCommandAction`) has no transmit
member, so there is no code path from a mesh text to PTT, TUNE, ARM,
drive or any keying API. Any tuning or mode command is refused with
`Refused: radio is transmitting` while the transmitter is keyed, tuning,
two-toning, RF-hot or held by a digital program, and with `… (transmitter
armed)` while armed — an armed station may key by itself at the next FT8
slot or CAT request and must not be moved from the field. Read-only
questions and `!help` are still answered then. Unknown verbs and bad
arguments get the viewer-chat usage reply.

What is ignored **silently** (logged, no reply, no airtime): ordinary
conversation, texts from nodes not on the allowlist (an empty allowlist
means nobody), the connected node's own echoes, and texts addressed to the
broadcast address unless **Accept broadcast commands** is on (default
off). A node removed from the allowlist is refused from its next text on;
edits take effect immediately.

Defaults and limits: the master toggle is **off**, the allowlist is empty
and broadcast commands are not accepted. The first time the toggle is
switched on a sheet explains that allowlisted nodes will steer the
receiver and that replies are transmitted by the node; that acceptance is
stored once (separately from the alerts acceptance), and the toggle is
never restored as on across launches or station-profile restores without
it. Commands are judged only while a **Monitor** session is open and has
received the snapshot; a rebroadcast heard twice is deduplicated by packet
id and judged once. Replies share the alerts link, the one-message-per-30 s
token bucket (burst three) and the 200-per-session cap; when the bucket is
empty the command still runs and only the reply is dropped. The window
counts commands received / executed / refused / ignored and replies sent /
dropped, and logs every command with time, node, text and outcome (last
200). Settings (toggle, allowlist, broadcast opt-in) persist per station
profile beside the alert settings.

## Nodes as station devices

Every node a monitor session hears also appears under **Station → Control
Devices → Station Devices** in a **Mesh nodes** strip (#156 phase 2 on the
#84 framework): name and id, battery % (or external power), voltage,
temperature, relative humidity, pressure, hourly rain, SNR, hops, and when
the node was last heard. Each reading shows its age — the node's own
telemetry timestamp when it sent one, otherwise the time the packet
arrived — and a node silent for an hour (two default telemetry intervals)
greys out with a **STALE** chip. Up to 256 nodes are kept; a new snapshot
replaces the table, and records keep their ages after the link closes.

**Display only.** Mesh nodes are not `StationDeviceState`s: they never
enter `StationInterlockAggregate.reduce`, have no driver, transport,
session or commands, and the strip has no controls. A mesh sensor cannot
inhibit, warn or key anything — the inhibit-only coupling the issue
sketched for phase 2 was deliberately **not** built; a weather or door
sensor on an unlicensed mesh is not a trustworthy interlock input. The
remote-hardware (GPIO) antenna switching idea is likewise not built.

- [Meshtastic TCP setup](https://meshtastic.org/docs/software/android/user/desktop/#tcpip)
- [Meshtastic protobuf schema](https://github.com/meshtastic/protobufs/blob/85f3f4357946a52daa5310285476d2dffb137c7b/meshtastic/mesh.proto)
- [Meshtastic stream framing](https://github.com/meshtastic/python/blob/master/meshtastic/stream_interface.py)
- [Meshtastic Python serial client](https://python.meshtastic.org/serial_interface.html)

- [Meshtastic telemetry schema](https://github.com/meshtastic/protobufs/blob/master/meshtastic/telemetry.proto)
