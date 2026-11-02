# Band Openings

Available from the first release after **2026.1101_001** (#313). The
detector is receive-side only: it reads what the station already decodes and
what the DX cluster already relays, and shows a per-band judgement with the
evidence behind it. Nothing in it keys, arms or tunes the radio, and nothing
about the station is sent anywhere.

The header's **Openings** chips (beside Kp and SFI; also on the console
layout's status row) show one chip each for **10 m**, **6 m**, **2 m** and
**70 cm**. 10 m is the HF sanity band: an Es season that opens 6 m opens
10 m first, and a 10 m that stays quiet while 6 m "opens" is a reason to
distrust the feed. Click a chip for the evidence popover. Station → Features
hides the strip.

## Inputs

| Source | What becomes evidence | Location |
| --- | --- | --- |
| This station's decoders | Every station the Stations Heard list records: FT8/FT4 spots, WSPR, JS8, DSC and APRS paths with a grid | Reporter = the station grid (Settings); reported = the decoded grid |
| DX cluster / RBN | Every spot on a judged band from any connected node | Reported = the spot's trailing grid when the skimmer sent one (kept on the spot since this release), else the country-file centroid for the DX call; spotter = the country-file centroid for its call. Centroid-located ends are marked *approximate* |
| PSKReporter | Not yet — HermitSDR only uploads to PSKReporter. The evidence type has the slot; the download is a follow-up | — |

Every decode or spot on *any* band, HF included, is a feed heartbeat even
when it is not evidence. The model samples the observables every 5 s
(≤0.2 Hz) on the main actor; the detector itself is a pure value type
(`BandOpeningDetector`) under package tests.

## States

| State | Meaning |
| --- | --- |
| **Disconnected** | No radio session and no cluster enabled — nothing to judge. |
| **Feed quiet** | Connected, but no decode or spot of any kind, on any band, for 10 min (or ever). The decoder may be off or the cluster logged out. This is the feed-dead case, deliberately separate from a quiet band. |
| **Quiet** | Feeds are alive (something was decoded or spotted recently) and the band has no qualifying path. |
| **Insufficient** | Some evidence, but not enough: too few distinct paths, too few distinct stations (one far superstation heard by many spotters never qualifies), only centroid-located cluster paths with nothing decoded here, or paths with neither end near this station. |
| **Opening** | Enough distinct paths from enough distinct stations, at least one grid-located. |
| **Strong opening** | An opening with many more paths and a sustained rate. |

## How a path qualifies

A *path* is one reporter → reported pair (a station decoded here twice is
one path with two reports). It qualifies when:

1. its great-circle length is at least the band's **minimum distance**
   (shorter is line of sight or ground wave — counted as *local chatter*,
   never as propagation);
2. one end is **near this station**: a local decode always is; a cluster
   path needs a grid-located end within 500 km of the station grid, or a
   centroid-located end within 1,500 km (approximate, and said so).

An opening additionally needs **distinct reported stations** (not just
paths) and **at least one grid-located path**. Without a station grid in
Settings, cluster paths cannot be placed and are reported as such.

## Thresholds (data-driven, per band)

| Band | Min path | Opening | Strong | Strong rate |
| --- | --- | --- | --- | --- |
| 10 m | 500 km | 6 paths / 4 stations | 20 paths | 1.5 reports/min |
| 6 m | 150 km | 3 paths / 2 stations | 8 paths | 0.5 reports/min |
| 2 m | 150 km | 3 paths / 2 stations | 6 paths | 0.4 reports/min |
| 70 cm | 100 km | 2 paths / 2 stations | 4 paths | 0.3 reports/min |

Common to every band: 15-minute window, 500 km / 1,500 km near radii, feed
timeout 10 min, hold 5 min, exit at 60 % of the entry count. The popover's
footer prints the band's live values. These are starting points chosen to
be explainable, not a sensitivity claim; they live in
`BandOpeningThresholds.defaults(for:)`.

## Hysteresis

Once a band is called open it stays open for at least 5 minutes, and after
that until its qualifying paths fall below 60 % of the entry threshold
(rounded up — for 6 m, below 2). A strong opening steps down to opening
before it ends; it never drops straight to quiet. An opening cannot flap on
one empty FT8 slot.

## The evidence popover

Each line is a sentence the detector can stand behind: the state and why
("3 distinct paths from 3 stations in 15 min, farthest 1,840 km to K1ABC
(FN42) — 800–2,300 km (single-hop Es); 0.4 reports/min"), the evidence
sources and counts, compass sectors of the qualifying paths, and a
distance histogram: **< 150 km (local)**, **150–800 km (tropo / meteor
scatter)**, **800–2,300 km (single-hop Es)**, **2,300–4,500 km (multi-hop
Es / F2)**, **> 4,500 km (F2 / TEP)**.

## Alerts

**Toast when a band opens** (in the popover; off by default; a global
preference) shows the band's headline at the top of the waterfall and in
the crab's action feed when a band moves into Opening or Strong opening.
No sound, no QSY, no PTT.

## Validation

`BandOpeningDetectorTests` fixtures cover every state, the isolated
superstation, duplicate reports, a dead feed versus a quiet band,
sporadic bursts, stale data ageing out of the window and the hysteresis
hold; `BandOpeningFeedTests` cover the heard-station and cluster
translations, once-only delivery and RBN grid capture.
