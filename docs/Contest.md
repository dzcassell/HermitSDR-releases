# Contest logger

Available in the release after **2026.1101_001** (#316, first slice).

Open **Log → Contest**. The window is a log-only contest logger: it chooses a
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
power category, the next serial and the imported MASTER.SCP. **End contest…**
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
or logs the contact when every field is valid; **Esc** clears the row. The
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
Cabrillo header, call-history files, shared serial allocation, per-radio
contest profiles and restoring pre-contest receiver settings on exit.

Regression fixture: `ContestRulesTests`.

## Club Field Day scoreboard

Use **Log → Club Field Day Scoreboard** with the same shared session key,
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
