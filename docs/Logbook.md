# Logbook workspace

Available in **2026.0904_002**.

Open **Log → QSO Log**. The workspace supports adding and editing contacts,
ADIF import with a preview, selected-contact bulk changes/deletion, saved filters,
and full/filtered/selected ADIF export plus [Cabrillo 3.0 contest export](#cabrillo-export). **Awards…** uses a snapshot of the current
filtered results; see [Awards.md](Awards.md). **World & radar…** opens the live
[worked-world view](WorkedWorld.md) with its own filters. **Statistics…** opens
the live [statistics window](#statistics).

Every contact that enters the log can also be broadcast to an external logger
as it is committed — the WSJT-X UDP *QSO Logged* / *Logged ADIF* messages and
N1MM `contactinfo` / `contactreplace` / `contactdelete` packets; see
[LoggerBroadcasts.md](LoggerBroadcasts.md) (off by default).

## Online logbook uploads

**Uploads…** configures optional QRZ Logbook, eQSL, Club Log and Wavelog
uploads, off by default, with Keychain credentials and per-contact receipts.
New contacts upload after the local disk save; imports/restores stay local.
Selected-contact upload, bounded retries and interrupted-delivery review are
in [QSOUploads.md](QSOUploads.md). LoTW behavior is unchanged.

## Import and preservation

The streaming ADI parser reads 64 KiB chunks and consumes each value by its
length, including values containing literal `<EOR>` text. It accepts typed and
unknown contact fields and retains relevant USERDEF header definitions. Export
preserves these fields, original station identity and mode/submode pairs. As of 2026.0905_001,
semantic whitespace around imported modes/submodes is normalized consistently;
native NFM exports as FM, and DSB/SAM as AM, per the ADIF mode enumeration. A
conflicting user-field definition stops export before replacing the destination.

ADIF 3.1.4 ADI is ASCII. Existing UTF-8 byte-length exports are accepted and
preserved as a compatibility extension, with a visible preview notice. ADX/XML
is not supported. Source:
[ADIF 3.1.4 specification](https://www.adif.org/314/ADIF_314.htm).

Validation identifies the record and field. It rejects missing contact identity,
invalid UTC dates/times, malformed lengths/tags, duplicate fields, invalid grids,
and inconsistent known frequency/band combinations. Frequency-only records use
all 33 ADIF band ranges; band-only records do not acquire an invented frequency.
Bounds: 1 MiB per field, 512 fields per record, 512 MiB per file, one million
contacts per import. An invalid record aborts the whole preview; no partial log
mutation occurs.

Import offers **Skip duplicates** or **Keep both**. Identity comprises call,
whole UTC second, band, ADIF mode/submode identity and station callsign. The
current log is checked again when committing; a contact arriving during backup
causes the operation to stop for review. Existing contacts are not overwritten.
Keep both creates distinct internal IDs. Missing station identity is not guessed
for duplicate detection.

The editor retains unknown fields. Changing call, timestamp, band, mode, or
station callsign clears old received confirmations and award credits.
Comment/location edits retain them. Quick logging, AI quick logging and FT8/FT4 auto-logging capture the current
station callsign/grid; FT8/FT4 also retain the exchanged grid and reports.

## Cabrillo export

Available in the release after **2026.1020_001** (#269). **Export → Contest →
Cabrillo 3.0…** in the QSO Log opens a sheet with the per-contest header, the
contact selection and a preview. The writer is `CabrilloExport`
(`HermitSDR/Integration/Logbook/CabrilloExport.swift`), compiled by the test
package; the sheet is `CabrilloExportView`. ADIF export is unchanged.

**Header.** The form holds CALLSIGN, CONTEST, CATEGORY-OPERATOR / ASSISTED /
BAND / POWER / MODE / STATION / TIME / TRANSMITTER / OVERLAY, CLAIMED-SCORE,
CLUB, LOCATION, GRID-LOCATOR, NAME, ADDRESS (up to 6 lines of 45 characters),
ADDRESS-CITY / STATE-PROVINCE / POSTALCODE / COUNTRY, EMAIL, OPERATORS,
SOAPBOX and the fixed **sent exchange** (zone, section, state…). It is saved
to `logbook.cabrillo.v1` in the defaults as you type, so it is filled once per
contest. Only CALLSIGN and CONTEST are required; CONTEST is normalised to
`A–Z 0–9 -` (32 characters) and CLAIMED-SCORE must be a whole number or blank.
Optional lines that are blank are written blank. CREATED-BY is
`HermitSDR <version>`; OPERATORS defaults to the entry callsign. Lines end
with LF. The file ends with `END-OF-LOG:`.

**Contacts.** Current filter (the workspace query), a saved filter, or the
full log, optionally narrowed to a **UTC day range** (whole UTC days, from
00:00:00Z of the first day through 23:59:59Z of the last) and to contacts
whose ADIF `CONTEST_ID` matches. Contacts are written in UTC time order
(then call, then frequency) regardless of the table sort, so the same contacts
always produce the same bytes; the regression suite pins a 1,000-contact
synthetic log by SHA-256.

**QSO lines** follow the public v3 template, one space between columns:
`QSO: freq(5, right) mo(2) yyyy-mm-dd hhmm sent-call(13) rst(3) exch(6)
rcvd-call(13) rst(3) exch(6) t`. Values wider than a column extend it. The
frequency is the logged frequency in kHz (rounded) below 30 MHz; above it the
band token from the spec (`50`, `70`, `144`, `222`, `432`, `902`, `1.2G` …
`241G`, `LIGHT`). A band-only contact writes the band's token (`7000` for
40 m). The sent call is the header CALLSIGN; a logged `STATION_CALLSIGN` that
differs is flagged, not rewritten. The transmitter column is always `0`.

**Mode mapping** (HermitSDR demodulator names and ADIF modes/submodes):

| Cabrillo | Logged mode |
| --- | --- |
| CW | CW |
| PH | USB, LSB, SSB, AM, SAM, DSB, DIGITALVOICE, FREEDV, C4FM, DSTAR, DMR, M17 |
| FM | FM, NFM, WFM |
| RY | RTTY |
| DG | DATA-U, DATA-L, FT8, FT4, MFSK, JS8, JT65, JT9, Q65, WSPR, PSK31/63/125, OLIVIA, CONTESTIA, THOR, DOMINO, HELL, PKT, RTTYM, MT63, MSK144, SSTV, FAX and the other digital modes listed in `CabrilloExport.digitalModes` |
| DG (flagged) | anything else — written as DG and listed in the preview |

**Exchanges and reports** come from stored fields only: RST from `RST_SENT`
/ `RST_RCVD`; the sent exchange from `STX_STRING`, else `STX` (serials under
three digits are zero-padded), else the form's sent exchange; the received
exchange from `SRX_STRING`, else `SRX`, else — flagged — from a `COMMENT` that
says `EXCH: value` / `EXCHANGE value` or consists of one short token (at
most 6 characters, at most 4 when letters only). A
missing RST is written as the mode's conventional 59 / 599 and flagged. A
contact with no exchange is written with the column **empty** and listed in
the preview under "missing an exchange"; the export never invents one. Fix
them in the contact editor (`SRX`, `SRX_STRING`, `STX`, `STX_STRING`,
`RST_SENT`, `RST_RCVD`) or submit as is. The file is written to a sibling
scratch file and renamed only after a complete write, like ADIF export.

Format reference: [Cabrillo v3 header](https://wwrof.org/cabrillo/cabrillo-v3-header/)
and [QSO data](https://wwrof.org/cabrillo/cabrillo-qso-data/). Regression
fixture: `CabrilloExportTests`.

## Statistics

Available in the release after **2026.1020_001** (#270). **Statistics…** in the
QSO Log opens a window with one chart and one table per breakdown: contacts per
**UTC day**, **month** and **year**, per **band**, per **mode** (ADIF mode, so
USB/LSB count as SSB and SAM as AM, as in the award matrix), per **DXCC entity**
and per **continent**, each split into confirmed and unconfirmed contacts. Six
cards summarise contacts, confirmed share, unconfirmed, active days with the
first → last UTC span, resolved entities and continents.

**Scope.** *Current filter* applies the workspace query exactly as the table
shows it (search, band, mode, QSL, UTC dates); *Full log* ignores it; any
**saved filter** can be chosen by name. The window is live: a log change (edit,
import, restore, quick log, LoTW batch), a filter change or a saved-filter change
recomputes, and the chart shows the newest inputs only. **Confirmed by** is LoTW,
a recorded `QSL_RCVD=Y`, or either (the default), remembered in
`statistics.confirmation`.

**Resolution.** Day/month/year buckets are UTC civil dates computed by integer
arithmetic from the stored timestamp, never through the Mac's time zone or
locale; a contact at 23:59:59Z and one at 00:00:00Z fall in different days,
months or years exactly as ADIF `QSO_DATE` would place them. DXCC follows the
awards rules: an explicit ADIF `DXCC` code wins (named from the bundled entity
table; an unknown code is shown as `DXCC <code>`), `/MM` and `/AM` are in no
entity, otherwise the installed `cty.dat` infers the entity. Continents come
from the country file's header for each callsign (`NA`, `EU`, …); without a
country file every continent is *Unknown*. Unresolved entities and unknown
continents are counted in their own trailing row so each table sums to the
contact count.

**Charts and tables.** Native Swift Charts in the active palette (Light and
Dark): days as two lines (contacts, confirmed) over a UTC date axis, the other
breakdowns as stacked confirmed / unconfirmed bars in the table's order (bands by
frequency, modes alphabetically, entities and continents by count; the entity
chart shows the top 30). The table beneath lists every row with contacts,
confirmed, unconfirmed and share, 500 rows per page.

**Export CSV…** writes one table through the save panel:
`HermitSDR-statistics-<table>.csv` with the scope, confirmation source, totals
and the rows. The bytes are deterministic for a given log, scope and
confirmation source (no timestamps, versions or timings), cells are quoted and
formula prefixes neutralised, and no callsign, station setting, comment or
credential is written; the regression suite pins a 1,000-contact synthetic log
by SHA-256 for every table.

**Computation.** `LogbookStatistics` (`HermitSDR/Integration/Logbook/
LogbookStatistics.swift`, compiled by the test package) is pure in its inputs.
`LogbookStatisticsEngine` runs it on its own serial queue
(`HermitSDR.logbook.statistics`, never the main actor and never the disk lane)
and caches snapshots per **log revision** (`LogbookWindowModel.revision`, bumped
on every distinct log publication) and request: an unchanged log, scope and
confirmation source is served from the cache, a new revision evicts every older
entry, and the window keeps at most one computation in flight, folding requests
that arrive meanwhile into one run. Measured on the optimised 100,000-contact
fixture below: **0.15 s** for the full log, 0.19 s with a search filter, 1 ms
for the CSV; the unoptimised test build takes about 0.42 s. Logbook persistence
is unchanged. Regression fixture: `LogbookStatisticsTests`.

## Callsign lookup (QRZ.com and HamQTH)

Available in the release after **2026.1020_001** (#265). Off by default.
**Settings › Station › Look up station details for logged contacts** turns
it on; pick **QRZ.com** or **HamQTH**, enter the username (saved in the
defaults like the LoTW login) and the password (saved in the macOS Keychain
under `callsignLookupPassword.qrz` / `callsignLookupPassword.hamqth`, never
in `Settings.plist`, the log or diagnostics). The status row underneath
reports the current state: *No account*, *Ready*, *Looking up CALL…*, the
last result, *CALL not found*, *Login rejected: …*, *Session expired* or a
network/HTTP error. QRZ.com returns the complete record with an XML Logbook
Data subscription and the public part of it otherwise (the reply's message
is shown); HamQTH is free.

**When.** After every logged contact — the LOG IT button, the Crab's quick
log and the FT8/FT4 sequencer's auto-log — the contact is appended first and
the lookup runs afterwards; logging never waits for it and a failed lookup
only updates the status row. The contact editor (Add… / Edit…) has a
**Look up** button beside the callsign for a contact on demand. ADIF imports
are not looked up automatically (an import can be thousands of contacts);
use the editor for individual ones.

**What is filled.** `NAME`, `QTH`, `GRIDSQUARE`, `COUNTRY`, `DXCC`, `STATE`,
`QSL_VIA`, `EMAIL`, `CQZ` and `ITUZ` — only fields that are still empty when
the reply arrives. Anything typed, imported or already filled is never
overwritten, so a second lookup after an edit changes nothing the operator
wrote. A grid is written only if it is a valid 2–8 character locator; a DXCC
or zone only if it is a plausible number. The provider and the UTC lookup
time are recorded on the contact as `APP_HERMITSDR_LOOKUP_SRC` (`QRZ` or
`HAMQTH`) and `APP_HERMITSDR_LOOKUP_TIME` (`YYYYMMDDHHMMSS`); both export
with the ADIF record and survive import, and the editor shows them as
"Station details from QRZ.com, looked up 2026-10-22 12:34Z".

**Sessions.** One session per provider: QRZ.com `?username=…;password=…;
agent=HermitSDR-<version>` → session key, then `?s=KEY;callsign=CALL`;
HamQTH `/xml.php?u=…&p=…` → session id, then `/xml.php?id=…&callsign=…&
prg=HermitSDR-<version>`. A "Session Timeout" / "Invalid session key" (QRZ)
or "Session does not exist or expired" (HamQTH) reply signs in again once
and repeats the lookup; a second expiry in a row is reported. HamQTH
sessions last one hour, so the client renews at 55 minutes before asking.
Changing the username, password or provider forgets the session. Requests
go through an ephemeral `URLSession` with no cookies and no URL cache, so
the login URL (which carries the password) is never written to disk.
Credentials are percent-encoded strictly (`+`, `;`, `&` included).

**Bounds.** At most one request per second and **60 requests per 10
minutes** (logins included); beyond that a lookup is refused immediately
with *Too many lookups* and no request is sent. Successful replies live in
a 512-entry LRU cache for 24 hours (not-found is not cached). At most 32
lookups wait in line. Disabling the feature, quitting, or changing the
provider cancels the in-flight request, drops the queue and forgets the
session. Replies are read with a bounded XML reader (depth 8, 512 fields,
4 KiB per value, 1 MiB per body).

Sources: [QRZ.com XML interface specification](https://www.qrz.com/XML/current_spec.html),
[HamQTH XML developer page](https://www.hamqth.com/developers.php). No
provider was contacted during fixture validation; `CallsignLookupTests`
replays recorded reply shapes (success, not found, expiry → re-login,
malformed, HTTP error) through a scripted transport and pins the
fill-only-empty rule, the cache, the rate window and cancellation.

## Persistence and recovery

The existing `Application Support/HermitSDR/qsolog.json` array remains the format.
New fields are optional, so old logs load without conversion. The first load
creates an exact `qsolog.pre-workspace.json` snapshot once. Profiling did not
justify a database migration.

All normal reads, full snapshots and atomic writes run on a serial utility lane.
Saves coalesce to the newest revision, reject stale writes, and show **Saving**,
**Saved locally**, or a retryable error. Edits, bulk operations, imports, restores
and LoTW confirmation batches create complete, uniquely named files in
**Logbook Backups** first. Restore replaces the full log and backs up the current one. An unreadable source stays
untouched until explicit recovery, when its original bytes are retained too.

Shutdown disconnects the radio first, then flushes the latest contact snapshot.
If the startup load has not returned, pending quick logs are merged on the disk
lane; an unreadable original instead leaves those pending contacts in a separate
recovery backup. No disk operation runs in a DSP/audio callback.

## LoTW identity

Confirmation downloads request station identity and QSL detail. Matching requires
a positive QSL, exact exported UTC second, call, band, mode/submode and station
callsign. Fractional local timestamps are truncated as in ADIF export. Missing or
ambiguous identity does not confirm a broad call/band group. Conflicting locations
in duplicate reports do not supply a guessed location. The documented terminal
`APP_LOTW_EOF` marker is accepted. Existing Keychain and ephemeral-session behavior
is unchanged; live LoTW requests were not made during fixture validation.

[ARRL LoTW developer query reference](https://lotw.arrl.org/lotw-help/developer-query-qsos-qsls/).

## Measured large-log budget

Run `tools/logbook-benchmark.sh /path/to/artifacts` to generate a deterministic
100,000-contact ADIF/JSON fixture and exercise the real parser, exporter, queries,
duplicate policy, editing and award engine. Recorded on the development Apple
silicon Mac, optimized Swift 6, 2026-09-04:

| Operation | Measured | Target |
| --- | ---: | ---: |
| Stream import 100,000 contacts | 1.13 s | 5 s |
| Filter and sort 100,000 contacts | 0.14 s | 1 s |
| Sort only | 0.04 s | 1 s |
| 200 slices of 500 rows | 0.003 s | 0.1 s |
| Check 100,000 duplicates | 0.11 s | 2 s |
| JSON encode / decode | 1.35 / 1.58 s | 5 s each |
| Stream ADIF export | 2.25 s | 5 s |
| Recompute all award families | 0.22 s | 2 s |
| Worked-world snapshot | 0.28 s | 2 s |
| Statistics snapshot (full log / search filter), 2026-10-22 | 0.15 / 0.19 s | 2 s |
| Match 100,000 LoTW confirmations | 0.15 s | 2 s |

Native Debug UI was exercised in muted Demo with a separate application-support
home: 100,000 contacts loaded; a grid filter returned exactly 50,000; editing
retained imported fields and created a verified pre-edit backup; full export
wrote 100,000 records in 3.8 seconds from the Save click under concurrent build
and test load. Further native checks added two contacts, rejected an invalid date
and bulk grid, bulk-updated both valid grids, then deleted both with backups.
The resulting log exactly matched the original 100,000 contacts. Duplicate import,
saved filters, award drill-downs and backup restoration were also exercised.
Tables retain only 500 rows per page; search is debounced 140 ms
and runs off the main actor. Budgets describe this fixture and machine, not a
universal hardware guarantee. No radio transmission is needed for these checks.

Regression fixtures: `LogbookWorkspaceTests`, `LoTWContactMatchingTests`,
`QSOAwardsTests` and `LogbookStatisticsTests` in `Tests/DSPTests`.
