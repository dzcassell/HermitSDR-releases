# SDRplay RSP Receivers

HermitSDR drives the SDRplay **RSPduo** (Single-Tuner and Dual-Tuner SUB / coherent
Diversity; live-validated) as well as the **RSPdx / RSPdx-R2**, **RSP2**,
**RSP1A / RSP1B**, and **RSP1** (conservative unvalidated profiles for models
without physical hardware validation) as **receive-only** USB radios through
SDRplay's API 3.15: 1 kHz – 2 GHz (10 kHz – 2 GHz on RSP1), 48 kHz – 6.144 MHz
of chain bandwidth in Single-Tuner mode (capped at 1.536 MHz in RSPduo
Dual-Tuner), model-specific §5 LNA tables, and model-appropriate front-end
controls. There is no transmitter in any RSP hardware, so a connected SDRplay
shows no TX banner, ARM, PTT, TUNE, or drive control anywhere; every SDRplay
`RadioProfile` has `supportsTX == false`.

Model notes:
- **RSPduo (`hwVer=3`, `0x1DF7:0x3020`)**: Single-Tuner Zero-IF (`3.072 MHz` ADC; Tuner 1 50 Ω ↔ Hi-Z switches live via `rspDuoAmPortSelect`, while Tuner 1 ↔ Tuner 2 and Single ↔ Dual transitions cleanly re-select the device via `Uninit → ReleaseDevice → SelectDevice → Init` to avoid the macOS API 3.15.1 `SwapRspDuoActiveTuner` wedge observed on 2026-11-24) plus Dual-Tuner synchronous Low-IF (`6.0 MHz` ADC, `1620 kHz` IF, resampled `96/125` to `48–1536 kHz`) for independent **SUB (VFO B)** or coherent **Diversity RX (`A + w·B`, with Find-null)** (one Dual-Tuner mode at a time, matching `supportsConcurrentDiversitySubRX = false`). Supports Tuner 1 50 Ω / Hi-Z and Tuner 2 50 Ω inputs, broadcast notches (`rfNotchEnable`, `rfDabNotchEnable`, `tuner1AmNotchEnable`), `24 MHz` ref out, and session-only Bias-T on Tuner 2 (`50 Ω`).
- **RSPdx (`hwVer=4`, `0x1DF7:0x3030`) & RSPdx-R2 (`hwVer=7`, `0x1DF7:0x3060`)**: Antenna A / B / C, HDR mode below 2 MHz, Bias-T on ANT B, AM/FM and DAB notches.
- **RSP1A (`hwVer=255`, `0x1DF7:0x3000`) & RSP1B (`hwVer=6`, `0x1DF7:0x3050`)**: Single SMA port with Bias-T, AM/FM and DAB notches, model-specific LNA tables.
- **RSP2 (`hwVer=2`, `0x1DF7:0x3010`)**: ANT A / ANT B (Bias-T) / Hi-Z (< 60 MHz), AM/FM notch, 24 MHz ref out, model-specific LNA table.
- **RSP1 (`hwVer=1`, `0x1DF7:0x2500`)**: Legacy single SMA input (10 kHz – 2 GHz), model-specific LNA table, no notches or Bias-T.

## Installing the API (once)

The RSPdx has no public USB protocol: its firmware is loaded and its stream
is managed by SDRplay's proprietary **API service**. HermitSDR does not
bundle it and never loads it into its own process.

**Assisted (recommended).** Wherever you meet an SDRplay receiver without
the API — the connect-sheet row's **Install API…**, the one-time toast when
an RSP appears on USB (its **Install…** button; "Not now" is remembered for
the launch), or Settings ▸ SDRplay API ▸ **Install…** — the "SDRplay API
required" sheet offers **Install for me…**. HermitSDR then:

1. downloads SDRplay's installer package from
   `https://sdrplay.com/download/hardware-api-macos/?wpdmdl=1907` (it
   redirects to `SDRplayAPI-macos-installer-universal-3.15.1.pkg`, about
   0.5 MB; 20 MB cap, two-minute timeout, progress in the sheet) into
   `~/Library/Application Support/HermitSDR/Downloads` — never
   `~/Downloads`;
