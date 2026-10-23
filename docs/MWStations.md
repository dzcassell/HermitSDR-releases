# MW Stations

HermitSDR looks up medium-wave (AM broadcast band, 530–1700 kHz) stations in
three places: the **MW Stations** window (Radio menu), the **medium-wave
channel labels** over the panadapter (View menu), and the crab's
`mw_station` tool. All three read the same rows and the same station grid, so
the label on a channel is the first row the window lists for it and the first
station the crab names.

## Station data

### FCC AM Query (fetched on request, never bundled)

The list is the FCC's public **AM Query** — US Government data, public
domain. HermitSDR fetches its pipe-delimited "text" output over the whole band
with every licence status:

```
https://transition.fcc.gov/fcc-bin/amq?state=&call=&arn=&city=&freq=530&fre2=1700&type=0&facid=&class=&list=4&dist=&dlat2=&mlat2=&slat2=&NS=N&dlon2=&mlon2=&slon2=&EW=W&size=9
```

(`list=4` = pipe-delimited rows, `type=0` = licences, construction permits and
applications, no distance origin.) Fetched 2026-10-22 it was 10.3 MB: 24,552
rows of 35 pipe-separated fields, which merge to 12,554 stations — 4,267 US
facilities plus the Canadian, Mexican, Caribbean and South American
notifications the FCC coordinates against (those carry the `CP` status in the
extract). The rows are *listings*, not measurements: a construction permit
or application may not be on the air, and nothing here says whether a signal
is audible at your antenna.

**Nothing downloads on its own.** The window's **Refresh** button fetches the
extract (one fixed HTTPS `GET`, no station, grid, frequency or audio data is
sent). **Refresh weekly**, off by default, re-fetches a cached copy older
than seven days when the window opens or the channel labels are on. The
cache lives at `~/Library/Application Support/HermitSDR/mw-fcc-am.txt`
(Debug builds use their own support folder) and survives relaunches; the
window footer shows the station count and fetch date. The crab's tool only
ever reads the cache.

A download is refused, with the reason in the footer and the previous copy
left in place, when it is larger than 48 MB, is not the FCC row format (an
error page), parses to no readable rows, or merges to fewer than 1,000
stations (a partial download). A cached file that no longer parses is
deleted so its fresh date cannot suppress a refresh.

### Row format

Each row is one facility × hours-of-operation record. Fields are read by
position as observed in the extract (field 0 is the empty token before the
leading pipe): 1 call, 2 frequency (`1030  kHz`), 3 service (`AM`), 5 hours
code (`UNL` unlimited, `DAY`, `NIG`, `CRI` critical hours), 7 station class
(A–D), 9 status (`LIC`, `CP`, `APP`), 10 city, 11 state, 12 country, 14 power
(`50.0   kW`), 15 `Directional` or blank, 18 facility id, 19–22 latitude
(N/S, degrees, minutes, seconds), 23–26 longitude (E/W, d, m, s), 27
licensee. A row whose service is not AM, whose frequency is outside
520–1710 kHz, or whose call is blank is skipped and counted; a row with an
unreadable coordinate is kept without one.

Rows merge per call + facility id. `LIC` outranks `CP` outranks `APP` for
the station's identity and frequency; the day power comes from the `DAY` or
`UNL` row and the night power from the `NIG` or `UNL` row of the best
status, each with its own directional flag. A daytimer therefore has no
night power and is never the label on a channel after dark. City and
licensee are title-cased from the FCC's capitals.

### Your own CSV (optional)

**Import CSV…** reads a comma-, semicolon- or tab-separated file with a
header row — the shape of an MWList or similar export — and copies it to
`mw-stations-import.csv` beside the FCC cache. No third-party list is
bundled or fetched. Columns are matched by header name, case- and
punctuation-blind (`Power (kW)` → `powerkw`):

| Field | Accepted header names | Required |
| --- | --- | --- |
| Frequency (kHz) | `kHz`, `frequency`, `freq`, `frequency_khz`, `f` | yes |
| Call letters | `call`, `callsign`, `calls`, `call letters` | one of call / name |
| Station name | `station`, `name`, `station name`, `programme`, `program`, `broadcaster` | one of call / name |
| City | `city`, `location`, `site`, `town`, `qth`, `tx site`, `transmitter site` | no |
| State / region | `state`, `region`, `province`, `prov`, `st` | no |
| Country | `country`, `itu`, `ctry`, `cty` | no |
| Day power (kW) | `power`, `power kW`, `kW`, `pwr`, `power day`, `day power`, `day` | no |
| Night power (kW) | `power night`, `night power`, `night`, `pwr night`, `pwrn` | no (defaults to the day power) |
| Latitude | `lat`, `latitude` | no (no distance or map pin without both) |
| Longitude | `lon`, `long`, `lng`, `longitude` | no |

Frequencies from 150 to 1800 kHz are accepted (long wave included), decimal
commas are understood, quoted fields may contain the delimiter. A file
without a frequency column, or without a call or name column, is refused
with the reason; rows that fail are counted in the footer. Imported rows are
tagged `CSV` in the table and keep an empty class / status. **Remove**
forgets the list.

## The window (Radio → MW Stations)

