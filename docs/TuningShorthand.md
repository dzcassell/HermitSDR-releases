# Tuning shorthand, filter drags, channel clicks and station labels

Six small receive-side additions from the interface survey (#495). None of
them changes transmit behaviour.

## Typing a frequency and a filter together

The frequency entry (double-click the dial, the **MHz** label, or
**Radio › Set Frequency…**) accepts a filter after a slash.

| You type | What happens |
| --- | --- |
| `7.074` | Tunes to 7.074 MHz, as before. |
| `7074/2.7k` | Tunes to 7.074 MHz and sets the filter 2.7 kHz wide. |
| `/7k` | Sets the filter 7 kHz wide. The dial does not move. |
| `/300,2.7k` | Sets both filter edges: 300 Hz and 2700 Hz from the carrier. |
| `/` | Restores the mode's default filter width with no shift. |

Rules:

- A bare frequency is megahertz. A bare number above 3000 is read as
  kilohertz, so `7074` means 7.074 MHz. While a transverter profile is
  active this rule is off, because a microwave dial really does read
  above 3000 MHz.
- A frequency may carry a unit: `7074k`, `7.074M`, `7074000Hz`, `1.2G`.
- Filter numbers are hertz; add `k` for kilohertz. Use a full stop for
  decimals after the slash, because the comma separates the two edges.
- Edges are measured from the carrier. In LSB and DATA-L two positive
  edges are placed below the carrier, so `/300,2.7k` gives the same voice
  passband in either sideband. Negative edges (`/-2.9k,-500`) are taken as
  typed.
- Widths, edges and shifts are held to the limits and steps of the current
  mode, the same ones the filter sliders use.
- If the frequency is refused (out of range for the radio, for example),
  the filter is left alone too.

## Dragging the filter edges

The yellow handles at the filter edges on the spectrum now depend on the
mode and on the keys held.

| Mode | Plain drag | Option-drag | Shift-drag |
| --- | --- | --- | --- |
| AM, SAM, DSB, FM, NFM | Both edges move about the centre | Only the grabbed edge moves | The passband slides, width unchanged |
| USB, LSB, CW, DATA-U, DATA-L | Only the grabbed edge moves | Same | The passband slides, width unchanged |

A slide changes the filter shift; the dial and the carrier stay where they
are. You can press or release a key in the middle of a drag.

This changes the plain drag in AM, SAM, DSB, FM and NFM: before, it moved
one edge and left the other in place. Hold Option for that.

## Shift-click lands on a broadcast channel

A Shift-click on the spectrum or waterfall tunes to the nearest channel
instead of the exact spot clicked:

- long wave (148.5–283.5 kHz): 9 kHz channels
- medium wave: 10 kHz or 9 kHz channels, following the channel plan chosen
  in **MW Stations** (10 kHz for the Americas, 9 kHz elsewhere)
- the shortwave broadcast bands: 5 kHz channels
- everywhere else: the nearest whole kilohertz

A plain click is unchanged. The dial lock holds a Shift-click like any
other click.

## Station name at the VFO line

Switch on **Station name at the VFO line** in the tune-step menu. A small
label then follows VFO A on the spectrum and names the broadcaster
catalogued on the dial, with `+2` when two more are listed on the same
channel. Hover it for the list. The arrows on either side hop to the
previous and next catalogued channel and select AM (SAM is kept if it is
already selected).

The names come from the two lists HermitSDR already keeps: the shortwave
schedule (stations on the air this minute) and the **MW Stations**
catalogue. On medium-wave channels the catalogue is used, nearest to your
grid first. Utility stations are included when **Shortwave Schedules** is
set to label them. The dial counts as on a channel within 500 Hz.

The setting is off by default. While it is on, the shortwave schedule is
loaded and may make its usual weekly refresh. The medium-wave catalogue is
only fetched if you have asked for that in **MW Stations**; without it,
medium-wave names come from the shortwave schedule's own listings.

## Spot labels: age and worked

DX cluster labels on the waterfall end in a mark when the call is in your
log:

- `✓` worked on this band
- `◦` worked, but only on other bands

Switch on **Colour waterfall labels by spot age** in the DX Cluster window
to colour each label by how old the spot is: yellow under 2 minutes,
orange up to 5, magenta up to 10 and violet after that. With the setting
off, labels stay magenta and fade, as before. The hover tip states the age
step and the worked status in words.

## Frequency turns red on ADC overload

Switch on **Frequency turns red on ADC overload** in the tune-step menu.
The dial digits then turn red for as long as the radio reports an ADC
overload, alongside the header's ADC OVF lamp. Off by default.

## Not verified

These were checked with unit tests and a compile of the app. They have not
been tried on screen, with a pointer, or with a radio connected.
