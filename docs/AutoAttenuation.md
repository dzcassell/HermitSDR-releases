# Automatic attenuation on ADC overload

The **Auto** latch beside the RF gain slider (control bar; **Auto gain** in
the console's receiver panel) adds front-end attenuation while the radio's
ADC overloads and takes it off again when the band calms down. It is off by
default and receive-side only: it never keys, arms or tunes anything, and it
does nothing at all while you transmit.

## What it does

- **Your RF gain setting is the ceiling.** The slider, band memory,
  bookmarks and profiles keep the value you chose. Auto only ever runs the
  radio *below* it, and shows by how much.
- **Overload → attenuate.** When the ADC OVF lamp stays lit for about a
  tenth of a second (or flickers repeatedly), 3 dB is added. If that is not
  enough, another 3 dB follows every 0.4 s, and 6 dB at a time after the
  third step. A single static crash is ignored.
- **Quiet → recover.** After 30 s with no overload, 3 dB comes off, then
  3 dB more every 10 s, until the radio is back on your setting.
- **No pumping.** If the overload returns within a minute of a step back,
  the next quiet time doubles (30 s, 1 min, 2 min … up to 10 min). It
  resets once your own setting has held for 30 s. At most six steps back
  happen in any minute.
- **You win.** Move the RF gain slider (or set the gain through the Control
  API or the crab) and the radio goes to exactly that value at once. Auto
  starts again from there.
- **Per-band memory.** The attenuation a band needed is remembered and
  applied the moment you return to it, so the band is not re-learned
  through a burst of clipping. Outside the amateur bands the memory is
  kept per MHz. It survives quitting the app.
- **Transmit.** While keyed, tuning or running a two-tone or PureSignal
  capture, Auto holds exactly where it is. What the ADC saw during the
  transmission is discarded, and the quiet time starts over afterwards.

Turning Auto off returns the radio to your RF gain setting immediately.

## What you see

- **Header chip**, right of the ADC OVF lamp, only while Auto is on:
  - `AUTO ATT` (dim): on, adding nothing.
  - `AUTO ATT +9 dB` (amber): 9 dB added to your setting.
  - `AUTO ATT +31 dB MAX` (red): the radio has no attenuation left and the
    ADC still overloads. Use an external attenuator, a band-pass filter or
    a smaller antenna.
  Hover for the state in words.
- **Receive Health** (Digital Modes header, the cue beside FT8/FT4, About ›
  Copy System Information) reports `autoAttenuated` with the amount, and the
  evidence line carries `auto att +N dB`.
- **The S-meter does not move.** The dBm reading, squelch threshold,
  overload mute and the panadapter's dBm reference follow each step, so a
  steady signal reads the same before and after. For a fraction of a second
  around a step the reading can flick by the size of the step while the
  radio catches up.

## Radios

| Radio | What Auto moves | Range |
| --- | --- | --- |
| ANAN / Protocol 2 | ADC step attenuator (both ADCs while diversity or SUB-on-ADC1 is on, so the pair stays matched) | down to −31 dB |
| Hermes-Lite 2 / Protocol 1 | LNA gain | down to −12 dB |
| NetSDR | front-end attenuator, in its 10 dB positions | down to −30 dB |
| SDRplay RSPdx | RF gain reduction (the RSPdx's own AGC, in Settings, is the better tool there) | per band |
| FlexRadio, radios with a fixed gain | nothing; the chip stays dim | — |

On a Protocol 2 radio a new attenuator value travels in the next
high-priority packet (every 100 ms), so the hardware follows the decision by
up to a tenth of a second.

## Limits

- It acts on the radio's overload flag. A radio that reports no flag
  (FlexRadio) never triggers it.
- Without a peak-level reading it can only find out whether a step back is
  safe by trying it. Expect one short overload flicker per attempt on a
  band that is still strong; the doubling quiet time keeps those rare.
- The enable is one switch for all bands; only the learned value is
  per band.