2. **verifies before anything runs**: the filename must be
   `SDRplayAPI-macos-installer-universal-<version>.pkg` with version
   ≥ 3.15, and `pkgutil --check-signature` must show
   `Developer ID Installer: SDRplay Limited (2J9W5H85P2)` and
   `Notarization: trusted by the Apple notary service`. On any mismatch the
   file is deleted, nothing is installed, and SDRplay's download page opens
   so you can continue by hand;
3. hands the package to the **macOS Installer** (`open`, deliberately not a
   silent `installer -pkg`): SDRplay's licence agreement and the
   administrator prompt are shown to you and accepted by you;
4. waits — "Finish the SDRplay installer; HermitSDR will continue
   automatically" — polling the availability probe every 2 s for up to ten
   minutes (library + receipt + `com.sdrplay.service` running + a helper
   hello that says the API is open), then reconnects to the RSPdx (or just
   closes when the prompt came from Settings). Cancel is clean at any
   point.

Settings ▸ SDRplay API shows the probe's verdict (installed and running /
installed but service stopped / not installed / wrong version) with **Check
again**. The probe (`SDRplayAPIAvailability`) reads the library candidate
paths, `pkgutil --pkg-info com.sdrplay.api` (receipt `3.15.1` here),
`launchctl print system/com.sdrplay.service` (or a running
`sdrplay_apiService`), and the helper's `sdrplay_api_ApiVersion` verdict.

**By hand.** Download the **SDRplay API 3.15 for macOS** from
<https://www.sdrplay.com/api/> and run SDRplay's installer (you accept
   their licence there). Observed on macOS 26 with the 3.15.1 installer:
   everything lands under `/Library/SDRplayAPI/3.15.1/` —
   `lib/libsdrplay_api.so.3.15`, `include/sdrplay_api*.h`,
   `bin/sdrplay_apiService` and `plist/com.sdrplay.service.plist` — with
   symlinks in `/usr/local/lib` (`libsdrplay_api.so`, `.so.3`, `.so.3.15`,
   `.dylib`, `libsdrplay_api_arm64.so.3.15`) and `/usr/local/include`.
2. The installer registers and starts the launchd daemon
   `com.sdrplay.service` (`launchctl print system/com.sdrplay.service` shows
   it `running`). It must be running: the library talks to the device only
   through it.
3. Plug the RSPdx in, open HermitSDR's connect sheet and rescan.

Only API **3.15** is accepted. The helper reads `sdrplay_api_ApiVersion()`
and refuses any other version — the C structures it drives changed shape
between 3.07 and 3.15 (`sdrplay_api_RspDuoTunerParamsT` grew, moving the
RSPdx tuner parameters) — rather than guessing a layout. If a future
installer ships 3.16, the connect sheet says so and HermitSDR needs an
update.

## How it works

```
HermitSDR.app (hardened runtime, library validation ON)
  └─ Contents/Helpers/HermitSDR SDRplay Helper   (own target, hardened runtime,
        com.apple.security.cs.disable-library-validation — the ONLY exception)
        ├─ dlopen /Library/SDRplayAPI/<ver>/lib/libsdrplay_api.so.3.15
        │  (then /usr/local/lib; HERMITSDR_SDRPLAY_LIBRARY overrides)
        ├─ sdrplay_api_Open → ApiVersion (3.15 only) → GetDevices/SelectDevice
        │  → GetDeviceParams → layout self-check → Init / Update / Uninit
        └─ stdin: requests · stdout: hello, device list, status, int16 IQ / Dual-IQ
             (little-endian frames, protocol v3, SDRplayHelperProtocol.swift)
```

The helper restarts sampling when the rate plan changes. A generation number on each IQ frame lets HermitSDR discard samples already in transit from the previous plan. A failed live dual-tuner update stops both tuners and asks the operator to reconnect.

