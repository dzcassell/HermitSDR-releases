# Search scan

**Radio → Search Scan…** steps the receiver through a frequency range looking
for signals it has no memory for: 118–137 MHz on an RSPdx, 26.9–27.5 MHz on a
Hermes Lite 2. The [Bookmark Scanner](BookmarkScanner.md) scans saved
memories; [Receive Watch](ReceiveWatch.md) watches ranges inside the span
already on screen and never retunes. This one moves the span.

It is receive only. Nothing here arms, keys or changes the transmitter.

## How it searches

The scan does not visit channels one at a time. It parks the centre of the
sampled span, judges **every channel in that span at once** from the same
spectrum the waterfall draws, then moves the centre on. On a 1536 kHz span
with 25 kHz channels that is 48 channels per look; a full pass of the
airband (761 channels) is 16 looks, under ten seconds.

Only the middle 80 % of the span is trusted (the edges are in the radio's
filter skirts), and the centre always falls between two channels, so a DC
spur at the centre is never taken for a station.

A channel is **active** when it stands the threshold above the *local noise
floor*. The floor is measured in every look from the quiet parts of the
same span, so the threshold means the same thing on a noisy band as on a
quiet one, at any gain and with any display averaging. A steady carrier and
a wider voice or data signal are both caught.

Before Start the window shows what to expect — spans, channels, seconds per
pass, channels per second — and, while running, what it measured.

## Plans and presets

A plan is one or more ranges, each with a start, a stop, a channel step, a
mode and (optionally) a filter width for listening. Up to 32 plans of up to
16 ranges and 20,000 channels each are saved.

**Add preset** copies a ready-made plan into your list, where you can edit
it for the local band plan:

| Preset | Range | Step | Mode |
| --- | --- | --- | --- |
| Airband 25 kHz | 118.000–136.975 MHz | 25 kHz | AM |
| Airband 8.33 kHz | 118.000–136.992 MHz | 8.33 kHz | AM |
| Marine VHF | 156.000–162.025 MHz | 25 kHz | NFM |
| 11 m CB | 26.965–27.405 MHz | 10 kHz | AM |
| 10 m FM | 29.000–29.700 MHz | 10 kHz | NFM |
| 6 m FM | 50.000–54.000 MHz | 10 kHz | NFM |
| 2 m | 144.000–148.000 MHz | 12.5 kHz | NFM |
| 70 cm | 430.000–450.000 MHz | 12.5 kHz | NFM |
| PMR446 | 446.00625–446.19375 MHz | 12.5 kHz | NFM |
| FRS / GMRS | 462.5500–462.7250 and 467.5625–467.7125 MHz | 12.5 kHz | NFM |

Only presets the connected radio can tune are offered: a Hermes Lite 2 is
offered 11 m and 10 m FM, an ANAN adds 6 m, an RSPdx gets all of them. With
no radio connected the whole list is shown.

## Stop rules

| Setting | Default | Meaning |
| --- | --- | --- |
| Threshold | 10 dB | Over the local noise floor to count as active (3–60) |
| Hysteresis | 4 dB | A channel being held stays active down to threshold minus this |
| Hang | 2 s | Quiet time before leaving a held channel; a signal that returns inside it continues the same hold |
| Max dwell | 0 (none) | Longest stay on one channel; then the scan resumes even if it is still active |
| Settle | 0.25 s | Wait after each centre move before the spectrum counts. The time the display's own averaging needs to forget the previous span is added automatically (more on Slow than on Fast or Peak) |
| Look | 0.3 s | How long each parked span is watched |
| Hold on a hit | on | Off = survey: log every active channel and keep moving |
| Mute while searching | on | Audio is muted between hits; your own mute setting returns on every hold and when the scan stops |
| Record hits | off | See below |

With **Hold on a hit**, the receiver tunes to the active channel in the
range's mode and filter and stays while it is active. Several active
channels in one span are held in turn, lowest first; one that has gone
quiet by the time its turn comes is logged without a stop. After a
maximum-dwell release the next pass stops there again unless you lock it
out.

## Skip and lock-out

