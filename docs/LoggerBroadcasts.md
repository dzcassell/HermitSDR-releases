# Logger broadcasts — WSJT-X UDP protocol, N1MM contact packets and spectrum

*Settings ▸ Station ▸ Logger broadcasts.* Issues #267 and #422. Every feed is
**off by default** and nothing in them can key, arm or start a transmission.

HermitSDR can speak the UDP dialects that logging and map programs already
listen for:

| Feed | What goes out | Who listens | Default destination |
|---|---|---|---|
| **WSJT-X UDP protocol** | Heartbeat, Status, Decode (FT8 / FT4), Clear, QSO Logged, Logged ADIF, Close | GridTracker2, JT-Bridge, MacLoggerDX, RUMLogNG, JTAlert-style helpers, anything written against WSJT-X's `NetworkMessage.hpp` | `127.0.0.1:2237` (WSJT-X's own default) |
| **N1MM contact broadcasts** | `contactinfo` when a contact is logged, `contactreplace` when it is edited, `contactdelete` when it is removed | N1MM Logger+ and every N1MM-compatible logger (Log4OM, DXKeeper via its N1MM listener, …) | `127.0.0.1:12060` (N1MM's suggested port — the Palstar HF-AUTO `RadioInfo` feed uses the same one) |
| **Spectrum to logger** | The panadapter as `<Spectrum>` datagrams, about four a second (see [Spectrum to logger](#spectrum-to-logger)) | N1MM Logger+'s Spectrum Display window | `127.0.0.1:13064` (the only port N1MM+ listens on for spectrum) |

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
  hear it too; HermitSDR drops its own datagrams when they come back, so
  "in" counts only other programs. If a program insists on a unicast port,
  keep HermitSDR on unicast and let GridTracker2 forward.
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
heartbeat retries. If the socket cannot be opened at all (a name that does
not resolve yet, a busy port at login) the row shows `failed: …` and the
open is retried after 2, 5, 15, 30 and 60 s; after that it stays failed
until a setting changes or the switch is turned off and on.

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

## Spectrum to logger

Issue #422. *Spectrum to logger (N1MM Logger+ Spectrum Display)* sends what
the panadapter shows to a logger's own spectrum window, so the logger can
draw its spots and multipliers over the band and a click there tunes the
radio. It is a display feed: analyzer rows in, UDP datagrams out. Nothing
is read from that socket.

> **Not yet checked against N1MM Logger+.** The datagram is written from
> N1MM's manual and pinned by tests against that description. No copy of
> N1MM Logger+ and no datagram captured from Thetis, SmartSDR or CW Skimmer
> was available, so nobody has yet seen this feed drawn in a Spectrum
> Display window. What is still owed is listed under
> [Not verified](#not-verified).

### Setting it up with N1MM Logger+

1. In HermitSDR: Settings ▸ Station ▸ Logger broadcasts ▸ **Spectrum to
   logger**. *Send to* is the machine N1MM+ runs on and port **13064** —
   N1MM's manual says that is the only port it listens on for spectrum.
   For N1MM+ in a virtual machine or on a second PC enter that machine's
   address; `127.0.0.1` only reaches programs on this Mac (N1MM+ under
   CrossOver).
2. *Source* is the name N1MM+ will list (default `HermitSDR`).
3. In N1MM+ open a Spectrum Display window and, as its source, choose
   **"For all other radios, source named…"**; pick `HermitSDR` from the
   list. The manual says the list shows the sources N1MM+ is hearing, so
   the name appears only while HermitSDR is sending; it can also be typed.
4. In the same window choose **Radio 1** (or Radio 2) — the radio whose
   frequency the window follows and that a click tunes.
5. Click-to-tune needs no extra setting here. N1MM+ tunes the radio it has
   configured for that Radio number, through its ordinary radio control.
   Point that at HermitSDR's CAT: the [Kenwood CAT server](KenwoodCAT.md)
   (N1MM+'s PowerSDR or Kenwood radio type; TCP port 19090 or the serial
   pseudo-terminal) or the hamlib rigctl server on TCP 4532. HermitSDR
   then follows the click like any other CAT tune, and the next spectrum
   update shows the new window. On Windows N1MM+ wants a COM port, so a
   virtual-COM-to-TCP bridge sits in between; that pairing has not been
   tried here either.

The status row reads `sending (no acknowledgement in this protocol) to
host:port — "HermitSDR" 14000–14055 kHz, 475 points` when frames are going
out, with the number sent on the line below. It also says when there is nothing
to send (`waiting for a receiver`, `no spectrum is arriving`), when the
chosen segment is outside what the radio samples, and when the destination
answers that nothing is listening: `nothing is listening at host:port —
open the logger's Spectrum Display window and pick this source` (the
system reports this for a machine that is up but has no program on the
port).

**"Sending" is not "received".** The spectrum datagram is one-way UDP: the
logger never replies, and HermitSDR does not invent a reply to wait for. A
machine that is switched off, on another network or behind a firewall
answers nothing at all, which looks exactly like success — so the row says
`no acknowledgement in this protocol` every time it says `sending`, and the
sent count keeps rising either way. The only proof that frames arrive is
the logger's own Spectrum Display window. To see the datagrams yourself, run `nc -ul 13064` in Terminal
with *Send to* `127.0.0.1`.

### Settings

- **Span** — *Panadapter window* (default) sends what the panadapter
  shows and follows zoom and pan. *Whole receiver span* sends everything
  the radio samples. *Fixed segment* sends the same band segment whatever
  the zoom, as far as the receiver's span covers it; if the radio is
  tuned away from the segment nothing is sent and the status says so.
- **Updates per second** — 1 to 10, default 4. N1MM's manual calls about
  three a second adequate and asks for no more than five to ten.
- **Points** — at most 512, 1024 (default) or 2048 signal levels per
  update. A window with fewer analyzer bins than that sends its bins as
  they are. A wider one is reduced, each level taking the **strongest**
  bin it covers, so a narrow carrier keeps its height. N1MM's manual
  warns that a source whose points are more than 100 Hz apart may not find
  some signals: zoom in, or raise the points, on a wide span (384 kHz in
  1024 points is 375 Hz a point).
- **Also send SUB as a second source** — while SUB is on, its spectrum
  goes out as a second source named `<Source> SUB`. Open a second
  Spectrum Display window in N1MM+, pick that source and choose Radio 2.
  SUB has no zoom or pan of its own: in *Panadapter window* mode it sends
  a window as wide as the main one, centred on VFO B.

### What is sent

One UDP datagram per update, UTF-8, exactly this shape (levels shortened):

```xml
<?xml version="1.0" encoding="utf-8"?>
<Spectrum>
	<app>HermitSDR</app>
	<Name>HermitSDR</Name>
	<LowScopeFrequency>14000</LowScopeFrequency>
	<HighScopeFrequency>14055</HighScopeFrequency>
	<ScalingFactor>0.5</ScalingFactor>
	<DataCount>475</DataCount>
	<SpectrumData>71,70,72,…,69</SpectrumData>
</Spectrum>
```

- **Frequencies** are whole kHz of displayed RF (through the active
  transverter, like the dial). The window is widened outward to whole
  kHz and then cut back to the whole-kHz range the receiver has bins for,
  so the sent window can be up to 1 kHz wider than the panadapter on each
  side and every level comes from real data.
- **Levels**: the first level is at `LowScopeFrequency`, the last at
  `HighScopeFrequency`, the rest evenly between. Each is
  `(dBFS + 150) / 0.5`, rounded and limited to 0…999: 0 is −150 dBFS,
  300 is full scale. The dBFS values are the analyzer's — the same trace
  and averaging (Fast / Med / Slow / Peak) as the panadapter, and the same
  rows the time machine or a file replay shows.
- **Frequency accuracy**: the row geometry comes from the receiver's NCO
  (`centerHz`) and sample rate; zoom and pan (`displayCenterHz`) only
  choose which bins go out. Measured against the production analyzer
  (`N1MMSpectrumTests`): a tone lands on the level nearest its frequency,
  never more than one sent point away (worst 0.80 of a point over 93 tones
  at 48, 192 and 384 kHz, zoom ×1/×4/×16, centred and panned, with and
  without a transverter); where the window is not reduced that is within
  one analyzer bin (worst 0.60 bin). With a reduced window the error in
  hertz can be up to half a point's spacing.
- **Size**: up to 4 bytes a level plus about 300. The largest possible
  datagram (2048 levels) is 8,540 bytes, under macOS's 9,216-byte UDP
  limit. Above roughly 300 levels a datagram no longer fits one Ethernet frame and
  travels as IP fragments; on a lossy Wi-Fi link choose 512 points.
- After the radio's own centre frequency, sample rate or transverter
  changes (a band change, a tune outside the sampled span) the source
  pauses for 0.15 s, so rows that still hold the old span do not go out
  under the new frequencies. The new window is computed on the main
  thread just after the retune; an update made in the few milliseconds
  between the two could still carry the previous frequencies.

### Where each field comes from

Sources, read 2026-11-16 through an automated page reader (the quotations
are its extracts; reread the pages before relying on exact wording):

- **[M1]** N1MM Logger+ manual, *External UDP Messages* › "Sending
  Spectrum Data to N1MM+":
  <https://n1mmwp.hamdocs.com/appendices/external-udp-broadcasts/>.
  One XML sample and a few sentences of notes.
- **[M2]** N1MM Logger+ manual, *The Spectrum Display Window*:
  <https://n1mmwp.hamdocs.com/manual-windows/spectrum-display-window/>.
- **[T]** Two other programs' public write-ups of the same feed (the
  issue text of `Reid-n0rc/n1mm-scope-bridge` #1 and the description of
  `HagaleTechnologies/manta` pull request #478 on GitHub). Only the prose
  was read, no source code. Both say they worked from [M1] and neither
  reports a test against N1MM+, so they show how other readers understood
  the manual, not what N1MM+ does.

| Element | What the manual says | What HermitSDR sends | Rests on |
|---|---|---|---|
| UDP port | [M1] "N1MM+ receives spectrum data from SDR receivers on port 13064"; [M2] "The only port that N1MM+ will listen on is 13064" | default 13064 | two manual pages |
| `<?xml …?>`, `<Spectrum>`, element names and order | [M1] sample, introduced with "Follow this XML layout" | the sample's names, order, case and tab indentation | one sample |
| `app` | not described; the sample has `WaterfallBandmap`; [M1] speaks of "only requiring six pieces of metadata", which matches the six other elements | `HermitSDR` | **inference** — that N1MM+ does not require the sample's value. If it does, set the hidden default `loggerSpectrumApp` to `WaterfallBandmap` (`defaults write`) |
| `Name` | [M1] "Name is the name of your source. It will be shown in the N1MMPlus UI"; [M2] "Sources heard by the software will be shown as choices" | the *Source* setting, XML-escaped, at most 32 characters | two manual pages |
| `LowScopeFrequency`, `HighScopeFrequency` — meaning | [M1] "lowest / highest frequency represented by the signal levels in SpectrumData" | frequency of the first and of the last level | one source. Whether N1MM+ treats them as the first and last level or as the outer edges of the first and last cell is **inference**; the difference is half a point |
| — units | not stated; the sample has `14000` and `14055` | kHz | **inference** from the sample ([T] read it the same way) |
| — number format | not stated; the sample has whole numbers | whole numbers only, so nothing depends on N1MM+ accepting a fraction or on its decimal separator | one sample; sending whole kHz is the cautious reading |
| `ScalingFactor` | [M1] "a number that converts your 0-N data in SpectrumData to dB for display in the UI"; sample `0.3125` beside "Icom uses a range from 0-160" | `0.5`, always written with a point | one source. "dB per count" is **inference** (0.3125 × 160 = 50 dB fits it). Where 0 sits in absolute terms is not documented; [M2] has an adjustable noise floor in the window |
| `DataCount` | [M1] "the number of signal levels sent in SpectrumData"; sample 475 | the count of levels, 2…2048 | one source. No upper limit is documented; more than the sample's 475 is **untested** |
| `SpectrumData` | [M1] "comma separated signal level values", "We can accept integer values from 0-65535" | integers 0…999 separated by commas, one line, no spaces | one source. Lowest frequency first is **inference** (not stated). The sample wraps the list over several lines; whether a single line matters is unknown |
| Update rate | [M1] "Icom provides this data about 3x per second and that seems adequate", "We wouldn't want more than 5x to 10x per second" | 4 a second by default, 1–10 | one source |
| Datagram size | not documented | up to 8,540 bytes | nothing; N1MM+'s receive buffer size is unknown |

Not readable in this pass: the Apache Labs forum threads on Thetis's feed
(the connection dropped) and the N1MM groups.io thread "Spectrum display
UDP scaling" (the site wanted payment for automated access). Nothing from
them is used.

### Not verified

- **N1MM Logger+ itself.** No screenshot of a Spectrum Display window
  drawing this feed exists. Owed: N1MM+ lists the source; the frequency
  scale is right within one point at three spans (compare a known carrier
  against HermitSDR's own panadapter); levels look sensible with
  `ScalingFactor` 0.5; 1024 and 2048 points are accepted; `app` =
  `HermitSDR` is accepted; a click tunes HermitSDR through CAT; two
  windows show main and SUB as Radio 1 and 2.
- **Byte-level comparison with a known-good sender** (Thetis, a Flex,
  CW Skimmer). No capture was available; the tests pin the layout against
  the manual's sample instead.
- **DXLab Waterfall Bandmap.** Its public page documents Commander's
  network service ports (13063 directives, 13064 reports) but not that
  the Waterfall Bandmap accepts a `<Spectrum>` datagram from another
  program; in N1MM's sample it appears as a *sender*. No recipe is given.
- **A real second machine or VM**: fragmentation of the larger datagrams
  across a real network, and the "nothing is listening" status against a
  Windows host, were only exercised on loopback.

## Design notes

- `LoggerBroadcastCenter` (`@MainActor`, `Integration/LoggerBroadcasts/`)
  owns both feeds; RadioState installs itself as the `LoggerBroadcastPort`
  (`App/RadioState+LoggerBroadcasts.swift`) and feeds decodes, status
  snapshots and contacts. Sockets open only when a switch is on.
- Each feed is a `LoggerDatagramLink`: one BSD UDP socket owned by the
  `hermitsdr.logger` serial queue; `enqueue` pushes into a bounded queue
  (256) under a lock and never blocks, sends drain on the queue, and
  inbound datagrams are read on the queue and handed to the main actor as
  copies. Multicast destinations get `IP_MULTICAST_TTL` 1 and loopback;
  a reading multicast link remembers what it sent for 2 s
  (`LoggerEchoFilter`) and drops one byte-identical inbound copy of each.
  At most 64 inbound datagrams wait for the main actor
  (`LoggerInboundGate`); a sender faster than that loses the excess.
  A reading link that cannot join its group (no multicast route yet at
  login) fails the open with `cannot join …` and is retried like any other
  failed open.
- Settings keys: `loggerWSJTXOn`, `loggerWSJTXHost`, `loggerWSJTXPort`,
  `loggerWSJTXInbound`, `loggerN1MMOn`, `loggerN1MMHost`, `loggerN1MMPort`
  (they ride along in the Settings.plist mirror).
- Spectrum (#422): `LoggerSpectrumCenter` (`@MainActor`,
  `Integration/LoggerBroadcasts/LoggerSpectrumFeed.swift`) owns the
  settings, the status line and the plans; `N1MMSpectrumPlan`
  (`N1MMSpectrumBroadcast.swift`) is the pure window-and-resample rule and
  `N1MMSpectrumFrame` the encoder. RadioState is the `LoggerSpectrumPort`
  (`App/RadioState+LoggerBroadcasts.swift`): geometry from `centerHz`,
  the sample rate, `displayCenterHz` and the transverter, and taps on
  `RadioEngine.spectrumFanout` / `subSpectrumFanout`. The taps exist only
  while the switch is on and the socket is open. `LoggerSpectrumFeed.offer`
  runs on the DSP thread: a rate check under a lock, then — a few times a
  second — one pass over the window's bins and a push into a bounded
  buffer of 8 frames that discards its **oldest** frame when full. XML
  encoding and `send` run on the feed's own serial queue
  (`hermitsdr.logger.spectrum`) on a non-blocking connected UDP socket, so
  neither the DSP thread nor the main actor waits for the network. Being
  connected is what lets the system report "port unreachable".
  Settings keys: `loggerSpectrumOn`, `loggerSpectrumHost`,
  `loggerSpectrumPort`, `loggerSpectrumName`, `loggerSpectrumRate`,
  `loggerSpectrumSpan`, `loggerSpectrumSegmentLowKHz`,
  `loggerSpectrumSegmentHighKHz`, `loggerSpectrumPoints`,
  `loggerSpectrumSub`, and the hand-set `loggerSpectrumApp`.
- Not done yet: a Reply hand-off into the native sequencer (so GridTracker2
  can start the exchange behind ARM + ENABLE TX) is a transmit-path change
  and waits for the staged transmit review; today a Reply selects only.
