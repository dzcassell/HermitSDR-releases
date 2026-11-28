# Reference Beacon Lock

Issue #483. A converter in front of the radio — a satellite LNB, a microwave
or VHF transverter — has a local oscillator, and an ordinary one drifts with
temperature. A consumer LNB moves by kilohertz, which makes SSB through it
unusable: the dial is right at noon and 1.5 kHz off by evening.

If a beacon of known frequency is inside the span the radio is already
sampling, its offset from where it should be *is* the converter's error, and
every other signal in the span is off by the same amount. HermitSDR measures
that offset and shifts the receiver by it, continuously.

Open **Radio ▸ Reference Beacon Lock**.

## Receive only

The correction is a separate term on the receive mixer. It changes what the
receiver demodulates and nothing else:

- The transverter profile's stored RF offset is **not** written.
- The transmit frequency, the mapping the operator TX policy judges it
  through, the drive ceiling and every keying path are computed exactly as
  they are without this feature. A regression test locks a large correction
  in and compares the transmit frequency and policy bit for bit.
- The lock is **off** (state `unavailable`, correction zero, nothing
  measured) while a transmit-enabled profile is armed, and whenever the
  transmitter is keyed, tuning or two-toning. It comes back holding its last
  value when the transmitter is disarmed.

Applying the same correction to an uplink is a transmit-path change and is
not part of this feature.

## Setting it up

1. A beacon belongs to a **transverter profile** (`Transverters.md`). Select
   the profile in Settings ▸ Transverter. Its RF offset should be right to
   within the search width; the lock follows the rest.
2. In the Reference Beacon Lock window choose **Add a beacon** (or one of the
   QO-100 buttons), enter the beacon's published frequency on the RF side, and
   pick its type.
3. Tune so that the beacon is **inside the sampled span** — it does not have
   to be on the dial, only somewhere in the span the radio is delivering.
4. Turn on **Lock to this beacon**. It is off by default.

| Setting | Meaning | Range, default |
| --- | --- | --- |
| Nominal RF | The beacon's published frequency | — |
| Type | `CW / carrier`: the strongest line is the beacon. `400 Bd BPSK`: the signal is squared first, which removes the phase keying and leaves a line at twice the carrier offset | carrier |
| Search ± | How far either side of nominal the beacon is looked for | 100 Hz – 25 kHz, 5 kHz |
| Loop bandwidth | Narrow rides through fades and follows slowly; wide follows a fast-drifting oscillator | 0.05 – 2 Hz, 0.5 Hz |
| Jump limit | A change in the correction larger than this is never applied until you confirm it | 10 Hz – 25 kHz, 1 kHz |

Beacons are stored under their own settings key, keyed by the profile's id.
Deleting a profile drops its beacon the next time the window opens.

## What the window shows

| State | Meaning |
| --- | --- |
| `searching` | No beacon found yet. Whatever correction was in force stays |
| `locked` | The beacon is being followed |
| `holding` | The beacon was lost (faded, covered by interference, or tuned out of the span). The last correction is held, unchanged, until it is found again |
| `confirm jump` | A beacon was found further from the correction in use than the jump limit. Nothing moves until you press **Apply**; **Ignore** keeps looking. The first lock after a start is judged the same way, from zero |
| `unavailable` | The lock may not run: transmitter armed or keyed through this converter, a replay, or no live receiver. No correction is applied |

Beside the state: the correction in hertz, the drift rate in Hz per minute,
the beacon's signal-to-noise ratio in the analysis bin, and the search width
in use (smaller than configured when the sample rate cannot carry it).

The **chart** is the correction over the last 24 hours: one sample every ten
seconds and one at each change of state, ten thousand samples at most.
**Export CSV…** writes `time_utc,state,correction_hz,drift_hz_per_min,snr_db`.
The history is kept in memory while the app runs and is not saved between
launches.

## How it behaves

- **Lock**: three consecutive analysis windows (half a second to a second
  each, half-overlapped) must agree before a beacon is accepted.
- **While locked** only a line within 40 Hz of the prediction counts, so a
  stronger signal elsewhere in the search window does not pull the lock.
- **Loss**: after three missed windows, or three seconds with no samples at
  all, the state is `holding` and the correction is frozen.
- **Relock**: the correction glides to the new value over a second or two
  with the mixer's phase kept. There is no step in the audio. (The very first
  lock after a start has nothing to protect and goes straight to the measured
  value.)
- **Jump limit**: a relock further away than the limit waits for you.

The hardware is not retuned, the IQ history is not cleared and nothing is
reset in the receiver when the correction moves.

