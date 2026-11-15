# Contest Calendar

Open **Log → Contests** to see which contests are on the air now and which
start in the next four weeks, in UTC: name, each operating period, modes,
bands, the exchange and a link to the rules, as far as your calendar file
provides them. It is information only. Nothing is tuned, keyed or uploaded,
and there is no account.

## Where the list comes from

HermitSDR ships **no contest list and contacts no contest calendar by
default**. You supply the list:

1. Download an iCalendar (`.ics`) contest calendar from a publisher you
   trust, or write a JSON list (format below).
2. Choose **Import File…**.

The window always shows the source (file name, or feed host) and when it was
imported. An import replaces the previous list; reminders you set stay with
contests that are still listed. Until you import something the window is
empty and says so.

A list older than **35 days** is not shown as current: the header chip
disappears, reminders stop, the assistant declines to say what is on, and the
window marks every row "unverified" until you import a newer file.

### About the WA7BNM Contest Calendar

The WA7BNM Contest Calendar (contestcalendar.com) is the usual reference.
Its terms of use (revision of 7 March 2025) do not allow software to fetch
the site automatically, and offer contest data to software authors only by
written agreement. They do allow using its ICS feed, when available, to load
contests into a calendar application for personal use. HermitSDR therefore
has no built-in connection to it. Read the terms on that site, and if they
cover what you want to do, download the calendar file yourself and import it.

### Optional feed address

**Calendar → Feed Settings…** lets you enter the HTTPS address of an
iCalendar or JSON feed whose publisher allows applications to read it. It is
off until you switch it on. When on:

- HermitSDR makes one request to the host shown in the window each time you
  choose **Refresh**, and at most one a week when the Contests window opens.
- Nothing about your station is sent: no callsign, grid, log or cookies.
  Redirects are not followed and the reply is limited to 2 MiB.
- A failed or unreadable reply keeps the previous list.

Switch it off again in the same sheet; no request is made while it is off.

## What the reader understands

iCalendar:

- Folded lines, CRLF or LF line ends, UTC times (`…Z`), times with a known
  `TZID`, and all-day dates.
- Times with no zone are read as **UTC** (how contest calendars publish
  them); the window says how many entries that applied to.
- A contest with several operating periods: either several events with the
  same name whose periods are within 48 hours of each other, or one event
  with `RDATE` values. Weekly repeats of the same name stay separate entries.
- `DTEND` or `DURATION`.
- Modes, bands, exchange and sponsor from description lines such as
  `Mode: CW`, `Bands: 80, 40, 20`, `Exchange: RST + serial`, or from
  `X-HERMITSDR-MODES`, `-BANDS`, `-EXCHANGE`, `-SPONSOR` properties. The
  rules link is the event's `URL`, or the first link in the description.
- Recurring events (`RRULE`), cancelled events and events without an end are
  skipped and counted, never guessed.

JSON (`schemaVersion` 1; times are ISO 8601):

```json
{
  "schemaVersion": 1,
  "contests": [
    {
      "name": "Example Club Sprint",
      "sessions": [
        { "start": "2026-11-21T14:00:00Z", "end": "2026-11-21T18:00:00Z" },
        { "start": "2026-11-22T02:00:00Z", "end": "2026-11-22T06:00:00Z" }
      ],
      "modes": ["CW", "SSB"],
      "bands": ["40m", "20m"],
      "exchange": "RST + serial",
      "rulesURL": "https://example.org/sprint/rules",
      "sponsor": "Example Radio Club"
    }
  ]
}
```

A contest with one period may use `"start"` and `"end"` directly in place of
`"sessions"`. Only `name` and the times are required.

## Using the list

- **On now / Next four weeks.** A contest between two of its periods is
  listed under the next four weeks with its next period.
- **Open in Contest Logger** appears for contests the native logger has
  rules for (ARRL Field Day, CQ WW DX SSB, CQ WW DX CW). It selects that rule
  set and opens **Log → Contest**; enter your exchange and press **Start**
  there. It will not switch rule sets while another contest session is
  running. Other contests show "No native rule set"; log those in the QSO
  Log.
- **Reminders.** Click the bell on a contest to get an in-app reminder before
  each of its periods starts (5, 15, 30 or 60 minutes; 15 by default) while
  HermitSDR is running. A start up to 30 minutes in the past is shown once on
  reopening.
- **"On now" chip.** Switch on **"On now" chip in the header** to show a chip
  in the main window header while a listed contest is running. Hover for the
  names and the list's age; click to open the Contests window. Off by default.
- **Ask The Crab.** "What contests are on this weekend?" or "Why is 20 m so
  busy?" is answered from the imported list, with its source and age. With no
  list, or an old one, the crab says so.

The list, feed address and reminder choices are saved per station profile in
`ContestCalendar.json` in the application support folder.
