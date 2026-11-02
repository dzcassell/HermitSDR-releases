# Diversity with an independent SUB receiver

Issue #176. On reviewed P2 profiles with enough DDC resources, enable SUB and
Diversity RX together. SUB retains its independent VFO B, receive chain and
volume. The existing SUB mode/filter controls remain shared with the main
receiver; this milestone does not add the general receiver bank in #165.

Orion2 reserves synchronized DDC0/1 for ADC0 + weighted ADC1 and streams their
interleaved coherent samples on port 1035. Independently tuned SUB uses DDC3 on
port 1038. Normal main DDC2 is parked during diversity. The selected SUB input
can be ADC0 or ADC1. Each ADC has a shared physical RF front end: SUB on ADC1
shares the diversity pair's ADC1 filters and attenuation. Independent digital
tuning does not imply independently selectable physical antenna/BPF/gain.

The capability requires P2, diversity support, at least two ADCs and sufficient
receiver/DDC slots beyond the coherent pair. Unsupported profiles keep the
existing mutual exclusion and show a reason. Radio catalogs preserve both
choices, adapting only the working copy to unsupported hardware. Cold restore
waits for profile adaptation before resolving the choices.

Monitor DDCs remain suspended during diversity and resume on exit. PureSignal
capture retains its existing DDC0/DAC-reference pair and suspends SUB/monitors;
this change does not modify transmitter authorization or keying behavior.
Wrong-mode and disabled SUB packets are dropped before per-port sequence state.
The combiner processes only coherent port 1035; SUB packets remain independent.

Software validation uses the virtual radio and packet fixtures for allocation,
rates, ADC selection, phase words, weighted sample decode, transitions, reconnect,
resource refusal and PureSignal/monitor reservation. Hardware verification must
separately establish packet behavior and coherent two-input RF reception; an
ANT3 antenna alone does not establish a second signal on the RX2/ADC1 input.

On 2026-10-04, the owned unicast RX-only probe ran the user's ANAN7000 on
ANT3 at main 7.100 MHz and SUB 7.074 MHz, 192 kHz. With SUB on ADC0 it
received 16,134 coherent packets (1,919,946 pairs) and 8,067 independent SUB
packets (1,919,946 samples) in ten seconds, with zero missing/duplicate/reordered
or malformed frames. A separate five-second SUB-on-ADC1 check also had zero
transport errors. PA/MOX/drive remained zero; each owned probe sent RUN=0 and
read-only identity discovery confirmed idle afterward. The RX2 input did not
have a known second antenna, so this establishes transport delivery only.

A further five-second 384 kHz SUB-on-ADC0 probe received 1,919,470 coherent
pairs and 1,919,708 SUB samples with zero transport errors. DUC configuration
also explicitly disables radio microphone-jack PTT, matching the application.

Native signed Debug validation used private mirrored preferences, volume zero,
mute on, RX ANT3 and TX SAFE. A guarded receive-only loopback relay verified the
exact child UDP owner and physical idle MAC before forwarding configuration;
PA/MOX/drive and TX IQ were prohibited. The real connected app enabled diversity
while SUB stayed on (DDC mask 0x09), toggled SUB off/on while diversity stayed on
(0x01/0x09), and toggled diversity off/on while SUB stayed on (0x0c/0x09).
Disconnect/reconnect restored both choices and resumed 0x09 reception. Native
status showed approximately 2,419 combined packets/s at 192 kHz. One sequence
error appeared around a live allocation transition, so this native relay check
is not a zero-loss assertion; the separate raw transport probes above are.
Only owned test children were stopped, followed by expected-MAC read-only idle
confirmation. The installed SquareSDR 2 streaming app was left alone. No RF
transmission or independent coherent two-antenna null test was performed.

## Find null (#294, first slice)

The diversity panel's **Find null** button is a finite measurement, not a
tracking loop. It captures about 0.75 s of both coherent ADC streams ahead of
the combiner, estimates one weight, previews it and waits. Nothing moves the
pad except **Apply** (the existing manual-steering path) and **Restore** (the
weight that was on the pad before the first Apply). Continuous, slow
tracking with confidence/hold reporting is a later slice and is not present.

### Objective and guard

Two analysis windows are derived from the receiver, in Hz offsets from the
DDC center: the **wanted window** is the current channel passband (mode edges
plus shift, placed at the dial's offset inside the sampled span); the
**interference band** is everything else in the span, less a two-bin guard
around the wanted window. The estimator minimises the interference band's
power and reports the wanted window separately — a weight that merely
lowered total power by cancelling the wanted signal is a failure, not a win.

### Mathematics (original, native vDSP)

Both streams are Hann-windowed in 4096-sample DFT blocks (shrinking to fit
a short capture). Per band the cross-spectral sums Sxx = Σ|X|², Syy = Σ|Y|²
and Sxy = Σ X·conj(Y) are accumulated. The combined power of any weight is
P(w) = Sxx + |w|²·Syy + 2·Re(w·conj(Sxy)), so the unconstrained optimum is
the closed-form Wiener weight w* = −Sxy/(Syy + ε) with ε = 10⁻⁹·(Sxx+Syy) as
regularisation. Confidence is the interference band's magnitude-squared
coherence |Sxy|²/(Sxx·Syy): below 0.25 there is no single weight that can
cancel the band and no suggestion is made. |w| is clipped to the pad's
radius (2). If the wanted window would lose more than 3 dB relative to the
current weight, the weight walks back along the straight line from the
current weight toward w* until it satisfies the bound; a result that then
improves the band by less than 3 dB is reported as "held by the passband
guard". "Before" always means the current weight, so the preview describes
the change the operator would hear.

### Refusals

No suggestion is ever a guess: too few samples, non-finite data, a silent
RX1, an RX2 more than 40 dB below RX1 in the interference band (silent,
disconnected or unplugged second antenna) and insufficient coherence each
name their reason in the panel. The button is disabled, and a running
capture is stopped, while the transmitter is keyed, tuning, two-toning or
RF-hot and while PureSignal capture is armed; those guards are read, never
changed. A retune, sample-rate change, disconnect or Diversity off also
stops a capture and drops the preview; a hand on the pad stops a capture and
ends the "applied" state. A result from a capture that was cancelled or
superseded is rejected when the worker returns.

### Ownership

`DiversityPairCapture` is a checked-`Sendable` bank under one typed lock:
the Protocol 2 connection queue decodes a diversity packet a second time with
the streams kept apart (only while a handler is installed) and the bank
copies what fits into pre-sized storage — no allocation, FFT, disk or UI
wait on the packet thread; excess samples are dropped and counted. The full
capture hops to the `hermitsdr.diversity.null` utility queue for the pure
estimator and the result crosses to the main actor with a generation check.
`DiversityNullFinderModel` (main actor) owns the phase, preview, applied and
restorable weights; `RadioState+DiversityNull.swift` supplies the windows,
guards and the weight setter and observes the published guards.

### Assumptions and limits

The interference must be coherent between the antennas over the capture (one
local source with a stable amplitude/phase ratio); several sources at
different ratios cannot be nulled by one weight and read as low coherence.
The wanted window is only as good as the current passband placement. Hardware
acceptance with two antennas on an ANAN is operator-assisted RX work and has
not been performed; the synthetic fixtures establish ≥ 20 dB of coherent-noise
reduction with ≤ 3 dB of wanted-signal change, the no-correlation and
silent-input refusals, |w| clipping, the guard, bounded capture, late-worker
rejection and the pair tap.
