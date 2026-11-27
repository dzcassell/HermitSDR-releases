# Net Scheduler

Open **Log → Net Scheduler** to keep a list of the nets you listen to: the
weekly club net, a daily maritime net, a monthly swap net. For each one
HermitSDR works out when it meets next, reminds you before it starts, and
tunes the receiver to it with one click.

It is receive only. **Tune**, **Tune Now** and every automation that reaches a
net set the receive frequency, the mode and (if you entered them) the filter
and a receive preset. Nothing here arms, keys or changes a transmit setting,
and the dial is not moved while the transmitter is busy.

The list is yours and stays on this Mac (`Nets.json` in the application
support folder). Nothing is fetched and nothing is sent anywhere.

## Adding a net

Choose **Add…** and fill in:

| Field | Meaning |
|---|---|
| Name, Notes | Free text. The notes show as the row's tooltip. |
| Frequency, Mode | The receive frequency in MHz as the dial shows it (with a transverter selected: the RF, not the IF), and the mode: USB, LSB, CW, AM, SAM, FM, NFM, DSB, DATA-U or DATA-L. |
| Filter width, Shift | Optional, in Hz. Left empty, the tune leaves the filter as it is. |
| Receive preset | Optional: a saved receive DSP preset (Radio → Receive Presets) recalled with the tune. |
| Alternate frequencies | Optional, up to eight, in MHz, separated by commas. They appear in the **Alternates** menu when the net is selected. |
| Repeats | **Once**; **Daily** (or every 2–52 days); **Weekly** on the days you tick (or every 2–52 weeks); **Monthly** on the first, second, third, fourth or last given weekday (or every 2–52 months). |
| First meeting | The date of the first meeting, in the net's own time zone. A net never meets before it, and "every 2 weeks" counts from its week. For **Once** it is the date. |
| Start, Duration | Wall-clock start time in the net's time zone, and the length in minutes (1–1440). |
| Time zone | **UTC**, **This Mac** (the Mac's current zone, saved by name), or **Other…** with a zone name such as `Europe/London`. |
| Remind | No reminder, at the start, or 5, 10, 15, 30 or 60 minutes before. |
| Record the audio | Optional; see *Recording a net* below. |

**Capture Current** fills the frequency, mode and filter from the dial. It
needs a connected radio, a recording or Demo Mode. It also selects the
receive preset when the receive DSP settings in effect are exactly those of
a saved preset (for example straight after recalling it). If you have
changed any DSP setting since, no preset matches and the menu is left as it
was: pick the preset yourself.

The sheet shows the **next five meetings** in UTC and in the net's own zone
as you change the fields, so you can check the rule before saving.

### Time zones and daylight saving

A net entered in **UTC** meets at the same UTC time all year.

A net entered in a **named zone** keeps its wall-clock time: a "7 pm
Eastern" net is at 00:00 UTC in winter and 23:00 UTC in summer, and the
Next column, the reminder and the recording follow it. Enter a zone name,
not an abbreviation: "EST" is refused, because an abbreviation has no
daylight-saving rule.

Two cases come up once a year each:

- A start time that **does not exist** on the day the clocks go forward
  (02:30 where 02:00 jumps to 03:00) is met the same span after the jump,
  at 03:30.
- A start time that **happens twice** on the day the clocks go back is met
  the first time.

Weeks run Monday to Sunday. "Every 2 weeks on Monday and Sunday" therefore
meets on the Monday and the Sunday of the same week, then skips a week.

## The list

Each row shows whether the net is switched on, its name, frequency and mode,
its repeat rule, its start time and zone, and **Next**: when it meets next,
in UTC and in the net's zone, and how long until then — or "on now until …"
with a green dot while it is meeting. A net that is switched off shows "off"
and is left out of reminders, labels and "next net"; it can still be tuned
by hand.

Select a row and press **Tune** to go there. Double-click a row to edit it.

## Reminders

When a net's lead time arrives, a banner appears over the panadapter and in
the Net Scheduler window:

- **Tune Now** sets the receive frequency, mode, filter and preset. If the
  radio refuses — the frequency is outside what the radio or recording
  covers, the mode is not one this radio offers, or the transmitter is
  busy — the window says why and the banner stays. Like a bookmark recall,
  it is a deliberate "go there" and is allowed while the dial is locked
  against accidental tuning.
- **Snooze** hides it for 5 minutes (10 or 15 if you choose) and brings it
  back once, unless the net ends first.
- **Dismiss** removes it.

A reminder is raised once per meeting and stays until you answer it or the
net ends. If HermitSDR starts, or the Mac wakes, after the lead time but
while the net is still meeting, the reminder appears then ("started 12 min
ago"). A meeting that passed entirely while the app was not running is not
announced afterwards. HermitSDR must be running for any reminder.

The banner makes **no sound**.

### macOS notification (optional, off by default)

Tick **macOS notification** to also post each reminder to Notification
Centre, with the same three buttons. macOS asks for permission the first
time. The notification is silent. While HermitSDR is the front app only its
own banner is shown and the notification goes straight to Notification
Centre.

## On the panadapter

While a net is meeting and its frequency is inside the visible span, an
orange **NET · name** label and a tick sit just above the band-plan strip at
that frequency. Clicking the label tunes to the net (receive only). Untick
**Label nets on the panadapter** to hide the labels. The labels need the
panadapter to be showing; they do not depend on the band-plan strip being
switched on.

## Recording a net

With **Record the audio for the net's duration** ticked, HermitSDR adds a
one-off entry called "Net *name*" to **Radio → Recording Schedule** five
minutes before each meeting. Recording Schedule then does what it does for
any entry: at the start time it tunes to the net's frequency and mode,
records the receiver audio to a WAV file for the net's duration, and puts
the dial and mode back afterwards. It refuses, and says so, while the
transmitter is armed, keyed or owned by a program, while the recorder is
already in use, or with no receiver running; see
[Recording.md](Recording.md).

The entry belongs to the radio that is selected when it is added. The entry
from the previous meeting is removed when the next one is added, and when
you delete the net. If HermitSDR is started more than about 30 seconds
after a net began, that meeting is not recorded.

## Sharing a list

**Export…** writes the whole list as JSON. **Import…** reads such a file.

- The file is checked before anything changes. If any net in it has a
  mistake, **nothing is imported** and the window names the first problem:
  the net's position and name, the field, and what is wrong — for example
  `Net 2 “Maritime Net”, startTime: must be a time as HH:MM, from 00:00 to 23:59.`
- If some nets in the file are already in your list (the same id, or the
  same name ignoring case), you are asked once what to do with them:
  **Skip** keeps yours, **Overwrite** replaces yours with the file's,
  **Add as New** keeps both. Nets that are not in your list are added in
  every case.
- The list holds at most 200 nets and a file may be at most 1 MiB.

### File format

```json
{
  "format": "hermitsdr-nets",
  "version": 1,
  "nets": [
    {
      "name": "Club Net",
      "frequencyHz": 3860000,
      "mode": "LSB",
      "repeat": { "kind": "weekly", "interval": 1, "weekdays": ["WE"] },
      "startDate": "2026-01-07",
      "startTime": "19:00",
      "timeZone": "America/New_York",
      "durationMinutes": 60,
      "reminderMinutes": 5
    }
  ]
}
```

| Key | Required | Value |
|---|---|---|
| `name` | yes | Text, 1–64 characters. |
| `frequencyHz` | yes | Receive frequency in hertz, 1 kHz – 100 GHz. |
| `mode` | yes | Mode name, for example `USB`. |
| `repeat` | yes | `kind`: `once`, `daily`, `weekly` or `monthly`. `interval`: 1–52 (default 1). Weekly: `weekdays`, a list of `SU MO TU WE TH FR SA` (omitted: the weekday of `startDate`). Monthly: `ordinal` 1–4 or -1 / `"last"`, and `weekday`. |
| `startDate` | yes | `YYYY-MM-DD` in the net's zone. |
| `startTime` | yes | `HH:MM`, 24-hour, in the net's zone. |
| `timeZone` | yes | `UTC` or a zone name such as `Europe/Berlin`. |
| `durationMinutes` | no | 1–1440; default 60. |
| `reminderMinutes` | no | 0–1440 minutes before the start; omitted or `null` = no reminder. |
| `enabled` | no | `true` (default) or `false`. |
| `notes` | no | Text, up to 500 characters. |
| `filterWidthHz`, `filterShiftHz` | no | 50–20000 and -5000–5000. |
| `receivePreset` | no | Name of a receive DSP preset on the importing Mac. |
| `alternateFrequenciesHz` | no | Up to eight frequencies in hertz. |
| `recordAudio` | no | `true` to record each meeting. |
| `id` | no | A UUID. Export writes it so a later import of the same file matches by id. |

Unknown keys are ignored. Reminder history is never exported.

## Command palette, Shortcuts, AppleScript and the Control API

- **Command palette (⌘K):** *Next Net* shows which net is on now or next;
  *Tune to Next Net* and *Tune to Net: name* tune the receiver.
- **Shortcuts:** *Get Next Net* and *Tune to Net* (leave the name empty for
  the net on now, otherwise the next one). See [Automation.md](Automation.md).
- **AppleScript:** `next net` and `tune to net "Club Net"`.
- **Control API:** `tuneToNet` and the read-only state keys `nextNet`,
  `nextNetStart`, `nextNetHz`, `nextNetMode` and `netOnAir` (revision 6).
  See [ControlAPI.md](ControlAPI.md).

A name may be shortened to its beginning, or to any part of it, as long as
only one net matches. All of these are receive tunes with the same refusals
as **Tune Now**.

## Limits

- HermitSDR has to be running; there is no background helper. A reminder
  whose whole meeting passed while the app was closed is not shown.
- Reminders are checked every 20 seconds, so a banner can appear up to 20
  seconds after its lead time.
- A net has no end date. Switch it off or delete it when it stops meeting.
- There are no exception dates ("not on 25 December") and no rule finer
  than those above (for example "first and third Tuesday" needs two nets).
- **Capture Current** selects a receive preset only when the DSP settings
  in effect match a saved preset exactly.
- The panadapter label marks the net's main frequency only, not its
  alternates.
- The recording covers the net's main frequency and uses Recording
  Schedule's rules, including putting the dial back at the end.
- The time-zone rules are the ones installed with macOS. If a country
  changes its rule, the times follow after a macOS update.
