# PSK signal browser: every PSK31 / PSK63 / PSK125 signal at once

The PSK decoder in the Digital Modes window copies one signal — the one at
its audio centre. The **PSK signal browser** copies all of them: every PSK31,
PSK63 and PSK125 signal inside the receive filter gets its own line of text, with
its frequency, strength and callsign, and you click the one you want.

It only listens. Nothing here transmits, keys the radio or moves the VFO.

## Turning it on

1. Tune to a PSK segment in **USB** or **DATA-U** (for example 14.070 MHz or
   7.040 MHz) with a filter wide enough to take in the activity — 2.4 to
   3 kHz.
2. Open **Decode › Digital Modes** and choose **PSK / QPSK**.
3. Switch **Browser** on (beside the variant picker).

The switch is remembered. The browser is separate from the **Decode**
switch: the single decoder above and the browser below run independently.

## What each line shows

| Column | Meaning |
| --- | --- |
| dot | green while the signal is being copied, grey once it has stopped |
| audio Hz | where the signal sits in the passband |
| kHz | its frequency on the dial (through a transverter if one is set) |
| mode | PSK31, PSK63 or PSK125, worked out from the signal itself |
| dB | the signal over the noise, measured in the signal's own bandwidth |
| Q | decision quality, the same figure the single decoder shows |
| IMD | the station's intermodulation, when it can be read (see below) |
| age | `now`, or how long ago the signal was last copied |
| callsign | the station on that frequency, once it has identified |
| text | the newest characters; callsigns are coloured and **CQ** is green |

Lines are in frequency order. A line stays for two minutes after its signal
stops, so you can still read what was sent; if the station comes back on the
same frequency it carries on in the same line.

**Click a line** to put the single PSK decoder on that signal: the mode is
set to PSK31, PSK63 or PSK125, the audio centre moves there and Decode turns on.
The VFO stays where it is.

The summary above the lines shows how many signals are listed, how many of
the 24 demodulators are in use, and how much of one processor core the
browser is taking.

## Callsigns

A callsign is shown — and passed on to the features below — only when the
station sent it the way PSK operators identify: a callsign-shaped word that
followed `DE` and has appeared at least twice on that line within two
minutes (`CQ CQ DE K1ABC K1ABC`). The station being called, a callsign-like
word in the chatter (`ANT G5RV`) and a single garbled mention are coloured
in the text but are not treated as the station.

A locator is taken only when it directly follows `LOC`, `LOCATOR`, `GRID` or
`QRA` (`LOC: JN58TD`).

## Where the callsigns go

- **Waterfall labels.** Each identified callsign is labelled at its frequency
  on the main waterfall (pink, below the CW skimmer's labels; `CQ` in front
  when the station is calling). Click a label to put the decoder there.
  **Waterfall labels** in the panel turns them off. At a wide span the
  labels of one passband sit close together — zoom in.
- **Stations Heard map.** A station that sent a locator is pinned under the
  **PSK** layer.
- **Needed DX.** Identified stations from the last half hour are ranked
  against your log like FT8 decodes, as "Heard here", mode PSK.
- **PSK Reporter.** If — and only if — **Settings › Station › PSK Reporter**
  uploads are already on and your callsign and grid are set, identified
  callsigns are reported with mode `PSK31` or `PSK63` and the signal's
  frequency. The browser adds no switch of its own and changes none of the
  upload rules: one report per callsign per five-minute upload, as for FT8.

Signals decoded from a recording or from the time machine are listed but
never put on the map, ranked or uploaded.

## IMD

When a station idles, a PSK signal is two clean tones; an overdriven
transmitter adds a second pair further out. The IMD column is how far down
that second pair is (−30 is clean, −20 is poor). It is read only while the
station is idle, only when the signal is at least 15 dB over the noise, and
it cannot read better than the noise allows: on a weak signal the figure
tells you about the noise, not the transmitter.

## Limits

- **Up to 24 signals at a time.** When more are present, the strongest that
  arrived first keep their demodulators and the rest are counted in the
  summary as "over the limit" until one frees up.
- **PSK31, PSK63 and PSK125.** The QPSK modes are not browsed; use the
  single decoder for those. (The browser finds a carrier by squaring the
  signal, which removes two-phase modulation and not four-phase.) A PSK125
  signal is 250 Hz wide: a PSK31 or PSK63 signal within 150 Hz of its
  carrier overlaps it and is not listed separately.
- **The receive filter is the search window.** Signals outside the filter,
  or within 40 Hz of its edges, are not looked for.
