# QSL confirmations: LoTW, eQSL and QRZ Logbook

Source version **2026.1102_001**, issue #323 (first slice). Open **Log → QSO
Log → Confirmations…**. The window matches a confirmation document from one
service against the local log as a **dry run**, shows exactly what would be
written and why anything was left out, and only writes on **Apply**. Each
service is recorded in its own ADIF fields; a LoTW, an eQSL and a QRZ
confirmation on the same contact are three facts, never one bit. An upload
receipt (see [QSOUploads.md](QSOUploads.md)) is not a QSL.

## Sources

| Source | Download | Import | Recorded as |
| --- | --- | --- | --- |
| LoTW | Username + password (the LoTW window's Remember option keeps the password in the Keychain); incremental | `lotwreport.adi` saved from LoTW | `LOTW_QSL_RCVD=Y`, `LOTW_QSLRDATE`, `APP_LOTW_2XQSL`, `APP_LOTW_MODEGROUP`, `CREDIT_GRANTED`; the LoTW ✓ flag |
| eQSL | Only when eQSL upload credentials are already saved in **Uploads…**; otherwise import | The `.adi` from eQSL › Inbox › Download | `EQSL_QSL_RCVD=Y`, `EQSL_QSLRDATE` |
| QRZ Logbook | Only when a QRZ Logbook API key is already saved in **Uploads…**; otherwise import | An ADIF export, or a saved FETCH reply | `QRZCOM_QSO_DOWNLOAD_STATUS=Y`, `QRZCOM_QSO_DOWNLOAD_DATE`, `APP_QRZLOG_STATUS=C`, `APP_QRZLOG_LOGID` |

Nothing downloads at launch or on a timer. A download reads the saved secret
once, on the button, and encodes it straight into the one documented request:

- LoTW: `GET lotwuser/lotwreport.adi?login=…&password=…&qso_query=1&qso_qsl=yes&qso_withown=yes&qso_qsldetail=yes[&qso_qslsince=YYYY-MM-DD]`.
  `qso_qslsince` is the QSL-updated filter: the QSO-received filter would miss
  an old upload that was confirmed recently. The report's `APP_LoTW_LASTQSL`
  header becomes the next cursor.
- eQSL: `GET qslcard/DownloadInBox.cfm?UserName=…&Password=…[&QTHNickname=…][&RcvdSince=YYYYMMDDHHMM]`,
  then the one `.adi` link the page names, accepted only on the same host
  under `/qslcard/`. An empty inbox is not an error.
- QRZ Logbook: `POST logbook.qrz.com/api` with `KEY`, `ACTION=FETCH`,
  `OPTION=TYPE:ADIF,MAX:250[,MODSINCE:YYYY-MM-DD][,AFTERLOGID:n]`, walked by
  log id until a short page. A record is a QRZ confirmation only with
  `APP_QRZLOG_STATUS=C`; a relayed `LOTW_QSL_RCVD` inside a QRZ record is
  LoTW's confirmation and is ignored here (download the LoTW report for it).

Sessions are ephemeral, follow no redirects and cap a reply at 32 MiB. A
login failure, a web page instead of ADIF, HTTP errors and oversized replies
stop the download with a visible message; nothing is written.

## Incremental sync and the ledger

Each source keeps a **per-account** record (LoTW login, eQSL callsign plus QTH
nickname, or the QRZ destination hash — never a secret) with the last sync
time, the next cursor and a one-line summary; the status lines at the top of
the window show them. The cursor advances **only when a plan is applied**: a
download that was reviewed and dismissed is downloaded again next time.
Incremental requests start one day before the cursor so clock skew between
the service and this Mac cannot skip a confirmation; re-applying the overlap
changes nothing. **Full (ignore last sync)** downloads everything the account
has. The ledger lives in the build's defaults under `qslSync.v1`.

## Matching

A confirmation matches a logged contact on the same callsign, the same ADIF
band (derived from the frequency when the document gives only `FREQ`), the
same **mode family** and, when the document names a station callsign, the
same own station (the station setting stands in for contacts without
`STATION_CALLSIGN`). Mode families fold USB/LSB/SSB, AM/SAM/DSB and FM/NFM,
and use the submode when there is one, so `MODE=MFSK SUBMODE=FT4`, legacy
`MODE=FT4` and a logged FT4 contact are all FT4; bare MFSK is not.

- **Strict**: the document's own time precision — the exact second, or the
  exact minute for documents that give `TIME_ON` as HHMM (eQSL).
- **Loose**: within the time window (default ±15 min, 0–180) on the same call,
  band, mode family and station. A loose match is listed as `loose ±N s`;
  **Apply loose matches** off keeps them out of Apply for review.
- Several different logged contacts inside the window are **ambiguous** and
  stay unmatched; duplicate rows of one contact (same identity) all receive
  the confirmation and are counted as duplicate log rows.

Every unmatched record says why: no logged contact with that call, band
differs (with the logged bands), mode differs, station callsign differs, time
differs by N min (with the nearest logged contact), or ambiguous. Records a
document lists without a positive QSL are counted but never confirm. Records
without a usable identity (no call, date, band or mode) are skipped and listed.

## What Apply writes

For each matched contact: the source's own received flag and date (the newest
date when a report repeats a QSO), the source's provenance fields when the
report is unanimous, and **empty** geography fields (`DXCC`, `COUNTRY`,
`STATE`, `CNTY`, `GRIDSQUARE`, `VUCC_GRIDS`, `CQZ`, `ITUZ`, `IOTA`) filled
from the report. A recorded value that differs from the report is a
**conflict**: it is shown (`STATE: logged ON, LoTW says QC. Kept as logged.`),
the confirmation is still recorded, and the logged value stays. A longer
locator refining a shorter one is not a conflict. Only fields that actually
differ are written, so applying the same document twice changes nothing and
the second plan shows every entry as **Already recorded** while still
explaining its conflicts. A log backup is written before Apply, as for every
bulk change. Editing a contact's identity (call, time, band, mode, station)
removes every source's confirmation fields, as it already did for LoTW.

