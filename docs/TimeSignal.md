# Time Signal (#421)

The standard time stations send the date and time as a slow code under
their ticks. The Time Signal window decodes that code and compares the
decoded second with this Mac's clock, so a station with no network still
has an independent time reference.

It only compares. Nothing in this feature sets, steps or steers the Mac's
clock.

**Not yet checked on the air.** Every station below was built from its
operating agency's published format and tested against signals generated
from those formats. No real off-air recording of any of them has been
decoded yet, and CHU is off the air at the development station, so CHU
has only ever been tested on generated signals. Treat a first real decode
as a test of the decoder, not of your clock, and please report what you
see.

## Where

- **Decode ▸ Time Signal** opens the window (Feature catalog `time-signal`,
  Decode category). Receive only: nothing here can arm or key.
- The decoder runs while **Enable** is on (the dot is green). Pressing a
  frequency button tunes the radio and switches it on.
- Its sessions appear in **Decoder Activity** as `TIME`, with a bookmark
  for each confirmed minute.

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
  DCF77 and MSF broadcast local time for the *following* minute; the window
  converts both to UTC and to the minute the frame was sent in. JJY sends
  Japan Standard Time; it is shown as UTC too.
- **DUT1** — UT1 minus UTC, in tenths of a second, where the station sends
  it (WWV, WWVB, MSF, CHU). **TAI−UTC** on CHU.
- **LEAP SECOND** — the station is announcing a leap second. **DST** and
  **DST CHANGE** — the station's daylight / summer time flags.
- **The strip of 60 cells** — the last minute, second by second, newest on
  the right: green 0, yellow 1, red marker, blue "no pulse", grey
  unreadable. A clean minute has no grey.
- **depth / quality** — how deep the code's amplitude steps are, and how
  cleanly the last second or minute was read.
- **decoded · refused** — minutes that passed every check, and minutes that
  were lined up but failed one (with the reason: parity error, value out of
  range, position markers out of place, …).

### Confirmed and unconfirmed

A minute is shown only if every one of its 60 seconds was read with margin
and the frame passed every check its format has: position markers in the
right seconds, fixed bits, digit ranges, a real calendar date, parity where
the station sends it (DCF77, MSF, JJY), the weekday agreeing with the date
(DCF77, MSF, JJY), the leap-year bit agreeing with the year (WWVB).

A minute becomes **confirmed** when the next minute decodes too and is
exactly one minute later (up to ten minutes later if minutes in between
were lost). For CHU, two bursts in the same minute must agree.

A noisy or faded minute therefore shows nothing new — the previous time
stays, ageing. WWV / WWVH and WWVB carry no parity, so a single wrong bit
in a single minute can only be caught by the next minute: such a minute can
appear as **unconfirmed**, never as confirmed. Rely on confirmed times
only. The clock comparison uses confirmed minutes only.

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
Each decoded minute prints as one line. A recording's start stamp is not a
clock, so no comparison is made.

Replaying an IQ recording in the main window feeds the Time Signal window
like live audio, again without the clock comparison.

## Limits

- Not yet decoded from a real signal; CHU cannot be tried here at all.
- Voice announcements and the 440 / 500 / 600 Hz tones on WWV / WWVH share
  the audio with the 100 Hz code. Minutes with heavy speech may be refused.
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
  the last stop bit remain from memory.
