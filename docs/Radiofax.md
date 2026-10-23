# Radiofax Schedules

HermitSDR bundles a worldwide marine radiofax schedule and uses it in two
places: the **Radiofax Schedules** window (Decode menu) with its timed
capture, and the crab's named-station fax tune ("tune the Northwood fax").
Both read the same table and the same UTC clock. The WEFAX decoder itself is
described in `README.md` (capability table) and the Weather Fax window; this
document covers the schedule, the dial convention and the timed capture.
Satellite APT (137 MHz) is out of scope.

## Schedule data and credit

The table is HermitSDR's own transcription of the **NWS "Worldwide Marine
Radiofacsimile Broadcast Schedules"** (`rfax.pdf`, dated **March 7, 2025**,
https://weather.gov/marine/media/rfax.pdf), a U.S. Government document in the
public domain. Only stations and products that could be transcribed with
confidence from that document are included — 21 stations, 640 scheduled
charts:

| Region | Stations |
| --- | --- |
| Asia | JMH Tokyo, JFX Kagoshima, Pevek (148 kHz), HLL2 Seoul, HSW64 Bangkok, JJC Kyodo News, XSQ Guangzhou |
| South America | CBV Valparaíso, CBM Punta Arenas |
| North America | VCO Sydney NS, NOJ Kodiak, NMC Point Reyes, NMG New Orleans, NMF Boston |
| Pacific | VMC Charleville, VMW Wiluna, KVM70 Honolulu |
| Europe | SVJ4 Athens, RBW Murmansk, DDK Hamburg/Pinneberg, GYA Northwood |

