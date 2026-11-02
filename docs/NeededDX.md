# Needed DX

Open **Log → Needed DX**. The board ranks the stations your feeds can see right
now against what your logbook still needs, and says why each one counts. It is
a local estimate built from your own contacts and the installed country file —
not a confirmed contact, not an award adjudication, and never a transmitter
control. Clicking a row tunes VFO A the way a DX Cluster row or an FT8 decode
row does; nothing keys.

## What feeds it

- **DX cluster spots** from every node enabled in Log → DX Cluster. Human
  spots and skimmer (RBN, spotter ending in `-#`) spots are told apart.
- **This receiver's FT8 / FT4 decodes** from the last 30 minutes (live only;
  time-machine and file replays are excluded). A decode proves the station is
  audible *here*; a spot only proves someone else heard it.
- Remote reception reports (PSKReporter and similar) are a recognised source
  in the ranker but no receive feed exists in HermitSDR yet; the app only
  uploads reports.

Sightings of the same call on the same band and mode merge into one row. The
row keeps the newest time, the most trustworthy source (heard here > cluster >
skimmer > reception report), the best SNR and a count per source. The row's
frequency is the best source's.

## What "needed" means

Coverage comes from the same rules as **Log → QSO Log → Awards**: DXCC entity,
CQ WAZ zone, US state and four-character grid, each worked / confirmed overall
and per band, per mode and per band + mode. Explicit ADIF `DXCC`, `CQZ`,
`STATE` and `GRIDSQUARE` fields win; otherwise the installed `cty.dat` resolves
the call conservatively — an exact-call entry first, then the stated portable
prefix (`KH6/JA1NUT` is Hawaii), while `/MM`, `/AM` and ambiguous multi-call
forms stay unresolved. Unresolved calls are hidden unless **Unresolved** is on,
and they never score as new entities.

Reasons and their points, highest first:

| Reason | Points | Example chip |
| --- | ---: | --- |
| New DXCC entity (never worked) | 100 | New DXCC entity: Chad (any band) |
| New CQ zone | 60 | New CQ zone 23 (Central Asia) |
| New US state (only when a feed states one) | 50 | New state: Vermont |
| New band for a worked entity | 40 | New band slot: 17 m for Japan |
| New grid square (from a CQ message's grid) | 30 | New grid square FN42 |
| Entity worked but not confirmed | 25 | Worked, not confirmed (LoTW): Japan |
| New mode for a worked entity | 20 | New mode: SSB for Japan |
| Zone or state new on this band | 15 | New on 17 m: CQ zone 25 (Japan) |
| New band + mode slot for an entity worked on both separately | 10 | New band/mode slot: 20 m CW for Japan |
| Zone new on this mode | 10 | New on CW: CQ zone 25 (Japan) |
| Entity confirmed, but not on this band | 8 | Not confirmed on 40 m: Japan |
| Grid new on this band | 5 | New on 40 m: grid FN34 |

Two garnish chips add evidence, not need: **Heard here at −12 dB** (10 points
plus up to 8 for SNR) when this receiver decoded the station, and
**Most-wanted #n** (20 points for #1, fading to nothing past #100) from the
bundled or live Clublog ranking. The source itself adds a little (heard here
10, cluster 5, skimmer 3, reception report 2) so a station you can actually
hear outranks the same station merely spotted.

A row needs at least one log-grounded reason. Ties order by freshness, then
callsign. The list is bounded (50 rows).

## Freshness

A sighting under two minutes old is **Live** and scores in full. Older rows
decay linearly to 30 % of their points at 15 minutes (**Recent** until then,
**Stale** after) and leave the board at 30 minutes. The clock re-ranks every
30 seconds even when no feed moves.

## Controls

- **Scope** — *All-time new only* shows just new entities, zones, states and
  grids; *New slots and confirmations too* adds the band / mode slot and
  unconfirmed reasons.
- **Confirmed by** — LoTW, QSL received or either, the Awards window's choice.
- **Unconfirmed** / **Unresolved** — include worked-but-unconfirmed targets;
  list unresolved calls.
- **Bands** / **Modes** chips — restrict to the bands and modes you care about
  (empty selection means all). Modes are ADIF modes: USB/LSB count as SSB,
  SAM as AM. A cluster spot's mode comes from its comment (`FT8`, `CW`, `SSB`
  …); without one the row has no mode and no mode-slot reasons.
- **Min score** — hide rows below a score.
- **Toast at ≥ n** — off by default. When on, an opportunity that first
  reaches the threshold shows the watch toast above the waterfall once per
  30 minutes per call/band/mode. No system notifications, sounds or network
  traffic are involved.

Settings persist with the other application settings. Nothing is uploaded; the
board reads feeds you already enabled.

## Checking a claim

Every chip is traceable: open Awards with the same confirmation choice and
look up the entity, zone, state or grid the chip names; its band / mode matrix
shows the slot the chip calls new. A disagreement means either a contact
lacks the explicit ADIF field (the Awards *Unresolved / outside scope* menus
list those) or the country file resolves the spotted call differently from
how the contact was logged.
