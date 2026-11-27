# AM co-channel canceller

Two AM broadcast stations on the same channel are normally heard as the
stronger one with the weaker one underneath. The co-channel canceller removes
one station so the other can be heard. It works in **AM** and **SAM**, on the
main receiver, on live signals, the time machine and Band DVR or `.hiq`
playback alike (they all run through the same receive chain).

It is off until you turn it on, and it starts off at every launch.

Nothing here has been heard on a real pair of stations yet. Every figure on
this page was measured on generated signals at the levels the stage sees in
the receiver (carriers 60 to 100 dB below full scale).

## Using it

Open **DSP** in AM or SAM and switch on **Co-channel canceller**.

- **LOCK** lights when the stage is holding a carrier. The number beside it
  is the depth: how far the stage lowered the power in the channel, in dB.
- **Remove › Strongest** removes the strongest carrier within 100 Hz of the
  dial. It changes to another carrier only when that one has been at least
  6 dB stronger over the last ten seconds.
- **Remove › By offset** removes the carrier nearest the **Offset** you set
  (hertz from the dial, 0.1 Hz steps), if there is one within 1.5 Hz.
- Under these is the list of carriers found within 100 Hz of the dial over
  the last ten seconds, strongest first, with offset and level. Click one to
  remove that station; the one being removed is highlighted. A carrier
  within 1 Hz of a stronger one is listed only when it is within 6 dB of it,
  and two carriers closer than about 0.25 Hz appear as one.
- **Width** is the audio bandwidth of the station being removed, in kHz.
  **All** removes it across the channel. A smaller value leaves the channel
  untouched above it, which helps when the station you want is wider than
  the one you are removing. It adds 5.3 ms of delay.
- The line of text says what the stage is doing.

The output is brought back to the level of the input, so switching the
canceller on and off compares clarity, not loudness. The S-meter and the
squelch keep reading the channel as received, not what is left of it.

What you will hear:

- **Two carriers at least 1 Hz apart.** The stronger station goes and the
  weaker one is rebuilt at normal level. Twice in every beat between the two
  carriers the weaker station dips for a moment (about a tenth of the time
  it is more than 3 dB down). With carriers 3 Hz apart that is six short dips
  a second.
- **A weaker carrier within 1 Hz of the removed one.** The stage cannot tell
  it from the removed carrier's own fading, so it does not rebuild it. The
  stronger station still goes, and the weaker one is heard rising and falling
  slowly at twice the beat rate. The status line reads "No second carrier
  found".
- **One station only.** It is removed and the channel goes quiet: what is
  left is the band noise, at its own level (the receiver's AGC will then
  bring that noise up, as it does on an empty channel).
- **No carrier.** The stage passes the audio through untouched and the
  status line says so. The same applies in By offset when no carrier is
  within 1.5 Hz of the offset.

After a retune, a mode change, a jump in the time machine or a transmission
the stage starts again: about one second to lock, about one more before the
second station is rebuilt.

## What was measured

Generated signals, 12 kHz channel, each station carrying three programme
tones with speech-rate envelopes at 50 % modulation. "Audio ratio" is the
kept station's audio over the removed station's audio after detection.

| Case | Result |
| --- | --- |
| Two stations 3 Hz apart, stronger +20 dB, carriers −60 / −80 dBFS | audio ratio −23.0 dB → +24.4 dB: **47 dB better**; depth 20.7 dB; LOCK on |
| The same at −80 / −100 dBFS | 47 dB better |
| The same at −6 / −26 dBFS | 51 dB better |
| The same through the whole receive chain, AM 8 kHz, SAM 8 kHz, AM 16 kHz (carriers −70 / −90 dBFS) | 45 dB better in each |
| Stronger +6 dB, 3 Hz apart | 47 dB better |
| Stronger +30 dB, carriers 30 Hz apart and off the dial | 68 dB better |
| Weaker carrier 0.7 Hz from the stronger (not rebuilt) | 37 dB better |
| Stronger station fading ±10 dB at 0.2 Hz with ±0.6 rad of carrier phase at 0.3 Hz | 45 dB better over 11 s; in the worst third of a second the removed station's audio is 7 dB **below** its uncancelled level as heard (23 dB of level match on), 33 dB below before the level match |
| One station, selected by offset | channel level down 52.8 dB |
| Removing the weaker of two (−70 dBFS, with −60 dBFS 3 Hz away) | its audio 31 dB further down |
| Noise only, or no carrier at the offset | output identical to the input, sample for sample |
| Canceller off | AM and SAM audio identical to a build without the stage, sample for sample |

