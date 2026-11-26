# Contest logger

Available in the release after **2026.1101_001** (#316, first slice).

Open **Log → Contest Tools → Contest Logger**. The window is a log-only contest logger: it chooses a
rule set, validates the exchange, flags dupes while you type, scores the
contest live and hands the contacts to the existing
[Cabrillo 3.0 exporter](Logbook.md#cabrillo-export). Nothing in it keys,
arms or sends anything — ESM / F-key CW and voice message sending is a
separate, transmit-gated milestone and is deliberately absent here.

## Rule sets

Rules are data (`ContestRuleSet`, `HermitSDR/Integration/Logbook/ContestRules.swift`),
each with a version, the sponsor's URL and the revision transcribed. Three ship:

| Rule set | Exchange | Dupes | QSO points | Multiplier | Cabrillo |
| --- | --- | --- | --- | --- | --- |
| **ARRL Field Day** (2026 rules, rev. 2026-03-01, [arrl.org/field-day-rules](https://www.arrl.org/field-day-rules)) | class + ARRL/RAC section (DX stations send `DX`) | once per band **per mode** (rule 6.3: phone, CW and digital are separate) | phone 1 · CW 2 · digital 2 (7.1) | one **power multiplier** for the whole entry — ×5 at ≤ 5 W from batteries/solar, ×2 at ≤ 100 W or QRP on mains/generator, ×1 above 100 W (7.2); sections are counted for information only | `ARRL-FD`, MIXED, QSO lines **without** signal reports |
| **CQ WW DX SSB** ([cqww.com/rules](https://www.cqww.com/rules/)) | RS + CQ zone | once per band (IV.B) | different continent 3 · same continent 1 · both in North America 2 · same country 0 but still a multiplier (IV.B) | each CQ zone and each country **per band** (IV.C); total = points × (zones + countries) (IV.A) | `CQ-WW-SSB`, SSB |
| **CQ WW DX CW** (same rules) | RST + CQ zone | once per band | as SSB | as SSB | `CQ-WW-CW`, CW |

Field Day allows 160–10 m (no 60, 30, 17 or 12 m) and 50 MHz up; CQ WW the
six bands 160–10 m. The logger shows when the dial is outside the contest's
bands or the mode is not a contest mode, but it still logs — the sponsor's
checker, not the logger, decides what counts.

A serial-number exchange (`STX` / `SRX`) is supported by the model and
tested with a synthetic rule set; no serial contest ships in this slice.

**Known gaps against the sponsors' scoring.** CQ WW counts the WAE
multipliers (IT9, GM/Shetland, TA1, 4U1V, JW/b) and IG9/IH9 as separate
countries; the installed cty.dat (DXCC) does not split them, so the
sponsor's score can be a little higher than the window's. A contact whose
country the file cannot resolve (an unknown prefix, `/MM`) earns no CQ WW
points here and is counted as *unresolved*; its zone still counts if you
typed one. Field Day bonus points (rule 7.3) are claimed on the ARRL entry
form, not in the logger.

## Session

Pick the rule set (locked while a contest runs), fill **Your exchange** — the
Field Day class and section with the power category, or your CQ zone — and
press **Start**. The session (`contest.session.v1` in the defaults) remembers
the rule set and its version, the start and end times, the sent exchange, the
power category, the next serial, the imported MASTER.SCP and the name of
each contest's call-history file. **End contest…**
stamps the end time and opens the Cabrillo sheet; **Reopen** lifts the end
time; **New session** forgets the session (never the contacts).

The contest's contacts are the logbook's contacts whose `CONTEST_ID` equals
the rule set's Cabrillo token and whose time lies inside the session. There
is no second store: edit or delete a contact in the QSO Log and the score
follows. A contact deleted from the recent list is removed through the same
backed-up logbook replace as the QSO Log, and a serial already sent is never
reused (the next serial only ever increases).

If the rules are re-transcribed after a session started, the window says the
edition changed and scores with the current one.

## Entry

The call field has focus when the window opens. Fields follow the rules:
Field Day shows **Class rcvd** and **Section rcvd**; CQ WW shows **RST sent**
(prefilled 59 / 599 for the current mode), **RST rcvd** and **Zone rcvd**.
Tab moves between fields; **Enter** in any field fills the next empty field,
or logs the contact when every field is valid (a field pre-filled from a
[call-history file](#call-history-optional) is confirmed first); **Esc** clears the row. The
frequency, band and mode come from the current receiver.

Validation: callsigns are letters, digits and portable slashes with at least
one letter and one digit; sections must be one of the 85 ARRL/RAC sections
([contests.arrl.org](https://contests.arrl.org/contestmultipliers.php?a=wve):
`CT`, `EMA`, … `GH`, `PE`, `TER`) or `DX`; zones are 1–40 (typed `5` becomes
`05`); classes are 1–99 followed by A–F; phone reports have two digits and
CW / digital three.

While you type, the row to the right of the entry shows **DUPE** with the
earlier contact's UTC time, band and mode when the call was already worked in
the dupe scope (band, or band + mode for Field Day), otherwise the country,
zone, the points the contact would earn (CQ WW) and **NEW ZONE** / **NEW
COUNTRY** when it would be a fresh multiplier on this band.

### Super Check Partial (optional)

**Load MASTER.SCP…** copies a plain-text callsign list (one call per line,
`#` comments) into Application Support (`contest/MASTER.SCP`) and shows up to
ten suggestions under the call field once two characters are typed —
prefix matches first, then calls containing the fragment; a suggestion
already worked in the dupe scope is drawn in the danger colour. Clicking a
suggestion fills the call and moves to the first exchange field. Nothing is
downloaded; obtain the file from the Super Check Partial project yourself.
**Remove SCP** deletes the copy.

### Call history (optional)

A call-history file lists, per callsign, the exchange that station sent in
earlier contests. With one loaded, entering a call fills the **empty**
received fields with what the file expects, so you confirm by ear instead of
typing. Available in the release after **2026.1115_001** (#423).

**Loading.** Footer → **Call history → Load file for …** copies the file
into Application Support (`contest/CallHistory/<rule set>.txt`). There is
one file per rule set; **Replace file…** swaps it, **Remove** deletes the
copy, and the choice is remembered across launches and sessions. Everything
is local: HermitSDR never downloads a history file and sends nothing about
it anywhere. Obtain files yourself, or build one from your own log (below).
The file is read and parsed off the main thread; a 50,000-line file imports
in about 0.1 s and a lookup takes a few microseconds.

**Format.** The N1MM Logger+ text format that other contest loggers also
read:

```
# comment lines start with #
!!Order!!,Call,Name,Sect,Exch1,UserText
K1ZZA,Pat,CT,3A,club station
W6ZZB,Sam,SCV,1D
```

- `!!Order!!` names the columns of the rows that follow. Column names are
  matched in any case: `Call`, `Name`, `Loc1`, `Loc2`, `Sect`, `State`, `CK`,
  `BirthDate`, `Exch1`, `Misc`, `Power`, `CqZone`, `ITUZone`, `UserText`,
  `LastUpdateNote`. Other names are ignored and listed in the status line.
- A file with **no `!!Order!!` line** is read in the N1MM default order, the
  list above. A first row that itself begins with `Call` is taken as the
  header.
- Rows are separated by commas, or by semicolons when the header (or the
  first row) has no comma. Missing trailing fields are empty; extra fields
  are ignored; blank lines and `#` lines are skipped. A field wrapped in
  double quotes loses the quotes and may contain the separator
  (`"Smith, John"`); two double quotes inside it stand for one. A quote in
  the middle of a field (`O"Brien`) is an ordinary character, and a line
  whose quote is never closed is split as if it had no quotes.
- Line ends may be LF, CRLF or CR. Text may be UTF-8 (with or without a
  byte-order mark), UTF-16 with a byte-order mark, or otherwise
  Windows-1252 — the Windows code page, which reads a Latin-1 file
  identically and also gives `Š`, `ž`, `œ`, `€`, curly quotes and dashes
  their proper characters.
- A row without a plausible callsign is skipped and counted. When a call
  appears more than once, **the last row wins** and replaces the earlier row
  whole.
- `!!MapStateToSect!!` makes an empty `Sect` read the `State` column.
  `!!FourCharGridSq!!` and `!!ValidateArrlSection!!` are accepted and change
  nothing (no shipped exchange uses a grid, and sections are always
  validated).
- An import is refused, with the reason in the status line, when the file
  has no callsigns, has no column the current rule set can use, or is
  larger than 32 MB.

**What is pre-filled.** Each rule set maps history columns to its received
fields:

| Rule set | Received field | History column |
| --- | --- | --- |
| ARRL Field Day | Class | `Exch1` |
| ARRL Field Day | Section | `Sect` (then `State` under `!!MapStateToSect!!`) |
| CQ WW DX SSB / CW | Zone | `CqZone` |
| *(model only)* state or province | State | `State`, then `Exch1` |

Signal reports and serial numbers are never taken from history. A value
that is not valid for the field (an unknown section, zone 41, a class such
as `9Z`) is not offered at all. The state/province field exists in the
model for a state QSO party and is tested with a synthetic rule set; no QSO
party rule set ships yet. The file's `Name` and `UserText` are shown in the
hint line under the entry row and go nowhere else.

**Portable calls.** The lookup is a dictionary lookup on the call, trimmed
and upper-cased:

1. The call exactly as typed wins — a file may list `W1ABC/4` itself.
2. Otherwise a call that only adds `/P`, `/M`, `/QRP` or `/QRPP` reads its
   home call's row (`W1ABC/P` → `W1ABC`); the hint line says *home call*.
3. Anything else finds nothing. A call-area digit (`W1ABC/4`), a country
   prefix or suffix (`DL/W1ABC`, `W1ABC/VP9`), `/MM` and `/AM` put the
   station somewhere else, where the home call's section, state, zone and
   class no longer apply — so nothing is pre-filled.

**Unconfirmed until you say so.** A pre-filled field is drawn in italic
amber inside a dashed amber border, and a line under the row names the
source. It becomes an ordinary field when you type in it or press **Enter**
in it. Enter never logs a contact while another field still holds an
unconfirmed pre-fill: it moves there first, so each pre-filled value takes
one deliberate Enter. The **Log** button logs the row as shown. History
never replaces anything you typed, including text typed before the call was
complete; changing the call withdraws the untouched pre-fills of the
previous call and leaves typed and confirmed fields alone.

**What is logged.** Only what is in the fields when you log. Nothing about
the history file is written into the contact, so the ADIF and Cabrillo
exports contain what you logged and never what the history said.

**Review marks.** History goes stale. When a contact's logged exchange
differs from the file, the status line says so at once and the recent list
shows `history: Section CT` in the **Review** column, with the count in the
list's title. The mark is worked out from the log and the loaded file each
time: it follows edits in the QSO Log and disappears when the file is
removed.

Once you have checked a marked contact, **right-click it in the recent list
and choose Dismiss review mark**. The contact itself is not changed. A
dismissal hides exactly the difference you looked at: if you later edit the
contact, or replace the file, so that the note would read differently, the
mark comes back. **Call history › Show dismissed review marks** brings all
of them back; clearing the session forgets the dismissals. Dismissals are
kept with the contest session on this Mac and are never written into a
contact or an export.

**Build from my log…** writes a history file from your own earlier contacts
in the same contest, any year — the contacts whose `CONTEST_ID` is the rule
set's (CQ WW SSB and CW feed each other, since both exchange the zone). The
latest contact with each station wins. The file is saved where you choose
and is not loaded automatically.

## Score

Cards show QSOs (with dupes), points, the multiplier — zones + countries for
CQ WW, ×power for Field Day with the number of sections worked — the total,
and the contacts in the last 60 minutes. The table lists each band in the
rule set's order with contacts, CW / phone / digital counts, points, zones,
countries and dupes. Scoring runs off the main actor on a snapshot of the log
and the country file; a 100,000-contact log is filtered by `CONTEST_ID` first.

Dupes are the second and later contacts in a scope, in time order; they stay
in the logbook, score nothing and are marked DUPE in the recent list.

## What a contest QSO is in the logbook

An ordinary contact at the current dial and mode with the station callsign and
grid, plus standard ADIF fields only:

| Field | Content |
| --- | --- |
| `CONTEST_ID` | `ARRL-FD`, `CQ-WW-SSB` or `CQ-WW-CW` |
| `RST_SENT` / `RST_RCVD` | reports (CQ WW; Field Day has none) |
| `STX` / `SRX` | serials, when the rules use them |
| `STX_STRING` / `SRX_STRING` | the sent / received exchange without the report (`1D WMA`, `3A CT`, `05`, `23`) |
| `CLASS`, `ARRL_SECT` | Field Day class and section received |
| `CQZ` | CQ zone received |
| `MY_ARRL_SECT`, `MY_CQ_ZONE` | the section / zone you sent |

The QSO Log editor, ADIF export and logger broadcasts treat them like any
other contact.

## Cabrillo

**Export Cabrillo…** (or End contest) opens the QSO Log's Cabrillo sheet with
the header prepared from the session: `CONTEST`, `CATEGORY-MODE`,
`CATEGORY-POWER` (Field Day), the sent exchange, the claimed score, and the
callsign when the header had none; the selection is the contest id over the
session's exact period (start to end, the same contacts the score counts)
from the full log; switching **Contest session period** off in the sheet
gives the whole-UTC-day range instead. The rest of the header (name, address,
club, operators…) is the operator's persisted header as before.

Field Day QSO lines are written without the RST columns
(`QSO: 14250 PH 2026-06-27 1812 WU1T          1D WMA K1ABC         3A CT  0`),
through the header's new `signalReports` flag; headers saved before this
slice decode with the flag unset and keep writing reports. CQ WW lines follow
the sponsor's template
([cqww.com/cabrillo.htm](https://www.cqww.com/cabrillo.htm)):
`QSO:  3799 PH 2026-10-24 0711 N6TW          59  05     JT1Z          59  23     0`.

## Not in this slice

ESM / F-key message sending (CW or voice), Winter Field Day, a shipped
serial-number contest (CQ WPX), assisted/unassisted controls beyond the
Cabrillo header, shared serial allocation, per-radio contest profiles and
restoring pre-contest receiver settings on exit. For call history: a shipped
state QSO party rule set, automatic downloads of published files (by
design), and name, check, grid and ITU-zone exchanges.

Regression fixtures: `ContestRulesTests`, `CallHistoryTests`.

## Club Field Day scoreboard

Use **Log → Contest Tools → Club Field Day Scoreboard** with the same shared session key,
rule edition and power category at each position. Give each position a
different label. Start the local Field Day session before exporting its
journal. A later export from the same position records edits and
retractions, and extends the previous journal.

Use **Combine Journals** to merge copies. The scoreboard uses the longest
compatible history for each position. It rejects divergent histories and
counts a repeated call on the same band and mode according to the Field Day
dupe rule. The result is a QSO score. Field Day bonus points are separate.

Export JSON for further analysis or **HTML for Browser** for a read-only
snapshot containing the aggregate and position counts. The HTML carries no
calls, contact times or session key. Journal files carry contact data and
are exchanged manually.

### Private LAN sync

Open **Club Scoreboard → LAN Journal Sync** on each Mac. Agree on a session
key, rule edition and power category. Enter a different position name at
each Mac. At the host, enter the Mac’s private IP address and choose
**Start Host**. The default port is 7347. The host listens on that address
while the separate Scoreboard window is open. You can continue logging in
the Contest window.

Copy the invitation and share it privately with trusted participants.
A guest enters the host address, port and invitation, then chooses
**Join / Sync Now**. On the host, **Publish Local Changes** publishes the
host position’s own edits. Each sync sends the selected Field Day position’s
journal and returns the shared aggregate score. Every invited position
can receive the club’s contact journals. Invitations expire when the host
stops, and a new host run generates a new invitation.

The host stores accepted journals separately from the radio log and retains
them across restart. If the network drops, keep logging on each Mac and sync
again later. Retries of the same journal are safe. Positions can edit or
retract their contacts. Conflicting copies of one position’s history and
incompatible sessions are refused. Use **Export Scoreboard → HTML for
Browser** for a read-only TV or browser snapshot. Field Day has no shared
serial-number allocation. Other contest categories do not appear in LAN sync.
