# Panadapter measurements (#474)

Markers, channel measurements and stored reference traces on the main
panadapter, with the same tool in each independent receiver window and a
markers-only form in the Bandscope. Use them to read how far apart two
signals are, how far down a spur is, how wide a signal is, how much power
sits in a channel and how the band compares with a trace stored earlier.
Receive only: nothing here can arm, key or change the transmit path, and
nothing leaves your Mac.

## Where

Choose **Measure** at the top of the spectrum pane. A panel opens at the top
right of the pane; **Done** closes it. Everything is off until you choose
Measure, and markers are forgotten when you choose Done. Stored reference
traces are kept until you remove them or quit.

| Surface | What it offers |
| --- | --- |
| Main panadapter | Everything on this page. Levels in dBm where the radio is calibrated. |
| An opened IQ recording | The same: a recording plays through the main receiver and its panadapter. |
| Independent receiver window | **Measure** beside Record WAV, while the window is running. Markers, all measurements and trace modes, in dBFS, read from the window's displayed rows (see "Receivers without the FFT tap"). Reference traces can be stored and exported but are not drawn. |
| Bandscope | **Measure** at the top right. Normal, delta and peak-track markers in dBFS. While measuring, a click places a marker instead of tuning. No noise markers and no channel measurements: each Bandscope bin is the strongest of four 7.5 kHz FFT bins, which cannot be integrated. |

## Markers

Up to eight markers, lettered A to H. Each is anchored to an RF frequency,
snapped to an FFT bin, so zoom, pan and an inverted transverter display do
not move it.

- The first click places **A**. The second click places **B** as a delta
  marker against A. Later clicks move the selected marker.
- **Add marker** chooses a kind for the next click. Select a marker by its
  letter; change its kind or the marker it is read against from its menu.

| Kind | Reads |
| --- | --- |
| Normal | Frequency and the level of its FFT bin. |
| Delta | Frequency and level difference from a reference marker. Both levels come from the same trace. |
| Peak track | As Normal, but the marker moves to the strongest bin within 40 bins of where it is on every update, so it follows a drifting carrier. It will also step to a stronger neighbour that comes inside that range. |
| Noise | Noise density per hertz: the mean power of the nine bins around the marker, divided by the bin's noise bandwidth (bin spacing × the Hann window's equivalent noise bandwidth of 1.50 bins). |

A bin level is the power of a steady carrier centred on that bin. A carrier
between two bins reads up to 1.4 dB low in a single bin (Hann scalloping);
use channel power when the absolute level matters.

## Measurements

One measurement at a time, chosen under **Measurement**. It is centred on
the selected marker, or on the receive frequency when there are no markers.
The shaded bands on the spectrum show what is being integrated.

| Measurement | Result |
| --- | --- |
| Channel power | Power integrated over the bandwidth, and the mean density across it. Edge bins count in proportion to how much of them the channel covers. |
| Adjacent-channel power | The carrier channel, and the channels of the same bandwidth one spacing below and above, each in dBc. A channel that leaves the usable span is reported as outside it. |
| Occupied bandwidth | The band holding the chosen share (default 99 %) of the power found in the search span, the rest split equally below and above. Everything in the span counts, noise included: keep the span close to the signal. |
| x dB bandwidth | The width between the outermost points −3, −6 or −26 dB below the strongest bin in the search span. A reading under about two bins is the FFT resolution, not the signal. |
| Signal-to-noise | Channel power against the noise the measured floor puts in the same bandwidth: (channel − noise) / noise. The floor is the 25th percentile of the bins across the usable span, corrected for the number of averages. |
| Peak table | Up to eight local peaks at least 10 dB above the floor, strongest first. |

## Trace modes

Under **Trace and references**. The measurement trace is separate from the
displayed trace and its Averaging setting: it is built from the power of
every FFT frame, taken ahead of the display's dB averaging.

| Mode | Trace |
| --- | --- |
| Live | The mean power of the FFT frames since the previous update (five updates a second). |
| Average | The mean power over the last N updates, 2 to 100. Every FFT frame counts once. |
| Max hold | The per-bin maximum of the live trace since Restart. |
| Min hold | The per-bin minimum of the live trace since Restart. |

The panel states the detector under the results, for example
`Average of 10 sweeps · RMS power · 118 FFT frames (≈ 112 independent)`, so
two readings can be compared. Overlapping FFT frames are not independent;
the second figure is what the averaging is worth.