The issue's target was 20 dB. The 47 dB figures are limited by the test
signal's own noise in the bands being measured (50 dB below the stronger
carrier), not by what the stage leaves behind.

Processing cost on an Apple M4 Pro, optimised build: 0.34 % of one core at
the 12 kHz channel rate and 0.56 % on the wide (24 kHz) path. Twice a second
one block also carries the carrier analysis and takes 0.8–0.9 ms. See
`docs/PerformanceBudget.md`.

## Limits

- The removed station must be ordinary AM. A C-QUAM stereo station carries
  programme in quadrature with its carrier, and that part stays.
- Selective fading that turns a station's sidebands against its own carrier
  leaves a remainder. The scripted fade above moves amplitude and phase of
  the whole station together; real sky-wave fading has not been tried.
- Where the two carriers pass through each other's phase the two stations
  cannot be told apart by any processing. The stage dips the kept station
  there instead of letting the removed one through.
- A third station is neither removed nor rebuilt cleanly.
- Removing the weaker of two stations works less well than removing the
  stronger: the phase reference is taken from the weaker carrier, with the
  stronger station's low audio beside it.
- The kept carrier must be within 100 Hz of the removed one, and both within
  100 Hz of the dial.
- While the switch is on, **CCC** shows beside the squelch badges in the
  control bar and the console: bright in AM and SAM, dim in any other mode
  (where the stage is idle). Its tooltip says what it is doing.
- Main receiver only. SUB is not processed.
- The switch is not saved between launches, in per-radio profiles or in
  receive DSP presets. The carrier choice, offset and width are saved.

## Not included

- The zoomed ±50 Hz carrier strip with click-to-select. The carrier list
  with click-to-select stands in for it.
- Carrier Sleuth's single-tone estimator (`CarrierToneEstimator`) is not
  used: it measures one tone in real audio, and this stage needs every
  carrier in the complex channel, so it has its own analysis.

## How it works

Two AM stations in one channel are `d(t)·e^{jφ1} + a(t)·e^{jφ2}`, where `d`
and `a` are the two envelopes (carrier plus programme). Both are real: AM
puts nothing in quadrature with its own carrier. Turned back by the first
carrier's phase, the channel is

    I = d + a·cos θ        Q = a·sin θ        θ = φ2 − φ1

so the quadrature arm holds the second station and none of the first,
whatever their levels and however the first station's amplitude fades. With
θ known, the first station is `I − Q·cot θ`. Put back on its carrier and
subtracted from the channel, it leaves `a·e^{jφ2}`: the second station alone,
which goes on to the normal AM or SAM detector.

- **Carriers.** The channel is decimated to 400 Hz. A Hann-windowed
  transform of the last ten seconds lists the carriers; a carrier must also
  be present in the last second. An equal pair either side of the removed
  carrier is its own modulation (a steady bass note, mains hum) and is not
  listed. A line within 1 Hz of a stronger one and more than 6 dB below it is
  taken as that carrier's fading skirt.
- **Tracking.** The removed carrier has a second-order phase-locked
  oscillator. The kept carrier has its own, corrected from the quadrature
  arm only when it is the weaker one, so the removed station's fading cannot
  disturb the angle θ. Loop bandwidths are 0.25–1 Hz, set by the spacing.
- **Fine phase.** A phase error on the removed carrier leaks that station
  into Q. A fast loop (40 ms) turns the pair until Q carries nothing that
  correlates with the removed station's own audio. It follows a fading
  path's phase far faster than a carrier loop can. It runs only while the
  removed station is at least 6 dB the stronger.
- **Where sin θ is near zero** the division is limited to a gain of 5.

The code is `HermitSDR/DSP/AMCochannelCanceller.swift`; the tests are
`Tests/DSPTests/AMCochannelCancellerTests.swift`. It was written from these
first principles; no other program's implementation was consulted.
