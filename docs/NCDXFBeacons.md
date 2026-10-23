# NCDXF / IARU beacon tracker (#278)

The NCDXF/IARU International Beacon Project runs eighteen beacons that share
14.100, 18.110, 21.150, 24.930 and 28.200 MHz in a three-minute cycle: each
beacon transmits for ten seconds on 14.100 MHz, then steps to 18.110, 21.150,
24.930 and 28.200 MHz in the four following slots, and the next beacon in the
list opens on 14.100 ten seconds later. A transmission is the callsign at
22 WPM followed by four one-second dashes; the callsign and the first dash are
sent at 100 W, the remaining dashes at 10 W, 1 W and 100 mW. 4U1UN opens the
cycle on 14.100 at hh:00:00, hh:03:00, … UTC. HermitSDR models the published
schedule and locations table from https://www.ncdxf.org/beacon/ (read
2026-10-22) in `HermitSDR/Integration/Beacons/NCDXFBeaconSchedule.swift`:
callsign, country, location and Maidenhead grid for all eighteen beacons, and
the slot arithmetic that names the beacon on any band at any UTC instant.
Whether an individual beacon is on the air today is not modelled — the panel
and label show the published slot plan.

## Where

- **Log ▸ NCDXF Beacons** opens the panel (Feature catalog `ncdxf-beacons`,
  Log category). The schedule table lists the five frequencies with the beacon
  transmitting now (callsign, place, grid), the seconds left in its slot with
  a progress bar, the beacon up next and a **Listen** button that tunes VFO A
  to the frequency in CW (the dial lands on the carrier; the CW pitch puts it
  in the passband). Receive only — nothing here can arm or key.
- **Waterfall label**: whenever a beacon frequency is inside the visible span,
  a `NOW: <callsign> <seconds>s` tag sits over it on the panadapter, in the row
  between the FT8 and cluster labels. Clicking the tag tunes like Listen. The
  tag follows the display axis (the IF under a transverter) and hides within
  8 pt of either edge like the other labels.
- **Log S/N**: see below. Both switches live in the panel header and are
  Ask The Crab controls `beacons.labels` and `beacons.logSNR` (defaults keys
  `beaconLabelsOn`, `beaconSNRLoggingOn`; both on by default).

## S/N measurement

While Log S/N is on and the receiver is live (connected, not a file replay,
not a time-shifted view, not transmitting), the tracker rides the existing
10 Hz meter tick with the renderer's newest spectrum row — the same row the
panadapter's Auto range and peak labels read; the DSP thread does no extra
work and no new timer, lock or queue exists on the radio path. If one of the
five beacon frequencies lies inside the sampled span with 2.5 kHz to spare on
each side, every row of the current ten-second slot is read
(`BeaconSlotSampler`):

- **carrier** = the strongest bin within ±100 Hz of the published frequency;
- **floor** = the median of the bins 300 … 2500 Hz either side (at most 256
  bins sorted per row, so the cost is bounded whatever the sample rate);
- the slot's **S/N** = the peak carrier over the median floor, referred to a
  **500 Hz bandwidth** (`peak − floor − 10·log10(500 Hz / bin width)`) so
  sessions at different sample rates — different bin widths — compare. A
  carrier narrower than a bin keeps its level whatever the bin width; the
  noise per bin does not, which is what the correction removes. The number
  is a per-bin spectrum estimate under whatever spectrum averaging is
  selected, not an audio-passband S-meter reading.
- **steps heard** (0 … 4) is *inferred* from the peak S/N: the 10 W, 1 W and
  100 mW dashes are 10, 20 and 30 dB below the 100 W level, so a step counts
  while its expected level still clears the floor by 6 dB. The dashes are
  not timed individually (spectrum averaging would smear them), so treat
  the dots as "would have been audible", not as four separate detections.

A slot is kept only when at least ten rows spanning at least five seconds
were read; a slot during which the sampled span moved, the transmitter was
keyed, the view was time-shifted or the session ended is discarded rather
than recorded short. Demo Mode's fixed 96 kHz around 14.2 MHz contains no
beacon frequency, so Demo logs nothing (the panel countdown still runs).

Synthetic fixture (`Tests/DSPTests/NCDXFBeaconTests.swift`): a −80 dBFS
carrier on a −120 dBFS ±3 dB floor at 384 kHz / 8192 bins measures
+29.7 dB (500 Hz) with three steps inferred; the same carrier and per-bin
floor at 48 kHz, 384 kHz and 1536 kHz differ by exactly the bin-width ratio;
a carrier 50 Hz off is still read, one 1.5 kHz off is not; two −40 dBFS
signals inside the noise window move the median floor by under 1.5 dB.

## History

`BeaconHistory` keeps one ring per beacon and band (90 series): entries
older than 24 hours relative to the newest are dropped and a series never
exceeds 512 entries (one slot every three minutes is 480 a day). The panel's
**S/N history** section shows, per band, every beacon's slots heard, best
S/N, last measurement, the inferred steps of the last slot and a 24-hour
sparkline (bar height −10 … +40 dB, dim below +6 dB).

The history survives relaunch: it is written as JSON to
`~/Library/Application Support/HermitSDR/ncdxf-beacons.json` (the Dev build
uses its own namespace) by `BeaconHistoryFile`, encoded and written on a
utility queue 30 s after the last new slot and at quit, and read on the same
queue at launch (decoding re-applies the ring bounds, so an oversized or
hand-edited file is trimmed, and an unknown format version is ignored).
**Clear history** empties it. Nothing is uploaded.

## Band scout

`BeaconHistory.bandEvidence(now:windowSeconds:minimumSnrDb:)` is the narrow
read API: per band, how many distinct beacons were copied at or above +3 dB
in the last 30 minutes and the best of them. `BandScout.report(…)` (the
crab's "which band is open?" and its receive-only active sweep) appends it
as *"NCDXF beacons heard in the last 30 min: 20m 2 beacons, best OH2B
+18 dB; …"* — hard evidence beside cluster activity, Kp and the clock. The
scout never invents a beacon: with nothing heard the sentence is absent.

## Tests

`NCDXFBeaconTests` pins every published start time (18 beacons × 5 bands)
against the model, a fixed UTC instant per band, half-open slot boundaries,
no drift across a UTC day (8640 slots) and before the Unix epoch (Demo
replays start in 1970), label placement and the 8 pt edge rule including a
transverter mapping, the sampler fixtures above, the history's 24-hour and
512-entry bounds, de-duplication, Codable round trip with bounds re-applied
on decode, the band-evidence window/threshold/order and the band scout
sentence.