Discontinued services the document still lists (Iqaluit, Resolute, Inuvik,
Wellington ZKLF) are not included. Each station carries the document's own
"information dated" line (Pevek's is from 1997, Seoul's from 2009), and the
window shows the document date in its footer. A row is a published schedule,
not a measurement: it says nothing about whether the signal is audible at your
antenna, and stations do change outlets without the document catching up
(Murmansk's notes are an example).

The data file is `HermitSDR/Resources/rfax-schedule.json`, written to be
refreshed by hand from a newer edition of the document:

```json
{"callsign": "NMF", "name": "Boston, Massachusetts, U.S.A.", "region": "North America",
 "lat": 42.09, "lon": -70.71, "informationDated": "2020-02-12", "format": "120/576",
 "outlets": [{"kHz": 4235, "times": "0230-1039"}, {"kHz": 6340.5}, {"kHz": 9110}, {"kHz": 12750, "times": "1400-2239"}],
 "products": [
   {"t": "0230/1400", "p": "TEST PATTERN"},
   {"t": "0325/1525", "p": "SURFACE ANALYSIS (PART 1 NE ATLANTIC)", "v": "00/12", "a": "2"},
   {"t": "----/1443", "p": "PRODUCT NOTICE BULLETIN"}
 ]}
```

- `t` is the document's transmission-time column, one `HHMM` per daily
  transmission separated by `/`; dashes mean no transmission in that half of
  the day. `e` gives an explicit end where the document prints a range.
- `p` is the chart title; `v` the valid time; `a` the map area; `d` the days
  (EiBi-style tokens: `TuFr`, `Mo-Sa`, `Su`); `n` a note (seasonal, "in case of
  tropical cyclone"); `k` restricts a product to some of the station's outlets
  (Kagoshima lists products per frequency; the Charleville 11030 kHz Tasmania
  repeats); `f` overrides the station `format` (RPM/IOC) for one product.
- `outlets[].times` is the outlet's on-air window; `carrier: true` marks an
  outlet the document lists as a carrier frequency (Athens).
- `productsSameAs` copies another station's products (Wiluna = Charleville).
- `region` must be one of the five WMO groupings above.

**Refreshing without an app update:** a file at
`~/Library/Application Support/HermitSDR/rfax-schedule.json` (the Debug
build's own support folder for a Dev build) replaces the bundled table when it
parses; the window's footer says when the override is in use and **Reload**
re-reads it. Structural problems (not JSON, no stations, an unknown region)
make the parser throw and the override is ignored with the reason shown in
the footer. A product with an impossible clock (`2560`, `0975`), an outlet
with a non-finite or non-positive frequency, or an unparsable format is
dropped and counted — the same row-level rejection the EiBi store applies to
bad clocks (#231) — and the footer reports the count.

## Product windows

The document lists start times only. A product's window runs until the
station's next product starts, capped at **20 minutes** (the decoder's own
image cap; a 120 LPM / IOC 576 chart is about ten minutes), or until the
explicit end for the few ranges the document prints (Pevek's two-hour ice
broadcasts). Only products that share an outlet shorten each other, so
Kagoshima's per-frequency lists do not interfere. A window that crosses UTC
midnight (Honolulu's 2354 streamline) is on the air on both sides of it and
is judged against the day it started.

## The window (Decode → Radiofax Schedules)

- **Search** — callsign, place, country, operator or chart title (`boston`,
  `gale warning`), or a number for a frequency in kHz matched within ±5 kHz of
  an outlet. **Region** and **Station** narrow the table.
- **Now / Next / All** — *Now* lists the charts on the air this minute;
  *Next* every chart, soonest start first, on-air rows (bold, `ON AIR`) at
  the top; *All* the whole table by station and time. *Capture only* keeps
  the ticked charts.
- **Outlets kHz** shows the station's outlets that carry the chart and are
  open at its start (not at the current minute — a 1400 row shows the 1400
  outlets); the recommended one is highlighted and **Dial MHz** is its USB
  dial. Click any outlet figure to tune that one instead.
- **km** is the great-circle distance from your station grid (Settings) to
  the transmitter; blank when the document gives no site (Kyodo News) or no
  grid is set.
- **Tune** / double-click / the context menu put the dial on the recommended
  outlet in **USB**. The table is a published document and lists the chart
  as it is, including days-of-week badges and the document's notes (ⓘ).

### Dial convention

The document lists **assigned** (centre) frequencies; a USB receiver dials
**1.9 kHz below** so the fax black/white tones land on 1500/2300 Hz, which is
what the WEFAX decoder expects. That is the same offset the crab's
named-station tune has used since 2026-09-15, pinned by test against the
`UtilityStation` table. Athens (SVJ4) is the one station the document lists
as carrier frequencies; its outlets are flagged and dial on the listed figure.
Bangkok's single outlet *may* be a carrier frequency according to the
document; the station note says so and the row dials the assigned convention.

### Outlet choice

Among the outlets open at the chart's start: a listener within ~700 km of
the transmitter gets the lowest usable outlet (the high ones are inside the
skip zone — measured from FN42 on 2026-09-15: NMF 9110 kHz was noise, 6340.5
kHz painted the chart at S9+27); otherwise night (before 1200 UTC) prefers
the second-lowest and day the second-highest of three or more, the extreme
otherwise. Click another outlet figure when propagation disagrees.

## Timed capture

Tick **Capture** on any chart (at most 32) and switch on **Timed capture** in
the footer. From then on, with or without the window open, on the chart's
published minute HermitSDR:

1. tunes the recommended outlet in USB;
2. selects the WEFAX profile matching the chart's RPM/IOC when one exists
   (`IOC 576 · 120 LPM`, `IOC 576 · 90 LPM`), remembering the profile it
   replaced;
3. enables the Weather Fax decoder if it was off (the decoder then waits for
   the start tone exactly as it does by hand);
4. at the chart's end calls the decoder's *Finish* (the chart in progress is
   saved as PNG through the normal path, with the usual metadata), disables
   the decoder again only if it was the one that enabled it, and restores the
   profile it replaced.

The toast over the waterfall, a line in the crab's feed and the decoder's
diagnostics (Decoder Activity) record each start and stop.

Rules, all pinned by `RFAXScheduleTests` with an injected clock:

- **Exactly once per occurrence.** Each (chart, UTC start) is recorded in a
  bounded in-memory fired map (entries older than two days pruned, 256 at
  most); ticking twice in the same minute or re-enabling inside the window
  cannot start it again. The map is not persisted: relaunching the app inside
  the three-minute grace is the one way an occurrence can start a second
  time. The next day's occurrence is new.
- **One capture at a time.** The decoder is single; two overlapping charts run
  in start order, the second starting in the tick that ends the first if its
  window is still inside the grace.
- **Late starts.** A start up to three minutes late (app launched late, Mac
  asleep) still happens — phasing is gone but the picture reads; later than
  that the occurrence is skipped.
- **Receive only.** A start is refused — and the occurrence consumed — while
  the transmitter is keyed, RF-hot or owned by any transmit program (native
  programs, CAT, Control API), or when no radio (live, replay or Demo) is
  connected. A refused start posts a toast and a decoder diagnostic; the
  capture never touches ARM, PTT or any TX surface.
- **Operator ownership.** Untick the chart or switch Timed capture off and a
  running capture stops at once (the chart so far is finished and saved). A
  decoder the operator had already enabled stays enabled afterwards.
- **Schedule changes.** Plans survive a schedule override that renames a
  chart only as orphans listed in the footer for removal; an orphan never
  starts.

The clock is a 60 s timer aligned one second past the UTC minute, so a 0325
chart starts at 03:25:01 at the latest. Plans and the master switch persist
in the app's defaults (`rfaxCapturePlans`, `rfaxTimedCapture`); the master
switch is off by default and is also readable by the crab as
`decode.rfaxTimedCapture`.

## The crab

`monitor_mode` with a station name ("Boston Coast Guard fax", "Northwood
fax", "Hamburg fax") resolves against the whole table (stations the document
gives a transmitter site for), picks the outlet for the UTC hour with the
listener-distance rule above, dials 1.9 kHz below in USB and switches the
decoder on — the same behaviour as before, now for every listed station.
The bundled five-station `UtilityStation` table remains the fallback when the
schedule file cannot be read, and the test suite checks it outlet for outlet
against the transcription.

## Tests

`Tests/DSPTests/RFAXScheduleTests.swift`: the bundled file parses with zero
rejected rows, 21 stations across the five regions, unique product ids and
capped windows; the five crab stations agree with the transcription; the
rejection fixture drops impossible clocks, negative frequencies, bad windows
and bad formats row by row while structural problems throw; product ends,
the −1.9 kHz dial, the Athens carrier flag, outlet windows and the outlet
recommendation; now/upcoming across UTC midnight and day tokens; and the
capture engine's exact-once start/stop, grace, handover, master-switch,
plan-removal and schedule-change behaviour with an injected clock.
