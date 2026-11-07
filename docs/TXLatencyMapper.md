# TX Latency Mapper

Transmit ▸ Measurements & Checks ▸ **TX Latency Map** explains the transmit path from the selected audio
source through HermitSDR's packetizer. The Phase 1 map is safe to open while
disconnected and has no ARM, PTT, coordinator, protocol-command, or test-signal
control.

## Reading the map

Every enabled stage names both its kind and its evidence:

- **Measured** values come from HermitSDR's existing callback counters or a
  queue/block depth observed by the running process.
- **Calculated** values follow directly from a configured sample count and
  sample rate, such as the limiter's 120-sample look-ahead.
- **Device-reported** values are CoreAudio driver properties. They are not
  independently measured.
- **Estimated** values use an explicit fallback, such as the requested
  512-frame input block before the first real block arrives.
- **Unknown** means the running configuration does not expose a defensible
  number. HermitSDR intentionally shows this instead of inventing one.

Observed callback CPU time is separate from algorithmic delay. The displayed
known-components sum is bookkeeping rather than a physical total: CoreAudio
buffers can overlap, the key-down prime applies only at startup, and no host
clock observes the radio DSP, DAC, or PA.

The window refreshes while visible and can export the current snapshot as
versioned JSON, CSV, or a human-readable Markdown report. Exports contain
configuration and timing summaries only; they do not contain microphone audio.

## Audio-loopback measurement (Phase 2)

The software-only Phase 2 core now generates a deterministic 80 ms log chirp
covering 350–2700 Hz. A normalized, polarity-independent correlation search
finds the return at sub-sample resolution and refuses captures below its
confidence threshold. Repeated measurements use median absolute deviation to
reject outliers and preserve every raw trial alongside the accepted set.

Calibration is always a separate, visible field: exports include both the raw
median and calibrated median. JSON uses an explicit schema version; CSV marks
the same accepted/rejected trial decisions used by the summary; Markdown
includes a warning that the result is audio loopback rather than RF latency.

The window now owns the CoreAudio playback/capture workflow. Choose a probe
output, a return input, and an input channel; route them with BlackHole or a
physical cable; then run 3–10 trials. Capture starts before a future monotonic
host-clock deadline, the chirp is played at that deadline, and the reported
path delay subtracts the pre-roll rather than mistaking it for device latency.
The selected device UIDs/names and channel are preserved in schema-v2 exports;
schema-v1 result files remain readable.

The Run button requests microphone permission only when pressed and refuses to
start while the transmitter is armed, keyed, tuning, or running two-tone. The
measurement session itself has no `RadioState`, `TXCoordinator`, `TXChain`,
ARM, PTT, or protocol-command dependency. Closing the window or pressing
Cancel tears down both audio engines and the input tap. Aggregate devices are
marked with a warning because earlier CoreAudio restart storms involved such
routes.

The first live BlackHole 2ch run also serves as an executor-safety gate: the
player schedules without an inherited completion closure, and the input tap
is created by the checked-Sendable capture processor rather than inheriting
the main actor. Five same-device virtual-loopback trials completed with full
confidence and effectively zero added delay/jitter.

## ANAN PA-feedback segment

When an ANAN Protocol 2 radio supplies a retained PureSignal analysis, the map
also shows its measured DAC-reference-to-coupled-PA-feedback delay and
correlation. This reuses the synchronized 192 kHz reference/feedback IQ pair
and is read-only: the latency window cannot enable capture, arm, or key the
radio. A capture still comes only from a separately approved dummy-load
transmission through the PA Linearity workflow.

This is a real physical endpoint but only a bounded segment. It does not begin
at the microphone callback and therefore is never labeled as end-to-end
microphone-to-PA latency. Network transit and the host-to-radio-reference
portion remain unknown until a common-clock probe spans the complete path.

## Later measurement phase

Phase 3 will add a separately gated RF-feedback or demodulated-return workflow
with explicit dummy-load acknowledgement, hard key-down timeouts, and an abort
path. Until a physical return path exists, neither the map nor the software
fixture may be described as microphone-to-PA latency.

## Analyze saved measurements

Open regular local files for saved measurements. The importer bounds capture,
recipe, calibration and comparison inputs before decoding, and refuses
symbolic links and pipes. Select the original file if you have a link to it.

In **TX Latency → Analyze**, choose **Compare Software Maps** to compare
matching stage IDs. A stage that changes from estimated to measured is
flagged as a provenance change. Deltas are shown for enabled stages with
comparable evidence. The two saved configurations and capture times are
shown alongside the changes.

**Compare Loopback Runs** reads exported version 1 or version 2 JSON,
recalculates the summaries from raw trials, and shows raw and calibrated
deltas. Check the route and probe indicators before attributing a difference
to a processing change.

**Analyze Stereo Capture** reads a synchronized two-channel WAV up to
60 seconds long. Put the reference on channel 1 and the return on channel 2.
Select demodulated audio or a detected RF envelope, mark the reference
windows and specify the maximum expected lag. Enter a separately measured
fixed calibration if available. Use **Calibration → Save Profile…** after a
capture has established the sample rate. The profile records the route, method,
date, channel, return type and independently known fixed delay. A loaded
profile must match the sample rate, reference channel and return type before
it is applied. The result carries raw and calibrated delay,
trial confidence, polarity, clipping flags and rejection decisions. With
three or more accepted windows spanning at least three seconds, it also
reports a delay trend and the remaining variation around that trend.
The app analyzes the capture offline. The physical meaning of the result
depends on where the two recorded signals were sampled.