## QO-100

QO-100 (Es'hail-2) is a geostationary satellite that is not visible from the
Americas. Its narrowband transponder downlink is 10489.500 – 10490.000 MHz,
vertical polarisation.

**Add QO-100 receive profile** adds a receive-only transverter profile for an
unmodified universal LNB (local oscillator 9750 MHz): the radio tunes
739.5 – 740.0 MHz and the dial reads the downlink frequency. It is added to
the list, not selected, with the middle beacon attached and the lock off. A
receiver that tunes 739 MHz is needed — today the SDRplay RSPdx. For an LNB
with a different oscillator, or a down-converter to another IF, edit the
profile's RF offset.

The three beacon buttons attach one of the beacons to the active profile:

| Beacon | Frequency | Modulation | Tracker type |
| --- | --- | --- | --- |
| Lower | 10489.500 MHz | CW, F1A, 400 Hz shift | carrier |
| Middle | 10489.750 MHz | 400 bit/s BPSK | 400 Bd BPSK |
| Upper | 10490.000 MHz | CW, F1A, 400 Hz shift | carrier |

Use the **middle beacon** when you can: its carrier is unambiguous. The lower
and upper beacons are frequency-shift keyed, so they are two tones 400 Hz
apart; the lock follows the stronger one, and the published plan does not say
which of the two sits on the nominal frequency. Expect a constant error of up
to 400 Hz on those two until you have compared against the middle beacon and
adjusted the nominal frequency.

The band plan below is drawn on the band-plan strip (`BandPlanOverlay.md`) in
every regional plan, with the three beacons as spot markers:

| Downlink, MHz | Use |
| --- | --- |
| 10489.500 – 10489.505 | Lower beacon, guard band |
| 10489.505 – 10489.540 | CW only |
| 10489.540 – 10489.580 | Digimodes, 500 Hz maximum bandwidth |
| 10489.580 – 10489.650 | Digimodes, 2700 Hz maximum bandwidth |
| 10489.650 – 10489.745 | SSB only, 2700 Hz maximum bandwidth |
| 10489.745 – 10489.755 | Middle beacon, guard bands |
| 10489.755 – 10489.850 | SSB only, 2700 Hz maximum bandwidth |
| 10489.850 – 10489.858 | Broadcast frequency 10489.855 MHz, guard bands |
| 10489.858 – 10489.865 | Emergency frequency 10489.860 MHz, guard bands |
| 10489.865 – 10489.990 | Mixed modes (2700 Hz maximum) and special purpose, including contests |
| 10489.990 – 10489.997 | Multimedia beacon (8APSK, 7200 bit/s), guard bands |
| 10489.997 – 10490.000 | Upper beacon, guard band |

Source: AMSAT-DL, *QO-100 NB Transponder Bandplan and Operating Guidelines*,
<https://amsat-dl.org/en/p4-a-nb-transponder-bandplan-and-operating-guidelines/>,
read on 2026-11-27. The beacon frequencies, modulations and every segment
limit above were checked against that page; a unit test pins them. The plan
is AMSAT-DL's and may change; it is a guide for listening, not a licence.

## Other converters

Nothing here is specific to QO-100. Any converter with a known carrier in its
passband works the same way: a 10 GHz or 24 GHz terrestrial beacon, or a 2 m
or 70 cm beacon through a transverter. Attach a `CW / carrier` beacon to the
profile and enter its published frequency.

## Limits

- **Not verified on the air.** The acceptance figures (a carrier drifting
  2 kHz in ten minutes, a signal 100 kHz away held within 5 Hz of the dial;
  hold on loss; relock without a step) were measured on synthetic I/Q through
  the app's real receive chain. No LNB, no satellite downlink and no
  transverter was connected. The virtual radio was not used: it emits
  constant I/Q and cannot place a drifting carrier.
- Only the **main receiver's** demodulator is corrected. The sub-receiver,
  independent receivers and decode-only slices are not.
- The **panadapter scale, the waterfall and click-to-tune are not shifted.**
  A signal is drawn where it arrives, off by the correction; the dial and
  what you hear are right. The passband marker is drawn at the dial, so with
  a large correction it sits beside the signal it is demodulating.
- **Recordings** hold the uncorrected I/Q, as before.
- The beacon must be inside the sampled span. With a narrow span that limits
  how far from the beacon you can tune; out of span the lock holds.
- On a direct-conversion receiver keep the beacon away from the exact centre
  of the span: a DC spur there looks like a carrier at zero offset.
- A fixed error larger than the search width (25 kHz at most) belongs in the
  profile's RF offset.