A hold trace is biased for noise, so noise markers, signal-to-noise and the
peak table give no reading in Max hold or Min hold. A retune, a sample-rate
change or a gain or attenuator change restarts the trace.

## Reference traces

**Store trace** keeps the current measurement trace, up to four (R1 to R4).
Stored traces are drawn as thin coloured lines over the spectrum pane while
Measure is on, at the frequencies and dBFS levels they were captured at. The
checkbox hides one; **CSV…** exports it as two columns, `frequency_hz`
(RF) and `level_dbm`, one row per FFT bin in ascending frequency. For an
uncalibrated receiver the second column is `level_dbfs`.

## Units and calibration

Levels use the same reference as the S-meter and the pointer readout: the
radio's calibration profile ([Radio calibration](RadioCalibration.md)) with
the RF gain and attenuator applied. The last line of the panel says which
applies:

- **dBm from this radio's operator-measured calibration profile.**
- **dBm from this radio's calibration profile, not yet verified by the
  operator.** The offset was migrated or is a default for the board.
- **dBm from the default S-meter offset.** The radio has no profile.
- **Uncalibrated … dBFS.** The receiver supplies relative IF or audio levels
  (TH-D75 and other IF feeds). Differences in dB are still valid; absolute
  levels are relative to digital full scale.

Levels are withheld during ADC overload and while transmitting.

## Accuracy

Measured by `SpectrumMeasurementTests` with synthetic signals run through
the production spectrum FFT at 192 kS/s (23.4 Hz bins). Errors are against
the analytic value.

| Signal | Reading | Error |
| --- | --- | --- |
| Two tones 16.5 kHz apart, 20 dB apart | Delta marker | 0.0 Hz, 0.00 dB |
| White noise at −112.83 dBFS/Hz, about 400 FFT frames | Noise marker | −0.11 dB |
| | 12 kHz channel power | −0.004 dB |
| | Floor from the 25th percentile | +0.001 dB (single frame: +0.08 dB) |
| 12 kHz rectangular noise channel at −30 dBFS over a −122.8 dBFS/Hz floor, 255 frames | Channel power | −0.002 dB |
| | 99 % occupied bandwidth (analytic 11,880 Hz) | +3.4 Hz (0.03 %) |
| | −3 / −6 / −26 dB bandwidth | −13 / +12 / +72 Hz (0.6 % at worst) |
| | Adjacent channels at ±16 kHz | −0.01 / +0.03 dB |
| | Signal-to-noise | −0.03 dB |
| Tone at −40 dBFS over a −132.8 dBFS/Hz floor, 239 frames | Marker level | 0.00 dB |
| | Noise marker | +0.06 dB |
| | Signal-to-noise in 3 kHz (analytic 58.06 dB) | −0.01 dB |

These are the errors of the mathematics on ideal signals. On air, the
absolute accuracy is that of the radio's calibration, and a noise reading
from a few frames scatters: one unaveraged bin has a standard deviation of
about 5.6 dB, falling with the square root of the independent averages.

## Cost

With Measure off the spectrum FFT runs one extra branch per frame; nothing
else exists. With Measure on, each FFT frame adds one 8192-element vector
add on the DSP thread (0.5 µs measured, against about 17 µs for the frame
itself), and the panel does its work five times a second on the main
thread: under 0.1 ms for a marker or channel reading and about 0.5 ms for
signal-to-noise or the peak table with a 100-sweep average (debug build,
Apple silicon). The Metal renderer is not involved.

## Receivers without the FFT tap

An independent receiver window, and any receiver whose main spectrum rows
do not come from the spectrum FFT, is measured from the displayed rows. The
detector line then reads
`log average of display rows · noise corrected +2.51 dB`: the display
averages dB values, which reads Gaussian noise 2.51 dB low, and noise
markers, signal-to-noise and the floor add that back (measured: a noise
marker within 0.05 dB of the analytic density after 100 averaged rows).
Channel power, adjacent-channel power and occupied bandwidth are not
corrected, because a carrier in the same channel would then read high: a
noise-like signal reads up to 2.51 dB low there. On the main panadapter,
with the display's Peak averaging, this fallback gives no noise readings.

## Not included

- The Bandscope has markers only, for the reason in the table above.
- Independent receiver windows and the Bandscope do not draw stored
  traces, and their levels are dBFS: neither has an antenna calibration.
- Marker and measurement settings are not saved between sessions.
- On the main panadapter, reference traces are drawn over the spectrum
  trace, not beneath it.
