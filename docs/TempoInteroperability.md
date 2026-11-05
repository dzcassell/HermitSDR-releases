# TempoFast and TempoDeep interoperability review

**Decision, 2026-11-05.** Defer a HermitSDR codec. A receive-only spike
could exercise our DSP plumbing, but it could not establish that a second
implementation interoperates with a stable wire format. Keep this review as
the record for issue #327.

TempoFast offers a four-second conversational slot and incremental redundancy
across repeat transmissions. TempoDeep is a separate, slower waveform designed
for fading channels. Both reuse the WSJT-X 77-bit message representation and
LDPC/CRC family. Receiving those existing modes does not make a receiver
compatible with Tempo framing, acquisition or redundancy. A second Tempo
receiver could help operators monitor existing Tempo activity. The current
interoperability target is the originating ecosystem.
[Upstream protocol and on-air history](https://hamradiotools.io/protocol/)

We reviewed the upstream source tree and protocol companion at commit
`0eb82b0cda613347d91a5783b286bf7f9413b79a`. The document describes slot
timing, modulation, synchronization, FEC, redundancy-version signaling,
and receiver expiry. It references the source for wire details. It does
not define a separate wire-version identifier or a conformance matrix for
old and new senders. The originator supplies standalone modem tests and
end-to-end loopback, noise and HARQ tests. Those are useful upstream
regression checks. This review did not find a second implementation or an
independently produced, versioned RF or PCM corpus with expected decoded
messages and reuse terms. A repository or application release number pins
what was tested and does not itself define wire compatibility.
[Pinned protocol companion](https://github.com/kd9taw/Nexus/blob/0eb82b0cda613347d91a5783b286bf7f9413b79a/docs/Tempo-Protocol.md)
[Pinned HARQ loopback](https://github.com/kd9taw/Nexus/blob/0eb82b0cda613347d91a5783b286bf7f9413b79a/crates/tempo-core/tests/harq_loopback.rs)

The originator reports a real TempoFast decode and a completed two-station
6 m QSO. Its sensitivity and HARQ gain figures come from bench simulations,
including noise and fading sweeps. We found no independent on-air
decode-rate-versus-signal-level curve. Use the on-air report as evidence
that a link worked under those conditions.
[Originator’s protocol and validation status](https://hamradiotools.io/protocol/)

The reference stack uses Fortran, C/C++, FFTW, and Rust wrappers. The project
is GPL-3.0 and the upstream notices identify reused WSJT-X code. A future
implementation proposal must review code provenance, distribution and the
terms on each proposed fixture. This review imports no upstream code,
recordings, or generated vectors.
[Pinned license](https://github.com/kd9taw/Nexus/blob/0eb82b0cda613347d91a5783b286bf7f9413b79a/COPYING)
[Pinned notices](https://github.com/kd9taw/Nexus/blob/0eb82b0cda613347d91a5783b286bf7f9413b79a/NOTICE)

Revisit receive-only evaluation when we have a pinned wire contract and
shareable independent vectors. Cover clean TempoFast RV0/RV1/RV2 and TempoDeep
frames, known messages and CRC failures, noise and fading, wrong waveform or
unsupported wire version, missing or reordered retransmissions, duplicate
redundancy versions, HARQ reset/expiry, and simultaneous nearby signals
that must never be combined. Measure false decodes and resource use as well
as successful decodes. RF transmit or QSO automation would require a
separate decision.
