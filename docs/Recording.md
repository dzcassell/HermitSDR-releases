# Recording

HermitSDR records in four ways, all receive-side and all started by the
operator, the crab or — since #289 — a schedule:

- **IQ (`.hiq`)** — the raw sampled span (interleaved float32 pairs behind a
  28-byte header; `HermitSDR/Recording/IQFile.swift`). Started from the
  header record button, the crab's `set_recording`, or a scheduled entry.
  Replayed from the connect sheet or File → Open IQ Recording. Live radio
  only: a replay cannot be re-recorded.
- **Audio (WAV)** — the demodulated audio you hear (16-bit mono at the
  12 kHz chain rate, `HermitSDR/Audio/WavRecorder.swift`). Works live and
  during replay.
- **Band DVR** — continuous, bounded, disk-backed full-span IQ with a
  timeline (`docs/RecordingStoreRecovery.md`).
- **Clips and excerpts** — bounded `.hiq` excerpts around decoder events
  from the RF time machine (`docs/Clips.md`).

Files land in `~/Documents/HermitSDR Recordings` (the Dev build uses its
own folder) and are named by UTC timestamp, dial and — for IQ — rate:
`20261022-030000_9420kHz_192k.hiq`, `20261022-030000_9420kHz_audio.wav`.

## Recording Schedule (#289)

**Radio → Recording Schedule…** records while you are away: a broadcast, a
net or a band segment at a UTC time, on the days you choose, so the file
is waiting in the morning. The window is one table of entries with
Add / Edit / Delete, a **Next run** column, a **Last** column (the outcome of
the most recent occurrence), the running capture with a **Stop** button and
the scheduler's log.

### An entry

| Field | Meaning |
| --- | --- |
| Name | Shown in the table, the header chip and the log; also written into the file name (`…_192k_BBC-WS.hiq`, `…_audio_BBC-WS.wav`, ASCII letters, digits and dashes, at most 24 characters). |
| Start (UTC) + duration | Hour and minute in UTC; 1–1440 minutes. A window may cross UTC midnight (`23:45–00:15`). |
| Days | **Daily**, a set of **weekdays**, or one **date** (a UTC calendar day; the entry shows *expired* afterwards). |
| Record | **Audio (WAV)**, **IQ (.hiq)** or **both** — the same recorders as the header buttons. |
| Preset | Optional dial RF and demodulator mode applied when the capture starts, through the same path as a bookmark or broadcast tune (a transverter profile maps and range-checks the RF). **Restore afterwards** puts the dial and mode back when the capture ends. |
| Split files at | Optional size roll-over, 16–65536 MB: when the current file reaches the limit the recorder is closed and reopened on a numbered part (`…_BBC-WS-p2.hiq`), with no gap longer than a stats tick. The larger of the IQ and audio files decides. |
| Enabled | Off keeps the entry without firing it (*off* in the next-run column). |

Entries are **kept per radio**: they travel with the radio's receive
profile (`RadioOperatingSettings.recordingSchedule`, keyed by the radio's
stable identity) and the shared defaults key `recordingSchedule` holds the
list for sessions without a stable identity. At most 64 entries.

### How it fires

The scheduler lives on the main actor and rides the existing 60 s
crab-watch tick; the recorders themselves are the existing engine paths,
so nothing here touches the audio or radio queues. Each entry carries the
start time of the last occurrence it decided about (`lastOccurrence`), and
a tick acts on an occurrence **exactly once**:

- A start seen within **120 s** of its minute starts the capture. A late
  start still ends at the scheduled end (start + duration), not later.
- A start first seen later than that — the Mac was asleep, the app was not
  running, or the entry was switched on afterwards — is logged as
  **missed** and stamped. It is never back-filled.
- A start is **refused** — logged, stamped, not retried — while the
  transmitter is keyed, tuning, two-toning or RF-hot; while a native,
  FT8 or scripted transmit program owns the radio; while the transmitter
  is **armed**; while a band-scout sweep is retuning; while the recorder
  the entry needs is already in use (a manual recording, or another
  scheduled capture); when IQ is asked for without a live radio; or when
  a preset tune would clear a rewound time machine.
- A refused preset tune (dial lock, transverter range) refuses the start.
- One scheduled capture runs at a time; a second due entry is refused with
  the running entry's name.

The stats tick (about 1 Hz) ends the run at the scheduled end, rolls the
files over at the size limit, and ends the run when a recorder stops
underneath it (the operator pressed the header stop button, the disk
filled, the connection dropped). The dial is restored at the end whichever
way it ended, if the entry asked for it.

Creating an entry, editing its timing or switching it on **re-arms** it: an
occurrence that began inside the grace window still starts on the next
tick; anything older is marked decided so it is neither started late nor
reported as missed. Toggling an entry off and on, or editing its name,
kind or preset alone, keeps its stamp.

Every start, refusal, miss, roll-over and end goes to the window's log,
the crab's action feed and a toast; while a capture runs the header shows
a red **SCHED name** chip beside the record buttons.

### Crab

`recording_schedule` — *"record 9.420 MHz AM at 0300Z for 30 minutes"*
adds an entry (frequency and unit as spoken; AM when no mode is given;
daily unless `days` says otherwise; audio unless `kind` is `iq` or `both`),
*"what's on the recording schedule"* lists entries with their next run,
and *enable / disable / toggle / delete* name an entry (`delete all` clears
the schedule); *stop* ends the running capture. The `app_control` commands
`recording-schedule-list`, `recording-schedule-toggle` (value = name) and
`recording-schedule-stop` do the same from the control router.

### What it does not do

It never arms, keys or transmits, never moves a keyed or program-owned
radio, and never starts a second recorder into a file that is already
open. A refused or missed occurrence is reported, not retried. Entries do
not survive a radio with no stable identity across a profile switch other
than through the shared list.

### Tests

`RecordingScheduleTests` (package): next-start across UTC midnight,
weekday sets and one-off dates; exact-once firing through two days of
jittered minute ticks (double ticks, 59.5 s and 61 s gaps) with an
injected clock; late start inside the grace window; missed start logged
and stamped; the refusal paths (TX-owned, second entry while one runs,
refused preset tune, throwing recorder with clean-up and restore); operator
stop and stop-underneath detection; roll-over into numbered parts and a
failed roll-over restart; JSON and per-radio catalogue round trips with an
older catalogue that lacks the field; validation bounds; the labelled
recorder entry points on `RecordingModel`.
