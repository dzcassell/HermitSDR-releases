# DeepFilter noise reduction (DeepFilterNet3 on Core ML)

Issue #299 — the build-out behind the top public request for "premium"
neural receive noise reduction. HermitSDR's fourth post-detector reducer,
selectable next to Spectral, RNNoise ("ML") and Adaptive in the RX **DSP**
popover, the console NR popup, the `N` key cycle and the SUB NR picker.

**What it is not.** WDSP's NNR models (GPL-2.0) are not used, consulted or
ported — owner decision pending, out of scope. This mode runs the
pretrained **DeepFilterNet3** network of H. Schröter et al.
(<https://github.com/Rikorose/DeepFilterNet>), whose code *and* weights are
dual-licensed MIT / Apache-2.0 (verified in the repository's `LICENSE`,
`LICENSE-MIT`, `LICENSE-APACHE` and README at commit `7b14b895`; notice in
`docs/licenses/DeepFilterNet.md`, provenance and hashes in
`HermitSDR/DSP/DeepFilterNet/Models/MODEL_MANIFEST.md`). Everything around
the network is native Swift written from the published algorithm.

## Status (2026-11-09)

Implemented and measured on synthetic fixtures. **No listening acceptance,
no HF recordings, no main+SUB load test yet** — see "Limits" before
treating any number here as a quality claim. Off by default.

## How it works

Chain audio (12 kHz, post-detector, pre-AGC) goes through the same ×4
bridge RNNoise uses (zero-stuff + 65-tap 5.4 kHz lowpass up, matching
lowpass + ÷4 down), so both neural modes share the resampler's alias
rejection and group delay. At 48 kHz, per 10 ms frame
(`HermitSDR/DSP/DeepFilterNet/`, reference: the upstream `libDF` streaming
runtime):

1. **STFT** — 960-point frames, 480 hop, Vorbis power-complementary window
   (`DeepFilterNetSTFT`). Analysis scales the unnormalized DFT by 1/960;
   synthesis overlap-adds the windowed inverse, so the round trip is exact.
2. **Features** (`DeepFilterNetFeatureExtractor`) — 32 ERB band energies in
   dB, minus an exponential mean (α = 0.99, ≈ 1 s), ÷ 40; and the lowest 96
   bins (0–4.8 kHz) divided by the square root of their tracked magnitude
   mean. Both trackers start from the reference ramps and advance every
   frame, even when the network is skipped.
3. **Network** — three Core ML ML Programs (`DeepFilterNetCoreMLInference`):
   the encoder sees the newest three feature frames and returns the
   embedding, the skip maps and a local-SNR estimate; the ERB decoder
   returns 32 band gains; the DF decoder returns a 5-tap complex filter for
   each of the 96 bins from a five-frame history of the encoder's `c0`
   map. GRU states live in the inference object. Estimates made at step t
   apply to frame t−2 (20 ms of look-ahead, as trained).
4. **Staging** (upstream real-time defaults) — local SNR < −10 dB: zero
   mask (frame judged noise only); > 30 dB: untouched; > 20 dB: ERB gains
   only; otherwise gains + deep filter. `Thresholds.alwaysProcess` exists for
   reference comparisons.
5. **Apply** — band gains multiply frame t−2; the deep filter replaces its
   first 96 bins with Σₙ Xₙ·cₙ over frames t−4…t; optional Valin post-filter
   (β = 0.02) against the noisy frame; the **attenuation limit** mixes a
   fraction of the noisy spectrum back (reference semantics: ≥ 100 dB =
   unlimited).
6. **Synthesis**, then the bridge back to 12 kHz.

**Delay.** One STFT hop + two frames of look-ahead = 1 440 samples at 48 kHz
(30 ms) + 2 × 32 samples of resampler group delay = **376 samples ≈ 31.3 ms
at 12 kHz**, plus up to one 10 ms frame of buffering (the first 120-sample
lump waits for a full frame) and, in the app, one chain block (~5 ms) of
worker hand-off. RNNoise adds ≈ 11 ms; the difference is the model's
look-ahead and 50 % overlap. (In stream-index terms each FIR head omits 64
samples, so sample-aligned tests see a lag of 344; `DeepFilterNetReducer`
documents both constants.)

**Worker.** `DeepFilterNetWorkerReducer` owns the pipeline and the models
behind a serial queue and three typed locks that never nest (bridge
resamplers — DSP thread only; bounded 0.5 s inbox/outbox + settings
mailbox; the non-Sendable processor — worker only). The DSP thread
upsamples, appends, schedules one drain and returns whatever finished
frames are waiting; it never waits for inference, loading or planning. More
than six frames of backlog → frames run through the STFT without the
network (identity, same delay) until it clears; a 0.5 s stall drops the
oldest input and counts it. The model loads on the worker on the first
drain after enable (never on the caller's thread); a missing or broken
model leaves an identity network in place and reports **unavailable** —
the mode is then an audible no-op with the same delay, never silence or a
stall. Status reaches the DSP popover through one generation-gated engine
callback.

## Controls

| Control | Where | Range | Default | Effect |
| --- | --- | --- | --- | --- |
| Noise reduction (DeepFilter / neural) | DSP popover · console NR popup · `N` cycle (Off → Gate → ML → Adaptive → DeepFilter) | — | off | Exclusive with the other three reducers. Fresh network/STFT/resampler state on enable. |
| Strength | DSP popover (main) · SUB NR ▸ Amount… | 0–100 % | 100 % (SUB 70 %) | Attenuation limit: 0 % caps the reduction at 6 dB, 99 % at 60 dB, 100 % lets the network remove everything it judges noise. Below 100 % that fraction of the untouched audio is mixed back, so a mis-gated syllable is never fully lost. |
| Post-filter | DSP popover (main) | on/off | off | Upstream's perceptual post-filter (β = 0.02): sharpens the gain where the network already attenuates. |
| Status line | DSP popover | — | — | "Loading the DeepFilterNet3 model…", "DeepFilterNet3 ready (Core ML)", or "Model unavailable — passing audio through (reason)". |

Persisted keys (`UserDefaults`): `nrDeepFilter`, `nrDeepFilterStrength`,
`nrDeepFilterPostFilter`. Operating settings / DSP presets carry the enable
flag as an optional (`deepFilterNoiseReductionEnabled`) so older catalogs
decode unchanged; crab flag `rx.deepFilterNR`. SUB selects it through
`SubReceiverDSPConfiguration.noiseReduction = "deepFilter"` and each SUB
chain owns its own worker and model instance.

## Verification

* **Golden vectors** (`Tests/DSPTests/DeepFilterNetPipelineTests`, 13
  tests): STFT, ERB and complex features, masked synthesis, deep filter and
  post-filter all match the upstream Python package (`libdf` Rust STFT /
  feature functions + `df.multiframe.DF`) at 1e-4 relative on an 8-frame
  synthetic input (`tools/deepfilternet-reference.py` →
  `Fixtures/DeepFilterNet/reference.json`); staging, attenuation limit,
  identity-network pure delay (exactly 1 440 samples), failure bypass,
  reset determinism and the bridge lag/gain are pinned.
* **Streaming decomposition** of the trained model (three-frame windows and
  five-frame `c0` history instead of causal padding, explicit GRU cells,
  grouped linears as batched matmuls) matches the official offline
  `DfNet.forward` to 3.9e-7 (gains), 1.2e-5 dB (local SNR), 9.5e-7
  (coefficients) over 200 frames.
* **Core ML vs PyTorch** (`DeepFilterNetCoreMLTests`, 3 tests; the suite
  compiles the `.mlpackage` sources with `MLModel.compileModel` and skips
  cleanly when they are absent): Float32 export within 2e-6 on 50 random
  frames per model and over a 200-frame recurrent run; on the reference
  input the Swift pipeline + Core ML reproduce the PyTorch streaming
  wrappers (`Fixtures/DeepFilterNet/network.json`) to < 5e-6. Float16 was
  rejected by the export gate (gain error 9.3e-3 > 5e-3), hence Float32 —
  which Core ML cannot place on the Neural Engine (fp16 only); it runs on
  GPU/CPU. The fp16 variants (4.4 MB) can be regenerated with
  `--precision float16` if listening finds a 1 % gain error acceptable.
* **Worker** (`DeepFilterNetWorkerTests`, 4 tests): identity network
  through the worker is a delayed passthrough with no drops; a throwing
  loader reports `.unavailable` while audio keeps flowing; disable drops
  queued audio and reset resumes; settings reach the processor before the
  next frame.
* Package: `python3 tools/swiftpm.py test --filter "DeepFilterNet"` → 20
  tests; with the adaptive, SUB-configuration, operating-settings, preset
  and docs-consistency suites → 144 tests, all passing on 2026-11-09.

## Measurements (Apple M4 Pro, macOS 27.2, Xcode 27.2, 2026-11-09)

Offline harness: `HermitSDR --hermit-deepfilter-ab <clean.wav|synth>
<new-dir> [snr-dB]` (`DeepFilterNetABCommand`, runs from the built app so
it uses the bundled models). Fixture: 18.2 s of **macOS text-to-speech**
(a synthetic voice, not a recording of a person) resampled to 12 kHz and
normalized to −20 dBFS RMS, plus white Gaussian noise with a 2 ms ×12
impulse every ~0.4 s (QRN-like) at the stated SNR. Each reducer's output is
aligned to the clean speech by searching its delay range; SNR is the
least-squares residual against the clean speech after a gain fit, first
second skipped.

| Input SNR | Bypass | Adaptive (defaults) | RNNoise | **DeepFilter** (100 %, upstream staging) |
| --- | ---: | ---: | ---: | ---: |
| 10 dB | 9.93 dB (+0.00) | 13.24 dB (**+3.31**) | 13.19 dB (+3.26) | 12.17 dB (+2.23) |
| 5 dB | 4.92 dB (+0.00) | 8.78 dB (+3.86) | 11.43 dB (+6.52) | 15.72 dB (**+10.81**) |
| 10 dB, `synth` harmonic bursts (not speech) | 9.88 dB (+0.00) | 13.81 dB (**+3.93**) | 12.11 dB (+2.23) | 5.19 dB (**−4.69**) |

Cost of the DeepFilter pass (synchronous reducer on one thread, STFT +
features + three Core ML models per 10 ms frame, 1 s warm-up, Core ML
compute units "all"):

| Metric | 10 dB run | 5 dB run |
| --- | ---: | ---: |
| Per-frame p50 | 0.432 ms | 0.433 ms |
| Per-frame p99 | 0.526 ms | 0.463 ms |
| Per-frame max | 0.702 ms | 0.535 ms |
| Real-time factor | 3.8 % | 3.7 % |
| CPU while running flat out | 108 % of one core | 110 % of one core |
| → CPU at real-time pace | ≈ 4 % of one core | ≈ 4 % of one core |
| Resident set before → after | 24.7 → 50.8 MB | 28.2 → 50.5 MB |
| Model load (three models) | 0.17 s (cold) | 0.07 s (warm) |
| Inference failures / frames bypassed | 0 / 0 | 0 / 0 |

The package test's per-frame figure on the same Mac is p50 0.439 ms /
p99 0.480 ms. The three compiled models add 8.5 MB to the app bundle
(8.6 MB of `.mlpackage` sources in the repository).

Reading the table honestly: at 10 dB the TTS-plus-white-noise fixture
favours the statistical reducers (the network treats parts of the synthetic
voice as noise and its zero-mask staging costs it on quiet syllables); at
5 dB it is far ahead, which is the regime the request is about. The third
row is the warning label: on harmonic bursts that are *not* speech the
network removes the "signal" itself (−4.7 dB; per-frame p50 fell to
0.26 ms because the staging skipped both decoders on frames it judged
noise-only). None of the rows says anything about SSB speech through an HF
channel, fading, QRM or how it *sounds*.

## Limits

* **Synthetic metrics only.** A text-to-speech voice in white noise with
  periodic impulses is not HF; SNR gain after a gain fit is not
  intelligibility or artifact assessment; no level-matched blind listening
  has happened. #299's acceptance list (matched recordings — weak HF
  speech, fading, interference, transients, clean strong speech and CW —
  and owner listening) is still owed before this is advertised as shipped.
* **Speech-trained.** Expect CW, data, carriers and broadcast music to be
  attenuated hard; do not run it ahead of decoders (the pre-NR decoder tap
  is unchanged, so decoders never hear it).
* **Staging mutes.** With the upstream thresholds a frame whose estimated
  local SNR is below −10 dB gets a zero mask; at 100 % strength that is
  silence. Lower the strength to keep a floor (e.g. 90 % → ≤ 54.6 dB).
* **Delay.** ≈ 31 ms + buffering + worker hand-off versus RNNoise's 11 ms.
  Not measured end to end in the app yet.
* **Not measured:** main + SUB simultaneous load, allocation counts, p99
  under system load, worker hand-off latency, repeated enable/disable and
  model-change stress beyond the unit tests. Float32 runs on GPU/CPU, not
  the Neural Engine.
* **Reference deviations** (documented in code): the post-filter is applied
  to all 481 bins (upstream's four-wide loop skips the Nyquist bin); the
  silence detector keeps the STFT running (upstream skips analysis); a 0 dB
  attenuation limit still passes through the STFT delay (upstream copies
  the input with zero delay).

## Reproducing the models and fixtures

```
brew install python@3.12 rust
/opt/homebrew/bin/python3.12 -m venv /private/tmp/dfn-venv
/private/tmp/dfn-venv/bin/pip install 'torch==2.7.0' 'torchaudio==2.7.0' coremltools 'numpy<2' soundfile deepfilternet
git clone --depth 1 https://github.com/Rikorose/DeepFilterNet /private/tmp/dfn-ref/DeepFilterNet   # check out 7b14b895
/private/tmp/dfn-venv/bin/pip install --no-deps /private/tmp/dfn-ref/DeepFilterNet/DeepFilterNet
unzip /private/tmp/dfn-ref/DeepFilterNet/models/DeepFilterNet3.zip -d /private/tmp/dfn-ref/models-unpacked
python3 -I tools/deepfilternet-reference.py Tests/DSPTests/Fixtures/DeepFilterNet/reference.json
python3 -I tools/deepfilternet-export-coreml.py /private/tmp/dfn-ref/models-unpacked/DeepFilterNet3 \
    HermitSDR/DSP/DeepFilterNet/Models --fixture Tests/DSPTests/Fixtures/DeepFilterNet/network.json
```

Downloaded code and models are untrusted data: keep them under their own
directory, never run an interpreter from inside it, and use `python3 -I`.
The speech fixture for the harness was made with
`say -o speech.wav --data-format=LEI16@48000 "<text>"`.

## Release pipeline

Nothing changes for the release scripts: Xcode compiles the three
`.mlpackage` bundles in the synchronized `HermitSDR` folder into
`.mlmodelc` resources during the normal build (verified in the Debug
product), and the package tests compile them on the fly. The generated
Swift classes Xcode emits for the packages are unused; the runtime loads by
resource name. Keep the `Models/` directory out of any size-based asset
check that assumes a Swift-only tree (8.5 MB).
