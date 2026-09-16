# Resolume-inspired UI implementation roadmap

Planning only, inspected 2026-09-16. Visual decisions and proposed geometry are in
[UI_DESIGN.md](UI_DESIGN.md).

## What is actually in this repository

Inspected `dzcassell/HermitSDR-releases`, `main` at
`ecdacd0b71beb41c43466fecb50469a6dbb809e9`, before these planning documents were added.
The remote advertised one branch, `main`. Its complete tracked tree was:

| Path/surface | Present | What it provides |
|---|---|---|
| `README.md` | Product guide | Features, operator controls, download instructions; describes SwiftUI/Metal architecture but does not contain implementation |
| `CHANGELOG.md` | Release history | Published capabilities and provenance; not executable source or a test suite |
| `assets/hermitsdr-logo.png` | Branding image | Existing product logo, not editable UI source or the requested AI Crab icon |
| GitHub release `v2026.0916_001` | DMG, ZIP, `release.json`, `SHA256SUMS` | Distribution assets and verification metadata, separate from the tracked tree |
| Latest release tag tree | Empty | `git ls-tree -r v2026.0916_001` returned no files |
| App/UI/build/test sources | Absent | No Swift/Metal files, Xcode project, Package.swift, UI assets catalog, tests or CI workflows in the inspected main tree |

The README explicitly states that source is unpublished and GitHub's automatic
“Source code” archives are empty. The latest release points to the empty anchor
`33258e549cb79b5261303ed6636eb3c5c57ef7d8`. The separately attached DMG/ZIP are the
app downloads; their contents were not unpacked or audited for this planning task.
The changelog records the latest publication from source revision `791c4e7`.
Release claims about builds/tests are documentation, not checks rerun here.

