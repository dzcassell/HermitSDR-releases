# DXpedition Calendar

Open **Log → DXpedition Calendar** to enter expedition plans in UTC. Each
plan has a callsign, entity, start and end, and optional bands, modes, source
link, notes, a Maidenhead grid and a recorded DXCC code. Use **Edit Plan** to extend, reschedule
or cancel it. Enable **Show ended and cancelled** to find older entries.

The calendar shows three different kinds of information.

- **Schedule** comes from the saved plan. “Scheduled now” describes its UTC
  window.
- **Log coverage** checks the exact callsign and, when you enter a DXCC code,
  the explicit DXCC field in local QSOs. It uses the log's recorded QSL
  sources. Calls without a recorded entity code can still match by callsign.
- **Cluster** shows a recent exact-call spot received inside the active
  window. **Tune to Spot** is an explicit frequency change on a live,
  disarmed receiver. It keeps the selected receive mode.

Mark a plan as a favorite for filtering. Choose **Remind at Start** to receive
an in-app reminder while HermitSDR is running. A start up to 30 minutes in the
past can be shown once on reopening if the window is still active. Extending
the end keeps the original reminder receipt. Changing the start allows a new
occurrence. The station profile owns its own plans and preferences.

**Plans → Export JSON** writes a portable version 1 file. Imports update
plans by UUID and keep the receiving station's favorites and reminder
receipts. Older publisher revisions are skipped. Duplicate IDs or invalid
rows leave the saved calendar intact.
Use **Import Plans…** or **Export Calendar (.ics)** to exchange
standalone events with calendar apps. For a third-party event, put the
expedition call at the beginning of its title and include a start and end.
Imports accept UTC, recognized time-zone identifiers and all-day dates.
An all-day event uses midnight UTC and an exclusive end date. Export
recurrences as individual events and use UTC for ambiguous clock-change
times. An older publisher revision cannot overwrite a newer one.
Exports carry stable IDs, UTC dates, source links and cancelled status.
Reminders stay in HermitSDR. Every line break in a note, including the
Unicode line and paragraph separators, is written as an escaped line break.
The format follows [RFC 5545](https://www.rfc-editor.org/rfc/rfc5545).

Choose **Plans → Refresh afu.tools Calendar…** to check the publisher’s
public DXpedition feed. Each refresh makes one HTTPS request. HermitSDR
shows when it last successfully checked the feed and keeps that snapshot
in the station profile. The publisher supplies announcement dates,
calls and source notes. Provisional prefixes and unsupported, malformed or
repeated events are skipped and counted; one bad event does not stop the
refresh. Bands and modes display as fields when the publisher
supplies them in the supported calendar extensions.

Cached announcements older than 24 hours, or omitted from a subsequent
snapshot, do not offer reminders or cluster tuning. A missing event does
not imply cancellation. Favorites and reminder receipts survive updates.
**Edit as Local Plan** keeps your correction as a local entry. The app
does not refresh in the background or send station data.
[afu.tools API documentation](https://afu.tools/api#dx-kalender)

Any website listed as a plan source opens when you choose its link.
If a plan has a grid, choose **Export Path Model Input…** from its row
to prepare a point-to-point prediction for the expedition’s model month.
Use **Plans → Open HF Path Outlook** to review results after running the
separate solver. [HF Path Outlook](HFPathOutlook.md)
