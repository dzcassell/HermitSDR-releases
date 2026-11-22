# Time Signal (#421)

The standard time stations send the date and time as a slow code under
their ticks. The Time Signal window decodes that code and compares the
decoded second with this Mac's clock, so a station with no network still
has an independent time reference.

It only compares. Nothing in this feature sets, steps or steers the Mac's
clock.

**Not yet decoded on the air.** Every station below was built from its
operating agency's published format and tested against signals generated
from those formats. The first on-air trial (WWV, 15 MHz, 2026-11-22, a
good signal with both the WWV and WWVH ticks present) decoded nothing in
three minutes: about one second in eight read wrongly, and a WWV minute
was then accepted only if all 60 seconds were right. The decoder now
combines minutes (see *Combining minutes* below); that change has been
tested on generated signals only and has not yet been tried on the air.
CHU is off the air at the development station, so CHU has only ever been
tested on generated signals. Treat a first real decode as a test of the
decoder, not of your clock, and please report what you see.

## Where

- **Decode ▸ Time Signal** opens the window (Feature catalog `time-signal`,
  Decode category). Receive only: nothing here can arm or key.
- The decoder runs while **Enable** is on (the dot is green). Pressing a
  frequency button tunes the radio and switches it on.
- Its sessions appear in **Decoder Activity** as `TIME`, with a bookmark
  for each confirmed minute.
- **Ask The Crab** can read the window back ("what time does WWV say",
  "is my Mac clock right"): its `time_signal` tool reports the decoded
  time, whether it is confirmed, how many minutes it was read from, the
  signal figures and the clock comparison. It only reports; it cannot
  start the decoder or tune.

## Stations

| Station | Agency | Frequencies | Preset tunes | What is read |
| --- | --- | --- | --- | --- |
| WWV / WWVH | NIST, USA | 2.5, 5, 10, 15, 20, 25 MHz | AM on the carrier | 100 Hz sub-carrier time code; the 5 ms seconds tick (1000 Hz = WWV, 1200 Hz = WWVH) for which station it is and for timing |
| CHU | NRC, Canada | 3330, 7850, 14670 kHz | USB on the carrier | The 300 Bd bursts in seconds 31–39 |
| DCF77 | PTB, Germany | 77.5 kHz | USB, dial 1 kHz below | 0.1 s / 0.2 s carrier reductions |
| WWVB | NIST, USA | 60 kHz | USB, dial 1 kHz below | 0.2 / 0.5 / 0.8 s power drops (the amplitude code, not the phase code) |
| MSF | NPL, United Kingdom | 60 kHz | USB, dial 1 kHz below | On-off keyed A and B bits |
| JJY | NICT, Japan | 40 and 60 kHz | USB, dial 1 kHz below | 0.8 / 0.5 / 0.2 s pulses |

BPC (China) and RBU (Russia) are not included.

The four LF stations need a radio and antenna that receive 40–77.5 kHz.
For them the carrier is turned into an audio tone: the preset puts the USB
dial **Tone** hertz (1000 by default) below the carrier, and the decoder
follows the carrier within ±150 Hz of that tone. The window shows how far
off it found it (`carrier +7 Hz`).

WWV and WWVH must be received in **AM** (or SAM): the time code is a
100 Hz tone in the detected audio. In USB or LSB the receive filter
removes it.

### Best frequency now

For WWV / WWVH and CHU one frequency button carries a ★. With the header's
MUF reading available and your grid set, it is the highest frequency under
85 % of an estimate of the path's maximum usable frequency. Without a MUF
reading it is a plain day / night rule from your grid (10–15 MHz by day,
5 MHz by night). For JJY it is the nearer of the two transmitters. It is a
hint: if the suggested frequency is empty, try the next one down.

## Reading the window

- **Date and time** — the UTC minute the last frame was sent in, with
  **CONFIRMED** or **UNCONFIRMED** beside it and the station that sent it.
  For WWV / WWVH and WWVB, "from 6 minutes" (or "from this minute alone")
  says how much signal the time was read from.
  DCF77 and MSF broadcast local time for the *following* minute; the window
  converts both to UTC and to the minute the frame was sent in. JJY sends
  Japan Standard Time; it is shown as UTC too.