## Where confirmations show

- The QSO Log **QSL** column lists every source on the contact (`LoTW · eQSL`,
  `QRZ`, `QSL` for a recorded card), and the QSL filter adds **eQSL confirmed**
  and **QRZ confirmed**; **Unconfirmed** now means no source at all.
- **Awards** and **Statistics** offer **eQSL**, **QRZ Logbook** and **Any
  source** next to LoTW, QSL received and Either. LoTW's cross-mode rule is
  unchanged: a `APP_LOTW_2XQSL=N` contact counts in mixed totals but not in the
  band/mode matrix unless another selected source confirmed that mode.
- Worked World's confirmed layer accepts any recorded source.
- The **Coverage summary** in the Confirmations window counts contacts
  confirmed per source, per band and per mode family (plus QSL cards and the
  any-source total) as copyable text with no station fields.

The existing LoTW window's **Fetch LoTW confirmations** keeps its strict
same-second matcher and is unchanged.

## Validation

`QSLReconciliationTests` runs the anonymised fixtures under
`Tests/DSPTests/Fixtures/QSLSync` (a LoTW report with banner, duplicate rows,
an unconfirmed row and the bare `APP_LoTW_EOF` trailer; an eQSL inbox with
HHMM times, an explicit `EQSL_QSL_RCVD=N` and a record without a call; a QRZ
`FETCH` reply with a relayed LoTW flag) through strict and loose matching,
midnight, window edges, ambiguity, mode families, station checks, conflicts,
per-source fields, idempotent re-application and the coverage text.
`QSLSyncProtocolTests` pins the exact request for each service, the eQSL
link safety rules, QRZ reply unwrapping, and drives the real transport against
a loopback HTTP server for the LoTW cursor, the eQSL two-step and QRZ paging.
No live account was used; the service-side formats follow the public
documentation and need operator acceptance the way the upload services did.
