# Parks & Summits — POTA / SOTA hunting

Open **Log → Parks & Summits**. The window lists Parks on the Air and Summits
on the Air activators who are on the air right now, as reported by the two
programs' public spot feeds, and turns a click into a tuned dial plus a
correctly referenced logbook entry. Receive only: nothing here keys, arms or
retunes a transmitter, and no spot is ever posted.

## Spot feeds

The feeds are **off by default**. Turn on **Spot feeds on**; the POTA and
SOTA switches beside it choose which program to poll (both by default).

| Program | Endpoint | Shape used |
| --- | --- | --- |
| POTA | `https://api.pota.app/spot/activator` | JSON array: `activator`, `frequency` (kHz, as text), `mode`, `reference`, `parkName` / `name`, `locationDesc`, `spotter`, `comments`, `spotTime` (UTC, no zone suffix), `invalid` (non-null = withdrawn), `spotId` |
| SOTA | `https://api-db2.sota.org.uk/api/spots/60/all/all` (SOTAwatch v3; the old `api2.sota.org.uk/api/spots/{n}` answers only with a deprecation record) | JSON array: `activatorCallsign`, `callsign` (the spotter), `frequency` (MHz), `mode`, `summitCode`, `summitName`, `AltM`, `points`, `comments`, `timeStamp` (ISO 8601, `Z`), `id` |

While on, both endpoints are fetched every 90 seconds with
`If-None-Match` / `If-Modified-Since` revalidation, so an unchanged feed
costs a 304. The requests are fixed public GETs with a `HermitSDR` user agent;
no callsign, grid, frequency or any other station data is sent, and no account
or key is involved. **Refresh** repeats the same two requests immediately.

The list is bounded (400 rows) and deduplicated by **activator + reference +
band**: a re-spot of the same activation replaces the older row, a band change
is a new row. Spots age out an hour after the program's own time stamp. A bad
reply never clears what is already listed; the status line under the header
shows each source's health (green = last fetch good, amber = not fetched yet,
red = the last fetch failed, with the failure count in the tooltip).

## The list

Columns: age, program, activator, reference and park/summit name (with the
POTA location or the SOTA altitude and points), frequency in kHz, the mode the
spot carries (a spot without one shows the band-plan guess in grey), and the
worked-before badge from your QSO log:

- green ⭑ — this activator at this park/summit is already in your log;
- cyan ⭑ — the park/summit is in your log with a different activator;
- · — not in your log.

The badge reads the hunter-side `POTA_REF` / `SOTA_REF` fields of every
contact, splits comma-separated multi-park values and compares base
callsigns, so `G4TGJ/P` on the air matches `G4TGJ` in the log.

Filters: program (both / POTA / SOTA), band, mode group (CW · Phone · Data)
and **Not yet worked**, which hides every activation whose reference is in the
log already.

## Hunting: tune and stage

Clicking a row does two things:

1. **Tunes VFO A** to the spot — band, frequency and mode — through the same
   path a DX-cluster spot click uses (the mode comes from the spot's mode
   token; SSB picks the sideband by band, data modes select USB).
2. **Stages the hunt.** The strip at the bottom of the window shows the
   activator, reference and what the next contact will carry.

The staged hunt is a draft for **one** contact. It is taken, exactly once, by
whichever contact starts next:

- **Log … @ kHz** in the hunt strip quick-logs the activator at the current
  dial with the reference.
- **QSO Log → Add…** opens the editor prefilled with the activator, frequency,
  mode and reference, so reports and a name can be entered first.
- Quick-logging from the TX console (or the crab's log command) with the
  activator's callsign also applies it.

If the next contact is with someone else — another station answers your CQ
first — that contact carries no park or summit reference and the hunt is gone:
click the spot again for the activator. A stale hunt never reaches the contact
after the one it was staged for. **Clear** forgets it without logging.

## Which fields, in which direction

HermitSDR writes the ADIF 3.1.4 program fields with the hunter/activator
direction kept straight:

| Field | Meaning | Written when |
| --- | --- | --- |
| `POTA_REF` | the **other** station's park | a POTA hunt is applied |
| `SOTA_REF` | the **other** station's summit | a SOTA hunt is applied |
| `MY_POTA_REF` | **your** park | your POTA activation reference is set in Settings → Station |
| `MY_SOTA_REF` | **your** summit | your SOTA activation reference is set in Settings → Station |

A hunt sets only the other station's field for its program and clears the
other three before doing so. Your own references, when set, ride on **every**
contact the app logs — quick logs, the editor's new contacts and hunts alike —
which is what an activator wants and what a hunter must leave empty. Clear
them in Settings → Station when the activation ends; the window shows an
"Activating" reminder while they are set. Several references stay
comma-separated (`US-1234,US-5678` for a two-fer), following the ADIF
convention the programs' uploaders accept.

All four fields are plain ADIF fields in the logbook: they appear in the
contact editor, survive import, edit and export, and are included in the QRZ
Logbook / eQSL / Club Log / Wavelog upload payloads. Cabrillo export is
unchanged. HermitSDR does **not** submit logs to the POTA or SOTA databases;
export ADIF and upload it through the programs' own sites.

## Privacy and bounds

- Off by default; nothing is fetched until the feeds are turned on.
- Two fixed public HTTPS GETs per poll, every 90 seconds, with revalidation.
- No station data is sent; no credentials exist for this feature.
- Bodies over 2 MiB are refused unparsed; at most 400 spots are kept.
- The feature cannot transmit, arm, key or post spots.
