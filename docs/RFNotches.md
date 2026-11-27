# RF notches (tracking notch filters)

An RF notch removes a steady interfering carrier — a switching-supply
birdie, an Ethernet spur, a broadcast carrier inside a 40 m SSB channel — and
**stays on that frequency**. Tune, change mode, turn on RIT or change the CW
pitch and the notch moves in the audio so it still sits on the same RF
frequency. When the carrier is outside the receive passband the notch does
nothing and costs nothing.

Receive only. Nothing here touches the transmitter.

## Placing and editing

- **Place:** right-click the carrier on the panadapter or the waterfall. A
  yellow bar appears on that frequency. New notches are 100 Hz wide, Normal
  depth, and last for the session.
- **Menu:** right-click the bar (anywhere along it), or its handle near the
  top of the panadapter:
  - **Depth** — Normal (at least 30 dB at the notch centre), Deep (50 dB),
    Very deep (70 dB).
  - **Width** — from "Narrowest the filter allows" up to 6 kHz.
  - **Remember for this radio** — the bar turns green and the notch is saved
    with this radio's settings. It is back the next time you connect this
    radio, and does not appear on your other radios.
  - **Delete**, and **Delete All in View** (every RF notch whose centre is on
    screen, remembered ones included).
  - **RF Notches On** — the global switch.
- **Move:** drag the handle (the small tab near the top of the bar).
- **Width by dragging:** when the bar is wide enough on screen (zoom in),
  drag one of the dark grips at the handle's edges.

Bars are dimmed while a notch is outside the passband, or while the global
switch is off.

The DSP popover (the **DSP** button) has the same global switch — "RF notches
(stay on their frequency)" — with a count of notches, how many are in the
passband right now, a **Clear session** button, and the decoder option below.

## What to expect

- **Notches of 100 Hz and wider** are drawn into the receiver's channel
  filter, which resolves about 100 Hz: the narrowest of these is about
  130 Hz wide at Normal depth, 160 Hz at Deep and 190 Hz at Very deep. With
  AM, SAM or DSB filters wider than 11 kHz the receiver runs at twice the
  rate and those figures double.
- **Notches narrower than 100 Hz** (10, 25 and 50 Hz in the Width menu) get
  a filter stage of their own. The whole width you ask for is taken down by
  the stated depth, and the −3 dB points are 1.7 times that width apart at
  Normal, 2.9 times at Deep and 2.4 times at Very deep: a 10 Hz Normal
  notch is 17 Hz wide at −3 dB, and a signal 30 Hz away is untouched. A
  narrow notch is slow by nature. It needs time to take a carrier out
  after the carrier appears or after you move the dial: about 0.2 s for
  10 Hz at Normal and Deep, 0.5 s at Very deep, and under 0.1 s for 50 Hz.
  While you tune across a notched carrier you hear it briefly at each
  step. Use it on a steady carrier beside something you want to keep;
  use a wider notch for a carrier that drifts. Each narrow notch costs a
  little processor time (eight at once measured 4.6 % of one core in an
  unoptimised build). Tested on generated carriers only; not yet heard.
- **Depth is measured at the notch centre.** A carrier that drifts wants a
  wider notch, not a deeper one.
- **AM and SAM.** A notch can sit on either side of the station's carrier and
  removes the whistle the interfering carrier makes. A notch placed on the
  station's own carrier removes the carrier — the audio distorts (AM) or the
  lock drops (SAM). Move it off.
- **FM, NFM and WFM** take no notches (the audio is in the phase, not the
  spectrum). The bars stay on screen, dimmed.
- **Limit.** At most 32 notches are applied inside one passband. A 33rd is
  refused with a message; if tuning brings more than 32 into the passband,
  the 32 nearest its centre are applied and the DSP popover says so. The
  list holds 256 notches in all.
- **Decoders.** FT8/FT4, CW, RTTY and the other decoders — and the passband
  mini-waterfall — are fed from *ahead* of the RF notches in USB, LSB, CW,
  DATA-U/L and DSB, so a notch you place for your ears never costs a decode.
  "Decoders hear RF notches" in the DSP popover makes them hear exactly what
  the speaker hears. In AM and SAM the decoder feed is always after the
  notches.
- **SUB and receive windows.** The SUB receiver (VFO B) and every running
  independent receiver window apply the same list in their own passband: a
  notch on 7.151 MHz is cut in whichever receiver is listening there. The
  bars are drawn on the main panadapter only. Not yet heard on a radio.
- **On the passband mini-waterfall** the RF notches in force are drawn as
  cyan bands at the audio frequencies they take out (the older audio
  notches stay purple lines). Compiled and unit-tested; not yet seen on
  screen.
- **Session notches** are forgotten when HermitSDR quits. Remembered notches
  are stored per physical radio (not per antenna port: the radio's settings
  do not distinguish ports). A radio with no stable hardware identity (a
  manually entered address that was never discovered) cannot keep them.

## The older audio notches

Right-clicking a tone on the **audio mini-waterfall** still places the
original kind of notch: fixed about 200 Hz wide, tied to the audio pitch
rather than the RF frequency, cleared by a mode change or a reconnect.
Right-clicking one of those (purple marker) on the panadapter removes it, as
before. The automatic notch (DSP popover, "Auto-notch") is unchanged.

## Remote control

- **Control API** (revision 6, [ControlAPI.md](ControlAPI.md)): `setRFNotches`
  is the master switch; `addRFNotch` adds a session notch at an RF frequency
  (optionally with a width and depth); `removeRFNotch` deletes the notch at a
  frequency; `clearRFNotches` deletes the session notches. The state keys
  `rfNotchesEnabled`, `rfNotchCount`, `rfNotchesInPassband` and `rfNotchList`
  report the switch, the counts and the centres.
- **Stream Deck and MIDI** ([StreamDeck.md](StreamDeck.md),
  [MIDIController.md](MIDIController.md)): **RF notches** is a toggle for the
  master switch (the key lights while it is on and shows the number of
  notches); **Clear session RF notches** deletes the session notches and
  leaves the remembered ones. A key cannot add or remove a single notch: it
  has no frequency to point at. Do that on the panadapter or through the
  Control API.

## Not included yet

- Notch bars in the SUB panadapter and in the independent receiver windows
  (the notches are applied there; only the drawing is missing).
- A Stream Deck key or MIDI pad that adds or removes one notch (it would need
  a rule for which frequency it means).
- Width, depth and "remember" of an existing notch cannot be changed through
  the Control API.
