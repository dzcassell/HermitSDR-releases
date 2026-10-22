# Receive filter phase: Linear / Low latency (#221)

The receive channel filter is a 513-tap complex bandpass run as 1024-point
fast convolution (`FFTChannelFilter`, `HermitSDR/DSP/Filters.swift`). As
shipped it is **linear-phase**: a symmetric impulse with a constant delay of
256 samples — 21.333 ms at the 12 kHz IF, 10.667 ms on the 24 kHz wide path.
That is the default and it is unchanged: with *Linear* selected the filter is
bit-identical to the one in every earlier release (pinned by a frozen copy in
`Tests/DSPTests/FFTChannelFilterReferenceFixture.swift`).

**Low latency (experimental)** rebuilds the same design as a minimum-phase
filter: the magnitude response — passband width, droop compensation, manual
notches, ~100 Hz skirts and the −110 dB stopband — is kept within 1e-5 dB, and
only the phase is re-shaped so the impulse energy arrives at the front. The
construction is the homomorphic spectral factorisation validated offline in
[docs/bench/2026-10-15/rx-filter-latency.md](bench/2026-10-15/rx-filter-latency.md),
now run in the app on fixed 65,536-point double-precision transforms (about
4 MB of transient scratch, freed on return) on the main thread like every other
filter rebuild — never on the DSP thread. In the Debug test build a rebuild
takes about 2.4 ms (median), printed by `FilterPhasePolicyTests`.

## Where

Receive filter popover (the width button in the control bar) ▸ **Filter phase**,
below *Shift*. Ask The Crab: `rx.filterPhase` = `linear` or `lowLatency`. The
choice is saved per radio in the operating catalogue (`rxFilterPhasePolicy`)
and in the shared defaults (`rxFilterPhase`); a catalogue written before the
control restores nothing, and an unknown spelling restores linear.

## What it saves (measured, no radio or audio device)

| Filter / IF rate | Median phase delay, Linear → Low latency | Speaker-tap onset advance in the production chain at 96 kHz |
| --- | ---: | ---: |
| USB / LSB 300–3000 Hz, 12 kHz | 21.333 → 1.277 ms | 20.08 ms (callback delivery 47.33 → 27.25 ms in the 2026-10-18 study) |
| CW 100 Hz, 12 kHz | 21.333 → 14.765 ms | 6.42 ms (47.33 → 40.92 ms) |

Interior passband magnitude differs by at most 7.8e-6 dB across the five
nominal filters of the October study, stopbands within 0.3 dB, and more than
99.99 % of the impulse energy stays inside the 513 taps. The production-chain
figures and the per-filter table come from `Tests/DSPTests/FilterPhasePolicyTests.swift`,
which reproduces the report's method (65,536-point analysis, interior
passband trimmed by 100 Hz or 20 % of the width).

## What it does not change

- The overlap-save batching (512 output samples per block), the decimators,
  AGC look-ahead, SNB, NR and the Mac / radio audio output cushions. The
  2026-10-18 study's modeled consumer figures (Mac 216 → 196 ms, radio
  90 → 70 ms for SSB) show the filter saving riding on top of unchanged
  buffering; CoreAudio, DAC, network and radio firmware latency were never
  part of these measurements.
- The decoders. FT8/FT4, JS8, WSPR, SSTV, WEFAX, CW, RTTY, ALE, Contestia and
  the hosted digital modes are fed by a linear-phase twin of the filter
  (`RXChain.decoderChannelFilter`) whenever the speaker filter is low latency,
  on the same block schedule, so their audio is bit-identical to Linear. The
  passband mini-waterfall shows the same linear feed.

## Exclusions (keep linear phase whatever the setting)

The October studies qualified the single-sideband detector paths only, so the
policy is honoured for **USB, LSB, CW, DATA-U and DATA-L on the main receiver**
(`RXMode.honoursFilterPhasePolicy`). Everything else is built linear:

- **AM, SAM (narrow and wide) and DSB** — envelope / PLL / product detectors;
  their source-envelope qualification failed in the pipeline study, and the
  C-QUAM stereo decoder rides the SAM path.
- **FM / NFM** — discriminator, not studied.
- **The SUB receiver** (independent, diversity and coherent combining) and
  the **FT8 sub-band monitor chains** — separate `RXChain`s that are never
  given the policy (`RadioEngine.rxFilterPhasePolicy` reaches the main chain
  only).
- **Binaural CW** runs after the filter on the speaker path and is unaffected
  in construction; it has not been listened to with the low-latency filter.
- **Transmit** filters, CESSB and RF envelopes are outside #221 entirely.

## Transitions

A policy change rebuilds the current filter through the same path as a width
change: the new filter inherits the overlap-save input history (no gap, no
repeated samples) under the chain's 60 ms raised-cosine duck. The test switches
a steady USB tone both ways at four instants across one hop and measures a
largest sample-to-sample step of 0.212 against the tone's own slope of 0.212,
no overshoot, and the same output length as an unswitched run.

## Status

Experimental. Still owed before it leaves that label: recorded and live
listening comparisons (intelligibility, ringing on CW keying, adjacent-signal
transients), coherent/stereo and wider decoder coverage, and operator-assisted
physical RX measurements. The default stays Linear.
