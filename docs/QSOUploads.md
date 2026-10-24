# QSO uploads

Source version **2026.1023_003**, issue #266. Open **Log → QSO Log →
Uploads…**, or **Settings → Station → QSO upload settings…**. QRZ Logbook,
eQSL, Club Log and Wavelog are independently **off by default**. LoTW/TQSL
and logger broadcasts remain separate.

## Configure an account

Choose QRZ Logbook, eQSL, Club Log or Wavelog in the top selector. **Receipts**
shows delivery history; upload/retry controls stay visible above the scroll area.

Enter the account settings, save credentials, then apply the account settings
with automatic uploads enabled. Secrets go into the build's Keychain service;
they are never stored in defaults, the Settings mirror, the outbox or receipts.
Dev and Release namespaces remain separate. Opening the configuration checks
whether a credential exists; an idle launch with uploads off does not read it.

| Service | Settings | Secret |
| --- | --- | --- |
| QRZ Logbook | An eligible QRZ subscription and its logbook | Logbook API key, separate from callsign-lookup credentials |
| eQSL | Login callsign; optional case-sensitive QTH nickname | eQSL password |
| Club Log | Account email and station callsign | Application Password and developer/application API key; do not enter the main account password |
| Wavelog | HTTPS installation URL, including any subdirectory; numeric station profile ID | Read/write API key for that profile |

Wavelog URLs may end in `/index.php`; HermitSDR appends the API route. HTTP,
embedded URL passwords, query strings and fragments are refused. TLS uses the
system's normal certificate checks, and credential-bearing POSTs never follow
redirects. No actual service credential or live contact was used for the
implementation fixtures. Club Log's developer key must be supplied by the
operator; HermitSDR does not bundle another application's key.

## What is sent

A fresh contact is queued after its local log file is saved. Existing contacts,
ADIF imports and backup restores do not automatically upload. Select older
contacts in the logbook and use **Upload selected** to submit them explicitly.
The batch limit is 2,000 contacts. Already accepted contacts for the same
configured destination and contact identity are coalesced, including after
restart. Identity includes call, UTC second, band, mode/submode and station.

Uploads include the contact identity, reports, station/grid, standard location,
contest, award/park/summit, propagation/satellite and QSL-message fields when
present. Private COMMENT text and arbitrary imported application fields are
excluded. FT4 retains its ADIF MFSK/FT4 mode/submode. The original station
callsign is preserved. QRZ inserts never request destructive REPLACE behavior.
Changing a contact's identity cancels stale waiting snapshots and prevents its
new identity inheriting an old acceptance stamp. Select and upload the corrected
contact explicitly. Editing an already uploaded contact does not overwrite a service's log; manage
corrections there. Removing a local contact cancels its waiting upload and does
not delete anything remotely. Edits/removals made while the outbox is still
loading are applied before it can send a stored snapshot.

## Receipts and retries

The logbook adds a separate status column for each enabled service or service
with retained receipts; unused services add no empty columns. Each shows its state; hover for the reason
or open Uploads for recent receipts.

| State | Meaning and action |
| --- | --- |
| Queued | Waiting for an enabled matching account and the pacing interval |
| Sent · awaiting reply | The outbox has a durable write-ahead marker; POST is in progress |
| Accepted | A recognized service receipt confirms acceptance; this is not a QSL confirmation |
| Already present | The service reported a duplicate; no replacement was requested |
| Retry pending | A connection could not be established, or the service returned busy/maintenance; retry within bounds |
| Rejected | Check contact/account fields; **Resend failed** permits a deliberate new attempt |
| Rejected · account | Fix and save credentials; this destination is suspended until then |
| Check service | An interrupted POST or unreadable receipt might already have been accepted; check the service's log before **Review interrupted…** |
| Cancelled | Removed locally or credentials changed before sending; select the contact and use Upload selected if desired |

Automatic retries cover known connection failures and busy/maintenance replies,
with increasing delays, a maximum of five attempts and a minimum ten seconds
between requests to each service. A timeout, lost reply or restart with an
in-flight marker is not automatically retried: HTTP cannot promise exactly-once
remote delivery after an ambiguous failure. Explicit retry can submit again;
the service's duplicate rules apply. Wavelog merges duplicates itself.

Changing an account or installation URL cannot redirect old queued contacts.
Saving credentials creates a new non-secret Keychain reference and cancels
waiting items for the old reference. This matters for QRZ, where a different
API key can identify a different logbook. Select the contacts and Upload selected
to use the new credentials deliberately. Accepted receipts for the old account
remain in Receipts; table columns show only the currently configured account
and never inherit acceptance from a different destination. Ordinary Resend failed never migrates a contact to a changed
account. Turning an account off pauses its queue and interrupts its active POST;
an interrupted delivery needs review.

The outbox is `qso-uploads.json` beside the local logbook in the build's
Application Support folder. It is atomically saved with private file permissions,
retains at most 10,000 receipts and 2,000 pending requests, and caps queued ADIF
payloads at 8 MiB. Accepted payloads are discarded while their duplicate
receipts remain. Each ADIF payload is capped at 128 KiB and each response at 64 KiB;
HTTP encoding and credential fields add their normal request overhead.
**Cancel waiting** frees pending capacity without deleting contacts or receipts.
A full or unreadable outbox leaves the log local with a visible status; an
unreadable file is preserved rather than replaced. Retain it with logbook backups.
Shutdown flushes pending contacts synchronously after the local log's final save.

## Protocol references and validation

The native implementations use the public wire contracts, without copying
another logger's code or adding dependencies:

- [QRZ Logbook API](https://www.qrz.com/docs/logbook/QRZLogbookAPI.html): form POST, INSERT, count and result receipt.
- [eQSL real-time interface](https://www.eqsl.cc/qslcard/ImportADIF.txt): multipart Filename and login fields, record-level QTH nickname, interface marker and one-record result/error messages.
- [Club Log's real-time example form](https://clublog.org/test_realtime.html) and [API usage policy](https://clublog.freshdesk.com/support/solutions/articles/3000023706-excessive-api-usage): realtime endpoint and form fields, paced individual uploads. The old linked real-time article returned 404 during this review; unknown replies remain unconfirmed rather than being marked accepted.
- [Wavelog API](https://docs.wavelog.org/developer/api/) and its [controller](https://github.com/wavelog/wavelog/blob/master/application/controllers/Api.php): JSON ADIF request with station profile and explicit created/count/error receipt.

`QSOUploadTests` uses scripted transports, an in-memory secret store, temporary
outboxes and URLProtocol HTTP stubs. It covers wire encoding, success/duplicate/
authentication/malformed replies, destination and credential changes, cancellation,
restart and corruption recovery, write ordering, queue limits, byte bounds and
retry limits. These are local software checks; live accounts and service-side
behavior remain operator acceptance, tracked in source issue 293.
