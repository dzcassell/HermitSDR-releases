# Bookmark schedules, stacked labels, ranges, the band grid and links

Five additions to the Bookmarks star (the control bar and both console
banks) and the panadapter. All of them are receive-side and none changes
what the transmitter does.

## Scheduled bookmarks

Open **Bookmarks**, press the pencil beside a memory and tick **On the air
only at set times (UTC)**. Choose the days and type a start and a stop as
`HHMM` in UTC, then Save.

- The day belongs to the start: Monday 2300–0100 runs from Monday 23:00 UTC
  to Tuesday 01:00 UTC. The same start and stop means the whole 24 hours
  from that time; a stop of `2400` is the end of the day.
- While a scheduled memory is off the air its panadapter label is faded and
  has a dashed border; on the air it has a solid border. A memory without a
  schedule has no border and is always on. The list shows a clock beside
  each scheduled memory, green while it is on.
- Recalling a memory always works, on the air or not.
- **Bookmark Scanner** has a new setting per list, **Skip memories that are
  off the air**. It is off by default. With it on the scanner passes over
  a memory outside its days and hours, starts on the first memory that is on
  the air, and pauses with a plain message when every memory left in the
  list is off the air.

Memories saved by earlier versions are read unchanged and are always on the
air. The schedule travels in the JSON library export and import; the CSV
spreadsheet and CHIRP exports do not carry it.

## Bookmark labels on the panadapter

Bookmark names are stacked in up to four rows above the frequency scale, so
two names never overlap. Where a spot is too crowded for four rows a memory
keeps its tick and loses its name until you zoom in. Names longer than 18
characters are shortened.

Labels are coloured by list. A memory that belongs to a Bookmark Scanner
list takes that list's colour (a memory in several lists takes the first);
a memory in no list is yellow, as before. **Bookmarks → Panadapter labels**
shows the lists with their colours and lets you hide any of them. The
choice is remembered.

## Frequency ranges

**Bookmarks → Ranges…** keeps up to 256 named, coloured frequency ranges.
Each is drawn as a thin bar along the top of the spectrum. Click a bar to
shade the whole range with its name; click it again to close it. Only the
bar takes the click, so tuning everywhere else is unchanged.

- **Add**: a name, the two edges in kHz and a colour. **Visible span** fills
  the edges from what the panadapter shows.
- **Go to** (in the Ranges sheet and in the Bookmarks popover) tunes to the
  middle of a range. It is a receive tune; the mode and filter stay.
- **Export CSV…** writes `name,lower_hz,upper_hz,colour`.
- **Import CSV…** reads the same columns (`color` and `gray` are accepted).
  The whole file is checked before anything is kept: if one row is wrong
  nothing is imported and the message names the row, for example "Row 7:
  upper_hz is not a plain number of hertz. Nothing was imported." Ranges
  already in the list are skipped. Colours are red, orange, yellow, green,
  teal, blue, purple, pink and grey.

Edges are the frequencies the dial shows, so a transverter profile moves
the bars with the scale. A range never limits tuning or anything else.

## Band grid

The grid button beside the Bookmarks star opens the band keys as a grid
with a group selector: **Ham Bands**, **Ham Bands VHF/UHF** and
**Broadcast Bands**. Each key shows the mode it lands in in small type and
the band you are on is lit. Only bands the connected radio can tune are
offered, and a group with none is left out.

- A ham key is the same band key as elsewhere: it returns to the band's
  last frequency, mode and filter, and pressing it on the band you are on
  steps the band stack. 60 m returns to the last used 60 m frequency; the
  channel chooser is on the 60 key of the console and in the Band menu.
- A broadcast key tunes the first channel of the band in AM (SAM is kept
  when it is selected). The bands follow the medium-wave channel plan in MW
  Stations: with the 9 kHz plan the grid shows the Region 1 allocations,
  long wave included; with the 10 kHz plan it shows Region 2.

## Copy Link

**Bookmarks → Copy Link** puts a link on the clipboard, for example

    hermitsdr://tune?f=7074000&mode=USB&bw=2700&shift=0&zoom=4

`f` is the frequency the dial shows in hertz; `mode`, `bw` and `shift`
(filter width and shift in hertz) and `zoom` are optional.

Opening such a link tunes the receiver that is already running: the
frequency, then the mode, the filter and the zoom. A link is treated as
untrusted text:

- It can only carry those five values. Any other field, a repeated field, a
  value out of range, an encoded character or anything else unexpected
  rejects the whole link, and nothing changes.
- The frequency goes through the same range check, dial lock and
  transverter mapping as a Control API tune.
- A link never connects a radio, never opens a recording and never replaces
  a session. With nothing receiving it only says so.
- Nothing happens while the transmitter is armed, keyed, tuning or owned by
  a program. Disarm, then open the link again.

The installed app and a development build both register the `hermitsdr`
scheme; macOS decides which one receives a link.

## Schedule timeline

**Bookmarks → Timeline…** shows the next 24 hours in UTC, starting now at
the left: one row for each shortwave station catalogued on the dial (from
the bundled schedule), each bookmark that carries a schedule and each
switched-on net in Net Scheduler that meets in that time. At most 40 rows
are shown. It is a display; nothing is tuned or recorded from it.

## Not checked

These were built and tested without a radio and without the app on screen.
The label rows, the range bars, the grid and the timeline have not been
looked at in a running app, and no link has been opened through macOS.