- **Discovery** (`SDRplayDiscovery`) launches the helper when the connect
  sheet is open and asks it for the device list every 3 s. Rows name the
  detected model (`SDRplay RSPduo`, `SDRplay RSPdx`, `SDRplay RSP1A`, …) with
  the API's serial (note that USB descriptor serials may differ from API
  serials or be empty on hubs, in which case USB fallback uses `locationID`).
  When the helper says the API is missing, the wrong version, or its service
  is not answering, attached SDRplay USB devices (vendor `0x1DF7`, product
  IDs `0x2500/0x3000/0x3010/0x3020/0x3030/0x3050/0x3060`) are still listed
  with the reason and an **Install API…** link; Connect stays disabled.
- **Connecting** (`SDRplayLink`) launches a helper for the session, opens
  the radio by serial and sends the complete configuration whenever
  anything changes; the helper diffs it and issues the matching
  `sdrplay_api_Update` reasons (or `Init` for the first stream). If the
  helper dies, the link relaunches it with a bounded backoff (0.5 s doubling
  to 8 s, six attempts) and re-opens the radio; the stream resumes without
  a disconnect. Unplugging the radio ends the session with a message.
- **Layout self-check.** The helper's struct access is by computed C offsets
  (`SDRplayAPITypes.swift`), pinned by tests against `sizeof`/`offsetof`
  values compiled from the installed 3.15.1 headers. After `SelectDevice` it
  also reads documented defaults (`fsHz` 2 000 000, `rfHz` 200 000 000,
  `bwType` 200, `loMode` auto, `minGr` 20, `refreshRateTime` 2048,
  `setPoint_dBfs` −60, `hdrBw` 1.7 MHz …) through those offsets and refuses
  the device if any differ. `HERMITSDR_SDRPLAY_SKIP_LAYOUT_PROBE=1` bypasses
  the probe for a diagnostic session.
- **Sample rates & RSPduo Dual-Tuner.** In Single-Tuner mode on every RSP,
  chain rates `48 kHz … 3.072 MHz` run on the `3.072 MHz` Zero-IF ADC
  (`÷32 … ÷1`, with `48 kHz` adding one host decimate-by-2 `ComplexDecimator`),
  while `6.144 MHz` switches the ADC to `6.144 MHz` Zero-IF (`dec = 1`,
  `5000 kHz` IF BW). When the RSPduo runs **SUB (VFO B)**
  or **Diversity RX**, the helper re-selects the device in Dual-Tuner Low-IF mode
  (`fsHz = 6.0 MHz`, `ifType = 1620 kHz`, IF BW ≤ 1536 kHz, chain rate capped
  at `1536 kHz`), delivering
  `2.0 MHz / decimation` (`62.5 kS/s … 2.0 MS/s`) synchronously on `StreamACbFn`
  and `StreamBCbFn` aligned by `firstSampleNum` into `.dualIQ` frames. `SDRplayLink`
  applies matched `ComplexRationalResampler(up: 96, down: 125)` filters on both
  tuners to reach `48–1536 kHz`, delivering RX2 before RX1 for SUB or computing
  `A + w·B` (with the `setOnDiversityPairIQ` tap for Find-null) for Diversity.
- **HDR mode** (below 2 MHz) parks the tuner on one of the ten fixed HDR
  centres (135, 175, 220, 250, 340, 475, 516, 875, 1125, 1900 kHz) and the
  link rotates the I/Q by the difference so the display still shows the
  dial. The HDR path delivers a sixteenth of the normal rate (measured; see
  below), so HDR is offered at chain rates up to 192 kHz and the link asks
  for decimation ÷16.
- **Gain & S-meter calibration.** The RF gain slider is the LNA gain reduction (0 … −84 dB); the
  link lands it on the band's nearest `LNAstate` using the specification's
  table (Settings shows the state and its dB for the current band). IF gain
  reduction (20–59 dB) and the API's AGC (off / 5 / 50 / 100 Hz) are in the
  SDRplay section; with the AGC on, the readback shows what it chose, and
  HermitSDR uses `SDRplayStatus.currentGainDb` to keep the S-meter and Level
  squelch calibrated in antenna-referenced dBm even while wideband hardware AGC moves.
- **Overload.** `sdrplay_api_PowerOverloadChange` events light and clear the
  header's ADC OVF lamp (the helper acknowledges each one as the API
  requires).
