# Logger broadcasts — WSJT-X UDP protocol and N1MM contact packets

*Settings ▸ Station ▸ Logger broadcasts.* Issue #267. Both feeds are **off by
default** and nothing in them can key, arm or start a transmission.

HermitSDR can speak the two UDP dialects that logging and map programs
already listen for:

| Feed | What goes out | Who listens | Default destination |
|---|---|---|---|
| **WSJT-X UDP protocol** | Heartbeat, Status, Decode (FT8 / FT4), Clear, QSO Logged, Logged ADIF, Close | GridTracker2, JT-Bridge, MacLoggerDX, RUMLogNG, JTAlert-style helpers, anything written against WSJT-X's `NetworkMessage.hpp` | `127.0.0.1:2237` (WSJT-X's own default) |
| **N1MM contact broadcasts** | `contactinfo` when a contact is logged, `contactreplace` when it is edited, `contactdelete` when it is removed | N1MM Logger+ and every N1MM-compatible logger (Log4OM, DXKeeper via its N1MM listener, …) | `127.0.0.1:12060` (N1MM's suggested port — the Palstar HF-AUTO `RadioInfo` feed uses the same one) |

The FT8/FT4 decodes come from the native decode panel (the control-bar FT8 /
FT4 toggle). The Digital Modes window's JS8 decoder is never sent as a WSJT-X
decode. Logged contacts come from every way a contact enters the QSO log —
the native FT8 sequencer, **LOG IT**, the Crab's "log W1AW", the logbook
editor — each exactly once. An ADIF import or a backup restore is a bulk
restore, not fresh contacts, and is not broadcast.

## Pointing a program at HermitSDR

Set the program's "WSJT-X UDP server" / "listen" address to the address and
port HermitSDR sends to. If the program *also* needs to talk to the radio
(GridTracker2's "reply", loggers that tune), it does so through this same
UDP feed; CAT for the logger itself is still the hamlib rigctl or
[Kenwood CAT](KenwoodCAT.md) server.

- **GridTracker2** — in its WSJT-X / JTDX UDP settings, listen on port
  **2237** at **127.0.0.1** (or the multicast group below); its own
  "forward UDP" option can pass the same stream on to another program. Turn
  on *Act on Reply / Halt Tx from the logger* in HermitSDR if a click in
  GridTracker2's call roster should select that station in the FT8 panel.
- **JT-Bridge** — set its WSJT-X UDP port to **2237**; JT-Bridge then hands
  the logged QSO on to MacLoggerDX / RUMlogNG / Aether as usual.
- **MacLoggerDX** — enable its WSJT-X / JTDX UDP listener on **2237**;
  logged QSOs arrive from the QSO Logged / Logged ADIF messages and decodes
  appear in its WSJT-X panel.
- **RUMlogNG** — enable its WSJT-X UDP listener on **2237**, exactly as for
  WSJT-X itself.
- **Several programs at once** — give HermitSDR a multicast group such as
  `239.255.0.1:2237` and set every program to the same group. Multicast is
  sent with TTL 1 (this LAN only) and loopback on, so programs on this Mac
  hear it too. If a program insists on a unicast port, keep HermitSDR on
  unicast and let GridTracker2 forward.
- **N1MM Logger+ / N1MM-compatible loggers** — enable the logger's inbound
  "N1MM contact info" UDP listener on **12060** (the option is named after
  N1MM in most general loggers). HermitSDR's `contestname` is `DX` and
  `contestnr` is `1`; `ID` is the contact's logbook identifier (32 hex
  characters), so edits and deletions address the same record.

Address and port are applied with **Apply** or Return. The status row shows
`sending to host:port (unicast|multicast)`, how many datagrams went out,
how many came in, and dropped / failed counts. A dropped datagram means the
bounded send queue (256 datagrams) was full — a map program that stalls
for several slots loses the newest decodes, never the application's
real-time paths. `failed` is a socket error (host unreachable); the next
heartbeat retries.

## What each WSJT-X message carries

Every datagram follows the public layout in WSJT-X's
`Network/NetworkMessage.hpp`
(<https://sourceforge.net/p/wsjt/wsjtx/ci/master/tree/Network/NetworkMessage.hpp>,
read 2026-10-22): magic `0xadbccbda`, schema **2**, the message type, the
client Id `HermitSDR`, then the fields in the documented order using
QDataStream (Qt_5_2) big-endian types — `quint32`/`quint64`/`qint32`,
one-byte `bool`, `float` serialized as a double, utf8 strings as
`QByteArray` (count + bytes, `0xffffffff` for null, `0` for empty), `QTime`
as milliseconds since UTC midnight and `QDateTime` as Julian day +
milliseconds + timespec 1 (UTC). The field order is the one
`MessageClient.cpp` emits
(<https://sourceforge.net/p/wsjt/wsjtx/ci/master/tree/Network/MessageClient.cpp>).
The encoder is HermitSDR's own (`Integration/LoggerBroadcasts/WSJTXMessage.swift`);
`LoggerBroadcastTests` pins every message against hand-built byte fixtures.

- **Heartbeat (0)** every 15 s, as WSJT-X does, with the app version.
- **Status (1)** whenever the picture changes (checked once a second and
  after every decode slot): dial frequency (the displayed RF dial), mode
  `FT8`/`FT4`, DX call (the addressee of the queued native TX message, if
  any), Tx enabled (the panel's ENABLE TX), transmitting, decoding, Rx/Tx DF
  (the TX audio offset), DE call/grid (Settings ▸ Station), T/R period
  (15, or 7 for FT4 — WSJT-X sends whole seconds), configuration name
  `Default`, the queued TX message.
- **Decode (2)** per decoded line: slot time, S/N, DT, audio offset, the
  mode column character (`~` FT8, `+` FT4 — the same character WSJT-X puts
  in a decoded line and sends in this field), the message text. A
  time-machine or file replay decode is flagged *Off air*.
- **Clear (3)** when the decode panel's Clear button empties the list.
- **QSO Logged (5)** and **Logged ADIF (12)** for every contact as it is
  committed: DX call/grid, TX frequency, mode, reports, name/comment if the
  record has them, your call/grid, and the logbook's own ADIF record
  wrapped as a one-record ADIF file (`<programid:8>HermitSDR`).
- **Close (6)** when the feed is switched off or the app quits.

### Inbound: Reply (4), Halt Tx (8), Replay (7)

The WSJT-X socket is read as well as written (unicast: the program answers
to HermitSDR's source port; multicast: HermitSDR joins the group). Every
inbound datagram is parsed with bounds checks; a malformed one (bad magic,
schema other than 2 or 3, truncated, bad UTF-8, unknown type) is counted
and shown as a receipt, never acted on.

- **Reply** — GridTracker2's "call this station". WSJT-X acts only when the
  message exactly describes a prior decode; HermitSDR applies the same rule
  (mode character, slot time, S/N, audio offset ±1 Hz, text) against the
  decode panel's list and then does **what a click on that row does**:
  tunes the dial to the signal (`tuneToFT8Spot`). While the native
  sequencer, beacon or a frame program is running the dial is frozen and
  the receipt says so. It never calls the sequencer's Reply, never enables
  TX, never arms. If you want the station answered, use the panel's Reply
  button with ARM + ENABLE TX as always. A Reply that arrives while the
  transmitter is disarmed is therefore selected-only, and the receipt
  says "TX is not armed; nothing transmits".
- **Halt Tx** — presses the panel's **STOP** (`ft8StopTX`, the existing
  abort through the coordinator release). "Auto Tx only" is honoured in
  the only way the native sequencer can: STOP.
- **Replay** — re-sends the panel's decodes with *New* false, then a Status.
- Heartbeat, Clear and Close from the program are noted in the receipt
  line; Free Text, Location, Highlight Callsign, Switch Configuration,
  Configure and Annotation are recognised and ignored (the protocol asks
  for silent ignoring of unknown types; these are known but unsupported).

Both actions sit behind *Act on Reply / Halt Tx from the logger*, off by
default. With it off, inbound datagrams are parsed, counted and receipted
only. The last Reply/Halt is also published as `LoggerBroadcastCenter.lastInbound`
for any future hand-off to the sequencer that goes through the transmit
review.

## N1MM contact packets

Element names and order follow the N1MM Logger+ documentation, *External
UDP Messages* (<https://n1mmwp.hamdocs.com/appendices/external-udp-broadcasts/>,
read 2026-10-22). `rxfreq`/`txfreq` are in 10 Hz units, `band` is the MHz
label (`3.5`, `7`, `14`, …, always with a point), `timestamp` is UTC
`yyyy-MM-dd HH:mm:ss`, `mode` uses N1MM's tokens (SAM → AM, NFM → FM,
DATA-U → USB, DATA-L → LSB), booleans are `True`/`False`. The page prints
`exchangel` and `ismultiplierl` with a letter L; the packets use the digit
forms `exchange1` / `ismultiplier1` that real N1MM packets carry. Fields
HermitSDR does not keep (contest scoring, zones, sections, N1MM network
fields) are sent as N1MM's neutral defaults so a positional parser sees
every element. `contactreplace` carries `oldtimestamp` / `oldcall` from
the record before the edit.

## Design notes

- `LoggerBroadcastCenter` (`@MainActor`, `Integration/LoggerBroadcasts/`)
  owns both feeds; RadioState installs itself as the `LoggerBroadcastPort`
  (`App/RadioState+LoggerBroadcasts.swift`) and feeds decodes, status
  snapshots and contacts. Sockets open only when a switch is on.
- Each feed is a `LoggerDatagramLink`: one BSD UDP socket owned by the
  `hermitsdr.logger` serial queue; `enqueue` pushes into a bounded queue
  (256) under a lock and never blocks, sends drain on the queue, and
  inbound datagrams are read on the queue and handed to the main actor as
  copies. Multicast destinations get `IP_MULTICAST_TTL` 1 and loopback.
- Settings keys: `loggerWSJTXOn`, `loggerWSJTXHost`, `loggerWSJTXPort`,
  `loggerWSJTXInbound`, `loggerN1MMOn`, `loggerN1MMHost`, `loggerN1MMPort`
  (they ride along in the Settings.plist mirror).
- Not done yet: a Reply hand-off into the native sequencer (so GridTracker2
  can start the exchange behind ARM + ENABLE TX) is a transmit-path change
  and waits for the staged transmit review; today a Reply selects only.
