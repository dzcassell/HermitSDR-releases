# Changelog

All notable changes to HermitSDR (named SquareDeck before 7.10 —
historical entries below keep the old name). From `2026.0727_001` onward
versions are `YYYY.MMDD_XXX` — release date plus a build number that starts
at `001` each day and increments. Earlier releases used `X.YZ` (`Y` =
feature, `Z` = bugfix, `X` = major milestone; `2.00` was transmit). Every
batch of improvements ships as a new version.

## [Unreleased]

### Added
- **Worked World & DX Radar** (Zeus parity #82): an interactive Metal-backed
  globe, 2D fallback, UTC day/night lighting and gray line, great-circle paths,
  beam heading/distance, logged/confirmed/spotted/decoded layers, and band/mode/date
  filters. Local radar prioritizes new contacts using the full log; unknown or
  ambiguous locations remain explicit. Coastlines are bundled public-domain data.
- **Logbook workspace** (Zeus parity #81): streaming ADIF import with validation,
  duplicate preview/policy, preserved unknown/typed fields, standard-field editing,
  bulk changes/deletion, saved filters, sortable paged tables and scoped exports.
  Atomic background persistence retains the legacy JSON format, creates migration
  and per-operation backups, supports recovery, and flushes safely at shutdown.
- **Worked and confirmed awards** (Zeus parity #83): filtered-log DXCC, WAS and
  2/4/6-character grid coverage, needed targets, band/mode matrices, QSO drill-downs,
  local CSV summaries, explicit unknowns and versioned entity/country data.
  Portable calls and state ambiguity are handled conservatively; six-character
  missing grids are generated in bounded pages.
- Large-log benchmark and regression fixtures for ADIF preservation, malformed
  imports, duplicate policy, atomic recovery, LoTW identity and award edge cases.
- Independent **Signals over scenery** (0–100% foreground visibility) and
  **Underlay brightness** (0–100%) controls for Deep Space and Night Garden.
  Dimming affects the entire scene, including particles, without dimming the
  signal overlay. Existing four presets, six signal colors and signal brightness
  remain available together in a Waterfall visibility section.
- **High contrast** shortcut selects bright amber signals over dimmed scenery.
  Settings remain independent per scene and preserve older saved appearances.
  Scrollable settings keep the title and action buttons reachable.
- Regression coverage for migration, bounds, persistence, preset overrides and
  independent controls; Metal smoke exercises full foreground opacity and dimming.

### Fixed
- Duplicate detection retains the full recorded ADIF parent-mode/submode pair,
  including distinctions between broad quick logs and more specific imports.
- LoTW confirmations now require a positive QSL and the contact's UTC second,
  call, band, mode/submode and station identity. Fractional quick-log timestamps
  match their exported whole second. Contact location details are retained only
  when matching reports agree; malformed responses do not partially apply.
- Cluster/radar receiver tuning honors explicit FM, NFM and DSB mode tokens.
- Quick-log entry points preserve station identity; FT8/FT4 logs retain exchanged
  grids/reports. Imported frequency-only contacts resolve all ADIF band ranges.

### Validation
- Final GitHub CI: 1,084 tests, two intentional skips, zero failures. Unsigned
  Debug/Release builds, documentation checks, repository audit and the
  10-second performance smoke (30-second limit) pass.
- A synthetic 100,000-contact log passes import/export, duplicate handling,
  adding/editing, multi-contact bulk changes/deletion, invalid-input rejection,
  saved filters, pagination, backup restoration and awards drill-downs in
  isolated muted Demo. Optimized import/export take about 1.1/2.3 seconds;
  awards/world snapshots take about 0.26/0.28 seconds and LoTW matching 0.15 seconds.
- Worked World passes deterministic geometry tests, native globe rotation,
  Home/selection navigation, 2D/layer/filter checks, and a 2,500-marker, 90-frame
  Metal API validation smoke (0.09/0.66 ms median/p95 GPU time).
- Deep Space and Night Garden pass 240-frame Metal API validation and native
  settings checks for sliders, High contrast, colors, presets, Reset, scrolling
  and independent preferences. No RF transmission or live LoTW requests were made.

## [2026.0904_001] — 2026-09-04

### Added
- **Deep Space Observatory** in Dynamic Underlays: slowly curling violet/teal
  nebulae, layered stars, a rotating gas giant, translucent planetary rings,
  an orbiting moon with transits/shadows, drifting dust, and rare comets.
  Independent settings include star density, motion, all signal colors/levels,
  brightness, and individual scene effects. Planet/ring/moon occlusion and
  surface motion are rendered directly on the GPU.
- **Night Garden** under the palette icon: a lush moonlit rainforest with GPU
  animated ferns and orchid vines, glowing fungi, drifting mist, moonbeams,
  fireflies with trails, rain, reflective stream ripples, frogs, moths and a
  rare distant owl. Includes independent scene settings, four signal levels,
  six overlay colors and adjustable brightness. Aquarium preferences remain
  separate, and the marquee and receiver controls remain available.
- Focused configuration, persistence, mesh-budget and rare-visitor tests plus
  a native Metal validation smoke with deterministic rare-event sampling.

### Changed
- Group Aquarium, Night Garden, Deep Space, and their settings in the palette icon's
  **Dynamic Underlays** submenu. Ordinary and animated color palettes remain
  in the main palette list; active selections retain native checkmarks.

### Validation
- Full regression suite: 1,042 tests, two intentional skips, zero failures.
  Unsigned Debug/Release builds, all 44 documentation checks, repository audit,
  and the 9-second performance smoke (30-second limit) pass.
- Native 240-frame Metal API validation covers Deep Space, Night Garden and
  the shared Aquarium signal passes. At 1800×720 with 4× MSAA, Deep Space
  with 1,600 stars measured 0.38 ms median / 0.47 ms p95 GPU time; Night Garden
  with 160 fireflies measured 0.61 ms / 0.90 ms on the development Mac.
- Muted Demo checks cover the Dynamic Underlays submenu, scene switching,
  settings launchers, color/brightness controls, Reset and saved preferences.
  Planet visibility preserves ring/moon choices. SKIM stays off after startup
  with an old enabled preference and after quitting while enabled.
- Night Garden and Deep Space default to Balanced/Ice blue to preserve their
  scenery under strong signals; Broadcast and Intense remain available.
  No RF was transmitted.

### Fixed
- **SKIM starts off every launch**, including when an older settings file
  saved it enabled. Enabling it remains available for the current session.

## [2026.0903_006] — 2026-09-03

### Added
- **More visible aquarium signals** — add Intense above Broadcast, a 50–300%
  signal-brightness control, and Sea glass, Ice blue, Amber, Violet, White,
  and Thermal signal colors under the palette icon's Aquarium Settings.
  Color changes affect the signal overlay while retaining the reef's colors.
- A photographic orange sea star creeps very slowly across the sand, and a
  large silver-blue trevally occasionally passes through the distant water.
  Both have independent toggles. Visits last 50 seconds, start after eight
  minutes, and recur roughly every ten minutes; Activity cannot speed up the
  visit schedule or sea-star crawl.

### Changed
- Fish now occasionally reverse within the tank as well as at its ends,
  slowing into a smooth edge-on turn with their orientation following actual
  travel. Shallow vertical drift and restrained tail motion remain.
- Existing saved intensity, fish counts, and effects survive the settings
  upgrade. New/reset settings select Intense; previous saved levels stay selected.

### Tests
- Cover color/brightness persistence, legacy settings, bounded signal controls,
  and rare-visit timing/directions/hourly wrap. The Metal smoke exercises four
  intensities, six colors, new wildlife toggles, and selectable scene times
  for rendering rare visits without waiting eight minutes.

### Validation
- Final full suite: 1,030 tests, two intentional skips, zero failures; unsigned
  Debug/Release builds, 44 documentation checks, repository audit, 8-second
  performance smoke, and Metal API validation pass. The 240-frame smoke
  covers new controls and a rare visitor at a deterministic scene time;
  1800×720, 4× MSAA, 64 fish plus the visitor measured 0.69 ms median / 0.89 ms
  p95 GPU time on the development Mac.
- Muted Debug Demo checks cover color switching, brightness adjustment,
  wildlife toggles, Reset, entry, persistence after relaunch, and picker layout.
  Extra HDR gain is confined to the water pass at default brightness so strong
  signals do not clip foreground wildlife to white. No RF was transmitted.

## [2026.0903_005] — 2026-09-03

### Changed
- **Broadcast aquarium signals** — add selectable Subtle, Balanced, and
  Broadcast signal treatments. The chosen preview C becomes the Broadcast
  default: brighter cyan-to-mint signals reach 100% opacity inside the water
  and a fainter 36% over fish, plants, coral, and crabs. Weaker signals fade
  progressively and the noise floor stays transparent, making band history
  easier to read in normal use and livestreams. Existing `_004`
  aquarium preferences migrate to Broadcast without losing scene choices.

### Tests
- Cover all three compositing levels and legacy aquarium preference migration;
  exercise the foreground overlay in the Metal validation smoke.

### Validation
- Debug app build and the 240-frame Metal API validation smoke pass. The
  built renderer's Broadcast PNG matches approved preview C pixel for pixel
  using identical synthetic history and fish positions. All three levels,
  28/64/0 fish, and effect toggles pass; the 64-fish composite measured
  0.60 ms median / 0.70 ms p95 at 1800×720 with 4× MSAA on the development Mac.
- Full regression suite: 1,028 tests, two intentional skips, zero failures
  (293 seconds). The preceding overlay revision also passed an isolated Demo
  Mode UI check; the stronger C treatment was verified offscreen.
- Release gates: unsigned Debug/Release builds, 44 version/documentation
  checks, repository audit, and a 9-second performance smoke all pass.

## [2026.0903_004] — 2026-09-03

### Added
- **Aquarium palette and living reef** — select Aquarium under the main
  palette icon to pair sea-glass waterfall colors with photographic reef
  artwork, eight fish species, flexing fins and tails, swaying plants/coral,
  crawling crabs, bubble streams, drifting particles, sunbeams, and moving
  caustics. Metal animates bounded, instanced meshes in the existing HDR scene;
  PNG captures and YouTube window capture include the reef. Aquarium Settings
  controls fish population, activity, waterfall visibility, and individual FX.
  Other palettes restore ordinary effects; reef GPU resources are released.
- **Waterfall scrolling marquee** — the main palette icon now opens saved
  message, installed font family, size, bold, color, speed, repeat pause, and
  vertical-position controls. Show now starts a fresh pass. Text scrolls fully
  offscreen before the next pause and appears in YouTube Live window capture.
  Off by default; animation does not intercept waterfall tuning or publish
  through the radio/Scene menu graph.
- Regression coverage for complete passes, long messages, repeat timing,
  disabled/blank content, invalid settings, persistence, and replay timing.

### Changed
- **Calmer aquarium fish** — default fish now make fluid 100–200 second
  circuits instead of racing around the tank. Whole-fish vertical travel is
  reduced by roughly fourfold; slower, tail-weighted deformation and gentler
  pitch keep bodies stable while fins and tails remain alive.

### Validation
- Full suite: 1,026 tests, two intentional skips, zero failures; unsigned Debug
  and Release builds, repository audit, and the 9-second performance smoke
  pass. Demo Mode checks cover settings, moving/repeating text, persistence
  after relaunch, aquarium palette re-entry, PNG capture, and Station
  child-window selection during animation. A timed visual pass covers the
  revised fish speed, shallow vertical drift, and tail-weighted deformation.
- Aquarium Metal smoke: 240 frames with 28/64/0 fish, effect toggles, and
  population changes; no API validation errors. At 1800×720 with 4× MSAA and
  64 fish, the revised aquarium pass measured 0.31 ms median / 0.40 ms p95 on the
  development Mac (not the whole SDR frame).

### Documentation
- Catalog the major ZeusSDR feature gaps in GitHub issue #94 and group the
  resulting implementation tracks under one milestone with area labels.

## [2026.0903_003] — 2026-09-03

### Fixed
- **Disappearing submenus during reception (#74)** — keep the application scene
  independent of frequent meter and decoder updates, so Station and other
  nested menus remain open and their items can be selected. Menu checkmarks
  and availability still follow operator settings through the focused menu
  model, whose changes also refresh the application scene so labels stay current.
  Preserve deferred radio initialization after settings migration.

### Tests
- Guard the application ownership boundary against observing the broad radio
  publisher and reintroducing menu rebuilds during reception. Full regression
  suite: 1,016 tests, two intentional skips, zero failures; Debug/Release builds,
  native child-window selection in Demo Mode, and release gates pass.

### Documentation
- Record the Codex-to-Claude handoff: published versus installed version,
  completed validation, bench findings, remaining issue scope, and release
  synchronization notes; update the record after Damon installed `_002` and
  resumed Codex to report the submenu regression.

## [2026.0903_002] — 2026-09-03

### Fixed
- **SSTV and weather-fax callback locking (#61)** — image, text-status, and
  decoder-session handlers now run after the decoder state lock is released.
  Handlers can read capture/configuration state and replace callbacks without
  deadlocking. Callback replacement shares the same protected state as DSP,
  lifecycle, mode/profile, polarity, and retained image captures.

### Changed
- **Checked image-decoder ownership (#61)** — both decoders now conform to
  checked `Sendable`, reducing unchecked declarations from 32 to 30. Immutable
  image/status effects cross the lock boundary; slant/phase re-rendering still
  works outside the lock on a capture snapshot. Wire formats and RF paths are
  unchanged.

### Validation
- All 1,015 tests pass with two intentional skips and no failures. Debug and
  Release app builds, the repository audit, and the signed Release launch
  smoke pass. The performance smoke completes in 9 seconds against a 30-second
  limit.
- Generated fixtures cover all SSTV modes and WEFAX profiles, manual starts,
  polarity, retained-image corrections, and session completion/failure.
- Callback reentry checks and 2,000 concurrent feed, lifecycle, configuration,
  capture, and handler-replacement operations per decoder pass under Thread
  Sanitizer without race reports. No live radio or RF validation was performed
  for this software-only change.

## [2026.0903_001] — 2026-09-03

### Fixed
- **Click on return to receive** — fade RX/sub audio in over 20 ms after
  transmit, starting after the AGC's silent look-ahead prefix. Rekey still
  mutes immediately; CW sidetone, TX-monitor audio, and RF timing are unchanged.
- **Retained PureSignal trial verdict** — PA Linearity now keeps the last
  accepted/rejected IMD comparison and capture-quality measurements separate
  from the current candidate status. Later feedback can no longer hide the
  reason a trial automatically unkeyed and returned to bypass. Its Capture
  and Trial LUT controls also return to idle eligibility after unkey by
  consuming the newly published TX flags instead of their previous values.
- **Choppy CW sidetone** — bridge the packet-clock keyer into block-based
  speaker playback with a 64 ms cushion, preserve short dits and queued rekey
  tails, and disable audio latency trimming through the last CW sample.
  Independent CW and native-digital continuity owners prevent one source's
  completion from releasing the other's protection. RF timing is unchanged.
  Start the cushion at the first produced audio block so SquareSDR's 63 ms
  Protocol 1 preload cannot consume it before the tone begins.

### Changed
- **Menus organized by operating task (#73)** — Radio, Transmit, Decode, Log, and
  Station give every instrument a primary home. Window now contains native
  window management and the open-window list. File exposes IQ/audio recording
  and waterfall capture; View exposes display controls. Settings (⌘,) and RX
  EQ open shared dedicated surfaces, and Help keeps documentation, issue
  reporting, and Ask The Crab. Multimeter retains ⌘⇧M.
- **Checked wideband-spectrum ownership (#61)** — `WidebandSpectrum` now
  protects its vDSP setup handle, reusable FFT buffers, smoothed output,
  callback, and row-rate gate behind one compiler-visible unfair-lock state.
  Concurrent processing is serialized and row callbacks execute only after
  unlocking, reducing unchecked-Sendable declarations from 33 to 32.

### Validation
- All 1,009 tests pass with two intentional skips. Signed Debug and Release
  builds, strict signature verification, the optimized launch smoke,
  repository audit, and performance benchmark pass.
- The menu inventory checks every existing instrument has one primary menu
  home. Native app checks cover the complete menu bar, the shortened Window
  menu, Settings, RX EQ, recording availability, and the Multimeter shortcut.
- CW regressions cover Protocol 1 preload, Protocol 2 packet cadence, short
  dits, rekeys, backlog preservation, and overlapping continuity owners.
  On an ANAN ANT1 dummy load at 14.074 MHz / 3% drive, the operator confirmed
  clean headphone sidetone. SquareSDR captures retain continuous TEST marks;
  the operator approved the receive-return fade preview. No RF timing changed.
- An ANAN dummy-load PureSignal trial measured 49.6 → 49.5 dBc IMD3 and
  correctly unkeyed/bypassed below the +1 dB improvement gate. The verdict
  survives candidate updates, disarm, and Capture off; controls become
  eligible again after unkey. No PA linearity improvement is claimed.
- Wideband tone placement and concurrent process/configuration stress pass
  under Thread Sanitizer. A receive-only ANAN probe assembled three complete
  wideband frames; its 384/768/1536 kHz matrix reported zero gaps, missing
  packets, duplicates, or reordering and ended at RUN=0.

## [2026.0825_005] — 2026-08-25

### Added
- **Deterministic 2G-ALE calling laboratory (#72)** — the default-off ALE
  software surface now drives the pure controller through a complete accepted
  call/response/acknowledgment sequence or a disarmed authorization refusal.
  It displays the final controller phase and a bounded 24-line scan,
  authorization, frame, exchange, release, and refusal log. Local value events
  supply every grant, completion, and remote response; the laboratory has no
  engine, socket, radio, MOX, or coordinator instance and cannot produce RF.

### Changed
- **Checked RTTY decoder ownership (#61)** — `RTTYDecoder` now keeps its
  callback, configuration, UART, detector, AFC, quality, and session state in
  one compiler-visible unfair lock. Text and decoder-status effects leave only
  after unlocking, reducing unchecked declarations from 34 to 33.
- **Narrow Ask The Crab state surface (#60)** — the chat window now observes
  `AIAssistant`, a settings-only `CrabPresentationModel`, and `SkinCenter`
  instead of the full `RadioState`. Direct facade-observing view files fall
  from 7 to 6 without changing provider, Keychain, voice, co-host, or tool
  behavior.

### Validation
- Accepted and refused ALE laboratory exercises are deterministic; the
  accepted trace reaches linked state and requests the third-way
  acknowledgment, while refusal restores scanning without beginning a
  waveform. Source guards keep the controller/laboratory free of physical RF
  dependencies.
- All configurable RTTY fixtures pass unchanged. A checked-Sendable compile
  guard and 2,000-operation concurrent lifecycle, feed, recenter,
  configuration, meter, and callback-replacement stress cover the new lock
  boundary, including a focused Thread Sanitizer run. The complete 997-test
  suite, repository/concurrency audits, and unsigned Debug and Release app
  builds pass. No physical radio was accessed or keyed.

## [2026.0825_004] — 2026-08-25

### Added
- **Software-only 2G-ALE calling control plane (#72)** — a pure controller now
  composes scan ownership, coordinator-gated calling, complete decoded
  exchanges, bounded retries, refusal, cancellation, termination, and exact
  disconnect/protection teardown. The production decoder emits complete burst
  snapshots after unlocking; receive-side summaries and the controller's
  semantic input share the same exchange assembler. The controller has no
  engine, socket, MOX, radio, or coordinator reference, so this batch cannot
  produce RF.

### Changed
- **Checked CW decoder ownership (#61)** — `CWDecoder` now keeps callbacks and
  all mutable capture, timing, adaptive-threshold, symbol, and speed state in
  one compiler-visible unfair lock. Callback and decoder-status effects leave
  only after unlocking, reducing unchecked declarations from 35 to 34.
- **Narrow RF Vision state surface (#60)** — the overlay, live-region panel,
  rows, and context actions now observe `RFVisionPresentationModel` rather
  than the full `RadioState`. Geometry, classifier results, replay readiness,
  skin, and arcade updates are limited to that adapter; mutations retain the
  existing weak facade action paths. Direct facade-observing view files fall
  from 8 to 7.

### Validation
- Generated accepted-response audio passes through the production 8-FSK/FEC
  decoder's burst boundary and drives the caller to request its third-way
  acknowledgment. Deterministic tests cover scan suspension/restoration,
  malformed bursts, linked termination, refusal, exact-once forced teardown,
  and retry elimination after protection or disconnect.
- Checked-Sendable compile guards and 2,000-operation concurrent lifecycle,
  feed, and callback-replacement stress cover both ALE and CW decoders. Focused
  Thread Sanitizer, the full unit suite, repository audits, and unsigned Debug
  and Release app builds pass; no physical radio was accessed or keyed.

## [2026.0825_003] — 2026-08-25

### Added
- **2G-ALE receive/exchange foundation (#72)** — a pure burst assembler now
  reconstructs extended TO/TIS/TWAS/FROM address groups, validates duplicate
  called-address conclusions, and reports accepted or rejected handshakes.
  Scan/call arbitration suspends scanning before a call and restores the prior
  preference after teardown. The ALE window also exposes an explicitly gated,
  default-off software frame preview that cannot ARM, key, or reach a radio.

### Changed
- **Checked ALE decoder ownership (#61)** — `ALEDecoder` now keeps callbacks,
  capture, timing recovery, FEC ring, and session state in one compiler-visible
  unfair lock and is checked `Sendable`. Immutable callbacks and status effects
  run only after the lock is released, reducing the unchecked inventory from
  36 to 35 declarations.
- **Narrow ALE and Weather Fax state surfaces (#60)** — the remaining decoder
  window file now observes feature-specific presentation models and
  `SkinCenter`, not `RadioState`. CW and RTTY were already narrow; ALE and
  Weather Fax complete this decoder slice and reduce direct facade-observing
  view files from 9 to 8.

### Validation
- A complete generated ALE call waveform passes through the production
  demodulator/FEC decoder and exchange assembler. Additional tests cover
  extended addresses, mismatched conclusions, scan suspension/restoration,
  and the rule that monitoring alone never enters calling state.
- A checked-Sendable guard and 2,000-operation concurrent feed/reset/configure
  stress cover the ALE decoder, including a focused Thread Sanitizer run.
  Unsigned Debug and Release app builds succeed; no physical radio was accessed
  or keyed for this batch.

## [2026.0825_002] — 2026-08-25

### Added
- **2G-ALE caller foundation (#72)** — pure MIL-STD-188-141B call, response,
  acknowledgment, rejection, and termination frames now reuse the existing
  exact Golay/interleave encoder and continuous-phase 8-FSK modem. A caller
  state machine handles authorization, response deadlines, bounded retries,
  rejection, cancellation, and teardown through typed TXCoordinator actions.
  A coordinator-backed virtual-radio harness makes physical RF unreachable.

### Changed
- **Checked FT8 slot ownership (#61)** — `FT8SpotEngine` now carries all
  mutable capture/configuration/callback state inside one compiler-visible
  lock and is checked `Sendable`. Status and decode callbacks execute after
  unlocking, and UTC slot labels no longer share a mutable formatter.
- **Narrow FT8 and SSTV state surfaces (#60)** — both leaf views now observe
  feature-specific presentation models instead of the full `RadioState`.
  Decoder, export, tuning, correction, and digital-TX mutations continue
  through weak facade actions; SSTV skin updates come from `SkinCenter`.

### Validation
- Standard-frame tests cover extended addresses, TO/TIS/TWAS framing, exact
  147-bit word-to-tribit conversion, and per-symbol 8-FSK demodulation.
  Lifecycle tests cover successful three-way handshakes, busy/reject, no-
  response retry exhaustion, stale/duplicate input, cancellation, exact-once
  release, forced reset, coordinator refusal, and virtual RF teardown.
- The checked-Sendable FT8 boundary passes concurrent configuration/feed
  stress. Unsigned Debug and Release app builds succeed with both narrow
  views; no physical radio was accessed or keyed for this batch.

## [2026.0825_001] — 2026-08-25

### Fixed
- **OmniSkimmer tune accessibility (#39)** — live list rows and waterfall
  labels are real plain-style buttons instead of mouse-only tap gestures.
  VoiceOver and keyboard automation now receive one stable tune target with
  decoded text, mode, frequency, signal level, speed where available, and an
  explicit VFO-A action hint.

### Added
- **Measured ANAN PA-feedback latency segment (#25)** — TX Latency Map now
  consumes an already-retained PureSignal analysis and displays the physical
  DAC-reference-to-coupled-PA-feedback skew, sample rate, and correlation.
  The latency window remains read-only and cannot enable capture, ARM, or PTT;
  this bounded segment is explicitly not presented as microphone-to-PA
  end-to-end latency.
- **Release-aware website updater** — `tools/update-website-release.sh` reads
  the immutable GitHub release metadata, updates the hermitsdr.com release
  card through the authorized server path, retains a timestamped backup, and
  verifies the live HTTPS version and DMG link. A dry-run shows the exact
  change without touching the server.

### Validation
- **Native FT8/FT4 TX closure (#69)** — retained WSJT-X audio from the fresh
  post-clock-fix ANAN ANT1 dummy-load cycle independently decoded
  `CQ WU1T FN42` at 34 dB, DT 0.1, and 1500 Hz with WSJT-X's bundled decoder.
  The issue is closed; the separately gated first on-air contact remains #9.
- A live receive-only ANAN session sustained Protocol 2 at 1.536 MHz with
  4096 skimmer channels, approximately 7,260 packets/s, 10.48 MB/s, and no
  displayed sequence errors. W3LPL supplied real DX spots; three forced local
  disconnect/reconnect cycles each recovered, parsed fresh traffic, and reset
  the reconnect delay. No RF was transmitted.
- The full suite passes 961 tests with two intentional skips and zero
  failures. Unsigned Debug and Release app builds, the repository audit, and
  every release benchmark gate pass; the benchmark smoke run finishes in
  9 seconds against its 30-second budget. The website updater dry-run changes
  only the release metadata and leaves the server untouched.

## [2026.0824_010] — 2026-08-24

### Fixed
- **High-rate main-RX fidelity (#11, #61)** — the bounded socket handoff now
  coalesces packet-sized IQ into approximately 5 ms batches before invoking
  RXChain and its fan-out. At 1.536 MHz this replaces 6,453 DSP dispatches per
  second with about 202 ordered batches, while eight reusable slots preserve
  bounded drop-newest backpressure and leave the protocol/control queue free.

### Changed
- **Narrow OmniSkimmer surfaces (#60)** — the panel, rows, and waterfall
  labels now observe a skimmer-only presentation model plus `SkinCenter`.
  Spot/stat cadence no longer gives those leaves a broad `RadioState`
  subscription; tune, ignore, and enable operations cross weak actions.
- **Ingress performance gate** — the release benchmark now measures a full
  thirty-two-packet 1.536 MHz enqueue/drain cycle, and the focused TSan stress
  overlaps 16,000 packet pushes with the serial consumer.

### Validation
- The first `_009` live receive-only pass proved the socket boundary—739,774
  Protocol 2 decodes had zero packet drops—but also exposed 360,621 bounded
  RX-DSP frame drops because packet-sized RXChain calls could not keep up.
  The radio was disarmed throughout and left at RUN=0.
- After batching, the release ingress cycle measures 63.166 µs p99 against a
  5 ms deadline with zero retained allocator growth; all 31 release scenarios
  meet their deadlines. Functional and focused TSan ingress stress pass with
  zero loss or data races.
- A signed optimized app then completed the receive-only 384/768/1536 kHz
  ANAN matrix with TX disarmed. At 1.536 MHz its diagnostics recorded 516,756
  Protocol 2 decodes and 99,252 RX-DSP batches with zero drops; RX DSP averaged
  64.3 µs and peaked at 4.478 ms inside the 5 ms budget. The unoptimized Debug
  app still sheds bounded work at this rate, as expected for `-Onone`. The
  radio was disconnected cleanly and no RF was transmitted.

## [2026.0824_009] — 2026-08-24

### Fixed
- **Bounded live-IQ processing handoff (#11, #61)** — main-receiver DSP,
  recording, DVR, remote relay, skimmer, and time-shift work now leave the
  protocol socket/control queue through 64 reusable frame slots. Overload
  drops the newest frame and increments the RX-DSP diagnostic instead of
  allowing high-rate Protocol 2 traffic to fill the kernel receive buffer.
- **Remote listener Swift 6 ownership warning (#61)** — new connections are
  accepted directly on the queue already supplied to `NWListener`, removing
  a redundant hop and its concurrently captured weak reference.
- **Modern IPv4 decoding** — UDP display addresses and both protocol hostname
  resolvers truncate their fixed C buffers at NUL and decode UTF-8 explicitly,
  replacing Swift 6.2's deprecated array-based C-string initializer.

### Changed
- **Narrow TX Meters state surface (#60)** — the floating TX instrument now
  observes a TX-lifecycle/telemetry snapshot, its existing `MeterState`, and
  `SkinCenter`; unrelated receiver, decoder, CAT, waterfall, and integration
  publications no longer invalidate the window.

### Validation
- A deterministic two-slot ingress test stalls the consumer, fills the bound,
  verifies newest-frame rejection and RX/IQ ordering, then proves clean drain
  and frame-size recovery. The signed Debug macOS app builds successfully
  with the new handoff and no new unchecked-Sendable declaration; the former
  remote capture and three deprecated address-decoding warnings are absent.
  The complete Swift suite passes all 956 tests (2 opt-in skips).

## [2026.0824_008] — 2026-08-24

### Added
- **Receive-only Protocol 2 high-rate probe (#11)** —
  `tools/p2_rx_rate_test.py` refuses a busy radio, measures 384/768/1536 kHz
  packet cadence and sequence continuity independently of app DSP, and leaves
  the radio at RUN=0 without ever enabling PA, drive, MOX, or PTT.
- **WSJT-X saved-slot diagnostic (#69)** — the digital-mode guide now shows
  how to run WSJT-X's bundled decoder against its own saved WAV, separating a
  live scheduler/display miss from virtual-audio or waveform loss.

### Changed
- **Wideband callback ownership (#61)** — bandscope callback replacement and
  row-rate state now share the existing configuration lock. The connection
  queue invokes an immutable callback snapshot after unlocking, with a
  concurrent replacement regression covering the boundary.

### Validation
- The ANAN-7000DLE MkII receive-only probe on ANT2 delivered 1,613.6,
  3,226.7, and 6,453.7 packets/s at 384, 768, and 1536 kHz respectively,
  with zero gaps, missing packets, duplicates, or reordering. The full-rate
  stream carried 9.32 MB/s and the radio finished at RUN=0. This isolates the
  unoptimized app's high-rate UDP drops to synchronous DSP backpressure rather
  than the radio, LAN, or macOS UDP stack.
- In the approved post-2026.0824_007 dummy-load cycle, WSJT-X saved the exact
  20:40:30 UTC input but skipped it in the live table. Its bundled `jt9` at
  default depth decoded that saved WAV as `CQ WU1T FN42`, 34 dB, DT 0.1, and
  1500 Hz. The frame and virtual-audio path are valid; separately gated on-air
  validation remains.

## [2026.0824_007] — 2026-08-24

### Fixed
- **End-to-end native FT8 monitor continuity (#69)** — timed digital audio
  now holds a no-trim lease through both the TX-monitor FIFO and the final
  CoreAudio output ring. Returning to ordinary voice mode captures the exact
  downstream write boundary, so an already-queued FT8/FT4 tail is played
  intact before gentle voice drift correction resumes. The output ring grows
  from about 2.7 to 5.5 seconds to absorb the measured ANAN packet/audio clock
  lead without overflow.
- **Testable real-time output ring** — the lock-free ring is now a standalone
  DSP source with regression coverage for continuity-mode startup, queued-tail
  preservation, return to voice trimming, and a complete `CQ WU1T FN42`
  decode while the producer runs 11% ahead of the consumer.

### Validation
- One explicitly approved ANAN-7000DLE MkII cycle used 14.074 MHz USB, TX
  ANT1 into the 1500 W dummy load, 3% drive, the 3.1:1 SWR guard, and TX
  Monitor at 59%. It keyed for one native FT8 CQ, stopped before the next
  slot, returned CAT PTT 0, and finished disarmed with native TX disabled.
- The independent 62.35-second BlackHole capture carried the keyed frame at
  -18.5 dBFS mean / -8.9 dBFS peak instead of digital zero, but neither live
  WSJT-X nor eight offline `jt9` timing offsets decoded it. Costas timing
  isolated the remaining defect: nominal 160 ms symbols contracted from about
  156 ms at the first sync block to 147/145 ms at the middle/final blocks,
  matching repeated 64-sample drift trims in the downstream output ring.
  Issue #69 remains open for a fresh post-fix dummy-load decode and its
  separately authorized on-air validation; this batch itself performs no
  additional RF test.

## [2026.0824_006] — 2026-08-24

### Changed
- **Native FT8 external-loopback guidance (#69)** — the ENABLE TX help and
  digital-mode guide now state that TX Controls › Monitor must be on for
  WSJT-X to hear HermitSDR's generated frame through BlackHole. The ordinary
  RX mix is intentionally silenced while keyed; the processed-TX monitor is
  the separate post-mute path used for this validation.

### Validation
- One explicitly approved native FT8 cycle on the ANAN-7000DLE MkII used
  14.074 MHz USB, TX ANT1 into the 1500 W dummy load, 3% drive, and the 3.1:1
  SWR guard. The complete frame keyed/unkeyed cleanly, the sequencer stopped
  before its next slot, CAT returned PTT 0, and the radio finished disarmed
  with native TX disabled. A simultaneous 35.84-second BlackHole recording
  measured -47.0 dBFS mean / -31.0 dBFS peak during receive, then exact
  digital zero from 26.457 seconds onward at key-down because TX Monitor was
  off. Issue #69 remains open for one separately approved repeat with TX
  Monitor on and for the separately gated on-air validation.

## [2026.0824_005] — 2026-08-24

### Fixed
- **Digital-mode receive-route readiness (#69)** — Tools ▸ Digital Mode
  Check now fails explicitly when RX mute or zero receive volume would send
  digital zero to BlackHole/WSJT-X, reports a missing saved output device, and
  warns when the system-default route must be verified manually. The checks
  refresh immediately when the route, mute, or volume changes.

### Validation
- Off-air probes isolated the previous BlackHole silence to persisted RX mute:
  the pre-output DSP stream measured -28.3 dBFS RMS and the render queue was
  healthy while mixer and BlackHole captures were exact zero. After unmuting
  at 51%, an independent five-second BlackHole capture measured -39.6 dBFS RMS
  and -24.8 dBFS peak. No radio was armed or keyed.

## [2026.0824_004] — 2026-08-24

### Added
- **Selectable CoreAudio TX-latency loopback (#25 Phase 2)** — Tools ▸ TX
  Latency Map can now play the bounded 80 ms probe to an explicit output,
  capture an explicit input/channel, and run 3–10 host-clock-aligned trials.
  BlackHole and physical-cable routes are supported; device names/UIDs and
  channel are preserved in schema-v2 JSON, CSV, and Markdown while schema-v1
  results remain readable. Calibration remains visible and raw observations
  are never replaced. The independent session requests microphone permission
  only on Run, refuses to start while ARM/key/tune/two-tone is active, tears
  down both engines on cancel/close, and has no radio/PTT/TXChain dependency.
- **Independent ALE recording gate (#35)** — an opt-in
  `HERMITSDR_ALE_FIXTURE` test loads a genuine external receiver recording
  through CoreAudio, down-samples it to the decoder contract, and requires a
  sustained GPR/KQ6XA/AMD word stream. The third-party WAV is not copied into
  the repository.

### Changed
- **Checked-Sendable IQ replay owner (#61)** — `IQFilePlayer` no longer makes
  a class-wide unchecked promise. Its timer, callback, and closed flag share
  one compiler-visible protected state; callbacks run after that lock is
  released, duplicate starts are harmless, and stop atomically hands file
  closure to the dispatch-source cancel boundary. The unchecked inventory
  falls from 38 to 37 declarations.

### Validation
- The independently produced 16-second HFLINK/PCALE recording decodes repeated
  GPR calls, KQ6XA, position/data words, and the sustained AMD suffix
  `ERYTHING FINE HERE NOW`. Focused ALE, latency, replay lifecycle, callback
  replacement, and seek tests pass. No third-party audio is redistributed.
- Five live BlackHole 2ch output-to-input trials complete with 1.00 confidence,
  a 0.00 ms median, and 0.00 ms jitter, as expected for the same virtual
  device. The first two runtime attempts exposed and fixed main-actor executor
  traps in AVFAudio completion/tap callbacks; playback now uses no completion
  closure and the capture callback is created from a nonisolated checked-
  Sendable processor.
- One post-fix native FT8 cycle on the ANAN-7000DLE MkII used 14.074 MHz USB,
  TX ANT1 into the confirmed 1500 W dummy load, 3% drive, and the 3.1:1 SWR
  guard. RF keyed/unkeyed cleanly and HermitSDR decoded its own
  `CQ WU1T FN42` at 1500 Hz. WSJT-X could not provide the independent decode:
  after the debug-app restart HermitSDR's selected BlackHole output delivered
  digital zero, confirmed by a separate four-second CoreAudio capture. The
  radio finished with native TX disabled, ARM off, and PTT/Tune/Two-tone off;
  ANT2 was never selected. Issue #69 remains open for the external decode and
  separately gated on-air validation.

## [2026.0824_003] — 2026-08-24

### Fixed
- **Native FT8/FT4 monitor continuity (#69)** — native data monitoring now
  primes a 100 ms cushion and preserves every queued sample instead of using
  the voice monitor's deliberate retain-newest latency trim. Temporary
  producer/consumer clock backlog can no longer delete symbols from the
  BlackHole/WSJT-X feed; already-queued digital tail samples also survive the
  transition back to ordinary mic monitoring. Voice monitoring keeps its
  established low-latency trim policy.
- **Standards-correct 2G-ALE Golay words (#35)** — ALE now uses the exact
  MIL-STD-188-141 systematic `[W|G]` generator matrix rather than the former
  provisional cyclic approximation, corrects any combination of up to three
  errors across the complete 24-bit word, rejects four-error fixtures, and
  applies the mandated inversion to the second transmitted word's twelve
  check bits. Published figure and on-wire frame vectors lock the convention.

### Added
- **TX audio-loopback measurement core (#25 Phase 2)** — a deterministic,
  bounded 80 ms chirp and normalized correlator recover integer and
  sub-sample delays despite gain, clipping, polarity reversal, and noise.
  Repeated-trial summaries retain raw observations, reject outliers with MAD,
  keep calibration explicit, and export versioned JSON, CSV, or Markdown.
  This is the non-RF analysis core; CoreAudio device capture remains a later
  integration step and results are never labeled microphone-to-PA latency.

### Validation
- **ANAN dummy-load diagnosis** — two explicitly approved native FT8 cycles on
  the ANAN-7000DLE MkII used 14.074 MHz USB, TX ANT1 into the 1500 W dummy
  load, 3% drive, and the 3.1:1 SWR guard. RF keyed and unkeyed cleanly and the
  native receiver displayed `CQ WU1T FN42` at the intended 1500 Hz offset, but
  WSJT-X rejected the virtual-audio copy. A simultaneous BlackHole capture was
  unclipped yet undecodable and showed missing monitor timing; the production
  post-DSP waveform decoded cleanly before that queue. New tests reproduce a
  backlog more than ten times the former trim threshold and prove the complete
  message remains decodable. One fresh cycle with this rebuilt version remains
  required before closing #69 milestone 4; the radio finished disarmed.
- **Software-only ALE and latency gates** — official ALE vectors plus
  exhaustive one- and two-bit correction positions pass without a radio.
  Loopback fixtures cover exact/fractional delay, clipping, polarity, noise
  rejection, outlier classification, calibration visibility, and export
  round-tripping. No RF was keyed for either addition.

## [2026.0824_002] — 2026-08-24

### Added
- **Native FT8/FT4 TX integration (#69 milestone 3)** — the FT8 panel can
  call CQ or reply to a decoded CQ through the production modulator and pure
  auto-sequencer. UTC slot-clock keying requests the central TXCoordinator as
  a system-owned Digital transmission, temporarily applies the
  processor-enforced Digital profile, paces the waveform through TXChain, and
  logs completed QSOs through the existing QSOLog/ADIF path. Station identity
  is shared with PSKReporter and the logbook rather than duplicated.
- **Explicit native-data safety controls** — ENABLE TX never persists and is
  unavailable until ARM; connected/live/USB/policy/interlock gates are
  rechecked before each coordinator request. STOP, disarm, protection,
  disconnect, and a bounded slot watchdog all use the coordinator's release or
  forced-unkey paths with exactly-once release coverage. Replay decodes cannot
  advance the live sequencer.

### Fixed
- **Exclusive FT8 program ownership** — the native data lease is now enforced
  under TXChain's DSP-owner lock as well as at the mic/file callback boundary,
  closing a race where an already in-flight voice block could cross the
  ownership change immediately before key-down. The lease and Digital profile
  now remain active through the RF-hot drain tail, and native data suppresses
  any saved voice roger beep.
- **FT4 passband/protocol edges** — the tone-zero offset now tops out at
  2.8 kHz so all eight FT4 tones remain inside the 3 kHz Digital channel, and
  replying to a decoded row explicitly selects that row's FT8 or FT4 clock.

### Validation
- **Software-only gate** — 20 focused controller/integration tests cover slot
  geometry, coordinator refusal, watchdogs, aborts, QSO flow, and exclusive
  program audio. No radio was keyed for this batch; issue #69 milestone 4
  retains the operator-approved dummy-load and on-air validation.

## [2026.0824_001] — 2026-08-24

### Fixed
- **About version label** — Help ▸ About now shows only the public HermitSDR
  version and no longer appends the internal bundle build number. The build
  identifier remains available in Copy System Information for diagnostics.

## [2026.0820_003] — 2026-08-20

### Added
- **The Colony** — a physarum simulation living on the waterfall. A few
  hundred thousand GPU agents (65k/262k/524k by resource preset) feed on
  the live spectrum: signals become food sources, glowing filament
  networks grow between active stations, and a dead band starves the
  colony until its trails fade. Entirely Metal compute on the existing
  draw clock (seed/update/diffuse kernels + an additive composite
  colored through the active palette, EDR-aware); the CPU never meets a
  single agent. Trail space is texture space, so zoom/pan apply for
  free. "Colony" toggle beside CRT Glass and Arcade FX, off by default;
  buffers are freed the moment it's switched off.
- **Band Geology** — Tools ▸ Band Geology compresses up to 48 hours of
  band activity into sediment strata: one 512-bin layer per minute
  (max-pooled, averaged, persisted across launches), rendered in a
  rock-toned LUT where band openings read as ore veins. Retunes draw
  fault lines; decoder bookmarks fossilize as kind-colored glyphs in
  the layer where they happened; a gutter shows Band DVR shelf
  coverage, and clicking a covered layer replays that minute through
  the production chain. The strata tee rides the existing spectrum row
  path, live-only, and costs a bounded max-pool per row.

## [2026.0820_002] — 2026-08-20

### Added
- **DVR timeline bookmark markers (#71 remainder)** — decoder bookmarks
  (the same events the time machine pins) now draw as indigo ticks on the
  Band DVR's wall-clock timeline, refreshed live as sessions complete.
  Clicking a marker replays that moment; the timeline model already
  computed the positions, so this closes the one cosmetic remainder from
  the DVR ship.

## [2026.0820_001] — 2026-08-20

### Added
- **Hermit Remote Phase 1 (#66, `docs/RemoteOperation.md`)** — operate the
  shack away from the shack: a second HermitSDR connects over an
  authenticated, encrypted link and becomes a full receive-only receiver
  (its own waterfall, DSP chain, and decoders) fed by relayed IQ.
  - **Wire protocol v1** (`Integration/Remote/RemoteWireProtocol.swift`,
    pure + package-tested): big-endian TLV frames
    (HELLO/CHALLENGE/AUTH/WELCOME/DENIED · TUNE/RATE/GAIN ·
    IQ/STATE/METER/BYE) with an incremental bounded parser,
    HMAC-SHA256 challenge/response (the pairing token never crosses the
    wire; the answer binds the HELLO+CHALLENGE transcript), float32↔int16
    IQ conversion (vDSP, >80 dB round-trip pinned), pure auth state
    machines for BOTH roles, the /2-reachable relay-rate plan, base32
    pairing codes, and the self-signed P-256 certificate builder. **The
    protocol has no transmit opcodes — absent, not refused** (test-pinned
    against enum drift).
  - **Shack server** (`Integration/Remote/RemoteAccessServer.swift`):
    NWListener + TLS with a Keychain-stored self-signed identity minted at
    first enable (SHA-256 fingerprint + pairing code shown in the gear
    popover's new Remote Access section, with copy buttons, connected-client
    name, and a kick button). One authenticated client in v1 (second connect
    is DENIED busy; three auth failures per address earn a 60 s cooldown).
    Inbound TUNE/GAIN hop to the main actor and drive the same
    RadioState entry points the UI uses; RATE retargets only the relay
    decimator — the radio keeps streaming at its own full rate. IQ tees
    live-only and generation-gated in `RadioEngine.rewireIQ` beside the DVR
    tee, decimates full-rate→relay-rate (default 96 k, cap 192 k) on the
    server's own queue, and drops frames under send backpressure (bounded
    in-flight, never blocking the radio path; drops surface as sequence
    gaps). STATE mirrors center/rate/gain changes, METER rides the 10 Hz
    S-meter tick, and the server advertises `_hermitsdr-remote._tcp` while
    enabled. The enable is persisted, but the listener binds only while a
    radio session is active.
  - **Remote client** (`Protocol/HermitRemoteConnection.swift`): an
    `HPSDRLink` whose radio is the shack. Certificate pinning
    (trust-on-first-use, exact match thereafter), Keychain pairing token
    read only at connect, relayed IQ through the standard `onIQ` seam with
    UDP-style sequence-gap accounting, and a **receive-only RadioProfile**
    (`.conservativeUnknown`, TX ceiling 0 Hz, one receiver) so the existing
    profile machinery keeps every TX/PA/Alex path closed — the entire TX
    surface is empty no-ops on a protocol that couldn't carry them anyway.
  - **Connect sheet**: a Remote HermitSDR section listing
    Bonjour-discovered shacks plus a manual host:port field; first contact
    runs the pairing sheet (code entry + fingerprint pinning), then the
    normal connect flow.

### Added
- **Multi-band Super-Skimmer (#70)** — the ANAN's spare DDCs (4–7 on an
  Orion MkII) become independent receive-only **monitor receivers**, each
  parked on a band's standard FT8 sub-band at 48 kHz and feeding its own
  slim decode chain + FT8 decoder: simultaneous FT8 spotting on up to four
  extra bands, every spot stamped with its own monitor's carrier and fed to
  PSKReporter and the heard map (never the main waterfall/FT8 log — those
  belong to the main receiver's band). Tools ▸ Super Skimmer window (narrow
  #60 presentation adapter): master enable, per-slot band picker over the
  standard FT8 frequencies, per-monitor rolling decodes/min + last-decode
  age, and a bounded recent-spot table; radios without spare DDCs (HL2) get
  a capability placeholder. Monitor NCO words ride every 100 ms
  High-Priority packet (bytes 25/29/33/37); enables apply via the
  measured-safe mid-RUN DDC-Specific resend. Monitors run only in the
  normal RX DDC branch — diversity and PureSignal capture suspend them and
  drop their in-flight packets until the mode ends. RECEIVE-ONLY by
  construction: no ARM/PTT/DUC surface anywhere in the monitor path, and no
  audio path (decode tap only). Config persists as one JSON key
  (`superSkimmerConfig`); wire bytes, suspension branches, port demux, and
  the pure model are pinned by `SuperSkimmerTests` against the virtual
  radio. See `docs/SuperSkimmer.md`; live-hardware validation (milestone 4)
  remains open.

## [2026.0819_007] — 2026-08-19

### Added
- **Band DVR (#71)** — continuous, bounded, disk-backed full-span IQ
  recording with a timeline and scrub-to-replay. While enabled and
  connected, live IQ tees into `Recording/DVRStore.swift`: standard
  `.hiq` segments in `~/Library/Application Support/HermitSDR/DVR/`,
  rolled at 300 s and at every center/rate change or stream restart (a
  `.hiq` carries exactly one center + rate), pruned oldest-first to the
  performance preset's new DVR disk budget (Conservative 2 GiB /
  Balanced 8 GiB / Maximum 32 GiB). Appends hop off the network thread
  behind a bounded pending counter (drop, never block); a failed disk
  write stops the DVR and surfaces why. Tools ▸ Band DVR (narrow #60
  presentation adapter) shows the shelf, a wall-clock timeline with
  gaps (`Recording/DVRTimeline.swift`, pure and fully unit-tested), and
  a per-segment list — click the timeline to replay that exact moment
  through the ordinary file-replay path via the new
  `IQFilePlayer.seek(toSampleOffset:)`/`positionSeconds`. Replay of a
  DVR segment never truncates it: disconnect only ends the recording
  session, segments stay on the shelf. Enable state persists
  (`dvrEnabled`) and the session resumes on the next connect.

### Added
- **Native FT8/FT4 TX core (#69, milestones 1–2)** — `TX/FT8Modulator.swift`
  exposes the vendored ft8_lib encoder (pack77 + CRC-14 + LDPC(174,91) +
  Costas + Gray) to Swift and synthesizes the WSJT-X GFSK waveform
  (BT = 2 Gaussian frequency pulse, continuous phase, raised-cosine key
  envelope). `TX/FT8Sequencer.swift` is the pure WSJT-X-style QSO state
  machine: answer-CQ and run-a-frequency flows, opposite-parity slot
  selection, bounded retries, single QSO-record emission, plus the
  standard-message parser and signed report formatting. Both are pure —
  no radio, coordinator, ARM, or key dependency; nothing here can reach
  RF. Round-trip pinned through the production slot decoder for FT8 and
  FT4, GFSK spectral containment pinned ≥35 dB at 150 Hz out, both QSO
  flows, retry exhaustion, RR73 repeat cap, and third-party rejection
  table-tested. TX integration (slot-clock keying through TXCoordinator,
  FT8 panel reply buttons) is milestone 3 and remains unwired; the
  README capability row intentionally still reads "no native FT8/FT4
  modulator" until transmission actually works end to end.

## [2026.0819_005] — 2026-08-19

### Fixed
- **Hermes-Lite 2 profile documentation (#68)** — the public discovery table
  now matches the shipped resolver: native Protocol 1 board 6 requires
  gateware 68+, while board-ID 1 Hermes emulation is accepted only when its
  extended discovery data carries HL2 build marker 2, 3, or 5. An ordinary
  Hermes reply remains conservatively receive-only.

### Tests
- Documentation consistency coverage rejects the obsolete gateware-75 HL2
  minimum so the safety-critical profile description cannot drift from the
  regression-tested resolver again.

## [2026.0819_004] — 2026-08-19

### Fixed
- **Developer ID-signed release DMGs** — the release pipeline now signs the
  outer disk-image container before notarization, protecting the complete
  drag-to-Applications layout as well as the app inside it. The post-staple
  signature and Gatekeeper checks now fail closed instead of allowing zsh's
  conditional-list behavior to hide a rejected DMG container.

### Tests
- Release-consistency coverage pins outer-DMG signing and the fail-closed
  Gatekeeper check. The published artifact is independently downloaded and
  checked for its SHA-256 digest, disk-image integrity, Developer ID signature,
  stapled notarization ticket, inner-app signature, and Gatekeeper acceptance.

## [2026.0819_003] — 2026-08-19

### Fixed
- **ANAN Protocol 2 connection ownership and control latency** — the discovery
  scanner now stops before the stream socket opens, and that socket sends the
  profile-required one-time discovery handshake before its first command. A
  failed connection restarts scanning instead of leaving the connect sheet
  inert. This prevents a scanner socket from competing with the active stream
  for the ANAN firmware's source-port ownership.
- **384 kHz dual-receiver packet loss and delayed relay/PTT commands** — RX2
  DSP now runs on a bounded serial worker instead of the Protocol 2 socket
  queue, and UDP receive draining yields after bounded batches so queued
  control-plane work cannot starve under sustained IQ load.

### Tests
- The virtual Protocol 2 radio now distinguishes discovery from General
  packets and proves that the stream socket discovers exactly once, before
  every command, with no discovery probes during keepalive.
- Receive-only hardware validation on the ANAN-7000DLE MkII (fw 2.2.10,
  169.254.76.129) sustained RX1+RX2 at 384 kHz at the expected 3,225 packets/s
  and 4.66 MB/s with zero sequence errors. RX ANT1→ANT2→ANT1 changes remained
  immediate under that load, with TX SAFE and no RF generated.
- All 848 SwiftPM tests pass with the one intentional benchmark skip; the
  Developer ID-signed Debug application also passes strict deep signature
  verification and reports version `2026.0819_003`.

## [2026.0819_002] — 2026-08-19

### Fixed
- **Hermes-Lite 2 discovery regression (#68)** — the reviewed Protocol 1
  profile now accepts the official 68p4 gateware family instead of requiring
  the later lab-radio version. HL2's board-ID 1 Hermes-emulation mode is also
  recognized from its extended build marker; an ordinary Hermes reply without
  that marker remains conservatively receive-only.
- **Named TX operate controls (#39)** — PTT, tune-carrier, and two-tone buttons
  now publish stable accessibility labels and keyed values instead of appearing
  as three anonymous buttons to assistive technology and UI test harnesses.

### Added
- **Gated PureSignal memoryless predistortion (#51 Phase 2)** — a valid,
  monotonic two-tone AM-AM/AM-PM measurement may build an immutable 65-node
  inverse LUT. Hard bypass remains the session default; an operator must
  explicitly enable Trial LUT while unkeyed, packet conversion clamps the wire
  envelope to 0.98, and a result that fails to improve RF-domain IMD by at
  least 1 dB automatically unkeys and restores bypass. Candidates and validation
  never persist across disconnects.

### Tests
- Added official HL2 68p4/native/emulation discovery fixtures, conservative
  unknown-Hermes coverage, foldback/correlation rejection, memoryless-PA error
  reduction, and hard wire-envelope bounds. All 848 SwiftPM tests pass with the
  one intentional benchmark skip; the Developer ID-signed Debug application
  also passes strict deep signature verification.

## [2026.0819_001] — 2026-08-19

### Changed
- **Powerwerx calibration record cleanup (#34)** — corrected obsolete Protocol
  2 source and project notes that still described an external DC-current
  measurement as pending. They now point to the retained, identity-bound
  2026-08-18 fixture and its 2.3 A trust floor. Telemetry math and runtime
  behavior are unchanged.

## [2026.0818_009] — 2026-08-18

### Changed
- **Narrow Multimeter ownership (#60)** — the standalone meter window now
  observes a scalar-only presentation snapshot of connection state, receiver
  gain, radio telemetry, and its six high-rate TX/RX meter inputs. Skin changes
  come from `SkinCenter`; decoder, waterfall, CAT, and integration churn no
  longer redraws the window. Direct facade-observing view files fall from 14
  to 13.
- **Checked IQ recorder concurrency (#61)** — the `.hiq` writer moves its file
  handle, interleaved buffer, completion flag, sample count, and failure state
  into one compiler-visible protected value. The unchecked-Sendable inventory
  falls from 36 to 35.

### Tests
- Added concurrent 16-writer append coverage, eight-way idempotent finish,
  exact file-size/progress assertions, late-write rejection, and source guards
  for both the narrow Multimeter boundary and checked recorder storage.

## [2026.0818_008] — 2026-08-18

### Added
- **Digital Mode Check (#66 milestone 4)** — a new Tools window converts the
  WSJT-X/fldigi contract into explicit pass, warning, and fail results for the
  resolved Digital profile, USB convention, audio-source availability, CAT
  listener health, loopback-only exposure, end-of-over audio, C-QUAM, and the
  safe local-check ARM state.
- **Reproducible local audio/CAT fixture** — private unkeyed production
  `TXChain` instances prove that hostile saved voice settings remain
  bit-identical under the Digital profile, measure 1500 Hz pass-through and
  4500 Hz rejection, and exercise the in-memory Hamlib capability, frequency,
  PKTUSB/passband, PTT set/read/release, and malformed-value contract.

### Safety
- The check window is read-only and the local fixture starts no TCP listener,
  installs no CAT callbacks, and has no RadioState, coordinator, connection,
  ARM, key, or RF path. A local pass is explicitly not presented as proof of
  virtual-audio routing or transmitted RF.

### Tests
- Added deterministic local-fixture, passband, profile-bypass, CAT-roundtrip,
  malformed-input, and source-boundary coverage. The signed Debug app builds
  with the narrow readiness adapter and no radio operation.

## [2026.0818_007] — 2026-08-18

### Added
- **Software-only TX Latency Map (#25 Phase 1)** — Tools now shows a live,
  read-only pipeline from the selected CoreAudio input through TXChain and the
  protocol packetizer. Every stage labels its delay as measured, calculated,
  device-reported, estimated, or unknown and separates observed CPU time from
  algorithmic, buffered, transport, and unobservable delay.
- The map includes CoreAudio latency/safety/buffer properties, the largest
  observed callback block, fixed RNNoise/filter/limiter/Hilbert delays, current
  TX I/Q queue depth, key-down prime, callback timing, and P1/P2 packetization.
  Network transit and radio DSP/DAC/PA remain explicitly unknown. Snapshots
  export as versioned JSON, CSV, or Markdown without captured audio.

### Safety
- The latency window has no ARM, PTT, key, test-signal, or protocol mutation
  control. It calls the component total diagnostic bookkeeping—not a physical
  microphone-to-PA measurement—because host buffers can overlap and the radio
  endpoint remains unobserved until later guarded loopback phases.

### Tests
- Added seven focused model, provenance, protocol-duration, optional-delay,
  unknown-boundary, and export/schema tests. The signed Debug app builds with
  the new narrow presentation adapter and window without connecting to or
  transmitting through a radio.

## [2026.0818_006] — 2026-08-18

### Added
- **Offline Stream Deck setup and MK.2 tile renderer (#52)** — Tools now opens
  a persistent 15-key layout editor with named pages, brightness, titles, SF
  Symbols/emoji, face colors, and curated band/mode/tuning/DSP/media/page
  assignments. The AppKit renderer produces cached 72×72 JPEG wire tiles with
  active, pressed, and live-value variants plus the MK.2's required 180°
  rotation; the editor previews those exact bytes in physical orientation.
- Stream Deck layouts now carry a version and normalize legacy/malformed
  documents safely: brightness clamps to the feature-report range, empty
  layouts gain a Main page, missing MK.2 keys become inert, and excess keys are
  retained for future larger models. Operator and safety notes live in
  `docs/StreamDeck.md`.

### Safety
- This slice is deliberately offline. The setup owner and view have no HID
  manager, radio facade, engine, coordinator, protocol connection, or action
  executor, so assigning PTT or TUNE cannot enumerate a device or key a radio.
  Device I/O, live lamps, action execution, and TX refusal/drop validation
  remain hardware-backed phases of #52.

### Tests
- Expanded Stream Deck coverage from six to nine focused tests with legacy-document
  migration, model normalization, face/color canonicalization, stable unique
  action presets, and page-action round trips. A source guard pins the offline
  control boundary; the complete suite passes with 829 tests (one skipped),
  and the Developer ID-signed Debug app builds and passes strict deep-signature
  verification without connecting to or transmitting through a radio.

## [2026.0818_005] — 2026-08-18

### Added
- **Hi-Fi SSB Profile Laboratory (#67)** — a standalone Tools window records a
  bounded ten-second microphone passage or imports up to thirty seconds of any
  CoreAudio-readable file, then renders the same DC-removed, repeatably
  normalized 48 kHz mono source through two selectable built-in SSB profiles.
  Original/A/B playback is active-RMS matched to prevent loudness bias, while
  the displayed measurements retain each profile's real gain behavior.
- The lab plots the production 513-tap passband plus voicing-EQ response and
  compares active RMS, peak, crest factor, central-99% occupied bandwidth,
  out-of-passband energy, ceiling activity, maximum compressor/limiter
  reduction, and warmth/body/presence/air energy balance.

### Safety
- The laboratory receives no `RadioState`, `RadioEngine`, `TXCoordinator`,
  protocol, network, ARM, or PTT dependency. Its private `TXChain` instances
  remain unkeyed, so recording, rendering, and playback cannot radiate.
  Baseband prediction is explicitly distinguished from RF/PA/antenna proof.

### Tests
- Added deterministic production-chain profile comparisons, normalization/DC
  removal and duration bounds, silence/finite-metric handling, loudness-match
  headroom, repeatability, profile containment, and wide-vs-normal-channel
  spectral regressions, plus a real 44.1 kHz stereo WAV resample/manual-downmix
  fixture.

## [2026.0818_004] — 2026-08-18

### Added
- **Sample-clock CAT Morse (#66)** — Hamlib `send_morse` / `b` and
  `stop_morse` now enter the same deterministic keyer and `TXCoordinator`
  boundary as local paddles. Text is pre-tokenized with exact element,
  character, and word spacing; the packet callback only advances fixed timing
  state. Messages are bounded to 256 bytes, cannot replace a keyboard/CAT
  owner, and stop safely when their CAT client disconnects.

### Changed
- **Narrow diagnostic-window ownership (#60)** — Performance Budget and PA
  Linearity now observe focused presentation adapters plus `SkinCenter`, not
  the root `RadioState`. Budget/configuration churn and paired-IQ analysis
  invalidate only their relevant windows, while PA Linearity retains a single
  guarded capture action and no ARM/PTT/drive/protocol surface. Direct facade-
  observing view files fall from 16 to 14.
- **Checked decoder status concurrency (#61)** — `DecoderStatusReporter`
  replaces its class-wide unchecked promise with compiler-visible protected
  session/callback state while preserving synchronous callbacks in exact state
  order. The audited unchecked inventory falls from 37 to 36 declarations.

### Tests
- Added exact automatic-message timing, weighting, punctuation, stop, source-
  collision, CAT ownership/disconnect, refusal, and coordinator-path coverage;
  ownership guards for both migrated windows; and a checked-Sendable reporter
  guard. The complete suite passes (817 tests, one skipped, zero failures),
  and the Developer ID-signed Debug app builds and passes strict signature
  verification without connecting to or transmitting through a radio.

## [2026.0818_003] — 2026-08-18

### Added
- **Production host-keyed CW bridge (#66)** — independently held keyboard dot
  and dash actions (default `[` / `]`) now enter the deterministic sample-clock
  keyer through the single `TXCoordinator`. Only an authorized CW generation
  can raise MOX; its exact raised-cosine envelope drives both the dial-frequency
  carrier and a separately mixed sidetone. Generic PTT retains its continuous
  CW-carrier fallback, and mode/focus/disconnect/watchdog/protection exits reset
  logical paddles without bypassing the normal RF tail/drop path.
- **Controlled AM hardware source (#38)** — the Protocol 2 dummy-load harness
  can now generate a production-level unmodulated AM carrier or repeatable
  symmetric AM tone, validate carrier/sideband shape in the radio's own-signal
  capture, summarize keyed voltage/current/power telemetry, and perform a
  best-effort PA/PTT/RUN hard-off on normal exit, exception, or interruption.

### Tests
- Added exact external-CW-envelope and generic-PTT-fallback coverage plus a
  forced-release regression requiring a genuine all-up paddle edge before
  reauthorization. The complete suite passes (806 tests, one skipped, zero
  failures), the AM harness compiles, and the Developer ID-signed Debug app
  builds and passes strict signature verification.
- Live ANAN-7000DLE MkII validation on ANT 1 into a 1500 W dummy load compared
  an eight-second 3.885 MHz AM carrier with the same carrier at 75% / 700 Hz
  modulation. The external Powerwerx analyzer held the same 13.54 V minimum
  in both cases (9.56 A / 129.4 W carrier; 9.32 A / 126.1 W modulated), while
  the radio reported 1.00–1.04 SWR, zero packet errors, and the own-signal
  capture verified symmetric sidebands. This exonerates modulation-related
  supply sag as the watery-audio mechanism in #38; the radio's internal
  voltage AIN remains too noisy to substitute for an external analyzer.

## [2026.0818_002] — 2026-08-18

### Added
- **Traceable PA-current calibration evidence (#34)** — the opt-in TX
  telemetry CSV now records the radio's smoothed raw PA-current detector count
  beside the existing converted amperage. The local rigctl calibration
  interface exposes the same count as `PA_CURRENT_RAW`, so an external DC
  power-analyzer observation can be paired with detector evidence during a
  deliberately operator-controlled dummy-load pulse.

### Fixed
- **ANAN low-end PA-current calibration (#34)** — three measurement levels
  across four six-second, zero-error dummy-load pulses on the ANAN-7000DLE
  MkII paired median raw AIN counts with a Powerwerx inline DC analyzer. After
  subtracting the measured
  1.00 A receive-idle baseline, the retained points are 96→2.75 A,
  326→7.14 A, and 767→15.44 A. Their affine fit
  (`A = 0.01889990567958 × count + 0.9526707157`) has 0.019 A RMS residual,
  exposes the real keyed PA-bias load, and agrees through ~62 W RF instead of
  hiding or substantially under-reporting it. The existing 2.3 A trust floor
  still suppresses the positive intercept while receiving.
- Untouched legacy Orion2 profiles carrying the exact former default are
  upgraded and saved on activation. Operator-measured or edited profiles are
  never overwritten.

### Tests
- Extended rigctl telemetry coverage to pin the raw current-detector command,
  including its unavailable default and stable one-decimal wire format.
- Added the identity/firmware/path-bound Powerwerx CSV fixture, fit residual
  regression, runtime conversion coverage, and guarded legacy-profile
  migration coverage. The complete suite passes (804 tests, one skipped,
  zero failures), and the Developer ID-signed Debug app passes strict
  signature verification.

## [2026.0818_001] — 2026-08-18

### Added
- **Virtual Media Deck completion (#24)** — pads may now hold local audio,
  the audio track of a movie, an authorized embedded YouTube player, or a
  normal web link. YouTube URLs are normalized behind a provider boundary,
  preserve optional start/end points, report preparing/buffering/playing/
  paused/completed/error state, and never download or extract media.
- Media Deck now has global pause/resume, a live output meter, an activity
  and queue popover with bounded error history, source badges, pad
  duplication, restored page selection, and a persisted always-on-top pin.

### Changed
- STOP ALL now leaves every interrupted or queued pad in an explicit stopped
  state. Web playback is deliberately system-output-only; radio transmission
  remains in TX Controls' File source so ARM, manual PTT, and all
  `TXCoordinator` interlocks cannot be bypassed by a soundboard pad.
- Added `docs/MediaDeck.md` as the operator and safety reference for local,
  YouTube, and open-URL sources, routing, keyboard controls, and deck files.

### Tests
- Added provider tests for YouTube watch/share/shorts/embed URLs, timestamp
  normalization, invalid/unsafe URLs, and generic links, plus document
  migration and playback-lifecycle coverage. The focused Media Deck suite
  now contains 36 passing tests. The complete suite passes (800 tests, one
  skipped, zero failures), as does the signed Debug app build.

## [2026.0817_018] — 2026-08-17

### Fixed
- **Keychain-free notarization on the self-hosted release runner** — the
  signed job failed at `notarytool store-credentials`, which insists on
  writing to the default keychain and a headless launchd runner session
  cannot unlock it. The workflow now materializes the App Store Connect API
  key as a file, and `tools/release.sh` / `tools/make-dmg.sh` pass
  `--key/--key-id/--issuer` directly when `NOTARY_KEY_PATH`,
  `NOTARY_KEY_ID`, and `NOTARY_ISSUER_ID` are set, falling back to the
  local `NOTARY_PROFILE` keychain profile otherwise. The `always()` cleanup
  step now also removes the materialized key and certificate files.

## [2026.0817_017] — 2026-08-17

### Changed
- **Fully self-hosted release pipeline** — the signed release job now runs on
  the repository's own Apple-silicon runner instead of GitHub's metered
  `macos-26` image, so publication can never be blocked by hosted-runner
  billing. The signing/notarization secrets originate from the same machine,
  so the move adds no new exposure. Because the runner is persistent, the job
  now ends with an `always()` cleanup step that restores the user keychain
  search list and deletes the ephemeral release keychain. The self-hosted
  runner requires `NODE_EXTRA_CA_CERTS` pointing at the local TLS-inspection
  root CA in its `.env`, or Node-based actions (artifact upload) fail with
  "self-signed certificate in certificate chain" while git operations
  succeed. The `release` environment's deployment policy now allows `main`
  and `v*` tags — "protected branches only" silently rejected the
  tag-triggered publish path. `docs/Release.md` records all three findings.

## [2026.0817_016] — 2026-08-17

### Changed
- **Narrow primary-frequency ownership (#60)** — the VFO digit readout and
  flywheel now observe `FrequencyPresentationModel` plus `SkinCenter`, not
  `RadioState`. The adapter publishes only current frequency and effective
  tune step; weak actions preserve the facade-owned clamping, replay, pan/NCO,
  CAT, persistence, and band-memory behavior. Auto-step derivation is shared
  with the facade, and direct facade-observing view files fall from 17 to 16.

### Tests
- Added a source-level ownership guard covering both frequency controls. The
  complete suite passes (794 tests, one skipped, zero failures), as does the
  signed Debug app build, without connecting to a radio.

## [2026.0817_015] — 2026-08-17

### Changed
- **Narrow Sub Receiver ownership (#60)** — the standalone RX2 panadapter now
  observes `SubReceiverPresentationModel` rather than `RadioState`. Live/idle
  state derives from session and recording owners; VFOs, span, and passband
  derive from typed receiver configuration; display limits retain narrow
  publications; the renderer stays engine-owned; and tune/enable operations
  cross weak actions. Direct facade-observing view files fall from 18 to 17.
- **Shared channel-passband derivation (#60)** — USB, LSB, and symmetric-mode
  filter offsets now belong to `ReceiverConfiguration`, removing duplicate
  edge calculations from both the Sub Receiver overlay and `RadioState`.

### Tests
- Added regression coverage for channel-passband orientation across every
  mode family and a source-level ownership guard for the Sub Receiver window.
  The complete suite passes (793 tests, one skipped, zero failures), as does
  the signed Debug app build, without connecting to a radio.

## [2026.0817_014] — 2026-08-17

### Changed
- **Narrow Diversity settings ownership (#60)** — the synchronized dual-ADC
  settings section now observes `DiversityPresentationModel` and `SkinCenter`
  rather than the broad `RadioState` facade. The adapter publishes only
  enable, gain, and phase; mutations retain the facade-owned sub-receiver
  interlock, engine commands, and persistence. Direct facade-observing view
  files fall from 19 to 18.
- **Warning-free real-voice fixtures (#61)** — both AVAudioConverter test
  loaders now signal end-of-stream directly from a zero-length read instead
  of capturing a mutable non-Sendable cursor in the converter's Sendable
  callback. This removes both Swift 6 warnings without unchecked conformance
  or extra synchronization.

### Tests
- Added a source-level ownership guard for the Diversity settings section.
  The complete suite passes (791 tests, one skipped, zero failures) without
  Swift concurrency warnings, and the signed Debug app passes strict codesign
  verification without connecting to a radio.

## [2026.0817_013] — 2026-08-17

### Changed
- **Narrow audio-waterfall ownership (#60)** — the demodulated-audio
  mini-waterfall now observes `AudioWaterfallPresentationModel` rather than
  the broad `RadioState` facade. The adapter publishes only mode, derived
  passband, and manual-notch markers; retains the engine-owned renderer; and
  exposes one weak notch action. The shared passband calculation now belongs
  to typed `ReceiverConfiguration`, reducing direct facade-observing view
  files from 20 to 19 without changing DSP or radio behavior.

### Tests
- Added a source-level ownership guard that prevents the audio-waterfall leaf
  from regaining a `RadioState` dependency, plus typed passband coverage for
  every mode family. The complete suite passes (790 tests, one skipped, zero
  failures), as does the signed Debug app build, without connecting to a radio.

## [2026.0817_012] — 2026-08-17

### Changed
- **Compiler-visible Media Deck playback ownership (#61)** —
  `MediaClipSession` is now main-actor isolated instead of unchecked
  `Sendable`. Its AVAudioEngine render callback captures a dedicated checked-
  `Sendable` processor whose converter, one-shot input, overlap gate, and
  master volume share one `OSAllocatedUnfairLock` state. Unsafe channel
  pointers remain local to the nonescaping render callback, while completion,
  fades, playback state, and security-scoped lifetime stay on the main actor.
- **Cancellable fade lifecycle (#61)** — clip fades now use one owned
  main-actor task rather than a Foundation timer with a cross-executor
  completion capture. Stop/restart cancels the task deterministically. The
  unchecked declaration inventory falls from 38 to 37; locks/queues/timers/
  unsafe references remain 49/21/26/70.

### Tests
- Added a source-level isolation guard for the Media Deck session/render
  boundary. The complete suite passes (788 tests, one skipped, zero failures),
  as does the signed Debug app build, without connecting to a radio.

## [2026.0817_011] — 2026-08-17

### Changed
- **Durable Media Deck file references (#24)** — Finder drops and file-picker
  assignments now persist read-only security-scoped bookmarks alongside their
  readable fallback paths. Playback resolves the bookmark first, follows moved
  files, falls back safely for older/corrupt documents, refreshes stale paths
  and bookmark data, and retains scoped access for the complete AVAudioFile
  session lifetime. Relinking an existing missing pad preserves its identity
  and configuration.

### Tests
- Added deterministic coverage for bookmark resolution after a stale absolute
  path, corrupt-bookmark fallback, and missing-reference refusal. The complete
  suite passes (787 tests, one skipped, zero failures), as does the signed
  Debug app build, without connecting to a radio.

## [2026.0817_010] — 2026-08-17

### Changed
- **Narrow bandwidth-mode presentation (#60)** — the startup Full/VPN choice
  and the always-visible header toggle now observe a dedicated
  `BandwidthPresentationModel` instead of the full `RadioState`. The adapter
  publishes only the selected mode and prompt preference, forwards mutations
  through the existing facade, and leaves skin updates with `SkinCenter`.
  Direct broad-facade view consumers fall from 21 files to 20.

### Tests
- Added a source-level ownership guard that prevents the bandwidth leaf views
  from regaining a `RadioState` dependency. The complete suite passes (784
  tests, one skipped, zero failures), as does the signed Debug app build,
  without transmitting.

## [2026.0817_009] — 2026-08-17

### Added
- **Media Deck keyboard navigation (#24)** — arrow keys now move focus
  deterministically through the pad grid, skipping unassigned pads in perform
  mode while exposing every slot in edit mode. Previous/next page buttons and
  Command-[ / Command-] cycle pages with wraparound, completing a keyboard-only
  path alongside per-pad shortcuts and the existing STOP ALL command.

### Changed
- **Narrow Bandscope presentation (#60)** — the standalone raw-ADC Bandscope
  no longer observes `RadioState`. Its adapter publishes only connection state,
  wideband availability, VFO position, and preselector bypass while preserving
  the engine-owned renderer and existing tuning/lifecycle actions.
- **Compiler-visible WAV ownership (#61)** — `WavRecorder` now keeps its file
  handle, PCM buffer, counters, completion flag, and error state inside one
  `OSAllocatedUnfairLock` value and conforms to checked `Sendable`. The audited
  unchecked-declaration count falls from 39 to 38.

### Tests
- Added sparse-grid and page-wrap navigation tests, a Bandscope source-level
  ownership guard, and concurrent WAV append/header/sample-clamping tests. The
  complete suite passes (783 tests, one skipped, zero failures), as does the
  signed Debug app build, without transmitting.

## [2026.0817_008] — 2026-08-17

### Added
- **Media Deck keyboard workflow and accessibility (#24)** — pads may have
  window-scoped Command/Option/Control shortcuts, with duplicate, invalid, and
  reserved STOP ALL conflicts rejected in the editor. Perform-mode pads expose
  their shortcuts visually and now provide VoiceOver labels, state values, and
  action hints for idle, playing, paused, queued, missing, and failed clips.
- **CW sidetone oscillator contract (#66)** — the non-transmitting keyer core
  now owns an allocation-free oscillator whose sample clock continues through
  silence and whose amplitude uses the exact same attack/release envelope
  exported for a future RF owner.

### Changed
- **Narrow DX-cluster presentation boundary (#60)** — the DX Cluster window,
  rows, ticker, and waterfall overlay no longer observe `RadioState`. A narrow
  presentation adapter snapshots only their persisted configuration, station,
  receiver, logbook, and lookup inputs while `DXClusterRuntime` remains the
  sole owner of transient spot/status/filter state.

### Tests
- Added deterministic CW oscillator/envelope tests, Media Deck shortcut and
  compatibility tests, stable DX-node color coverage, and a source-level guard
  against restoring broad `RadioState` observation in the DX-cluster view.
  The complete suite passes (778 tests, one skipped, zero failures), as does
  the signed Debug app build, without transmitting.

## [2026.0817_007] — 2026-08-17

### Added
- **CW setup and virtual-radio integration (#66)** — TX Controls now exposes
  persisted straight/iambic mode, WPM, weighting, paddle swap, hang, and
  sidetone preferences. A repeat-safe keyboard/HID edge mapper and a strictly
  in-memory harness carry CW intent through the production `TXCoordinator`,
  proving authorization, refusal, tail, reset, and watchdog behavior without
  any engine, socket, MOX, or HPSDR protocol access.
- **Media Deck group queues (#24)** — grouped pads can now Interrupt, Queue,
  or Ignore when their group is busy. Queues are duplicate-free FIFO,
  cancellable, visibly numbered on pads, and advance after completion, stop,
  fade-out, or an unreadable queued clip.

### Changed
- **DX-cluster runtime ownership (#60)** — transient spots, node statuses,
  filters, WWV text, dedupe, cap, and expiry move into `DXClusterRuntime`.
  The cluster window, ticker, and waterfall overlay observe that narrow owner
  directly while `RadioState` retains temporary action/configuration adapters.
- **Discord gateway queue boundary (#61)** — callbacks are immutable after
  construction; dispatch events cross queues as `Data` and are decoded on the
  service queue. A pure lifecycle value now owns generation rejection,
  heartbeat acknowledgement, READY state, and capped reconnect backoff.

### Fixed
- **CW watchdog reauthorization** — a forced watchdog drop can no longer
  reauthorize while the physical paddle remains held; a genuine all-up edge is
  required before the next coordinator request.

### Tests
- Added four CW input/virtual-radio tests, three DX runtime tests, two Discord
  lifecycle tests, and four Media Deck queue/policy tests. The complete suite
  passes (771 tests, one skipped, zero failures), as does the full signed Debug
  app build, without transmitting.

## [2026.0817_006] — 2026-08-17

### Added
- **Coordinator-gated CW session contract (#66)** — added a non-transmitting
  handshake that withholds sample-clock keying until `TXCoordinator`
  authorizes it, produces one release after hang, forces immediate unkey on
  watchdog, and requires fresh authorization after reset/release. Keyer
  preferences now persist in the versioned transmitter snapshot with safe
  defaults for older v2 data; actual engine/MOX/protocol wiring remains a
  later hardware-gated milestone.

### Changed
- **Narrow CW/RTTY decoder windows (#60)** — the two auxiliary windows now
  observe `DecoderCenter` (and CW's narrow receiver mode) instead of the broad
  facade. `DecoderCenter` owns their bounded transcripts and CW speed, while a
  stateless action bridge preserves engine commands and persistence.
- **Compiler-enforced DX-cluster ownership (#61)** — `DXClusterClient` is now
  main-actor isolated; Network callbacks explicitly return to that owner and a
  pure generation gate ensures duplicate failure callbacks schedule only one
  reconnect. The concurrency audit falls to 39 unchecked declarations.

### Fixed
- **Decoder transcript append path** — CW, RTTY, and ALE text now enters its
  single domain owner exactly once and remains bounded, avoiding duplicate or
  independently published facade transcript state.

### Tests
- Added six coordinator/keyer session tests, backward-compatible keyer
  persistence coverage, transcript ownership/bounds tests, and deterministic
  DX-cluster reconnect-generation tests.

## [2026.0817_005] — 2026-08-17

### Added
- **Deterministic CW keyer core (#66)** — added a pure sample-clock engine for
  straight key and iambic A/B behavior, WPM and weighting, paddle swap,
  sidetone ramping, transmit-intent hang, a stuck-key watchdog, and immediate
  disconnect/reset unkeying. This milestone is deliberately disconnected from
  the radio, MOX, and protocol paths, so it cannot transmit on attached
  hardware until a later coordinator-routed integration.

### Changed
- **Three more narrow control leaves (#60)** — the Kp chip, S-meter renderer,
  and PSKReporter status now receive only their display values and tokens from
  their existing parent boundary instead of independently observing the full
  `RadioState` facade.
- **Compiler-enforced OAuth ownership (#61)** — the interactive Google OAuth
  flow is now main-actor isolated, with Network callbacks explicitly hopping
  to that owner. Its one-shot continuation no longer needs a class-wide
  `@unchecked Sendable` promise or an `NSLock`; the audit falls to 40 unchecked
  declarations and 49 lock constructions.

### Tests
- Added nine CW keyer regressions covering exact 48/96 kHz timing across
  arbitrary render blocks, weighting, squeeze alternation, iambic A/B release,
  paddle swap, bounded sidetone ramps, hang time, watchdog rearm, and reset.

## [2026.0817_004] — 2026-08-17

### Changed
- **Repository-scoped self-hosted CI** — ordinary CI, weekly extended gates,
  and no-secret release dry runs now target the dedicated Apple-silicon Mac
  runner instead of consuming hosted macOS minutes. Fork pull requests are
  excluded from the personal machine, persistent Xcode products are always
  unregistered and removed to prevent duplicate app sightings, and the
  secret-bearing signed release remains isolated on a disposable hosted
  runner.

## [2026.0817_003] — 2026-08-17

### Added
- **Traceable calibration hardware fixture (#65)** — retained the measured
  ANAN Orion MkII / Bird 43 forward-power sweep as an identity-, profile-,
  firmware-, source-log-, and path-bound CSV fixture. A new operator procedure
  covers dummy-load prerequisites, one-point-at-a-time capture, rejection of
  under-range/saturated evidence, residual review, export, and recovery while
  explicitly preserving the rule that calibration never keys automatically.

### Changed
- **Three narrower control views (#60)** — bookmark, keyboard-map, and
  waterfall-capture controls now receive only their displayed values and
  actions from `ControlBar` instead of independently observing the full
  `RadioState` facade. Direct root-facade view declarations fall from 62 to 59
  without changing persistence, navigation, sharing, or Discord behavior.
- **Compiler-enforced clip-player ownership (#61)** — `ClipPlayer` and its
  AVFoundation lifecycle are now main-actor isolated, with framework
  completions explicitly returning to that actor. This removes another
  `@unchecked Sendable` promise; the audited inventory falls from 42 to 41.

### Tests
- Added a known-measurement regression that imports the retained seven-point
  CSV and pins its identity, path, range, fitted coefficient, RMS residual,
  and maximum residual, plus explicit under-range and saturated-plateau
  rejection coverage. All 740 SwiftPM tests pass (one hardware benchmark
  skipped), and the signed Debug app builds without radio hardware or RF
  transmission.

## [2026.0817_002] — 2026-08-17

### Fixed
- **CAT two-tone/tune shutdown truth** — every unkey path now clears its
  specialized carrier flag before publishing the final rigctl snapshot. A
  `U TWOTONE 0`, `U TUNER 0`, disarm, or asynchronous RF-tail completion can
  no longer leave CAT reporting stale `PTT=1` / function-on state after the
  radio has returned to receive.
- **ANAN TX harness current telemetry** — `tools/p2_tx_test.py` now uses the
  same Orion MkII PA-current fit and 2.3 A trust floor as the app, and prints
  the raw current/voltage detector counts needed to finish issue #34's
  low-end calibration instead of presenting the obsolete current fit as fact.

### Tests
- Live-validated the ANAN ANT1 dummy-load two-tone diagnostic at 14.074 MHz,
  USB, and 3% drive. The 100 ms phosphor displayed the actual wire-IQ
  two-tone envelope, identified the audio-chain bypass, kept every fault lamp
  clear, and reported 0.01 V forward / 0.00 V reverse at this sub-calibration
  power level.
- Extended the rigctl function fixture through the `TWOTONE 0` transition.

## [2026.0817_001] — 2026-08-17

### Added
- **ANAN network configuration** — each idle Protocol 2 radio in the connect
  sheet now has a guarded Configure flow for selecting DHCP/link-local fallback
  or writing a validated static IPv4 address. The MAC-targeted v4.4 Set IP
  command is confirmed before it writes EEPROM, broadcasts only while
  discovery is active, and triggers bounded rescans as the radio changes
  address.
- **Operator FM controls and CTCSS (#66)** — the DSP popover now exposes
  separately remembered wide/narrow FM deviation, an off-by-default transmit
  CTCSS encoder with the standard 50-tone set, and received-tone detection.
  CTCSS is injected after speech shaping with reserved deviation headroom;
  receive detection requires two stable half-second windows and reports only
  state changes.

### Changed
- **Three more narrow view dependencies (#60)** — the FT8 heard-map button now
  observes `DecoderCenter`, Network Speakers observes `SkinCenter`, and About
  uses a refreshable support-info snapshot adapter. Direct `RadioState` view
  consumers fall from 28 to 25, avoiding unrelated redraws without changing
  window behavior.

### Fixed
- **TX-policy phantom range** — the compact TX editor no longer lets an
  operator confirm its displayed 0–54 MHz fallback while the typed range list
  is actually empty. Empty policies now say “Edit range” and disable
  confirmation; changing a range or IARU-region tag also clears the previous
  confirmation so the revised policy must be acknowledged explicitly.
- **Manual/unknown radio connection crash** — the RF-gain control now renders
  an inert fixed-gain slider for the conservative zero-width hardware profile
  instead of asking SwiftUI to normalize `0...0`, which trapped immediately
  after a manual connection. Profile changes clamp gain before publishing the
  new range, and app discovery once again retains the ANAN link-local fallback
  while adding the operator's last manual host.

### Tests
- Added byte-exact Protocol 2 Set IP fixtures for static addressing, DHCP,
  malformed MAC/IP input, and unsafe unicast destinations.
- Live-validated the ANAN Set IP flow on MAC `80:1F:12:6E:4C:81`: DHCP
  returned at its link-local fallback, static `169.254.76.129` restored, and
  both states rediscovered idle before a successful receive connection.
- Re-ran the independent ANAN ANT1 dummy-load harness at 29.600 MHz and low
  drive: zero stream sequence errors, 0.1–0.3 W forward, negligible reflected
  power, 1.00–1.05 SWR, correct sideband, and a clean forced unkey.
- Added a TX-policy regression fixture proving range/region edits invalidate
  prior confirmation and an empty displayed fallback cannot be confirmed.
- Added CTCSS configuration, tone acquisition/clear, adjacent-tone rejection,
  speech-only rejection, configurable-deviation, and TX injection fixtures.
  All 738 SwiftPM tests pass (one hardware benchmark skipped), and both
  unsigned Debug and Release app builds pass. A rebuilt Debug app also
  completes the formerly crashing manual/unknown-radio connection and presents
  its fixed RF gain as disabled, receive-only UI.

## [2026.0816_003] — 2026-08-16

### Added
- **Chat-aware Crab co-host (#54)** — in OAuth YouTube Live sessions the crab
  polls live chat and answers explicit viewer questions; in Discord it answers
  direct bot mentions in the configured text channel without requesting the
  privileged Message Content intent. YouTube replies refresh expired OAuth
  access tokens, skip pre-session backlog, and follow the API's polling pace.
  Discord and YouTube both ignore self-authored messages to prevent loops.
- **Public-chat safety boundary** — viewer questions run in a separate model
  conversation that resets after every message, use a reporting-only tool
  allowlist, and pass through bounded duplicate/global/per-viewer cooldown
  gates. Public text cannot tune, change settings, inspect private logs,
  transcripts, skeds, credentials, or contaminate the operator's conversation;
  accepted exchanges remain visible to the operator in Ask The Crab.

### Changed
- **Three more narrow view dependencies (#60)** — Software Update now observes
  only a two-property TX-safety adapter, while QSO Log and LoTW observe a
  bounded logbook/LoTW adapter plus their concrete activity service. All three
  read theme changes from `SkinCenter` and no longer observe `RadioState`,
  reducing direct root-facade view consumers from 31 to 28 without changing
  persistence, logging, export, update interlocks, or LoTW behavior.
- The Crab and YouTube settings explain that viewer-chat answers require
  Co-host mode and YouTube account/OAuth mode; pasted stream keys have no Data
  API identity and therefore cannot read chat.

### Tests
- Added pure fixtures for chat sanitization, question selection, bounded
  duplicate/cooldown behavior, the external AI-command allowlist, Discord
  mention parsing and gateway intents, and YouTube live-chat request/response
  parsing. All 728 SwiftPM tests pass (one hardware benchmark skipped), both
  unsigned Debug and Release app builds pass, the repository audit is clean,
  and every deterministic benchmark-smoke deadline passes.

## [2026.0816_002] — 2026-08-16

### Added
- **Active Band Scout (#54)** — Ask The Crab now performs a receive-only,
  time-of-day-ranked sweep across seven representative HF CW/digital stops,
  dwells with OmniSkimmer and RF Vision, ranks sustained signals by analyzer
  evidence and SNR, and returns exact tune-to offers. The sweep refuses armed
  TX, recording, replay/time-shift, and sub-RX states; cancellation and normal
  completion restore the original VFO, center, display pan, mode, filter, CAT
  mirror, and analyzer-enable choices without ever touching the TX frequency.

### Changed
- **YouTube view ownership (#60)** — the YouTube Live window now observes its
  narrow `YouTubeLiveService` directly and reads chrome from `SkinCenter`, so
  broadcast status, diagnostics, and configuration changes no longer require
  the 7,000-line `RadioState` compatibility facade as a view dependency.
- **Release automation closeout evidence (#63)** — all seven protected
  environment secret names are configured, the hosted no-secret release dry
  run produced and uploaded its exact asset layout, and the public
  `2026.0816_001` DMG independently passed checksums, strict deep Developer ID
  verification, Team ID validation, Gatekeeper's notarized assessment, and
  stapler validation.

### Tests
- Band Scout fixtures pin day/night stop selection, radio tuning-range
  filtering, analyzer-evidence ranking, exact tune offers, and the no-signal
  DX-cluster fallback. All 721 SwiftPM tests pass (one hardware benchmark
  skipped), both unsigned Debug and Release app builds pass, the repository
  audit is clean, and every benchmark-smoke deadline passes.

## [2026.0816_001] — 2026-08-16

### Fixed
- **CI flake: `testRegionTimesBackOutTheTimeShift` timeout** — the test
  pushed all 40 spectrum rows in one up-front burst. On a slow hosted
  runner the engine's first drain could cover only the tracker's warm-up
  rows, publish an empty snapshot, and close the 0.25 s publish gate;
  with no further rows the confirmed region never published and the
  5-second wait timed out (two red runs on 2026-08-15). The test now
  streams rows until the region publishes, matching the live spectrum
  tee, whose continuous ~30 rows/s cadence is what keeps the gate
  reopening in production. Engine behavior is unchanged.

## [2026.0815_005] — 2026-08-15

### Added
- **Actual-IQ two-tone scope (#39)** — TX Meters now switches to a 100 ms
  envelope trace tapped from the complex IQ that the internal 700 + 1900 Hz
  source delivers to the protocol packetizer. The face explicitly labels the
  source as wire IQ and the coach states that the clean RF generator bypasses
  the microphone, audio processing, limiter, and audio-chain IMD analyzer.
  The fixed lock-free SPSC tap drops optional diagnostic bins instead of ever
  delaying the radio queue.

### Changed
- **One release app, one development app** — Xcode Debug products are now
  named `HermitSDR Dev` with bundle id `com.hermitsdr.app.debug`; LaunchServices
  can no longer register DerivedData as a second installed HermitSDR. Debug
  builds skip automatic update checks and cannot self-install over their build
  artifact, while the signed release keeps its canonical name/id and continues
  to replace its running bundle in place. Local release/dry-run verification
  now builds in temporary DerivedData, unregisters its canonical-name product,
  and removes all staging directories on exit.
- **YouTube session cleanup** — OAuth cancellation now closes its loopback
  listener immediately, and every OAuth session deletes its temporary
  `liveStream` resource after completion. Cancelling during setup also deletes
  any stream/broadcast already created. Stop/failure finalization blocks a new
  start until the exact prior broadcast has been completed (or an unstarted one
  deleted), preventing a quick restart from completing the new broadcast.
- **YouTube startup recovery** — HermitSDR no longer calls a stream live merely
  because RTMP accepted the publish command. It waits for a real H.264 access
  unit, polls the OAuth stream's ingest/health and broadcast lifecycle, surfaces
  YouTube configuration errors, explicitly advances a stuck ready broadcast
  after ingest becomes active, and confirms LIVE only when viewers can watch.
  Transient startup failures retry the same bound ingest up to twice with
  backoff, preserving the broadcast URL and avoiding duplicate Studio events.
  OAuth streams use YouTube's recommended resolution/frame-rate auto-detection
  so an aspect-preserved app window cannot conflict with a fixed CDN profile
  and remain stuck on Preparing Stream.
- **Discord view ownership (#60)** — the Discord settings window now observes
  `IntegrationCenter` instead of the whole `RadioState` facade. Persisted
  configuration, ephemeral Keychain-loaded credential buffers, connection and
  voice status, directory results, and the bounded diagnostics log have one
  domain owner; UI commands retain the established persistence and service
  lifecycle bridge.
- **Hosted CI stabilization (#63)** — the RF Vision historical-timestamp test
  can force its deterministic CPU mask instead of racing first-use Metal
  pipeline compilation on shared macOS runners. A documentation-consistency
  test now pins the scheduled Address/Thread Sanitizer virtual-radio jobs,
  benchmark and repository audits, release dry run, protected environment,
  and complete seven-secret release contract already present in the workflows.

### Fixed
- **YouTube quality selection** now constrains the actual ScreenCaptureKit
  encoder dimensions (360p/480p/720p/1080p, aspect-preserving and even-sized)
  instead of changing only the Data API declaration while always capturing at
  the old near-1080p size. An AAC-converter initialization failure now stops
  the session instead of falsely reporting a 128 kbps audio stream.
- **YouTube OAuth reliability/security** — the callback listener is explicitly
  loopback-only, accumulates fragmented HTTP requests through the header
  terminator, rejects wrong-state callbacks without aborting the real browser
  flow, escapes browser error text, and accepts only one token exchange.
- **YouTube real-time fan-out** — AAC and caption input buffers now use the
  fixed-capacity FIFO rather than `Array.removeFirst` compaction on the DSP
  audio callback; overflow remains bounded and AAC timestamps still account
  for dropped wall time.
- RTMP ingest parsing rejects malformed/out-of-range ports and credentials and
  correctly handles bracketed IPv6 hosts. Transcript filenames are sanitized
  and bounded, writes are atomic, and a filesystem failure is reported instead
  of logging a false success.

### Tests
- Focused coverage drains and grades the synthesized two-tone wire envelope,
  proves Discord credentials never enter persisted integration configuration,
  caps the Discord diagnostic log at 200 entries, and exercises the previously
  flaky RF Vision timestamp contract in milliseconds on the CPU path.
- 56 focused YouTube/update tests pin capture geometry, resource-delete
  requests, safe transcript filenames, strict RTMP endpoint parsing, and the
  invariant that Debug and Release products have distinct identities.
- The reviewed concurrency inventory advances from 41 to 42 unchecked types
  and from 69 to 70 unsafe references for the fixed-storage TX diagnostic tap;
  lock, queue, and timer counts remain 50, 21, and 26.
- The complete SwiftPM suite passes 717 tests with 0 failures and the one
  intentionally skipped opt-in benchmark; unsigned Debug and Release app
  builds also succeed, and the repository dependency/license/workflow/secret
  audit is clean.

## [2026.0815_004] — 2026-08-15

### Added
- **PureSignal Phase 1 PA characterization (#51)** — ANAN paired feedback now
  feeds a capture-only PA Linearity instrument with fractional loop-delay and
  correlation estimates, small-signal gain/phase, binned AM–AM and AM–PM
  curves, and RF-domain IMD3/SFDR when a credible two-tone is present. The
  analyzer produces observations only; no correction coefficients exist or
  enter the transmit path.

### Changed
- **Narrower transmitter diagnostics ownership (#60)** — the packet-rate
  PureSignal capture monitor has left `RadioEngine` for a dedicated bounded
  service. Borrowed protocol arrays are copied only into one fixed 8,192-pair
  bank, heavy analysis runs at most twice per second on its own queue, and an
  occupied bank drops optional analysis samples instead of blocking radio
  delivery. Level telemetry remains bounded to 10 updates per second.
- TX Controls links directly to the new instrument, Tools exposes it beside
  TX Meters, and the audio-chain IMD tooltip now distinguishes its post-limiter
  measurement from ANAN PA/RF feedback analysis.

### Tests
- Deterministic analyzer coverage pins fractional delay, complex gain/phase,
  visible AM–AM compression and AM–PM rotation, and a bin-centered two-tone
  with 30 dBc injected third-order products.
- The documented unchecked-Sendable inventory baseline advances from 40 to 41
  for the independently synchronized PureSignal service.
- The full SwiftPM suite passes 705 tests with 0 failures and the one
  intentionally skipped opt-in benchmark; the Developer-ID-signed Debug app
  also passes strict deep signature verification.
- Approved ANAN-7000DLE MkII ANT1 dummy-load validation at 14.074 MHz USB and
  3% drive captured 130,512 paired frames. Phase 1 reported 1.000 correlation,
  0.03-sample (0.15 µs) loop delay, -31.0 dB / -137.2° small-signal gain,
  and 48.8 dBc RF IMD3/SFDR, with visually linear AM–AM and flat AM–PM curves.
  Unkey/disarm returned forward and reverse readings to 0.00 V.
- The same live run leaves #39 open: TX Meters continued to label the source
  `MIC METERS IDLE` and showed an empty phosphor trace while the two-tone was
  active, so the requested live pre/post-limiter scope proof is not yet met.

## [2026.0815_003] — 2026-08-15

### Changed
- **WSJT-X end-to-end closeout (#8)** — the documented digital-mode contract is
  now backed by a final SquareSDR own-receiver check, and the setup guide no
  longer lists hardware validation as outstanding.

### Tests
- Live SquareSDR dummy-load validation at 14.074 MHz USB completed a
  `WU1T TEST` FT8 transmission through WSJT-X 2.7, Hamlib NET rigctl, CAT PTT,
  BlackHole 2ch, and HermitSDR's Digital profile. At 3% drive the continuously
  streaming receiver showed one narrow FT8 trace consistent with the protocol's
  approximately 50 Hz occupied width at the intended 1500 Hz audio offset
  (14.0755 MHz), peaking at S9+30 / -42 dBm with 1.0 SWR and no reverse
  indication. WSJT-X logged the 10:17:30 UTC cycle, then HermitSDR was
  explicitly unkeyed and disarmed; a later WSJT-X software-only queued cycle
  occurred after ARM was off and therefore produced no RF.
- `DocsConsistencyTests` confirms the release number remains synchronized
  across the Xcode project, README, and changelog.

## [2026.0815_002] — 2026-08-15

### Changed
- **Real-time performance closeout (#62)** — the measured callback contract
  now records cadence, deadlines, ownership, overload behavior, and the
  benchmark-backed transient-storage exceptions for every packet, DSP, audio,
  spectrum, skimmer, and GPU boundary. The audio-render support snapshot now
  includes ring fill high-water and producer-overrun sample counts without
  adding work to the CoreAudio callback.

### Tests
- The complete 30-scenario Apple M4 Pro release benchmark is retained as the
  issue-closeout report under `docs/performance/`: every deadline passes,
  29 paths return to zero live allocator growth, and the only retained
  exception is the documented 640-byte Metal RF Vision framework block.
  Focused diagnostics tests pin audio drop and queue-high-water formatting in
  Copy System Information. The full regression suite completes 702 tests with
  no failures and one intentional benchmark skip; the Developer ID-signed
  Debug app build and strict deep signature verification both succeed.

## [2026.0815_001] — 2026-08-15

### Added
- **ANAN PureSignal Phase 0 capture (#51)** — Protocol 2 can opt into a
  session-scoped, keyed-only pair of synchronous 192 kHz/24-bit streams: DDC0
  captures the internal PA-feedback sample routed to ADC0 and DDC1 captures
  the firmware's DAC/TX reference. The TX panel exposes ANAN-only capture and
  0–31 dB feedback-attenuation controls plus bounded feedback/reference level
  telemetry. Capture is off by default, restores the normal receive DDC layout
  after unkey and protection trips, and deliberately performs no predistortion
  correction in this phase.

### Fixed
- **Keychain-safe startup** — enabled Discord integrations now load their
  credentials off the main actor, and all in-process Keychain operations are
  serialized. A Discord restore can no longer race the lifecycle high-water
  check and leave HermitSDR running without ever creating its first window.
- **WSJT-X CAT handshake (#8)** — the built-in NET rigctl server now returns
  the bare integer Hamlib expects for `\chk_vfo` and acknowledges `q` before
  closing the socket, allowing WSJT-X Test CAT/PTT and Tune to complete the
  real end-to-end handshake instead of timing out during setup.
- **WSJT-X CAT PTT capability (#8)** — rigctl `\dump_state` now advertises
  protocol 1, the connected radio's real TX frequency range, and
  `RIG_PTT_RIG_MICDATA`. Current Hamlib clients can now discover the explicit
  CAT PTT port and send `T` for Test PTT and normal digital transmit.

### Tests
- The focused Protocol 2 fixture verifies the PureSignal DDC assignments,
  synchronized paired-IQ dispatch, Alex routing, attenuation, and receive-path
  restoration without connecting a radio or producing RF.
- The full regression suite completes 702 tests with no failures and one
  intentional benchmark skip. Focused rigctl coverage verifies the protocol-1
  CAT PTT capability block and the connected radio's advertised TX range. The
  final Developer ID-signed Debug app build and strict deep signature check
  both succeed.
- Live SquareSDR dummy-load validation at 14.074 MHz USB confirms WSJT-X 2.7
  Test CAT, CAT PTT, a three-second Tune, and one complete 13.9-second FT8
  free-text cycle end to end through BlackHole 2ch. At 3% drive the Tune
  measured 0.15 V forward, 0.00 V reverse, and 1.0 SWR; the TX meters captured
  the waveform with no clip, flat-top, overdrive, or underrun flags. The radio
  was explicitly unkeyed and disarmed after the test.
- Live ANAN-7000DLE MK2 dummy-load validation on ANT1 at 14.074 MHz USB and
  3% drive confirms Phase 0's keyed paired-IQ path. A brief two-tone capture at
  31 dB feedback attenuation retained 7,290 paired frames; feedback measured
  -77.8 dBFS RMS / -74.7 dBFS peak and reference measured -13.7 dBFS RMS /
  -10.7 dBFS peak. Forward/reverse detector readings were 0.01/0.00 V, and
  the capture unkeyed cleanly before the radio was explicitly disarmed.
  Automated fixtures separately pin restoration of the normal receive layout.

## [2026.0814_002] — 2026-08-14

### Changed
- **Narrow runtime statistics owner (#60)** — one-second packet, byte,
  sequence-error, CPU, GPU, and GPU-frame telemetry now belongs to a dedicated
  main-actor observable model. The status bar observes it directly, so routine
  statistics sampling no longer invalidates every `RadioState` observer.
- **Compiler-visible AI-provider state (#61)** — Claude conversation history,
  generation, and API-key state plus Foundation Models session/tool/budget
  state now live behind `OSAllocatedUnfairLock`. Neither provider needs a
  class-wide `@unchecked Sendable` promise, and no protected state is held
  across an awaited model request. The inventory falls from 42 to 40 unchecked
  declarations while retaining 48 visible lock constructions.
- **Borrowed TX IQ output (#62)** — the Protocol 1 and 2 connection queues own
  reusable 63- and 60-sample I/Q scratch arrays and lend them to TXChain for
  in-place voice, tune, two-tone, CW, starvation, and unkey-tail output. Live
  packet pacing no longer creates a new output tuple and two arrays per packet;
  the owned-array API remains available only for tests and non-hot callers.

### Tests
- The focused runtime-statistics, borrowed-output, and protocol lifecycle set
  completes 25 tests with no failures. The full suite completes 698 tests with
  no failures and one intentional benchmark skip. The Apple M4 Pro release
  matrix meets all 30 deadlines; every TX scenario reports zero live allocator
  growth after warm-up, with voice at 160.333 µs p99 and key/unkey tail at
  97.291 µs p99. The unsigned Debug app build and complete release dry-run
  packaging both succeed. No radio was connected and no RF was emitted.

## [2026.0814_001] — 2026-08-14

### Changed
- **Clublog acceptance closeout (#48)** — live most-wanted downloads are now
  explicitly opt-in from the DX Cluster window and persist that choice. Turning
  the service off cancels an in-flight refresh, removes the live overlay, and
  immediately restores the bundled offline ranking; cached data remains
  available for the next opt-in enable. The existing weekly atomic cache,
  current-rank overlay, and authoritative full-call/longest-prefix DXCC mapping
  retain their offline fallbacks.
- **RF Vision acceptance closeout (#14)** — the release performance matrix now
  measures a complete 2,048-bin RF Vision mask-and-track row against its 30 Hz
  cadence budget. Each Metal row drains its own autorelease pool so a long
  analysis batch does not retain command objects until the outer dispatch work
  item finishes.
- **Release-secret readiness (#63)** — the protected signed-release job now
  validates all seven required secret names before decoding or importing any
  credential and reports only missing names. Release documentation fixes the
  inventory count and records the non-leaking preflight behavior. Repository-
  side CI, extended gates, dry-run packaging, and release automation are
  complete; hosted signing remains gated on configuring the environment
  secrets and proving one real signed release.

### Tests
- Clublog/DXCC and RF Vision acceptance fixtures complete 33 focused tests with
  no failures. The full suite completes 694 tests with no failures and one
  intentional benchmark skip; the unsigned Debug app build and complete release
  dry-run packaging both succeed. On the Apple M4 Pro, all 30 release scenarios
  meet their deadlines with zero live allocator growth; RF Vision Metal analysis
  is 564.542 µs p99 against a 33,333 µs row budget. No radio was connected and
  no RF was emitted.

## [2026.0813_007] — 2026-08-13

### Changed
- **Independent PSKReporter lifecycle (#60)** — `IntegrationCenter` now owns
  a main-actor `PSKReporterService`; decoded spots and station configuration no
  longer route through `RadioEngine`, and the settings status observes the
  narrow service directly. Upload DNS/socket work remains off-main, while a
  generation rejects results that finish after disable or reconfiguration.
- **Compiler-visible integration/audio synchronization (#61)** —
  `PSKReporterClient` is main-actor isolated and uses a cancellable task rather
  than an unchecked class, lock, private queue, and dispatch timer. Audio
  fanout and TQSL pipe draining now encapsulate mutable state in
  `OSAllocatedUnfairLock`, removing two more class-wide unchecked promises.
  The inventory falls from 45 to 42 `@unchecked Sendable` declarations, 49 to
  48 lock constructions, 20 to 19 queues, and 27 to 26 timers.
- **Allocation-stable TX queues (#62)** — a fixed-capacity paired I/Q FIFO now
  backs the TX output ring, and bounded Float FIFOs back pre/post scope and IMD
  windows. The monitor null-test uses cursor-based streaming storage. Normal
  TX feed/pull no longer grows arrays or periodically compacts consumed
  prefixes with `removeFirst`; overflow retains the newest bounded samples.

### Tests
- Added wrap/overflow/pairing tests for the complex FIFO and single-sample/
  snapshot tests for the Float FIFO. A local Thread Sanitizer run completed 28
  lifecycle/configuration tests with 20 stress iterations and no races or
  failures. The Apple M4 Pro release matrix meets all 29 deadlines with zero
  live allocator growth in every scenario: voice TX is 92.875 µs p99,
  key/unkey tail is 119.208 µs, 1.536 MHz RX is 247.042 µs, and the combined
  load is 328.583 µs. The unsigned Debug app build succeeds. No radio was
  connected and no RF was emitted.

## [2026.0813_006] — 2026-08-13

### Changed
- **Narrow domain views (#60)** — the Tuning Device, Decoder Activity, and
  Stations Heard windows now observe `IntegrationCenter` or `DecoderCenter`
  directly instead of invalidating on every `RadioState` change. Time-machine
  and bookmark controls likewise observe recording/decoder state directly and
  use a stateless action bridge for facade-owned effects. Tuning-device runtime,
  learning, and mapping state now have one owner in `IntegrationCenter`.
- **Deterministic async finalization (#61)** — audio configuration restarts use
  a tested rolling-window breaker that stays latched until an explicit reset.
  LoTW refreshes cancel their transport and reject late transport/cache
  completions by generation. Application shutdown now stops integrations and
  discovery without restarting discovery, while the settings mirror removes
  its observer, drains any in-flight export, and writes one authoritative final
  snapshot.
- **TX/audio performance matrix (#62)** — the release harness now covers TX
  voice, tune, two-tone, and CW production, key/unkey tail transition,
  Protocol 2 60-to-240-sample TX upsampling, audio callback sizes from 64 to
  1,024 frames, and deterministic Protocol 2/audio jitter-loss schedules.

### Tests
- Added tuning mapping/learning ownership and LoTW cancellation tests plus
  restart-window storm/reset coverage and 250 rapid voice key/tail/re-key
  cycles with finite, bounded IQ. The Apple M4 Pro release report meets all
  29 deadlines: voice TX is 85.541 µs p99, key/unkey tail is 124.708 µs,
  Protocol 2 TX upsampling is 3.292 µs, and the 1,024-frame audio callback is
  6.167 µs p99. Every scenario has zero live-block growth; 28 also have zero
  live-byte growth, while the stateful tail fixture retains 5,120 bytes after
  warm-up. The Debug suite completes 691 tests with one opt-in benchmark skip
  and zero failures, and the unsigned Debug app build succeeds. No radio was
  connected and no RF was emitted.

## [2026.0813_005] — 2026-08-13

### Changed
- **Integration configuration owner (#60)** — `IntegrationCenter` now owns
  CAT listener intent, Discord routing/notification selection, tuning-device
  lifecycle settings, DX-cluster connections/ticker state, and LoTW display
  preferences. Typed lifecycle commands cross to the existing concrete service
  adapter while `RadioState` keeps compatible bindings and legacy preference
  keys without retaining a second configuration copy. Credentials remain in
  Keychain and are intentionally absent from the model.
- **Extended lifecycle sanitizer matrix (#61)** — the scheduled Address/Thread
  Sanitizer job now repeats Protocol 1 and 2 reconnects while changing sample
  rates, receiver counts, diversity, wideband, TX state, and callback
  generations. Replay and recording start/stop cycles and concurrent DSP
  reconfiguration run in the same extended gate; iteration count is bounded
  and configurable for local reproduction.
- **Complete release performance matrix (#62)** — the deterministic harness
  now measures P1 one/two-receiver decode, P2 normal/diversity decode, 5 ms RX
  blocks at every supported 48–1536 kHz rate, and a combined P2 decode +
  384 kHz RX + IQ-history + OmniSkimmer workload. Resource-budget tests cover
  every rate, receiver count, preset, and pressure level and require either a
  bounded fit or an explicit degradation/overage report.

### Tests
- Added focused `IntegrationCenter` transition/restore tests and lifecycle,
  replay, recording, and budget-matrix stress. The Debug suite completed 686
  tests with zero failures (the one opt-in release benchmark was skipped there
  and run separately), along with a successful unsigned Debug app build and
  focused TSan run. The Apple M4 Pro release report
  meets all 17 deadlines: 1.536 MHz RX is 373.875 µs p99 against 5 ms and the
  combined workload is 239.542 µs p99 against 10 ms, both with zero live
  allocator growth after warm-up. No radio was connected and no RF was emitted.

## [2026.0813_004] — 2026-08-13

### Changed
- **OmniSkimmer channelizer framing (#62)** — CPU and Metal channelizers now
  retain input history in `StreamingFloatBuffer` rings and consume prefixes
  without `Array.removeFirst`. Persistent linear/interleaved staging buffers
  preserve CPU/GPU output equivalence while steady fixed-cadence storage is
  reused after warm-up.
- **Sendable stream callbacks (#61)** — Protocol 1, Protocol 2, UDP transport,
  replay IQ, wideband, TX-IQ, and lifecycle callback contracts are explicitly
  `@Sendable`. `RadioEngine` now supplies sendable handlers, keeps ADC overflow
  edge state atomic, and treats the wideband FFT as queue-owned.
- **Decoder configuration owner (#60)** — `DecoderCenter` now exclusively owns
  SSTV, WEFAX, CW, RTTY, and ALE enablement/configuration, including session-only
  ALE scan intent. Typed commands adapt those transitions to decoder engines
  and scanner infrastructure while `RadioState` keeps compatible bindings and
  legacy preference keys without retaining duplicate state.

### Tests
- Added fixed-cadence CPU-channelizer storage reuse, 64-way callback replacement
  and disconnect/replay lifecycle stress, and decoder configuration/command
  transition coverage. The unsigned Debug app build, focused TSan callback
  runs, 670 executed non-documentation tests, and all eight documentation/
  version consistency tests pass (the opt-in benchmark skip is run separately
  in release).
  The Apple M4 Pro release benchmark meets all nine deadlines; the new 4,800-
  sample CPU channelizer scenario reports 144.417 µs p99 and zero live allocator
  growth after warm-up. No radio was connected and no RF was emitted.

## [2026.0813_003] — 2026-08-13

### Added
- **Recording domain owner (#60)** — `RecordingModel` now exclusively owns
  IQ/WAV recording state, elapsed-time polling, time-shift/history status,
  replay identity, and restoration of the live sample rate. Engine operations
  cross a narrow port and failures return as typed effects while `RadioState`
  remains a compatibility facade.
- **Atomic callback epochs (#61)** — connection, main-RX, and sub-RX callbacks
  capture lock-free generation tokens. Disconnects and DSP replacement reject
  late IQ, audio, spectrum, decoder, meter, protection, and wideband delivery
  from superseded sessions without blocking a real-time queue.

### Changed
- **Capacity-stable DSP framing (#62)** — FIR decimation, overlap-save channel
  filtering, the audio spectrum, spectral NR, RX RNNoise, and TX mic RNNoise
  now consume a reusable grow-on-demand float ring. Steady-state framing no
  longer shifts an `Array` prefix; fixed-cadence storage remains stable after
  warm-up without dropping samples.
- The release benchmark now covers a 1.536 MHz FIR block, 12 kHz spectral-NR
  cadence, and the reusable 480-sample framer in addition to packet, RX/TX,
  and bounded-mix paths.

### Tests
- Added recording lifecycle/failure/replay tests, sequential and concurrent
  generation-gate checks, and ring wrap/growth/10,000-cycle reuse coverage.
  Focused DSP tests and an unsigned Debug app build pass. The Apple M4 Pro
  release benchmark meets all eight deadlines; all three new scenarios report
  zero live allocator growth after warm-up. No radio was connected and no RF
  was emitted.

## [2026.0813_002] — 2026-08-13

### Added
- **Decoder domain owner (#60)** — `DecoderCenter` now independently owns
  live/recent decoder sessions, replay-safe time-machine bookmarks, and the
  bounded FT8/FT4 heard-grid map. Engine and integration side effects cross
  the boundary as typed values while `RadioState` remains a compatibility
  facade for existing views.
- **Block-boundary configuration mailbox (#61)** — RX retune, attenuation,
  squelch/overload thresholds, and TX mic gain publish immutable latest-value
  snapshots. The packet/mic owner copies the newest version at a block
  boundary instead of making UI setters wait behind a multi-millisecond DSP
  pass.

### Changed
- **Reusable protocol conversion storage (#62)** — live Protocol 1 and 2 IQ
  decoding now writes into queue-confined, capacity-stable arrays borrowed by
  synchronous callbacks. P1 no longer builds four fresh float arrays per EP6
  packet; P2 no longer creates a new I/Q pair per DDC packet, and diversity
  combines directly into the reusable output. Wideband storage is reserved
  to its fixed frame size at connection construction.
- The real-time benchmark now measures the production reusable P1/P2 decode
  APIs rather than compatibility helpers that intentionally return owned
  arrays.

### Tests
- Added DecoderCenter lifecycle/stamp/bookmark/heard-data tests, reusable
  buffer capacity/orientation/diversity checks, and a TSan-ready concurrent
  reconfigure/process stress scenario. Virtual-radio lifecycle coverage
  passes without connecting to hardware or emitting RF. The final Apple M4
  Pro release benchmark meets all five deadlines with zero live allocator
  growth in both reusable packet decoders.

## [2026.0813_001] — 2026-08-13

### Added
- **Evidence-based audio doctor (#54)** — Ask The Crab's `fix_my_audio` tool
  now interprets silence/quiet, hiss, whine, boomy, harsh, and hollow
  complaints. A live audio-spectrum observation reports a prominent tone's
  frequency and floor-relative level; an approved whine fix adds one
  idempotent manual notch, while complaint-specific NR/EQ A/B fixes remain
  explicit and reversible.
- **Bounded FIFO benchmark (#62)** — the opt-in release harness now measures a
  120-sample append/mix/consume cycle against a 100 µs p99 deadline.

### Changed
- **Bounded real-time queues (#62)** — spectrum overlap, sub-receiver audio,
  TX monitor, and media-deck mixing now use fixed-capacity head-cursor FIFOs.
  Steady-state consumption no longer performs `Array.removeFirst` compaction;
  overflow keeps the newest samples within each queue's explicit latency cap.
- **Complete transmitter state ownership (#60)** — `TransmitterModel` v2 now
  exclusively owns all persisted TX user configuration: safety policy,
  antenna/drive, mic/profile/source/file/monitor settings, EQ/effects, and the
  complete processing rack. v1 and individual defaults migrate once, the v2
  snapshot is authoritative, and ephemeral ARM/PTT/TUNE/tail/playback/meter
  state remains outside persistence.

### Tests
- Added ring wrap/overflow/order tests, an Apple M4 Pro bounded-FIFO baseline,
  complaint/tone-evidence fixtures, and v1/legacy/full-v2 transmitter
  migration and validation coverage. Focused Swift tests and a signed Debug
  app build pass without connecting to a radio or emitting RF.

## [2026.0812_009] — 2026-08-12

### Added
- **Operational real-time diagnostics (#62)** — Instruments signposts and
  lock-free counters now cover Protocol 1/2 decode, RX DSP, TX feed/pull,
  CoreAudio capture/render, spectrum, OmniSkimmer, and Metal submission.
  Support information reports sample counts, average/maximum latency,
  deadline misses, drops, underruns, and queue high-water marks without
  formatting or taking a telemetry lock on a real-time path.
- **Debug lock-order enforcement (#61)** — the one permitted nested order,
  `TXChain.lock` then `TXChain.ringLock`, now uses ranked locks that trap on
  inversion, recursion, or non-LIFO release in Debug builds while preserving
  plain `NSLock` behavior in Release.

### Changed
- **Transmitter state ownership (#60)** — `TransmitterModel` now exclusively
  owns the versioned SWR-protection and operator-policy snapshot, migrates the
  legacy defaults, and builds the immutable policy consumed by
  `TXCoordinator`. `RadioState` remains an observing compatibility facade;
  ARM, PTT, TUNE, trip, and tail state still cannot persist.
- **Concurrency inventory (#61)** — replacing TXChain's two independently
  constructed locks with the ranked wrapper reduces source lock constructions
  from 48 to 47; cross-component nested locks remain forbidden.

### Tests
- Added deterministic counter/summary/deadline tests, transmitter migration,
  ownership, and coordinator-policy tests, plus positive and adversarial
  lock-order policy coverage. Focused tests and the unsigned Debug app build
  validate the new paths without connected-radio or RF-emission claims.

## [2026.0812_008] — 2026-08-12

### Added
- **Deterministic real-time benchmark (#62)** — added an opt-in release
  harness for Protocol 1/2 packet decode plus 192 kHz RX and 48 kHz TX DSP
  blocks. JSON reports capture p50/p95/p99/max timing, CPU time, post-warm-up
  allocator growth, and enforced p99 deadlines; the first Apple M4 Pro
  baseline and methodology are documented in `docs/RealTimePerformance.md`.
- **Typed receiver ownership (#60)** — `ReceiverModel` now exclusively owns
  versioned VFO, mode/filter, rate/zoom, gain/attenuation/antenna, split,
  RIT, and XIT configuration plus transient tuning geometry. Existing
  `RadioState` properties remain an observing compatibility facade and legacy
  defaults migrate into the typed snapshot.

### Changed
- **Adaptive RF Vision workload (#14)** — resource presets now cap optional
  RF Vision analysis at 10/20/30 rows per second, falling with memory pressure
  without changing live RX or TX. Admission uses monotonic arrival time while
  replay age remains the detection timestamp; UI/support diagnostics separate
  policy shedding, queue overflow, and processing failures.
- **CI benchmark smoke (#62)** — the smoke script runs packet/resource tests
  and the real-time benchmark in release mode, requires a non-empty JSON
  report, and excludes compilation time from the deadline window.

### Tests
- Added receiver snapshot migration/validation/ownership tests, deterministic
  RF Vision cadence and pressure-policy coverage, and four opt-in percentile
  benchmark scenarios. Debug and release app builds plus the full Swift test
  suite validate the compatibility facade without connected-radio claims.

## [2026.0812_007] — 2026-08-12

### Added
- **Guided calibration fitting (#65)** — CAL PROFILE now captures operator-
  approved forward-power and PA-current points without controlling PTT,
  rejects invalid/duplicate/non-monotonic evidence, fits the production
  detector models, and displays RMS/maximum residuals before the operator
  applies them. Raw points round-trip through identity-bound CSV and remain
  embedded in JSON profile backups.
- **Concurrency ownership inventory (#61)** — added a reproducible audit of
  unchecked Sendable declarations, locks, queues, timers, and unsafe-buffer
  sites, plus documented control/real-time ownership and transition lock
  ordering in `docs/ConcurrencyOwnership.md`.

### Changed
- **Station configuration ownership (#60)** — the main-actor
  `StationConfigurationController` now exclusively owns station identity,
  reporting preferences, typed per-band memories, the calibration catalog,
  active physical-radio profile, and persistence/recovery status. Legacy band
  dictionaries migrate without losing compatibility. `RadioState` remains an
  observing compatibility facade rather than a second source of truth.
- **Discovery concurrency contract (#61)** — discovery targets are immutable,
  callback payloads are Sendable, and the queue/main-actor safety invariant is
  explicit. Raw PA-current AIN counts are retained only as calibration
  evidence; display trust behavior remains unchanged.

### Tests
- Added exact forward-power and PA-current fit fixtures, residual/error and
  hostile-evidence checks, quoted CSV/identity round trips, independent
  station-controller calibration and band-memory migration/persistence
  coverage, and a gate requiring every unchecked Sendable type to remain
  classified in the ownership inventory.

## [2026.0812_006] — 2026-08-12

### Added
- **Calibration editor and interchange (#65)** — TX Controls now edits the
  connected radio's S-meter offset, forward-power constant, PA-current
  slope/offset/trust floor, equipment/notes, and per-frequency/path drive
  ceilings. Profiles import/export as validated versioned JSON and reject a
  different physical identity, board profile, or firmware.
- **Formal Digital TX profile (#66 milestone 4)** — the new 200–3000 Hz
  Digital profile enforces a voice-processing bypass inside `TXChain`, even
  when saved voice controls remain enabled; only channel filtering and the
  lookahead safety limiter remain. A reproducible WSJT-X/virtual-audio setup
  and off-air diagnostic are documented in `docs/DigitalModes.md`.
- **Session lifecycle domain (#60)** — `RadioSessionController` now owns
  discovery results/diagnosis, connection status, and selected identity/
  profile behind the existing `RadioState` facade. Independent generation
  tokens reject discoveries and completions from stopped or superseded
  sessions.

### Changed
- **Per-radio telemetry conversion (#65)** — P1/P2 connections receive the
  active physical radio's detector calibration before streaming and use it
  for forward watts, PA-current conversion, and trust-floor display. Live
  edits install atomically; protocol-global constants remain migration-only
  compatibility values.
- **CAT failure safety (#66)** — rigctl tracks the TCP client that asserted
  PTT and force-unkeys through the normal coordinator callback if that client
  quits, disconnects, or fails. Digital-profile PTT requests are typed as
  digital at the coordinator boundary.
- **Connection callback hardening (#60/#61)** — ADC-overflow delivery now
  carries the same engine connection-generation check as hardware key,
  forced-unkey, and protection callbacks.

### Tests
- Added detector conversion/trust-floor and calibration JSON interchange
  fixtures, stale discovery/connection generation tests, a hostile-control
  Digital profile bypass test, and CAT-owner disconnect-unkey coverage.

## [2026.0812_005] — 2026-08-12

### Added
- **Per-radio calibration foundation (#65)** — versioned calibration profiles
  are keyed by stable radio identity, board profile, and reviewed firmware,
  stored atomically in Application Support, and migrated from the former
  protocol-global S-meter/forward-power values as legacy/unverified data.
  Invalid or unknown-schema catalogs fail closed while preserving a recovery
  copy. Optional frequency/path drive limits feed the centralized TX policy,
  and support information states the active calibration provenance.
- **Region-aware operator TX policy (#66 milestone 5)** — the operator can tag
  confirmed station ranges with an IARU region or Custom context and choose
  Off, Warn, or Inhibit behavior. Split/XIT-aware decisions apply to every key
  source through `TXCoordinator`; warning mode remains visible without
  bypassing other interlocks, while inhibit and calibration-limit decisions
  cannot produce a key effect.

### Changed
- **First application-state extraction (#60)** — station identity/reporting
  and persisted transmitter safety policy now live in independent, Codable
  domain models. `RadioState` remains a compatibility facade and preserves
  the existing defaults while writing authoritative versioned snapshots;
  ephemeral ARM/PTT state remains solely in `TXCoordinator`.

### Tests
- Added per-radio/IP/firmware isolation, atomic round-trip, corrupt-store
  recovery, non-finite input, drive-limit, model-persistence, policy boundary,
  warning/inhibit, every-source, and coordinator choke-point tests.

## [2026.0812_004] — 2026-08-12

### Added
- **Board- and firmware-aware radio profiles (#59)** — discovery identity now
  follows a radio through UI, engine, and protocol connections; validated HL2
  and Orion MkII profiles centrally define DDC/ADC layout, rates, gain and
  frequency ranges, antennas/Alex, telemetry, quirks, and TX support. Unknown
  boards and manual hosts default to receive-only without PA/Alex/TX commands,
  and support information records the stable identity and match rationale.
- **Authoritative transmit coordinator (#58)** — a pure state/event/effect
  machine now coordinates UI, CAT, hardware, keyboard, voice/CW, TUNE, and
  TWO-TONE requests. Typed policy refusals cover connection, replay, radio,
  build, mode, hardware/operator frequency limits, protection, and TX INHIBIT;
  generation-checked tails preserve roger beeps while stale callbacks cannot
  affect a later over. The TX panel adds an optional persistent operator
  frequency envelope, and support bundles include recent TX transitions.

### Changed
- **Transmit hot paths (#53)** — completed an implementation and regression
  audit of the previously landed split-lock/vectorized TX path and its
  documented dummy-load validation; focused TX/voice/C-QUAM tests remain green.

### Tests
- Added radio-profile resolution and receive-only virtual-radio tests plus
  exhaustive/adversarial TX coordinator tests for policy denial, ownership,
  protection, watchdog, disconnect/restart/termination, tail preservation, and
  stale generations. Existing P1/P2 virtual lifecycle and wire-safety tests
  remain green.

## [2026.0812_003] — 2026-08-12

### Fixed
- **Hosted release publishing targets the download repository (#63)** — the
  release workflow's publish stage was creating its GitHub release on the
  private source repository with auto-generated notes. It now publishes to
  `dzcassell/HermitSDR-releases` via a dedicated `RELEASES_REPO_TOKEN`
  environment secret (the default workflow token cannot write cross-repo),
  points the tag at that repository's empty anchor commit so tag archives
  contain no source, and takes release notes from the version's CHANGELOG
  section — refusing to publish if the section is missing.

## [2026.0812_002] — 2026-08-12

### Added
- **Adaptive resource budgets (#64)** — Conservative, Balanced, and Maximum
  are now live operating policies rather than advisory estimates. HermitSDR
  sizes IQ history and waterfall textures against unified-memory and Metal
  limits, rate-limits waterfall work, sheds optional history under pressure,
  and reports every degradation in Performance Budget and support bundles.
  IQ history uses a single virtual-memory reservation and falls back to a
  shorter safe duration if the requested allocation cannot be made.
- **Deterministic virtual radios (#57)** — production Protocol 1 and Protocol
  2 packet codecs now have typed malformed-packet failures and run unchanged
  against deterministic, manually stepped virtual transports. Golden captures
  and lifecycle tests cover connect, receive, rate/receiver reconfiguration,
  key/unkey safety, SWR/TX inhibits, sequence wrap, loss, duplication,
  truncation, reordering, restarts, stalls, and wrong-source traffic without
  touching RF hardware.
- **Release and extended CI gates (#63)** — CI now compiles both Debug and
  unsigned Release apps. Weekly/manual AddressSanitizer, ThreadSanitizer,
  deterministic benchmark, dependency/license, and secret audits preserve
  failure diagnostics. A protected release workflow performs a reproducible
  dry run before its separately permissioned signing, notarization, checksum,
  metadata, DMG, and immutable GitHub Release stages; the operator runbook
  documents local equivalents, retry, and rollback.
- **Stable workflow status badges (#63)** — README now exposes the current CI,
  extended-quality, and release-workflow results after all three gates passed
  on the completed implementation.

### Fixed
- **Virtual-radio lifecycle hardening (#57)** — Protocol 1 rejects traffic
  from the wrong source port as well as the wrong host; Protocol 2 virtual
  streams exercise both configured receivers; retune, rate/receiver changes,
  reconnects, and autonomous P1/P2 watchdog unkeys have named regressions.
- **Bounded IQ-history replacement (#64)** — sample-rate changes now release
  the old RX chain and mmap-backed history before allocating the replacement,
  avoiding a transient double allocation at high rates.
- **Hosted extended gates (#63)** — repository auditing no longer assumes
  ripgrep is installed on GitHub runners, and the deterministic benchmark
  measures the warmed test workload rather than charging cold compilation
  against its runtime threshold.
- **Agent changelog discipline** — repository guidance now requires every
  landed code, test, documentation, build, CI, or workflow change to update
  this changelog in the same commit.

## [2026.0812_001] — 2026-08-12

### Added
- **RF Vision click actions (#14)** — every detection now dispatches, not
  just tunes. Each panel row (and the right-click menu on rows and the
  waterfall overlay bands) offers: **open the matching decoder** (CW-shaped
  → CW decoder, FSK-shaped → RTTY decoder, FT8-shaped → FT8 spots panel),
  tuned first so the audio lands in the decoder's passband; **rewind to
  signal start** — the RF time machine jumps to 5 s before the region first
  appeared and replays it through the live chain; and **pin + export** —
  the event joins the time machine's pinned-events list (with the same
  expiry handling as decoder bookmarks) and its IQ writes out immediately
  as a bounded `.hiq` + `.json` sidecar. Signals older than the ring clamp
  to the oldest buffered RF instead of refusing.
- **Time-shift-proof detection times (#14)** — RF Vision rows are stamped
  with their data's true age at the spectrum tee (the same stamp the
  waterfall renderer takes), so regions detected during a rewind report
  the signal's historical wall-clock time. Pinned by a regression test.
- **Performance Budget window (#64)** — Tools ▸ Performance Budget feeds
  the advisory estimator with this Mac's unified memory, Metal's
  recommended GPU working set, and the live sample-rate/receiver
  configuration: RAM/GPU targets, affordable IQ-history depth, the current
  waterfall texture footprint, GPU headroom or overage, analysis lanes,
  plus Metal's live allocation as ground truth. The Conservative/Balanced/
  Maximum preset persists (`resourceBudgetPreset`). Still advisory only —
  nothing resizes at runtime yet.

### Fixed
- **RF Vision panel overflow** — the main window gave the panel a 340 pt
  slot while the panel itself insisted on 410 pt (since 2026.0810_004's
  six-way sort row), so it overhung the waterfall by ~70 pt. The slot now
  matches the panel width (470 pt, including the new action buttons).

## [2026.0810_006] — 2026-08-10

### Fixed
- **CI Xcode compatibility (#63)** — the full app build now runs on the
  GitHub-hosted macOS 26 ARM image with Xcode 26.6, matching HermitSDR's
  use of the macOS 26 Speech framework APIs.

## [2026.0810_005] — 2026-08-10

### Fixed
- **CI environment scoping (#63)** — the diagnostics directory now uses
  the `runner` context only at step scope, allowing GitHub Actions to
  validate and start the workflow.

## [2026.0810_004] — 2026-08-10

### Added
- **CI foundation (#63)** — GitHub Actions now runs the complete Swift
  package test suite and an unsigned Debug app build for pushes to `main`,
  pull requests, and manual dispatches. Runs cancel when superseded and
  preserve test logs plus the Xcode result bundle on failure.
- **RF Vision sort completion (#14)** — the detection panel can now order
  regions by lifetime, novelty (most recently first observed), or classifier
  confidence in addition to SNR, frequency, and signal family. All six pure
  ordering rules have deterministic tie-breakers and regression tests.
- **Advisory resource budgeting foundation (#64)** — pure, tested
  Conservative/Balanced/Maximum estimates cover IQ-history RAM, the current
  waterfall texture footprint, GPU headroom/overage, receiver count, and
  optional-analysis concurrency. This milestone reports plans only; it does
  not resize live buffers or react to memory pressure.

### Fixed
- Removed the duplicate `Recording/IQFile.swift` entry from the Swift package
  source manifest.

## [2026.0810_003] — 2026-08-10

### Added
- **DSB (double sideband, suppressed carrier) mode**, receive and
  transmit. Transmit is the textbook case: the band-limited, limited
  audio IS the wire (I = x, Q = 0) — both sidebands, ≥40 dB carrier
  suppression (pinned), and the true-peak limiter bounds the wire
  directly since no Hilbert means no analytic-envelope regrowth. Receive
  is zero-beat product detection: a symmetric passband and the real part
  of the complex baseband, which is a coherent product detector with a
  0 Hz LO — both sidebands add in phase when tuned on frequency. The
  roger beep rides the same real modulator. Filter 2–11 kHz (default
  6 k, own memory group); CAT `DSB` (hamlib-native name). New
  `DSBChainTests` (4): loopback recovery, carrier suppression, sideband
  symmetry within 1 dB, wire bound. Mode row is now eight segments wide;
  main window minimum width 1365 → 1410.

## [2026.0810_002] — 2026-08-10

### Added
- **FM and Narrow FM (NFM) modes**, receive and transmit. Receive: both
  flavors demodulate at a **24 kHz IF** — the decimation cascade stops one
  stage early so the full Carson bandwidth of ±5 kHz-deviation FM
  (~16 kHz) fits, where the 12 kHz IF caps channels at 11 kHz — through a
  quadrature discriminator, −6 dB/oct de-emphasis, and a final ÷2 back to
  the 12 kHz audio chain. The S-meter and squelch read the channel
  envelope (carrier power — proper FM squelch behavior), and manual IF
  notches are deliberately inert ahead of the discriminator. Transmit: a
  phase-continuous constant-envelope modulator behind the same ARM/PTT
  interlocks; +6 dB/oct pre-emphasis sits ahead of the leveler (the NRSC
  arrangement) so the true-peak limiter's 0.95 ceiling doubles as the
  deviation cap — rated ±5 kHz (FM) / ±2.5 kHz (NFM), and the transmitter
  cannot over-deviate. The roger beep FM-modulates with click-free carrier
  ramps. Filter widths: FM 8–20 kHz (default 16 k), NFM 3–12.5 kHz
  (default 11 k), remembered per mode group. CAT: `FM`/`PKTFM` and
  `FMN`/`NFM` select the modes; NFM reports as plain `FM` (hamlib has no
  narrow name). New `FMChainTests` (7) pin loopback recovery, the
  deviation bound, constant envelope, channel occupancy, emphasis
  flatness, and a deviation-meter self-check — which caught a
  stride-aliased spectrum scan reading phantom splatter before it could
  lie (the sensitivity-check rule pays again).

### Fixed
- **OmniSkimmer and RF Vision panels no longer squat on the waterfall
  after their features are switched off.** The enable toggles opened
  their panels but never closed them; the panel now follows the feature
  both ways, and a panel can no longer render at all while its engine is
  off.

### Changed
- The Crab now keeps sand between his claws: sea, marine, seafood, and
  beach puns are part of the house style — one or two per reply, never at
  the cost of a clear answer.

## [2026.0810_001] — 2026-08-10

### Added
- **C-QUAM matched difference chain (#32 milestone 4)** — reviewed and
  approved, promoted from the staged TX commit. In AM stereo the L−R
  difference channel now experiences the same net processing as the sum:
  linear stages (phase rotator, voicing + user EQ, NRSC emphasis, both
  profile bandpass passes) are cloned with their own filter state, and
  the nonlinear stages' composite gains are recovered per sample as
  guarded out/in ratios over three spans of the sum path (gate + platform
  AGC, de-esser, compressor→limiter with the 120-sample lookahead folded
  into the alignment) and applied to the difference in stage order. The
  multiband leveler — whose per-band gains and LR4 crossover allpass
  phase cannot collapse to a scalar trace — is reproduced exactly by a
  slaved clone driven by the sum instance's recorded per-band gain
  traces. Stereo separation through the full production loopback:
  collapse → ~20 dB (pinned >15 by
  `testFullLoopbackSeparationWithMatchedDifferenceChain`); right-only
  content at the 1600 Hz 5-band crossover: 23.5 dB (pinned by
  `testFullLoopbackSeparationWithFiveBandMultiband`). Hardware-validated
  2026-08-04 on the dummy load at 0.3 W with the full broadcast stack
  live: L-only 35.5 dB / R-only 32.4 dB separation, correct orientation,
  pilot −28 dBc, dual-mono mono-compatibility margin 41 dB. With C-QUAM
  off (or any non-AM mode, or a mono source) the new code costs one nil
  check per block and the wire is untouched. On-air antenna L/R
  validation remains the last open item on #32.

## [2026.0809_001] — 2026-08-09

### Fixed
- **YouTube Stream Health: "The audio stream's current bitrate (0) is
  lower than the recommended bitrate."** Two independent defects, both
  real, and the first one alone explains the literal zero.

  1. **`onMetaData` never declared `audiodatarate`.** Video declared
     `videodatarate`; audio declared its codec and sample rate but not its
     bitrate, so YouTube's health panel had nothing to report and printed
     **0** — while perfectly good audio was arriving and playing back.
     The metadata now carries `audiodatarate`, `audiochannels`,
     `audiosamplesize` and `duration` (0 = live), and `stereo` is derived
     from the channel count instead of being hardcoded false.
  2. **The AAC encoder was running at 64 kbps.** `AVAudioConverter`
     defaults AAC-LC to 64 kbps and the encoder never set a rate
     (measured on this machine: `bitRate` 64000 out of the box). That is
     half what YouTube asks for, so even once the rate was declared the
     warning would have stood. It now requests 128 kbps, choosing the
     lowest *applicable* rate that meets the target rather than assuming
     128000 is on offer — the applicable set depends on channel count and
     sample rate. Verified end to end: 117 kbps actual on program-like
     material, up from 19 kbps.

  The declared rate is read back from the converter rather than assumed,
  so a stream can never advertise 128 while sending 64. The startup
  diagnostic now prints the negotiated audio format and warns if it
  landed below 128.

## [2026.0808_002] — 2026-08-08

### Fixed
- **CESSB's user-facing description no longer overclaims.** The toggle
  tooltip, the TX Audio Chain stage help, and the `txCESSBEnabled` doc
  comment all promised "~2–3 dB more average talk power at the same PEP".
  Measured (2026.0808_001), it delivers −0.09 dB of talk power and
  3.9–10.6 dB less out-of-band energy. All three now describe it as the
  cleanliness feature it is, so nobody enables it expecting to be louder.

### Added
- `AMPumpingTests` — an objective probe for hypothesis 2 of #38 (watery
  75 m AM TX audio: "the unvalidated 5.10 broadcast rack is pumping").
  Wateriness is measured as gain-trace modulation in the 0.3–8 Hz swirl
  band: recover the audio a listener's detector would hear from the
  transmitted analytic pair, divide by the source envelope, and look for
  energy at syllabic-and-slower rates.

  **Result: the rack is largely exonerated.** Against the same profile and
  the same real-voice program, platform AGC, 3- and 5-band multiband, the
  de-esser, the gate, Hall Reverb, and the full stack together all land
  within **−0.58 to +0.35 dB** of the bare profile. Hall Reverb actually
  *reduces* the number, which is what a reverb tail should do to envelope
  modulation. Nothing here behaves like a pumping rack.

  The metric ships with its own sensitivity check
  (`testSwirlMetricDetectsKnownPumping`), because a null result is only
  worth anything if the instrument could have seen a positive one: it
  reads 0.000 dB on a flat gain trace and 0.83 / 1.65 / 3.30 dB for
  injected 1 / 2 / 4 dB wobble at 3 Hz, localizing the rate to within
  0.1 Hz. So a real pumping artifact of even 1 dB would have been visible,
  and none of the rack configurations produced one.

  Two measurement notes recorded in the test for whoever measures this
  next: the AM envelope is mostly CARRIER, so dividing it by a source
  envelope yields a trace dominated by 1/source that is identical no
  matter what the rack does (every configuration read 5.84 dB before the
  detector was added); and the cross-profile numbers the sweep also prints
  are bandwidth-confounded and deliberately marked not-for-ranking.

  This does not close #38 — it removes the one hypothesis that could be
  tested without a radio, an ionosphere, and an ear, which leaves
  selective fading (the original favourite) in front.

## [2026.0808_001] — 2026-08-08

### Changed
- **CESSB's documented benefit corrected: it is a cleanliness feature,
  not a talk-power feature.** The 3.80 notes claimed 2–3 dB more average
  power at equal PEP. Measured on a dummy load (SquareSDR 2, 3.885 LSB,
  own-signal IQ recorded through the receiver and analysed offline) and
  then again offline on real off-air voice through the production
  `TXChain`, CESSB delivers **−0.09 dB** of talk power at equal PEP —
  i.e. nothing. On a two-tone it is bit-identical with CESSB on and off,
  which is expected: the 3.80 lookahead limiter already caps the envelope,
  leaving CESSB nothing to clip.

  What it *does* deliver is real and worth keeping. The always-on wire
  guard (which trims analytic-envelope overshoot to 1.0 before the Int16
  conversion) stops having to engage at all — 0.051% → 0.000% of samples
  on a bare chain, 0.154% → 0.000% on the full broadcast stack — and
  out-of-band energy drops **10.6 dB** (bare) / **3.9 dB** (broadcast
  stack). The guard is a zero-attack gain modulation, so every sample it
  touches is splatter that no upstream filter can still clean up; CESSB's
  job in this chain is to prevent that, not to raise average power.

### Added
- `CESSBRealVoiceTests` — measures CESSB through the production chain on
  a real off-air aircheck, in both a bare and a fully-loaded configuration.
  Asserts only the physics (CESSB must never raise PEP, never destroy
  average power, never leave the wire guard *more* to clip) and prints the
  dB figures, since how much there is to reclaim is a setting rather than
  an invariant. The aircheck is not bundled; the test skips without it.

  Ships with two ruler checks that exist because each caught a wrong
  answer during this work, and any future TX measurement is liable to
  repeat them: `testSplatterAnalyzerSelfCheck` (known-spectrum tones
  through the analyzer) and `testHarnessCleanlinessWithPureTone` (a pure
  sine through the real chain must come out pure). The three traps were:
  feeding a long clip in one call and pulling it back measures **silence**
  (the IQ ring holds ~4 s, so a 41 s push is dropped and `pull` zero-pads
  — 1,987,200 samples returned, 192,000 non-zero); feeding one block and
  immediately pulling one block **starves the ring** (the Hilbert pair
  alone is 1025 taps, so prime first); and assuming which sideband carries
  USB **measures the empty one**, comparing two numerical noise floors and
  returning a confident, meaningless number — it read −30 dB out-of-band
  on a tone whose analytic envelope was flat to 0.01 dB.

### Validated on a dummy load (issue #13)
- TUNE: SWR 1.02–1.04, 0.40–0.56 W at 15% drive, carrier PAPR 0.12 dB,
  all other products ≥78 dB down.
- Two-tone at 15/50/80% drive: PAPR 3.05–3.28 dB against a 3.01 dB
  theoretical floor, so the envelope is **not** flat-topping even at 80%;
  IMD3 −31 to −40 dBc, IMD5 −39 to −47 dBc.
- Speech splatter: −59/−60 dBc immediately outside the passband.
- **The Studio SSB trio, on real RF**: 3.0k flat within ±2 dB from
  200–2900 Hz with 3400 Hz at −46 dB; 2.9k identical but 2900 Hz at
  −2.5 dB, correctly rolling off earlier; ESSB Wide flat out to 3400 Hz.
  All three read −10 dB at 100 Hz, which is the 513-tap bandpass skirt
  sitting on the profile's low corner rather than a defect.
- The TRANSMIT section of the 2026.0807_004 LED meter bridge read
  correctly live while keyed.

  Still requiring a human ear and explicitly NOT covered: gate behaviour
  on word onsets, de-esser judgement, multiband A/B, roger beep with
  CESSB, Optimod AM +125% positive peaks, and rack-unit voicing.

## [2026.0807_005] — 2026-08-07

### Added
- **Receive squelch beside the RF gain.** The squelch DSP has existed
  since 3.x (dBm threshold → dBFS, 6 dB hysteresis, 10 ms ramps) but was
  only reachable from the DSP popover. It now sits in the control bar
  next to the LNA/RF gain — the pair an operator actually works together:
  set the gain for the band, then set the gate just above its noise
  floor. SQL latch, threshold slider, dBm readout, and a dot that shows
  green while the signal is above the threshold (indicative — the real
  gate carries hysteresis, so it can disagree for a moment right at the
  setting; it answers "why am I hearing nothing").
- **Eight new Arcade FX sprites**, because the shack is a strange place
  at 3 am: a **jellyfish bloom** (three bells on independent pulse
  phases — quick contraction, slow relax, with eight fine tentacles and
  four frilled oral arms lagging behind the power stroke, gonad rings
  and a bioluminescent glow), a **fish hook** that drops from above on a
  line, dangles, twitches hopefully twice and reels back up with
  nothing, plus a **flying toaster** (After Dark, wings and all,
  launching a slice mid-flight), a **UFO** that tractor-beams a scrap of
  spectrum away, a **banana FOR SCALE**, a **shark fin** cutting a wake
  across the waterfall, a **sasquatch** peeking over the panadapter
  edge, and a **portal** that opens in the noise floor and waves a
  tentacle. Three carry new achievements. The critter cadence also
  tightened (was one per 5–12 min, now one per ~3–7) since the roster
  more than doubled.

## [2026.0807_004] — 2026-08-07

### Changed
- **The Multimeter is now a collapsible stack of LED segment meters**
  (SmartSDR-style), replacing the single-function analog dial. One
  needle showing one quantity meant knowing in advance which reading
  mattered — and while transmitting, they all do.
  - Three collapsible sections: **RECEIVE** (signal in S-units, signal in
    dBm, AF gain, attenuator), **TRANSMIT** (forward power, SWR, mic
    level, ALC, compression, talk power) and **PA / HEALTH** (temperature,
    drain current, forward and reverse volts).
  - Each meter is a scale row with the numbers at their true positions
    and the name centred, over a 48-segment bar that lights cyan and
    turns **red past the danger threshold** — with the scale numbers in
    that zone red too, exactly like the reference. A white peak-hold
    marker rides the bar and decays after 1.6 s.
  - The stack **follows the radio**: TRANSMIT opens the instant RF is hot
    (`txRFHot` — keyed or inside the unkey tail) and RECEIVE returns on
    unkey, so stale TX numbers are never presented as current. The
    audio-chain meters read while ARMED, not just keyed, because that is
    when mic gain gets set.
  - Non-linear scales are honest: power on a square-root curve so a QRP
    rig isn't squashed into two segments, SWR spaced by reflection
    coefficient the way a real meter is printed. `LEDMeterScaleTests`
    (11) pins the mappings, the danger zones and the S-unit convention
    (S9 = −73 dBm, 6 dB per unit).
  - No data reads "—" on a dimmed bar rather than a confident zero, and
    PA current still respects the #34 trust floor.

### Fixed
- Views must not read `engine.isConnected` directly — the engine is not
  an ObservableObject, so the window sat on "Not connected" through a
  live connect. The meters read the published `status`/`replayingName`.

## [2026.0807_003] — 2026-08-07

### Fixed
- **Ask The Crab was a narrow island in a comically wide window.** The
  view declared a fixed `.frame(width: 420)` while the window itself
  restored a much larger saved frame (900 pt), so the chat sat marooned
  in the middle with dead margins either side and a prompt box that used
  a fraction of the real estate.
  - The content is now flexible (min 360, ideal 460) and fills whatever
    the window is, so no size looks broken.
  - The window opens at a sensible 460×560 and is resizable down to its
    content minimum rather than pinned to it.
  - Bubbles hug their text with Spacer gutters instead of stretching to
    the full width: a one-word reply and a long answer both read
    correctly, and line length stays comfortable as the window widens.
  - The stale saved 900-pt frame is cleared, so the tidy default
    actually takes effect rather than being overridden on open.

## [2026.0807_002] — 2026-08-07

### Added
- **"Tune back to the last frequency" actually works.** The crab had no
  notion of a previous frequency, so asked to go back it did the only
  thing it could: read the current frequency out of its own telemetry
  line and *narrate* a tune it never performed — no tool call, no
  receipt, and (verified against CAT) a radio that never moved.
  - New `TuningHistory`: a bounded stack of frequencies the operator
    actually **parked** on. RadioState records a position once tuning
    settles for 2 s, so a scroll-tune sweep doesn't fill the history with
    every sample, and moves under 500 Hz count as the same spot (RIT
    nudges and click-tune snapping don't manufacture entries).
  - New `tune_back` tool + `.tuneBack` command, in the router's **core**
    set so any phrasing of "back" reaches it.
  - Semantics are browser-back, not A/B toggle: repeated calls walk
    further back, and running out says so rather than inventing a
    destination.

### Fixed
- **A tune to the frequency the radio is already on now says so.** It
  used to report "Tuned to 7.2000 MHz" — a no-op that read as success,
  which is precisely the fiction the ✓ receipt system exists to prevent.
  It now answers "We're already on 7.2000 MHz — I didn't move the radio",
  and points at `tune_back`.
- The live telemetry line now carries the **previous parked frequency**.
  Tool descriptions alone did not move the on-device model off
  `tune_radio` for "go back" (tested), but handing it the *fact* lands
  the tune correctly whichever tool it reaches for — the same lever that
  fixed the band-name guess yesterday.

## [2026.0807_001] — 2026-08-07

### Fixed
- **The crab's context-window failure, properly this time.** The
  2026.0804_004 fix trimmed the *instructions* and missed the real cost:
  every one of the **42 tools** spends its name, description and
  parameter schema from Apple's small on-device window *before the
  operator's question arrives*. A completely fresh session overflowed on
  "How are you" — which is why the reset-and-retry couldn't save it and
  the in-character "too big a bite" line kept coming back. Slimming the
  instructions had bought ~700 tokens against a shortfall several times
  that.
  - New `CrabToolRouter`: the crab is handed a **per-question subset** —
    six always-on core tools (tune, nudge, mode, band, volume, status)
    plus whatever the question's words point at, capped at 14. Sessions
    are reused while the toolset still covers the question, so follow-ups
    keep their conversational context; a question needing something new
    rebuilds.
  - `CrabToolRouterTests` pins the budget, that the routing table only
    names tools that exist, and — the one that matters when tool #43
    arrives — that **every registered tool is reachable**, since a tool
    in no topic row is silently never offered to the model.
  - Verified live: "How are you", "what band am I on?", "set the volume
    to 40" (with its ✓ receipt), "who is on the cluster?" and "which band
    is open right now?" all answer normally again.
- **"What band am I on?" answered wrongly.** The live telemetry line
  prepended to every question carried raw megahertz and no band label,
  and the on-device model cannot do that mapping — at 27.385 MHz it
  confidently said "160-meter band". The line now carries the band label,
  and says *"outside the ham bands"* when there isn't one, because an
  absent fact is what invited the guess.

## [2026.0806_002] — 2026-08-06

### Added
- **Experimental Modes lab gate** (Tools ▸ Experimental Modes) — the
  master interlock for the CASCADE arc, built *before* any transmit path
  exists on purpose: an interlock added after the fact is one nobody
  trusts. Off by default. Enabling it presents a disclaimer naming the
  real hazards (up to 48 kHz occupied, not a mode anyone else can
  decode, the operator's own licence responsibility) that must be
  accepted before the modes open; the accepted revision is recorded, so
  rewording the warning re-asks. A dummy-load / closed-network
  affirmation is required **every launch** and deliberately never
  persisted — that's a statement about right now, not a preference.
  The mode list is honest about what exists (DUET and ARIA are tagged
  "not built yet") and every row states, in plain words, why it cannot
  transmit. `ExperimentalGateTests` (8) pins the fail-shut defaults and
  the load-bearing rule: **no experimental mode can key the radio under
  any gate configuration today**, because nothing wires CASCADE to the
  transmitter. A future transmit path has to consciously rewrite that
  test.
- **LUMEN mode window** — the progressive image mode's face. Load any
  image (downscaled to 320 px on the long edge; LUMEN sends pictures
  over tens of kbit/s, so a camera frame would be meaningless), pick a
  quality, and read the real numbers: bytes and seconds on the air per
  pass, computed from the production CASCADE throughput model. "Play
  transfer" paces the passes by their true on-air duration and paints
  the picture in exactly as a receiving station would see it —
  measured on a 320×240 test card: **8 passes, 21.7 kB, 1.2 s total,
  with a recognizable picture after 0.08 s.** The receiving side is a
  single accumulating `LumenDecoder`, like a real receiver, and reports
  live PSNR against the source. Nothing here touches the radio.
- `LumenImageBridge`: NSImage ↔ planar YCbCr 4:2:0 with box-averaged
  chroma (point sampling aliased hard on the sharp edges these test
  cards are full of).

## [2026.0806_001] — 2026-08-06

### Changed
- **The 30-day expiry now degrades to receive-only instead of quitting.**
  A hard wall took the *receiver* away from an operator mid-net (or
  off-grid with no bandwidth for a 9 MB dmg) for a reason that was only
  ever about stale TX code reaching the air. The new shape:
  - **Days 0–23**: normal.
  - **Days 23–30**: "stops transmitting in N days" nag strip.
  - **Days 30–90**: **receive-only.** The receiver, decoders, streaming
    and everything else keep working; the transmitter is locked out at
    the arming interlock and a persistent strip says so and counts down
    to the hard stop.
  - **Day 90+**: the app stops entirely, as before.
  - **Tampering is unchanged** — a positively invalid signature still
    refuses to run immediately, with no grace window.
  - An **implausible clock** (dead PRAM battery) now locks TX but never
    hard-stops: we can't trust a reading we don't believe, and a
    locked-out transmitter is already safe.
  - The TX lockout is a pure refusal at `applyTXArm`, the single arming
    choke point — it can only ever prevent emission, never cause it, and
    it sits outside the TX signal path. CAT PTT and the hardware KEY jack
    are covered transitively (both require an armed transmitter).
  - `BuildLifecycleTests` grew to 15: the grace window, the hard-stop
    boundary, the countdown, and that tampering gets no grace.

### Fixed
- The lifecycle strip is now a `safeAreaInset` rather than an overlay —
  as an overlay it sat **on top of** the header controls (measured: it
  covered Ask The Crab and the record button), which would have been
  unacceptable for a strip that can be up for 60 days.

## [2026.0804_005] — 2026-08-04

### Added
- **Build lifecycle timer (dev-cycle expiry).** Every build now stops
  working **30 days after its release date** and sends the operator to
  the download page, with a nag strip over the last 7 days. Beyond
  "hams are stubborn": this is a transmitter control app under heavy
  development, a months-old build can carry a known TX defect onto the
  air, and there is no other way to reach an operator who never updates
  (Xcode betas and TestFlight work the same way).
  - The build date is parsed from the version string itself
    (`YYYY.MMDD_XXX`), which lives in the code-signed Info.plist —
    editing it to buy time breaks the signature.
  - **Anti-rollback**: the verdict runs against the LATEST time ever
    seen, not the current clock. That high-water mark lives in three
    independent stores (UserDefaults, the Keychain, an Application
    Support file) plus any server `Date` header the app already
    receives (update check, cty.dat refresh — no new network calls);
    the max wins, so winding the Mac back buys nothing. An implausible
    future reading (dead PRAM battery) is never persisted, so one bad
    clock can't brick an honest operator forever.
  - **Anti-patch**: release builds verify their own Developer-ID
    signature. Only a POSITIVE seal failure walls the app; inconclusive
    results are treated as fine — bricking a legitimate operator over a
    Gatekeeper quirk would be worse than letting a patched build run.
  - **TX-safe**: expiry disarms the transmitter and stops any stream
    before the wall appears, so it can never strand a keyed radio.
  - Fails OPEN on anything it can't parse; `BuildLifecycleTests` (12)
    pins the boundaries, the rollback rules and the fail-open policy.
  - Debug-only `HERMITSDR_LIFECYCLE_RESET=1` clears the rollback
    history for testing (no such door in release builds; it cannot
    extend a build in any case).

### Fixed
- Two launch-path bugs found while testing the above, both pre-existing
  hazards this feature would otherwise have inherited: an `.overlay`
  view does not reliably inherit `@EnvironmentObject` (it crashed on
  launch — the banner now takes its dependency explicitly), and a
  Keychain read on the launch path can wedge the app **invisibly** on an
  authorization prompt (measured: alive, no window, no explanation).
  The project rule already said secrets are read lazily; the lifecycle
  guard now honors it, reading the Keychain off-thread after launch.

## [2026.0804_004] — 2026-08-04

### Fixed
- **The crab's "Exceeded model context window size" snag.** The
  instructions had grown a ~3,600-character per-tool capability
  enumeration — pure duplication of the 35 tools' own self-describing
  schemas, all sharing Apple's small on-device context window — until a
  fresh session barely fit and the reset-and-retry couldn't save it.
  Three-part fix: (1) instructions slimmed 5.1k → 2.3k chars (tools
  document themselves; summary + rules + personality stay); (2) a
  proactive rolling reset retires a long conversation before it
  overflows (chat memory yields to the receipts feed — losing small talk
  beats erroring); (3) if even a fresh session overflows, the crab now
  answers in character ("too big a bite — ask it in a smaller piece")
  instead of leaking a raw error. `AIKnowledgeBudgetTests` pins the
  instructions under 3,000 chars and the load-bearing rules present, so
  tool #36 can't quietly regrow the enumeration.

## [2026.0804_003] — 2026-08-04

### Added
- **LUMEN codec core** (Experimental Modes arc, LAB ONLY — the first of
  the three CASCADE modes): a progressive image codec built to ride
  CASCADE frames. 8×8 DCT + libjpeg-style quality scaling, YCbCr 4:2:0
  (grayscale = luma only), JPEG-style spectral-selection passes — the
  first pass paints every block's DC (an instant thumbnail), each later
  pass sharpens a zig-zag coefficient band, luma before chroma. Byte-
  oriented zero-run + signed-LEB128 entropy coding (FEC/ARQ move whole
  frames, so no bit-level resync needed), DC delta-prediction, self-
  describing payloads decodable in ANY order with duplicates ignored —
  a truncated transfer is a complete, merely softer, picture (pinned:
  progressive PSNR monotonicity, out-of-order equivalence, half-transfer
  renders). One pass survives the full production CASCADE loopback
  (frame → offset + AWGN → sync → decode → pixels). `LumenCodecTests`,
  10 tests. Protocol lesson recorded in-test: pad link frames with a
  PRBS, never zeros — constant bytes collapse OFDM symbols into
  energy-spike deltas that blind the sync detector's energy gate.
  Still to come for LUMEN: the mode window + Lab gate UI, and TX
  plumbing (behind interlocks, after the C-QUAM gate clears).

## [2026.0804_002] — 2026-08-04

### Added
- **Studio SSB profile trio** — broadcast-quality voice inside the
  standard SSB channel widths, for when eSSB is unwelcome but
  "communications quality" undersells the mic: **Studio SSB 2.8k**
  (100–2900 Hz), **2.9k** (100–3000), **3.0k** (100–3100). One shared
  voicing, pick by passband: lows extended to 100 Hz (where most of the
  hi-fi impression lives), +2 dB presence so articulation survives the
  sub-3 kHz top, a whisper of air off the 3.5 kHz shelf's skirt, and the
  Broadcast profile's smooth 3:1 leveling. `testStudioSSBTrio` pins the
  exact edges and that the RF respects the 2.8k channel (2.7 kHz passes,
  3.4 kHz crushed ≥30 dB).

## [2026.0804_001] — 2026-08-04

### Added
- **Media Deck Phase 2 (#24)** — the soundboard grows up:
  - **Exclusive groups** (1–8, across pages): starting a pad fades out
    every other sounding pad in its group — one music bed at a time,
    radio-station style. Each victim rides its own fade-out.
  - **Fades**: per-pad fade-in/out (0–10 s), applied at start and on
    stop/group-bump; STOP ALL (⌘.) still cuts instantly — it's a panic
    switch, not a segue. Fading pads read idle and are restartable
    immediately (a restart plays over the old tail, DJ-style).
  - **Send to stream mix**: a pad toggle that routes its audio through
    the radio's speaker mix instead of its own output device — you hear
    it through the app, and every audioFanout sink (Discord voice,
    YouTube Live) carries it. 12 kHz mono mirror via a pad-mixer tap
    (hand-averaged channels + rate-only AVAudioConverter — the
    MicInput/TXFilePlayer lessons), summed AFTER the keyed-mute zero so
    deck audio survives TX overs. Needs the receiver streaming (the mix
    is packet-paced). Never touches the transmitter — TX routing remains
    a later phase behind interlocks.
  - **Import/export**: the whole deck (pages, pads, trims, groups) as
    pretty-printed JSON — version-gated on import, newer documents
    refused rather than mangled. Audio travels by path, not embedded.
  - Phase-2 model fields are optional keys, so every existing v1
    document decodes unchanged (and older builds ignore the additions);
    document version stays 1. `MediaDeckPhase2Tests` pins groups,
    compatibility, and the round-trip.

## [2026.0803_007] — 2026-08-03

### Fixed
- **Screen saver no longer kills a live stream**: while a YouTube stream
  is up, HermitSDR holds a `PreventUserIdleDisplaySleep` power assertion
  AND re-declares user activity every 30 s
  (`IOPMAssertionDeclareUserActivity`, the VLC playback idiom — the
  assertion alone does not stop the screen saver, only the idle-clock
  reset does). Both engage at go-live and release at teardown through
  `teardownMedia`, so stop() and fail() can never leak the assertion.
  A diagnostics row confirms the hold (or warns with the System Settings
  fallback if the assertion is refused). `StreamKeepAwake.swift`.

## [2026.0803_006] — 2026-08-03

### Added
- **Clublog live most-wanted rankings (#48)**: the rarity flames (spot
  rows, waterfall labels, the Times Square ticker) now rank from
  Clublog's current monthly DXCC most-wanted list — fetched weekly from
  the free JSON endpoint into an App Support cache (the cty.dat idiom),
  bridged ADIF-number→entity-name through a bundled AD1C-aligned
  snapshot (`Resources/adif-entities.csv`), and applied as an exact
  normalized-name overlay on `rarityRank`. The curated static tables
  remain the offline fallback; a status line in the DX cluster window
  shows which list is live. Pure layer `ClublogMostWanted.swift`,
  package-tested.
- **Caption ham vocabulary**: the YouTube caption transcriber now feeds
  Apple's speech model contextual strings — the ITU phonetic alphabet
  (plus the informal phone-net phonetics), Q-codes, band/mode/propagation
  vocabulary, and the callsigns actually in play (station call, last 50
  QSOs logged, last 80 DX spots) — so "whiskey one alpha whiskey" has a
  fighting chance of landing as W1AW. `HamVocabulary.swift`,
  package-tested; wired via `AnalysisContext.contextualStrings`.

## [2026.0803_005] — 2026-08-03

### Added
- **YouTube Live captions + transcript** (account/OAuth mode): the receiver
  audio is transcribed on-device (macOS 26 SpeechAnalyzer/SpeechTranscriber —
  long-form, fully offline, first use downloads Apple's speech model) and
  published two ways. LIVE: the broadcast is created with
  `closedCaptionsType=closedCaptionsHttpPost` and each finalized utterance is
  POSTed to the stream's `closedCaptionsIngestionUrl` (`&seq=N`, UTC-millisecond
  timestamp line + text), so viewers can toggle CC on the player in near-real
  time. VOD: every cue is accumulated into an SRT and uploaded via
  `captions.insert` (multipart, 400 quota units) when the stream ends — that
  track replaces the auto-captions and fills the watch page's "Show
  transcript" panel. The SRT is also always saved to
  `~/Documents/HermitSDR Transcripts/` (upload failures lose nothing).
  "Live captions + transcript" toggle in the YouTube Live window (OAuth mode,
  default on); the whole pipeline degrades gracefully — caption trouble logs
  a diagnostic and never touches the stream itself.
- New pure layer `Integration/YouTube/CaptionFormats.swift` (live-POST wire,
  SRT builder, captions.insert multipart) + caption fields on the
  YouTubeAPI builders — package-tested (`YouTubeCaptionsTests`, 14 tests).

### Changed
- **OAuth scope moved to `youtube.force-ssl`** (superset of the old plain
  `youtube`; `captions.insert` accepts only force-ssl). The granted scope is
  now stored beside the refresh token in the Keychain — an existing sign-in
  is detected as under-scoped and the one-time browser consent re-runs on
  the next Go Live. Approve it once and everything (including captions)
  works as before.

## [2026.0803_004] — 2026-08-03

**Skins are selectable again** (user report: hovering "Skin" under the
palette menu flashed the submenu open then collapsed it, highlight
flickering — unusable). Root cause: `ColormapMenu` observed the whole of
RadioState via @EnvironmentObject, so every publish (10 Hz S-meter,
skimmer, cluster…) re-evaluated its body while the menu was open, and
AppKit rebuilds an open NSMenu when its SwiftUI content re-renders —
top-level rows survive the rebuild visually, but any open SUBMENU (Skin,
Waterfall view, History — the latter two were latently flaky too)
collapses under the cursor on every rebuild. Fix: the menu now holds a
plain unobserved RadioState reference with keypath-derived bindings —
menu content is built fresh at open (checkmarks stay correct), and the
stable reference means SwiftUI skips the body on parent re-renders, so
an open menu is never rebuilt. Same reference-not-observation idiom as
the 9.71 timer-starvation class; apply it to any future Menu living in
a high-publish-rate hierarchy.

## [2026.0803_003] — 2026-08-03

**YouTube Live "server closed the connection" ROOT-CAUSED AND FIXED — it
was never the stream key.** The _003 diagnostics log (thanks, yesterday's
work) showed the tell: exactly 3073 bytes from the server = S0+S1+S2 and
nothing else — YouTube completed the handshake and never answered our
`connect`. Root cause: `sendConnectSequenceStart` announced an outbound
chunk size of 4096, then serialized the connect command at the 128-byte
DEFAULT — splicing type-3 continuation bytes into what a 4096-chunk
server consumes as payload. YouTube discarded the garbled connect and
idle-killed the TCP ~30 s later, which the old code (and yesterday's
coaching) misread as a bad key. **Proven by live A/B probe against
a.rtmp.youtube.com: split-at-128 framing → 0 bytes back; single-chunk →
WindowAck + PeerBW + `_result`.** Fixed by serializing connect (and the
FMLE trio + FCUnpublish) at the announced chunk size; regression pinned
in RTMPProtocolTests both directions (correct framing round-trips; buggy
framing must NOT parse). Also: a 20 s setup watchdog fails a stalled
ladder with the stage it died in (the Test-ingest client used to dangle
forever — Damon's log showed its 30 s corpse interleaving into the next
attempt), Go Live cancels an in-flight ingest test, and `closeHelp` now
distinguishes handshake-only closes (≤3073 bytes: "protocol-level, NOT
your key — file an issue") from post-connect drops (the real key
signature).

## [2026.0803_002] — 2026-08-03

**The crab can read the integration diagnostics** (user question: "is
there a log the crab is ingesting so it can assist with this?" — there
wasn't; now there is). New read-only `integration_diagnostics` tool (36th
tool, both providers — on-device Foundation Models + Claude): returns the
Discord status pair + the YouTube Live status plus the last 8 entries of
each window's connection-diagnostics log, timestamps and levels included,
fix-it hints attached to warnings/errors (trimmed for the small on-device
window). "Crab, why won't my stream connect?" now gets the actual failing
RTMP stage and its checklist instead of a shrug. Instructions teach it to
summarize the last error + fix rather than recite the log. Wired through
the standard four-site recipe (AICommand case, executor, FM Tool,
ClaudeToolCatalog Spec).

## [2026.0803_001] — 2026-08-03

**YouTube Live gets real diagnostics** (user report: gave it a stream key
and got "server closed the connection" with nothing beyond). The Discord
treatment, applied: a **Connection diagnostics** log in the YouTube Live
window shows every step of the RTMP ladder as it happens (TCP → handshake
→ connect → createStream → publish → media), with Copy/Clear for bug
reports. The key insight wired in: **where the connection died is the
diagnosis** — YouTube refuses a bad/expired/not-yet-activated stream key
by silently dropping TCP mid-sequence, so a close during the publish
sequence now coaches the key checklist (re-copy from Studio, the ~24 h
first-time live-streaming activation, right channel, no pasted
whitespace), a close during the handshake coaches network/firewall (it
never reached RTMP — not a key problem), and a close while live coaches
uplink/Studio. Also surfaced: NWConnection's `.waiting` state (a
firewalled port 1935 used to look like an eternal silent "Connecting…"),
explicit publish rejections (BadName → another encoder is on the key),
YouTube API errors with a Google Cloud checklist hint, and screen-capture
start failures with Screen Recording permission coaching. **Preflight**
checks run before any socket opens: URL-pasted-into-the-key-field,
whitespace/odd characters in the key, unparseable ingest URL (the key is
only ever logged masked: last 4 chars + length). New **Test ingest**
button (stream-key mode) runs the entire ladder and disconnects the
moment YouTube accepts the publish — validates the key end-to-end with
no screen capture and nothing streamed. New pure `YTDiag` coaching layer
+ `StreamDiagnostic`, package-tested (stage→hint mapping pinned).

## [2026.0802_009] — 2026-08-02

**Overnight whole-codebase bug sweep** (5 parallel review agents over
Discord/network, app+persistence, DSP+decoders, P1/P2 protocol, and
integrations+UI; every finding personally verified before fixing; 21
fixes, 1 TX-gated finding staged for review, not shipped).

Discord (the _007/_008 new code, highest priority): webhook-only mode's
notifications actually fire (the poll gate demanded a text-channel ID
that mode doesn't have); token-change restart now does a FULL teardown
(was leaking the voice streamer mid-stream and, with credentials
cleared, the poll timer forever) and is debounced 0.8 s (hand-typing a
token opened one gateway per keystroke, each IDENTIFYing a truncated
token); `startDiscord` reentrancy through the lazy Keychain load could
build two live services (duplicate gateway, orphaned audio tap) — didSet
retries now gate on `loadingKeychainToken` + a post-load re-check; two
service-side `onState` emissions hopped to main (off-main @Published
writes); pending gateway backoff reconnects die on stop()/start()
(generation counter — stale block double-opened sockets); manual
guild-ID typing no longer fires a channel fetch per keystroke (snowflake
gate); network-supplied application ID validated before the
force-unwrapped invite URL (crashable); the offline presence message is
no longer swallowed by the 10 s rate limit; webhook-only start posts the
online presence; duplicate "joined voice" log rows suppressed on server
mute/region events.

App layer: the `micChan` restore clamp no longer destroys the saved TX
mic channel when the interface is absent at launch (stale-UID channel
count falls back to the 1-ch system default; now clamps only against a
PRESENT device); ALE heard log written `.atomic` (torn file = whole
history lost); DX cluster node label colors are launch-stable
(deterministic UUID hash replaces per-process-seeded `hashValue`); five
filename date formatters pinned to en_US_POSIX (Buddhist/Japanese system
calendars rendered e.g. 25690802 in export names).

DSP: noise-blanker threshold floored at 1.5 (a hand-edited/corrupt
Settings.plist value ≤ 1 inverted the reference tracker into sustained
audio-chewing); WEFAX 60 LPM phasing fold gated on one full fold span of
history (enable-mid-tone wrapped the fold into unwritten ring samples
and could mis-phase the chart).

Integrations/UI: the YouTube Live window now OBSERVES its service —
status flips, error rows, and the LIVE badge repainted only on unrelated
app publishes (split into an @ObservedObject pane); the multimeter's
60 Hz ballistics moved off a stored `Timer.publish` (the 9.71
publish-storm starvation class) onto a `.task` loop; EiBi schedule cache
written `.atomic` + a load-path sanity floor falls back to the bundled
snapshot over a torn cache; cancelling Ask-the-Crab (Claude) mid-turn
now persists the exchange — tools that already executed no longer vanish
from history (the model would contradict or re-run them); AMF0 string
encoding truncates payload WITH the declared length (a >64 KiB string
would have desynchronized the whole RTMP stream — latent).

Protocol: no findings shipped — the full P1/P2 byte-map, length-guard,
pacing, and lifecycle audit came back clean. One TX-gated finding
(disarm during the unkey tail truncates the roger beep and leaves a
keyed dead carrier; fix is `txRFHot` in `disarmTX`) is STAGED on top of
this release for review — not in this build.

## [2026.0802_008] — 2026-08-02

**Discord setup, de-portaled** (user report: "too many workflows on the
Developer Portal side, and I'm technical"): the portal is now one step —
create the app and copy the bot token. Everything else moved in-app, or
away from the bot entirely. (1) **Webhook easy mode**: paste a channel
webhook URL (one right-click in Discord: channel → Integrations →
Webhooks → Copy URL) and notifications + `/waterfall` snapshots post
with **no bot, no token, no IDs, no gateway** — the service runs
webhook-only, `postEvent`/`postImage` route through the webhook (which
wins over the bot path when both are set), and a **Test webhook** button
validates then posts a real message. The URL embeds its own secret, so
it lives in the Keychain like the token (never in defaults or the
Settings.plist mirror). (2) **Invite bot button**: the app derives the
application ID from the token (READY, or `/oauth2/applications/@me`) and
opens the browser on an invite URL with scopes + exactly the needed
permissions (view/send/attach/connect/speak = 3181568) pre-baked —
the OAuth2 URL Generator workflow is gone. (3) **Server & channel
dropdown pickers**: the bot lists its own servers
(`/users/@me/guilds`, auto-refreshed on READY) and the picked server's
channels (type-filtered: text/announcement vs voice/stage, sidebar
order) — Developer Mode and Copy-ID are gone; a lone server
auto-selects, manual ID fields remain as a disclosure fallback, and a
stored ID not in the fetched list stays selectable. Setup checklist
rewritten around the two paths. New pure `DiscordDirectory` parsers +
invite/webhook helpers, package-tested.

## [2026.0802_007] — 2026-08-02

**Discord connection tests** (user request — Discord setup was failing
silently): new **Test text** and **Test voice** buttons in the Discord
settings window. Both run a staged REST diagnostic ladder where each rung
only runs after the previous one passes, so the first error in the log is
the actual problem, not a cascade: token identity (`/users/@me`, flags
user tokens vs bot tokens), guild membership (`/guilds/{id}` — a bot
that was never invited is the top cause of the silent voice-join
timeout), channel fetch (exists? visible? right **type** — text vs
voice vs stage/forum/category? belongs to the **configured** server, not
one pasted from elsewhere?), then a definitive action: Test text posts a
real message to the channel (403 split into can't-see vs can't-post
coaching); Test voice hands off to the real gateway join with its
existing timeout coach. New pure helpers in `DiscordDiag`
(`channelTypeName`, `identityCheck`, `guildFetchHelp`, `guildCheck`,
`channelCheck`; `preflight` generalized to name the channel kind) are all
package-tested. Tests run even while the gateway is down — REST-only
rungs isolate token/ID problems from gateway problems, and the ladder
opens with a gateway-state line.

## [2026.0802_006] — 2026-08-02

**Hover bubbles everywhere** (user request: sweep the whole UI): the
instrument-styled hover bubble from `_005` now covers every window —
main chrome and its seven control-bar popovers (DSP, display, RIT/XIT,
filter, RX EQ, settings, time machine), all decoder windows, TX Meters
and the TX Audio Chain rack, DX Cluster, LoTW, QSO Log, Stations Heard,
Multimeter, Discord, YouTube Live, Network Speakers, Ask The Crab,
Media Deck (pad editor included), Tuning Device, Keys, Connect sheet,
Software Update, About. **359 tips total**: ~190 existing descriptions
converted verbatim plus **~110 newly written** for controls that never
had any — Floor/Ref sliders, frequency entry, RIT/XIT, filter shift,
squelch, RTTY baud/shift conventions, ALE channels, rack slot
reorder/amount, the entire YouTube Live panel, LoTW credentials,
Discord voice, Multimeter functions, Media Deck editor, updater
buttons, and more. Native `.help` remains only where hover plumbing
can't reach: AppKit-backed menu items, one MapKit annotation, and
Bandscope's whole-window hint.

## [2026.0802_005] — 2026-08-02

**Hover bubbles in TX Controls** (user request): every control in the
TX window now explains itself in an instrument-styled bubble overlay on
hover (~0.4 s), replacing the native tooltip there — panel surface,
hairline border, skin-tokened, clamped to the window, flips above the
control when there's no room below, never intercepts the mouse. New
`Views/HoverTips.swift`: `.hoverTip("…")` tags a control (anchor
preference carries text + frame up the hierarchy), `.hoverTipHost`
renders the single bubble at the window root — 49 controls converted,
reusable window-by-window. Popover/sheet interiors (PWR CAL, save
dialog) keep native `.help` — preferences don't cross into separate
window hierarchies. The main-window banner and the shared RX/TX EQ
fader readouts also keep `.help` for now.

## [2026.0802_004] — 2026-08-02

**Expander ratio** (user request, dbx 286s-style): the TX noise gate was
always a downward expander with a fixed 2:1 slope — it now has the
missing knob. **Ratio 1.5:1–10:1** (default 2:1 = the historical
behavior, bit-identical: the slope multiplier is exactly 1.0 there) sets
how many dB the output drops per dB below threshold; depth still caps
the total cut and release still sets the close speed. The TX window row
is relabeled **Expander** with the Ratio slider joining Rel/Depth.
Pinned by `testNoiseGateRatioSteepensSlope` (relative slopes exact:
ratio 4 cuts 3× ratio 2's dB) plus the untouched legacy gate test
passing unchanged. Persisted as `txGateRatio`.

## [2026.0802_003] — 2026-08-02

**TX EQ ghost curve** (user question: "should the EQ track the
profile?"): each TX profile carries a hidden voicing stage — passband
edges plus a 3-band EQ (250 Hz shelf / 2.2 kHz presence / 3.5 kHz
shelf) — that never showed anywhere, so switching profiles looked like
it did nothing to tone. The 8-band user EQ now draws the selected
profile's composite voicing response as a dashed ghost line behind the
faders: the real 513-tap bandpass response × the real RBJ biquad
responses, single-sourced so the drawing can never drift from the chain
(`TXProfile.voicingEQ` now builds the chain's biquads AND the curve;
`Biquad.magnitudeDb` is pure coefficient math; pinned by
`testTXVoicingCurve`). Custom profiles resolve to their base voicing.
The user EQ deliberately stays independent — your mic correction
survives profile switches; the ghost shows what it sits on top of.

## [2026.0802_002] — 2026-08-02

**Hardware KEY/PTT jack now keys the transmitter** (user report: a
mechanical switch in the SquareSDR front-panel KEY/PTT jack T/R-switched
the radio but produced zero RF — the radio keys its own relay in
firmware, but the host never noticed, so no MOX, no TX IQ, nothing on
the wattmeter). The radio reports the jack state over the protocol (P1:
EP6 C0 bits [2:0] PTT/dash/dot, present in every status frame; P2: HP
status byte 4 bits [2:0] PTT/dot/dash — ANAN PTT and key jacks
included), and HermitSDR now edge-detects it and drives the exact same
interlocked keying path as the PTT button: ARM required, USB/LSB/AM/CW
on a live connection, roger-beep tail, aircheck, RX freeze — all of it.
Unarmed or wrong-mode presses are refused with the usual explanation
(the radio still T/R-switches itself; that part is firmware, not ours).
A hardware press never cuts short a software over and vice versa — only
the side that keyed may unkey. In CW mode a straight key in the jack
keys the clean carrier (PTT semantics with the 10 ms envelope — fine
for testing, not a speed-key path). Hardware validation: Damon's
switch + wattmeter.

## [2026.0802_001] — 2026-08-02

**"Wide ESSB" TX profile** (user request): a full-range eSSB voicing at
**50–4550 Hz** — real chest bass at the bottom, the classic "4.5k" eSSB
width at the top. Gentle +3 dB low shelf and +2 dB air, feather-light
1.7:1 leveling; sits next to ESSB Wide (100–4000) in the profile picker.
The 50 Hz low edge dips below the Hilbert modulator's ~70 Hz
clean-quadrature floor, so bottom-octave image rejection is now pinned by
a regression test (`testTXWideESSBProfile`: 4.3 kHz passes Wide ESSB and
is rejected by ESSB Wide; a 100 Hz tone passes and stays single-sideband
by >30 dB). Preset-table addition only — no TX processing-path changes.

## [2026.0801_006] — 2026-08-01

**Review-sweep bugfixes** — four parallel review agents read everything
new since this morning (Claude provider, crab voice/skeds/scout, antenna
+ CAT, the TX EQ tap and instrument components); every finding was
verified against the code before fixing. Nothing here changes behavior
you'd bug-check visually — the redesign target from `_005` is unchanged.

TX safety (the two that mattered):
- **TX-antenna interlock now covers the unkey tail.** `txKeyed` drops the
  instant PTT releases, but MOX stays up while the faded voice remainder
  and roger beep drain (up to 1.5 s) — the picker, rigctl `Y`, and the
  crab could all swap the Alex relay under PA power mid-beep. The
  interlock (and the crab's refusal) now key off `RadioEngine.txRFHot`,
  which stays true until MOX actually falls.
- **rigctl `Y n` while transmitting is refused whole.** It used to move
  the RX side and quietly refuse only the TX half — `y` then reported the
  new jack as truth while the PA stayed routed to the old one (the
  "keyed cal script aims at the dummy load, next over radiates on the
  air antenna" trap). Refused sets push the unchanged truth to the CAT
  mirror instead.

CAT / antennas:
- The CAT antenna mirror no longer goes stale: the RX-antenna didSet and
  connect/disconnect port-count changes push state immediately (before,
  a disconnected radio advertised 3 ports forever and `Y 2` returned
  success for a silent no-op).
- The connect-time antenna clamp is bracketed like the LNA clamp — it no
  longer grinds a remembered EXT1/ANT2 band preference down to ANT1 when
  the HL2 connects.
- Antenna phrase parsing: the first digit decides ("ANT12" was ANT2), and
  a bare "antenna" no longer silently means ANT1 — the crab asks which
  jack instead of throwing a relay you never named.

Crab (voice, skeds, scout, provider):
- CrabEars guards the zero-Hz input format (no mic connected used to be
  an uncatchable AVAudioEngine crash), refuses double-starts during the
  async permission hop (two engines, hot-mic leak), always ends the
  session on a recognizer error (an error after partials left the mic
  hot forever — the words heard so far are delivered, not lost), and
  retains its SFSpeechRecognizer for the session.
- The mic button always works while listening (a co-host interjection
  used to trap a hot mic behind a disabled button), and a transcript that
  can't send stages into the draft field instead of vanishing.
- Sked times: 1–2 digit input is a bare hour — "the net's at 7 UTC" now
  means 0700Z, not 0007Z. The persisted sked wire format is pinned by a
  canned-JSON test so future fields must decode as optional.
- Band scout only claims "cluster connected" when a cluster is enabled.
- Claude provider: history saves are generation-guarded (a slow reply
  can't resurrect a conversation you cleared), the context-overflow trim
  can no longer strand an orphaned tool_result at the head (an API-400
  loop), cancelled asks no longer clobber the next question's thinking
  state, and `set_volume` clamps before integer conversion.
- Crab commands issued through a cancelled turn now actually stop — the
  executor hop kept Task cancellation intact instead of severing it.

TX EQ meters:
- The per-band tap no longer allocates: the scratch-buffer copy was COW'd
  into 8 fresh allocations per feed block; the bandpasses now run
  sample-wise accumulating only the peak (the transmitted IQ stays
  bit-identical — pinned by test).
- The display is dark during TUNE/two-tone/CW (those synthesize RF past
  the chain, so the meters were showing the room mic, same reasoning as
  the IMD gate) and band envelopes reset at key-down (re-arming used to
  replay the previous session's peaks as ~1.8 s of ghost bars).
- `EQBandSlider` takes its dB range as a parameter — the RX EQ shares the
  control and was silently riding on the two ranges being equal.

## [2026.0801_005] — 2026-08-01

**The compact-instrument redesign** (CODEX-DESIGN.md, executed phase by
phase with visual gates) — HermitSDR's chrome now reads as RF test
equipment instead of enlarged macOS defaults, with the waterfall as the
centerpiece of a contiguous panel frame. **Plus a live TX EQ.**

The design system:
- `InstrumentMetrics` (2/4/6/8 pt spacing scale, 20/24/28 pt control
  heights, 2 pt radii, the 62/46 label/value columns, 10–11 pt type)
  and nine new semantic `SkinTokens` per skin (surfaces, border, text,
  selection, rx-green, armed-amber, danger-red, disabled).
- Reusable components: instrument buttons, illuminated lamp toggles,
  latched text buttons, adjoining segment banks, status chips/lamps,
  `ValueSliderRow`, `MonoValue`, uppercase section labels.

Converted end to end: header, both control-bar rows, status bar, DSP/
Display/gear/filter/RIT-adjacent popovers, decoder windows, side
panels, the crab window, and TX Controls (last, under a safety
protocol — interlock conditions, tooltips, and bindings verified
untouched; PTT/TUNE/2-TONE keep their lit/dim interlock encodings).

- **TX EQ, jazzed**: spectral band colors (warm 63 Hz → cool 8 kHz),
  a ±12 dB scale with gridlines, taller faders, and **live per-band
  modulation columns** while armed — a read-only 8-band envelope tap
  on the same pre-limiter point as the mod scope (bit-identical-IQ
  pinned by test), fed through the 30 Hz meter tick.
- **Flux Radio fixed**: six windows hard-coded the Hermit navy over
  the skin since skins shipped; all follow the skin now, and the
  selection accent renders per-skin (Hermit amber / Flux cyan).
- Main-window minimum re-derived for the new chrome: 1240 → 1270, with
  the root layout now leading-pinned so an over-wide bar can only ever
  clip at its trailing edge.

## [2026.0801_004] — 2026-08-01

**Antenna follow-ons + the rest of the crab slate (#54).** The morning's
per-radio antenna model grows its control surfaces, and the crab learns
its last six planned tricks — including a Claude API brain and a voice.

Antennas everywhere:
- **Crab `set_antenna` tool** — "put RX on the transverter input" routes
  a jack the connected radio actually has; TX swaps are refused while
  transmitting.
- **rigctl CAT antenna** — `Y n` / `y` (`\\set_ant` / `\\get_ant`)
  select ANT 1–N (bounded by the radio's jack count); `Y` moves RX and,
  when unkeyed, TX with it. RX-only inputs report antenna 0.
- **Stream Deck `DeckAction`s** — `setRXAntenna` / `setTXAntenna` /
  `cycleRXAntenna` join the shared action model for #52's next phase.
- **Model-level TX-antenna interlock** — the hot-relay lock that lived
  only in the TX window's disabled picker now lives in `txAntenna`
  itself, so CAT, deck, and crab paths can't swap the Alex relay under
  PA power.

The crab (#54 knowledge → full slate):
- **Claude API provider** — pick "Claude API" under the new gear in the
  crab window: `claude-opus-5` with the full 41-tool table, prompt-cached
  instructions, and a tool-use loop. API key lives in the Keychain
  (never the plaintext settings mirror); on-device stays the default.
- **Band scout** — "which band is open?" ranked from 15 minutes of DX
  cluster spots + Kp + time of day (`BandScout`, package-tested).
- **Net/sked memory** — "the 3905 net is 0100Z on 3.908 LSB, daily" →
  a ⏰ toast + chat line ~10 minutes before every occurrence
  (`SkedEngine` UTC math, package-tested; persists like watches).
- **Fix-my-audio** — RX audio doctor: mute, buried volume, closed
  squelch, pinched filter, needless attenuation, forgotten notches;
  `apply` fixes the safe knobs (overload-doctor pattern).
- **Voice** — a mic button dictates to the crab (on-device speech when
  available; auto-sends on final transcript) and "Speak replies" reads
  answers aloud. New speech-recognition privacy string.
- **Co-host mode** — while connected, the crab chimes in on its own
  every few jittered minutes: spots, conditions, whatever's on the air.
  Rides the 60 s watch clock; off by default.

Suite: +4 test files (SkedMemory, BandScout, ClaudeWire/catalog
dispatch, rigctl Y/y) plus antenna-parse and DeckAction round-trips.

## [2026.0801_003] — 2026-08-01

**Every radio now shows its antennas.** The header RX/TX antenna chips
appear for every connected radio, sized by how many ANT jacks the
hardware actually has — a new `HPSDRLink.antennaPortCount` capability
(HL2/SquareSDR: 1, ANAN-7000/Orion-class: 3). Single-jack radios get
static ANT1 chips (nowhere else to route); multi-jack radios keep the
full switch menus.

- `RXAntenna`/`TXAntenna` extracted to `Protocol/Antennas.swift` with
  per-model `available(ports:matrix:)` lists, package-tested
  (`AntennaSelectionTests`) — every picker now lists only jacks that
  exist, instead of a hardcoded `allCases`.
- Connect-time clamp: a persisted or band-memory antenna pick from a
  bigger radio (e.g. EXT1 from an ANAN session) lands on ANT1 when the
  connected radio doesn't have that input — same class as the LNA range
  clamp, and offline band-hopping still applies memories verbatim.
- Chips hide during file replay (no live jacks to show).

## [2026.0801_002] — 2026-08-01

**The #55 post-mortem: no DSP bug — four stacked measurement artifacts**
(and one real operator trap). A CAT-instrumented shack session traced
the "positive-peak ceiling not observable" finding to: the mod scope
drawing abs-max bins (cannot show asymmetry); aircheck file peaks being
the roger beep (0.700 FS, appended by design — every file "railed"
identically); the file-player level parked at 1% (a two-tone whispering
at 14% modulation); and steady two-tone physics (the +peak ceiling
needs transient program). Full-level confirmation on the dummy load:
tap +0.960/−0.950, 11.4 W peaks — chain healthy, matching the package
harness within 2%. #55 closed.

- **File level readout now shows ×-multiplier** (like Mic gain) instead
  of "%", and turns orange below 0.1× — "1" reading as 1% put an
  operator's AM at 14% modulation with no visible tell.
- **Warmth rack unit honors "exact bypass" at amount 0** — its low
  shelf used to keep coloring the audio with the knob fully down.
- New `TXAMHarnessTests`: an AM calibration harness reproducing the
  operator configuration with deterministic two-tone — pins the healthy
  limiter rails, per-stage non-starvation, symmetric control, and the
  1%-level undermodulation signature, with the measurement lessons
  documented in-file.

## [2026.0801_001] — 2026-08-01

**TX gate cleared — the four staged sweep fixes ship**, validated on the
dummy load (operator session, ANT 1): beeped unkeys clean ×3 with zero
underruns; disarm-mid-over beep confirmed making RF on the wattmeter;
airchecks verified closing per-over with sane headers (the previous
build left a 27 MB runaway file recording off-air mic audio — the bug
in the wild); C-QUAM/asymmetry interlock validated as no-regression
against the published build with a deterministic two-tone source.

- **Aircheck closes on force-unkey and disarm** — SWR trip, TX INHIBIT,
  stream-watchdog, or disarm no longer leave the recorder running on
  your off-air mic with an unfinished WAV header.
- **Roger beep renders outside the ring lock** — the up-to-1 s beep
  synthesis + FIR chain used to hold the lock that paces the radio's
  DUC (~6 ms cushion), risking an on-air glitch at the voice-tail/beep
  boundary. The ring now takes a microseconds-cheap append.
- **Asymmetric AM and C-QUAM are mutually exclusive** — the polarity
  follower's sign flips never reached the stereo difference path, which
  would decode as a hard L/R channel swap toggling on syllables.
- **Disarm zeroes drive after the unkey tail** — disarming mid-over on
  P2 used to transmit the voice fade and roger beep at zero drive.
- Follow-up filed as #55: the +125% positive-peak ceiling is not
  observable in processed audio on ANY recent build (pre-existing;
  measured this session with a two-tone control on both builds).

## [2026.0731_007] — 2026-07-31

**The overnight bug sweep: 43 verified fixes across seven subsystems**
(8 parallel review agents over every recent subsystem; every finding
verified against the code before fixing; 4 additional TX-chain findings
are staged separately for operator review per the TX gate).

*Media Deck (7):* stale completion no longer tears down a re-pressed
pad's fresh session; pausing a looping clip at the loop boundary stays
paused; the debounced deck save flushes at quit; a previewed editor
clip can't outlive the sheet (ESC included); Cancel no longer kills pad
playback the editor didn't start; drag/drop and slot-swap are edit-mode
only; an unreadable/newer deck document moves aside instead of being
overwritten by the next edit.

*YouTube Live (12):* OAuth broadcasts now actually go live
(enableAutoStart/AutoStop + monitor stream off — the old ready→live
call was guaranteed-rejected and try?-swallowed); the OAuth loopback
ignores favicon/prefetch requests instead of aborting consent, takes
its completion under a lock (double-resume crash), and times out after
5 min; a server close during RTMP setup now surfaces ("check the
stream key") instead of pinning "Connecting…"; audio+video share one
epoch (lip-sync) and overflow drops advance the audio clock; screen
capture death and repeated VT encode failures are detected (delegate +
session rebuild); RTMP send gets backpressure (sheds inter-frames,
resyncs on keyframe) and error propagation; the chunk reader parses
2/3-byte basic headers and fmt-3 extended timestamps (the ~4.66 h
desync); createStream's server Double converts safely; stop() during
OAuth startup can't resurrect the stream; the stop-time transition
refreshes its expired token and failures also end the broadcast.

*Audio infrastructure (4):* switching the output picker back to
"Default" actually rebinds (was stuck on the last device — BlackHole,
failover targets — forever); the restart-storm breaker LATCHES instead
of duty-cycling the HAL hammering every 30 s; the mic delivery watchdog
backs off exponentially (1→30 s) instead of hammering a dead input at
~1 Hz; ClipPlayer detects engine death so the voice-check transport
can't wedge in "playing".

*CASCADE + skimmer (3):* the ARQ sender no longer false-ACKs unsent
frames on >128-seq queues (a 13 KB message died silently) and bounds
its window to the receiver's 8-seq acceptance span (retry-storm →
spurious link failure); two new pinning tests. The Metal channelizer
recomputes metrics on CPU when a batch fails mid-drain (the failed
batch could scribble the GPU metrics buffer).

*Ask The Crab (8):* streaming replies address their bubble by ID so
Clear-mid-turn can't overwrite receipts; explicit VHF/UHF MHz values
clamp honestly instead of silently tuning kHz ("146.52 MHz" ≠ 146 kHz);
the storm-failover toast auto-clears (20 s) and toast lifecycles no
longer race; clear_watch matches exactly before falling back to
substring ("5" no longer deletes K5RSA); Enter-while-thinking no longer
eats the typed question; identify_signal keeps a running best across
polls (intermittent CW); the mode tool no longer advertises FM; model
availability re-checks live ("still downloading" is no longer forever).

*RX/DSP (6):* PSKReporter and the ALE heard/LQA log are gated during
file replay (real uploads/log pollution from replayed recordings);
time-machine bookmarks created while shifted land on the true event
time, and bookmarks from continuous decoders (CW/RTTY/ALE) record the
CURRENT dial, not the enable-time one; RF Vision click-tune offsets
USB-suggested signals into the passband (they landed at 0 Hz audio and
vanished); the time machine refuses to engage while the sub-RX runs
(mixed time epochs in one audio stream) and the slider says why.

*App layer (3):* leaving VPN Mode clamps the snapshot's sample rate to
the connected radio (an ANAN-era 1536 k snapshot desynced every overlay
on an HL2); the Settings.plist mirror now exports AFTER the final
settings flush at quit (last-moment changes made it to defaults but not
the mirror); shared toast helper (above).

## [2026.0731_006] — 2026-07-31

**The Virtual Media Deck lands (issue #24, Phase 1).** Tools ▸ Media
Deck… opens a broadcast-soundboard grid of programmable pads that play
local audio clips — station IDs, sweepers, sound effects, net-control
beds.

- **Pages + grid presets** (3×5 / 4×6 / 5×8), sparse slots — shrinking a
  grid hides off-grid pads without deleting their configs.
- **Per-pad config:** title, emoji face, color, gain (0–2×), start/end
  trim, loop, and press policy (Restart / Pause-Resume / One-shot).
- **Edit mode:** click a pad to configure, drop an audio file from
  Finder straight onto a pad, drag pads between slots to rearrange;
  per-pad context menu (Edit / Stop / Clear).
- **Playback:** one engine session per active pad (the ClipPlayer
  lesson — no shared-graph glitches), per-pad output device routing
  (system default or any CoreAudio output), live progress bar, paused /
  missing-media / failed states on the pad face.
- **STOP ALL** (⌘.) halts everything instantly; master volume rides all
  playing clips live; activity lamp shows when any pad is sounding.
- **Persistence:** versioned JSON document in Application Support
  (atomic writes, newer-version documents refused rather than mangled);
  missing files keep their pad config and flag for relinking.
- Buttons bridge to the shared `DeckAction` model, so a future physical
  Stream Deck key can fire the same clips (#52).
- Radio TX routing is deliberately **not** in Phase 1 — it arrives in
  Phase 2 behind explicit interlocks per the issue's transmit
  safeguards.
- New pure-layer test suite `MediaDeckTests` (13 tests: document
  round-trip + version gate, policy state machine, trim math,
  off-grid survival, DeckAction bridge).

## [2026.0731_005] — 2026-07-31

**Shack-session polish from the validation day.**

- **TX Controls window can no longer restore itself too narrow** — macOS
  was restoring the pre-relayout 440-wide saved frame over the new
  layout's 820 minimum and silently clipping the entire right column
  (processing rack, Aircheck toggle) off the window edge.
  `.windowResizability(.contentMinSize)` makes restored frames honor the
  content minimum.
- **IMD3 readout capped at "≥60 dB"** — a pure tone pair with products
  below the noise floor used to display an absurd "IMD3 155 dB".

Validated on the dummy load this session (see issues #13/#53/#34):
TUNE + 2-TONE keying, SSB voice PTT, talk-power coach, aircheck logger
(format/duration/content verified), roger beep placement (clean gap
after the final word), AM carrier + upward modulation, Optimod AM
positive-peak engagement (22× positive-peak density), full-drive
verification of the new power cal (app 137 W vs Bird ~120 W).

## [2026.0731_004] — 2026-07-31

**TX Meters honesty during built-in TUNE/2-TONE.** Caught live in the
dummy-load session: the built-in test tones are synthesized directly at
the modulator (chain bypassed), so the IMD3 readout and mic coach were
grading the *idle live mic* — a monitor sidetone looping back
acoustically graded as a red "DIRTY" tone pair while the transmitted
signal was clean by construction.

- IMD3 readout suppressed while TUNE or 2-TONE own the output — it's
  only meaningful when the chain carries the program (two-tone file
  through the file player, or voice).
- Mic coach line shows "TEST TONE — MIC METERS IDLE" instead of voice
  advice during test tones.

## [2026.0731_003] — 2026-07-31

**The ANAN was a 120-watt radio all along: Bird-43 dummy-load
calibration (#34).** First hardware-validated power cal — an 8-point
scripted TUNE sweep (10–100% drive, driven over the new rigctl TX
automation) against a Bird 43 with 25/50/100/1000 W elements.

- **P2 forward-power cal `k` 0.28 → 0.122** (log-LSQ over 7 Bird
  points; per-point spread 0.106–0.138, best-resolution points at
  0.119). The old 0.28 was circular — it trusted PA-current telemetry
  whose own fit assumed the same wrong power. pihpsdr's 0.12 was right.
  Full drive is ~120 W, not ~60 W.
- **PA current fit rescaled by the same 2.295×** (slope 0.0101725 →
  0.02335, offset 3.0 → 6.885): 17.5 A at full drive → 49.6% PA
  efficiency at 13.8 V, coherent class AB across the whole sweep. The
  near-zero under-read (#34) remains until a DC-ammeter measurement;
  the untrusted-region floor is now stamped per connection (P2 2.3 A,
  HL2 unchanged at 1.0 A) so readings in the rescaled fit's fuzzy zone
  show "—" instead of a precise-looking wrong number.
- Measured sweep (drive → Bird): 20% → 2 W, 30% → 7.5 W, 40% → 19 W,
  55% → 46 W, 70% → 77 W, 85% → 100 W, 100% → 120 W into a 1.0:1
  dummy load (SWR 1.00–1.03 app-side throughout).

## [2026.0731_002] — 2026-07-31

**TX Controls relayout: wide two-column window, operate controls always
reachable.** Shack report: the rack had grown so tall (reverb, gate,
Comp+, Mic NR, aircheck…) that the fixed stack outgrew the screen and
the ARM switch was pushed off the top with no way to scroll to it.

- **Pinned operate core** — state/frequency header, then ARM + PTT +
  TUNE + 2-TONE on ONE row, then TX ANT / SWR guard / quick-log, then
  Drive + Mic gain side by side. These never scroll.
- **Two-column scrollable rack** — voicing (source/file/mic, profile,
  FX + variable reverb, beep, EQ) on the left; processing + monitoring
  (Mic NR, gate, de-esser, comp/Comp+, AGC, AM controls, monitor,
  voice check, aircheck) on the right, in a ScrollView.
- **Pinned bottom** — mic/ALC meters, telemetry strip, underrun lamp,
  PWR CAL, condensed safety line.
- Window is now wide-and-short: default 940×660 (min 820×560) instead
  of 440×790.

## [2026.0731_001] — 2026-07-31

**CAT grows TX-automation hands: scripted dummy-load sweeps over rigctl.**

- **rigctl `L`/`l RFPOWER`** — get/set TX drive over CAT (hamlib 0–1
  scale ↔ the app's 0–100 %). Same finite-range boundary validation as
  `set_freq`.
- **rigctl `U`/`u TUNER`** — key/release the steady TUNE carrier
  remotely, and **`U`/`u TWOTONE`** (HermitSDR extension) for the
  700 + 1900 Hz IMD pair. Both run through the same model-level guards
  as the UI buttons: ARM interlock, never over a live voice over,
  mutually exclusive with each other.
- **Telemetry readback levels** — `l RFPOWER_METER_WATTS`, `l SWR`, and
  `l PA_CURRENT_A` (extension) mirror the TX telemetry at poll rate, so
  a power-cal sweep script (issue #34) can log the app's estimates next
  to the external wattmeter readings.
- `RigctlServer` command parser is now covered by the package test suite
  (`RigctlServerTests`, incl. the "F nan" trap regression).
- **Fixed: loopback-only CAT never started** (broken since 2026.0728_006).
  Setting `requiredLocalEndpoint` *and* passing `on: port` to
  `NWListener.init` throws EINVAL, so enabling CAT silently snapped the
  toggle back off. The endpoint already carries the port; the listener is
  now created without the redundant argument. LAN mode was unaffected.

## [2026.0730_007] — 2026-07-30

**The crab passes the Extra exam: band plan + award bookkeeping (35 tools).**
Knowledge group of #54 complete.

- **`band_plan`** — "where can I run AM tonight?" gets a real answer: a
  bundled **US/FCC Part 97 table** (160 m–6 m, post-2006 class splits —
  Extra/Advanced/General/Technician segments, 60 m channels with the
  100 W ERP note, 30 m's no-phone-ever) plus **conventions** labeled as
  such: the AM windows (3885, 7290, 29.0–29.2 …), FT8 calling
  frequencies, SSTV spots. Ask with a mode and/or band — or with
  nothing, and it reports what's legal **at the current dial**,
  most-permissive class row per mode family. Table is package-tested
  (`BandPlanTests` pins the class splits the crab will be quoted on).
- **`award_progress`** — DXCC straight from the QSO log: unique entities
  worked and LoTW-confirmed (entity-level, resolved through cty.dat),
  distance to the 100, best bands, and per-band counts on request. Pure
  `AwardTally` counter, package-tested (dedupe across calls from the
  same entity, confirmation at entity level).

## [2026.0730_006] — 2026-07-30

**The crab turns clinician: overload doctor + modulation coach (33 tools).**
Two more from the #54 bundle.

- **`overload_doctor`** — "why does everything sound like splatter?" Reads
  the ADC overflow lamp and the gain ladder (LNA, digital ATT, S-meter)
  and explains the physics: the step attenuator sits *after* the
  converter, so it can't cure ADC clipping — the LNA is the knob. With
  `apply` it actually drops the LNA 6 dB (clamped to the radio's range)
  and reports the move; at the LNA floor it says so honestly (external
  attenuation territory). Healthy front ends get a status line plus
  headroom advice (drop unneeded ATT, consider Auto-LNA).
- **`modulation_coach`** — "how's my audio?" Reads the live TX meters
  (mic-clip latch, compressor/limiter split, ALC, speech-gated talk
  power, PAPR) and coaches: clipped source → fix the interface gain;
  limiter shaving > 1.5 dB → flat-topping; heavy ALC → overdriven chain;
  low talk power → raise gain; peaky voice → compressor/Leveler. Clean
  chains get told they're clean. Read-only — it never touches the TX
  chain, and requires TX armed (the meters only run while armed).

## [2026.0730_005] — 2026-07-30

**Aggregate-audio defense-in-depth: storm failover + picker warning.**
Follow-up to the _001 lockup fix after a report that the lockup can still
occur — layered protection that doesn't wait on the root cause.

- **Storm failover**: when the config-change restart breaker opens (5
  restarts in 30 s), the engine no longer just leaves audio dead — it
  abandons the storming device and binds a safe **non-aggregate** output
  (built-in speakers preferred), restarting once. One-shot per storm: if
  the safe device also storms, the breaker stays open for real. A toast
  tells the operator what happened and why; a deliberate device pick or
  reconnect returns to their choice.
- The failover overrides follow-the-system-default too — the two-monitor
  lockup case is exactly "the system default *is* the aggregate".
- **Device picker warning**: aggregate/auto-aggregate outputs are now
  flagged "⚠️ aggregate" in the speaker menu
  (`kAudioDevicePropertyTransportType` surfaced through
  `AudioDevices.Device.isAggregate`).

## [2026.0730_004] — 2026-07-30

**Crab watches (31 tools).** The initiative group of #54: "let me know
when…" now sticks.

- **`add_watch` / `list_watches` / `clear_watch`** — persistent watches,
  three kinds: a **callsign** appearing on the DX cluster (exact call or
  a `VP8*` prefix), a **shortwave station** coming on the air (checked
  against the EiBi schedule clock every minute), and the **Kp index**
  reaching a threshold (checked on the hourly NOAA fetch). Watches
  survive relaunch (same persistence idiom as bookmarks).
- When a watch hits, the crab posts a line into the chat's action feed
  AND slides a toast over the waterfall (auto-dismisses in 8 s; the chat
  line stays). Per-kind refire cooldowns — spots 30 min, stations 6 h,
  Kp 3 h — keep an armed watch from nagging.
- Matching logic is its own pure subsystem
  (`Integration/AI/CrabWatches.swift`) in the SPM package with a full
  test suite (wildcards, cooldowns, kind phrasing, Codable round-trip).
- Honest edges: adding a callsign watch with no cluster node connected
  says so; an unparseable Kp threshold is rejected at add time.

## [2026.0730_003] — 2026-07-30

**Callsign intelligence (28 tools).** First checkbox of the #54 knowledge
group: ask the crab "who is JA1NUT?" and get an actual briefing.

- **`callsign_info`** — DXCC entity, continent, and CQ zone for any
  callsign (via the bundled/weekly-refreshed AD1C cty.dat), the
  most-wanted rank when the entity is rare, **beam heading and distance**
  from the operator's grid square (the PSKReporter `stationGrid`
  setting; the crab tells you where to set it if it's empty), and a QSO-
  log cross-check: worked-before (with QSO count + LoTW state), new-call-
  but-worked-entity, or the money line — **ALL-TIME NEW ONE**.
- `CountryFile` now keeps the header metadata it used to discard
  (continent, CQ zone, lat/long — cty.dat's west-positive longitude
  normalized to east-positive, pinned by test).
- New pure `Maidenhead` helper (4/6-char locator → coordinates, haversine
  distance, initial great-circle bearing, 16-point compass) in the SPM
  package with its own test suite.

## [2026.0730_002] — 2026-07-30

**The crab reads the mail (27 tools).** First checkbox of the #54 senses
group.

- **`read_transcript`** — "what's he sending?" now works: the crab reads
  the live decoded text from the **CW**, **RTTY**, or **ALE** decoder
  (last ~400 characters, newline-flattened) and can summarize or quote
  it. Stale text from a since-disabled decoder still reads (worth
  having); an empty transcript reports whether the decoder is off and
  where its switch lives — honestly, since the crab deliberately cannot
  toggle the CW/RTTY *decoders* itself (`set_decoder`'s "cw"/"rtty"
  route to the skimmer).

## [2026.0730_001] — 2026-07-30

**Aggregate-output hard-lockup fix: the audio engine no longer storms the HAL.**

- A user running RX audio into an **aggregate output device built from two
  monitors** hit a full system lockup. Root cause on our side: AVAudioEngine's
  config-change notification re-fires on every engine restart against an
  aggregate (each device rebind renegotiates the aggregate's clock/format),
  and `AudioOutput`'s observer restarted the engine immediately and
  unconditionally — an undamped stop/rebind/start loop hammering coreaudiod
  and the display-audio drivers (monitor audio rides the display pipeline;
  the OS-level wedge is Apple's bug, but we were feeding it). Three-part fix
  in `AudioOutput`:
  - **No-op device rebinds are skipped** — `applyPreferredDevice` reads the
    io unit's current device and leaves it alone when unchanged; rewriting
    the same ID tears down and rebuilds an aggregate, which was the main
    feedback edge of the loop.
  - **Config-change restarts are debounced** — notification bursts coalesce
    into a single restart 300 ms after the last one.
  - **Restart storm breaker** — 5 config-change restarts inside a rolling
    30 s window opens a breaker: audio stays down on that device (loud
    NSLog) instead of cycling forever; re-picking an output device or a
    reconnect closes it.

**The crab learns the shortwave broadcast schedule (25 tools).**

- **`shortwave_schedule`** — "What frequencies are the BBC on right
  now?" works: the full EiBi seasonal database (~9,300 broadcasts, the
  community-standard schedule from eibispace.de) ships bundled
  (`Resources/eibi-a26.csv`) and answers by station name (frequencies on
  the air right now, with language, target area and end time) or by
  frequency in kHz (who broadcasts there now — the natural follow-up to
  `identify_signal` finding an AM carrier). Time-of-day (UTC, including
  past-midnight wraps) and day-of-week rules (Mo-Fr ranges, SaSu lists,
  EiBi digit codes) are honored; irregular/monthly patterns are shown
  with their raw tag rather than guessed at.
- The parser + query engine is pure and package-tested
  (`SWSchedule.swift`, 6 tests incl. parsing the entire bundled
  snapshot); the store refreshes the season file over HTTPS at most
  weekly, silently keeping the bundle as fallback, and computes the
  EiBi season code (A/B, last-Sunday-of-March/October boundaries) so
  refreshes track season changes automatically.

## [2026.0729_004] — 2026-07-29

**The crab gets ears and a logbook pen (24 tools).**

- **"What mode is this?"** — new `identify_signal` tool: the crab borrows
  RF Vision as its ears, watching the waterfall for up to ~7 s and
  classifying whatever sits at the VFO (CW, FSK/RTTY, SSB voice, AM,
  FT8-style bursts, steady/drifting carrier, pulsed RFI) with bandwidth,
  SNR, drift and repetition facts plus a which-decoder-reads-it hint.
  With `lockOn` it also tunes onto the signal and switches to the
  matching mode (the operator-sanctioned "adjust tuning and mode as
  necessary"). RF Vision's on/off state is restored afterwards if the
  crab had to borrow it.
- **Situational awareness** — every question now silently carries a
  one-line radio snapshot (VFO, mode, filter width, connection, RF
  Vision/recording/time-machine state). "What band am I on?", "widen it
  a bit", "am I still rewound?" ground instantly; the transcript shows
  only what the operator typed, and the crab is told never to echo the
  telemetry line.
- **`log_qso`** — "log this contact with K1ABC" appends a real logbook
  entry at the current frequency and mode (same store as Tools ▸ QSO
  Log / LoTW export).
- The assistant executor is now async end-to-end (identification watches
  the band in real time instead of guessing).

## [2026.0729_003] — 2026-07-29

**The crab gets a memory, a mouth, and seven more claws (22 tools).**

- **Action receipts** — every state change the crab actually performs now
  posts a small ✓ line into the chat under its reply: visible proof of
  what really happened, independent of what the model says (born of the
  tune bug, where it claimed actions it never took).
- **Seven new tools**: `rewind_audio` (the RF time machine — "rewind 30
  seconds", 0 returns to live, capped to the buffered history),
  `set_recording` (the IQ recorder), `search_log` (QSO logbook by
  callsign or a summary with today/LoTW counts), `go_to_bookmark`
  (recall by name with fuzzy match, or list them), `set_zoom` (in/out/
  level 1–8), `set_palette` (waterfall colormaps by name, or list them),
  and `decoder_heard` (one readout for FT8 callsigns, skimmer signals,
  or ALE stations heard).
- **Personality: salty North Shore crab.** Playful trash talk, CB-rat
  grumbling, dry pointed wit about Donald Trump and the Republican
  party, proudly pro-Ukraine, and occasional subtle nods to Dick
  Bulger, roast beef three-ways, and onion rings. The persona wording
  was tuned against Apple's on-device guardrails (probed live: the
  first draft made the safety layer reject even "say something nice
  about my radio setup"; the shipped wording keeps the spice with
  per-question blocks only). When Apple's layer does clamp a reply
  (direct presidential-opinion questions sometimes trip it), the crab
  says so in character instead of erroring, and the flagged exchange is
  dropped so it can't sour the session.
- New prompt-window suggestions showing off the new powers.

## [2026.0729_002] — 2026-07-29

**The crab learns about the band: five new tools (15 total).**

- **`dx_spots`** — "who's on the air?" lists the eight most recent DX
  cluster spots (call, frequency, comment, age).
- **`tune_to_spot`** — "take me to JA1NUT" finds the newest spot for a
  callsign (exact match first, then prefix) and tunes it through the
  spot-click path, so the mode heuristics apply just like clicking the
  ticker.
- **`set_rf_vision` + `band_activity`** — the crab can switch RF Vision
  on and read back what it currently sees: classified signals (CW, SSB,
  FT8?, RFI…) with frequency and SNR, strongest first.
- **`set_filter_width`** — "narrow the filter to 500 Hz" / "give me
  2.4 kHz"; number + unit as spoken (`AIFrequency.filterHz`, bare
  numbers below 20 read as kHz), clamped to the current mode's limits.
- Instructions updated so the crab knows its new capabilities.

## [2026.0729_001] — 2026-07-29

**Ask The Crab tune-up: frequency changes now actually happen.**

The crab claimed to QSY but the dial never moved. Probing the on-device
model directly found two real defects, both fixed:

- **The tune tool no longer asks the model to do unit math.** It demanded
  raw Hz, and the small model botched the conversion exactly when the
  request wasn't spelled out ("go to 14.250" became 22.8 MHz, measured).
  The tool now takes the number + unit as the operator said them and the
  radio converts (`AIFrequency`, unit-tested): explicit MHz/kHz/Hz pass
  through, bare numbers are inferred by magnitude (the three readings are
  disjoint over 0.1–54 MHz, so 14.074 / 7200 / 14074000 each have exactly
  one sane meaning), and an implausible unit label falls back to the
  magnitude reading.
- **The crab now remembers the conversation.** Each question used to get
  a brand-new model session, so follow-ups like "take me there" had no
  context and the model invented a success message. One session now
  persists across turns (per the probe, multi-turn tune requests then
  work); Clear wipes the model's memory along with the window, and a
  context-window overflow silently restarts the conversation and retries.
- **New `nudge_frequency` tool** for relative moves ("up 5 kHz") — the
  offset math happens in code, not in the model.
- **Tuning no longer clobbers the mode**: the executor previously routed
  through the spot-tune helper, whose mode map forces anything but
  CW/LSB/AM to USB — asking for a frequency change while in SAM or FM
  switched the radio to USB. Frequency changes now leave the mode alone,
  and the confirmation reports the radio's *actual* resulting frequency
  and mode rather than echoing the request.
- Instructions updated to match (pass units verbatim, use the nudge tool
  for relative moves, never claim success without a tool result).

## [2026.0728_019] — 2026-07-28

**Four TX voice tools (TX-chain: hardware validation pending, like the
_016 batch).**

- **Mic NR** — RNNoise neural noise suppression on the mic path, at its
  native 48 kHz (no resampling, unlike the RX wrapper), ahead of the
  whole chain so the gate/AGC/compressor work on the cleaned voice.
  Constant 10 ms latency; steady n-in/n-out framing contract
  (test-pinned).
- **Null-test monitor** — a "Null" checkbox on the Monitor row: the
  sidetone plays processed − input, so you hear exactly what the chain
  adds and removes. The reference is delay-aligned through the chain's
  bulk latency AND passed through its own copy of the always-on phase
  rotator — without that the rotator's designed dispersion would drown
  the difference (an in-band tone now cancels ≥ 12 dB with the optional
  stages off, while audio the chain removes survives at full strength —
  both pinned). Transmit, meters, and airchecks are untouched.
- **Talk power + coaching** — TX Meters gains a speech-gated ~3 s
  average level with the peak-to-average ratio (density: raw voice runs
  PA 14+, dense broadcast lands 6–9) and a coach line that reads the
  whole meter set: QUIET / PEAKY / DENSE / CRUSHED / SOLID TALK POWER.
- **Aircheck logger** — every keyed voice over saved as a timestamped
  48 kHz WAV in ~/Documents/HermitSDR Airchecks (roger beep included,
  sub-0.75 s key blips discarded; CW/TUNE/two-tone skipped). Rides a new
  always-true-processed tap so null-test monitoring never leaks into a
  recording. Toggle + folder button under the voice check.
- 4 new tests: 332 total.

## [2026.0728_018] — 2026-07-28

**Demo Mode — try the whole app with no radio.** A ✨ **Demo Mode**
button on the connect sheet generates (once, cached in Application
Support) a deterministic 30 s synthetic slice of a lively 20 m band and
loops it through the real receiver via the ordinary replay path: an SSB
voice (the VFO lands on it), a 20 wpm CW beacon calling CQ DE HERMIT,
45.45 Bd RTTY, an AM broadcaster playing a pentatonic tune, FT8-shaped
15 s bursts, a slowly drifting carrier, two birdies (one at +31.337 kHz,
naturally), and an ignition crash every 5 s. Every steady tone sits on
the loop-periodic frequency grid so the 30 s seam doesn't click. Tune,
filter, run the decoders, open the DSP popover, flip on RF Vision — all
of it is real processing on real IQ; TX stays disabled exactly as in any
replay. Disconnect returns to the connect sheet.

- Replay path improvements that Demo Mode surfaced (they help real
  recordings too): **RF Vision now reconfigures for the replay file's
  rate/center** (it previously kept the last live session's geometry —
  every region would have been mislabeled during replay), and **FT8/FT4
  decode now runs during replay** (sessions carry the REPLAY badge and
  PSKReporter stays suppressed, as before).
- New DemoBand fixture (header validity, replay-rate constraints,
  wire-safe normalized amplitude, and each advertised occupant present
  at its offset): 328 tests.

## [2026.0728_017] — 2026-07-28

**RF Vision phase 1 (issue #14) — the GPU semantic waterfall.** A new
**VISION** toggle turns the waterfall into a live RF situational-awareness
display: every signal in view is detected, tracked, and broadly
classified — CARRIER, DRIFTER, CW, FSK, SSB, AM, FT8-shaped burst, pulsed
RFI, wideband noise — with center frequency, occupied bandwidth, SNR,
duration, duty cycle, drift rate, and repetition interval. Fully
deterministic (rule-based, no neural net): decoders remain the source of
truth, and RF Vision can never key, retune the radio on its own, or touch
TX.

- **Pipeline** (`DSP/RFVision/`, OmniSkimmer architecture): a Metal
  compute stage (runtime-compiled MSL, fast-math off, CPU fallback +
  test oracle) estimates an adaptive per-bin noise floor (chunked 25th
  percentile → median-of-3 → temporal EMA), thresholds a signal mask,
  and does morphological cleanup in a single barrier-free kernel; a CPU
  tracker links masked runs into clusters and persistent tracks, then
  classifies from measured features. Rows tee off the existing spectrum
  callback — non-blocking, drop-under-backpressure, never touching
  RX/audio; analysis follows whatever the waterfall shows (incl. the
  time machine).
- **UI:** translucent bandwidth-band annotations over the waterfall
  (click a region to tune — and, when the family implies one, set the
  likely mode) + a sortable detections panel (freq / family / bandwidth /
  SNR / duration / confidence, diagnostics footer with GPU ms). Arcade
  mode adds the local-only Bulger commentary (POSSIBLY HAUNTED, AUDIO
  FELONY, MACHINE CONSPIRACY…) — never in any log or export.
- **Tests:** 13 fixtures — the issue's acceptance list (synthetic
  carriers, keyed CW, drifter with measured drift rate, two-tone FSK,
  voice-like region, symmetric AM, FT8-shaped 15 s bursts, pulsed
  interference, retirement) + mask morphology/seam contracts + Metal ≡
  CPU parity on the real GPU: 327 total.
- Known phase-1 limits (by design): wide-shift (425/850 Hz) RTTY reads
  as two keyed carriers; SSB sideband sense isn't guessed. Phase 2
  (optional MPSGraph classifier, decoder dispatch, semantic squelch,
  IQ auto-capture) remains open on #14.

## [2026.0728_016] — 2026-07-28

**TX-GATED (issue #13/#53 class): all three changes touch the transmit
audio chain — needs Damon's dummy-load validation before any release
ships.** All processing is pre-limiter/pre-bandpass, so band containment
is architecture-guaranteed (and re-pinned by a new everything-cranked
splatter test).

- **Variable reverb.** Room/Hall/Plate grew user controls: **decay**
  (RT60 0.2–5 s), **damping** (bright metallic → dark soft), and
  **predelay** (0–80 ms — separates the dry voice from the tail, the
  classic clarity trick). The preset still picks the *size* of the space
  (comb network), so Room with a 3 s decay rings like a small hard room,
  not a hall; toggling custom off restores each preset's designed sound
  bit-identically (test-pinned). Retunes click-free mid-drag — feedback/
  damping change in place, the delay lines never reset.
- **Custom compressor (Comp+).** The single-band leveler's threshold,
  ratio, attack, release, and makeup are now fully user-adjustable —
  the attack/release were hard-coded at 5/60 ms since 1.x. Off = the
  profile's designed leveler, untouched. Multiband keeps the profile's
  per-band design either way.
- **Gate release + depth.** The noise gate's close speed (40–400 ms) and
  maximum cut (6–40 dB — 18 breathes, 40 is nearly a hard gate) join the
  threshold slider, shown when the gate is on.
- The TX Audio Chain map shows the new gate/compressor/reverb settings
  live; all eleven new settings persist.
- 9 new tests (gate depth caps the cut, release timing, compressor
  ratio/threshold/attack behavior, reverb decay/predelay/stability/
  preset-restore, and the all-overrides band-containment pin): 314 total.

## [2026.0728_015] — 2026-07-28

- **ALE scanning + station log (issue #35, milestone 2).** The ALE window
  grew a **SCAN** button: the receiver steps around the network's channel
  list (dwelling ~2.5 s per channel) and **parks the moment a word decodes**,
  holding until the exchange goes quiet — scan-on-silence, park-on-signal,
  like a hardware ALE controller. Every decoded word is logged against the
  channel it was heard on, and a **STATIONS HEARD** link-quality table ranks
  who's workable where: heard count, last-heard, and a 0–100 LQA score that
  weighs recency (3-hour half-life — HF moves), copy cleanliness (Golay-
  corrected words score lower), and depth. The heard log persists across
  launches. Scanning never fights you: it pauses during transmit, replay,
  or disconnect, and never auto-starts at launch.
- **New app icon.** The Dock finally shows the hermit crab — headphones on,
  tucked in its shell under the falling waterfall — rendered from the About-
  window artwork. The old "SD" tile (from the SquareDeck days) is retired.

## [2026.0728_014] — 2026-07-28

- **CASCADE ARQ — the lab PHY stack is complete (core-only).** Selective-
  repeat ARQ over the FEC'd frame channel: 8-frame window, cumulative ACK +
  selective bitmap, timeout retransmission, in-order exactly-once message
  delivery, and a clean link-failed state after retry exhaustion. Fully
  deterministic (the caller owns the clock) and package-tested — including
  the whole stack composed: ARQ frames through the LDPC+CRC channel with
  2.5% bit corruption deliver a 600-byte message intact, and a seeded 40%
  frame-loss channel still gets everything through. With sync, FEC and ARQ
  done, the Experimental Modes themselves (LUMEN / DUET / ARIA) are next —
  behind the future Lab gate, dummy-load/closed-network only.

## [2026.0728_013] — 2026-07-28

- **CASCADE gains forward error correction (Experimental Modes groundwork,
  core-only).** The lab modem now has a rate-½ LDPC code (n=648, k=324,
  (3,6)-regular, built deterministically from a shared seed — both link ends
  derive the identical matrix) with a normalized min-sum soft decoder, plus
  CRC-32 framing so a residual decode error is a dropped frame, never
  corrupted data. Package-tested end to end: a channel running ~5% raw bit
  errors (Eb/N0 = 4 dB) decodes every frame clean. Pure DSP — no radio or
  TX path touches this yet; LUMEN/DUET/ARIA will ride it behind the future
  Experimental Modes (Lab) gate. Next increment: ARQ.

## [2026.0728_012] — 2026-07-28

- **Network Speakers (Tools ▸ Network Speakers).** HermitSDR now finds the
  AirPlay and Sonos receivers on your local network and lists them, so you
  can see what's available to listen on. To route the receiver audio to one,
  set it as your Mac's Sound Output (or pick it in the gear ▸ audio-output
  menu) — there's a button to jump straight to Sound settings. This is
  discovery + routing help; direct casting from inside the app isn't built.

## [2026.0728_011] — 2026-07-28

- **Ask The Crab can do more, and now replies as it thinks.** Answers
  **stream in live** word-by-word instead of appearing all at once. And the
  crab picked up six new skills on top of tune / mode / volume / status: it
  can **switch bands** (“take me to 40 meters”), **turn decoders on/off**
  (FT8, the skimmer, ALE), toggle **noise reduction** and the **sub-receiver**,
  **bookmark** the current frequency, and give you a quick **band-conditions**
  read from the planetary K-index. Still fully on-device and private.

## [2026.0728_010] — 2026-07-28

- **Ask The Crab — a built-in AI assistant.** A little crab button in the
  header (and Tools ▸ Ask The Crab) opens a small prompt window where you can
  ask the app anything — “why does my SSB sound inverted?” — or just tell it
  what to do: “tune to 14.074 MHz”, “switch to LSB”, “set volume to 60%”,
  “what’s my status?”. It runs **entirely on-device** and **privately** on
  Apple’s Foundation Models (Apple silicon, macOS 26) — nothing leaves your
  Mac, no account, no network. It can drive the radio through a small set of
  tools today; the plumbing is built to be extended with more agentic
  capabilities (and other model backends) over time. If your Mac isn’t
  Apple-Intelligence-eligible, the window says so instead of pretending.

## [2026.0728_009] — 2026-07-28

- **YouTube Live streaming.** Broadcast the HermitSDR window plus your
  receiver audio (and the TX monitor while you transmit) straight to
  YouTube Live — Tools ▸ YouTube Live. Two ways in: paste a **stream key**
  from YouTube Studio (no sign-in), or connect a **YouTube account** and let
  HermitSDR create and start the broadcast for you via the YouTube Data API
  (OAuth; needs a Google Cloud project with the Data API v3 enabled). Pick
  the title, privacy, resolution and bitrate, hit **Go Live**. Built on a
  hand-rolled, dependency-free RTMP stack (AMF0 + chunk framing + FLV muxing
  + handshake), ScreenCaptureKit window capture → VideoToolbox H.264, and
  AAC audio off the same speaker mix Discord uses — all package-tested at the
  wire level. First use asks for Screen Recording permission. Stream key,
  OAuth secret and refresh token live in the Keychain.

## [2026.0728_008] — 2026-07-28

- **VPN Mode.** A new low-bandwidth mode for running HermitSDR — or
  screen-sharing it — over a remote/VPN link. It trades richness for
  bytes on the wire: caps the IQ sample rate at 96 kHz (a quarter of the
  384 k default's UDP rate), forces a flat static waterfall, turns off
  animations and the DX ticker and CRT glass, slows the waterfall redraw
  to 15 fps (so a screen-shared session sends far fewer pixels), and
  trims the Discord voice bitrate. A startup prompt offers **Full
  Experience** (the default) or **VPN Mode** each launch — with a "Don't
  ask again" checkbox — and a **Full / VPN** toggle in the header flips
  between them any time. Switching to VPN Mode snapshots your rich
  settings and switching back restores them exactly, so your sample rate,
  3D waterfall and animations come back the way you had them.

## [2026.0728_007] — 2026-07-28

Calmer-by-default cosmetics, an ALE decoder that holds sync, plus a batch
of robustness fixes for the recorders and decoders.

- **Arcade FX is now off by default.** A fresh install starts calm — no
  balloons, critters, fireworks or floaters. Turn the eye-candy on any
  time with the **Arcade FX** toggle in the appearance (palette) menu or
  the **`A`** hotkey. Existing installs keep whatever you already had set.
  (The lightning-static warning is unaffected — it's advisory safety, not
  decoration.)
- **ALE holds sync through long transmissions.** The 2G-ALE monitor now
  recovers symbol timing at two granularities: while unsynced it votes a
  coarse grid of sub-symbol boundary phases and jumps to the strongest
  (a half-symbol misalignment used to straddle every tone window and
  corrupt tribits below what the triple-vote could outvote), and once
  word-synced it nudges the boundary ±1 sample at a bounded rate to ride
  a few-hundred-ppm TX/RX clock offset without jitter. The noise floor
  now learns across all candidate phases, so a misaligned start no longer
  looks like silence.
- **FIXED: WEFAX polarity flip re-announced a finished chart.** Toggling
  INV on a completed fax re-emitted it as in-progress; it now re-emits
  with the same done state.
- **FIXED: SSTV unmatched R-Y row rendered white.** A dropped R-Y match
  under QRM/QSB left a stashed luma row at its blank init value; it's now
  salvaged with neutral chroma instead of a white streak.
- **FIXED: IQ replay dropped the file's final <20 ms on every loop** — an
  audible tick on short loops — and could spin forever on a sub-tick-sized
  file. The partial tail is now delivered (whole IQ pairs only) before the
  seek-to-loop, through one shared sanitizing path.
- **FIXED: WAV length over-reported after a disk-full stop.** `seconds`
  now reports frames actually flushed to disk, not buffers a failed write
  discarded (up to ~5.5 s over).
- **FIXED: decoder status could flicker a stale snapshot.** Session
  begin/mutate/end now serialize handler delivery in state order, so a
  concurrent update can't emit ahead of a begin's ended/updated pair.
- **OmniSkimmer GPU mid-drain resets now count as drops** instead of
  vanishing from every counter, and the batches already computed in that
  drain are kept rather than discarded.

## [2026.0728_006] — 2026-07-28

Two operator-approved follow-ups from the second sweep's design questions:

- **6 m on the ANAN.** The VFO ceiling now follows the connected radio
  (54 MHz ANAN, 30 MHz HL2 — adopted at connect like the RF-gain model),
  where a fixed 30 MHz clamp had made 6 m unreachable even though the TX
  side and the 6 m preamp toggle already supported it. New "6m" band
  preset (50.125 USB, full 50–54 band memory); the Band menu hides bands
  the connected radio can't tune. VFO A/B, CAT, and restore clamps all
  follow the radio.
- **CAT server binds to localhost by default.** The rigctl server is
  unauthenticated and accepts tune/mode/PTT requests (RF stays gated by
  ARM) — it now listens on loopback only, which keeps WSJT-X and loggers
  on this Mac working unchanged. A new "Allow CAT from other machines on
  the LAN" toggle (gear popover, persisted, off by default) restores the
  old any-interface behavior for remote clients.

## [2026.0728_005] — 2026-07-28

The TX-safety half of the second sweep — reviewed and approved:

- **FIXED: stuck PTT on focus loss.** Holding the PTT key (Space) and then
  clicking into any text field made the text-editing gate eat the key-up —
  and Cmd-Tabbing away delivered the release to the other app — either way
  **MOX stayed up indefinitely**, the one found path where physical-key
  state and keyed RF could diverge. Held-action release now processes
  before the text-editing gate (release is unconditional once a hold is
  live), and app deactivation force-releases any held action.
- **FIXED: P2 live sends could interleave with the stream bring-up.**
  `running` goes true ~200 ms before the staged General→DDC→DUC→RUN
  sequence completes; a CAT PTT or diversity flip in that window fired a
  high-priority packet ahead of the sequence — a premature RUN with
  unsent config, after which the bring-up's own DDC-specific landed
  mid-RUN (the documented fw 2.1.18 IQ-stall packet class). Live-change
  sends now wait for bring-up completion; the bring-up packets themselves
  carry the current config, so nothing is lost.
- **FIXED: Alex T/R relay stuck in TX after stop-while-keyed.** The
  firmware only drives relays on a General, and the General latch was
  gated on RUN — so the final RUN=0 stored the T/R release without ever
  driving it; the relay sat in the TX position until the next session's
  bring-up. Stop/disconnect while keyed now sends one unkeyed RUN=1
  high-priority first, whose Alex change fires the General (T/R released,
  PA bit clear), then RUN=0.
- **FIXED: P1 force-unkey callback threading** — the stream-watchdog fire
  site delivered on the network queue while every other site (both
  protocols) delivers on main; unified to the documented contract.

## [2026.0728_004] — 2026-07-28

Second bug sweep of the day: six parallel review agents over everything the
morning sweep didn't cover (protocol/network, app-state core, audio +
services, decoders + recording, integrations, skimmer + CASCADE + views),
every finding verified against source before fixing. TX-adjacent findings
are staged separately for review, as usual.

### Fixed — crashes and wedges

- **FT8/FT4 decode could silently die for the session.** The C decoder's
  per-slot duplicate table consumed slots even for messages that later
  failed message-decode, and its probe loop had no cap — a busy contest
  slot could fill the table and spin the decode queue at 100% CPU forever.
  Probe loop bounded (same fix the callsign hashtable already had).
- **Remote crash via CAT:** `F nan` over rigctl parsed successfully, landed
  NaN in the optimistic frequency mirror, and a `get_freq` before the
  main-thread round-trip trapped in `Int(freq)`. Values are now validated
  (finite, 0–2 GHz) at the protocol boundary.
- **Crafted/corrupt `.hiq` file → allocation storm.** The header's sample
  rate was unbounded (only ≥12 kHz was checked): a corrupt rate like
  3.1 GHz meant ~503 MB per replay tick. Clamped to the P2 maximum.
- **Discord voice remote-data crash:** the voice READY payload's
  `ssrc`/`port` used trapping integer conversions on server-controlled
  JSON. Now clamping.
- **CASCADE bit loader trapped on a zero-noise sounding** (`Int(+inf)`
  on a clean loopback — exactly the dummy-load regime it targets).

### Fixed — leaks and lost data

- **CPU meter leaked ~144k Mach port refs per hour** — `task_threads`
  returns a send right per thread and only the array was freed. Long RX
  sessions grew the task's port table without bound.
- **Discord token could be permanently lost:** the every-launch Keychain
  migration removed the defaults copy even when the Keychain write failed
  (locked keychain) — now gated on the write succeeding.
- **Privacy opt-out could be silently reverted:** the fresh-install
  settings import and the SquareDeck migration copied wholesale over keys
  the user had already set (non-persist() keys like the usage-ping toggle
  don't plant the "has run" sentinel). Both now skip existing keys.
- **Settings flush at quit could be clobbered** by an in-flight debounced
  export (cancel() can't stop an executing work item) — flush now
  serializes through the export queue.
- **cty.dat cache written non-atomically** — a torn cache shadowed the
  bundled snapshot for up to 7 days.

### Fixed — behavior

- **DX cluster:** reconnect backoff now resets on login success, not TCP
  connect (a rejecting node was hammered every 2 s forever — the exact
  behavior sysops ban clients for), and TCP keepalive detects half-open
  connections ("spots flowing" while nothing arrives, forever).
- **Discord:** pasting the bot token after enabling the integration now
  starts it (was a dead end until toggling off/on); a garbled gateway
  resume URL or voice endpoint no longer strands the session in
  "connecting…" limbo; a server-requested heartbeat no longer risks a
  spurious zombie-reconnect; stale voice audio (up to 1 s) no longer
  replays at the next voice join; LoTW fetch uses an ephemeral URL
  session so the password can't reach the on-disk URL cache; TQSL
  failure summaries no longer lose their final stderr chunk.
- **Cross-band spot click corrupted band memory:** tuning to a cluster
  spot/ticker entry baked the NEW mode + filter into the DEPARTING band's
  memory (missing `restoringBand` bracket its siblings have).
- **SWR-guard threshold from a hand-edited Settings.plist silently
  skipped the engine push** (didSet early-return on clamp) — UI showed
  the clamped value, protection used the old one.
- **Decoder sessions from file replay were stamped as live** (Discord
  "decode complete" events posted during `.hiq` replay).
- **Rate change while time-shifted left FT8's historical slot clock in
  place** (one-line consistency fix with its sibling paths).
- **Stopped audio-output device fallback:** if the preferred output device
  disappeared (USB unplugged, BlackHole uninstalled) the engine retried
  against the dead device and gave up — RX audio dead until manual
  re-pick. Now falls back to the system default (the MicInput lesson,
  applied to the output side).
- **Voice-check playback:** a quick play→stop→play could go silent (stale
  completion handler nilled the new player — identity guard added).
- **Updater:** the release-asset picker now matches the app zip
  specifically (a future dSYMs.zip attachment would have broken every
  one-click install); the swap helper bails to manual install if the app
  never exits (was: swap under a running process → two instances).
- **OmniSkimmer:** NCO retune now flushes pending old-span IQ (up to
  0.5 s was channelized under the new center); CW re-probe no longer
  flaps CW→?→CW every 10 s (cumulative stats reset); per-session drop
  stats; TX-banner arcade jiggle timer actually fires now (9.71
  stored-publisher class); WEFAX max-length charts keep their final ~11
  lines in re-render; CW decoder SNR now reads correct (was half — 
  10·log10 on an amplitude ratio); discovery replies can no longer
  surface after stop; IQ recorder guards mismatched plane lengths.

### Performance

- P2 hot path: per-datagram source check is now a numeric compare (was
  inet_ntop + String alloc ~6.5 k/s on the queue that paces RF); wideband
  bandscope packets bulk-convert via vDSP (was ~2.4 M bounds-checked
  Data subscripts + appends/s); IQ sequence tracking uses fixed slots
  (was a Dictionary hash per packet).
- Band-memory writes are debounced off the tune path (was a UserDefaults
  bridge + change-notification per scroll tick); DX spot expiry no longer
  re-publishes the whole UI tree every second when nothing expired.

## [2026.0728_003] — 2026-07-28

The TX half of today's bug sweep — reviewed and approved before shipping
(all five are on-air signal-purity fixes, verified against the source):

- **FIXED: SSB roger beep replayed ~10.7 ms of un-faded voice.** The beep's
  delayed-I path spliced raw Hilbert filter history in AFTER the voice tail
  had been faded to silence and a 5 ms gap inserted — a full-amplitude,
  mid-waveform step (the key-click class of splatter the envelope machinery
  exists to prevent) on every beeped SSB unkey. The beep now modulates from
  zeroed filter state: silence → gap → click-free beep (its own 4 ms
  raised-cosine edges shape the onset).
- **FIXED: AM +peak at 125% hard-clipped at the wire.** The 1.28 chain cap
  consumed the Int16/Int24 headroom exactly (0.45·(1+0.95·1.28) = 0.9972),
  but the limiter's 0.95 bound is not preserved downstream: the post-limiter
  bandpass regrows shaved peaks (Gibbs overshoot) and the P2 interpolation
  FIR adds true-peak overshoot — dense asymmetric program clipped at the
  DAC conversion, after every band-limiting stage. Chain cap is now 1.22
  (~2.8% true-peak margin); the slider tops out at 120% (persisted 125%
  values clamp down on first launch).
- **FIXED: SSB with CESSB off could clip one quadrature at the wire.** The
  limiter bounds the REAL waveform at 0.95, but the Hilbert Q of heavily
  limited speech regrows past ±1.0 (the analytic envelope is not bounded by
  the real peak) — and the wire conversion clipped Q alone: asymmetric
  distortion plus opposite-sideband spurs injected after all filtering,
  invisible to every meter (they read pre-modulation audio). An always-on
  envelope trim at 1.0 on the analytic pair (same op as CESSB's final
  stage, phase/PEP preserved) now guards the wire; it touches only
  overshoot samples.
- **FIXED: beep-off unkey tail.** With the roger beep off, unkey left the
  key envelope up and the ring tail un-faded until the next mic block —
  so (a) a CAT client switching modes mid-over (WSJT-X `M`) radiated
  ~10 ms of the NEW mode's modulation in the tail (a full-carrier AM blip
  on a USB→AM switch), and (b) a fast re-key cleared the draining ring
  outright — an IQ step from full amplitude to zero, the exact key click
  the fade-instead-of-clear machinery was written to prevent, just on the
  beep-off path. Unkey now fades the tail in place, zeroes the envelope,
  and arms the same re-key fade window the beep path gets.
- **FIXED: TX pre-fill latency stuck after leaving a large-block mic.** The
  observed-mic-block estimate only ever ratcheted UP — switching from the
  MOTU M4 (4800-sample blocks) to a 512-block interface kept ~110 ms of
  avoidable key-down voice latency until app restart. The estimate resets
  on mic device change.

## [2026.0728_002] — 2026-07-28

Bug-sweep release: three parallel review agents over the RX chain, TX chain,
and waterfall/rendering pipeline (~11k lines), every finding verified against
the source before fixing. RX + rendering fixes below; the TX-chain findings
are staged separately for review before they ship.

### RX / DSP

- **FIXED: `.hiq` replay NaN poisoning.** IQ file replay fed raw disk floats
  straight into the chain; a corrupt or foreign file carrying one NaN/Inf
  pair permanently latched multiple adaptive stages (auto-notch weights →
  silence until toggled, noise-blanker gate → blanking and the lightning
  watch silently dead, AGC back-averages → no hang/recovery until reset).
  Samples are now sanitized at ingest — one guard protects every stage.
- **FIXED: stale EQ state splice.** Re-raising an audio-EQ band that had sat
  bypassed at 0 dB spliced the section's frozen delay-line samples (from
  whatever was playing when it was zeroed, minutes ago) into the fresh
  recursion — a one-shot click. State is zeroed on the bypass→active
  transition; live drags through zero stay clickless (the section is
  near-identity at the ±0.01 dB crossing).
- **FIXED: mismatched IQ pair lengths could overrun.** `RXChain` sized its
  mixer loops from the I count while writing through the Q buffer; a caller
  passing unequal lengths would read/write past the end. Now truncated to
  the paired length at ingest (same guard SpectrumAnalyzer already had).
- **Perf: noise blanker vectorized + sub-RX dead work removed.** The
  blanker's per-sample |I|+|Q| pass — the largest scalar cost in the RX path
  at full IQ rate — now runs as three vDSP calls; and the sub-RX chain no
  longer burns a full-rate detection pass feeding an impulse counter nobody
  reads (only the main chain drives the lightning watch).
- **Perf: AM envelope via `vDSP_zvabs`** (was a scalar sqrt loop), wideband
  spectrum max-hold via strided `vDSP_vmax` (3 full-width calls instead of
  ~100k tiny dispatches/s), and the fade-leveler's per-call `exp()`
  constants hoisted.

### Waterfall / rendering

- **FIXED: waterfall PNG capture froze the UI.** The capture's PNG encode
  (up to ~500 ms on a Retina window) ran inline on the Metal
  completion-handler queue — ahead of the frame semaphore's signal, so the
  render loop (and main thread) stalled for the whole encode. The readback
  and encode now hop to a background queue; capture is stall-free.
- **FIXED: NaN spectrum bins painted permanent white streaks.** A NaN dB
  value survives Swift's `min/max` clamp as +100 dB and landed in the
  history texture as a full-scale white pixel forever. Non-finite bins now
  clamp to the floor.
- **FIXED: rare hot-white triangle flash in 3D.** The 3D rim-light term took
  `pow` of a slightly negative base when a mesh normal aligned exactly with
  the view ray (normalize() rounding pushes the dot past 1.0) — NaN, which
  the EDR composite turned into a max-brightness flash. Clamped with
  `saturate`.
- **FIXED: carrier beacons sat half a bin right of the peak** (visible at
  high zoom — the pulsing glow rode the shoulder of narrow carriers, ~5 px
  off at ×8). Beacons and their sparkles now share the trace's exact grid.
- **FIXED: beacon pulse degraded over multi-day sessions.** The pulse phase
  grew unbounded; after a day the shader's `sin()` visibly quantized. Now
  wrapped to 2π like the established `timeSec` mod-3600 pattern.
- Minor: `preferredFPS` changes are honored on view updates (was applied
  only at creation); S-meter/TX-scope no longer strand an acquired drawable
  in an uncommitted command buffer when encoder creation fails.

- **Release pipeline: launch smoke test.** `tools/release.sh` now opens the
  signed Release build and confirms it stays running for a few seconds before
  spending a notarization submission — aborting if it crashes on launch. This
  is the gate that would have caught the 2026.0727_002 launch crash, which a
  pure compile-pass could not (nothing had actually run the app). Tooling
  only; no app change.

## [2026.0728_001] — 2026-07-28

- **Check for Updates.** HermitSDR can now update itself. **HermitSDR menu ▸
  Check for Updates…** compares the running build against the latest release
  and, if a newer one exists, shows its notes and a one-click **Install &
  Relaunch**. The installer downloads the notarized zip and — before trusting
  it — verifies the code signature, the HermitSDR developer Team ID, and the
  Apple notarization ticket, then swaps the app in place and relaunches; if
  anything doesn't check out (or the app isn't in a writable spot), it falls
  back to opening the release page for a manual drag-install and never leaves
  a half-swapped bundle. A quiet daily background check (toggleable in the
  window; on by default) surfaces the same window only when an update is
  found, with **Skip This Version** to silence a build you don't want.
  Install is blocked while the transmitter is armed/keyed. No third-party
  updater framework — it's a small client over the GitHub Releases API.
- **Hotkey: toggle screen animations.** A new key binding — **A** by default,
  rebindable under Settings ▸ Keys — toggles the Arcade FX layer (the balloon,
  VOTE-for-democracy, critters, fireworks and the rest) without reaching for
  the paint-palette menu. Same setting as the existing "Arcade FX" toggle,
  which now shows the shortcut in its tooltip.
- **Fixed: 2026.0727_002 crashed on launch.** The new skin-aware window
  chrome from 2026.0727_002 read the active skin from `@EnvironmentObject`,
  but it is applied as an *outer* modifier on every window — above the
  `.environmentObject(radio)` injection — so at launch SwiftUI could not
  find `RadioState` and trapped (`EnvironmentObject.error()`) the instant the
  first window's content view was installed, before anything drew. (The
  regression slipped out because 2026.0727_002 shipped without a launch
  check.) The chrome now reads the skin from a process-wide `SkinCenter`
  holder that never depends on environment-injection order, so every window —
  including auxiliary ones that never injected `radio`, like the Trophy Case —
  opens cleanly and still re-tints live on a skin swap. Verified by actually
  launching the built app. No functional change beyond the fix.

## [2026.0727_002] — 2026-07-27

- **Skins.** A new **Skin** picker (paint-palette menu) switches the whole
  app between two looks. **Hermit** (default) is the original warm, analog
  feel — navy chrome and the phosphor "comet" S-meter with its over-S9
  flames. **Flux Radio** mimics Flex SmartSDR: near-black charcoal chrome, a
  cool cyan-blue accent, and a **flat segmented LED S-meter** (uniform green
  bar, red over S9, a crisp cyan peak line — no comet, no flames). The Metal
  waterfall, arcade sprites, CRT glass and every other bit of eye-candy carry
  over unchanged in both skins. Persisted (`skin`). Groundwork for
  per-view meter re-styling (TX meters, multimeter) is in place via
  `SkinTokens`; the header S-meter and window chrome are the first surfaces
  to follow the skin.
- **Experimental Modes — CASCADE preamble sync (LAB ONLY, no UI yet).** The
  modem core assumed the receiver already knew where each symbol started; a
  real link doesn't. Added a **Schmidl & Cox preamble** (`DSP/Cascade/
  CascadeSync.swift`) that recovers an unaligned, frequency-offset stream:
  an even-subcarrier symbol whose two identical time halves give the
  fractional **carrier-frequency offset** (from the half-to-half phase) and
  a coarse timing plateau, then a **matched-filter cross-correlation**
  against the known preamble body sharpens timing to the sample. Wired into
  `CascadeModem` as `encodeFrame`/`detectFrame`/`syncDecode`. Pinned by
  `CascadeSyncTests`: a full frame dropped into noise at an unknown offset
  with a fractional CFO is found (timing within a few samples, CFO within
  0.03 subcarriers) and decoded end-to-end at BER < 1e-2, and pure noise
  does not trip a false detection. Next increments: LDPC FEC + CRC, then the
  three mode app layers (LUMEN/DUET/ARIA).

## [2026.0727_001] — 2026-07-27

- **SWR protection (configurable, PTT settings).** The Protocol-2 PA
  already force-unkeyed on sustained high SWR, but at a fixed 3.0:1 that
  only wrote to the log. It is now a proper feature: a **"SWR guard"**
  control in the TX panel with an on/off switch (on by default) and a
  **1.5–10:1 trip level** (default **3.1:1**), persisted. When it trips it
  stops transmitting *and* raises a **dialog** explaining the SWR that
  fired and to check the antenna/feedline. A lab operator can turn it off
  entirely. (ANAN/P2 only — the HL2 has no reflected-power sensor.)
- **Experimental Modes — CASCADE modem core (LAB ONLY, no UI yet).** The
  shared physical layer for the coming experimental modes (LUMEN image,
  DUET split-screen chat, ARIA hi-fi voice). `DSP/Cascade/`: a
  complex-baseband **adaptive-OFDM** modem — Gray-coded square-QAM
  (BPSK…4096-QAM, unit power), cyclic-prefix OFDM mod/demod over vDSP
  DFTs, scattered-pilot 1-tap channel equalization (recovers through
  multipath in test), and DSL-style **adaptive bit-loading** that pours
  bits onto high-SNR subcarriers (SNR-gap rule). Pure DSP, no TX, gated
  for lab/dummy-load/closed-network use only — it deliberately ignores
  symbol-rate/bandwidth limits and must never radiate on the air. Pinned
  by `CascadeTests` (QAM round-trip, OFDM identity, AWGN BER, multipath
  equalization, bit-loader, throughput). Next increments: LDPC FEC + CRC,
  Zadoff–Chu preamble sync + CFO, then the three mode app layers.
- New versioning scheme (`YYYY.MMDD_XXX`); `release.sh`/`make-dmg.sh`
  version extraction updated to carry the full string.

## [9.91] — 2026-07-27

- **C-QUAM TX→RX loopback test + honest separation status** (issue #32).
  A new end-to-end test crosses BOTH production chains — feed L/R into
  `TXChain` (AM + C-QUAM), pull the wire IQ, undo swapIQ, and demodulate
  through `RXChain`'s SAM path. It proves the two guarantees that hold on
  the air today: **mono compatibility** (an ordinary AM listener recovers
  L+R faithfully through the full dynamics chain) and the **25 Hz stereo
  pilot** lighting the STEREO lamp end-to-end. It also pinned a real
  limitation: full channel **separation collapses** through the TX
  dynamics chain, because the difference channel does not yet track the
  sum's audio processing (phase rotator / EQ / compressor / limiter). The
  "AM stereo" help text now says so plainly; a matched difference chain is
  the next C-QUAM milestone.
- **Bug-sweep fixes** (4-agent review across TX, RX, protocol, app state):
  - **RX overload-mute hysteresis** — the ear-protection overload mute
    shared the squelch gate with a bare threshold compare, so a signal
    parked at the mute level chattered the gate open/closed every ~20 ms
    (audible ~25 Hz warble). It now latches with the same 6 dB hysteresis
    the squelch uses, holding a clean mute.
  - **C-QUAM difference channel now takes mic gain** — the stereo
    difference was tapped from the raw L/R and skipped the `micGain` the
    sum path applies, mis-balancing the decoder's (S±D)/2 matrix whenever
    mic gain ≠ 1. With the gain matched, the linear path is exact at flat
    EQ (the remaining EQ/dynamics matching is the milestone above).
  - **P2 high-priority status honors `running`** — a stale status
    datagram arriving after `stopStream()` no longer runs telemetry EMAs
    or fires `onADCOverflow` into a torn-down session (matches the
    `guard running` its IQ/mic/wideband siblings already had).
- The full DSP suite is green at 220 tests (two new loopback cases).

## [9.90] — 2026-07-26

- **C-QUAM AM-stereo transmit** (issue #32, milestone 3) — the encoder
  counterpart of the C-QUAM decoder. `CQUAMStereoEncoder` (promoted from
  the spec test fixture, so it is bit-identical and round-trips through
  the production decoder at >30 dB separation) emits the classic
  Motorola form: a pure-AM envelope carrying the mono sum (L+R) — any AM
  receiver hears mono — with the difference (L−R) plus a 25 Hz pilot in
  the phase. Wired into `TXChain`: in AM mode with a stereo source (the
  file player), the sum drives the full processing chain as the envelope
  (peak control rides the envelope only, never the phase) while the
  difference is band-limited and delay-aligned and rides the quadrature.
  New "AM stereo (C-QUAM)" toggle in TX Controls (AM mode), persisted as
  `txCQUAM`. A first cut — the encoder core is exact and test-pinned; the
  through-chain stereo separation still wants dummy-load tuning, and the
  L/R orientation is to be confirmed on the air (like the SSB sideband
  sense was). Not yet transmitted on hardware.
- **TX telemetry logger** (calibration aid, issue #34) — an opt-in CSV
  capture of transmit telemetry for dummy-load work. While keyed it
  appends `burst, elapsed_s, drive_pct, fwd_v, rev_v, swr, watts_est,
  pa_current_a, temp_c` to a per-session file under
  `~/Documents/HermitSDR TX Telemetry/`, one burst index per key-down so
  drive-level sweeps group cleanly. Off unless the `txTelemetryLog`
  default is set (`defaults write com.hermitsdr.app txTelemetryLog -bool
  true`), so it never runs in normal operation and adds no UI. Purpose:
  gather the PA-current-vs-drive points needed to re-fit the low-end
  current curve and to calibrate forward power against an external meter
  over a slow remote link, where reading live meters is impractical.

## [9.80] — 2026-07-22

- **Niagara waterfall mode** — a new hybrid view (the waterfall picker is
  now Flat / 3D / Niagara). The most recent rows lie on a flat "river"
  running toward you, then curl over a lip and fall away into the
  distance for older rows — a spectrum waterfall that pours over a cliff.
  Built on the existing 3D mesh path with a bent geometry and its own
  camera; amplitude adds relief on the flat and fades down the falls.
  A first cut — the cliff position, fall depth, camera angle, and
  shading on the falls are all easy to tune from here.

## [9.73] — 2026-07-22

- **Stream Deck support — foundation** (#52, physical companion to #24):
  the pure, unit-tested groundwork for driving an Elgato Stream Deck as a
  radio operator keypad. `StreamDeckProtocol` (model table + HID image-
  report framing + key-state parse + brightness/reset feature reports,
  MK.2 15-key first) and a **shared action model** (`DeckAction` /
  `DeckButton` / `DeckPage` / `DeckLayout`) that the physical deck and the
  future on-screen deck (#24) both use — radio actions (PTT, TUNE, band,
  mode, tune steps, NB/NR/notch/split/sub toggles, memory, palette) and
  media actions (clip/segment/stop/URL). Native IOKit HID, no third-party
  dependencies. 6 protocol tests green; no user-visible feature yet — the
  HID transport, tile rendering, radio wiring, and config UI follow in
  #52's later phases. TX keys will sit behind the existing ARM interlock.

## [9.72] — 2026-07-21

Two low-hanging issues off the board:

- **OmniSkimmer RTTY handles off-nominal shift** (#15): the probe already
  measures the FSK shift, so the decoder is now seeded from that
  measurement instead of a hardwired ±85 Hz (170 Hz). Shifts from 170
  through ~300 Hz classify and decode; a 250 Hz-shift signal is now a
  regression fixture. Wider shifts (425/850 Hz) put a tone past the
  ~375 Hz channelizer bin edge and still need a multi-bin RTTY combiner
  (noted on #15 as future work).
- **PA drain-current meter stops showing a wrong near-zero value** (#34):
  the AIN→amps fit is calibrated at operating power and its offset
  subtracts the idle-bias baseline, so below ~1 A it under-read ~10× (it
  showed 0.04 A at a real ~0.5 A). The meters now show "—" below the
  trust floor — honestly "unknown" rather than a precise-looking wrong
  number. Operating-power readings (the ones used to confirm the radio's
  power calibration) are unchanged. A correct low-end curve needs a
  dummy-load current measurement to calibrate.

## [9.71] — 2026-07-21

**Bug-sweep + performance pass** (four parallel subsystem reviews — RX
DSP, waterfall/GPU, arcade overlay, memory/CPU — every finding verified
against the source before fixing):

Bugs:
- **Arcade sprites starved under load** (HIGH): the overlay's 1 Hz
  scheduler was a `Timer.publish` stored on the view struct, so every
  `RadioState` publish rebuilt the struct and reset the countdown before
  it could fire. With OmniSkimmer or the DX cluster running (spots
  publish several times a second), time-scheduled sprites never spawned
  AND their cleanup never ran — which also left `comboEvents` growing
  and pinned the overlay at 60 fps. Converted to a `.task` loop tied to
  view identity (the same fix the ticker already uses), so it survives
  rebuilds. This is the same class of bug the ticker hit; it had spread
  to the sprite scheduler.
- **Trophy case miscounted**: six trophies added recently (shack cat,
  QSL pigeon, tumbleweed, fireflies, meteor scatter, disco ball) were
  awarded but missing from the catalog, so they were invisible and the
  counter could read "7/6". Catalog completed; the counter now tallies
  only catalogued trophies.
- **Waterfall peak-hold fell at the wrong rate on ProMotion**: it
  decayed per draw frame, so it dropped twice as fast at 120 Hz as at
  60 Hz. Now scales by ingested rows (like the ghost trace) — refresh-
  rate independent, and it freezes when the data stalls.
- **`heardGrids` grew unbounded**: the FT8 heard-grid map only ever
  appended, one entry per Maidenhead field for the whole session. Now
  capped (least-heard evicted).

Performance:
- **RX down-conversion mixer** fused from six vDSP passes (4×mul + sub +
  add) into a single `vDSP_zvmul` complex multiply — same math, far less
  memory traffic at up to 1536 kHz. Sideband-sense regression tests
  confirm it's identical.
- **Decimator cascade** no longer allocates a fresh output array per
  stage per block (~2.7k heap allocations/s at 1536 kHz eliminated) —
  reuses a persistent buffer, COW-safe.
- **Mixer phase ramp** writes through an unsafe buffer pointer, dropping
  per-element bounds checks on a full-rate scalar loop.
- **Depth-of-field blur target** (a ~15 MB full-drawable texture per
  renderer) is now allocated only while the 3D waterfall's DOF is active
  and freed in the default flat mode, instead of sitting resident always.

Deliberately not changed: the 180 s IQ time-machine ring stays always-on
(gating it would break "rewind what already happened," and its RAM isn't
scarce on the target hardware); the P1 per-sample IQ decode keeps its
current form (a subscript-fill micro-opt wasn't worth risking an
un-hardware-testable receive path).

## [9.70] — 2026-07-20

- **Usage-ping system, both ends** (extends the 8.20 Settings ▸ Privacy
  beacon): the app now POSTs its anonymous daily ping — install UUID,
  app version, build, full macOS version, CPU architecture — as JSON to
  hermitsdr.com/api/ping (endpoint still overridable via the
  `usagePingURL` default, no rebuild needed). The server side ships in
  the repo under `tools/server/`: a stdlib-only Python capture service
  (systemd-sandboxed, nginx-fronted with rate limiting) that appends
  one JSON line per ping and resolves a coarse country from the
  connection's IP **locally** via geoip — no third-party analytics or
  lookup services on either end, IPs never leave the box. Includes a
  `telemetry-report.py` summarizer (unique installs; breakdowns by app
  version / macOS / arch / country, counted per-install rather than
  per-ping) and a step-by-step Debian/Ubuntu install README. Hardened
  and integration-tested against malformed input: strict field
  allow-list, UUID-shape check, 2 KiB body cap, printable-ASCII
  clamping — junk is answered 204 and dropped, never reflected. The
  toggle help text and a new README Privacy section disclose exactly
  what is (and is not) collected.

## [9.60] — 2026-07-20

- **Disco ball**: at most once every 3 hours (the timer re-randomizes
  to 3–6 h after each show), a mirror ball winches down from the top
  of the window with a damped overshoot, spins — facet highlights
  sweep the tiles — and throws twelve hue-cycling rays plus wandering
  sparkle glints for about five seconds before retracting into the
  ceiling like nothing happened. Arcade FX only. New trophy:
  MIRROR BALL — THE BAND IS A DANCE FLOOR.
- **Every build is now code-signed** with the Developer ID Application
  certificate (Damon's Apple Developer Program membership, team
  UG29A6ZW54) — Debug and Release both, wired as manual signing in the
  project. Stable identity means the Keychain authorization dialog now
  appears at most ONCE per protected item, ever, instead of once per
  rebuild; it also clears the runway for the first notarized public
  release (#43 — one `notarytool store-credentials` step remains).

## [9.51] — 2026-07-20

- **Keychain prompt tamed**: the Discord token now loads from the
  Keychain LAZILY — only when the integration is enabled at launch,
  when it starts, or when its settings window opens. Idle launches
  never touch the Keychain, so unsigned Debug rebuilds (whose identity
  churn triggers the macOS authorization dialog) no longer ambush you
  with a prompt when you aren't using Discord. A token freshly read
  from the Keychain is also no longer written straight back (the write
  was its own second prompt). Prompts disappear entirely once Debug
  builds sign with a stable identity (#43 — needs the one-time Xcode
  certificate step).

## [9.50] — 2026-07-20

**The sparkle menagerie** — six new inhabitants for the arcade layer
(all behind Arcade FX, all click-transparent, all rate-limited):

- **Shack cat**: pads along the spectrum boundary, sits, swishes its
  tail, blinks its green lamp eyes, swats one spark out of the
  spectrum, stretches, and leaves. Joins the critter rotation.
- **Tumbleweed**: when the S-meter has sat on the floor with zero
  decode events for 3 straight minutes, a tumbleweed rolls across the
  dead band, hopping less and less. Comedy that doubles as a
  band-condition indicator.
- **Fireflies**: after local sunset (21:00–04:59), a six-firefly swarm
  drifts through the deep waterfall every few minutes, each pulsing on
  its own clock.
- **QSL pigeon**: logging a QSO launches a courier pigeon that flaps
  across the sky towing your QSL card on a string. The bureau was
  never this fast.
- **Meteor showers**: during the nine real annual showers (IMO UTC
  calendar — Quadrantids through Ursids), meteors streak the spectrum
  sky with bright heads and fading trails; some say PING! because
  every ham hears meteor scatter in their heart. First sighting of
  each shower is its own trophy — nine collectibles a year.
- **Satellite pass**: every 15–40 minutes a tiny satellite crosses the
  top of the window — solar panels, blinking beacon, and one specular
  glint mid-pass when the panels catch the sun.

New trophies: SHACK CAT, DEAD AIR, NIGHT SHIFT, PAPER CHASE, and the
nine METEOR SCATTER shower observations.

## [9.40] — 2026-07-20

Three feature remainders off the board (#15, #42):

- **OmniSkimmer multi-bin combining** (#15): off-center RTTY whose far
  tone aliased past the ±187.5 Hz channel edge was classify-only — now
  it decodes verbatim. The filterbank is critically sampled at the
  channel spacing and keeps the input carrier phase, so the
  straddle-side neighbor's stream adds essentially in phase (relative
  phase e^(−jπ/N) ≈ 1.4°); one coherent add restores the far tone at
  full amplitude. Found and fixed on the way: aliasing inverts the
  apparent tone order, and inverted Baudot is 100% printable letters —
  the printable-ratio polarity score could NOT tell the two UARTs apart
  (deterministic garbage from the wrong one). Polarity is now scored by
  stop-bit validity (the line must idle mark after each character):
  correct polarity scores ~1.0, inverted ~0.65, decisive. The +140 Hz
  heavy-straddler fixture is upgraded from classify-only to a full
  verbatim-decode regression.
- **Keychain secrets** (#42): the Discord token now lives in the macOS
  Keychain instead of UserDefaults — it previously rode the settings
  mirror into a plaintext, hand-editable Settings.plist. Migration is
  automatic and sweeps every launch (a stale mirror import can
  reintroduce the defaults copy). The LoTW fetch gains an opt-in
  "Remember password (Keychain)" checkbox — off by default, one-shot
  behavior unchanged — plus username prefill (saved login, else the
  station callsign). Unsigned Debug builds may show one Keychain
  prompt per rebuild for existing items (identity changes); signed
  releases (#43) won't.
- **Post your own spots** (#42): a spot composer in the DX Cluster
  window sends "DX <kHz> <call> <comment>" at the VFO A frequency.
  One node is enough (the cluster network propagates it), so posting
  walks the enabled nodes in config order and stops at the first
  success; receive-only RBN feeds are skipped. The command formatter
  rejects non-callsigns, flattens newlines (no smuggled second telnet
  command), and caps the comment — all regression-pinned.

## [9.31] — 2026-07-20

**Second full bug sweep** (four parallel reviews over everything shipped
since 8.11; every finding verified before fixing — 24 fixes):

The big ones:

- **cty.dat parsing collapsed to ONE entity at runtime**: Swift's
  grapheme clustering makes "\r\n" a single Character, so splitting a
  CRLF file on "\n" never split at all — the authoritative country
  mapping silently fell back to the approximate tables since 9.10.
  Line endings normalized; the real bundled snapshot is now test-pinned
  (300+ entities).
- **LoTW report parser crashed on malformed ADIF** (negative length
  field built an inverted range — reproduced, fixed, regression-pinned)
  and **TQSL uploads could deadlock forever** on a chatty run (pipes
  never drained → 64 KB buffer → TQSL blocks → "Uploading…" for
  eternity). Both pipes now drain continuously.
- **The arcade resync guard ate every busy FT8 slot**: ft8Spots
  republishes wholesale with fresh UUIDs each slot, so >12 "new" spots
  is a NORMAL band, not a resync — fireworks/combo/SPOTTER never fired
  on active bands. Guard now keys on an empty known-set only.
- **Off-center RTTY misclassified as CW**: the probe's 0.4·peak
  envelope gate dropped frames of the prototype-skirt-attenuated far
  tone; gate lowered to 0.15 + decaying peak reference (one static
  crash no longer poisons the verdict) + a confidence-driven re-probe
  escape hatch (≤ once/10 s) + polarity-flip hysteresis on the text.
  Off-grid RTTY regression-pinned (+100 Hz decodes verbatim; +140 Hz
  classifies; single-bin decode past the alias edge stays future work).
- **Cluster reconnect churn**: a failure fired BOTH the receive-error
  and state-failed paths, doubling reconnects that then cancelled each
  other's fresh connections in an endless login loop. Connection
  generations now orphan stale callbacks.
- **QSO log durability**: atomic writes (a crash mid-write could
  silently destroy the whole logbook), no rewrite-on-load, batched
  confirmation flips (was O(k·n) encodes + k disk writes on main).

Also: LoTW passwords with "+" now encode correctly; ADIF export forces
en_US_POSIX/Gregorian (Buddhist-calendar systems exported year 2569);
mode-guess uses whole tokens ("5 EL BEAM" no longer tunes AM); bare
"CONGO" rarity match no longer flames common 9Q calls; the ticker's
spawn timer survives parent re-renders (it could starve entirely on
busy bands), its backdrop no longer swallows waterfall clicks, crawler
clicks outlive spot expiry, and the RBN preset pair is addable
separately; node colors keyed host:port + stable across deletes;
worked/confirmed badges use O(1) sets (was ~10⁶ string compares/s
worst-case); stale post-limiter scope/IMD cleared on disarm; ghost
decay tied to ingested rows (ran 2–4× fast, refresh-dependent); WWV
line clears when all clusters stop; skimmer empty-state and probing
labels updated.

## [9.30] — 2026-07-20

**OmniSkimmer speaks RTTY (issue #15, phase 3 opens):**

- Every fresh candidate is now probed for ~1.5 s and classified: on/off
  keying → CW, continuous carrier with a two-cluster frequency split of
  ~110–260 Hz → RTTY. Verdicts are committed per candidate; the CW
  decoder runs provisionally during the probe so no text is lost.
- **RTTY decode on the subchannels**: a per-candidate frequency
  discriminator (8.25 frames/bit at 45.45 Bd on the 375 Hz frames)
  drives the existing BaudotUART — with BOTH mark/space polarities
  decoded in parallel and the higher printable ratio owning the text,
  so sideband/polarity conventions sort themselves out.
- Panel rows wear a mode chip (CW green / RTTY purple / ? while
  probing); RTTY waterfall labels go violet.
- Acceptance test: three synthesized Baudot FSK carriers through the
  real channelizer+tracker classify RTTY and decode "RYRY DE HERMIT"
  verbatim at >0.8 confidence, while keyed CW neighbors stay CW; the
  25-CW-signal test still passes untouched.

## [9.20] — 2026-07-20

**The logbook grows up (issue #42, continued):**

- **QSO Log window** (Tools ▸ QSO Log): the full searchable logbook —
  filter by call/band/mode, per-band counts, entity names from cty.dat,
  confirmation ticks, per-row delete, ADIF export.
- **LOG IT in the TX console**: a quick-entry field right under PTT —
  type the call as the over ends, hit return, done (current VFO
  frequency, mode, UTC). Confirms with a green tick.
- **"New ones" spot filter**: hide every call already in your log —
  combined with the rarity flames, LoTW ✓, and worked ⭑ badges, the
  spot stream now ranks itself by what YOU still need.

## [9.10] — 2026-07-20

**Authoritative DXCC mapping (issue #48):** callsign→entity now comes
from the AD1C country file (cty.dat — the same database every major
logger uses), with a snapshot bundled in the app and a weekly-refreshed
cache from country-files.com. Full exception lists mean the ticker's
country names are now CORRECT (VP8STI resolves to South Sandwich, not
Falklands), and the rarity flames gained an entity-NAME bridge — the
prefix-ambiguous most-wanted entities the 8.80 table deliberately
omitted (South Sandwich, Malpelo, Mount Athos, Swains, Glorioso,
Tromelin…) now burn when the authoritative file identifies them. The
built-in approximate tables remain as offline fallback; parser,
exact-call precedence, portable forms, and the rarity bridge are
fixture-pinned (CountryFileTests). Live Clublog most-wanted stays open
on #48 (needs an API key).

## [9.00] — 2026-07-20

**The operator release** (milestone: HermitSDR becomes a station tool,
not just a receiver — issues #40 + the #42 MVP):

TX instrumentation (#40, closing it):

- **Post-limiter scope overlay**: a crisp cyan edge line on the phosphor
  mod scope showing what ACTUALLY modulates — the gap under the
  pre-limiter fill is the limiter/CESSB's work, finally visible.
- **Two-tone IMD3 analyzer**: continuously watches the post-limiter
  audio and, when the output is a credible tone pair (feed a two-tone
  file through the TX file player), measures IMD3 by FFT and grades it
  in the TX Meters footer — CLEAN ≥30 dB, OK ≥24, DIRTY below.
  Self-qualifying: voice/noise never gets mis-graded (refusal pinned by
  test, measurement pinned within ±2 dB against injected products).
  Architecture honesty: the 2-TONE button's RF pair is synthesized
  clean and bypasses the audio chain, so this grades the CHAIN;
  PA/RF IMD stays a dummy-load-with-outside-receiver job (#13).

QSO log (the #42 MVP):

- **In-app logbook**: "Log @ VFO" in the LoTW window records call +
  frequency + mode + UTC now; JSON in Application Support; last five
  shown with confirmation ticks.
- **ADIF export** (3.1.4: USB/LSB→SSB, SAM→AM, UTC fields, band
  tokens — test-pinned) ready for TQSL's sign-and-upload.
- **Worked-before badges**: spots now wear ⭑ when the call is in your
  log (cyan) or LoTW-confirmed (green) — alongside 8.50's "will
  confirm" ✓.
- **LoTW confirmation matching**: fetch your QSL report (credentials
  used once, never stored, cleared after the request) and matching log
  entries flip to confirmed; the report parser and call|band|mode match
  keys are test-pinned.

## [8.90] — 2026-07-20

**DX cluster follow-ups (issue #41, closing out):**

- **Spot filters**: band picker, "LoTW only" (needs the badge list),
  and "Humans only" (hide skimmer spots — tame the RBN firehose).
  Filters apply everywhere at once: the window rows, the waterfall
  labels, and the ticker.
- **Per-node colors**: each configured cluster gets a stable color —
  a dot on its config row, the "de spotter" text, and a ring around
  its waterfall labels, so multi-cluster spots are tellable apart at
  a glance.
- **Solar line**: WWV/WCY propagation broadcasts relayed by clusters
  now show in the window footer (SFI / A / K at a glance) instead of
  being dropped.

## [8.80] — 2026-07-20

**Rarity flames** 🔥: ticker crawlers from most-wanted DXCC entities now
burn. A built-in Clublog-derived top-50 table (distinctive prefixes
only — ambiguous ones like VP8 are deliberately omitted so a common
Falklands call never wears an undeserved flame; longest-prefix match,
test-pinned) maps rank → flame intensity: 2–5 flickering tongues,
growing height and vigor toward rank 1, ember bubbles shedding off the
top half of the table, and a bonfire for P5. Rare calls also go gold
with an orange glow and name the entity in their tooltip; the ticker
strip grew to 13 % of the waterfall (was 10) for flame headroom.

## [8.70] — 2026-07-20

**The deluxe eye-candy batch (issue #44) + ticker tuning:**

- **Glowing glyph readout**: the VFO frequency renders in-scene from a
  runtime-built digit atlas, just right of the VFO line — the numerals
  feed the bloom/halo chain like every other light source, and breathe
  with the audio. Flips sides when it would clip.
- **3D depth of field**: in 3D mode the far ridge and horizon melt into
  a blurred copy of the scene while the near rows stay razor sharp;
  eases in and out with the mode toggle.
- **Long-exposure ghost trace**: a minutes-scale max-hold (a ~20 dB
  carrier lingers ~7 minutes) drawn as a dim violet memory behind the
  live and peak traces — where signals WERE. Clears on retune like the
  peak trace.
- **Koi, evolved**: each swim wears its own color morph (gold through
  calico and dusk reds), and mid-crossing the koi now JUMPS — the
  water-warp fades while it's airborne and a splash ring warps the
  surface where it lands.
- **Degauss**: switching palettes rings the tube — a horizontal wobble
  and an RGB purity ripple that settle over ~0.8 s, exactly like
  slapping the side of a 1984 Trinitron.
- **Ticker tuning** (user feedback): crawlers cross in 26–36 s (was
  12–19), spawn 4.5 s apart (was 2.4), carry generous hit targets, and
  clicking one now sets band, frequency, AND mode — the mode guessed
  from the spot comment (FT8/CW/SSB tokens) or band-plan heuristics
  (CW segments, LSB below 10 MHz, USB above), test-pinned.

## [8.61] — 2026-07-20

- Documentation sweep: the README's decade-long intro paragraph is now
  a readable era-by-era story; Highlights, Using, Architecture, and the
  Roadmap catch up with everything through 8.60 (the old roadmap still
  listed the TX antenna picker, EDR, and "a CW skimmer someday" — all
  long since shipped). Capability table gains OmniSkimmer and Spotting
  rows. Outstanding to-dos filed as issues #39–#44.

## [8.60] — 2026-07-20

**DX cluster grows up (and puts on a show):**

- **Multiple clusters at once**: the DX Cluster window manages a list of
  connections — each with its own enable switch, status line, and
  optional login override (empty = station callsign; SSIDs like WU1T-2
  let one call hold several sessions). Add from presets or custom;
  spots from all nodes merge into one deduped stream, each tagged with
  the node it came from (hover any spot). 8.50's single-cluster
  settings migrate automatically.
- **Times Square ticker** (toggle in the DX Cluster window, default
  on): spots crawl across the bottom of the waterfall, left to right,
  capped at 10 % of the waterfall's height — BAND chip (colored by
  band) · CALLSIGN (per-spot font family, size, and hue) · COUNTRY.
  Five deterministic motion personalities: bob, wobble, pulse, a
  mid-flight barrel roll, and the full showboat combo. Click a crawler
  to tune to it. Band + DXCC-prefix country mapping are pure and
  test-pinned (~200-prefix built-in table).
- **RX/TX antenna chips** (header, ANAN only): which jacks are live is
  now unmissable — a green RX chip and an orange TX chip (red while
  keyed, glowing when armed) sit beside the clock, and each doubles as
  a quick-switch menu.
- **Consistent window chrome**: every auxiliary window (DX Cluster, TX
  Meters, decoders, multimeter, …) now wears the main window's dark
  navy and dark controls instead of the system's light-gray chrome
  (user report: mismatched grey-brown backgrounds).

## [8.50] — 2026-07-20

**Two new integrations + the road to signed builds:**

- **DX cluster spotting** (`Integration/DXCluster/`, Integrations ▸ DX
  Cluster): telnet client for DX Spider/AR-Cluster/CC-Cluster nodes
  (and the RBN skimmer feeds) — logs in with your station callsign,
  parses spot lines (parser is pure + test-pinned across the dialects,
  junk rejected), reconnects with capped backoff. Spots appear as
  magenta labels on the waterfall at their frequency (in-span only,
  fading with age, click to tune VFO A) and as live rows in the window
  (time/freq/call/comment/spotter, skimmer spotters tinted). Presets
  for VE7CC, NC7J, W3LPL, and both RBN feeds; per-call dedupe, 300-spot
  cap, 15-minute expiry, persisted host/port/enable.
- **LoTW support** (`Integration/LoTW/`, Integrations ▸ LoTW):
  - *Badges*: opt-in download of ARRL's public LoTW user-activity list
    (cached in Application Support, weekly refresh) — spotted calls
    that upload to LoTW get a green ✓ ("it'll confirm"), portable
    prefixes/suffixes handled. No account needed.
  - *Sign & upload*: pick any ADIF log (WSJT-X's wsjtx_log.adi, the
    FT8 panel export) and it's signed with your callsign certificate
    and uploaded via TrustedQSL's CLI (`tqsl -d -u -a compliant`);
    duplicate-only uploads reported as such. Requires TQSL + a cert;
    the window says so when they're missing. Credentials never touch
    this app.
- **Signed distribution scaffold** (`tools/release.sh`): Release build
  → Developer ID signing with hardened runtime → notarytool submit →
  staple → Gatekeeper-verified zip in `build/`. Two one-time manual
  steps (create the Developer ID certificate in Xcode; store a notary
  keychain profile) are documented in the script header.

## [8.41] — 2026-07-20

- Discovery: the ANAN's link-local fallback address (169.254.76.129) is
  now in the default unicast probe list — when the router ignores its
  DHCP requests (the known lease failure) the radio is found on the
  first probe burst instead of relying on broadcast reach. Diagnosed
  live: a wedged boot (PHY answering ARP, discovery engine silent)
  needed a power cycle; the lease failure then recurred as usual.

## [8.40] — 2026-07-20

**TX Meters, the eye-candy-that-works edition** — the window's zones,
scales, and coach logic are unchanged from the hardware-validated 3.70
originals; the presentation is rebuilt in the app's GPU family look:

- **GPU phosphor modulation scope** (`Rendering/TXScopeRenderer.swift`,
  `txscope_fragment`): the pre-limiter envelope renders as a mirrored
  phosphor trace — dark core at the midline, glowing edge, bin-smooth
  interpolation, half-second time ticks riding the scroll, the target
  zone washed onto the glass. The limiter ceiling is a pulsing amber
  line that RAGES when the flat-top lamp latches, and every peak shaved
  above it burns as a red slab (brighter than SDR white on EDR panels).
  The face dims when TX is disarmed.
- **LED-segment meters**: all seven bars (mic/speech/comp/limiter/ALC/
  PWR/SWR) are now 36-segment LED ladders with zone-colored unlit ghost
  scales, tube shading, and a falling amber peak-hold tick (1.2 s hold)
  — read your syllable peaks without staring. PWR moved to the
  wattmeter √ (voltage-linear) scale, matching the multimeter.
- **Warning jewels**: the MIC CLIP / FLAT TOP / OVERDRIVE / UNDERRUN
  lamps are glass indicator jewels with a specular sparkle and a
  colored glow when lit; labels glow with them.
- **LCD telemetry chips**: TEMP / PA / FWD / REV readouts in the
  multimeter's green-on-black LCD style. Coach text now glows its
  verdict color.

## [8.31] — 2026-07-19

**Lightning-watch false alarm fix** (user report: the "heavy static
crashes" chip stuck on permanently):

- The detector was counting ordinary band activity as weather — CW
  key-downs and voice plosives exceed the noise blanker's 5× blanking
  gate on full-span IQ, so the "crash rate" never fell below the clear
  threshold on any active band. Detection is now storm-specific: a
  fixed 10× threshold (independent of the user's blanker setting) with
  a 20 ms hold-off so one crash counts once, not once per ring of the
  envelope.
- Watch thresholds recalibrated to deduped crashes/s: warn at a
  sustained 4/s, clear after 2 consecutive minutes under 1/s.
- The chip is now click-to-dismiss (✕) — dismissing snoozes the watch
  for 30 minutes. The sprite layer stays click-through; only the chip
  takes the tap.

## [8.30] — 2026-07-19

**Second fruit basket:**

- **Trophy Case** (Tools ▸ Trophy Case): every achievement on one dark
  shelf — earned in gold, locked with a padlock and its how-to-earn
  hint, plus a running count. Reads the persisted trophies from 8.20.
- **Skimmer acquisition sparks**: every newly tracked OmniSkimmer
  candidate now fires the same expanding decode spark on the waterfall
  that FT8/CW decodes get — acquisitions glitter as the skimmer finds
  carriers.

## [8.20] — 2026-07-19

**Low-hanging fruit batch** (small comforts, autonomously gathered):

- **Privacy toggle**: the anonymous daily usage ping (install ID + app/
  macOS version, nothing else) now has a visible switch — Settings ▸
  Privacy. It was previously opt-out only via a hidden defaults key.
- **Kp chip**: the header now shows the live planetary K-index next to
  the UTC clock — green when quiet, orange at Kp 4, red in a storm —
  with a propagation-odds tooltip. Same hourly NOAA number that drives
  the 3D sky's aurora.
- **Multimeter drag pointer**: a passive orange peak-hold pointer rides
  up with the needle, holds 2 s, then drifts back — like the lazy
  pointer on a bench meter. Resets when the function knob turns.
- **Achievements persist**: trophies are earned once, ever — the toast
  no longer repeats every session (`arcadeAchievements` defaults key).
- CLAUDE.md refreshed (issue list current, 7.90–8.20 map for future
  sessions).

## [8.11] — 2026-07-19

**Full-codebase bug sweep** (five parallel reviews over rendering,
OmniSkimmer, the new UI layer, recent DSP changes, and app state; every
finding re-verified against the source before fixing — 18 fixes):

Crash/UB class:
- OmniSkimmer's Metal staging loop read up to N−1 elements past the end
  of its input arrays on nearly every batch (masked only because the
  stdlib compiles the bounds check out and the kernel never touched the
  tail). Staging count now exact.
- `pngData`'s CGContext kept `&raw` past the initializer call —
  formally dangling by `makeImage()`. The whole use now sits inside
  `withUnsafeMutableBytes`.

Correctness:
- **File replay no longer feeds OmniSkimmer**: the tee ran on replayed
  IQ under the previous session's center/rate, producing confident CW
  spots at garbage frequencies that click-to-tune would chase. Live
  radio IQ only, per the issue #15 contract.
- Skimmer spots/stats and the lightning watch now clear on disconnect
  (both froze stale — the panel showed a dead session's spots as live,
  and a tripped warning could persist through hours of idle).
- Lightning watch hysteresis: quiet seconds must now be CONSECUTIVE
  (they accumulated across noisy interludes, clearing mid-storm), and
  sustained legitimate high crash rates are clamped instead of dropped
  (the wrap guard silently muted the watch during the most violent
  storms — its strongest-signal case).
- Tracker: `reset()` clears the ignore list (channel-keyed ignores
  survived retunes and suppressed innocent frequencies); ignore now
  covers ±1 channel (exact-match ignores respawned the spot within
  seconds); drift/acquisition can no longer treat the ±fs/2 wrap seam
  as frequency-adjacent.
- `onUpdate` closure read moved onto the main queue (unsynchronized
  cross-thread read raced RadioState's wiring at launch).
- `writeIndex` now advances under `rowLock` (readers locked, the writer
  didn't — latent race for any off-main `addSpark` caller).
- Decode-spark pruning wraps ring distance like the render path —
  seam-adjacent sparks were killed after 1 s while still visible.
- Waterfall PNG capture times out with nil after 3 s instead of hanging
  its caller forever when the window is occluded/minimized (paused MTK
  view never drains the queue).
- Persistent GPU failure no longer grows the channelizer's input
  buffers without bound (~12 MB/s) — the backlog drops, history stays.
- WEFAX slant/phase re-render caps at the CAPTURED profile's line
  budget (switching the picker to a slower profile after a long chart
  silently truncated the corrected image). Pre-existing since 4.50.
- NoiseBlanker `reset()` clears the impulse edge state (one-event
  undercount per TX unkey).

Arcade polish:
- The balloon is no longer culled 7 s before its fade (it vanished
  abruptly near the top; the fade-out was unreachable).
- Combo meter: ID-cap resets and arcade re-enables no longer re-count
  every displayed spot as a fresh decode (phantom ×50 surges, spurious
  ON FIRE and shatters). Resync bursts are absorbed silently.
- The 4:20 leaf dedupe key includes the day — multi-day sessions only
  fired on day one.
- Periscope: dropped a no-op `.clipped()`; it now emerges from below
  the window edge properly.

Also reviewed clean: every Swift↔MSL struct layout and buffer index,
the CESSB scratch refactor (proven identical to the pre-refactor
output), PrefixMeanTable semantics, capture-buffer lifecycles, the Kp
fetch, persistence-key invariants, and passband-aura math.

## [8.10] — 2026-07-19

**The instrument release:**

- **Analog multimeter** (Tools ▸ Analog Multimeter, ⌘⇧M): a
  finely-detailed taut-band needle meter in its own window — "HERMIT
  ELECTRIC CO. MODEL 800". Canvas-drawn face: colored zone arcs, an
  anti-parallax mirror band, minor/major ticks with serif labels, a
  spring-physics needle (real ballistics with a bounce off the end
  pegs), counterweight, jeweled hub, corner screws, glass highlight
  sweep, warm lamp glow, and a green LCD sub-readout. Six functions on
  a click-to-rotate knob: SIG (dBm/S-units), PWR (voltage-linear watts
  scale, full-scale from `maxExpectedWatts`), SWR (classic compressed
  scale), PA amps, forward bridge volts, PA temperature. Functions with
  no live source park the needle and dim the LCD.
- **Tools menu** (new top menu): the multimeter plus one-stop access to
  Bandscope, Decoder Activity, Stations Heard, TX Meters, and the TX
  Audio Chain windows.

## [8.00] — 2026-07-19

**The full arcade** (milestone: the gamification generation, complete):

- **Koi in the waterfall** (GPU): every few minutes a golden koi swims
  clear across the waterfall — the water (the sample coordinates)
  bulges around its body and warps back behind it, tail wiggling, all
  in the fragment shader. Flat view, Arcade FX gated.
- **Live aurora** (real space weather): the 3D sky's aurora strength
  now follows the actual planetary K-index (NOAA SWPC, fetched
  hourly, silent when offline). Quiet sun = faint curtains; Kp 5+
  storm = the sky rages — and a third crimson curtain unfurls —
  exactly when the bands die.
- **Prefix fireworks**: the first time a callsign prefix is heard this
  session (FT8/FT4 spots), a firework bursts at its waterfall
  frequency.
- **Combo meter**: decode events (new FT8 spots + new skimmer
  candidates) in a rolling 45 s window build a "×N COMBO" badge that
  pulses hotter as it climbs; letting it lapse shatters it into
  star fragments.
- **Achievement toasts** (once per session, gold-bordered, 🏆):
  SPOTTER, BIG GUN (S9+40), RAGCHEW RADAR (10 CW at once), ON FIRE
  (combo ×10), STORM RIDER (lightning watch cleared), BULGER
  MULTIPLICATION COMPLETE.
- **Skimmer health bars**: every waterfall label wears an RPG hit-point
  bar — full green at 40 dB SNR, red sliver when barely alive.
- **The critter parade**: the crab now has friends — a periscope that
  rises from the deep, scans with a glinting lens, and sinks; a
  four-duck convoy paddling the bottom edge; a little yellow submarine
  blowing bubbles. One critter every 5–12 minutes; the crab keeps its
  own never-twice-in-10-minutes rule.
- **4:20 leaf** 🍁: at 04:20 UTC — and at 4:20 am/pm local — a leaf
  flutters down from the top of the window, lands mid-waterfall, and
  goes up in flames and smoke.
- **Realism pass** (user feedback): the lightning airplane is now a
  proper little banner tug — high wing, tailplane, prop-disc blur,
  sagging tow rope, fluttering banner — at a believable ~22 s
  crossing (was 9 s); the Ukraine balloon grew a gored envelope,
  suspension lines, a woven wicker basket, an occasional burner
  flick, and a pendulum sway.

## [7.90] — 2026-07-19

**The arcade release** (sprites, a liquid seam, and a real safety
feature wearing a costume):

- **Liquid boundary** (GPU): the hard seam between the spectrum trace
  and the waterfall is now a glowing ribbon that undulates with two
  drifting waves, swells over strong signals (the vertex shader samples
  the live trace), breathes with the audio, and feeds the bloom chain.
  Flat view only; always on.
- **Arcade sprite layer** (`Views/ArcadeOverlay.swift`, master toggle
  "Arcade FX" in the palette menu, persisted, default on):
  - **S-meter floaters**: signals at S9+10 or better launch their
    reading ("S9+23") from the boundary at the VFO — it rises, wobbles,
    and pops. At most one per 4 s.
  - **Ukraine balloon** 🎈: a blue-over-yellow hot-air balloon drifts
    up through the whole display every 2–5 minutes, swaying.
  - **VOTE FOR DEMOCRACY**: sneaks into the spectrum region every few
    minutes, every letter dancing to its own beat in cycling hues,
    then fades away.
  - **The crab**: at most once every 10 minutes, two eye stalks peek
    over the boundary from a side edge, look down into the waterfall,
    blink twice, a claw sneaks up — then the whole crab pops.
  - **TX banner jiggle**: ACTIVATE TX CONTROLS periodically shimmies
    and cycles through brief hue-rotated psychedelia before composing
    itself. Never while armed or keyed.
- **Lightning watch** (NOT gated by Arcade FX — it's advisory safety):
  the noise blanker's impulse detector now runs even when blanking is
  off and counts broadband crash EVENTS; a sustained crash rate trips
  `lightningWarning` — a pulsing red chip appears, and once a minute an
  airplane flies across the waterfall towing "⚡ LIGHTNING STATIC
  RISING — CONSIDER DISCONNECTING ANTENNA". Heuristic (severe local
  QRN can trip it), self-clears after ~3 quiet minutes.

## [7.80] — 2026-07-19

**OmniSkimmer** (issue #15, phases 1 + 2): the GPU now does DSP, not
just pixels — a Metal polyphase filter-bank channelizer splits the
entire sampled span into ~375 Hz complex subchannels and a full-span CW
skimmer decodes every carrier at once.

- **Metal channelizer** (`DSP/OmniSkimmer/`): polyphase fold kernel +
  batched Stockham radix-2 FFT (one dispatch per stage, ping-pong) +
  per-channel metrics kernel (mean/peak power, fine-frequency offset
  from phase progression). 128 channels at 48 k up to 4096 at 1536 k,
  Blackman-Harris prototype, nothing baked into the shaders — rate/
  channels/taps flow from `ChannelizerConfig`. MSL compiled at runtime,
  so `swift test` instantiates the real GPU path and pins it against
  the CPU reference. CPU polyphase fallback when Metal is unavailable.
- **Secondary-pipeline contract honored**: the radio thread only
  appends to a bounded ring (overflow drops skimmer blocks and counts
  them — live RX/audio are untouchable); all GPU work runs on a
  dedicated coordinator queue; the skimmer always analyses the LIVE
  stream, never time-shifted replay; NCO retune / rate change / restart
  clear FIR history and candidates.
- **CW skimmer**: per-channel candidate tracker (attack hysteresis,
  hang time, drift-follow gated on mean SNR so key-up gaps can't
  random-walk a candidate off its carrier, boundary merge, temporary
  ignore) feeding one envelope-domain CW decoder per signal — adaptive
  keying threshold, self-correcting dit estimate (two agreeing short
  marks re-seed after a dah-first acquisition), WPM and confidence per
  signal, morse table shared with the CW mode decoder.
- **UI**: SKIM toggle in the decoder row (master switch, default off,
  persisted `omniOn`); OmniSkimmer panel — live rows (freq/text/SNR/
  WPM) sortable by SNR or frequency, click = tune VFO A, context menu
  ignore-for-10-min, diagnostics footer (channels × bin width, GPU
  ms/batch, active count, drops); green waterfall labels at each
  skimmed frequency, FT8-overlay conventions, click to tune.
- **Tests** (11 new): tone→channel mapping, IQ orientation pinned
  against SpectrumAnalyzer's display convention, fine-offset sign/
  magnitude, adjacent-tone separability, strong-carrier leakage bound,
  bit-continuity across arbitrary block boundaries, reset semantics,
  frequency mapping across all six rates, GPU-vs-CPU agreement, and
  the phase-2 acceptance test: 25 simultaneous shaped-keying CW
  signals across the span, all tracked exactly once, ≥20 decoding
  "CQ TEST" verbatim.

Not yet: on-air validation (labels against real band activity, click-
to-tune accuracy live, backlog behavior at 1536 k with the radio
connected), RTTY/FSK/other phase-3 detector plug-ins, and time-machine
integration for candidates.

## [7.70] — 2026-07-19

**The Mario Kart release** (eye candy, fifth helping — gamified):

- **3D brightness overhaul** (user report: "pretty dark no matter what
  I do with Floor and Ref"): ambient floor lifted (shade now bottoms at
  0.70 instead of 0.40), hot ridges are emissive (+0.55·t self-glow),
  fog is thinner (density 1.8 → 1.25) and capped at 90 % so far ridges
  keep a shimmer of color, the reflection is less dimmed, and the glass
  floor + grid are brighter.
- **Rainbow rim sheen**: 3D ridge crests catch an iridescent
  grazing-angle rim light whose hue cycles across the span and drifts
  with time — pure Rainbow Road.
- **Carrier sparkles**: the beacon tracker now sheds coin-glint star
  sprites — 4-point flares that rise off strong signals through the
  spectrum region, twinkling gold (with the occasional icy one) before
  burning out. Spawn rate follows carrier strength; capped at 96.
- **Drift streak**: spin the dial fast and a cyan whoosh trails the VFO,
  sharpening toward the marker and fading ~half a second after you
  stop — the VFO shaft also flares while you're moving.
- **Passband aura**: the reception window glows gold with shimmering
  edges (GPU, additive under the SwiftUI overlay), bright in the
  spectrum region and fading down the waterfall.
- **S-meter boost flames**: past S9 the bar tip catches fire —
  flickering flame tongues lick ahead of the comet head, hotter the
  further over nine you go.

## [7.60] — 2026-07-19

**The shenanigans release** (eye candy, fourth helping — all GPU):

- **CRT Glass mode** (palette menu, persisted): gentle barrel
  distortion, scanlines, an RGB aperture-grille mask, animated film
  grain, a slow rolling brightness band, and heavier corner shading —
  all in the composite pass, eased in over ~0.3 s when toggled. Pairs
  outrageously well with the Phosphor and Amber CRT palettes.
- **Dreamy halos**: a second, much wider Gaussian (σ20) of the same
  bright-pass now composites under the tight bloom — hot carriers and
  the trace get big soft halos instead of just a rim glow.
- **3D starfield + aurora backdrop**: in 3D mode the flat clear color
  is replaced by a procedural night sky — two slowly weaving aurora
  curtains and twinkling hash-grid stars; the horizon matches the
  terrain fog so the far ridge dissolves into it.
- **VFO light shaft**: a soft crimson glow column under the VFO marker,
  drawn in the scene pass so the bloom/halo chain picks it up (main
  panadapter only).
- **Audio-reactive glow**: the final speaker mix's RMS envelope (fast
  attack, ~0.3 s release, self-zeroing when audio stops) breathes the
  bloom (+35 %), the halos (+60 %), the phosphor trace deposit, and the
  VFO shaft — the display pulses with what you hear.

## [7.50] — 2026-07-19

**The #37 closeout + a fourth helping of eye candy:**

Performance (the issue #37 rump — the backlog is now fully shipped):

- **SSTV/WEFAX re-render is O(1) per pixel**: the slant/phase slider
  paths now build one prefix-sum table per re-render (`PrefixMeanTable`)
  instead of running an O(window) scalar mean per pixel — a 1200-line
  WEFAX chart no longer re-sums the whole capture once per pixel column
  while you drag. Equivalence with the old scalar mean is test-pinned
  (clamping, fallback, and numerics at gray-level precision).
- **`framebufferOnly = true` restored**: PNG capture re-renders the
  composite pass into an owned texture instead of blitting the drawable
  — the compositor gets the fastest presentation path back, and the
  capture can never tear against presentation again.
- **CESSB allocation-free**: the analytic filter's padded inputs, four
  convolution outputs, and carried tails now live in persistent scratch
  (two fresh-array rounds per TX block gone); vDSP calls unchanged, so
  the output is bit-identical and the pinned envelope/containment tests
  agree.

Waterfall palettes (more colors, and *moving* colors):

- **Turbo** and **Spectral**: two new static multi-hue colormaps — the
  full blue→cyan→green→yellow→red sweep for maximum signal contrast.
- **Prism ✦** and **Nebula ✦**: the first *dynamic* palettes, computed
  procedurally in the shader from wall time. Prism lays the entire hue
  wheel across the dB range and drifts it one lap per minute; Nebula
  slowly rotates while its hue span breathes between moody two-tone and
  full rainbow over 90 s. Both keep a near-black noise floor and
  white-hot carriers, crossfade cleanly with every other palette, and
  color the 3D terrain too. (Uniforms grew `paletteMode`/`timeSec`.)

- **GPU S-meter**: the header meter is now a Metal shader — 57 LED
  segments (2 dB each) with rounded-bar shading, analog ballistics
  (35 ms attack / 300 ms damped decay between the 10 Hz meter ticks),
  a phosphor ember trail behind falling signals, a 1.2 s peak-hold
  marker, a hot comet-head glow at the bar tip (brighter than SDR white
  on EDR panels), etched S-unit ticks, and an S9 notch. Readout text
  stays SwiftUI on top. Same -127…-13 dBm scale and calibration.

## [7.40] — 2026-07-19

**The indulgence release** (eye candy, third helping):

- **Glass-floor reflections in 3D**: the terrain is drawn mirrored
  beneath a translucent gridded floor plane — depth-tested, fogged, and
  dimmed under the glass. Three mesh passes, still trivial GPU load.
- **Draggable 3D camera**: drag on the waterfall region (in 3D mode)
  orbits the camera — azimuth ±66°, elevation 5°–72°; double-click
  resets and resumes the automatic drift. The spectrum-trace region
  keeps its click/drag tuning, and ⌥-scrub still wins.
- **Carrier beacons**: the strongest live-trace peaks (chunk-max scan,
  12 dB over the median, EMA-tracked) get warm pulsing glows that ride
  the trace and follow carriers as they drift. Up to 8, self-managing.
- **Sparks ride the history**: decode rings are now pinned to the row
  they decoded — they scroll into the past with the waterfall and fade
  out as they ride down, instead of hovering at the top.

## [7.30] — 2026-07-19

**Eye candy, second helping** (all GPU, all in the existing post chain):

- **True EDR/HDR output**: the drawable went rgba16Float in extended
  sRGB with `wantsExtendedDynamicRangeContent` — on XDR panels, bloom
  and hot carriers render *brighter than SDR white* (headroom queried
  per frame, capped ×3; SDR panels clamp exactly as before). PNG
  capture handles the float drawable (tone-clamped to SDR).
- **Decode sparks**: every FT8/FT4 spot and CW/RTTY/SSTV decoder
  bookmark fires an expanding glow ring on the waterfall at the decoded
  frequency (additive, ~1.4 s life, 64 live max). The display shows the
  band being *worked*, not just heard.
- **Colormap crossfade**: switching palettes morphs the whole display
  (2D, 3D, all views) over 0.4 s instead of snapping.
- **3D waterfall, phase 2**: slow ±11° orbital camera drift (~63 s
  period), per-vertex diffuse + specular lighting from central-
  difference normals, and a faint graticule on the low terrain.
- **Composite polish**: gentle vignette, and chromatic aberration
  applied to the bloom halo only — the scene underneath stays sharp.

## [7.20] — 2026-07-19

**The waterfall generation**: resolution, smoothness, and a GPU post
chain — plus region availability policy and a Discord snapshot command.

- **Region availability** (`App/RegionGate.swift`): the app declines to
  run in the Russian Federation (system region or a Russian timezone)
  while Russia's war against Ukraine continues. Deliberately offline —
  reads local settings only, nothing phones home; trivially bypassed by
  changing the locale, and that's accepted: it's a statement, not DRM.
- **Discord /waterfall**: new slash command snapshots the panadapter and
  posts the PNG to the configured text channel (reuses the existing
  capture + multipart-upload path).
- **3D waterfall** (palette menu): the history ring rendered as a
  perspective heightfield — depth-tested ridges, distance fog, same
  zoom/pan window and colormap. Main panadapter only, not persisted.
- **Long-history waterfall**: the main ring grew 2048 → 16384 rows
  (~9 min at 30 rows/s, 256 MB) with a History ×2/×4/×8 compression
  picker; compressed rows peak-preserve in time so brief transmissions
  survive. The full-ring wipe is now a clear-only render pass (the old
  cold-buffer blit would have needed 512 MB).
- **Blue-noise dither** on the colormap lookup kills gradient banding on
  the dark schemes (Abyss/Glacier) for one `fract()` per pixel.

- **GPU eye candy: phosphor persistence, bloom, springy zoom.** The
  panadapter now renders geometry into an offscreen HDR scene (4× MSAA,
  memoryless resolve) and composites through a post chain:
  - *Phosphor persistence*: the live trace deposits into a decaying
    accumulation buffer (τ ≈ 0.45 s), leaving analog-scope trails that
    make QSB and keying visible as texture. Cleared on retune (trails
    are frequency-indexed). dt-scaled so 120 Hz isn't brighter than 60.
  - *Bloom*: luminance bright-pass at half res + Gaussian blur,
    composited additively — strong carriers glow instead of clipping.
  - *Springy zoom*: zoom animates through the model (log-space
    exponential approach, ~0.2 s), so the shader, scale labels, VFO
    marker, and click-tune math stay in lockstep every tick.
  Whole chain measured at 0.49 ms/frame live. Applies to all
  panadapter-family views; the audio mini-waterfall (split 0) skips
  persistence.
- **Waterfall smoothness + resolution overhaul** (needs eyes-on-hardware
  validation for feel):
  - *Sub-row scroll interpolation*: the scroll position is now continuous
    in time (fractional `writeRow`, advanced by the EMA'd row period each
    frame), so the waterfall glides at display rate instead of stepping
    once per FFT row. Costs one row (~33 ms) of display latency.
  - *ProMotion*: the panadapter display link follows the screen's
    refresh rate (120 Hz on ProMotion) instead of a hardcoded 60; the
    sub-RX/audio/bandscope views keep their 30 fps caps (`fpsCap`).
  - *8192-point FFT* (was 2048): 46.9 Hz/bin at 384 kHz — zoomed-in
    signals stop smearing. History texture grows 8 → 32 MB per renderer.
  - *50 % FFT overlap* (adaptive hop, up to 87.5 % at narrow spans):
    doubles temporal coverage so CW dits/FT8 starts can't fall between
    FFTs, and holds ~30 rows/s at every sample rate. New DSP test pins
    tone placement, row rate, and the adaptive hop.
  - *Shader x-filtering*: minified spans peak-preserve across each
    pixel's footprint (narrow carriers stay solid lines — slight noise-
    floor brightening is expected, ~3 dB order-statistics bias); zoomed
    spans use Catmull-Rom instead of bilinear mush. 4× MSAA smooths the
    spectrum trace/peak lines (near-free on Apple-silicon TBDR).
- **About window artwork + contact info**: Help ▸ About now shows the
  HermitSDR hermit-crab artwork (`HermitSDR/Branding/HermitSDR-About-Art.png`,
  replacing the SVG wordmark), a live environment line (macOS version,
  architecture, radio connection state), and the author's contact email
  as a mailto link next to the copyright. Fixes a latent packaging bug:
  the old SVG lived in a top-level `Resources/` folder that was never
  part of the target, so clean builds silently fell back to the text
  wordmark — the artwork now lives inside the synchronized source group
  and is genuinely bundled.
- IQ recording extension renamed **`.sqiq` → `.hiq`** (the "sq" was
  SquareDeck-derived), finishing the 7.10 rename. No read-compat shim —
  no `.sqiq` recordings exist; the format itself (28-byte header + raw
  float pairs) is unchanged. Also removed a leftover
  `SquareDeck.xcodeproj` husk from the repo root.

## [7.10] — 2026-07-19

**The project is now HermitSDR** (formerly SquareDeck).

- Renamed everywhere that is alive: app/product/target/scheme, source
  tree (`HermitSDR/`), bundle id (**com.hermitsdr.app**), bridging
  header, entitlements, `HermitSDRDSP` package targets, UI strings,
  external-facing names (PSKReporter/ADIF program id, Discord
  user-agent, rigctl greeting), docs, tools. Historical changelog
  entries and git history keep the old name. GitHub repo renamed to
  `dzcassell/HermitSDR` (old URLs redirect).
- **One-time migration** (`App/LegacyMigration.swift`, runs before any
  settings read): copies the com.squaredeck.app defaults domain into
  the new one, moves `Application Support/SquareDeck` →
  `…/HermitSDR`, and `Documents/SquareDeck Recordings` →
  `Documents/HermitSDR Recordings`. No-op once migrated.
- The TCC permissions cannot follow a bundle id: macOS re-prompts once
  each for **Local Network** (on first connect), **Microphone** (on TX
  arm), and **Input Monitoring** (on tuning-device enable).

## [7.00] — 2026-07-19

**Tuning devices: user-remappable controls with per-control tune steps.**
(Version note: 6.9x had no room left for a feature bump — this is the
scheme's Y-digit rolling over, not a milestone claim.)

- Every control in the Tuning Device window is now an editable row:
  action picker (any of the twelve radio actions, or Unassigned) plus,
  for tune actions, a **per-control step** — "UI tune step" (follows
  the control-bar picker, the old behavior) or a fixed 1 Hz…1 MHz
  choice. Dial at a locked 10 Hz with keys jumping 5 kHz is now a
  30-second setup.
- **Learn**: arm it, press anything on the device, and the control
  appears as a new row ready to assign — this is how the D100H's four
  edit keys (Copy/Paste/Undo/Redo, keyboard-page combos we deliberately
  didn't pre-map) become usable, and how a future device's surprises
  get mapped without code changes. While armed, the captured press
  never fires an action. Rows are removable; **Reset to defaults**
  restores the template's factory mapping.
- Mappings persist per template as JSON (`tuningDevMappings`), seeded
  from the template's factory bindings; the template itself stays
  read-only code.
- Architecture: `TuningDeviceManager` no longer resolves actions — it
  reports raw (usage page, usage) presses and RadioState owns the
  mapping, so remap/Learn edits never drop and re-seize the device
  mid-session.

## [6.91] — 2026-07-19

**FIXED: the D100H template never matched the real hardware.** The knob
advertises itself over Bluetooth as **"Ulanzi Dial"** (observed live at
first pairing), not anything containing "D100H", so the product-name
match — and therefore the whole integration — sat at "waiting for
device" forever. The template now matches "ulanzi dial" too.

## [6.90] — 2026-07-19

**Tuning Devices integration: hardware knob controllers drive the VFO,
starting with the Ulanzi D100H.**

- New `Integration/TuningDevices/`: predefined device **templates**
  (match a HID product name → map its controls to radio actions) behind
  a Tuning Device window (Integrations menu). Off by default; nothing
  changes while disabled.
- **Ulanzi D100H** template (Bluetooth 5.0 dial + 7-key pad, factory
  "offline mode" mapping — no Ulanzi Studio needed): dial = tune
  up/down one tune step, dial press = cycle tune step (10…500 → Auto),
  prev/next-track keys = band step down/up, play/pause = RX mute. The
  four edit keys (Copy/Paste/Undo/Redo) are left unmapped for now.
- `TuningDeviceManager` (IOHIDManager, main run loop): enumerates
  consumer-control/keyboard HID devices, claims only template-matched
  ones, and opens them **exclusively** (seize) by default so the D100H
  dial's factory Volume± usages tune the radio without also sliding the
  system volume — with automatic fallback to shared capture (status
  says which). First enable prompts for the macOS **Input Monitoring**
  permission; the window's checklist covers the grant-then-relaunch
  dance.
- Settings window shows live status (waiting/connected/permission
  coaching), the template's control map, a **Live input** monitor
  printing every raw HID press (bring-up aid for unrecognized devices),
  and the product names of all knob-candidate HID devices present.
- Persisted: `tuningDevOn` / `tuningDevTemplate` / `tuningDevExclusive`
  (enable restored last, Discord-style, so the manager starts with
  restored settings).
- Knob actions reuse the existing tuning vocabulary (`tuneBy` at
  `effectiveTuneStep`, `stepBand`, mode cycle, volume/mute, A⇄B) — a
  detent behaves exactly like the equivalent scroll/arrow gesture, and
  the tune-step picker in the control bar reflects dial-press cycling
  live.

*Not yet hardware-validated: written against the D100H's documented
factory HID mapping (consumer-page Volume±/Mute/media keys); the Live
input panel is the bring-up tool if the real device reports different
usages.*

## [6.81] — 2026-07-18

**FIXED: PTT with Source = Audio file made zero RF (field-found on the
ANAN → Mercury IIIS amp chain).** The mic contract is "blocks always
flow while armed" — silence included — and AM's carrier depends on it
(I = 0.45·(1+x) needs x = 0 blocks to exist; a starved TX ring streams
zero IQ, so the amp's relay clicked on PTT but never saw drive). The
file player only delivered while the transport was rolling, so keyed-
with-stopped-transport starved the ring. Now its 10 ms feeder runs for
the whole armed window (`startFeeding`/`stopFeeding` on the engine's
arm lifecycle) and ticks silence blocks whenever the transport is
stopped, paused, at EOF, or has no file loaded — PTT in AM now makes
the same carrier the mic source would, and play/pause merely swaps
program audio in and out of the running stream. Natural EOF stops the
transport, not the feeder.

## [6.80] — 2026-07-18

**RX EQ grows up: dedicated button, 7 bands, profiles.**

- The receive EQ moves out of the DSP popover into its own **RX EQ**
  button on the control bar (label glows orange while active), and
  goes from two shelves to a **7-band graphic EQ** — RBJ peaking
  sections at 100/200/400/800/1600/3200/5000 Hz, ±12 dB, one-octave
  bandwidth. Peaking on the end bands too (a shelf only reaches half
  its gain at the labeled corner — the sliders should mean what they
  say). Vertical faders with 0.5 dB detents, double-click to zero,
  same fader control the TX user EQ uses.
- **Built-in profiles**: Flat, DX / Contest, Rag-Chew Warmth,
  Broadcast Hi-Fi, Presence, Hiss Tamer, AM Music. Picking one
  switches the EQ on.
- **Custom profiles**: Save as… snapshots the current curve under
  your name (persisted, deletable from the Profiles menu). The footer
  shows which profile the current curve matches, or "Custom curve".
- The old bass/treble settings migrate into an equivalent 7-band
  curve on first launch; `AudioEQ` tolerates short/stale persisted
  arrays (missing bands stay flat, gains clamp). Band response,
  profile sanity, flat-passthrough, and clamping pinned by
  `testAudioEQBandSense`.

## [6.70] — 2026-07-18

**RX antenna selector on the main control bar.** The ANT jack picker
(ANT1/2/3, EXT1, XVTR, BYPS) now also lives in the control bar's DSP
row next to the ATT/LNA controls, as a compact menu showing the active
jack — no more digging into the gear popover to switch antennas. Same
per-band memory and P2-only gating as before (`rxAntennaSelectable`);
the gear popover keeps the full section with the filter-bypass and 6 m
preamp toggles.

## [6.60] — 2026-07-18

**Performance pass (#37): the traced hot-path backlog, implemented.**
All behavior pinned by the existing test suites (162/162 green, bit-
identical limiter minima, FIR outputs, multiband flat-sum).

*Structural.* RXChain now fires its callbacks (decoder fleet, audio
ring, meters, Discord fan-out) AFTER releasing the chain lock — the
decoder fan-out alone could hold it for hundreds of µs, every
main-thread setter blocked behind it, and a callback touching a chain
setter was a standing NSLock deadlock trap. And the high-rate readouts
(S-meter 10 Hz, the 11-property TX meter set at 30 Hz, the hover
cursor at pointer-move rate) moved off the monolithic RadioState into
a dedicated `MeterState` object observed only by the leaf views —
hovering the panadapter no longer re-evaluates every window in the
app at pointer rate.

*Allocation churn.* UDP receive hands parsers a zero-copy view into a
reused buffer (was ~6.5 k Data allocations/s at the P2 1536 k rate;
borrow contract documented, all handlers parse synchronously). P2 IQ
unpack subscript-fills; the 800 pkt/s TX IQ packet reuses one scratch
buffer and sends zero-copy (new `UnsafeRawBufferPointer` send
variant), P1 EP2 likewise skips its per-packet Data copy.
TXUpsampler (the hottest FIR site, ×2 channels at 800/s while keyed),
TXChain's `firWithTail`, and the multiband compressor all run on
persistent scratch instead of per-block concat/allocate; the TX ring
drains via a head cursor instead of memmoving the remainder every
pull; the LookaheadLimiter's O(window) sliding-minimum scan (121
compares/sample at 48 k) became a monotonic deque — amortized O(1),
bit-identical output.

*Decoders/UI/misc.* WEFAX renders new lines incrementally instead of
rebuilding the whole RGBA chart every 8 lines (~430 MB of cumulative
conversion per chart, gone). AutoNotch predicts/updates via vDSP over
a doubled history buffer (~3 M modulo ops/s removed). The waterfall
wipe is one full-texture blit instead of 2048 per NCO retune; the
sub-RX window runs its display link at 30 fps. Data sockets set DSCP
EF (0xB8) like pihpsdr — QoS switches prioritize the IQ/TX stream.
Discord voice reuses its PCM buffer and drains a bounded second frame
per tick when backlogged, so clock skew no longer ratchets latency to
the 1 s FIFO cap. PSKReporter resolves DNS and opens its socket once
per upload cycle instead of per 50-spot chunk.

Deferred (still on #37): SSTV/WEFAX `meanFreq` prefix sums, the
offscreen-capture rework that would restore `framebufferOnly`, CESSB
filterPass scratch (default-off path).

## [6.51] — 2026-07-18

**#36 cleared: the twelve minor defects deferred from the 6.50 sweep.**

*Protocol/streaming.* The P2 wideband assembler is now linear (seq 0
starts a frame, any gap drops the partial) — the old dict-by-raw-seq
design collided across frames after a dropped packet and emitted a
spliced half-and-half bandscope frame, and its hole-recovery branch was
unreachable. Discovery unicast probes finally resolve hostnames
(`hl2.local` was silently never probed — `UDPSocket.send` is
inet_pton-only; successes cache, failures retry after 60 s so a dead
name can't stall the 3 s burst), and an unparseable host records EINVAL
instead of leaving a stale errno to poison the Local-Network-denied
classifier. Both stacks now zero-fill a short `onTXIQ` return instead
of indexing out of range mid-over ("starved = silence" is now true).

*TX/audio.* Re-keying while the roger-beep tail is still draining now
fades the tail's next 5 ms into the new over instead of hard-stepping
the transmitted IQ to zero (a key click) — gated on a tail deadline so
a long-dead over's leftover ring still never transmits. The beep runs
on COPIES of the shared bandpass/Hilbert FIR tails, so ~10 ms of beep
no longer convolves into the next over's first mic block. TXFilePlayer
drains the rate converter's internal tail at EOF/loop wrap (the reset
used to drop it — an audible tick on every seamless loop, a clipped
ending on natural EOF).

*Decoders/UI/app.* WEFAX finally has an exit from `imaging` besides a
stop tone or the 1200-line cap: 10 s of solidly out-of-band signal
aborts — salvaging a real partial chart (>30 lines) or failing
`noSignal` for a noise-only run. RTTY's AFC floor creeps only while no
tone rides above the gate, so slow drift-tracking survives long
transmissions (same failure family as 6.50's ALE floor fix). SUB
toggle now clears the IQ history ring and bumps `historyEpoch` (the
stop/start paused the ring's sample clock against wall time, skewing
bookmark ages ~0.5 s per toggle) and drops any time shift back to live
— ending the historical-main-plus-live-sub incoherence. Click-tune
clamps the carrier inside the sampled span (LSB clicks near the pinned
display edge could demodulate an alias with the marker off-screen).
Waterfall captures queue instead of overwriting each other, and the
shared capture texture can't be re-blitted while a readback is still
encoding the PNG (torn image). Discord op 9 honors the resumable flag
— a resumable invalid session resumes instead of discarding the
session and replayed events.

## [6.50] — 2026-07-18

**Full-codebase bug sweep — 7-subsystem audit, ~20 fixes + a perf pass.**
A parallel deep review of every subsystem (protocol, RX DSP, decoders,
TX/audio, app state, UI/rendering, integrations) confirmed the
documented invariants all hold (CAT PTT cannot key without ARM; P2 byte
maps match the spec docs; TXChain/RXChain lock discipline is clean) and
surfaced the defects fixed here.

*ALE (the headline fixes).* The noise-floor estimator fed **every**
symbol's winning-tone power into its EMA — under a continuous 8-FSK
transmission the floor converged toward the signal and the 6× "strong"
test started failing ~1.5 s in, killing decode for the rest of the
transmission (and, floor still elevated, gating out the start of the
next one). It now learns from non-signal symbols only. And ALE finally
reports through the decoder-session layer as 6.20 documented: sessions
in the Decoder Activity window, per-word time-machine bookmarks, proper
acquiring/decoding transitions — plus a real enable toggle
(`aleMonitorEnabled`, persisted, off by default like every other
decoder; tapping a network channel turns it on) so the decoder no
longer burns DSP cycles in every mode with no window open.

*State/persistence.* Recalling a cross-band bookmark (or an ALE
channel) baked the destination's mode/filter/LNA/ATT into the band
being **left** — the exact didSet-vs-stale-VFO clobber `restoringBand`
was invented for, now gated at both call sites. `dbFloor` restored
before `dbCeil` and got clamped against the default ceiling, silently
drifting saved waterfall levels 20 dB darker across launches — restore
order swapped. `disconnect()` now clears the leftover stats/S-meter/
C-QUAM-lamp state and re-arms decoder enables so a half-received SSTV
session can't sit "Receiving" forever. FT8 spot clicks subtract RIT
(the spot's RF was computed RIT-shifted). Replay rejects `.sqiq` rates
the UI can't describe (foreign 24 kHz files tuned at 8× off) and
corrupt headers with non-finite center frequencies.

*TX.* The AM +peak control could arm ratios the 0.45 carrier can't
carry — past ~129% positive peaks flat-topped at the Int16/Int24 wire
conversion, i.e. clip splatter applied AFTER every band-limiting stage.
`setAMPositivePeak` hard-caps at 1.28 and the slider tops out at the
classic Optimod 125%; the pinned test now asserts the wire envelope
stays inside full scale even for a requested 150%. Roger beep: the
next mic block after unkey passed the `keyEnv > 0` gate and appended
~10 ms of live mic scrap BEHIND the beep — envelope now zeroed on the
beep path. WavRecorder headers count only frames that reached disk, so
a disk-full salvage no longer claims audio that isn't there.

*Protocol.* Both stream watchdogs stamped wall-clock `Date()` — an NTP
step or sleep/wake adjustment could fake >1.5 s of "silence" on a
healthy stream, restarting it and force-unkeying a keyed TX; both
stacks now use monotonic uptime. P2 `phaseWord` clamps below 2³²
instead of trapping (a ≥122.88 MHz frequency would have killed the
process mid-stream).

*RX DSP.* NoiseReducer: a bin seeded at exactly 0 (digital-silence
replay leader) could never leave 0 and permanently disabled NR for
that bin — additive epsilon on the creep. C-QUAM: retune now re-arms
the carrier-track warm-up seed (stale weak-station track over-scaled a
strong station ~100× for the first second). WEFAX: the tone-end anchor
captured `pos - blockCount` AFTER the counter reset, landing 0.1 s
late — captured before.

*Integrations.* Discord gateway + voice now track heartbeat ACKs — a
missed ACK reconnects (gateway) or stops with a clear message (voice)
instead of showing "connected"/"streaming" forever on a dead session.
Non-recoverable close codes (4004/4013/4014) stop reconnecting instead
of re-identifying into a rate limit. Voice IP discovery retransmits
(one lost UDP datagram used to hang the join silently) and a re-sent
SESSION DESCRIPTION no longer resets the AES-GCM nonce counter under
an unchanged key. The "going offline" message actually posts now (it
always lost the race with gateway teardown). PSKReporter re-queues
spots on transient send failures (a DNS blip used to silently drop up
to 5 minutes of them) and no longer resets its upload timer on every
callsign/grid keystroke. rigctl surfaces port-in-use to the UI
(NWListener reports it async — CAT used to look healthy while another
rigctld owned 4532). Sub-RX window: clicks within ±8 px of center were
swallowed by a phantom VFO-marker grab (nil drag handler) — exactly
where the tuned signal lives. The stale disabled "PTT — coming in
phase 2" button is gone.

*Performance.* `persist()` (~100 UserDefaults keys + change
notifications) fired on every scroll tick — now debounced 0.3 s with a
guaranteed quit flush; band memory keeps an in-memory cache instead of
bridging the whole dictionary per tick. Filter rebuilds use a
tabulated decimation-droop curve (was ~500k scalar trig ops on the
main thread per bandwidth-slider quantum). NoiseReducer hoists its six
per-call scratch arrays; FT8 slot capture pre-reserves its buffer;
Discord status polling skips the 5 s main-actor round-trip when
notifications are off.

## [6.40] — 2026-07-18

**ALE "easy button" — seeded networks + noise gate (#35).** The ALE
Monitor window now leads with a one-click network/channel picker: the
**HFLINK HFN** amateur 2G-ALE net (active 24/7 since 2001) with all nine
band channels (80 m → 10 m, USB) — tap a band and it tunes the dial to
USB on that channel, ready to monitor (the active channel highlights).
And a false-positive fix: because the perfect Golay decoder "succeeds"
even on noise, the decoder now only emits words whose three characters
are valid ALE address symbols (A–Z, 0–9, space, @, ?), so band noise no
longer spews `[DATA] …` garbage. Frequencies verified against
hflink.com.

## [6.30] — 2026-07-18

**ALE — real 2G reception chain (#35).** Rebuilt the decoder from the
simplified 6.20 framing to the actual MIL-STD-188-141A waveform, pinned
against the standard and the LinuxALE reference: the **Gray tone mapping**
(tribit→tone `[0,1,3,2,7,6,4,5]`), **even/odd bit-interleave** into two
Golay(24,12) codewords, **triple-redundancy majority voting** (each 49-bit
word sent 3×; vote bit *i* against *i*+49 and *i*+98), and **FEC-success
self-synchronization** (no preamble — it slides the symbol phase and locks
where Golay decodes cleanly). The extended `ALEProtocolTests` fixture
proves it end-to-end: junk lead-in → self-sync → both words recovered,
plus majority-vote correction of injected bit errors. Remaining for
genuine off-air decode (issue #35): matching ALE's exact Golay systematic
convention + the second-word bit inversion, then an on-air ear test.

## [6.20] — 2026-07-18

**ALE decoder — working 8-FSK pipeline + monitor window (#35).** Builds
on the 6.10 FEC foundation into an end-to-end decoder: `DSP/ALE/
ALEDecoder.swift` adds the **8-FSK modem** (8 tones 750–2500 Hz, 125
baud, continuous-phase modulate + Goertzel tone-bank demod) and a
**streaming word decoder** (symbol squelch → tribits → 48-bit FEC words →
Golay decode → 24-bit ALE words → TO/FROM/TIS/CMD text). A
**synthesize→decode fixture** proves it end-to-end (words → 8-FSK audio →
decoder recovers `[TO] WU1`, `[FROM] K1A`). Wired into the demod-audio
tap like the other decoders, reporting through the decoder-session
system, with a new **ALE Monitor window** (Window menu). Milestone-1
scope: decodes clean, symbol-aligned 8-FSK; robust real-signal lock
(preamble/dotting sync, 49-bit interleave, redundant-word majority
voting) and off-air validation remain on #35.

## [6.10] — 2026-07-18

**ALE decode core — milestone 1 foundation (#35).** Groundwork for an
Automatic Link Establishment (MIL-STD-188-141A "2G ALE") monitor — no
user surface yet. `DSP/ALE/ALEProtocol.swift` lands the protocol/FEC
base: the **Golay(24,12)** codec (built on the perfect cyclic [23,12,7]
Golay, generator 0xC75, with an exact syndrome→coset-leader table so it
corrects any ≤3-bit error unambiguously), the eight ALE **word types**,
and the 24-bit **word model** (3-bit preamble + three 7-bit chars) with
FEC-protected pack/unpack. `ALEProtocolTests` pins clean encode/decode
over all 4096 data words, full ≤3-error correction, and word round-trips
through FEC-with-errors. Next on #35: the 8-FSK demodulator, deinterleave
+ majority vote, and reporting through the decoder-session system.

## [6.00] — 2026-07-18

**Waterfall image sender.** A new camera button in the control bar
captures the live panadapter (spectrum + waterfall) to a PNG and sends
it two ways: **Save / Share** (writes to the Recordings folder and opens
the macOS share sheet — AirDrop, Messages, Mail, …) and **Post to
Discord** (uploads the image to the configured text channel as a message
attachment, captioned with the current frequency/mode, over the
integration hardened in 5.80). The capture reuses the render: the just-
drawn Metal drawable is blitted to an owned texture and read back to PNG
off the render path, so it matches exactly what's on screen. **Speed
presets** (WSJT-X, KiwiSDR slow/medium/fast, Thetis, Fast) set the
waterfall scroll rate to emulate how each SDR's waterfall looks before
you capture.

## [5.90] — 2026-07-18

**Status-bar CPU indicator + seq-error hover.** A **CPU %** readout now
sits beside the GPU indicator, showing SquareDeck's own usage across all
its threads as a share of one core (can exceed 100% multicore — the same
basis Activity Monitor uses; `CPUMonitor` reads mach thread scheduling
info, polled with the 1 Hz GPU timer). And the **sequence-errors** count
now has a hover explanation: what a seq error is (a dropped/out-of-order
UDP packet = a gap in the IQ stream), the usual causes (Wi-Fi, congested
LAN, sample rate too high for the link), and the fixes.

## [5.80] — 2026-07-18

**Discord integration diagnostics + coaching.** The integration used to
fail silently — a bad token or a bot that couldn't join just looped with
no explanation. Now every connection step and failure surfaces in a
**Connection diagnostics** log in the Discord window, with plain-language
coaching:

- **Gateway close codes** are read and explained — e.g. 4004 → "bad token,
  re-copy from Developer Portal → Bot → Reset Token"; 4013/4014 (intents);
  4008 (rate limited). A drop before the bot ever authenticates falls back
  to the same bad-token / firewall coaching even when the raw code is lost.
- **Voice join** now logs each step (join requested → voice state → voice
  server → media connecting → streaming) and, if Discord sends no voice
  server within 6 s, prints the checklist: bot is in the server, correct
  Server/Voice-channel IDs, it's a voice channel, and the bot has Connect.
- **Voice close codes** (4004/4006/4011/4014/4015/4016) and **REST errors**
  (401 token, 403 permissions/scopes, 404 wrong ID, 429 rate limit) are
  explained instead of only hitting the log.
- **Pre-flight** validates the token/ID fields (snowflake shape) before a
  join and flags a pasted name or invite link.
- A **Setup checklist** disclosure in the window, plus Copy/Clear for the
  log. Pure helpers (`DiscordDiag`) are unit-tested; no change to the
  SDR/audio path.

## [5.70] — 2026-07-18

**Customizable keyboard map + richer bookmarks.**

- **Keyboard shortcuts** (new ⌨ button in the control bar): map keys to
  actions — PTT (push-to-talk, hold), TUNE, mute RX, cycle NR, volume
  ±, mode ±, band ±, VFO A/B swap, zoom ±, bookmark current, toggle
  sub-RX, record. An app-wide key monitor (`App/KeyMap.swift`) fires
  bindings regardless of focus but is suppressed while you're typing in
  a field; PTT uses key-up tracking for true hold-to-talk and, like CAT
  PTT, only transmits when armed. The mapping table supports
  click-to-record rebinding, conflict resolution (a key bound to a new
  action is cleared from its old one), clear, and reset-to-defaults;
  bindings persist as `keyMap`. Defaults: Space=PTT, Esc=mute, N=cycle
  NR, V=VFO swap, =/− zoom, B=bookmark. The panadapter's hardcoded `N`
  moved into the map (arrows still tune the focused panadapter).
- **Bookmarks now store the full station setup** — a bookmark captures
  filter width, IF shift, LNA gain and attenuator alongside frequency +
  mode, and restores them all on recall (mode first, then the saved
  filter so per-mode memory doesn't override it). New fields are
  optional, so pre-5.70 saved bookmarks still load. The popover shows
  the filter width and gain in each row.

## [5.60] — 2026-07-18

**TX bandwidth footprint on the panadapter.** The transmit bandwidth is
set by the selected TX **profile** (its audio passband), independent of
the main-window RX filter width — and it's now drawn so you can see it.
An orange **TX** band (fill + edge lines + label) is always shown on the
panadapter at the profile's occupied bandwidth around the TX carrier
(the dial — RIT slides the RX passband off it, the TX footprint stays
put), mapped to RF per mode: USB above the carrier, LSB mirrored below,
AM/SAM double-sideband, CW nothing (carrier only). Styled apart from the
yellow RX passband so both read at once. The TX Controls Profile row
also gains a live readout — e.g. `100–4000 Hz · 3.9 kHz occupied (LSB)`
— resolving custom profiles to their base voicing. Display-only, no
change to the TX path (`RadioState.txProfilePassband` /
`txFootprintOffsets`).

## [5.50] — 2026-07-18

**Selectable TX antenna on Protocol 2 (ANAN) — live-validated.** The P2
TX path previously force-pinned the PA output to ANT1 while keyed (a
deliberate 3.20 safety default when no picker existed). It now routes to
a **user-selected ANT1/2/3**: new `TXAntenna` type + `supportsTXAntenna`
capability, the keyed Alex0 relay word sets bits 24/25/26 from the
selection (the RX antenna routing is still never allowed to steer the PA
— RF can only ever follow the dedicated TX pick), and a **TX ANT
segmented picker** in the TX Controls window (P2 only, disabled while
keyed/tuning since a hot relay swap under power arcs the Alex contacts).
The selection is a single global setting (not per-band) so a band hop
can never silently move the PA, and it persists as `txAntenna`.

Validated live on the ANAN-7000DLE MK2 (2026-07-18): keyed into a dummy
load on ANT2 through a Bird wattmeter, **flat SWR 1.0 across 3–34 W**,
power-cal `fwdPowerCalK.p2 = 0.28` reconfirmed against the Bird and PA
drain current (~43–48% efficiency, physically consistent), and a 2-tone
test at 80% drive with no flat-topping. The HL2 (single RF port) reports
`supportsTXAntenna = false` and the picker is hidden.

## [5.40] — 2026-07-17

**Eight new waterfall palettes.** The palette menu grows from 5 to 13:
**Plasma** (matplotlib's midnight → violet → magenta → orange →
yellow), **Abyss** (black-blue → indigo → teal → aqua → foam),
**Sunset** (indigo → plum → crimson → orange → gold), **Aurora**
(deep green → emerald → ice cyan → violet-white), **Synthwave**
(indigo → electric purple → hot pink → cyan glow), **Amber CRT**
(the Phosphor idea in vintage-terminal amber), **Glacier** (black →
navy → steel → ice → white) and **Copper** (oxide brown → copper →
rose gold → warm white). All keep a dark floor so the noise level
recedes and saturate near the ceiling so strong signals pop; the
existing five schemes are untouched, and the choice persists as
before (`wfColor`).

## [5.30] — 2026-07-17

**C-QUAM AM stereo in the receiver (#32, milestone 2).** The 5.20
decoder core is now live behind the SAM PLL: in SAM mode the chain
feeds the PLL's carrier-locked I/Q pair — normalized by a slow
carrier-amplitude track so the decoder's envelope math (A ≈ 1+L+R)
holds at any signal level — through `CQUAMStereoDecoder` on every
block, and the DSP popover grows an **AM stereo** row (SAM only): a
STEREO lamp driven by the 25 Hz pilot detector plus a **Mono / L / R**
pick (persisted, `cquamPick`). The audio path is still single-channel,
so milestone 2 is a channel pick, not a blend — Mono is the classic
coherent sum, bit-identical to 5.20's SAM. Wrinkles found and pinned
by the new `CQUAMChainTests` (C-QUAM at RF through the production
mixer → decimators → PLL → decoder chain):

- The SAM loop (ωn = 250 rad/s) **tracks part of the 25 Hz pilot's
  phase wobble** before the decoder sees it, so the lamp threshold is
  scaled by the loop's phase-error transfer at 25 Hz (analytic 0.28,
  measured ~0.6 through the chain — comfortably conservative).
- During PLL acquisition the pilot correlator reads unlocked-phase
  garbage ~10× the real pilot decaying over ~1 s — a bare threshold
  would flash STEREO on every mono station. The lamp requires two
  consecutive ~100 ms reports within ±30% (a real pilot is steady, a
  transient never is); the mono-AM test asserts the lamp never lights,
  even during acquisition.
- The FFT channel filter emits **empty blocks during overlap-save
  warmup**; `vDSP_meanv` over zero samples wrote NaN into the carrier
  seed, and `NaN == 0` kept it from ever re-seeding (permanently dead
  audio in L/R pick). Guarded, and the seed is finite-checked.

Sub-RX stays on the plain sum; L/R pick is main-chain only. Milestone
3 (TX encoder — envelope-only limiting, stereo file-player path)
remains on #32.

## [5.20] — 2026-07-17

**C-QUAM AM stereo decoder core (#32, milestone 1).** Groundwork release
— no user-facing surface yet: `DSP/CQUAM.swift` implements the Motorola
C-QUAM decode math on carrier-locked complex baseband (S = |z|−1,
D′ = |z|·Q/I with a clamp past 100% negative modulation, matrix to L/R)
with a quadrature 25 Hz pilot detector. Pilot removal is **coherent
subtraction** of the tracked estimate, not a filter — a notch deep
enough to kill 25 Hz carries phase lead across the whole program band
(measured: −30 dB Q2 still led +5.5° at 700 Hz, degrading channel
separation to 27 dB), while subtraction leaves the program untouched.
`CQUAMTests` proves the math against a spec-faithful encoder fixture:
envelope exactly 1+L+R (mono compatibility), >30 dB channel separation,
equal-split mono decode with no false pilot lamp, pilot cancelled from
the audio. Next milestones: RXChain integration behind the SAM PLL +
STEREO lamp, then the TX encoder.

## [5.10] — 2026-07-17

**AM broadcast air chain (#31) — NRSC conformance, platform AGC, 5-band,
adjustable positive peaks.** The Optimod-topology batch, all pinned by
`TXBroadcastTests` (dummy-load validation batched with #13):

- **NRSC AM Broadcast profile**: the true NRSC-1 truncated 75 µs
  pre-emphasis curve (`NRSCEmphasis`, bilinear prewarped at the 2.12 kHz
  zero, +10 dB truncation pinned against the analog formula) applied
  just ahead of the leveler so compression/limiting control the
  emphasized modulation; the profile's 10 kHz bandpass edge is the
  NRSC-2 lowpass. 50–10000 Hz, dense 5:1, +125% positive peaks.
- **RX AM de-emphasis** toggle (DSP popover, AM/SAM only, main + sub
  chains): the exact inverse at the 12 kHz audio rate — the 6.71 kHz
  analog pole sits above that Nyquist, so a grid-searched correction
  shelf (3.8 kHz, +2.8 dB, Q 0.7) flattens the 48 k-pre → 12 k-de
  monitor loop to ±0.16 dB through 5.5 kHz (test-pinned ±0.3 dB).
  Applied after the decoder tap — decoders keep raw detector audio.
- **Platform AGC** (`PlatformAGC`, TX Controls toggle): slow feedforward
  gain rider ahead of EQ/compression — ±10 dB toward −14 dBFS RMS,
  +1 dB/s release / −4 dB/s attack, and a 10 ms-envelope gate at
  −45 dBFS so pauses freeze the ride within ~50 ms instead of dragging
  the noise floor up (the slow envelope alone coasts above the gate for
  most of a second — caught by test).
- **5-band compression**: the multiband is now an N-band Linkwitz-Riley
  crossover tree with per-band allpass phase compensation (LR4's LP+HP
  sums to exactly that AP2) — Single/3-band/5-band picker; 5-band splits
  at 100/400/1600/6300 Hz with geometrically-spread time constants; the
  validated 3-band constants are untouched. Flat reconstruction pinned
  for both topologies.
- **AM +peak slider** (100–150%, asymmetric-AM profiles): the user
  ceiling now drives the limiter's positive headroom (the profile flag
  only arms the machinery); test-pinned that 140% yields a 1.40
  positive/negative modulation ratio and 100% never lets positives past
  the cap.
- Chain map: PLATFORM AGC and NRSC PRE-EMPH stages, band-count in the
  compressor row. Persisted: `txAGC`, `txMbBands`, `amPosPeak`,
  `amDeemph`.

## [5.00] — 2026-07-17

**Flexible TX program input (#33) — built-in file player + stereo-capable
source path.** First slice of the AM broadcast roadmap: repeatable lab
program material with no external audio routing.

- **Source picker** in TX Controls: Microphone (unchanged) or **Audio
  file** — `TXFilePlayer` plays any CoreAudio-readable file (WAV/AIFF/
  MP3/AAC/CAF/FLAC) into the same `TXChain` push path as the mic at
  real-time pace (480-frame / 10 ms blocks off a monotonic dispatch
  timer), so profiles, rack, meters, monitor and keying behave
  identically. Transport (play/pause/stop/seek slider), loop, file
  level, position readout; playback is armed-gated like the mic, and
  the file source skips mic capture entirely (no TCC prompt). BlackHole
  loopback remains the zero-code route for live system audio.
- **Stereo-capable source API**: `TXChain.feed(left:right:)` — folds to
  the exact mono average today (pinned bit-identical by
  `TXStereoFeedTests`), reserved to carry L/R deeper for C-QUAM (#32).
  The player delivers a true L/R pair (channels extracted by hand after
  a rate-only AVAudioConverter — never a channel-count conversion, the
  MicInput 3.62 lesson).
- TX Audio Chain map shows the FILE stage when the file source is
  selected. Persisted: `txSource`, `txFilePath`, `txFileLoop`,
  `txFileLevel`.

**Quit can no longer be silently cancelled (P2 busy-latch, third
round).** Found while verifying this release: with the connect sheet
front and its manual-host field editor active, AppKit cancels the ENTIRE
termination sequence before the app delegate is even consulted — Cmd-Q,
AppleScript quit and `kill -TERM` all silently no-oped (so the 4.81
clean-quit guarantee evaporated exactly when the app sat disconnected,
and a previously-connected P2 radio would re-latch; logout would have
been blocked the same way). SwiftUI installs its own NSApplication
subclass, so neither `NSPrincipalClass` nor `applicationShouldTerminate`
can intercept. Fix: `quitUnstoppably()` — end editing, attempt the
normal terminate (never returns when it succeeds), and when it comes
back cancelled, run the same synchronous cleanup the real path runs
(willTerminate observers: RUN=0 disconnect + settings flush) and exit.
Wired into all three entries: the SIGTERM/SIGINT handlers, a replaced
Quit menu command, and our own quit-AppleEvent handler (installed after
AppKit's at launch). Verified 3× SIGTERM + AppleScript + Cmd-Q under
the repro conditions.

## [4.90] — 2026-07-17

**Settings survive uninstall — Application Support config file.** Every
app setting (the whole `com.squaredeck.app` defaults domain: band
memories, TX profiles + rack, cal factors, Discord config, …) now
mirrors to a human-readable XML plist at
`~/Library/Application Support/SquareDeck/Settings.plist`
(`SettingsFileStore`, activated before `RadioState` restores).

- Fresh install / reinstall (empty defaults) → the file is imported
  wholesale at launch and everything comes back.
- Hand edits while the app is closed are honored: each export records
  `savedAt` inside the file, so a later filesystem modification date
  means an editor touched it and the file wins at next launch. (Edits
  while the app is running are clobbered by the next export.)
- Runtime behavior unchanged: UserDefaults stays the source of truth;
  exports ride `UserDefaults.didChangeNotification` on a 2 s debounce
  plus a synchronous flush at quit, so no persist() site changed.

## [4.81] — 2026-07-17

**ANAN busy-latch after app restart — actually fixed.** The 4.02 clean
quit only covered AppKit-mediated termination (Cmd-Q): a raw
`kill -TERM` (or Ctrl-C) kills the process with its default signal
disposition — no `willTerminateNotification`, no RUN=0 — leaving the P2
radio latched "in use" and un-connectable. Confirmed live today: the
scripted restarts between releases left the ANAN reporting busy
(status 0x03).

- SIGTERM/SIGINT now route through `NSApp.terminate` via
  DispatchSourceSignal handlers, so every termination path sends RUN=0.
- **Release button** in the connect sheet for busy P2 radios: sends a
  discovery probe + High-Priority RUN=0 from the discovery socket (the
  firmware only honors C&C from a source it has seen a probe from) and
  refreshes the list — recover in-app from ANY unclean death of a
  previous client (crash, force-kill, power loss), no Python required.

## [4.80] — 2026-07-17

Three-issue batch: Local Network permission detection (#26), the About
window (#28), and the optional Discord integration (#29).

**Local Network detection (#26)**: UDPSocket records failed-send errnos;
discovery classifies a fully-failed probe burst — no broadcast-capable
interfaces = *no network*; all failures EHOSTUNREACH/EPERM/EACCES with
interfaces up = the *macOS Local Network permission wall*; anything else
= plain send failure (firewall/VPN hint). Sticky diagnosis (change-only,
unified-log), auto-clearing the moment sends succeed or a radio answers
(discovery already retries every 3 s). The connect sheet shows a
prominent non-modal banner per case with a System Settings deep link and
a Learn More explainer.

**About window (#28)**: Help ▸ About SquareDeck… (and the app-menu item)
open a single-instance dark branded window — the checked-in SVG logo
(bundled copy; text fallback), version/build from bundle metadata,
description, GitHub/Docs/Issues links, a Licenses popover (RNNoise
BSD-3, ft8_lib MIT), and Copy System Information via the testable
`SupportInfo` formatter (privacy-safe: version, macOS, arch, connection
summary only).

**Discord integration (#29)** — optional, off by default, zero
third-party dependencies (URLSession WebSockets, CryptoKit AES-256-GCM,
AudioToolbox Opus):
- Gateway v10 client (hello/identify/heartbeat/resume, exponential-
  backoff reconnect) on its own queue — Discord outages can't touch the
  SDR path.
- Slash commands `/status /frequency /mode /signal /uptime /recording
  /decoders /help` registered on READY and answered from a main-actor
  state snapshot (`RadioStatusSnapshot`, S-meter in S-units, layout
  matching the issue's example).
- Optional channel notifications (connect/disconnect, tuning, recording,
  live decoder completions — never replays), rate-limited per category.
- **Voice streaming**: gateway op4 → voice gateway v4 → UDP IP
  discovery → `aead_aes256_gcm_rtpsize` → Opus (48 kHz, 20 ms frames,
  encoded by AVAudioConverter) at a paced 20 ms cadence with trailing
  silence frames. Encryption/RTP layout pinned by seal↔open and
  tamper-detection tests.
- **AudioFanout** (`RadioEngine.audioFanout`): the final speaker mix now
  broadcasts to registered sinks — local monitoring, recorder, and the
  Discord encoder run simultaneously off one stream; no virtual audio
  cable anywhere.
- Integrations ▸ Discord… settings window: token, guild/channel IDs,
  notifications toggle, voice join/leave, live status. Settings persist;
  token stays local and is never logged.
- 13 new tests: gateway payloads, status/command formatting, voice
  packet seal↔open + header-tamper auth failure, IP discovery framing,
  SupportInfo. Suite: 137 tests green.

## [4.70] — 2026-07-17

**FT4 promotion + docs single source of truth** (issues #19 and #23 —
the decoder series 4.10–4.70 is complete).

FT4 (#19) — the engine, spots, panel, PSKReporter, persistence, session
layer, and time-machine replay already handled FT4; this release closes
the real gaps:
- **ADIF fix**: FT4 was exported as `MODE=FT4`, which is invalid ADIF —
  FT4 is a SUBMODE of MFSK. Stations-heard exports now write
  `MODE=MFSK` + `SUBMODE=FT4` (`Integration/ADIF.swift`, shared with
  the test package and pinned by tests, incl. UTF-8 byte-count field
  lengths).
- Decode panel title reflects the active mode; log rows carry an FT4
  tag when the session log holds both modes.
- README/capability matrix now states the FT4 support level explicitly.

Docs source of truth (#23):
- **One authoritative version**: `MARKETING_VERSION` in project.pbxproj;
  `DocsConsistencyTests` fails `swift test` when the newest CHANGELOG
  heading or the README "Current version" line disagrees (both configs
  must match each other too).
- **Capability manifest**: `DSP/Capabilities.swift` — SSTV/WEFAX/RTTY
  mode lists derive from the live mode tables (cannot drift); radio/
  platform prose lives there as the single statement. The README
  "Capabilities" table is generated from it and validated by test (the
  failure prints the fresh block to paste).
- **Fixture-coverage gate**: every SSTV mode must be named in
  SSTVModeTests; the WEFAX/RTTY suites must iterate their full preset
  tables — adding a mode without a fixture fails the build.
- README refreshed to 4.70 reality (intro, decoder highlights,
  capability table, contributor doc under Versioning). `swift test` is
  the repo's CI gate; historical changelog entries untouched.

## [4.60] — 2026-07-17

**Decoder events × RF Time Machine** (issue #22, 7/8 of the decoder
series): jump back to, re-decode, and export the signals your decoders
just saw.

- **Bookmarks**: every session bookmark (SSTV image start, fax start
  tone, FT8/FT4 slot decodes, …) is mirrored into a time-machine event
  list (family-colored, capped 60) shown in the clock-button popover
  with age, mode, frequency, and outcome. Bookmarks carry the IQ ring's
  generation counter (`historyEpoch`, bumped on every clear/rebuild/
  free) — retune, rate change, diversity switch, or disconnect marks
  them *expired* rather than silently pointing at the wrong RF.
- **Jump + replay**: tapping an event retunes the VFO to the bookmarked
  frequency (same epoch ⇒ still inside the sampled span) and rewinds
  the time machine to 5 s before it — the enabled decoders then
  re-decode the replayed audio through the exact same production path
  as live reception, with whatever settings you've changed since (RTTY
  config, SSTV manual mode, WEFAX profile). Sessions decoded while
  shifted are stamped `isReplay` and badged REPLAY in the Decoder
  Activity window, so original and replayed results sit side by side in
  the history for comparison. Expired jumps produce a clear error.
- **FT8/FT4 replays now too**: the slot engine gets a historical clock
  offset that follows the (clamped) time shift, so replayed audio
  decodes into its true UTC slots (offset changes abort the in-flight
  capture; PSKReporter uploads are suppressed during replay — those
  slots were already reported when they happened).
- **Excerpt export** (arrow button per event): a bounded IQ excerpt —
  2 s before the event through its end, capped at 60 s / ~96 MB — as a
  standard replayable `.sqiq` plus a same-basename `.json` sidecar
  (`DecoderExcerptMetadata`: decoder, mode, event label/dates, outcome,
  tuned/center Hz, rate, window, truncation flag; ISO-8601, documented
  in code) for regression fixtures and bug reports.
- Tests (7): ring excerpt extraction (window addressing, head clamp,
  2 s freshness margin expiry, wraparound seam, post-clear), metadata
  JSON round-trip + legibility, replay-flag default. Suite: 117 green.

## [4.50] — 2026-07-17

**WEFAX profiles + image recovery** (issue #21, 6/8 of the decoder
series).

- `WEFAXProfile` (data-driven): IOC 576 at 120/90/60 LPM (1200 px,
  300 Hz start tone) and IOC 288 at 120 LPM (600 px, 675 Hz start
  tone) — line rate, width, and start/stop-tone detection windows all
  come from the profile (blocks classify flips to the NEAREST of
  start/stop within ±25%). Profile picker + INV polarity toggle in the
  fax window, both persisted; sessions carry the profile name (#16).
  Fixed en route: the phasing fold reads back 4 line-lengths — 4 s at
  60 LPM — which overran the old 2.7 s discriminator ring; it's now
  5.5 s.
- **Polarity**: rows are stored polarity-neutral; INV applies at
  emit/re-render time, so flipping it re-displays the current chart
  immediately.
- **Correction suite** (SSTV #18 pattern, one shared row renderer):
  the discriminator stream for the current/last chart is retained
  (20 min cap ≈ 58 MB) and re-renders with SLANT (±2000 ppm) / PHASE
  (±250 ms) sliders, live while dragging and usable mid-reception.
  **Crop** top/bottom sliders + **rotation** (90° steps) apply to the
  processed preview and export (`ImageOps`, pure and unit-tested).
  Original stays untouched and auto-saves as before.
- **Metadata**: saved PNGs (auto + processed) carry a tEXt Description —
  profile, frequency, ISO timestamp, and correction values (slant,
  phase, inverted, rotation).
- Tests (7): round-trip fixture per profile (all four), inverted
  polarity (live emit + independent re-render polarity), zero-correction
  re-render vs live pipeline, ±5000 ppm clock error (corrected straight,
  uncorrected visibly leaning, both directions), +125 ms phase shift,
  crop/rotate transform units. Suite: 110 tests green.

## [4.40] — 2026-07-17

**Configurable, more resilient RTTY** (issue #20, 5/8 of the decoder
series — taken ahead of #19/#21 since FT4 is already user-surfaced).

- `RTTYConfig`: baud presets 45.45/50/75/100, shift presets
  170/200/425/850 Hz, adjustable mark tone (space = mark + shift),
  normal/**reverse** polarity, AFC on/off. Classic amateur RTTY
  (45.45/170 at 2125/2295) remains the default; last-used settings
  persist (`rttyBaud/Shift/Mark/Rev/AFC`). Detector bandwidth now
  tracks the baud rate. (No stop-bit setting: the UART re-arms on the
  next start edge rather than timing the stop — documented in code.)
- **Bounded AFC**: a two-stage wide discriminator path estimates the
  tone pair's absolute offset (residual of instantaneous frequency vs
  ±shift/2 around the nominal center) and slews a correction hard-
  clamped to ±min(shift/2 − 20, 100) Hz — it cannot chase adjacent
  signals; Recenter zeroes it. (Bug found during bring-up: one filter
  pole left enough mixing image to swing the estimator across zero and
  cancel the correction — the second pole fixed convergence.)
- **Baudot/ITA2 UART extracted** into `BaudotUART` (framing + LTRS/FIGS,
  explicit `bitSamples` input) — tone detection, symbol timing, and the
  character state machine are now separate per the issue.
- RTTY window: baud/shift pickers, mark stepper, REV/AFC toggles,
  Recenter, plus live mark/space tone lamps, a Q (tone-separation)
  meter, the AFC offset/bound readout, and the session acquisition
  state chip. Session details/confidence report the active config (#16).
- Tests (12): every baud + shift preset, custom mark, both polarities
  (incl. wrong-polarity negative), AFC pull-in at +40 Hz with readout
  accuracy, +150 Hz out-of-range not chased and clamp respected, AFC-off
  applies no correction, noise (~10 dB SNR) and 0.5 Hz fading fixtures,
  FIGS/CR/LF behavior, Q-meter sanity. (Test-encoder gotcha for the
  suite: "\r\n" is ONE Swift Character — encode by unicode scalar.)
  Suite: 104 tests green.

## [4.30] — 2026-07-17

**SSTV slant correction + re-rendering from retained history** (issue
#18, 3/8 of the decoder series).

- The decoder now retains the full discriminator stream for the
  current/last image (seeded with the ring tail as pre-roll, capped
  ~320 s ≈ 15 MB — enough for PD290), surviving image completion. The
  frame renderer was split so live decode and re-render share one pixel
  pipeline (`renderFrameInto`) — the only difference is where line
  starts come from: live = per-line sync tracking, re-render =
  deterministic linear timing from the user's slant/phase.
- **SLANT slider** (±2000 ppm sample-clock correction) and **PHASE
  slider** (±100 ms line-start offset) in the SSTV window re-render
  live while dragging (coalesced background renders, usable
  mid-reception on the partial capture). **Auto** resets to the slant
  estimated from the live sync tracker's accumulated drift; **Original**
  flips back to the as-received image (corrections are never
  destructive); **Save corrected** exports a second PNG alongside the
  auto-saved original, logged to the decoder session as a diagnostic.
- Manual mode + sync-hunt start (4.20) already covers damaged-VIS
  joins; combined with re-render, a mis-phased manual join can now be
  fixed after the fact instead of waiting for a retransmission.
- Tests: zero-correction re-render reproduces the live pipeline
  bit-for-tolerance; a +3000 ppm transmitter fixture pins the
  auto-estimate (±20%), proves the matching slant renders straight
  while the uncorrected render visibly leans; a +20 ms phase fixture
  pins shift direction and magnitude. Suite: 92 tests green.

## [4.20] — 2026-07-17

**SSTV: data-driven modes, Robot/PD families, manual override**
(issue #17, 2/8 of the decoder series). The decoder's mode table is now
pure data (`Mode` + a `ColorPlan` enum) interpreted by one generalized
frame renderer — nothing assumes 320×256 GBR anymore.

- New modes (9): **Scottie DX**, **Robot 36/72** (320×240 YCrCb; Robot
  36's alternating R-Y/B-Y chroma is selected by the separator tone,
  1500/2300 Hz, and rendered as row pairs), and **PD50/90/120/160/180/
  240/290** (YCrCb 4:2:0, two image rows per transmitted frame, up to
  800×616). Existing Martin M1/M2 + Scottie S1/S2 unchanged.
- YCrCb→RGB via the BT.601 relations (R/B straight off the tone scale,
  G reconstructed from luma weights); chroma scans sample at full image
  width over the half-length segment, so subsampled modes need no
  separate interpolation pass.
- **Manual override** (SSTV window): mode picker (Auto/VIS or a fixed
  mode) + "Start now" hunts the next line sync and decodes mid-
  transmission without a VIS header; MANUAL badge + "(manual)" status
  make auto vs. manual unambiguous. Back to Auto aborts a pending hunt.
- Session layer (#16): selected mode, per-frame progress against the
  known frame count, sync-hit confidence, and typed `unsupportedMode`
  failures for clean-parity unknown VIS codes all flow through the
  shared reporter.
- Tests: a generic SSTV encoder synthesizes full transmissions straight
  from the same mode table — **round-trip fixtures for all 14 modes**
  (VIS recognition, dimensions, line count, color reconstruction,
  duration), a published-transmission-time table check, ±500 ppm
  sample-clock-offset cases (GBR + YCrCb), and a manual-start-without-
  VIS fixture. Suite: 89 tests green.

## [4.10] — 2026-07-17

**Shared decoder session layer** (issue #16, 1/8 of the decoder series):
every digital decoder (FT8/FT4, SSTV, WEFAX, CW, RTTY) now narrates a
uniform lifecycle through a `DecoderStatusReporter`
(`DSP/DecoderStatus.swift`) — sessions move
acquiring → synchronized → decoding and end completed / failed /
cancelled, with failures typed (no signal, sync failure, unsupported
mode, insufficient samples, cancelled), progress, SNR/confidence,
diagnostics, and wall-clock bookmarks as the replay hook for the future
RF-time-machine integration (#22).

- Per decoder: SSTV sessions are per-image (VIS parity noise stays in
  session as a diagnostic; a clean-parity unknown VIS — Robot/PD — is a
  typed `unsupportedMode` failure; confidence = sync-pulse hit rate).
  WEFAX sessions are per-chart (`finishNow` on <5 lines →
  `insufficientSamples`; confidence = in-band fraction). CW/RTTY are
  per-enable-span, falling back to *acquiring* after 10 s without copy
  (CW reports envelope SNR, RTTY mark/space separation as confidence).
  FT8/FT4 cycle waiting → capturing (slot-fill progress) → decoding,
  posting per-slot results as diagnostics + bookmarks.
- **Decoder Activity window** (ECG icon in the decoder row): live state /
  progress / signal quality / last diagnostic per running decoder, plus
  a capped history of completed and failed decodes stamped with the RF
  frequency they were tuned to.
- 14 new unit tests pin the reporter state machine (event coalescing,
  begin-replaces-active, no-session no-ops) and drive real decoders
  end-to-end with synthesized audio: SSTV VIS sync + unsupported-VIS
  failure, WEFAX insufficient/complete, CW/RTTY decode-then-complete
  vs. silent-cancel.
- Decoder behavior itself is unchanged — the existing round-trip
  regression suite passes untouched.

## [4.02] — 2026-07-17

Clean radio stop on app quit/SIGTERM (`willTerminateNotification` →
`disconnect()`, queue-sync so RUN=0 is on the wire before exit). Found
the hard way: killing the app mid-connection left the ANAN reporting
"in use" to discovery — the connect sheet correctly greys busy radios,
so the radio was un-selectable until an out-of-band probe + HP RUN=0
released it (`tools/`-style recipe; the P1 HL2 self-recovers on EP2
silence, so only P2 radios stick).

## [4.01] — 2026-07-17

**Whole-codebase bug sweep** — four parallel review passes (TX stack,
protocol stack, RX DSP, app state/UI), every finding verified against
the code before fixing. 17 fixes, no behavior changes outside the bugs
themselves; docs refreshed (README to 4.00 state, CLAUDE.md, issue #13).

RX correctness across TX (extends the 3.52 freeze):
- Noise blanker no longer trains on our own TX signal while keyed
  (it was the one adaptive stage missing from the freeze — real static
  crashes passed unblanked for ~0.5 s after unkey); reset at unkey.
- Squelch/overload gate decision idles while keyed (own signal forced
  the overload mute / pinned the squelch open into the first post-unkey
  window); accumulators cleared at unkey.
- Spectral NR keeps its (valid, pre-key) noise floor across unkey
  instead of reseeding from the first post-unkey frame — reseeding
  treated whatever station was present as noise and max-cut it for ~1 s.
- AGC reset now clears the hang-decay flag (stale flag picked the wrong
  release τ once after unkey). Sub-RX enabled mid-key now starts frozen.

TX interlocks:
- TUNE / 2 TONE can no longer hijack a live voice over (clicking TUNE
  mid-PTT silently replaced speech with a steady carrier, and toggling
  off dropped the whole over); exclusion is now model-level, not just
  button-disable.
- A mode change with MOX up (CAT `M CW` mid-over → continuous dead
  carrier at full drive) now drops MOX first.
- Disarming mid-over no longer unwires the modulator at +30 ms while
  MOX rides out a roger-beep tail (up to 1.5 s of keyed silence, beep
  cut); the unwire now waits out the same tail.
- Stale unkey-tail timers are generation-guarded — a quick unkey/re-key/
  unkey cycle could drop MOX mid-way through the second over's beep.

Protocol robustness:
- P2 bring-up continuations are generation-guarded: two stream restarts
  within ~200 ms could interleave two half-finished bring-up chains,
  landing a DUC-specific mid-RUN (the documented never-safe packet).
- P2 key-down orders the upsampler reset/credit prime BEFORE the keyed
  flag is visible to the mic handler (a mic datagram in the ~µs gap
  transmitted the previous over's filter state with stale credit).
- P2 wideband parser requires exact datagram length — one oversized or
  odd-length packet from the radio's IP crashed the app.
- P1 stop/disconnect while keyed now fires onTXForceUnkey like P2 (the
  keyed lamp and RX mute no longer latch against an unkeyed radio).
- UDPSocket fd teardown is queue-confined (data race with send/drain).

State/UI:
- Connecting to a different radio family no longer overwrites the
  current band's memory via the RF-gain clamp, and band-hopping while
  DISCONNECTED no longer grinds HL2 LNA memories through the previous
  radio's ANAN range.
- Rack sliders retune units in place (state carried across coefficient
  rebuilds) — dragging Leveler/Warmth while armed was resetting
  envelopes every tick, audible as pumping/clicks. Biquad gained a
  state accessor for this.
- Custom-profile EQ arrays are length-normalized on apply (index-crash
  surface); restored mic channel clamps to the present device's count;
  stale UNDERRUN warning clears on disarm; audio-output device picks
  reset the restart-retry budget (a depleted budget left RX audio
  permanently dead after repeated device-swap failures).
- Defensive length guards in IQHistoryRing.write / SpectrumAnalyzer.feed.

## [4.00] — 2026-07-17

**TX audio chain map + snap-in rack** (version rollover from 3.90 —
next feature increment, not a milestone claim). Still no keying this
session; ear checks added to the issue #13 dummy-load list.

- **TX Audio Chain window** (flowchart button in TX Controls, next to
  the meters gauge): a live mic-to-antenna map of every processing
  stage — green = fixed architecture, orange = enabled option, dim =
  bypassed — each with its current settings (profile edges, gate
  threshold, comp topology/ratio, FX, CESSB, Optimod asymmetry when
  active) and live gain-reduction readouts on the compressor/limiter
  rows while armed.
- **Snap-in rack** (managed inside the chain map, persisted as
  `txRack`): ordered character units inserted between the compressor
  and FX — **Tilt EQ** (±6 dB dark↔bright, center flat), **Warmth**
  (low shelf + gentle saturation), **Exciter** (mid-band harmonics →
  sparkle), **Leveler** (slow ±9 dB RMS ride toward −14 dBFS),
  **Density** (tanh loudness at bounded peak). Add / reorder / blend /
  remove; amount 0 is exact bypass. Saturating units are band-safe by
  architecture — the post-limiter bandpass cleans up — pinned by a
  fully-loaded-rack containment test (68 tests total).
- **Fixed: high-shelf EQ biquad** — a sign slip in the RBJ b2
  coefficient (present since the shelf EQ shipped in 2.10) made every
  profile with a high-shelf gain also cut lows it should have left
  alone (≈ −3 dB at 100 Hz for a +3 dB shelf) and overshoot its top
  gain. Found while pinning the new Tilt unit; now regression-tested.
  ESSB Wide / Broadcast / Hi-Fi AM / Top 40 / Optimod voicings all
  shift subtly (more correct lows) — worth an ear pass on the load.

## [3.90] — 2026-07-17

**"Optimod AM Broadcast" TX profile** — the big-city AM air-chain
sound, and the first profile that changes modulator behavior rather
than just voicing (still awaiting dummy-load validation, keying was
off-limits again this session):

- Voicing: NRSC-ish 50–9500 Hz, +6 dB bass shelf, +3 presence, +4 top
  shelf standing in for NRSC pre-emphasis, dense 5:1 leveling with
  +12 dB makeup so program material genuinely drives the peak limiter
  (that "always loud" density is the point — pair with Comp: 3-band).
  19 kHz occupied bandwidth: dummy-load / clear-channel etiquette.
- **Asymmetric positive peak control** (the Optimod signature, AM mode
  only): a new `TXProfile.amPositivePeak` field (1.25 here, 1.0 =
  symmetric everywhere else) gives the lookahead limiter a per-polarity
  ceiling, and a polarity follower in TXChain orients speech so its
  naturally bigger peaks point positive — flips only at zero crossings,
  inaudible. Positive modulation rides to ~125% relative while
  negatives never pass 95%: louder AM with zero carrier pinch-off, peak
  envelope ≈ 0.98 full scale. Limiting stays pure gain (no clipper),
  so the 3.80 band-containment guarantees hold.
- Tests (61 total): asymmetric-ceiling unit test, plus an end-to-end
  burst-speech AM test pinning >100% positive modulation on the Optimod
  profile, no carrier pinch-off, and the symmetric cap on Hi-Fi AM.

## [3.80] — 2026-07-17

**SSB transmit audio quality batch** (issue #13) — five upgrades to the
TX voice chain. DSP validated by 11 new regression tests (59 total);
on-air character unchanged until the new toggles are enabled — except
the limiter change, which is always on because it fixes a real
splatter path. **Dummy-load A/B still pending (no keying this
session).**

- **Lookahead peak limiter** replaces the hard ±0.95 clipper. True-peak,
  provably no overshoot (sliding-min + moving-average gain over a
  2.5 ms lookahead), bit-transparent below the ceiling — and a second
  bandpass pass after it keeps limiter products inside the profile
  edges. The old clipper ran *after* the bandpass, so its harmonics
  went straight to the modulator: heavy compression could splatter.
  Pinned by an end-to-end hard-drive test (≥ 40 dB band containment).
- **Phase rotator** (always on): four cascaded allpasses through the
  low mids symmetrize the speech waveform — the classic broadcast
  trick, worth 1–2 dB of limiter headroom, magnitude-flat by test.
- **Noise gate** (downward expander, −80…−30 dB threshold slider) —
  stops compression makeup gain from transmitting the shack noise
  floor between words. **De-esser** (0–12 dB slider): broadband duck
  driven by a 5 kHz-sidechain dominance detector, so it tracks any
  mic-gain setting; vowels measurably untouched.
- **CESSB** (checkbox, default off — Hershberger W9GR, QEX 2014): the
  transmitted SSB envelope √(I²+Q²) overshoots the audio-domain
  limiter up to ~2× after the Hilbert transform; this clips the
  analytic *envelope*, re-filters with a complex bandpass on the
  profile edges (twice), and final-trims. Envelope provably ≤ 0.95,
  out-of-band products ≥ 40 dB down, ~2–3 dB more average talk power
  at the same PEP. Worth A/B-ing on the dummy load first.
- **3-band compressor** (Comp: Single/3-band): Linkwitz-Riley splits at
  500 Hz / 2.5 kHz, per-band time constants, profile threshold/ratio —
  a bass syllable no longer ducks the presence range (pinned: quiet
  3.5 kHz tone moves < 2 dB while a loud 200 Hz tone compresses 4+ dB).
- **2 TONE button** (next to TUNE): keys the classic 700 + 1900 Hz
  equal-amplitude IMD pair, synthesized as clean complex exponentials
  in pull() — any IMD you see on a monitor RX is the transmitter's.
  Same interlocks as TUNE; mutually exclusive with it.

New settings persist (`txGate`, `txGateThresh`, `txDeEss`,
`txDeEssAmt`, `txMultiband`, `txCESSB`); the meters window's LIMITER
lamp now reads the true lookahead-limiter gain reduction.

## [3.71] — 2026-07-17

Documentation refresh — README brought from 3.30 to 3.70 state
(diversity RX, the 19-effect FX shelf, TX Meters window, mic channel
picker, audio self-healing, updated roadmap/troubleshooting/test
count), CLAUDE.md TX section updated (effects + post-FX bandpass, meter
snapshot/scope plumbing, TX-keyed RX freeze, MicInput channel
extraction + watchdog) and a new gotcha entry for the AVAudioEngine
silent-death pattern with its diagnosis recipe.

## [3.70] — 2026-07-17

**TX Meters window** — floating transmit diagnostics (gauge button in
the TX Controls header; the S-meter stays on the main window):

- **Modulation scope**: scrolling 3 s pre-limiter voice envelope at
  200 bins/s. Green target zone (peaks 0.35–0.95 of full drive), red
  limiter line — peaks crossing it are being flattened and draw red.
  A mic-technique coach reads the last second of peaks: "CLOSER TO THE
  MIC / MORE GAIN" → "GOOD" → "BACK OFF — FLAT-TOPPING".
- **Warning lamps**: MIC CLIP (interface ADC hit full scale — hardware
  preamp problem, latched ~0.7 s), FLAT TOP (limiter shaving > 1.5 dB),
  OVERDRIVE (ALC pinned > 8 dB for a second), UNDERRUN (existing
  counter).
- **Audio meters**: MIC IN (raw device level *before* mic gain — true
  gain staging, 40 dB/s fall), SPEECH (processed voice), COMP and
  LIMITER (split out of the combined ALC with the same 20 dB/s hold
  decay), ALC (classic combined, tick at 6 dB).
- **RF meters**: PWR (full scale auto-picks 10 W HL2 / 100 W ANAN),
  SWR bar (red past 3 — the force-unkey threshold), TEMP / PA A /
  FWD V / REV V readouts.
- Plumbing: `TXChain.meterSnapshot()` (one coherent locked read) +
  `drainScope()` (5 ms abs-max envelope bins, capped ring); the TX
  meter timer now runs 30 Hz while armed. All pinned by a regression
  test (raw level, comp/limiter split, ALC sum, pre-limiter scope
  peaks, drain semantics).

## [3.62] — 2026-07-17

**Fixed TX mic silence on multichannel interfaces + mic channel picker.**
The real root cause of "no TX audio" on the MOTU M4 (3.61's watchdog was
necessary but not sufficient — blocks were flowing, they were just
silent): with the M4 presenting 4 input channels and no readable channel
layout (CoreAudio −10877), `AVAudioConverter`'s 4→1 downmix emits
**all-zero output with no error** — measured live with a standalone
probe (channel 1 carried signal at −56 dBFS; converted mono was exactly
0.0).

- MicInput now extracts ONE channel by hand from the deinterleaved tap
  buffer and gives the converter a mono→mono (rate-only) job. Verified
  against the live M4: extracted channel 1 converts to real audio where
  the downmix produced zeros.
- New "Ch N" picker beside the mic device picker (shown only when the
  device has >1 input channel; persisted `micChan`, 1-based). Takes
  effect live — the tap reads it per block. Switching mic device snaps
  the channel back to 1.

## [3.61] — 2026-07-17

**Fixed TX mic capture dying silently** (root-caused live: mic engine
running, HAL input active, zero blocks reaching TXChain):

- Selecting a non-default mic rebuilds the system input aggregate
  ~100 ms *after* the engine starts (observed: MOTU M4 aggregate going
  4-channel); the io-unit config change that follows can leave the tap's
  `AVAudioConverter` with a stale format, and its error guard dropped
  every block with **no log** — meter dead, monitor dead, nothing to
  modulate.
- MicInput now runs a delivery watchdog: if capture should be running
  and no block has arrived for >1 s, it tears down and rebuilds the
  engine (fresh format query heals any flavor of silent death — config
  change, device unplug, failed earlier start), retrying ~1/s while
  armed and logging each rebuild. Restart-on-notification was rejected:
  every mic start posts a config change here, which would loop.
- Converter errors now log (once per start) instead of vanishing.

## [3.60] — 2026-07-16

**The weird FX shelf** — 11 new TX voice effects joining the classic
reverb/echo family. All causal per-sample DSP: zero added stream latency
(the spectrum-benders pay one extra 513-tap bandpass ≈ 5 ms, nothing
else changes). Existing FX intensity slider drives them all (wet-replace
effects crossfade dry→wet).

- **Jet Flanger** (0.7–7.3 ms swept comb with feedback), **Phaser**
  (6 swept first-order allpasses, 250 Hz–2.8 kHz exponential sweep,
  0.55 feedback), **Space Echo** (330 ms tape echo, ±8 ms wobble at
  0.9 Hz, repeats darken through a 2 kHz one-pole each round trip),
  **Underwater** (±6% vibrato at 4.5 Hz + 1.1 kHz muffle),
  **Helicopter** (13 Hz cubed-raised-cosine rotor chop).
- **Dalek** (30 Hz sine ring mod), **Toy Robot** (50 Hz square ring mod
  into a 6 ms metallic feedback comb), **Chipmunk / Giant** (granular
  dual-tap pitch shift ×1.35 / ×0.72, 30 ms window, sin² crossfade),
  **Alien** (true Bode frequency shifter: Niemitalo IIR Hilbert pair +
  quadrature oscillator, +90 Hz, 49 dB image rejection — measured),
  **8-Bit** (6-bit quantize at a 6 kHz sample-hold).
- Spectrum-bending effects (`TXEffect.bendsSpectrum`) re-run the profile
  bandpass after the effect so ring-mod sidebands, shifted formants, and
  crush harmonics can't leave the transmitted channel — pinned by test
  (5/7 kHz crush harmonics ≥40 dB under the voice at the monitor tap).
- Tests: Alien shifts 1 kHz → exactly 1.09 kHz with image and residual
  buried (catches a swapped Hilbert pairing), Chipmunk moves 400 Hz →
  540 Hz with the original gone, crush containment as above.

## [3.52] — 2026-07-16

**Fixed RX audio taking seconds to come back after PTT release.** Two
things stacked: the roger-beep unkey tail intentionally holds the mute
while the beep transmits (~1.2 s with a 1 s beep — pick Beep "Off" if you
want instant turnaround), but on top of that the RX chain kept
demodulating our own transmit signal all through the over, clamping the
WCPAGC to minimum gain; after unmute it crawled back 40–60 dB at
tauDecay (1.5–2 s on Med, worse on Slow), so band audio faded in from
silence.

- RXChain now freezes its adaptive post-detector stages (auto-notch, NR,
  EQ, AGC) while TX is keyed — our own signal can no longer train them
  (the LMS auto-notch was also learning the roger beep's tones) — and
  resets them at unkey, so full AGC gain is back the instant the mute
  lifts. The 4 ms look-ahead attack still catches strong signals without
  a pop. Driven from every mute transition (key, unkey tail, watchdog
  force-unkey) on both the main and sub-RX chains; spectrum/waterfall
  still show the own-signal picture during TX.
- Regression test: two chains hear quiet tone → 39 dB "own signal" →
  quiet tone; the TX-aware one must be at target level 50 ms after
  unkey while the control is still clamped.

## [3.51] — 2026-07-16

**Fixed RX audio dying silently when AVAudioEngine self-stops** (root-caused
from the unified log of a live failure):

- macOS stops the audio engine on an output-unit configuration change —
  including the one our own preferred-device swap triggers during connect
  bring-up when the saved device's format differs from the system default
  (observed: default stereo → built-in Mac mini speaker, mono; the engine
  self-stopped 50 ms after start). `AudioOutput` never observed
  `AVAudioEngineConfigurationChange`, so audio stayed dead for the rest of
  the session while the DSP kept filling the ring (the every-2 s overrun
  log was the tell).
- Worse, picking a different output device couldn't recover: the device
  setter only restarted the engine `if engine.isRunning`. Both fixed —
  `AudioOutput` now tracks intent (`shouldBeRunning`), restarts on the
  config-change notification, restarts on device selection whenever audio
  *should* be playing, and retries a failed start up to 5× at 0.5 s (the
  notification can beat the device's readiness). Restart failures are
  logged instead of swallowed (`try? engine.start()` hid them before).

## [3.50] — 2026-07-16

**Diversity RX on the ANAN (issue #12)** — dual-ADC combining on the
Orion MkII's phase-synchronous LTC2208 pair, live-validated same day on
fw 2.2.10 (framing + app end-to-end; the two-antenna null hunt awaits a
second antenna on the RX2 jack):

- Protocol: diversity enables DDC0 only (ADC0) with DDC1 (ADC1) synced
  via DDC-Specific byte 1363 = 0x02 — interleaved sample pairs arrive on
  DDC0's port 1035 and are combined per-packet as out = A + w·B with a
  complex weight. Mid-RUN switch both ways measured clean (zero seq
  errors, no stream restart). Alex1 carries ADC1's BPF relay bits, the
  ADC1 step attenuator mirrors ADC0's, and RX-time packets stay
  byte-identical to the validated milestones while diversity is off.
- UI: Diversity section in the gear popover (P2 only) — enable toggle +
  Thetis-style polar steering pad (drag: radius = gain 0–2, angle =
  phase; double-click resets 1∠0°) with live gain/phase readouts.
  Mutually exclusive with SUB (both spend the second signal path).
  Persisted (`divOn`/`divGain`/`divPhase`).
- Spec OPEN #4 resolved by measurement (tools/p2_diversity_test.py):
  samples-per-frame field counts TOTAL samples (238 = 119 pairs, DDC0
  first); the spec's "×164" example is wrong. Also learned: the firmware
  ignores C&C from a client it hasn't seen a discovery probe from — the
  harness lore is now in the spec notes.

## [3.41] — 2026-07-16

CAT bugfixes (reproduced and verified live against the running server)
plus regression tests for the 3.40 features:

- **Fixed the rigctl `F`+`M` batch quirk** (was in the known-bugs list):
  `set_mode` never wrote the optimistic state mirror that `set_freq` and
  `set_ptt` already had, so a hamlib client that set-then-verified in one
  batch read the STALE mode back and treated the set as failed. The
  mirror now updates immediately; RadioState pushes the canonical truth
  right back (normalizing aliases like PKTUSB→USB, restoring the real
  mode if the requested name doesn't map).
- **Fixed dropped replies on batched `q`**: a quit at the end of a
  command batch cancelled the connection while earlier replies were
  still queued — the batch's replies now flush in one send before close.
- New DSP tests: FX intensity wet-mix scaling (0×/1×/2× + carry across
  effect swaps), Top 40 FM Announcer voicing (width/warmth/compression
  density), ALC meter rise and 20 dB/s decay. 43 tests total.

## [3.40] — 2026-07-16

TX audio rack additions (both mics verified working this session):

- **FX intensity slider** (TX Controls, under the FX picker): scales the
  selected effect's wet mix 0–200% (100% = the effect's designed level).
  Feedback/decay are untouched, so echoes and reverbs stay stable at any
  setting. Persisted (`txFXIntensity`) and snapshotted into custom
  profiles (older saved profiles load at 100%).
- **New "Top 40 FM Announcer ESSB" profile**: FM-air-chain voice
  processing translated to 80–4000 Hz ESSB — +5 dB low-shelf warmth,
  +4 dB forward mids at 2.2 kHz, the top shelf eased −1 dB to stay warm
  rather than sibilant, and dense 5:1 compression (−20 dBFS threshold,
  +7 dB makeup) for the always-loud, never-peaky announcer sound.
- **ALC meter** (TX Controls, under the mic meter): live compressor +
  soft-limiter gain reduction in dB, peak-held with a 20 dB/s decay,
  0–20 dB scale with a tick at the 6 dB healthy-peak mark. Runs whenever
  the mic does (armed, keyed or not) — dial in mic gain off-air.
- Mic/ALC/underrun meters now poll at 10 Hz while armed (own timer)
  instead of riding the 1 Hz stats tick — the mic meter finally moves
  like a meter.

## [3.31] — 2026-07-16

Documentation refresh, no code changes:

- README brought from the 2.60 era to 3.30: ANAN transmit, bandscope,
  1536 kHz rates, antenna matrix, roger beeps, updated architecture
  diagram/key files/roadmap, ANAN power-cal troubleshooting note.
- docs/Protocol2-Spec-Notes.md annotated with everything measured on
  hardware this cycle: the Alex relay latch rule (HP stores, General
  drives), the validated TX recipe, PA-enable honored on fw 2.2.10,
  exact mic-stream pacing, TX IQ wire sense, board-5 power fit
  (P ≈ V²/0.28 measured vs the board-4 0.12), the drive/PA saturation
  curve, and TX INHIBIT polarity — with the pre-hardware notes kept
  for reference and OPEN item #2 partially resolved.

## [3.30] — 2026-07-16

**Roger beeps** — a Beep picker in TX Controls with a 16-entry portfolio
(Off, the traditionalists' Classic, and 14 deliberately weird ones: Wolf
Whistle, Morse 73, DTMF 73, Droid, Dial-Up, Laser, Power-Up, Sonar,
Bloop, Geiger, Theremin, Whale, Meep Meep, Sci-Fi). All ≤ 1 s,
deterministic renders, click-free edges — pinned by test.

- The beep transmits *after* the over: on PTT release the ring's voice
  tail gets a 10 ms fade in place, then a 5 ms gap, then the beep — and
  MOX is now held until the whole tail drains (previously a fixed 20 ms;
  live-checked on the dummy load: S-meter shows the whistle going out
  after the PTT lamp clears, then a clean unkey).
- Beeps are band-limited by the live TX profile bandpass *before*
  modulation, so square-wave/chirp content stays inside the transmitted
  passband; AM overs ramp the carrier around the beep.
- Voice modes only — CW and TUNE never beep; leave Off for digital
  modes. The monitor plays your beep too. RX stays muted until MOX
  actually drops (you'd otherwise hear your own beep come back through
  the receiver).
- Persisted as `rogerBeep`; default Off.

**ANAN transmit LIVE-VALIDATED on the dummy load** — first-ever P2 keying
worked on the first try (drive 10/255 → 0.5 W, SWR 1.00–1.04, zero
sequence errors through key → TX → unkey). Full session: sideband sense
confirmed both ways from the radio's own RX (USB tone at +700 Hz, 80 dB
over the −700 Hz image; LSB the mirror), PA-enable bit confirmed honored
by fw 2.2.10 (keying with it clear = 0.01 V forward — a real hardware
interlock), drive sweep mapped the PA's compression knee, in-app
ARM → TUNE → PTT voice overs all clean.

- **TX pinned to ANT1** while keyed regardless of the RX antenna
  selection — that's where the dummy load (and later the TX antenna)
  lives; a TX antenna picker is future work.
- **PA protection**, using the ANAN's fast TX telemetry (~1 ms status
  cadence): sustained SWR > 3 at real power force-unkeys in ~100 ms,
  and the rear-panel TX INHIBIT input (IO5, polarity measured on this
  unit) unkeys in ~3 ms.
- **Drive scale calibrated to the measured PA curve**: forward volts rise
  linearly to register ~80 then flat-top (the PA saturates near 80 on
  the current supply — the rail sags 13.3 → 11.4 V at 9 A), so the UI's
  0–100% now maps onto 0–80: full slider ≈ the PA's clean maximum
  (~60 W estimated), and the top fifth of the old range — pure
  distortion — is unreachable.
- **Power cal corrected**: pihpsdr's k = 0.12 over-read ~2.3× against DC
  input power (4.06 V read "137 W" while the PA drew 97 W DC); default
  is now the current-derived k = 0.28. Still an estimate — trim against
  a real wattmeter via PWR CAL when one is available.
- **TX audio underrun fixed** (found live: 23–89 ms of zero-padding per
  voice over): AVAudioEngine delivers mic taps at whatever block size it
  likes — ~4800 samples (100 ms!) on the MOTU M4, not the requested
  512 — and the TX ring couldn't survive a full inter-block gap.
  TXChain now pre-fills one observed mic-block plus margin of silence at
  key-down (under the still-zero key envelope; no monitor latency, one
  block of on-air voice latency). Underrun accounting now keys off real
  fed audio, not ring delivery.
- tools/p2_tx_test.py grew the measurement kit: own-signal sideband
  check, PA current/supply readout, mic-packet rate, --pa-off-test.

## [3.10] — 2026-07-16

**Protocol 2 transmit for the ANAN** — the full TX stack (mic → TXChain
voicing rack → modulator) now drives the 7000DLE's DUC. Code-complete
and regression-tested, **not yet keyed on hardware**: first RF happens
into a dummy load with the user present (tools/p2_tx_test.py is the
clean-room prototype for that session).

- Keying is a single high-priority packet (PTT bit, drive, Alex T/R) —
  P2 has no NCO-slaving, so no preload phase; the Alex change fires the
  proven General relay latch, which now also carries the PA-enable bit.
  PA-enable, T/R, drive, and the 31 dB RX-protection attenuators are all
  gated on the keyed state, so **RX-time packets stay byte-identical to
  the live-validated 3.01 stream** (only the bring-up DUC-Specific gains
  its inert TX config: TX attenuation 31/31, radio mic-jack PTT
  disabled).
- TX IQ: 240×24-bit pairs at the DUC's fixed 192 kHz (port 1029), paced
  off the radio's own 48 kHz mic stream (64-sample credit per mic packet
  → exactly 800 pkt/s), primed with a ~6 ms send-ahead cushion. The
  TXChain's 48 kHz output is ×4-interpolated by a new 191-tap
  `TXUpsampler` (unity passband, stuffing images ≥60 dB down — pinned by
  a new DSP test).
- Receive keeps running while keyed (the P2 RX NCO is independent):
  waterfall shows your own signal, audio muted, front end at full
  attenuation. Stream-watchdog restarts and stop/disconnect force-unkey
  and reconcile the PTT lamp.
- Telemetry: forward/reverse watts through the ANAN detector fit
  (P = V²/k, k = 0.12 presumptive — PWR CAL popover now calibrates
  per-radio, persisted separately from the HL2's), REV pre-scaled so the
  SWR matches pihpsdr's power-based math; TEMP shows a dash (no sensor
  in the P2 status packet).
- TX frequency clamp is now per-radio (30 MHz HL2 / 54 MHz ANAN — 6 m
  transmit is representable).

## [3.01] — 2026-07-16

**Bandscope live-validated on the ANAN** (fw 2.2.10) and tuned:

- Clean-room probe + in-app test confirmed: wideband packets flow,
  sequences run 0–31 resetting per frame (spec OPEN #5 resolved),
  samples are big-endian signed, and click-to-tune retunes the VFO
  with the main display following.
- dB scale recalibrated to measured raw-ADC levels (per-bin noise
  ~−90 dBFS, carriers −60…−40): floor −100, ceiling −30.
- New in-window hint: the raw ADC sits behind the Alex preselector, so
  with a band BPF engaged the bandscope mostly shows the current band —
  the hint points at the 2.80 "Bypass RX bandpass filters" toggle for a
  true full-span view. (The preselector's passband is plainly visible
  as the energy hump moving when you change bands — a nice live view of
  the Alex relays doing their job.)

## [3.00] — 2026-07-16

**Wideband bandscope** — the entire 0–61.44 MHz HF spectrum in one
window (ANAN/Protocol 2 only; a feature Thetis has and pihpsdr never
implemented):

- New **Bandscope window** (button in the settings popover's ANAN
  section): full-span spectrum + waterfall built from the radio's raw
  16-bit ADC snapshots (16384 samples every 20 ms → 8192 bins at
  7.5 kHz, max-held to 2048 for the display). Amateur bands are shaded
  and labeled straight from the band presets; click anywhere to take
  the VFO there.
- Wideband streaming is enabled via General bytes 23–28 only while the
  window is open (~400 KB/s extra), and rides the measured-safe mid-RUN
  General resend.
- Frame assembly is agnostic to the spec's ambiguous wideband sequence
  semantics (OPEN #5): any 32 consecutive sequence numbers form a
  frame, correct under both readings.
- New DSP test pins the bandscope FFT's bin mapping, dB reference, and
  max-hold decimation. **Live validation pending** (radio was in use):
  first-packet arrival, sequence semantics, and sample endianness are
  spec-derived — see the checklist in issue #11.

## [2.90] — 2026-07-16

**768 k / 1536 k sample rates on the ANAN** — up to 4× the HL2's
maximum span:

- The rate picker is now bounded by the connected radio's hardware
  (`HPSDRLink.maxSampleRate`): 48–384 k on the HL2/SquareSDR, 48–1536 k
  on Protocol 2. A persisted or recorded high rate still shows before a
  radio narrows the list; connecting an HL2 with a 768/1536 k
  preference clamps it to 384 k (same pattern as the RF-gain range).
- The P1 stack hard-clamps to 384 k defensively (its 2-bit EP2 speed
  field can't express more).
- RF time machine at high rates keeps its ~553 MB ceiling by halving
  the window per octave: 180 s up to 384 k, 90 s at 768 k, 45 s at
  1536 k.
- UDP receive buffer doubled to 4 MB (~9.3 MB/s at 1536 k).
- New DSP regression test pins the seven-stage decimation cascade at
  1536 k (clean USB tone, correct pitch, droop comp holding amplitude).

## [2.80] — 2026-07-16

**ANAN hardware batch 2** — the settings popover's ANAN section grows:

- **ADC dither and random** toggles (LTC2208 linearization: dither
  breaks up correlation spurs, random decorrelates bus noise). Applied
  live via a mid-RUN DDC-Specific resend — measured safe on fw 2.2.10
  (zero IQ sequence errors across repeated resends with the bits
  toggling; the fw 2.1.18 "never resend mid-RUN" rule does not apply
  on current firmware).
- **RX bandpass-filter bypass** — route around the Alex preselector
  for wideband listening or an external filter/preamp chain (the
  bit-12 path pihpsdr uses).
- **6 m preamp control** — the auto-engaged >35 MHz preamp can now be
  disabled (falls back to the bypass path).
- All four settings persist; they push to the radio on connect and
  switch live thanks to the 2.71 Alex General-latch fix.

## [2.71] — 2026-07-16

**Fix: ANAN Alex relays now actually switch mid-stream.** Orion MkII
firmware stores the High-Priority Alex word but only drives the relays
when a General packet arrives — so 2.70's antenna picker (and 2.60's
band-following BPF preselector selection) silently never moved the
hardware while streaming; de-energized relays default to ANT1, which
masked it. Root-caused with a clean-room packet prototype against fw
2.2.10: a mid-RUN antenna change via HP alone did nothing; the same
change followed by one General packet switched the relay (−20 dB on an
empty jack) with **zero** IQ sequence errors. The connection now sends
a single General whenever the computed Alex word changes (antenna
picker, or the VFO crossing a BPF/LPF boundary). On fw ≤2.1.18 that
one-shot resend costs its known ~200 ms IQ stall — same class as a
retune, only on explicit changes.

## [2.70] — 2026-07-16

**ANAN RX antenna selection** — the first radio-specific settings GUI:

- **RX antenna picker** in the settings (gear) popover: ANT1 / ANT2 /
  ANT3 / EXT1 / XVTR / BYPS on the ANAN's Alex antenna matrix. EXT1 and
  XVTR route through the "Rx Master in Sel." relay (Alex0 bit 14 + bits
  9/8), BYPS takes the filter-bypass input (bit 11), per pihpsdr's
  ORION2 cases. Switches live via the 100 ms high-priority packet — no
  stream restart.
- **Dynamic per-radio settings**: the section only renders while the
  connected radio reports the capability (`supportsRXAntenna` on
  `HPSDRLink`) — HL2/SquareSDR sessions never see ANAN controls. This
  is the pattern for future ANAN-only settings (dither/random, BPF
  bypass, high sample rates, OC outputs).
- The selection is persisted and **remembered per band** alongside
  freq/mode/filter/LNA/ATT in the band memory.

## [2.60] — 2026-07-16

**Apache Labs ANAN support — openHPSDR Protocol 2 (RX)**, validated live
against an ANAN-7000DLE MK2 (Orion MkII, fw 2.1.18, protocol v3.9):

- **Dual-protocol discovery**: the connect sheet now probes P1 and P2
  simultaneously and lists both radio families (the ANAN shows its P2
  firmware version and MAC; a busy radio is flagged IN USE).
- **`HPSDRProtocol2Connection`**: the full P2 network layer — single
  socket demuxed by source port, General/DDC-specific/DUC-specific/
  High-Priority packet builders, NCO phase words, 100 ms high-priority
  keepalive (the radio safes itself if C&C goes silent >1 s), IQ
  watchdog with automatic stream restart, per-stream sequence tracking,
  and 24-bit/238-sample IQ unpacking into the existing RX chain. Byte
  maps derived from the openHPSDR v3.8/v4.4 spec + pihpsdr and archived
  in `docs/Protocol2-*.md`.
- **Alex filter control**: RX band-pass and TX low-pass relays follow
  the VFO (ANAN-7000 "MkII 5.2" bit map), antenna 1 fixed for now.
- **Step attenuator**: on P2 radios the RF-gain slider becomes the
  0…−31 dB hardware step attenuator (shared S-meter math, per-band
  memory, Auto backoff all work unchanged); connect-time clamping maps
  saved HL2 LNA values onto the legal ANAN range and back.
- **RX-only for now**: the TX banner hides on a P2 connection and
  arming is refused — ANAN transmit is a separate, gated milestone.
- Both connection stacks now sit behind a common `HPSDRLink` protocol;
  the HL2/P1 path is unchanged.

## [2.50] — 2026-07-14

The TX polish batch:

- **CW transmit**: CW mode keys a clean carrier at the dial frequency
  (envelope-shaped, no clicks; the mic never modulates it). The PTT
  button or CAT `T` is the key, so external keyer/logging software can
  send CW today. Verified live: a single narrow column exactly on the
  VFO line. Full iambic keyer/paddle support remains future work.
- **Transmit SWR meter**: a color-coded SWR strip under the S-meter
  (green < 1.5 → red ≥ 2.5, 1–3 scale), lit while keyed, dim when idle.
  Read 1.1 on the dummy load, matching the TX-window telemetry.
- **Watts calibration UI** (PWR CAL… under the telemetry row): key TUNE
  into a known meter, enter the true watts, and k = FWD²/W applies
  immediately and persists — no more `defaults write` + relaunch.
- **TX underrun counter**: keyed zero-fill (mic delivery stalls) is
  counted per over and surfaced as an orange warning row. The intrinsic
  key-down fill gap (~10 ms while the first mic block is in flight) is
  excluded — the instrumentation itself found that gap on its first
  live over. A clean speech over now shows nothing.
- No key-down soak test by design — the PA wasn't stress-tested beyond
  the usual brief validation keys.

## [2.40] — 2026-07-14

- **Voice check** (Check row in the TX window): record up to 10 s of
  your voice EXACTLY as it would be transmitted — profile bandpass, EQ,
  compression, and FX all applied — then play it back off-air to catch
  mic problems or judge EQ moves. Nothing is keyed; recording just needs
  ARM (the mic only runs armed). Playback runs at the full 48 kHz
  through the app's selected output device, so even the lab profiles
  play back at full width (unlike the 12 kHz live monitor). Rec
  auto-stops at 10 s and on disarm; the transport resets itself when
  the clip ends. Validated by capturing the app's output through
  BlackHole during playback with nobody speaking: the recorded phrase
  came back with 13 dB of speech-band dominance.

## [2.30] — 2026-07-14

- **Lab profiles** (dummy-load experiments only — the blurbs say so):
  **Mega-ESSB** (20–12,000 Hz SSB) and **Mega-Fidelity AM** (20–16,000 Hz
  full-carrier AM, ±16 kHz RF). Verified on the air: Mega-ESSB speech
  occupies the full 12 kHz above the carrier on the peak-hold trace.
  The 12 kHz monitor path reproduces them only to ~5 kHz; the RF is the
  full width.
- **Multiband TX EQ**: eight octave faders (63 Hz–8 kHz, ±12 dB, 0.5 dB
  detents, double-click to zero, Flat button) in the TX window — applied
  after the profile voicing, before compression, live while transmitting.
- **Custom profiles**: Save… snapshots the current voicing base + EQ
  curve + FX under your name (★ in the picker, trash to delete);
  selecting one restores all three. Survives relaunch — verified live
  (saved "Lab Wide" = Mega-ESSB + 4 kHz boost + Hall Reverb, quit,
  relaunched, everything came back selected).
- New regression tests: Mega-ESSB passes 9 kHz that ESSB Wide crushes,
  Mega-Fidelity AM puts symmetric sidebands at ±14 kHz, and a +12 dB
  EQ band boost lifts a tone by 12 dB — 33 tests green.

## [2.20] — 2026-07-14

- **TX monitor (sidetone)**: hear your own processed voice — profile,
  EQ, compression, FX included — while armed, keyed or not, so you can
  dial in ESSB or a reverb without radiating a watt. Toggle + level in
  the TX window (headphones advised; speakers feed an open mic back).
  Post-limiter tap in the TX chain → 4:1 anti-aliased decimate to the
  12 kHz output → mixed into the speaker path like the sub-RX, with a
  drift-resync cap so mic-vs-radio clock skew can't grow the latency.
- **RX mutes while keyed** (half duplex done right): the main RX sits on
  our own TX signal during transmit — it now goes silent instead of
  blaring your own sidetone-shifted audio. Verified by recording the
  app's output through BlackHole: band noise −41 dB mean unkeyed,
  digital silence (−91 dB) keyed with monitor off, and with the monitor
  on the recording contains the profile-shaped voice (speech band 17 dB
  above the >3.5 kHz floor).
- Mic capture tap shrunk 2048 → 512 frames (~43 → ~11 ms) — tighter
  monitor latency and faster key-to-audio.
- New regression test pins the monitor tap (runs unkeyed, mirrors every
  sample, carries the profile shaping) — 31 tests.

## [2.10] — 2026-07-14

The TX audio batch — all validated live into the dummy load:

- **Mic input selection** (TX window): capture from any CoreAudio input —
  USB, Bluetooth, or virtual (BlackHole shows up, ready for WSJT-X TX
  audio). Keyed by stable device UID, hot-swaps while armed, falls back
  to the system default if the device leaves.
- **Six TX voicing profiles**: Standard (300–2900), DX SSB (400–2600,
  presence rise, 6:1), Contest (500–2400, 8:1), ESSB Wide (100–4000),
  Broadcast (200–3300), Hi-Fi AM (50–5000). Each sets the transmit
  bandpass, a three-band EQ (250 Hz shelf / 2.2 kHz presence / 3.5 kHz
  shelf), and an envelope compressor with makeup gain. On-air check: DX
  speech cuts off at exactly +2.6 kHz, ESSB reaches +4 kHz with energy
  down at the carrier.
- **AM transmit**: full-carrier AM modulator (carrier + both sidebands)
  — the Hi-Fi AM profile now means something. PTT/TUNE accept AM mode
  alongside USB/LSB. Verified on the waterfall: carrier column at the
  dial, symmetric ±5 kHz speech sidebands.
- **Eight TX voice effects** (FX picker): Doubler, Slap Echo, Echo, Long
  Delay, Chorus, and Room / Hall / Plate reverbs (Schroeder combs +
  allpasses, RT60-derived feedback). Echo tail confirmed still
  transmitting ~1 s after the phrase ends.
- The Hilbert transformer grew 129 → 1025 taps so ESSB's 100 Hz low edge
  keeps clean opposite-sideband suppression (good to ~70 Hz).
- New regression tests: profile bandwidth (ESSB passes 3.6 kHz, Standard
  rejects it), AM carrier + sideband symmetry, echo timing — 30 tests
  total, all green.

## [2.00] — 2026-07-14

**Transmit is live.** Validated on the air into a dummy load on real
hardware (HL2 gw v75, 14.2 MHz): sideband sense correct both ways,
SWR 1.1 flat from 1–5 W, clean key/unkey with instant RX restore, and
speech occupying exactly the USB passband. Issue #7 closed.

- **PA enable (the critical fix)**: EP2 register 0x09 carries the HL2
  onboard-PA switch in C2 bit 3 — we never set it, so every key-up
  transmitted microwatt exciter leakage (visible on our own waterfall,
  0.00 V forward, 0.00 A PA). Now sent throughout the preload/keyed
  sequence and hard-off in RX. First keyed watt: 2026-07-14, 06:53 local.
- **TUNE mode**: steady 700 Hz tone at the drive setting (button under
  PTT) for dummy-load tests and antenna tuning. Synthesized
  phase-continuously in the TX chain behind the same key envelope and
  interlocks as PTT; the mic path idles while tuning. Tone sideband
  sense pinned by a new regression test (27 total).
- **CAT PTT**: rigctl `T 1`/`T 0` now keys the radio (WSJT-X digital TX
  ready) and `t` reports the real key state, pushed on every change.
  Still gated by the in-app ARM interlock — a disarmed rig refuses and
  shows why. Validated live over TCP 4532.
- **Power readout**: PWR cell in the TX telemetry row, P ≈ FWD²/2 —
  the stock detector fits 5.0 W at the measured 3.17 V full-drive
  point. Per-board trim: `defaults write com.squaredeck.app
  fwdPowerCalK <k>`.
- Dummy-load cal points (14.2 MHz): 9% drive → 1.41 V / 0.60 A ≈ 1 W;
  49% → 2.13 V / 0.87 A ≈ 2.3 W; 100% → 3.17 V / 1.35 A ≈ 5 W; SWR 1.1
  and ≤40 °C throughout.

## [1.95] — 2026-07-14

- The FT8/FT4 decode panel has a close (✕) button in its header — the
  only way to dismiss it was the little list-icon toggle by the FT8
  button, which nothing pointed to. Decoding keeps running when closed.

## [1.94] — 2026-07-14

- NR ear A/B verdict (issue #2, closed): the spectral gate wins on this
  station — RNNoise pumps on impulsive QRN (its voice detector rides the
  gain, then the AGC amplifies the wobble). DeepFilterNet/ANE plan
  dropped; RNNoise stays as a toggle for steady-hiss conditions, and the
  DSP-popover help now says so.

## [1.93] — 2026-07-13

The easy-features-and-optimizations batch:

- Network throughput indicator in the status bar next to pkt/s
  (~1.6 MB/s at 192 kHz, ~2.8 MB/s with the sub-RX on).
- Trackpad continuous tuning: two-finger horizontal pan over the
  panadapter tunes smoothly (~⅕ tune-step per point, like the
  flywheel); vertical scrolling and mouse wheels stay stepped, and
  momentum flicks stay dropped.
- FT4 decode (FT4 toggle beside FT8, mutually exclusive): 7.5 s slots
  through the same spot pipeline — panel, overlay, ADIF, and
  PSKReporter all label FT4 correctly. Round-trip tested.
- Frequency bookmarks (star button in the tuning row): named spots
  with mode, yellow markers on the panadapter, jump/delete popover.
- Stations-heard map (globe button in the FT8 panel): grids parsed
  from CQ messages plotted on a world map with decode counts.
- QRZ lookup: right-click any decode row in the FT8/FT4 panel.
- Pixel-art app icon: amber "SD" over a spectrum trace and waterfall.
- Optimizations: Metal views pause while their window is occluded or
  minimized (three renderers no longer burn GPU behind other windows);
  the CW/RTTY/SSTV/WEFAX oscillators use phasor recurrence instead of
  per-sample trig (~5× cheaper detectors, decode-verified by the test
  suite).

## [1.92] — 2026-07-13

Documentation refresh (README rewritten from its stale 1.10 state;
CLAUDE.md brought current) plus a three-agent full-codebase bug sweep —
15 findings, all fixed:

- CRITICAL: enabling the sub-receiver on 1.71–1.91 deadlocked the whole
  RX pipeline (a 1.71 lock-hygiene fix made the mix closure re-take its
  own lock). Live-verified fixed.
- TX safety hardening: the mic-permission dialog can no longer re-arm
  the transmitter after you've disarmed; stopping/disconnecting sends a
  final MOX=0 frame instead of leaving the radio's last word keyed; a
  watchdog stream restart force-unkeys (and the PTT lamp follows); the
  10 ms unkey ramp is now actually transmitted (no key click), including
  when disarming mid-over; sample-rate/sub-RX changes unkey first.
- FT8/PSKReporter: "RR73" is no longer mistaken for a grid square
  (spots would have plotted in the Arctic); uploads are chunked ~50
  spots per datagram so busy-band batches don't fragment and vanish.
- Tuning: marker drags and clicks no longer pan the display out from
  under the cursor during replay; a cancelled flywheel drag can't make
  the next drag jump; digit double-click undoes the correct half-step.
- Stale telemetry clears on disconnect; drive 100% programs 255;
  LNA/VFO-B restores are clamped.

## [1.91] — 2026-07-13

Fine-tuning batch (features ride Z-bumps until 2.00, which stays
reserved for validated transmit):

- Tune-step control in the tuning row: 10/25/50/100/250/500 Hz or Auto
  (follows zoom — finer as you zoom in). Drives waterfall scroll, arrow
  keys, and the flywheel; ⇧ = ÷5 fine, ⌥ = ×10 coarse still apply.
- Drag the red VFO marker directly (grab within ±8 px): continuous
  carrier positioning at the 10 Hz snap — no 100 Hz click quantum, no
  passband offset — with a magnified frequency readout floating at the
  marker while you drag.
- VFO flywheel: a ribbed knob strip under the frequency-readout digits.
  Drag it like spinning a weighted VFO knob (~⅕ tune-step per pixel,
  applied in 10 Hz quanta) — the missing "big knob" for sub-kHz work.
- Reminder of the existing fine controls these compose with: scroll
  over any frequency-readout digit tunes at that digit's place, and the
  audio mini-waterfall (23 Hz/bin) is the high-resolution view for
  parking CW/digital signals on pitch.

## [1.90] — 2026-07-13

- HL2 telemetry decoded from the EP6 control responses: board
  temperature, PA current, forward/reverse power (bridge volts) and SWR,
  metered in the TX Controls window. Temperature and current are live
  in RX (verified on air: 37 °C idle); the power bridge reads during
  transmit — instrumentation ready for the dummy-load session.
- PSKReporter spotting: enter your callsign + grid in the gear popover
  and flip the toggle — received FT8 decodes upload to pskreporter.info
  every ~5 minutes (spec-paced), putting your station on the world map
  as a monitor. Status line shows each upload.

## [1.80] — 2026-07-13

Transmit framework — the complete TX path, built SAFE-first and not yet
keyed on air (2.00 waits for dummy-load validation):

- Pixel-art ACTIVATE TX CONTROLS banner in the header opens the new TX
  Controls window: SAFE/ARMED/ON-AIR state lamp, ARM interlock (starts
  mic capture; nothing persists — every launch is SAFE), a PTT that
  refuses to key unless armed + connected + live + USB/LSB, drive %,
  mic gain and level meter, split/XIT-aware TX frequency readout.
- TX DSP: 48 kHz mic capture → speech bandpass → Hilbert-pair SSB
  modulator (≥40 dB image suppression, regression-tested both sidebands)
  → soft limiter → 10 ms raised-cosine key envelope.
- Protocol: MOX sequencing honors the HL2 NCO-slaving quirk — the real
  TX frequency is delivered to the radio for ~60 ms of frames BEFORE MOX
  rises, keyed frames stream 16-bit IQ, and unkey restores the receiver
  immediately. Keying refuses during replay/disarm; disconnect disarms.

## [1.71] — 2026-07-13

Consolidation release: live hardware verification plus a three-agent bug
sweep over everything added since 1.20 (11 confirmed findings, all fixed).

Live-verified on the radio: **sub-receiver two-RX framing and the RX2
register work on gw v75** (packet rate matched theory, clean second
panadapter on VFO B) — TX's protocol prerequisites are now proven. CW
decoder and WEFAX capture verified mechanically on air.

- FT8: callsign hashtable could spin forever once 256 distinct calls
  accumulated (busy band, ~3 min) — probe-capped. Spot frequencies are
  now stamped with the carrier the slot was captured under, not the one
  at decode time (tuning mid-slot mislabeled a whole cycle). Spots now
  age out even after decoding stops. FT8 pauses while the time machine
  is rewound (slot alignment is wall-clock).
- WEFAX: phasing now anchors to the measured end of the start tone —
  a real-length (5 s+) start tone previously got folded into the phase
  estimate, wrapping the whole chart horizontally. Phase search can no
  longer read future/stale ring data.
- CW: 12× SNR gate (was 6×) — band noise through a 500 Hz filter no
  longer chatters dit-strings at 60 WPM (found live); noise-gated marks
  drop the pending pattern instead of emitting garbage.
- EP2 keepalive pacing now counts received samples, not packets — with
  the sub-RX on it ran 1.75× fast (harmless today, would overrun the TX
  FIFO in phase 2). Receiver-count changes are queue-ordered with the
  stream stop/start.
- Sub-receiver window no longer shows a frozen, fake-live panadapter
  during replay/disconnect; sub waterfall clears on enable, rate change,
  and disconnect; SUB toggles duck the audio.
- WAV recording: timers and disk-failure detection now work during
  replay; a failed mid-recording write patches the RIFF header so the
  audio already on disk stays playable.
- ADIF export is locale-proof (Gregorian dates regardless of system
  calendar). Notch chips remove by value (stale-index crash window).
  Decoder/FT8 panels only auto-scroll when already at the bottom.

## [1.70] — 2026-07-13

Three new decoders (the Black Cat Systems-inspired batch), each with its
own window and a synthesize→decode regression test:

- CW decoder: Morse from the 700 Hz CW pitch — adaptive threshold and
  8–60 WPM speed tracking, live WPM readout, scrolling text window.
- RTTY decoder: 45.45 Bd Baudot (US-TTY), mark/space 2125/2295 Hz,
  LTRS/FIGS shift tracking — tune in LSB so the tones land there.
- Weather fax (FAX): 120 LPM IOC-576 charts — automatic start-tone and
  phasing detection, per-line rendering into a scrollable window,
  auto-save as PNG, plus Start-now/Finish overrides for joining a fax
  mid-transmission. Try 8.682 USB on the NOAA schedule.
- The mode group is now a two-line block: modes on top, all five decoder
  toggles (FT8, SSTV, FAX, CW, RTTY) beneath.

## [1.60] — 2026-07-13

- SSTV decode (SSTV button in the mode group): Martin M1/M2 and Scottie
  S1/S2 — VIS auto-detect, per-line sync tracking (no slant), picture
  paints line-by-line in its own window, completed images auto-save as
  PNG to ~/Documents/SquareDeck Recordings. Works live and during IQ
  replay. Pinned by an encode→decode round-trip test in both layouts.
- Audio (WAV) recording: a second record button in the header captures
  the demodulated audio you hear (16-bit 12 kHz mono WAV, sub-RX mix
  included) — distinct from the raw-IQ record button, and it works
  during replay, so old .sqiq captures can be bounced to WAV.
- FT8 controls moved into the mode group beside the mode picker, with
  SSTV alongside; recenter/zoom moved to the second row.

## [1.51] — 2026-07-13

UI reorganization and resize fixes (verified by scripted resize + screenshots).

- The control bar is now two rows — tuning (frequency readout, mode,
  filter, VFO cluster, band, step, zoom) and DSP/system (NB/DSP/FT8,
  display, palette, ATT/LNA/volume/rate) — each pinned to the leading
  edge. The frequency readout can no longer roll off screen: a narrow
  window clips trailing controls only. Previously the single overflowing
  row was centered, so BOTH edges clipped and the readout slid off left.
- Window minimum is now 1240×760 (was 1700 wide), and everything fits at
  the minimum.
- Waterfall colors get a palette icon in the control bar (was buried in
  the Display popover) — one click, five schemes.
- Fixed: "Band" menu truncating to "Ba…"; Floor/Ref labels in the status
  bar wrapping into vertical letter stacks when squeezed.

## [1.50] — 2026-07-13

- FT8 decode panel (list button by the FT8 toggle): full message history
  beside the panadapter with UTC time, SNR, and audio offset — CQ calls
  highlighted green, click a row to tune to it, auto-scrolls on new
  decodes. Export the session's unique stations heard as an ADIF SWL log
  (grids parsed from CQ messages) to ~/Documents/SquareDeck Recordings.
- Waterfall color schemes (Display popover): Classic, Inferno, Viridis,
  Phosphor (green CRT), and Mono — one 256-entry gradient texture swap,
  so the whole scroll history recolors instantly across the main,
  sub-RX, and audio waterfalls. Persisted.

## [1.40] — 2026-07-13

- 24-hour UTC clock in the header bar, drawn with the same FT-1000MP
  amber seven-segment LCD as the frequency readout — HH:MM:SS, ghost
  segments, and colons blinking at 1 Hz. Handy for FT8 cycle timing.

## [1.30] — 2026-07-13

- FT8 decode with callsign spots on the panadapter — a live band map
  (FT8 button in the control bar; USB mode). Decodes each 15 s UTC cycle
  in-process (vendored ft8_lib, MIT) off the DSP thread; cyan labels sit
  over their signals, age out after ~3 cycles, and click-to-tune. Pinned
  by an encode→decode round-trip regression test.
- Sub-receiver panadapter in its own window: full spectrum/waterfall of
  RX2's span centered on VFO B, with click/scroll tuning of B, a ghost
  "A" marker, and the shared dB scale. Opens automatically with SUB.
- Noise-reduction ear A/B: press N over the panadapter to cycle
  Off → spectral gate → RNNoise. Offline analysis on real 40 m
  recordings (issue #2): the gate measures ~0 dB against this station's
  QRN while RNNoise nets 4–6 dB SNR at zero speech cost.
- Swift 6 strict concurrency (app + test package): internally-
  synchronized classes annotated, zero warnings, no behavior change.

## [1.20] — 2026-07-13

- Sub-receiver + VFO A/B + split + RIT/XIT (VFO cluster in the control
  bar): SUB requests a second hardware receiver over Protocol 1 (RX2 NCO
  on VFO B, interleaved EP6 frames), demodulates it in parallel with the
  main RX (same mode/filter), and sums it into the audio with its own
  level. A⇄B swap / A▸B copy / direct B entry; SPLIT armed for phase-2
  TX; RIT shifts the received passband off the dial (panadapter shading
  and notches follow), XIT stored until TX ships. VFO B drawn in green
  on the panadapter.
- Audio passband mini-waterfall (Display popover toggle): a 0–6 kHz strip
  under the panadapter showing the demodulated audio spectrum — precise
  CW/digital tuning, passband edges, CW pitch line, and manual-notch
  markers on the audio axis. Right-click a tone there to notch it.
- Time machine click-to-scrub: ⌥-click (or ⌥-drag) a row in the waterfall
  history to jump the time machine to that moment — the past is now
  navigable visually, not just by slider. Rows are timestamped with their
  data's true age (scrubbing while already shifted stays accurate);
  clicking the newest rows snaps back to live.
- RX audio EQ (DSP popover): two shelving bands ±12 dB — bass at 300 Hz,
  treble at 2.5 kHz — to warm thin SSB voice or brighten a muffled one.
  Runs ahead of the AGC so the limiter absorbs boosted peaks; pinned by a
  shelf-sense regression test.
- Display popover (magnifier icon by the zoom controls): spectrum averaging
  modes — Fast/Med/Slow EMA or Peak detect (per-bin max between rows, so
  brief CW/FT8 bursts can't slip between FFTs) — and waterfall speed
  (10/20/30/60 rows/s). Both persisted.

## [1.11] — 2026-07-13

Bugfix batch from a full-codebase sweep (13 findings, none critical).

- Recording no longer crashes the app if the disk fills mid-recording: all
  file writes use the throwing FileHandle API, and a failed write stops the
  recording with an error message instead of raising.
- Per-mode-group filter bandwidth memory now restores unconditionally on a
  mode change — AM→SSB→AM comes back at your AM width, not the SSB one.
- Reconnecting while muted stays muted (the mute icon no longer lies).
- Replaying a .sqiq no longer leaks the file's sample rate into the saved
  preference (even quitting mid-replay); live connects come back at your rate.
- The audio "duck" retriggers continuously: dragging filter/shift/time-machine
  sliders no longer snaps the envelope from silent to full in one sample
  (the zipper-click the duck existed to hide).
- Manual notches survive a sample-rate change (they silently vanished from
  the filter while their markers stayed).
- Double-clicking a frequency digit no longer steps the frequency before
  opening the editor.
- Connecting to an unresolvable hostname now fails with an error instead of
  a silent blank waterfall.
- The waterfall clears on an NCO retune — old rows were drawn misaligned
  under the relabeled scale (peak-hold already cleared for the same reason).
- Replay clamping the VFO into the recorded span now goes through the normal
  tuning path (CAT/WSJT-X sees the real frequency; 10 Hz snap applies).
- A queued ADC-overflow callback can no longer strand a stale OVF badge
  after disconnect.
- The audio-output device menu re-reads the device list when opened —
  plugging in BlackHole no longer needs the manual refresh.
- The SQUAREDECK_MIX_TAP diagnostic can no longer double-install its tap
  (which raised) when the engine restarts after a failed file open.

## [1.10] — 2026-07-13

- Manual notch filters: right-click a tone on the waterfall to notch it
  (right-click again to remove; purple markers; chips in the DSP popover).
  ≥45 dB deep, zero extra DSP cost — shaped into the FFT channel filter.
- Squelch (S-meter-calibrated dBm threshold, 6 dB hysteresis) and overload
  auto-mute above −20 dBm, with click-free 10 ms gate ramps.
- Raised-cosine slew ramps (~60 ms) hide the click when changing
  mode/filter/NB/NR settings or jumping the time machine.
- Time machine "Save buffer": dump the buffered IQ to a replayable .sqiq.
- Band-step controls: ◀/▶ buttons with a 1/5/10/20/50/100 kHz step menu,
  snapping the VFO to the step grid.

## [1.00] — 2026-07-13

First stable release: a complete, high-performance receive-only client for
the Hermes-Lite 2 / SquareSDR over openHPSDR Protocol 1. Apple silicon only,
macOS 15+.

### Receiver
- USB / LSB / CW / AM / SAM demodulation at 48–384 kHz sample rates, verified
  on the air (SSB voice, FT8 via WSJT-X).
- FFT overlap-save channel filter: 513 taps as 1024-point fast convolution —
  −120 dB stopbands, ~100 Hz skirts, measured −123 dB just 100 Hz past the
  passband edge.
- Continuously variable filter width with per-mode ranges and presets;
  click-free live width changes; independent IF-shift / passband tuning.
- Decimation-droop compensation folded into the channel filter (flat wide
  passbands).
- WDSP-lineage WCPAGC (look-ahead, hang, pop recovery) with Fast/Med/Slow/Off;
  fixed makeup gain in Off for digital modes.
- Synchronous AM with carrier-tracking PLL and fade leveler.
- Noise tools: impulse blanker (full-rate, duty-governed), spectral-gate
  noise reduction, RNNoise ML noise reduction (recurrent network, vendored
  BSD-3), LMS auto-notch.
- Digital step attenuator (0/−10/−20/−30 dB) and full-range LNA control
  (−12…+48 dB) with per-band memory and auto-backoff on ADC overload.
- Calibrated S-meter (antenna-referenced through LNA/ATT settings).

### RF time machine
- The last 3 minutes of full-span IQ are always buffered; rewind with a
  slider and re-tune / re-mode / re-filter the past. Live IQ keeps recording
  underneath.

### Panadapter
- Metal waterfall + spectrum with 2048-row history, GPU zoom (×1–×8),
  pan-over-span without retuning the radio, peak hold, adjustable
  floor/reference.
- Tuning UX: per-digit readout scrubbing, click-to-tune that lands the SSB
  passband on the click, momentum-scroll rejection, band memory
  (freq/mode/filter/LNA/ATT per band).

### Integration
- IQ record/replay (.sqiq raw float pairs), replay through the full receiver.
- Hamlib NET rigctl CAT server on TCP 4532 (WSJT-X-compatible), selectable
  audio output device (BlackHole-friendly).
- HL2 discovery via broadcast + unicast probe bursts; stream watchdog;
  sequence-error tracking.

### Under the hood
- Lock-free SPSC audio ring between DSP and the CoreAudio render thread.
- IQ batching (~5 ms blocks): whole RX chain ≈0.7% of one core at 384 kHz.
- GPU-timeline waterfall updates (blit ring, private texture, triple-buffer
  fencing).
- `swift test` DSP regression suite (filter sideband sense, skirt depth,
  AGC dynamics, SAM lock, ML NR, history ring).
- Workaround for HL2 gw v75 slaving RX1's NCO to the TX NCO register.