- **DUT1** — UT1 minus UTC, in tenths of a second, where the station sends
  it (WWV, WWVB, MSF, CHU). **TAI−UTC** on CHU.
- **LEAP SECOND** — the station is announcing a leap second. **DST** and
  **DST CHANGE** — the station's daylight / summer time flags.
- **The strip of 60 cells** — the last minute, second by second, newest on
  the right: green 0, yellow 1, red marker, blue "no pulse", grey
  unreadable. A clean minute has no grey. The legend under the strips
  names the colours.
- **The thin strip under it** (WWV / WWVH and WWVB) — the minute as the
  held minutes decide it, second 0 on the left, in the same colours. Grey
  there is a second the minutes do not yet agree on. Its caption says how
  many minutes are held and how many seconds are still undecided; a time
  is given when none is.
- **depth / quality** — how deep the code's amplitude steps are, and how
  cleanly the last second or minute was read.
- **decoded · refused** — minutes that gave a time, and minutes that ended
  without one (with the reason: parity error, value out of range, position
  markers out of place, "not enough agreeing minutes yet", …). While WWV
  or WWVB minutes are still being collected every minute counts as
  refused; that is expected for the first few minutes on a fading signal.

### Confirmed and unconfirmed

A minute decodes on its own only if every one of its 60 seconds was read
with margin and the frame passed every check its format has: position
markers in the right seconds, fixed bits, digit ranges, a real calendar
date, parity where the station sends it (DCF77, MSF, JJY), the weekday
agreeing with the date (DCF77, MSF, JJY), the leap-year bit agreeing with
the year (WWVB).

A time becomes **confirmed** when an earlier minute gave the time exactly
that many minutes earlier (the minute before, or up to ten minutes before
if minutes in between gave nothing). For CHU, two bursts in the same
minute must agree. A time is never confirmed the first time it appears.

Rely on confirmed times only. An unconfirmed time is shown for
information: it is not compared with the Mac's clock and nothing else in
the app uses it.

DCF77, MSF and JJY are read one minute at a time, so for them a noisy or
faded minute shows nothing new — the previous time stays, ageing.

### Combining minutes (WWV / WWVH and WWVB)

WWV / WWVH and WWVB send no parity or check bits, and on short wave a
minute with all 60 seconds readable is rare: fading, the second station
on the same frequency and the voice announcements each cost a few
seconds. So for these two the decoder also keeps the last fifteen minutes
of seconds and combines them:

- It finds where the minute starts from the position markers, the missing
  pulse at second 0 (WWV) and the reserved zeros of all the held minutes
  together.
- Successive minutes carry the same frame with one known change: the
  minute counts up, and the hour, day and year roll over with it. Each
  possible minute, hour, day and year is scored against what every held
  minute would have carried if the newest minute had that value, and the
  best must be clearly ahead.
- Every second of the result is then decided by a vote of the minutes
  that read it: the readings for the winning symbol must outnumber the
  readings against it by two (a plain majority is enough for a reserved
  zero). An unreadable second is an abstention, so it does not sink a
  minute when the same second read cleanly in the minutes around it.
- The combined minute must pass every check a single minute must pass,
  and the newest minute must itself have been at least half readable and
  agree with the result. A time is never carried forward through a
  minute that was not heard.

Such a time is **confirmed** only if, in addition, the minute before gave
the time one minute earlier and every second of the time was decided by a
margin of four. The window says how many minutes each time came from.

A clean-looking minute that the held minutes outvote is not shown as it
stands: the combined time is shown instead, or nothing. This catches the
single wrong bit that the format itself cannot (it used to appear as an
unconfirmed wrong time). The first minute after switching on has nothing
to be compared with, so one wrong bit in it can still appear as an
unconfirmed time; it cannot be confirmed.

What to expect, from generated signals (`TimeSignalAccumulationTests`):

