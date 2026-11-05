# Hi-Fi SSB Profile Laboratory

For agent-authored comparisons, see the [offline recipe and report format](../skills/hermitsdr-lab/references/commands.md#compare-ssb-audio).

The Hi-Fi SSB Profile Laboratory is an offline listening and measurement tool
for HermitSDR's built-in SSB voice profiles. Open it from
**Transmit ▸ SSB Profile Lab**.

It cannot transmit. The window is constructed without `RadioState`,
`RadioEngine`, `TXCoordinator`, a protocol connection, or an ARM/PTT action.
It creates a private, unkeyed `TXChain`, feeds local 48 kHz mono audio into it,
and captures the production post-limiter audio tap.

## A useful comparison

1. Import a CoreAudio-readable file, or record a natural one- or two-sentence
   microphone passage. The microphone recorder stops after ten seconds. An
   imported file is bounded to thirty seconds.
2. Pick profiles A and B. Studio SSB 3.0k and Wide ESSB are a useful first
   pair: one keeps broadcast-style voice inside a normal-width SSB channel;
   the other exposes the lows and top octave that extended SSB can preserve.
3. Choose **Render Comparison**. Both profiles receive the exact same source,
   after DC removal and repeatable 0.70-peak normalization.
4. Listen to Original, A, and B. Playback uses a shared active RMS target,
   normally −20 dBFS. A high peak in any clip lowers the target for every
   clip. The measurements describe the renders before the playback gain.

Changing either picker invalidates the old result. Render again to measure and
hear the new pair.

## What the numbers mean

- **Active RMS** averages 20 ms speech windows within 30 dB of the passage's
  loudest window, so pauses do not make a profile look quieter.
- **Peak** and **crest factor** describe headroom and density.
- **99% occupied** gives the low and high audio offsets containing the central
  99% of measured spectral energy. For USB these offsets map above the carrier;
  for LSB they mirror below it.
- **Outside profile** is energy outside the selected profile's configured
  passband relative to energy inside it. It is a baseband containment check.
- **Compressor max**, **limiter max**, and **near 0.95 ceiling** show how hard
  the production dynamics worked on this passage.
- **Warmth**, **body**, **presence**, and **air** are shares of total measured
  spectral energy in 50–300, 300–1000, 1000–3000, and 3000–5000 Hz bands.

The response plot is calculated from the same 513-tap profile bandpass and
three voicing-EQ biquads used by `TXChain`; it is not a hand-drawn marketing
curve.

## Scope and interpretation

The first release compares built-in profile voicing: profile bandpass, phase
rotation, profile EQ, profile compressor, always-on lookahead limiter, and
post-limiter cleanup. It intentionally does not copy the live window's user EQ,
optional gate, platform AGC, de-esser, multiband choice, rack, effect, mic NR,
or CESSB settings. That keeps the question precise: *what does this built-in
profile itself do to the same voice?*

This is a baseband prediction and listening tool, not RF proof. It does not
measure microphone/interface distortion, the DAC, PA linearity, RF occupied
bandwidth, antenna system, a receiver's filters, or propagation. Use the TX
Meters and PA Linearity instruments—and an explicitly approved dummy-load
session—when those are the question.


## Audition a draft recipe

Load a voice take and choose **Audition Recipe…** to compare two to four
trials from a local JSON file. Each trial uses a built-in base profile and
can add graphic EQ or parametric EQ and a single-band compressor override.
The sheet shows before-playback metrics and lets you hear each trial at the
same target. The same recipe works in the headless command and with the
operator-shared MCP voice experiment.
[Recipe formats and commands](../skills/hermitsdr-lab/references/commands.md)
