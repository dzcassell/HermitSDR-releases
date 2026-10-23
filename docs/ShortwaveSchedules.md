# Shortwave Schedules

HermitSDR bundles the EiBi shortwave broadcast schedule and uses it in three
places: the **Shortwave Schedules** window (Radio menu), the **on-air
broadcaster labels** over the panadapter (View menu), and the crab's
`shortwave_schedule` tool (plus its "shortwave station coming on the air"
watch). All three read the same rows and the same UTC clock, so what the
window shows in bold is what the labels draw and what the crab answers.

## Schedule data and credit

The schedule is the **EiBi** database by Eike Bierwirth
(eibispace.de) — the community-standard seasonal listing of shortwave
broadcasters, about 9,000 rows per season. It is free for non-commercial use
with credit; HermitSDR credits it in this document, in the window's footer and
in About → Licenses. Nothing about the listing is HermitSDR's own: a row is a
published schedule, not a measurement, and it says nothing about whether the
signal is audible at your antenna.

One season file (`eibi-a26.csv` for the summer A26 season) ships inside the
app so the feature works offline. When online, the app refreshes its copy at
most once a week from `https://www.eibispace.de/dx/sked-<season>.csv` into
Application Support; a refresh that does not parse to a plausible season
(fewer than 1,000 rows, an error page) is discarded and the bundled file keeps
serving. The window itself makes no network request — opening it only reads
the rows already loaded.

Rows with EiBi persistence code 8 / 98 (inactive) are dropped at parse time.
Rows with code **90 and above** are *utility* rows — time signals, navy and
aeronautical traffic, data links — not broadcasters; the window hides them
unless **Utility** is ticked and tags them `UTIL` when shown, and the label
layer leaves them out unless *Include Utility Stations* is on.

## The window (Radio → Shortwave Schedules)

- **Search** — one field: a station name (`BBC`, `Romania`), an ITU country
  code (`G`, `MLI`), a language code or name (`E`, `French`), a target area
  (`ME`, `SEA`), or a number for a frequency in kHz (`9410`, `9,410`,
  `9.41 MHz`) matched within ±5 kHz. Matching is case- and accent-blind.
- **Now / Next / All** — *Now* lists only what EiBi says is on the air this
  minute (by frequency); *Next* lists everything with the soonest start first
  (on-air rows at the top, then "in 5 min", "in 2 h 10", "in 3 d 04 h");
  *All* is the whole schedule by frequency.
- **UTC hour** — keeps only slots that overlap that hour on today's weekday.
- **On-air rows are bold** with an `ON AIR` status; the clock is UTC and the
  list re-evaluates on every minute boundary. Day-of-week tokens (`Mo-Fr`,
  `SaSu`, `1245`, `Su`) are honoured; irregular tokens (`irr`, `alt`, dates)
  are shown as *possibly on* rather than hidden.
- **Tune** — double-click a row, press Return with it selected, or use the
  context menu. The dial lands on the channel in **AM** (if the receiver is
  already in SAM, SAM is kept — it fares better on fading shortwave). With a
  transverter profile the RF is mapped and range-checked like any other tune.
- **Favourites** — click the star. Favourites persist (defaults key
  `swbcFavourites`, in the Settings.plist mirror like everything else) and
  carry the row's fields, so a season refresh that drops or moves a row leaves
  the favourite listed in the footer as "no longer in the current season"
  with a one-click removal; it is never tuned to a frequency the schedule no
  longer claims. **★ only** filters the table to favourites.
- **Remind** — tick the box on a favourite. **Five minutes before** the slot
  next comes on the air (honouring its day token, across the UTC midnight
  boundary) a toast appears over the waterfall and a line lands in the crab's
  action feed: `📻 BBC — 9410 kHz (English → ME) at 1300 UTC, on in 5 min`.
  Each occurrence reminds exactly once — the favourite is stamped before the
  fire is delivered, so the 60 s clock cannot repeat it; the next day's or
  week's occurrence fires fresh. Untick to stop; re-ticking clears the stamp.
- The footer shows the row count (the table is capped at the first 2,000
  rows — narrow the search), how many are on the air, the favourite count,
  the **Panadapter labels** switch, and the EiBi credit with the loaded
  season.

## Panadapter labels (View → Shortwave Broadcast Labels)

*Show On-Air Broadcasters* draws the names of the stations EiBi says are
transmitting **now** inside the visible span, in the same label layer as the
FT8, skimmer and DX cluster overlays (three staggered rows under the cluster
rows). Amber labels are broadcasters, grey ones utility rows (only with
*Include Utility Stations*), a ★ marks a favourite; a channel shared by
several transmitters or languages shows the first name and `+N`, and hovering
lists them. Click a label to tune to it in AM.

The layer is bounded: **at most 24 labels** per span, chosen favourites
first, then broadcasters, then utility rows, then nearest the display centre
— so a crowded 49 m evening shows the stations you starred before the ones
you did not. Selection runs on the minute tick and on zoom / pan, never per
frame; measured over the bundled A26 season at 1900 UTC on a 1.5 MHz span
(5.75–7.25 MHz): 9,289 rows, 1,265 on the air, 24 labels selected in 3.8 ms
(Debug build), and a season-wide station search returns in under 40 ms.
With the toggle off the layer is not in the view tree at all.

Both switches are also crab-settable (`display.swbcLabels`,
`display.swbcLabelsUtility`) and persist across launches.

## The crab

`shortwave_schedule` now takes an optional UTC time and an empty query:

- "What's on this frequency?" — empty query → what EiBi lists within 5 kHz of
  the dial right now.
- "Who's on 9410?" / "Where is the BBC?" — frequency or station, as before.
- "What's on 7300 at 0100 UTC?" / "Is Radio Romania on at 2100?" — the
  `time_utc` argument evaluates the schedule at that clock on today's weekday.

The existing *station watch* ("tell me when the BBC comes on") is unchanged
and is the other route to a reminder for stations you have not starred.

## Tests

`SWBCScheduleTests` (package) pins: the UTC clock conversion and on-air
predicate across the day boundary and every day-token style (`Mo-Fr`,
`SaSu`, `1245`, `Su`, `Mo`, daily, midnight wrap), the next-start scan across
the week, search by every field plus the hour filter and scope ordering,
favourite toggling / reminder flags / Codable round trip (with unknown keys
tolerated), reminder exact-once on a simulated 60 s tick (including a late
tick and the next week's occurrence), the label bound / de-duplication /
favourite priority on a synthetic 300-row span, and the bundled-season timing
above. `SWScheduleTests` continues to cover the parser and the crab's older
paths; `CrabWatchTests` the station watch.