Evidence: [inspected tree](https://github.com/dzcassell/HermitSDR-releases/tree/ecdacd0b71beb41c43466fecb50469a6dbb809e9),
[README at inspection](https://github.com/dzcassell/HermitSDR-releases/blob/ecdacd0b71beb41c43466fecb50469a6dbb809e9/README.md),
[changelog at inspection](https://github.com/dzcassell/HermitSDR-releases/blob/ecdacd0b71beb41c43466fecb50469a6dbb809e9/CHANGELOG.md),
[release](https://github.com/dzcassell/HermitSDR-releases/releases/tag/v2026.0916_001).

**Conclusion:** this repository is suitable for the public design brief and roadmap,
but cannot build or implement the redesign. Keep application source in its existing
source repository; do not publish it here or repoint release tags to source commits.

## Source handoff

A separate local source checkout was found with origin `dzcassell/HermitSDR`, at
`d8458d2991e9c34cd92aa8f8bf7aa241d5c87a27` (2026-09-11). It initially predated the latest release. At the owner's request it was then
fast-forwarded by 50 commits to GitHub `main` at
`c886bc27c9af103fdc6cb59f588a92a0bba131ca`. Tracked files match that revision;
the pre-existing untracked `Tests/DSPTests/ReviewJS8TimingTests.swift` was preserved
byte-for-byte. No application source was authored or altered beyond this upstream sync.
The updated checkout has not been built or fully re-audited in this planning task.

The preliminary map below refers only to that older checkout. Revalidate all paths,
owners and commands against the current source before editing:

| Work area | Existing integration leads |
|---|---|
| Window shell and panels | `Views/ContentView.swift`, `MainWindowPresentationModel`, `SpectrumPresentationModel` |
| Header, VFO and compact RX controls | `Views/HeaderViews.swift`, `ControlBarViews.swift`, `ControlViews.swift`, `ReceiverControlsViews.swift`, `FilterControlsView.swift` |
| Theme propagation | `Views/Theme.swift`, existing `SkinCenter`, `SkinTokens`, `AppSkin` |
| Waterfall interactions | `Rendering/MetalSpectrumView.swift`, existing renderer and spectrum geometry |
| RX meter | `Rendering/SMeterRenderer.swift`, `Rendering/Shaders.metal`, existing meter presentation/calibration |
| TX controls/status | `Views/TXViews.swift`, `TXStatusViews.swift`, existing coordinator and policy |
| Crab and workspaces | `Views/AskTheCrabView.swift`, `DecoderActivityView.swift`, `MediaDeckView.swift`, existing feature/menu routing |
| Build/test entry points | `HermitSDR.xcodeproj`, `Package.swift`, `Tests/DSPTests`, repository audit tools |

## Delivery sequence

Each numbered slice should remain buildable and reviewable. Apply source-repository
instructions and its established issue/landing workflow once implementation is
requested; these milestones are a planning proposal, not newly created issues.

| Slice | Deliverable | Acceptance gate |
|---|---|---|
| 0. Establish baseline | Identify authoritative source checkout/ref, read its project instructions, preserve outstanding work, inventory controls/actions/settings and current screenshots; record baseline build, tests and performance | Source revision recorded; actual build/test commands pass or failures are documented before redesign; current VFO, meter, theme, renderer and TX ownership mapped |
| 1. Theme + control vocabulary | Extend existing tokens for six palettes and fixed safety/VFO colors; compact button/toggle/value-slider/tab/panel primitives; UI-only preview fixtures | All six switch live and restore after relaunch; fresh settings use Cold Cyan; existing preferences migrate safely; keyboard/focus/disabled states and SwiftUI/Metal colors agree |
| 2. Console shell | Disconnected interactive shell with left/right/bottom collapse, resize, tab selection, restore/reset and persistent layout; retain existing renderer identity in integrated shell | All eight visibility combinations work at both review sizes; waterfall gains space; existing overlays remain aligned; no controls overflow; hiding views has no radio/decoder side effects |
| 3. Readouts + Crab | LED Amber VFO with last three numeric digits red, calibrated RX gradient, persistent labeled Crab button and final icon | Existing tune/scrub/direct-entry actions unchanged; no frequency precision loss; S-meter calibration unchanged; icon legible at small sizes; text entry cannot key radio |
| 4. Migrate controls | Move RX, TX and chosen bottom workspaces one group at a time onto existing action/model APIs; retain specialized windows/menu access | Before/after control parity checklist complete; no duplicate business logic; TX state/stop remain reachable when collapsed; all refusals and safety semantics survive every palette |
| 5. Regression + performance | Full app checks, UI fixtures, persistence/upgrade tests, accessibility review, resize/theme stress with waterfall/decoders active | No build/test regressions; no lost history, audio underruns or material frame-time/memory regression versus slice 0; measurement conditions recorded |
| 6. Owner acceptance + rollout | Review integrated screenshots and interactive build; retain a reversible legacy-layout option during evaluation if feasible; use established signed release pipeline only when release is requested | Visual acceptance, completed software gates, separately authorized hardware checks as needed; only normal public notes/assets mirrored to releases repo |

## Verification plan

- Start with focused tests for palette persistence/migration, fixed safety tokens,
  VFO digit segmentation, layout restoration/clamping and existing tuning actions.
  Test behavior and boundaries rather than merely repeating color constants.
- In the inspected source checkout, `swift test` exercises DSP/protocol and selected
  model logic, not the entire SwiftUI app. Pair it with
  `xcodebuild -project HermitSDR.xcodeproj -scheme HermitSDR -configuration Debug build`
  and the current repository's prescribed audits/CI. Reconfirm these commands at
  slice 0. Add UI/snapshot or fixture coverage for visual behavior separately.
- Preserve existing TX coordinator tests: ARM, inhibit, refusal, key ownership,
  disconnect, watchdog and unkey tail. Exercise UI RX/armed/TX/fault states with
  synthetic fixtures; never key hardware merely to capture a screenshot.
- Use identical hardware, window size, sample rate, decoder load and capture duration
  for before/after waterfall frame-time, CPU/GPU, memory and audio-underrun checks.
  Set the acceptable regression budget from the existing real-time contract and
  baseline before migration; do not invent an unsupported FPS guarantee.
- Test relaunch and upgrade with existing settings, fresh settings, invalid palette
  IDs and off-screen/oversized stored panel dimensions. Never persist ARM/PTT as
  a side effect of layout or palette persistence.
- Live RX/TX validation is separate from software verification and requires the
  operator's session-specific authorization and setup. Existing transmission,
  privacy, calibration and real-time behavior must be preserved.

## Decisions still needed before implementation

1. Use the synchronized source revision above as the candidate baseline, confirming
   checkout ownership and any newer upstream changes before implementation. Preserve
   the outstanding untracked test; do not silently adopt or delete it.
2. Review proposed panel allocation and minimum supported window size at slice 2.
   The waterfall priority, three collapsible panels, palette list, readout style,
   meter direction and fixed TX colors are already decided.
3. Select the final LED glyph/font asset and modern AI Crab icon during slice 3;
   verify distribution rights and small-size legibility.
4. Decide how existing decorative skins/effects coexist with the new console and
   whether a temporary legacy-layout switch is needed for rollout.

No runtime changes, application builds, hardware sessions or releases are part of
this documentation task. Completion of this roadmap does not imply the UI exists.
