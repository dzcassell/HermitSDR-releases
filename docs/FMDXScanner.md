# FM DX Catalog and band scan

RDS is the FM DXer's spotter: when Sporadic-E or tropospheric ducting
opens the VHF band, a distant broadcaster's programme service name, PI
code and RadioText identify it in a second or two, long before anyone
could recognise the programme. **Radio → FM DX Catalog…** (also the list
button beside the WFM chips) is a running log of every station whose RDS
this receiver has decoded, most recent first, with a band scan that keeps
it fresh. Receive only; the transmitter is never touched and nothing is
downloaded.

## Which radios

The scan needs a radio that tunes the FM broadcast band and streams
**1536 kHz** — today the **SDRplay RSPdx**. The Start button is disabled
with the reason otherwise (an HF-only radio, 384 kHz maximum, a bookmark
scan in progress, the dial locked, the transmitter armed, replay or time
shift active). Without a scan, the catalog still fills from the live
**WFM** receiver: whatever station you listen to is logged as it decodes.

## The catalog

One row per **(channel, PI)** — a DX station on a local's channel is its
own row. Columns:

| Column | Meaning |
| --- | --- |
| Last seen / First seen | Local time of the newest and first decode |
| MHz | Channel centre |
| Station | Latest complete 8-character PS; hover for every PS variant seen (stations cycle slogans), at most 12 |
| Call | RBDS call sign derived from the PI (N. American direct-assignment range) |
| PI | The 16-bit programme identification code |
| PTY, TP | Programme type from the RDS / RBDS table chosen in the DSP popover; TP / TA flags |
| RadioText | Latest RadioText; hover for the last 10 distinct texts |
| Level | Last / best channel power in **dBFS** (relative to the ADC's full scale — raise the RSPdx gain for a truer picture; it is a relative measure, not calibrated dBm) |
| BLER | Block error rate of the last decode |
| Seen | Scan passes (or listening sessions) in which the station appeared |
| Dist | Great-circle distance from home when a station table is imported (see below) |
| Local | The persistence heuristic's verdict |
| Tag | Your free note; a call sign here helps the station table when the PI gives none |

New rows and stations **returning after six hours** away are shown in
bold for two minutes, announced by a toast (at most one every ten
seconds, batched) and offered to the mesh as the **FM DX** alert kind
(Meshtastic → Send alerts → *FM DX scan: new or returning RDS stations*;
line `FMDX 15:06 100.7 WZLX PI17E1 -41dB new`). The catalog is kept in
`Application Support/HermitSDR/fm-dx-catalog.json`, bounded to 5,000
stations (oldest-last-seen evicted), saved a second after it changes and
at quit. **Export CSV…** writes every column; **Clear catalog…** asks
first.

**Double-click a row** (or Tune) to stop the scan, come back to your
previous sample rate when it allows WFM, and listen to that station in
WFM with the speakers unmuted.

## The scan

Press **Start scan**. The receiver is muted, switched to 1536 kHz and
WFM, and its centre is parked on the first **hop**: a 1536 kHz span in
which the scanner runs **seven 200 kHz channels in parallel** (thirteen on
the 100 kHz raster) from the same IQ block — per channel a complex
frequency shift, a 95 kHz low-pass and decimation to the 384 kHz WFM IF,
a quadrature discriminator and one RDS decoder, plus a channel-power
measurement. After the **dwell** (1.5 s by default, 1–5 s) the centre
hops 1.4 MHz up and the next seven channels are decoded; the band is
covered in **15 hops ≈ 25 s** (Americas preset) or 16 hops ≈ 26 s
(Europe). Each hop pays about 150 ms for the retune to settle; IQ from
the previous centre is discarded, not decoded. Stations are catalogued
the moment their PI is confirmed, so a row appears within the dwell, not
at the end of the pass. A 1.5 s visit rarely hears all four PS segments
(or a whole RadioText), so the catalog **keeps the segments heard so far
per station and carries them across hops and passes**: the Station
column shows the characters received with `·` for the missing ones
(`WB·R····`) until the name completes, usually by the second or third
pass; RadioText assembles the same way. The partial state belongs to the
(channel, PI) entry, so a different station on that channel never
inherits it.

**Adaptive** (off by default) lets a hop end early once every channel
that carries a signal (6 dB above the hop's quietest channel) either has
a complete station name in the catalog or has shown no RDS sync at all
after 0.6 s; the dwell slider is then the maximum. Leave it off for the
first passes so names and RadioText have time to assemble.

| Preset | Range | Raster | Channels per hop | Hops |
| --- | --- | --- | --- | --- |
| Americas | 87.9–107.9 MHz | 200 kHz (odd 100 kHz) | 7 | 15 |
| Europe / world | 87.5–108.0 MHz | 100 kHz | 13 | 16 |
| OIRT | 65.8–74.0 MHz | 100 kHz | 13 | 7 |

The status line shows pass, hop and centre; the footer shows the live
channel power of every channel in the hop.

The scan **owns the dial** while it runs: its hops go through the normal
tuning path as the deliberate `fmDXScan` source (so dial lock and tuning
history behave), and it stops by itself when you tune by hand, change
mode or sample rate, disconnect, arm the transmitter, or press **Stop
scan**. Stop, a disconnect or a refusal restore the frequency, mode,
sample rate and mute state the receiver had before the scan; a manual
tune or mode change keeps what you set and only gives the audio and the
sample rate back.

## Telling locals from DX

Two independent filters:

1. **Persistence heuristic** (always on, needs no data): after five
   complete passes, a station present in **at least 80 % of the last 20
   passes** is tagged *local*. DX comes and goes; your locals are in every
   pass. **Hide locals** removes them from the table.
2. **Distance** (optional): set a **Home** — a US ZIP code (looked up in
   the bundled Census ZCTA centroid table, see
   [`docs/licenses/ZCTA-Gazetteer.md`](licenses/ZCTA-Gazetteer.md)) or a
   Maidenhead grid; empty uses the station grid from Settings — and
   **Import station table…**, a CSV of FM transmitters with call sign,
   frequency (MHz), latitude and longitude. The app never downloads one;
   the FCC's public FM Query export works directly: both a header CSV
   (`Call Sign, Frequency (MHz), Latitude, Longitude`; the names
   `call`/`callsign`, `frequency`/`freq`/`mhz`, `lat`/`latitude`,
   `lon`/`lng`/`longitude` are accepted) and the pipe-delimited `fmq` text
   (call sign, `nnn.n MHz`, `N dd mm ss.s` / `W ddd mm ss.s` groups) are
   read. A station is matched by its call sign on the same channel, then
   by call sign alone (translators); a channel alone is never enough.
   With both present the **Dist** column fills and **Hide within N**
   miles (or km) filters the locals out; without a table the window says
   so and only the heuristic applies.

## Privacy and data

Nothing leaves the Mac. The ZIP table is bundled; the station table is
a file you choose; the catalog, settings and imported table live in the
app's Application Support folder. Mesh alerts go out only when you have
enabled the **FM DX** kind under the Meshtastic alerts you already
confirmed.

## Validation

`Tests/DSPTests/FMDXScannerTests.swift` pins the design on synthetic
signals: seven FM carriers with RDS on one 1536 kHz span decode their PI,
PS and RadioText within one 1.5 s dwell with the channel power within
0.01 dB of the synthesised power; the worker discards the settle time and
ignores blocks at the wrong rate; the catalog merges, sorts, evicts and
round-trips JSON and CSV; the local heuristic over fake passes; ZIP
centroids (Boston, Beverly Hills, Honolulu) and the Boston → Los Angeles
great circle; station-table parsing; and the hop sequencer with a fake
tuning sink; a further test cuts the synthetic span into 0.3 s visits
with a fresh decoder each time and asserts every PS and RadioText
completes through the catalog's accumulation.

**On the air (Boston, 2026-11-09, RSPdx on an outdoor VHF antenna)**: the
first live run catalogued **26 stations in 3 passes within 90 s**, pass
time ≈ 25 s as designed, levels and BLER populated, Stop restored the
mute. After three passes most rows had PI and PTY but no PS — the
observation that led to the cross-hop accumulation above. The first RSPdx session should confirm that a full pass over
a city dial catalogs the expected locals, report the channel power the
strongest station shows, and note any hop where the settle time is too
short (a station from the previous span appearing at the wrong channel).