- **Tuning with the browser on.** A small dial move — a 1 Hz or 10 Hz step,
  a RIT change, anything smaller than the passband — keeps the list: every
  line moves along the audio axis by the same amount, keeps its text and
  callsign and goes on printing. A line is dropped only when the move takes
  its signal out of the filter. A strong signal is back in lock within a
  second or two of a move of a few tens of hertz; a move while a station is
  sending can cost a character or two. New signals are looked for again
  about half a second after the dial stops. Changing the mode, or moving the
  dial by a passband or more (a band change, a click elsewhere on the
  waterfall), clears the list, because the lines would then be different
  stations.
- **Signal strength.** A signal needs to be roughly 10 dB over the noise in
  its own bandwidth to be picked up promptly; weaker ones appear later or
  not at all. A PSK31 signal 100 Hz from one 30 dB stronger is still copied.
- **End of an over.** For up to a second after a signal stops the line can
  gain a few random characters, exactly as the single decoder does. They are
  not callsign-shaped by any realistic chance, and a callsign needs `DE` and
  a repeat, so they do not create stations.
- **One passband.** This first version looks at the audio passband of the
  main receiver only. Skimming a whole 48–192 kHz span for PSK is not built.

## Asking, reading and replaying it

- **Ask The Crab** — "who is on PSK", "what does the PSK browser see". Its
  `psk_browser` tool reads the list back: how many signals, the eight
  strongest with frequency, mode, callsign, S/N and the last of their
  text, and the stations identified this session. It only reports; it
  cannot switch the browser on, tune or transmit.
- **Control API** — three read-only state keys from revision 5:
  `pskBrowser` (the switch), `pskBrowserSignals` (lines listed now) and
  `pskBrowserCalls` (the callsigns on them, strongest first, at most 12).
  There is no message that switches the browser or tunes to a line.
  See [ControlAPI.md](ControlAPI.md).
- **Live captions** — with decoder captions on for a YouTube stream, each
  station the browser identifies off the air adds one cue
  (`14070.512 kHz K1ABC FN42 CQ +18 dB`), under the same rate limit and
  30-second repeat filter as the other decoders. Replays add none.
- **Decode a Recording** — **Decode ▸ Decode a Recording…** lists **PSK
  Signal Browser**. It runs the browser over the file in USB (or LSB with
  the sideband option), prints a line for each callsign as it is confirmed
  (`08:00:21  14071.000 kHz  PSK31  K1ABC  CQ  S/N 37 dB`) and, at the end,
  what each signal still listed last sent. Nothing from a recording goes
  to the heard map or PSK Reporter.
- **Operator Manual** — the *Decode and operate digital modes* chapter
  describes the Browser switch.

## How it was tested

All figures below are from synthetic signals run through the browser faster
than real time (`Tests/DSPTests/PSKBrowserTests.swift`). It has **not** been
checked on the air or against a recording of real PSK activity.

- Eight simultaneous PSK31 signals inside 2 kHz, 30 dB apart in strength
  (the weakest 15 dB over the noise in its own bandwidth), at a realistic
  receive level (−70 to −100 dBFS) and again near full scale: eight lines,
  each with the right text and callsign. A ninth signal switched on mid-test
  had its line 0.9 s later.
- PSK125: a strong and a weak PSK125 station beside a PSK31 and a PSK63 one
  gave four lines, each with its own rate, carrier (within 3 Hz) and
  callsign, and no extra line on the wide signals; an idling PSK125 station
  gave one line on its carrier; a PSK125 signal about 10 dB over the noise
  in 125 Hz was found and identified.
- Ten minutes of noise: no line, no demodulator started, no callsign.
- Five minutes of noise bands 60, 130 and 260 Hz wide, 12 dB over the floor
  (which the detector does look at, about 1,100 times): every look rejected,
  no line.
- Carriers, a keyed carrier and an FSK signal: looked at and rejected, no
  line.
- A dial move in mid-over (30 Hz at once, and ten 1 Hz steps): the line
  kept its number, text and callsign, moved to the new offset and carried on
  printing clean text; a move that took one of two signals out of the filter
  dropped that line only. The splice in these fixtures is a generated
  frequency step, not a recording of a radio being tuned.
- The report for the crab, the Control API keys, the caption text and the
  Decode a Recording output are unit-tested on generated signals. The
  caption hook into a live stream and the Control API keys in the running
  app are compiled, not exercised.
- **Cost of 24 simultaneous signals: 1.07 to 1.16 s of processing for 60 s
  of audio — about 1.9 % of one processor core** (five runs, 1.78 to
  1.93 %), measured on a Mac mini (M4 Pro) in the unoptimised test build,
  while other builds were running. The released app is compiled with
  optimisation and has not been measured separately; the panel shows the
  live figure. With no PSK signal present the browser costs one small
  spectrum four times a second.
