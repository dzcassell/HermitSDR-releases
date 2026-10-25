# SAM RF sidebands

In SAM, open the receive-filter width button and choose **Both**, **Upper** or
**Lower** under **SAM RF sideband**. Center the carrier first, then choose the
side with less interference. The width remains the full nominal channel width:
for example, a centered 10 kHz channel supplies 0–5 kHz on Upper or −5–0 kHz on
Lower. The selected side is painted on the spectrum; **U/L** on the compact
width button keeps the active choice visible after the popover closes.

This first milestone applies to the **main receiver** at the existing 12 kHz
and 24 kHz AM IF rates. **SUB remains Both/mono**, whether it follows main or
uses independent settings. There is no automatic sideband chooser.

**Both is the unchanged default.** It retains the original SAM and C-QUAM
path. Upper/Lower produces mono audio, so the AM stereo channel selector is
disabled while either is selected. Returning to Both restores the saved
Mono/Left/Right preference. The 25 Hz pilot detector can still indicate a
C-QUAM transmission while listening to one RF sideband.

The selection is saved with receiver settings, per-radio receive profiles and
named receive DSP presets. Older presets, absent fields and unknown spellings
restore Both without discarding the catalog. RF-center tuning, display panning,
RIT, IF notches, sample rate and raw IQ recordings retain their existing paths.
Audio-waterfall notches follow the selected RF side; an RF notch stays at its
signed channel offset when changing sides.

## Processing and latency

The original PLL always receives the complete filtered complex IF. In parallel,
an original Blackman-windowed Hilbert phasing separator combines delayed I/Q
with their quadratures to select positive or negative RF frequencies. Its
product detector uses the recovered carrier delayed by exactly the same number
of samples. Separating the already-rotated Q arm instead would turn PLL motion
back into audio interference. No upstream implementation or coefficients are
copied and no dependency is added.

The 257-tap narrow and 513-tap wide filters add **128/12,000 = 256/24,000 =
10.667 ms** of steady audio group delay. Every call emits exactly the input
sample count, including warmup; there is no extra FFT block or decoder-clock
jump. Both bypasses the separator and adds no delay. An independent gated-chirp
correlation of the production speaker taps measured exactly 128 samples at
12 kHz and 256 at 24 kHz for both choices, with normalized correlation above
0.9999999978. Choice changes interpolate over 20 ms under the existing audio duck; RF retunes, mode/rate changes and
replay discontinuities discard old phasing history.

The original carrier level feeds the existing fade leveler in all selections.
Using the selected carrier amplitude here could double the DC of a slightly
mistuned carrier and compress wanted audio in the existing AGC-Off limiter.

## Offline acceptance and limits

`SAMSidebandTests` uses conventional AM with a wanted 1 kHz program and an
independent interfering tone confined to either RF sideband. All stated
frequency ranges describe tested points, not an exhaustive RF sweep:

| Case | Tested points / bound | Measured worst result |
| --- | --- | --- |
| Separator with known carrier phase | 300, 700, 2,200 and 5,000 Hz at 12 kHz IF; upper point 9,500 Hz at 24 kHz IF; carrier offsets −100/0/+100 Hz | 72.47 dB unwanted rejection; wanted error below 0.000019 dB |
| Full production chain, steady or 14 dB selective carrier fade | Same points; recovered carrier offset +73 Hz; both side choices; ≥30 dB rejection and ≤0.25 dB wanted change versus Both required | 38.80 dB rejection; 0.031 dB wanted change |
| Deliberate 20 dB selective carrier fade stress | 300/700 Hz; carrier can become weaker than remaining modulation; original PLL retained | 28.49 dB rejection; outside the 30 dB acceptance envelope |

The fading fixture changes only carrier amplitude (0.7 Hz sinusoidal fade),
leaving modulation and the interfering sideband present. The acceptance case
ranges from 0.5 to 0.1 carrier amplitude; the separate stress case reaches 0.05.
Very deep fades and low-frequency content can therefore reduce rejection.
The Hilbert transition also weakens separation below 300 Hz. Width and IF-shift
controls still work at their normal limits, but they cannot create useful
one-sideband audio when the selected half is outside the channel.

The existing narrow AM/SAM/DSB baseline remains within its pinned **1e−6 ×
max(1, reference)** sum/energy tolerances. Further checks cover fractional
stream blocks and resets, silence/reacquisition, rapid controls, width/rate
limits, replay resets, decoder/speaker sample-count agreement, C-QUAM mono and
stereo restoration, preset migration, main/SUB separation, and production
Dark/Light filter rendering at 280 points. Actual VoiceOver navigation and
real MW/SW listening remain operator acceptance; no audible on-air improvement
is claimed from these synthetic tests.

## Optimized CPU receipt

Measured on Apple M4 Pro / Mac16,11, arm64, Version 27.0.1 (Build 26A434). The existing deterministic
benchmark runs 500 five-millisecond input blocks per scenario (2.5 seconds of
synthetic IQ), after warmup, with no other build or timing-sensitive test running.
These are DSP simulation measurements, not radio/network/audio-device latency.

| Channel / IF | Both p99 | Upper p99 | Lower p99 | Both / Upper / Lower process CPU for all 500 blocks |
| --- | --- | --- | --- | --- |
| 10 kHz / 12 kHz | 66.25 µs | 88.42 µs | 87.63 µs | 8.40 / 9.62 / 9.86 ms |
| 20 kHz / 24 kHz | 71.42 µs | 100.67 µs | 98.75 µs | 10.34 / 13.47 / 13.56 ms |

Every scenario stays below the existing **5,000 µs** p99 deadline. Additional
process CPU versus Both is about **0.05–0.13% of one core** for this input;
all six scenarios have **zero live malloc block/byte growth after warmup**.
This is not a claim of zero transient allocations. The complete benchmark smoke
passes in **11 seconds**, against its unchanged **30-second** limit.