- **I/Q** arrives as int16 (full scale ±32767) and is scaled to ±1.0. The API
  delivers I then Q; `SDRplayLink.conjugateIQ` flips the sense if a live
  check shows a mirrored spectrum (none did on the first run's noise floor;
  a known on-air signal is the test).

## Settings ▸ SDRplay Front End

Controls adapt to the connected model (`SDRplayModel`):

| Control | API field | Models & notes |
| --- | --- | --- |
| Input / Antenna | `rspDxParams.antennaSel`, `rspDuoTunerParams.tuner1AmPortSel` / active tuner swap, `rsp2TunerParams` | RSPduo: Tuner 1 50 Ω / Tuner 1 Hi-Z (< 60 MHz) / Tuner 2 50 Ω (Single-Tuner only); RSPdx/dx-R2: ANT A / B / C; RSP2: ANT A / B / Hi-Z; RSP1/1A/1B: ANT A only. |
| LNA state | `gain.LNAstate` | Model-specific per-band §5 tables (including Hi-Z rows on RSP2/RSPduo and HDR row on RSPdx/dx-R2). Shared with the RF gain slider. |
| IF gain reduction | `gain.gRdB` | 20–59 dB; greyed while the AGC is on. |
| AGC | `agc.enable`, `setPoint_dBfs` | Off / 5 / 50 / 100 Hz loop; set-point −30 dBFS. |
| HDR mode + bandwidth | `rspDxParams.hdrEnable`, `rspDxTunerParams.hdrBw` | RSPdx / RSPdx-R2 only; below 2 MHz, chain rate ≤ 192 kHz; 200 k / 500 k / 1.2 M / 1.7 M. |
| Bias-T | `biasTEnable` | Session-only, off at launch, restore, disconnect and helper restart. Requires confirmation for the current helper open and port: ANT B on RSPdx/dx-R2/RSP2, Tuner 2 (50 Ω) on RSPduo (live in Dual-Tuner; stripped if returning to Single-Tuner on Tuner 1), single port on RSP1A/1B, absent on RSP1. |
| Notches | `rfNotchEnable`, `rfDabNotchEnable`, `tuner1AmNotchEnable` | AM/FM notch (all except RSP1); DAB notch (all except RSP1/RSP2); Tuner 1 Hi-Z MW AM notch (RSPduo). |
| 24 MHz reference out | `rspDuoParams.extRefOutputEn`, `rsp2Params.extRefOutputEn` | RSPduo and RSP2 external 24 MHz clock reference output on the MCX connector. |
| IF bandwidth | `tunerParams.bwType` | Auto (widest inside the rate, capped at 1.536 MHz in RSPduo Dual-Tuner) or a narrower pin. |

Every non-Bias-T choice is saved per device serial in the operating catalog's
`sdrplayFrontEnd`; Bias-T is stripped from persistent storage and cleared on
disconnect. The diagnostics line shows API version, RSPduo tuner mode, stream
state, IF and LNA gain reduction readback, ADC overload, delivered rate,
helper dropped samples, and helper restarts.

## First hardware run — 2026-11-02

Owner's Mac (macOS 26, Apple silicon), SDRplay API **3.15.1** installer,
`sdrplay_apiService` pid 27844 running as `com.sdrplay.service`, RSPdx on a
generic 4-port USB 2.0 hub, no antenna connected. Driven by the embedded
helper from a Debug build through a Python copy of the protocol — no GUI
app, receive only, bias-T never turned on.

- Hello: `apiState ready`, API version **3.15**, library
  `/Library/SDRplayAPI/3.15.1/lib/libsdrplay_api.so.3.15`.
- `GetDevices`: one device, serial **2005009343**, hwVer **4** (RSPdx),
  tuner mask 1, valid. `SelectDevice` + `GetDeviceParams` + layout probe:
  0.14–0.16 s, no mismatches.