- **Skip** leaves the held channel (or the current span) now.
- **Lock out for this session** also keeps the scan from stopping there
  again until you choose *Clear temporary lock-outs* or quit.
- **Lock out permanently** adds the channel to the saved lock-out list —
  for birdies, pagers and carriers that are always there.

The list at the bottom of the window is the editor: add a frequency, a
width and a note by hand, or remove an entry. A lock-out covers its width
centred on the frequency, in any plan. Up to 1,000 entries are kept.

## Hit log

One row per channel: last and first heard (UTC), frequency, mode, peak and
minimum level, peak over the noise floor, total duration and how many
times it was found. Levels are antenna dBm on a calibrated radio (the same
calibration as the pointer readout) and dBFS otherwise. The log holds 2,000
channels for the session and is not saved; **Export CSV…** writes it:

```
first_seen_utc,last_seen_utc,frequency_hz,frequency_mhz,mode,peak_dbm,minimum_dbm,peak_over_floor_db,duration_s,count
2026-11-18T11:06:40Z,2026-11-18T11:07:43Z,118325000,118.325000,AM,-85.0,-97.0,25.0,9.4,2
```

Right-click a row to **tune** to it (stops the scan), **save it as a
bookmark**, **add it to a Bookmark Scanner list** (the bookmark is made if
needed), **lock it out** or remove it.

Hits are drawn on the panadapter and waterfall as thin cyan lines (brighter
on the channel being held) and lock-outs as grey bars. The checkbox under
the log hides them.

## Recording hits

With **Record hits**, the scan starts one audio recording through
[Gated Recordings](Recording.md) and keeps its gate shut except while it is
holding on a hit, so the file holds the hits and nothing else, each with
its UTC time, frequency and mode in the cue list. The Gated Recordings
pre-roll, hang, minimum length and layout apply, and the session appears in
**Radio → Gated Recordings…** with the name `search-scan`. With the squelch
on, only what opens it during a hold is kept. It works whether or not
*Record only when open* is switched on there, and it needs *Hold on a hit*.
Stopping the recording yourself (♪) leaves the scan running without it.

## When it will not start, and what stops it

Start is refused — and a running scan pauses — while the transmitter is
armed, keyed, tuning or owned by a program, the dial is locked, a file is
replaying or the time machine is not live, SUB or linked VFOs are on, a
recording you started is running, or ALE scan, Band Scout, the Bookmark
Scanner or the FM DX scan has the receiver. It is also refused with a
transverter active (ranges are in the radio's own tuning range) and on
radios whose IF follows the dial (TH-D75, FTDX10 and IC-7410 IF feeds),
which have no wide span to search. Resume is always explicit.

**Tuning by hand stops the scan** — the dial, a click, CAT, a band button —
and leaves the receiver where you put it. So does changing the sample rate
or moving the span. Mode, filter and gain may be changed while listening to
a hit.

Stop leaves the receiver where it is. **Return to start frequency** puts
back the dial, span, mode and filter from before Start (not after you have
tuned by hand). A disconnect or quit during a scan restores them first, so
the scan's parked span is never filed as your setting.

Each centre move clears the waterfall and the IQ time-machine history, as
any retune of the span does.

## Seek on the step buttons

The tuning-step menu (the step button beside ◀ ▶) has **Seek: ◀ ▶ jump to
the next signal**. With it on, ◀ and ▶ jump to the next signal below or
above the receive filter — the nearest one at least 12 dB over the noise
floor in the sampled span — instead of moving one step; hold the button to
keep going. ◀◀ ▶▶, the wheel and the arrow keys still step. Nothing is
retuned when there is no further signal in the span. In USB and LSB the
dial lands on the strongest part of the signal, so expect to touch it up by
ear; with *Snap to step grid* on and a step of 500 Hz or more a landing
close to a step multiple is put on it. Seek is off by default, works on a
replayed file too, and obeys the dial lock like any step.

## Not established without a radio

The stepping, timing, activity decision, lock-outs and log are tested
against a synthetic band and a bench receiver with a manual clock
(`SearchScanTests`, `SearchScannerModelTests`). Still to
be checked on air: the settle time each radio really needs after a centre
move, levels against the S-meter, the sound of a hold, and the window's
layout on screen.
