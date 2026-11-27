# Display options, tuning conventions and status readouts

A group of receive-side options from the interface survey (#495). Every one
is off, or set to the picture and gestures the app already had, until you
change it. None of them changes what is transmitted, and none touches the
audio path. They are in the **View** menu.

## Density spectrum

**View › Spectrum › Density Spectrum** replaces the filled trace with a
colour cloud of where the trace has been, and draws the average trace over
it in white.

- Each point of the cloud is one frequency bin at one level. Its colour says
  how much of the recent past the trace spent there: deep blue for rarely,
  through cyan and yellow, to near white for almost always.
- A steady carrier is a bright spot. A signal that is only there some of the
  time (a keyed carrier, a burst, a fading station) leaves a fainter smudge
  at the level it reaches, above the noise it sits in the rest of the time.
- **Density Memory** (2, 8, 30 or 60 seconds) is how long a point takes to
  fade to about a third. Longer shows rarer events and reacts more slowly.
- The peak-hold line is still drawn if it is on. The fill, the violet ghost
  trace and the green phosphor trail are not: they would cover the faint
  points the mode exists to show.
- Retuning the radio, or dragging the display far enough that the radio
  retunes, empties the cloud.

Cost: nothing while the mode is off (its GPU resources are created the first
time it is switched on and released when it is switched off). While on it
holds a 16 MB texture and adds, per frame that brings a new spectrum row, one
blend over that texture, one point per bin and one quad. Measured offscreen
on the build Mac (M5 Max) at 8192 bins and a 2560 × 500 pixel pane: about
0.14 ms of GPU time for a frame with a new row and 0.07 ms for a frame
without, 0.32 and 0.16 ms while other builds were running. The app's status
bar shows the whole frame's GPU time.

## Waterfall height as a time span

**View › Waterfall › Time Span** sets how much time the waterfall shows from
top to bottom: the last 30 seconds, 2 minutes or 10 minutes. It works out
the rows per pixel from the measured row rate and the height of the pane,
and follows when you resize the window or change the waterfall speed.

- **Use History setting** (the default) hands control back to the
  **History** presets (Live scroll, ×2, ×4, ×8).
- The waterfall never stretches rows, so a span shorter than one row per
  pixel shows one row per pixel. At 30 rows a second a 400-pixel waterfall
  shows at least 13 seconds.
- It cannot show more than the history the waterfall keeps. If 10 minutes
  does not fit, it shows all it has.

## Peak hold decay

**View › Spectrum › Peak Hold Decay**: Hold until cleared, Slow, Normal (the
previous behaviour), Fast or Very fast. **Clear Peaks** on the panadapter
restarts the line from the current spectrum, as before.

## Trace width and scale text size

- **View › Spectrum › Trace Width**: Hairline (the previous one-pixel line),
  1.5, 2, 3 or 4 points.
- **View › Spectrum › Scale Text Size**: Small, Normal, Large, Larger or
  Largest, for the dB labels on the left and the frequency labels on the
  ruler. The ruler grows a little taller with the larger sizes.

**View › Reset Display to Defaults** puts the display options on this page
back (density spectrum, time span, peak decay, trace width, text size,
impulse blanking, markers through the waterfall), sets History to Live
scroll and clears the peak-hold line. It leaves the palette, the level
sliders, zoom, the tuning conventions and the status readouts alone.

## Waterfall impulse blanking

**View › Waterfall › Impulse Blanking** keeps wide noise bursts (lightning
crashes, switching transients) from painting bright stripes across the
waterfall. When the typical level of a whole row jumps 6 dB or more above
the rows before it, the waterfall repeats the last clean row instead.

- It is display only. The spectrum trace, measurements, decoders and the
  audio are untouched; use NB for the audio.
- At most three rows in a row are replaced. A change that lasts (the band
  opening, a preamplifier switched in) then comes through and becomes the
  new normal.
- A narrow signal, however strong, never triggers it: it looks at the
  middle level of the whole row, not at peaks.

## Markers through the waterfall

The VFO line, the passband shading and the notch markers have always run
down through the waterfall. **View › Spectrum › Markers Through the
Waterfall** is on by default; switch it off to stop them at the bottom of
the spectrum pane. In Waterfall-only view they are always drawn.

## FM tuning meter

**View › Spectrum › FM Tuning Meter** shows a small −5…+5 kHz meter at the
top right of the panadapter in FM and NFM. The needle is the carrier's
offset from the dial, read from the FM detector; the green zone in the
middle (within 300 Hz) reads "on tune". A needle to the right means the
carrier is above the dial: tune up.

- It reads "no carrier" on noise and on signals too weak to quiet the
  detector.
- It does not appear in WFM or in any other mode.

## Health warnings on the panadapter

**View › Spectrum › Health Warnings on the Panadapter** draws short text at
the top of the plot only while something is wrong:

- `ADC OVERLOAD` while the radio reports it (the same lamp as the header).
- `SEQ ERRORS n in 5 s` while packets from the radio are being lost. It
  clears five seconds after the last one; the status bar keeps the running
  total.
- `HIGH SWR n.n` when the SWR the header already shows while transmitting
  is 2.5 or more. This is a readout only; SWR protection is unchanged.

## Tuning conventions

All three are in **View › Tuning Conventions** and are off by default.

**Wide Modifier Steps.** Normally Shift divides the tuning step by five and
Option multiplies it by ten, for the arrow keys and the wheel. With this on:

| Keys held | Step |
| --- | --- |
| Shift | × 0.1 |
| none | × 1 |
| Option | × 10 |
| Shift + Option | × 100 |
| Control + Option | × 1000 |

The step never goes below 1 Hz. Control on its own is left alone because
macOS uses Control with the arrow keys to switch Spaces. If **Require Option
to Scroll Tune** is on, Option is already spent on allowing the scroll and
the wheel keeps only the Shift step.

**⌘-Drag Tunes by Pointer Height.** Normally a Command-drag puts the dial
under the pointer. With this on, a Command-drag moves the dial by how far
you drag, and how fast depends on where the pointer is: at the top of the
spectrum pane the VFO line keeps up with the pointer; down at the frequency
ruler (and anywhere over the waterfall) the same movement tunes twenty times
more slowly. Start high to get close, slide down to finish. Shift and Option
scale it as well. A plain drag still pans the display and dragging the VFO
line still moves it directly.

**Flick to Coast.** With tuning by pointer height on, releasing the mouse
while still moving lets the dial carry on and slow to a stop over two or
three seconds, covering at most a little more than one screen width. Any
click, key or scroll stops it at once; the click that stops it
does not also tune. A drag that pauses before the release does not coast.
Wheel and trackpad momentum are still ignored, as before.

**Zoom Anchor Marker** (View › Spectrum): a small cyan triangle on the
frequency ruler at the point zoom holds still — the VFO while it is on
screen (filled), otherwise the centre of the display (outline).

## What has and has not been checked

The arithmetic behind every option has unit tests. The density spectrum's
GPU code is run offscreen in the tests: the accumulation texture is read
back and the cloud and the wide trace are rendered into a texture and
checked pixel by pixel. The FM meter is tested through the real receive
chain on generated carriers.

Nothing on this page has been looked at on screen or used with a radio yet.
In particular the density cloud's colours and brightness, the look of the
wider trace, and the feel of tuning by pointer height and of the coast were
chosen from the numbers, not by eye or by hand, and may need adjusting.