- First `Init` (fs 3.072 MHz, decimation 16, 7.074 MHz, ANT A, LNA 4, IF GR
  40, AGC 50 Hz): success in ~0.5 s; first I/Q 0.55 s after the request;
  `samplesPerPkt` read back 0 (the API did not fill it on this build).
  4 s window: 1528 frames, 666 981 samples, 0 sequence gaps, 0 dropped.
  Gain readback: IF GR 20 (AGC at minimum reduction — nothing to hear
  without an antenna), LNA GR 12 (state 4 in the 0–12 MHz row, as the
  table says), system gain 62.6 dB.
- Live `Update`s, each accepted with no gap in the stream: ANT B, ANT C,
  ANT A; LNA state 0 → LNA GR 0 / gain 75.1; LNA state 10 → LNA GR 36 /
  gain 39.2 (table: 36 dB); AGC off + IF GR 59 → GR 59 / gain 23.6; IF GR
  20 → GR 20; AM/FM notch on; DAB notch on; retune 14.074 MHz; decimation 2
  (1.536 MS/s, BW 1.536 MHz): 4 593 525 samples in 3 s, 0 gaps, 0 drops;
  decimation 32 (96 kS/s). `Uninit`, `ReleaseDevice`, `Close`: clean,
  helper exit 0.
- **HDR mode** (`hdrEnable` 1, 875 kHz, 1.7 MHz BW): the delivered rate was
  **1/16 of the decimated rate** — decimation 16 gave ~12 kS/s, decimation 1
  gave **191 961 S/s** (3.072 MHz ÷ 16), decimation 2 ~84–96 kS/s (short
  window), fs 2.0 MHz ÷ 1 ~107–125 kS/s. At fs 6.0 MHz the HDR rate was
  ~2.0 MS/s instead (a different internal path); HermitSDR stays on
  3.072 MHz. In HDR the API reports IF GR 0 and system gain 23.7 dB
  regardless of `gRdB`; the LNA GR followed the HDR row. Turning HDR off at
  1.0 MHz produced a brief near-full-scale transient (peak 32 233, one
  window) before the AGC settled to GR 27.
- No overload event occurred (no antenna). The overload path is exercised
  only by the fake-helper fixture so far.
- **USB descriptor** (`ioreg -p IOUSB`), identical at all three moments —
  before `SelectDevice`, while streaming after `Init`, and after
  `Uninit`/`ReleaseDevice`: idVendor 0x1DF7, idProduct **0x3030**,
  bcdDevice **0x0207** (the issue recorded 0x0200 before the API was
  installed: the service's firmware download ran once at its first start
  and re-enumerated the device then, not during our Init), bDeviceClass
  0xFF, high speed, one configuration, no product string, USB serial
  **F96051EF**; the device's interface 0 is vendor-specific with 3
  endpoints. The service kept pid 27844 throughout, no re-enumeration and
  no multi-second delay on Init: the `fwDownload` path did not run during
  this session.

Still owed on the hardware: a receive session in the GUI app with an
antenna (waterfall + audio at every rate, the I/Q sense against a known
signal, an overload event), the HDR 96 kS/s rate over a longer window, and
the RSPdx-R2.

## RSPduo hardware run — 2026-11-24

Owner's Mac (Apple silicon), SDRplay API **3.15.1** (`com.sdrplay.service`),
RSPduo USB `0x1DF7:0x3020` (empty USB `iSerialNumber`, API serial `1806041B32`,
`hwVer=3`, `tunerMask=3`, `rspDuoMode=7`), 50 Ω antenna on **Tuner 1** only,
receive only with Bias-T off:

- **Direct API 3.15.1 probe (`libsdrplay_api.so.3.15`):**
  - Single-Tuner `3.072 MHz` Zero-IF (`192 kS/s`) + WBZ 1030 kHz sideband sense
    (`+10 kHz` peak at `1.020 MHz`, `-10 kHz` peak at `1.040 MHz`; no I/Q swap).
  - Dual-Tuner synchronous `6.0 MHz` Low-IF `1620 kHz` across `dec = 32, 16, 8, 4, 2, 1`
    (`~62.5 kS/s … 2.0 MS/s`) with matching `firstSampleNum` on Tuner A and Tuner B,
    live independent Tuner B retune, Tuner 1 Hi-Z switch, broadcast notches / ref-out
    updates, and WBZ 1030 kHz LIF sideband sense (`+10 kHz` at `1.020 MHz`,
    `-10 kHz` at `1.040 MHz`).