| Seconds damaged | Minutes that give a confirmed time, once running | First time shown | First confirmed |
| --- | --- | --- | --- |
| none | all | 1 minute | 2 minutes |
| 10 % | 98 % (WWV), 96 % (WWVB) | 4 to 5 minutes | 7 to 9 minutes |
| 15 % | 93 % (WWV), 88 % (WWVB) | 6 minutes | 9 minutes |
| 20 % | 84 % | 8 minutes | 11 to 12 minutes |

"Damaged" means a mix of unreadable seconds, a 0 read as a 1 or the
reverse, markers cut short, random symbols, and in a quarter of the
minutes a burst over seconds 45 to 59 (where the voice announcements
are). Times are medians over 80 half-hour runs of WWV and 20 of WWVB at
random dates; "once running" is the last twenty minutes of each half
hour. In those runs, and in runs across the top of the hour, midnight,
the end of a 365-day and a 366-day year, no combined time was wrong.
Eight days of randomly classified seconds, two days of bare seconds
pulses and marker lattices, two days each of another station's code on
the wrong decoder, and half an hour of noise as audio gave no time at
all, confirmed or not. A test
that feeds audio (WWV with WWVH on the same channel at half its strength,
damaged seconds and noise, across an hour change) showed its first time
after six minutes and confirmed from the eighth.

Limits of the method:

- The DUT1, daylight-time and leap-second bits are decided by the same
  vote. After they change at 0000 UTC the new day's minutes decide as soon
  as two agree; for a minute or two the time may be withheld.
- A leap second moves the minute boundary by a second. The combiner then
  needs a clean minute, or several minutes, to find the minute again.
- If the audio stream loses samples the seconds lattice moves and the held
  minutes are discarded.
- The damage model in these tests is a guess at what short wave does. The
  rates above are not a prediction for any real path.

In minutes 15 and 45 JJY replaces the year and weekday with its Morse call
sign; those minutes decode only after an earlier confirmed minute supplied
the year.

## The Mac clock comparison

    Mac clock is +0.12 s (±0.03)

Positive means the Mac is fast. The figure is the median of the last five
confirmed minutes (ten minutes at most).

How it is measured: the decoder notes the Mac's clock as each block of
audio arrives, finds the on-time point of the minute in that audio, and
subtracts the decoded UTC. What is left still contains two delays, which
are then taken off:

1. **The receive chain.** From the code: the decimating filters down to
   12 kHz (1.9–2.6 ms depending on sample rate) plus the 513-tap channel
   filter (21.3 ms; the wide AM path is 13.3 ms instead), plus a 3 ms
   allowance for the radio's own filters and the network, which the app
   cannot see. About 27 ms in total at 384 kHz.
2. **The path from the transmitter.** With your station grid set in
   Settings, the distance to the transmitter gives it: ground wave for LF,
   and for HF the fewest ionospheric hops (300 km virtual height, at most
   3500 km a hop) — 9 ms for a 2600 km path, for example.

The ± figure includes:

- how precisely the second was found: 0.5 ms from the WWV / WWVH tick, 1 ms
  from a CHU burst, 5 ms from an LF carrier edge, 8 ms when the WWV tick is
  too weak and the sub-carrier edge is used instead;
- 4 ms for the receive-chain figure (the radio / network allowance is an
  estimate);
- the path estimate's own doubt (1–2 ms; on HF, the difference to one more
  hop);
- the scatter between the minutes.

It does **not** include, and you should keep in mind:

- **An unknown path.** With no grid set, or when WWV and WWVH are both
  audible and cannot be told apart, the path delay is *not* removed. The
  window says so in orange, the Mac may be slower than shown by up to the
  path delay, and the ± figure grows by the largest plausible delay (70 ms
  on HF, 9 ms on LF) rather than hiding it.
- **Radios other than openHPSDR.** The chain figure is read from the
  filter designs, not measured against a reference. Front ends with their
  own resampling (NetSDR, SDRplay, FlexRadio) add delay that is not
  modelled.
- **The stations' own accuracy** and anything unusual in the ionosphere
  (long path, multi-mode propagation).
- **Leap seconds.** A minute with a leap second in it gives no comparison.

On generated signals with the clock deliberately set 0.5 s fast, 27 ms of
chain delay and 3 ms of delivery jitter, all six stations measured +0.500 s
within 1 ms. That checks the arithmetic, not a radio.

