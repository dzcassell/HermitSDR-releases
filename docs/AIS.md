# AIS ship tracking

`Decode ▸ AIS Vessels` decodes the Automatic Identification System that ships,
shore stations and navigation marks use on marine VHF. Both AIS channels are
decoded at once from the sampled span, wherever the dial sits inside it:

| Channel | Frequency | Marine channel |
|---|---|---|
| AIS 1 | 161.975 MHz | 87B |
| AIS 2 | 162.025 MHz | 88B |

Receive only. Nothing here transmits, and nothing is uploaded to any tracking
service. **Not verified on a real signal:** as of 2026-11-27 every test has
run on generated signals; no off-air recording was available.

## What you need

- A radio that tunes 162 MHz (today the SDRplay RSPdx, an rtl_tcp receiver or
  an Airspy), or a receive transverter profile that covers it. On any other
  radio the Decode menu and the command palette do not list AIS Vessels.
- A sampled span that contains the channels. The two are 50 kHz apart, so
  centre the span on **162.000 MHz** (the window's **Tune 162.000** button
  does this) at **96 kHz or more** for both. Every sample rate from 38.4 kHz
  to 20 MHz works; the dial can be anywhere as long as a channel, plus 7 kHz
  either side, lies inside the middle 94 % of the span.
- A span too narrow for both still decodes one: a 48 kHz span centred within
  about 15 kHz of one channel decodes that channel, and the status line says
  which. The 12 kHz audio path cannot carry AIS (9,600 bit/s needs more
  bandwidth than a voice channel's audio), so there is no audio-fed decoder.

Turn on **Decode** in the window. The switch is off until you turn it on and
is remembered. With it off, or with a span that holds neither channel, the
receiver takes no samples and costs nothing.

## The window

- **Vessels**, **Base Stations**, **Aids to Navigation** and **SAR / Distress**
  are separate tables: MMSI, name, call sign, type, flag, position, course and
  speed over ground, destination and ETA, time since last heard, message
  count, and distance and bearing from your station grid (Settings › Station).
  Click a column heading to sort. The flag is the administration that issued
  the MMSI (its Maritime Identification Digits), which is not always where
  the ship is.
- **Safety** lists safety-related broadcast text (Message 14).
- **Messages** lists the last 300 messages of every type, newest first, each
  with its `!AIVDM` sentences. Types that are not taken apart (binary
  messages, interrogations, assignments and the rest) are shown with their
  type name and length, and counted in the footer.
- **Search** filters the open table by MMSI, name, call sign, type, country,
  destination or status.
- **Export CSV…** saves every table in one file. Names and destinations are
  typed by a stranger and sent over the air: text cells are quoted, and one
  that a spreadsheet would run as a formula gets a leading apostrophe.
- A row is drawn dimmed after 10 minutes without a message and removed after
  an hour. The table holds at most 3,000 stations; the least recently heard
  goes first.

A ship sends its position every 2 to 10 seconds under way and every 3 minutes
at anchor, but its name, call sign and destination only every 6 minutes, so a
new row starts as a bare MMSI. Class B craft (yachts, small boats) send less
often and at lower power.

## On the map

`Log ▸ Propagation ▸ Stations Heard` gains an **AIS** layer once something
with a position has been heard: a pin per station, turned to its heading (or
course) when it is moving, a short track behind each moving vessel (at most
120 points; a point is added once the vessel has moved 25 metres and 20
seconds have passed; a jump faster than 120 knots starts a new track rather
than drawing a line), base stations and
aids to navigation with their own symbols. Pins fade once a station has been
silent for 10 minutes. The map shows the 300 most recently heard stations
and redraws at most every five seconds.

"Not available" values never reach the table as numbers or the map as a
position: latitude 91°, longitude 181°, speed 102.3 kn, course 360.0°,
heading 511, a time stamp of 60–63 and a rate of turn of −128 are all shown
as blank, and a position outside the globe is ignored.

## Sentences for a chart program

**NMEA Output…** sends each message as NMEA 0183 `!AIVDM` sentences
(checksummed, long messages split into numbered parts) so OpenCPN and
similar programs can plot the same ships. It is off until you turn it on.

- **UDP** sends datagrams to one address and port (default `127.0.0.1`,
  port 10110). In OpenCPN add a Network connection: protocol UDP, address
  `127.0.0.1`, the same port.
- **TCP** opens a server on the port for up to eight programs to connect to.
  Anything a client sends is discarded.
- **Allow LAN** lets a UDP destination be a private or link-local address on
  your network (10.x, 172.16–31.x, 192.168.x, 169.254.x) and lets TCP clients
  connect from other computers. Any other address is refused: this output
  cannot feed an Internet service. There is no login; anyone on the LAN who
  can reach the port sees what you decode.

A replayed recording is decoded but never forwarded as sentences or MQTT.

## Recordings and MQTT

- `Decode ▸ Decode a Recording` offers **AIS (both channels)** for an IQ
  recording (`.hiq`, Band DVR segment, SigMF or I/Q WAV) that contains either
  channel. Rows are stamped with the recording's clock. A recording made
  through a transverter uses the mapping saved in its header.
- With MQTT publishing on (`docs/MQTT.md`), each message is published on
  `decode/ais` with `mmsi`, `type`, `channel`, and the position, speed,
  course, heading, name and destination when known.

## How it works, and how well

Written from Recommendation ITU-R M.1371-5 (physical and link layer in
Annex 2, messages in Annex 8), Recommendation ITU-R M.585 and the ITU Table
of Maritime Identification Digits (MMSI formats and flags), and the public
"AIVDM/AIVDO protocol decoding" reference text
(<https://gpsd.gitlab.io/gpsd/AIVDM.html>) for the sentence layer and the
field tables. No other program's source code was read.

Each channel is shifted to 0 Hz and decimated to 48–96 kHz with a filter
whose length follows the decimation ratio (about 6.5 taps per output sample
for 70 dB, so 15 taps at 96 kHz and 831 at 6.144 MHz). It then passes through
five narrow filters 1 kHz apart, which is how a carrier up to about 2.5 kHz
off frequency is still decoded; a ship is allowed 500 Hz and an uncorrected
receiver may add more. In each filter an FM discriminator is followed by a
correlator for the end of the 24-bit training sequence and the start flag,
which gives the bit timing and the carrier offset for that one burst; the
bits are then sliced, NRZI and bit stuffing are undone, and the 16-bit frame
check is verified. A burst decoded in several filters is reported once. A
frame whose type and length do not belong together is dropped even when its
check passes.

Measured on generated signals (single-slot position reports on both channels,
random carrier offsets within ±600 Hz, white noise; Eb/N0 is the same number
as the signal-to-noise ratio in a 9.6 kHz bandwidth):

| Eb/N0 | Messages decoded |
|---|---|
| 10 dB | 28 % |
| 11 dB | 52 % |
| 12 dB | 80 % |
| 13 dB | 91 % |
| 14 dB | 98 % |
| 20 dB | 100 % |

The result is the same at every rate tried from 48 kHz to 10 MHz, and with a
second signal 40 dB stronger on the other channel. Thirty seconds of noise on
both channels produced one sync candidate and no message. This is an FM
discriminator receiver; a coherent GMSK receiver would do several decibels
better and is not built.

Cost, in an optimised build on an Apple M-series Mac, both channels: about
1.6 % of one core at 96–768 kHz, 2 % at 2.048 MHz and 4.5 % at 10 MHz. The
work runs on its own queue. The radio's receive thread only copies each block
into a bounded half-second inbox; if the worker falls behind, the block is
dropped and counted (shown in the status line) and the receiver starts afresh.

## Limits

- Not verified on a real signal (see the top of this page).
- No message is corrected: a burst with a single wrong bit is discarded.
- Two transmissions that overlap in the same slot are both lost unless one is
  much stronger.
- Binary messages (types 6, 8, 25, 26), which carry weather, lock and tide
  data, are counted and logged with their sentences but not taken apart.
- Type 27 long-range positions are coarse (a tenth of a minute).
- The Kenwood TH-D75's USB IF output is a 48 kHz span, so at most one
  channel fits (tune within about 15 kHz of it). Whether the radio's IF
  filter is wide enough for a 9,600 bit/s signal has not been tried.
- The receiver takes the sampled span as the radio delivers it; a receiver
  with a large frequency error (an uncorrected RTL dongle can be 5 kHz off at
  162 MHz) needs its ppm correction set first.
- Replaying a recording in the main window also feeds the receiver; its rows
  are stamped with the Mac's clock. Use Decode a Recording for the
  recording's own times.
- The flag table and the ship-type names are in the application; there is no
  ship database, photo or port lookup, and nothing is fetched.