- **Built helper (`HermitSDR SDRplay Helper`, protocol v2, Debug build):**
  - `hello` v2 (API 3.15), `GetDevices` (`1806041B32`, `hwVer=3`, `tunerMask=3`,
    `valid=true`), `SelectDevice` + `GetDeviceParams` + layout probe (0 mismatches).
  - Single-Tuner `3.072 MHz` streaming across all five rate steps (`dec = 32, 16, 8, 4, 2`
    → `~96 k / 192 k / 384 k / 768 k / 1.536 MS/s`) with 0 sequence gaps and 0 dropped
    samples; WBZ 1030 kHz ZIF sideband sense (`1.020 MHz`: `+10 kHz = -22.1 dBFS` vs
    `-10 kHz = -61.2 dBFS`; `1.040 MHz`: `-10 kHz = -36.1 dBFS` vs `+10 kHz = -99.6 dBFS`);
    LNA gain readback (`0 / 18 / 61 dB` at states `0 / 3 / 6` on `7.074 MHz`); live broadcast
    notches + 24 MHz ref-out updates; live Tuner 1 `50 Ω → Hi-Z` (`rspDuoAmPortSelect`);
    clean Single-Tuner `reselectRspDuo` `A → B → A` (0 gaps, 0 dropped).
  - Dual-Tuner `6.0 MHz / 1620 kHz` LIF `.dualIQ` streaming across all six decimation steps
    (`dec = 32, 16, 8, 4, 2, 1` → `62,496 / 125,055 / 249,984 / 500,220 / 1,008,504 /
    2,003,968 S/s` pairs over 1 s windows) with 0 gaps, 0 dropped, and aligned pairs;
    WBZ 1030 kHz LIF sideband sense (`250 kS/s`, Tuner B at `14.074 MHz`: `1.020 MHz` →
    `A(+10k) = -33.5` vs `-87.3 dBFS`, `B(+10k) = -78.2 dBFS`; `1.040 MHz` →
    `A(-10k) = -33.4` vs `-95.4 dBFS`, `B(+10k) = -79.0 dBFS`); live independent Tuner B
    retune (`14.074 → 7.074 MHz`, 0 gaps/drops); simultaneous A+B retune (`7.074 / 7.074 MHz`,
    0 gaps/drops); live Dual Tuner 1 `Hi-Z` switch (0 gaps/drops); clean Dual → Single return
    (`192 kS/s`, `dual=False`, 0 gaps/drops); clean `Close` + `Bye` (`exit 0`, 0 errors).
  - Bugs/quirks caught and fixed:
    1. Calling `sdrplay_api_SwapRspDuoActiveTuner` out of Tuner 1 Hi-Z wedged `com.sdrplay.service`
       in `libusb` transfer timeouts; `SDRplayHelperRuntime` uses `reselectRspDuo` on Tuner 1 ↔
       Tuner 2 and Single ↔ Dual-Tuner transitions while keeping Tuner 1 `50 Ω ↔ Hi-Z` a live
       `Update`.
    2. An independent post-`dec=1` sample-counter reset on one tuner during Dual-Tuner retuning
       triggered a mutual clear loop between `ring` and `ringB` in `appendDualSamples` while
       `Update(A)` / `Update(B)` fired back-to-back without settling. Fixed with tracked
       `dualSampleOffset` re-anchoring and sequenced per-tuner writes/updates in
       `SDRplayHelperRuntime`.

## Limits

- API 3.15 only; macOS only.
- RSPduo runs Single-Tuner OR Dual-Tuner (SUB or coherent Diversity, not both simultaneously).
- Two-antenna coherent Diversity null depth (requires a second antenna on Tuner 2), Bias-T under DC load, and physical hardware validation of RSP1 / RSP1A / RSP1B / RSP2 / RSPdx-R2 remain unvalidated here.
- HDR mode is RSPdx / RSPdx-R2 only and is not offered above a 192 kHz chain rate.
- The helper process is relaunched at most six times in a row per session.
- Nothing here transmits, and nothing here can.
