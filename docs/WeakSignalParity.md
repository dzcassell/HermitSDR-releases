# Weak-signal mode parity audit (#326)

Scope: every WSJT-family and weak-signal mode HermitSDR touches, verified
against the source tree and CHANGELOG as of 2026.1101_001. This is a planning
document — nothing here authorises transmit work, hardware sessions or new
dependencies. "Shipped" claims cite a file or a release; names that occur only
as logbook strings are called out as such.

Terms: **RX decode** = a native in-app decoder; **native TX** = HermitSDR's own
waveform behind ARM/`TXCoordinator`; **external** = WSJT-X / JS8Call / fldigi
driving the radio through HermitSDR's hamlib NET rigctl server (CAT PTT) and a
virtual audio route (`docs/DigitalModes.md`, "WSJT-X setup"). The Kenwood/`ZZ`
CAT emulation and the TCI server are receive-only — both refuse every keying
command (`HermitSDR/Integration/CAT/KenwoodCATServer.swift`, `docs/TCI.md`), so
an external program can decode and tune through them but must key through
rigctl (`HermitSDR/Integration/RigctlServer.swift`, `\set_ptt` behind ARM).

## 1. Matrix

| Mode | Submodes / periods | RX decode | Native TX | External | Evidence |
|---|---|---|---|---|---|
| FT8 | 15 s UTC slots; 77-bit messages, free text | Yes — in-process vendored `ft8_lib` (MIT) on the FT8 engine, time-machine replay, offline `.hiq` decode (#264), multi-DDC Super Skimmer | Yes — CQ / reply auto-sequencer, free-text beacon; dummy-load validated (ANAN, 2026-08-24; WSJT-X `jt9` decoded the monitored WAV); on-air validation pending (#69) | Yes (rigctl CAT PTT + audio) | `HermitSDR/DSP/FT8/` (`ft8_decoder.c`, `ldpc.c`, `encode.c`), `HermitSDR/Integration/FT8SpotEngine.swift`, `HermitSDR/TX/FT8Modulator.swift`, `FT8TXController.swift`, `FT8Sequencer.swift`, `FT8Beacon.swift`; releases 1.30 (RX), 2026.0824_002 (TX milestone 3), 2026.0908_003 (beacon), 2026.1022_001 (#264) |
| FT4 | 7.5 s slots; mutually exclusive with FT8 | Yes — same engine, `is_ft4` path of `ft8_decoder.c` | Modulator + slot clock implemented (`FT8Modulator.tones(for:ft4:)`, 105 tones, 5.04 s; `FT8SlotClock.slotSeconds(ft4:)`) — **no FT4-specific dummy-load cross-decode is recorded**; only FT8 frames were decoded externally | Yes | `HermitSDR/TX/FT8Modulator.swift:22-48`, `HermitSDR/TX/FT8TXController.swift:19-32`; release 1.93 (RX) |
| JS8 | **Normal only.** Fast / turbo / slow / ultra not decoded or sent; JSC-compressed data frames not ported | Yes — LDPC(174,87) sum-product decoder, frame reassembly | Yes — clean-room `JS8Modulator` (heartbeat, compound, directed, Huffman data); decoded by JS8Call-improved 3.0.3; used by MAGNET HF | JS8Call via rigctl + audio; JS8Call API hand-off | `HermitSDR/DSP/Digital/JS8Decoder.swift:5-15`, `JS8LDPC.swift`, `HermitSDR/TX/JS8Modulator.swift`; releases 2026.0911_002 (TX), 2026.0915_007 (RX) |
| WSPR | Type-1 messages only (call + 4-char grid + power); compound / hashed types 2 and 3 unpack to nil | Yes — K=32 Fano, 2-minute even-slot clock, WSPRnet reporter | Yes — finite UTC beacon schedule in Transmit › Native Transmit (`NativeTXWaveform.wspr`, `WSPRBeaconSchedule`); **operator dummy-load acceptance still owed** (#174) | WSJT-X WSPR via rigctl + audio | `HermitSDR/DSP/Digital/WSPRDecoder.swift:1-8`, `FanoDecoder.swift`, `WSJTMessage.swift`, `HermitSDR/TX/NativeTXWaveform.swift:91-126`; releases 2026.0915_007 (RX), 2026.1018_001 (TX) |
| JT65 | **JT65A only** (2.69 Hz spacing); B/C not implemented | Yes — RS(63,12) Berlekamp–Massey with erasures, 1-minute slots | No. `JT65.tones(for:)` and a 12 kHz fixture modulator exist for tests only | WSJT-X via rigctl + audio | `HermitSDR/DSP/Digital/JT65Decoder.swift:5-10,69-98`, `ReedSolomon63.swift` (`JT65Code`); release 2026.0915_007 |
| JT9 | **JT9A only** (1.736 Hz, 1-minute); JT9B–H fast submodes absent | Yes — K=32 Fano shared with WSPR | No. `JT9Decoder.tones(message:)` + fixture modulator (test only) | WSJT-X | `HermitSDR/DSP/Digital/JT9Decoder.swift:4-9,31,265`; release 2026.0915_007 |
| Q65 | **Q65-30A and Q65-60A only** (sub-mode A: tone spacing = symbol rate). 15 / 120 / 300 s periods and sub-modes B–E absent | Yes — QRA(65,15) belief propagation, 77-bit payload unpacked through `ft8_lib` pack77 | No. `Q65Code.encode` + continuous-phase 65-FSK fixture (test only) | WSJT-X | `HermitSDR/DSP/Digital/Q65Decoder.swift:8-57,92-93,432-487`; release 2026.0915_007 |
| MSK144 | — | **No** | **No** | WSJT-X MSK144 via rigctl + audio only; needs a 6 m-capable radio (see §2) | **Name only**: a Cabrillo `DG` mode-class string in `HermitSDR/Integration/Logbook/CabrilloExport.swift:147` and `docs/Logbook.md:105`. No decoder, modulator, panel or test |
| FST4 | — | **No** | **No** | WSJT-X ≥ 2.3 via rigctl + audio | **Absent** — zero occurrences in the tree |
| FST4W | — | **No** | **No** | WSJT-X via rigctl + audio | **Absent** — zero occurrences |
| FT2 | — | **No** | **No** | WSJT-X Improved 3.1.0 (fork) via rigctl + audio | **Absent** — zero occurrences |
| Feld Hell | 122.5 Bd Feld Hell (2.5 cps, 7×14 half-dots) | Yes — raster panel in Digital Modes | Yes — text / raster preview and TX (`NativeTXWaveform.hell`); dummy-load acceptance owed (#223) | fldigi via rigctl + audio | `HermitSDR/DSP/Digital/HellDecoder.swift:1-7`, `HermitSDR/TX/NativeTXWaveform.swift:45-68`; releases 2026.0915_007 (RX), 2026.1018_001 (TX) |

Shared infrastructure every row above relies on: the one-at-a-time
`DigitalModeDecoding` host in the Digital Modes window (`HermitSDR/App/DecoderCenter.swift`,
`DSP/Digital/DigitalModeMultiplexer.swift`), slot-clock rewinding under the RF
time machine (2026.0929_001) and the offline decode job
(`HermitSDR/Recording/OfflineDecodeJob.swift:503-509`), the WSJT-X UDP
logger broadcast (Decode messages for FT8/FT4 only — `Integration/LoggerBroadcasts/`),
and on the TX side `NativeTXWaveform.fsk` (48 kHz continuous-phase FSK used by
Hell/WSPR/ALE), `NativeTXPlayer` and `DataModeTXBundle`.

Correction found while auditing: none. The README/Capabilities rows
(`HermitSDR/DSP/Capabilities.swift:35,43,53`) describe exactly what the code
does; the only overstatement risk is reading "JT65 · JT9 · Q65" as covering
every submode, which the row's "receive only" plus this matrix now qualifies.

## 2. Gaps and feasibility

Common ground: all five gap modes carry the same 77-bit payload (`pack77`),
which HermitSDR already packs/unpacks through the vendored `ft8_lib`
(`ftx_message_encode`, `ftx_message_decode_std`; see `Q65Decoder.swift:454`),
so message handling, callsign hashing, grid/report parsing and the
stations-heard / PSKReporter plumbing are reusable as-is. Every HermitSDR
decoder to date is written from the published protocol description with
parameter tables treated as protocol constants (JS8LDPC header, Q65 header);
WSJT-X itself is **GPLv3**, so that clean-room discipline — read the paper and
the parameter tables, write the algorithm — must hold. `ft8_lib` (MIT) carries
only the (174,91) code, FT8/FT4 sync and the message codec; it has no MSK144,
FST4 or FT2 code to borrow.

### MSK144 (meteor scatter)

- **Protocol** (Franke & Taylor, "The MSK144 Protocol for Meteor-Scatter
  Communication", QEX Sept/Oct 2017; WSJT-X user guide, Protocols): 2000 baud
  minimum-shift keying, 144-bit frame = 8-bit sync + 136 coded bits from
  LDPC(128,90) over 77 message bits + 13-bit CRC, 72 ms per frame, frames
  repeated back-to-back for the whole 15 s (or 5/10 s) T/R period so a
  50–200 ms meteor ping can carry one frame. Audio centre 1500 Hz, occupied
  bandwidth ~2.4 kHz (the full SSB passband); an optional short-hand ("Sh")
  frame for the final exchange.
- **Reuse:** the JS8 sum-product decoder generalises to any sparse H
  (`JS8LDPC.swift` — column tables become a parameter), `pack77` from `CFT8`,
  the Digital Modes host. Nothing in HermitSDR does continuous (non-slotted)
  frame hunting at 2 kbaud; that is the new piece: a complex 12 kHz front end,
  MSK matched filter, sync-correlation search every ~6 ms, soft bits → LDPC,
  frame averaging across a ping, and a ping/dT/width report instead of slot
  S/N. The 15 s T/R clock only matters for TX turn-taking.
- **Hardware limit:** meteor scatter lives on 6 m / 2 m. HL2 stops at 30 MHz
  (`docs/RadioProfiles.md`, `p1.hermes-lite-2`); the ANAN Orion MkII covers
  0–54 MHz, so 6 m is in range on P2 only; 2 m needs a transverter profile.
  RX needs a 6 m antenna at the station, which Damon's station does not have
  on record (`docs/RadioProfiles.md` lists HF antennas only).
- **CPU / memory:** trivially small (12 kHz stream, 24 complex samples per
  frame-sync step, decoder of 128 variable nodes). The cost is engineering,
  not CPU.
- **Size:** RX ~1,200–1,600 lines Swift + fixtures (synthetic ping generator,
  AWGN threshold, noise/invalid-frame rejection) — about the Q65 decoder's
  size. TX adds ~300 lines (MSK synthesis at 48 kHz through `NativeTXWaveform`
  + a 15 s turn controller) but is a TX-path change → stage branch.

### FST4 / FST4W (LF/MF and slow-period HF)

- **Protocol** (WSJT-X 2.3 "FST4 Quick Start", wsjt.sourceforge.io/FST4_Quick_Start.pdf;
  user guide, Protocols; a Franke/Somerville/Taylor QEX write-up exists but the
  issue was not verified for this audit): 4-tone GFSK, tone spacing = symbol
  rate, 160 channel symbols = 120 data symbols (2 bits each) + five 8-symbol
  Costas sync arrays; LDPC(240,101) over 77 bits + 24-bit CRC; T/R periods 15,
  30, 60, 120, 300, 900 and 1800 s (WSJT-X `nsps` 720 / 1680 / 3888 / 8200 /
  21504 / 66560 / 134400 samples at 12 kHz). FST4W is the same waveform with
  the WSPR-style beacon message (call, grid, power) and only the 120–1800 s
  periods; FST4W-120 is ~2 dB more sensitive than WSPR in ~6 Hz. The reference
  decoder adds ordered-statistics decoding behind belief propagation for the
  deep passes; a BP-only first cut costs ~1–2 dB of threshold.
- **Reuse — the best fit of the five:** `WSJTSlotDSP` (down-conversion,
  averaged spectra, tone correlation, slot clock), the `Q65Mode` pattern for a
  period table (`Q65Decoder.swift:39-60`), the GFSK pulse maths already in
  `FT8Modulator.swift:59-130` for fixtures, `JS8LDPC` generalised to (240,101),
  `WSJTMessage` / `pack77` for FST4W's beacon payload, WSPRnet-style reporting
  (`WSPRNetReporterTests`) and the existing WSPR beacon workflow as the TX
  template. Long periods (900/1800 s) need the decoder to hold up to 1800 s ×
  12 kHz × 4 B ≈ 86 MB of audio unless it decimates on arrival — decimate to
  ~100 Hz baseband per period as Q65 does and the buffer is < 1 MB.
- **Hardware limit:** none for RX — HL2 and ANAN both receive 2200 m / 630 m.
  TX on LF/MF is out of scope (licence, Alex LPF coverage) and FST4 on HF uses
  the same Digital profile as WSPR.
- **Size:** RX ~1,500–2,000 lines (period table, sync search over seven
  geometries, LDPC(240,101), CRC-24, FST4W message type, tests with reference
  WAVs). FST4W-only first slice ~900 lines. TX ~250 lines (GFSK synth +
  schedule controller reusing `WSPRBeaconSchedule`) — staged.

### FT2

- **Status:** FT2 is not a WSJT-X mainline protocol. It shipped as
  open-source in the DG2YCB **WSJT-X Improved 3.1.0** fork (2026-02-26) as an
  "ultra-fast" 77-bit mode with 3.75 s T/R (half of FT4); a separate,
  parameter-incompatible IU8LMC "FT2" exists (ft2.it), and early builds
  reported auto-sequence interoperability problems with JTDX/MSHV betas and a
  crash on fast band/mode changes. There is no QEX-style specification, no
  stable parameter set agreed across implementations, and the only reference
  code is GPL.
- **Recommendation:** do not implement. Re-evaluate when (a) a single
  protocol description is published, (b) mainline WSJT-X or two independent
  implementations interoperate, and (c) a public reference-recording set
  exists. External use through rigctl + audio works today; nothing in
  HermitSDR needs to change for that beyond the existing 3 kHz data filter.

### JT65 / JT9 / Q65 native TX

- **What exists:** complete encoders and tone generators already compile into
  the app for test fixtures — `JT65.tones(for:)` (RS(63,12) + interleave +
  sync vector), `JT9Decoder.tones(message:)` (K=32 + bit-reversal), `Q65Code.encode`
  + `Q65.syncPositions`. `NativeTXWaveform.fsk(tones:samplesPerSymbol:hz:)`
  already turns tone lists into 48 kHz continuous-phase FSK for WSPR, and
  `WSPRBeaconSchedule` is the slot-clocked, explicitly-selected-dial, no-catch-up
  session model that a 60 s (JT65/JT9) or 30/60 s (Q65) transmission needs.
- **Size:** ~200–400 lines per mode plus a shared "WSJT slot session" in
  Native Transmit, plus Native Transmit UI rows and `NativeDigitalTXLimits`
  entries. Entirely TX-path work → `stage/<issue>-wsjt-native-tx`, external
  cross-decode by WSJT-X on a dummy load before merge (acceptance criterion
  from #326).
- **Demand check:** JT65/JT9 HF activity has largely moved to FT8; Q65 is the
  live EME/scatter mode. If any of the three is worth native TX it is Q65 —
  but Q65 QSOs run on 6 m/VHF/EME where the station has no antenna, so this is
  the lowest-value TX item.

### JS8 fast/turbo/slow, Q65 other periods, JT65B/C

Small, well-specified extensions of shipped decoders: JS8 speeds change only
symbol length and slot period (`JS8Decoder.swift:15` lists them as
unsupported); Q65-15/120/300 and sub-modes B–E are `Q65Mode` rows plus a tone
spacing multiplier; JT65B/C double/quadruple the tone spacing. Each is ~100–
300 lines plus fixtures. They are listed for completeness; none is requested.

## 3. Recommended order

1. **FST4W RX (receive-only spike).** Lowest risk, best reuse, clear
   workflow fit: WSPR beacon monitoring, WSPRnet-style reporting and the
   stations-heard map already exist, and FST4W is "WSPR with 2 dB more and
   seven periods". It exercises the two components every later mode needs — a
   general sparse-LDPC BP decoder and a multi-period slot clock — on a mode
   with a public reference decoder and WAVs for acceptance (WSJT-X saves its
   own; `jt9` decodes them offline). Deliverable: decode WSJT-X-generated
   FST4W-120/300 recordings in the offline `.hiq` decoder, reject noise,
   publish measured thresholds.
2. **FST4 RX** — same decoder, 77-bit standard messages, the 15–60 s periods
   for HF QSO monitoring; the LDPC(240,101) + OSD improvement lands here.
3. **MSK144 RX** — new signal-processing shape (continuous frame hunting),
   needs 6 m hardware and an antenna the station lacks; feasibility is clear
   but acceptance cannot be done locally, so it waits for either a 6 m antenna
   or a reference-recording-only acceptance agreed in its issue.
4. **Native JT65/JT9/Q65 TX, FST4W TX** — staged TX work; only after the
   existing WSPR and Feld Hell dummy-load acceptance (#174, #223) is recorded,
   since they share the same `NativeTXWaveform`/schedule path and the same
   open acceptance.
5. **FT2** — not now (see above).

Open implementation issues only after step 1 demonstrates decoding of
independently generated recordings, per #326's acceptance clause.

## 4. References

- Franke, Somerville, Taylor, "The FT4 and FT8 Communication Protocols",
  QEX July/Aug 2020.
- Franke, Taylor, "The MSK144 Protocol for Meteor-Scatter Communication",
  QEX Sept/Oct 2017.
- Taylor, "The JT65 Communications Protocol", QEX Sept/Oct 2005.
- WSJT-X 2.3 FST4 Quick Start and the WSJT-X User Guide "Protocol
  Specifications" chapter (FST4/FST4W, Q65, MSK144 parameters).
- WSJT-X Improved 3.1.0 release notes (FT2, 2026-02-26).
- In-tree: `docs/DigitalModes.md`, `docs/NativeTransmit.md`,
  `docs/TCI.md`, `docs/KenwoodCAT.md`, `HermitSDR/DSP/Capabilities.swift`.
