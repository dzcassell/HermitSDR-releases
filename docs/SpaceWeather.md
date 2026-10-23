# Space Weather

Available from the first release after **2026.1022_001** (#277). The window
is receive-side only: it fetches public NOAA data, draws it, and can wake a
crab watch. Nothing in it can key, arm or tune the radio, and nothing about
the station is ever sent.

Open **Log → Space Weather**. The header's **Kp** and **SFI** chips stay as
they were (`planetary_k_index_1m.json`, 1-minute Kp; `f107_cm_flux.json`,
observed noon F10.7, 48-hour freshness). The window adds the rest of the
SWPC picture.

## Products, cadence and freshness

All requests are fixed HTTPS `GET`s to `https://services.swpc.noaa.gov/`
with no query string, cookie or body, sent at launch and then hourly from
one owning queue (`SpaceWeatherCenter`: a serial `URLSession` delegate
queue parses each body; the result is published on the main actor as one
value-type `SpaceWeatherSnapshot`). The DSP and audio threads are never
involved. About 1 MB per hour in total; any body over 4 MB is rejected
unread.

| Product | Path | Shown as | Freshness limit |
| --- | --- | --- | --- |
| 3-hourly planetary Kp (7 days) | `products/noaa-planetary-k-index.json` | Kp card, Kp line on the "Kp & A" plot | 6 h |
| Daily geomagnetic indices (30 days) | `text/daily-geomagnetic-indices.txt` | Planetary and Fredericksburg A-index, Ap bars | 48 h |
| Daily solar indices (30 days) | `text/daily-solar-indices.txt` | Sunspot number, daily F10.7, flare counts, "SFI & SSN" plot | 48 h |
| GOES X-ray flux (1-minute, 24 h) | `json/goes/primary/xrays-1-day.json` | Flux + flare class badge, log plot with A/B/C/M/X bands | 2 h |
| GOES X-ray flares (7 days) | `json/goes/primary/xray-flares-7-day.json` | Latest flare line; flare watches | 7 d (newest event) |
| Propagated solar wind (1 h) | `products/geospace/propagated-solar-wind-1-hour.json` | Speed, density, Bz, Bt; "Solar wind" plot | 2 h |
| GOES integral protons (24 h) | `json/goes/primary/integral-protons-1-day.json` | ≥10 and ≥100 MeV cards, PROTON EVENT badge, "Particles" plot | 2 h |
| GOES integral electrons (24 h) | `json/goes/primary/integral-electrons-1-day.json` | ≥2 MeV card and plot | 2 h |
| NOAA scales | `products/noaa-scales.json` | R / S / G badges (now, yesterday, three-day outlook in the tooltip) | 24 h |
| 27-day outlook | `text/27-day-outlook.txt` | "Outlook" plot (A-index bars; F10.7 and largest Kp per day parsed) | 10 d (issue time) |
| 45-day AP and F10.7 forecast | `text/45-day-forecast.txt` | "Outlook" plot (Ap line) | 10 d (issue time) |
| Alerts, watches, warnings, summaries | `products/alerts.json` | The alert list (headline, product code, issue time, full text) | 7 d (newest message) |

The freshness rule is the SFI chip's rule applied per product: the newest
timestamp inside the body (the issue time for the text outlooks) must be no
older than the limit, allowing five minutes of clock skew. A product that
fails to parse, answers with a non-200 status, times out or is unreachable
(networking denied, offline) records a failure; a previously fetched value
survives only while it is itself still within its limit. Between refreshes
the same rule expires a reading. Anything missing shows a **dash**; the
"Product freshness" disclosure at the bottom of the window lists every
product's age or failure reason. These are observations and short forecasts
from NOAA, not a prediction of which band is open.

The **WWV / WCY** geophysical line relayed by a connected DX cluster node is
shown beneath the reading cards when one has arrived, so the two sources
can be compared.

## Plots

Swift Charts, palette-aware through the active skin's tokens, UTC axes:

- **Kp & A** — daily planetary A-index for the last 30 days (bars) with the
  3-hourly Kp of the last 7 days (line, ×10 so both fit one axis).
- **SFI & SSN** — daily F10.7 and SESC sunspot number, 30 days.
- **X-ray** — GOES 0.1–0.8 nm flux over the last 24 hours on a log axis
  with the B/C/M/X class lines.
- **Particles** — ≥10 MeV protons and ≥2 MeV electrons, 24 hours, log
  axis, with the 10 pfu S1 line.
- **Solar wind** — speed and Bz (×20) over the last hour.
- **Outlook** — 27-day outlook A-index (bars) with the 45-day Ap forecast
  (line).

## Alert watches

Watches live in the existing crab watch list (`crabWatches`, persisted like
bookmarks) and can be added from the window's buttons or by asking the crab
("watch for M flares", "tell me when G2 hits", "alert me on a proton
event"). Beside the pre-existing callsign, station and **Kp ≥ n** watches
(Kp keeps its 3-hour re-fire cooldown), three event kinds are new:

| Kind | Target | Fires |
| --- | --- | --- |
| Flare | a class: `M`, `X`, `X2`, `C9.5` | once per flare whose peak class is at or above the target, keyed by the flare's begin time; only flares that began after the watch was created, within the last 7 days |
| Scale | `R1`–`R5`, `S1`–`S5`, `G1`–`G5` | once when the current NOAA level reaches the target; silent while it persists or escalates; re-armed when the level drops below the target |
| Proton event | a pfu threshold, default 10 (NOAA S1) | once when the ≥10 MeV flux reaches the threshold; re-armed when it drops below |

A fire shows the usual watch toast, writes a line into Ask The Crab, and —
when **Speak alerts** is on (off by default; also the crab control
`spaceWeather.alertSound`) — reads the message aloud through the spoken
status voice. That voice is its own system audio client: it never enters
the receive chain, a recording, a stream or the transmitter.

The crab's `band_conditions` tool reports the same readings (Kp, A-index,
sunspot number, X-ray class and latest flare, R/S/G, solar wind, proton and
electron flux, the newest SWPC message) after the Kp and SFI lines it
already gave.

## Fixtures and checks

`Tests/DSPTests/SpaceWeatherTests.swift` parses every product from a
captured fixture under `Tests/DSPTests/Fixtures/SpaceWeather/` (public
products captured 2026-10-22, trimmed where the live body is large), and
pins stale rejection, malformed bodies, non-200 and oversized answers, the
network-denied case (every product unavailable, no invented summary line),
each clock spelling NOAA uses, and that every watch kind fires exactly once
per event. In a Debug build, `HERMITSDR_DEMO=1` with
`HERMITSDR_SPACE_WEATHER_FIXTURES=<directory>` replays such fixtures
(`<product>.json` / `.txt`, named by `SpaceWeatherProduct`) instead of the
network, so the window renders deterministically in an isolated UI check.