- **Search** — one field. Call letters match fuzzily: exact first, then a
  call the query begins with (or that begins the query — `WBZZ` → WBZ), then
  calls within one edit (two for queries of five or more characters,
  adjacent transpositions count as one: `WZB` → WBZ); two-letter queries do
  not fuzz. A number is a frequency in kHz (`1030`, `1,030 kHz`,
  `1.03 MHz`) and lists every station on that channel. Any other word
  matches city, state, country or licensee / name. Within equal scores rows
  are nearest first; without a valid station grid, most powerful first.
- **Columns** — call (bold on an exact match; `CP` / `APP` / `CSV` tags),
  kHz, city, state, country, power (`50 kW DA`, or `6 kW DA / 1 kW DA night`
  when day and night differ, `45 kW / — night` for a daytimer), class,
  distance and bearing from the station grid (Settings › Station; the footer
  says when the grid is missing or invalid), licensee or station name.
- **Channels** — the 10 kHz (Region 2) or 9 kHz grid used by the panadapter
  labels; persisted (`mwChannelPlan`).
- **Tune** — double-click, Return, the context menu or the button: the dial
  lands on the channel in **AM** (SAM is kept when already selected), through
  the same path as a shortwave schedule row.
- **Plot on Map** — sends the current rows (those with coordinates, at most
  200) to the Stations Heard map as an **MW** layer: a pin per station
  showing its kHz, hover for the full line, a layer toggle and a Clear MW
  button in that window's bar. The context menu plots one row. Plotting is a
  lookup, not a reception, which is why it is a separate layer with its own
  colour.
- The footer shows the row count (capped at the first 500 — narrow the
  search), the station total and the grid in use, the FCC fetch status with
  **Refresh** and **Refresh weekly**, the import status with **Import CSV…**
  or **Remove**, the outcome of the last fetch or import, and the data credit.

## Panadapter labels (View → Medium-Wave Station Labels)

*Show MW Stations* names the station most likely heard on each channel of
the chosen grid inside the visible span — the one nearest your station grid,
or without a grid the most powerful at this daypart (civil daylight at your
location decides day versus night power; a daytimer never names a channel at
night). A channel with several stations shows `+N` and hovering lists the
top four with distances; click a label to tune to it in AM. The labels sit
in the same layer as the shortwave labels, one row lower, in light blue.

The layer is bounded: **at most 24 labels** per span, the channels nearest
the display centre first, so a 1.5 MHz span over the whole band shows the
middle 24 channels and zooming in shows every channel. Selection runs on
zoom / pan, on a data change, on a grid change and on a ten-minute daypart
tick, never per frame; distances are computed once per station when the
index is built, not per selection. Measured on the 2026-10-22 extract
(12,554 stations, Debug build, FN42 home): parse 0.9 s off main; index
with distances and per-channel ordering 16 ms; 24 labels at a 1.5 MHz span
0.6 ms; a fuzzy `WBZZ` search over the whole list 75 ms. With the toggle off the layer is not in
the view tree.

Both switches are crab-settable (`display.mwLabels`, `data.mwFCCAutoRefresh`)
and persist across launches (`mwLabels`, `mwChannelPlan`, `mwFCCAutoRefresh`
in the defaults and the Settings.plist mirror).

## The crab

`mw_station` takes one optional query:

- "What's on 1030?" / "Who is on 1030 kHz?" — every station on the channel,
  nearest first: `On 1030 kHz, nearest first: WBZ 1030 kHz — Boston, MA,
  50 kW DA, class A, 27 km SSE; …`.
- "What's on this frequency?" — empty query → the current dial, rounded to
  the kHz, when it is inside 520–1710 kHz.
- "Who is WBZ?" / "Who is WBZZ?" — the call, or `Nothing is called exactly
  "WBZZ"; closest: WBZ 1030 kHz …`.
- "AM stations in Boston" — a city or licensee.

The tool reads the cached lists only; if nothing has been fetched it says so
and points at the window. It is read-only and available to viewer chat.

## Tests

`MWStationsTests` (package) pins: every field of one real FCC row (the
format witness) and synthetic rows in the same format — day / night merge,
`LIC` over `CP`, a daytimer, a `-` licensee, a southern-hemisphere
coordinate; malformed rows (truncated, FM service, out-of-band frequency,
blank call, bad hemisphere) counted with the first reason, an HTML error
page, an empty file, a file of only bad rows and a short file refused with
their reasons; the CSV importer's header mapping across the three
delimiters, quoted delimiters, missing coordinates, a bad frequency row and
the no-frequency-column / no-call-or-name / empty refusals; edit distance
and call scoring (exact, prefix, one edit, transposition, the two-letter
guard); `WBZ`, `WBZZ`, `WZB`, `1030`, `1.03 MHz`, `Boston` and `MA` queries
ranked, with and without a home grid; distance and bearing from FN42 to the
WBZ site; the label bound (24 of 118 channels nearest the centre at 1.5 MHz,
every channel when zoomed, nearest station per channel, most powerful
without a grid, daytimer excluded at night, the 9 kHz grid, off-band and
zero-span spans); label timing over an extract-sized synthetic list; the
crab's answers; civil daylight at the home grid. A whole-extract test runs
only when `HERMITSDR_MW_FCC_EXTRACT` names a downloaded file (the extract is
never bundled) and is otherwise skipped. `CrabToolRouterTests` pins that
`mw_station` is registered and routable.
