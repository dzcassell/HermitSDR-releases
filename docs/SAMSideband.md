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

## Stereo sidebands

**Stereo** is the fourth choice (#428): the lower sideband in the left ear and
the upper sideband in the right, so interference on one side of the carrier
sits in one ear and your hearing does the rejection. Two controls appear under
the selector while it is chosen:

- **Swap left and right** puts the upper sideband on the left instead.
- **Width**, 0–100 %. 100 % is one sideband in each ear. 0 % is the Both
  audio in both ears. Turn it down for loudspeakers.

**ST** on the compact width button marks the choice. Both sidebands stay
painted on the spectrum and audio notches behave as on Both. Width and swap are
saved with the sideband choice in receiver settings, per-radio receive profiles
and named receive DSP presets; older settings restore 100 %, not swapped.

**Who hears two channels.** Only this Mac's speakers and headphones, and only
from the main receiver in SAM on a channel of 11 kHz or less. Everything else
gets the normal Both mix, sample for sample what Both delivers:

| Consumer | Gets |
| --- | --- |
| This Mac's audio output (speakers, headphones, a virtual device) | Left and right |
| Decoders and the audio mini-waterfall | Both mix |
| WAV recording and gated recording | Both mix (the recorder is mono) |
| Streams and other outputs (YouTube Live, Discord, Control API audio, remote listeners) | Both mix (mono feeds) |
| The radio's own audio output / headphone codec | Both mix |
| SUB receiver | Both, as before |
| Channels wider than 11 kHz (the 24 kHz audio path) | Both mix at full width: there is no 24 kHz stereo route to the speakers yet, and the popover says so |

**From another program.** The Control API reads and sets the choice
(revision 4): the state key `samSideband` is `both`, `upper`, `lower` or
`stereo`, and `{"t":"setSAMSideband","sideband":"stereo"}` selects it — the
same setter as the popover, with the same fallbacks. The client's own audio
downlink stays the mono Both mix. See [ControlAPI.md](ControlAPI.md). There
is no CAT or MCP command for it, and the width and swap controls are not in
the API.

**AM stereo (C-QUAM).** Both features want the two output channels, so they
are mutually exclusive. While Stereo is selected the AM stereo channel selector
in the DSP popover is disabled, with a line saying why, and the mono mix is the
plain synchronous sum whatever channel was saved. Returning to Both restores
the saved Mono/Left/Right choice. The pilot lamp keeps working.

**Loudness.** An ordinary AM programme has identical sidebands, so both ears
carry exactly the Both audio and nothing changes level when you switch.
Content on one sideband only (the interference this is for) is 6 dB stronger in
its own ear than it was in the Both mix and absent from the other, the same
level the Upper or Lower choice gives it.

### How the pair is made

The mono chain is not touched. The pair is built beside it as mid and side:
the mid is the finished Both audio, and the side signal is half the difference
of the Lower and Upper detectors, taken from the same Hilbert phasing filters
and the same delayed carrier the single-sideband choices use. Left is mid plus
side, right is mid minus side, with the side scaled by Width (negated by Swap).

| Stage | Treatment of the pair |
| --- | --- |
| S-meter, squelch decision, decoder tap, fade leveler | Mid only. The side signal's carrier residue (a carrier slightly off the dial) is removed with the leveler's own 20 ms tracker |
| NRSC de-emphasis, auto-notch, audio EQ | The side signal runs through its own copy of each with the same settings |
| AGC | One gain for both ears: computed from the mid by the normal AGC and applied to the side signal with the same look-ahead, so the image does not move with level. AGC Off applies the same fixed gain |
| Squelch gate and setting-change duck | The same envelope on both |
| Noise reduction (all four kinds), Audio Unit inserts | Mid only. They are single-channel processors with their own delay, so while one is on both ears get the processed Both audio |
| Per-ear peak limiter | New, Stereo only: one linked gain holds each ear at 0.95 full scale, because one-sided content can be 6 dB above the level the AGC set from the mid. Idle, it does not alter a sample |

**Carrier loss.** A lock detector watches the loop's own output (carrier
average over 15 ms against total power over 60 ms; locked above 0.5, unlocked
below 0.35). When the carrier goes, the side signal fades out in 8 ms and both
ears carry the mono Both audio; it returns about 130 ms after the carrier is
held again. The pair is delayed 20 ms more than the phasing filters need so
that this decision arrives before the audio it concerns. Without that head
start an abrupt carrier loss rang through the phasing filters and reached the
ears 2.75 dB above the mono chain's own thump; with it the pair adds nothing.

**Latency.** The speakers run **30.667 ms** behind the mono consumers while
Stereo is selected (10.667 ms phasing delay plus the 20 ms above). Choosing
Stereo, retuning, changing mode, a replay jump and the end of a transmission
restart the side path from silence; width and swap changes slew over 30 ms.

**Transmit.** While the transmitter is keyed the side path is idle like the
other post-detector stages, and it restarts from rest at unkey.

### Stereo acceptance

`SAMStereoTests`, synthetic signals through the production chain at 96 kHz
input, 10 kHz channel, carrier 73 Hz off the dial, a 1 kHz tone on the lower
sideband only and a 1.6 kHz tone on the upper sideband only:

| Case | Required | Measured |
| --- | --- | --- |
| Separation, carrier at −6, −70, −80 and −100 dBFS, AGC Medium | 40 dB in each ear | Left 63.7–63.9 dB, right 61.7–61.8 dB |
| Same at −80 dBFS with AGC Off, AGC Slow, EQ plus de-emphasis | 40 dB | Worst 60.8 dB |
| Mono outputs (speaker-chain audio and decoder tap) versus Both | Identical samples | Identical in every case above |
| Conventional AM programme, each ear versus Both | Within 0.1 dB | +0.03 dB |
| Width 0 % | Both audio in both ears | Identical samples, 368 samples later |
| Whole signal vanishes abruptly, returns 2.5 s later | No peak or sample-to-sample step above the settled pair or the Both mix; mono while unlocked | Peak −0.02 dB / +0.00 dB, step +0.00 dB; ears identical to the Both mix from 0.3 s after the drop |
| Carrier alone fades out over 100 ms, sidebands remain | Finite, under the ceiling | Ear peak 0.580 against 0.577 for Both |
| Noise reduction on, transmit key cycle | Mono during, 40 dB separation after | Met |

Not covered: nobody has listened to it, on headphones or speakers, on a real
station. The tones are steady; programme audio, real selective fading and
real adjacent-channel splatter are untested. The separation figures are for
these two frequencies; below 300 Hz the Hilbert transition weakens separation
as it does for Upper and Lower. A very strong one-sided signal (stronger than
the carrier) can pull the lock detector below its threshold and collapse the
image exactly when it is wanted, and the per-ear limiter then also works
hard. In a very narrow SAM filter the detector can report lock on band noise;
the result is noise that is wider than mono, not a burst.

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
