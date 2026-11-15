# Signal History (#427)

A long-running chart of how strong the tuned signal is: the S-meter level in
dBm, the noise floor inside the receive filter and the SNR, over anything
from the last minute to the last 48 hours. Use it to compare two antennas,
watch a fade, follow sunrise and sunset on medium wave, log a VLF station for
sudden ionospheric disturbances, or find out when a noise source switches on.
Receive only: nothing here can arm or key, and nothing leaves your Mac.

## Where

**Radio ▸ Signal History…** (Feature catalog `signal-history`, Radio
category).

- Recording starts when the window first opens and keeps running after you
  close the window, until you press **Stop** or quit. It is in memory only.
- **Log to CSV** is off until you switch it on. Each time you switch it on a
  new file is started.
- The window remembers the span and the log interval. The history itself is
  not kept across launches; the CSV log is the permanent record.

## What is charted

| Trace | What it is |
| --- | --- |
| Level (dBm) | The S-meter's own reading: in-filter power with the radio's calibration, LNA gain and attenuator applied, exactly as the meter shows it. The line is the mean, the band behind it the minimum to maximum. |
| Noise floor | Estimated from the panadapter: a low percentile of the spectrum across the sampled span (signals sit at the top of that distribution, noise at the bottom), scaled to the width of the receive filter. |
| SNR (lower pane) | Level minus noise floor, in dB. Noise alone reads about 0 dB. |
| SUB | The sub-receiver's level, when SUB is on, as a second trace. |

Readings are taken 20 times a second. The receiver integrates the S-meter over
100 ms, so neighbouring readings come in pairs.

The right-hand scale shows S-units (S9 = −73 dBm, 6 dB per S-unit) for the
same grid lines. Times are UTC.

### Spans and resolution

| Span | Kept as | Held for |
| --- | --- | --- |
| up to 15 min | every 20 Hz sample | 15 minutes |
| up to 4 h | minimum / mean / maximum per second | 4 hours |
| up to 48 h | minimum / mean / maximum per 15 seconds | 48 hours |

The store is a fixed 1,676,160 bytes (about 1.7 MB), allocated when the
window first opens and never grown, plus at most 1,000 markers and 4,096
settings changes. Means are means of the dB values.

A gap in the chart means there was nothing to read: the radio was
disconnected or the stream had stalled.

During a file replay or a time-shifted view the readings are of the replayed
signal, stamped with the clock time at which you played it.

### Accuracy of the floor and SNR

The level is the S-meter and is as accurate as your S-meter calibration. The
noise floor is an estimate: on band noise it lands within about 1 dB of what
the meter reads on the same noise (tested in every mode family at Fast, Med
and Slow display averaging, and with strong carriers on a fifth of the span).
It reads a few dB high with **Peak** display averaging, and it can be lifted
on a span that is mostly occupied by signals (a crowded broadcast band at a
narrow sample rate). The floor needs about two seconds after a retune of the
sampled span before it reappears. WFM uses the same arithmetic as FM and has
not been checked separately.

## Markers

- **Automatic**: a marker is drawn when the frequency, band, mode, antenna or
  filter width changes, so a step in the trace is explained. A dial or filter
  that is still moving gives one marker, placed where it first moved, once it
  has been still for a second.
- **Yours**: type a note ("switched to loop") and press **Stamp marker** or
  Return. An empty note stamps "mark".

Markers also go into the CSV marker column.

## Transmit and overload

Readings taken while transmitting (and for a third of a second afterwards),
while the ADC overload lamp is lit, or while the receiver's overload mute is
closed are shaded red on the chart, flagged `TX` or `OVL` in the CSV, and
left out of every minimum, mean, maximum and statistic.

## Statistics and A/B comparison

Below the chart: median, 10th–90th percentile spread, minimum and maximum of
the level, floor and SNR, and the number of samples used and excluded.

- With nothing selected the figures cover the visible span.
- **Drag** across the chart to select interval A. **Shift-drag** selects
  interval B; the panel then shows **A − B**: the difference of the medians
  (level and SNR) and both spreads. **Pause view** holds the chart still
  while you select. A click clears both selections.
- With SUB on, **Main − SUB** is the median and spread of the difference
  taken reading by reading — the figure to use when main and SUB listen to the
  same signal on two antennas, or to two frequencies at the same moments.

Antenna comparison with one receiver: stay on a steady signal, stamp a marker
or just switch the antenna (it is marked for you), then select a stretch
before the switch as A and one after it as B. Fading makes short intervals
misleading; a minute or more each side is better, and several switches better
still.

Up to 15 minutes back the statistics use every sample; further back they are
taken over the one-second or 15-second means, and say so.

## Continuous CSV log

**Log to CSV** writes rows as readings arrive to

`~/Documents/HermitSDR Recordings/Signal History/SignalHistory-YYYYMMDDTHHMMSSZ.csv`

Choose **Row every**: each sample (20 Hz, about 180 MB a day), 1 s (about
9 MB a day, the default), 10 s or 1 min. With an interval, a row holds the
minimum, mean and maximum of the valid readings in that interval.

The file is forced to disk every 5 seconds. If the app crashes or the power
fails you lose at most the last 5 seconds (plus the interval still being
averaged); the file never ends in half a row. An existing file is never
overwritten. If the disk fills or the file cannot be written, logging stops
and the window says why.

Columns:

| Column | Meaning |
| --- | --- |
| `utc` | ISO 8601 UTC time with milliseconds (start of the interval) |
| `frequency_hz` | Receive frequency (RF, including RIT and a transverter offset) |
| `mode`, `filter_hz` | Mode and filter width |
| `dbm`, `dbm_min`, `dbm_max` | Level: mean, minimum, maximum |
| `floor_dbm`, `snr_db` | Noise floor in the filter and level minus floor |
| `sub_dbm` | SUB level, empty when SUB is off |
| `attenuator_db`, `preamp_db` | Step attenuator and LNA / RF gain |
| `antenna` | Selected receive antenna or input |
| `samples`, `excluded` | Readings used, and readings left out as TX / overload |
| `flags` | `TX`, `OVL` or `TX+OVL` when any reading in the row was flagged |
| `marker` | Marker text; a marker is its own row with no level |

A marker row carries the time the change happened, so it can sit up to a
second or so before the rows around it.

## Export

- **Export CSV…** saves interval A, or the visible span when nothing is
  selected, with the same columns, at the resolution the history holds for it.
- **Export PNG…** saves the chart as drawn.

## Cost

The history reads numbers the app already shows — the S-meter value, the
dial, mode, filter, antenna — on the main thread, 20 times a second, and
looks at the newest panadapter row twice a second. Nothing is added to the
receive chain or the audio path. One reading, including its CSV row, costs
about 14 microseconds in a Debug build.

## Not in this version

- Independent receiver windows as extra traces (main and SUB only).
- "Log signal strength" as a Recording Schedule capture type.
- The chart in the local MCP snapshot.
- Keeping the in-memory history across launches.