The comparison needs a connected radio. File replay and the RF time
machine decode the time but do not compare clocks.

### Shown only

The figure is a readout. It is not fed to FT8 / FT4 slot timing or to
anything else in the app, and the Mac's clock is not changed. FT8 and FT4
keep their own estimate (the CLOCK line in the FT8 panel). To correct the
Mac itself, use System Settings › General › Date & Time.

## Recordings

**Decode ▸ Decode a Recording…** lists **Time Signal** with a station
picker. WWV / WWVH are demodulated in AM and CHU in USB with the dial on
the carrier; for the LF stations set the dial 1 kHz below the carrier.
Each decoded minute prints as one line, ending "(6 minutes combined)"
when it was read from more than one. A recording's start stamp is not a
clock, so no comparison is made.

Replaying an IQ recording in the main window feeds the Time Signal window
like live audio, again without the clock comparison.

## Limits

- Not yet decoded from a real signal; CHU cannot be tried here at all.
- Voice announcements and the 440 / 500 / 600 Hz tones on WWV / WWVH share
  the audio with the 100 Hz code. Seconds under heavy speech may be
  unreadable; combining minutes is meant to cover that, but if the same
  seconds are lost in every minute they cannot be recovered.
- Combining applies to WWV / WWVH and WWVB only. DCF77, MSF and JJY still
  need a whole clean minute.
- How far WWV's 100 Hz sub-carrier drops between pulses is not stated in
  the NIST text that was read; the decoder accepts anything from absent to
  about 70 % of the pulse level.
- WWV has no parity and its reserved seconds must read 0 for a frame to be
  accepted. If NIST starts using a reserved second, every WWV minute will
  be refused until the decoder is updated.
- Two-digit years are read as 2000–2099.
- WWVB's phase-modulated code and DCF77's phase noise code are not decoded.
- CHU sends its year only in second 31. If that burst is missed the year
  is taken from the Mac's calendar and the window says "year assumed".

## Sources

Frame formats were taken from the operating agencies' own publications and
the decoders were written for HermitSDR from them:

- **WWV / WWVH, WWVB** — NIST Special Publication 432, *NIST Time and
  Frequency Services* (Table 3.13 and Figure 3.10 for WWV / WWVH; chapter 2
  for WWVB), and the NIST "WWV and WWVH Digital Time Code and Broadcast
  Format" and "WWVB Time Code Format" pages.
- **DCF77** — PTB, "DCF77 time code" and "DCF77 amplitude modulation".
- **MSF** — NPL Time & Frequency Services, "MSF 60 kHz Time and Date Code"
  (March 2019).
- **JJY** — NICT Japan Standard Time Group, "Time code" diagrams and the
  standard-frequency transmission specification.
- **CHU** — NRC, "CHU broadcast codes". The NRC site refused automated
  reading while this was written, so the CHU layout (tones, 300 Bd, ten
  characters ending 500 ms into the second, the two frame kinds) was
  written from memory of that page and has not been re-read against it.
  A second attempt on 2026-11-17 was refused the same way (HTTP 403 from
  both `nrc.canada.ca` and `cnrc.canada.ca`), so the layout is unchanged
  and still unchecked against NRC's text. A search engine's summary of the
  page agrees with what is implemented as far as it goes — Bell 103 at
  300 Bd in seconds 31–39, one start, eight data and two stop bits, five
  data bytes then five redundancy bytes, digits nibble-reversed, and for
  second 31 the fields |DUT1| in tenths, four-digit year, TAI−UTC and the
  daylight-time pattern number in that order — but a summary is not the
  page: the meaning of each bit of the leading digit and the 500 ms end of
  the last stop bit remain from memory. A third attempt on 2026-11-22 got
  HTTP 403 from both addresses again. A search summary that day gave the
  leading digit's bits as 1 = DUT1 negative, 2 = a second will be added,
  4 = a second will be subtracted, 8 = even parity of the digit, and the
  FSK as present from 10 ms to 510 ms after the second — both as
  implemented — but it took them from descriptions of other receivers,
  not from NRC's page, so the note stands.
