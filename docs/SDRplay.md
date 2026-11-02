# SDRplay RSPdx

HermitSDR drives the SDRplay RSPdx (and, untested, the RSPdx-R2) as a
**receive-only** USB radio: 1 kHz – 2 GHz, 14-bit, up to 1.536 MHz of chain
bandwidth, three antenna inputs, HDR mode below 2 MHz, bias-T, AM/FM and
DAB notches. There is no transmitter in the hardware, so a connected RSPdx
shows no TX banner, ARM, PTT, TUNE or drive control anywhere; the profile
(`RadioProfile.sdrplayRSPdx`) is receive-only by construction.

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
        └─ stdin: requests · stdout: hello, device list, status, int16 I/Q
             (little-endian frames, protocol v1, SDRplayHelperProtocol.swift)
```

- **Discovery** (`SDRplayDiscovery`) launches the helper when the connect
  sheet is open and asks it for the device list every 3 s. Rows read
  "SDRplay RSPdx" with the API's serial (the RSPdx reports its API serial —
  `2005009343` on the owner's unit — which differs from the USB descriptor's
  serial `F96051EF`; the API serial is the device identity, the USB serial
  appears only in diagnostics). When the helper says the API is missing,
  the wrong version, or its service is not answering, the plugged-in RSPdx
  is still listed from the USB bus (vendor `0x1DF7`, product `0x3030`) with
  the reason and an **Install API…** link; Connect stays disabled.
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
- **Sample rates.** The ADC always runs at 3.072 MHz; every chain rate is a
  decimation of it (96 k ÷32 … 1536 k ÷2), so a rate change is a live
  `Update`, not a restart. 48 kHz takes the radio's 96 kS/s through one host
  decimate-by-2. The IF filter follows the rate (200 k / 200 k / 300 k /
  600 k / 1.536 M) unless pinned narrower in Settings.
- **HDR mode** (below 2 MHz) parks the tuner on one of the ten fixed HDR
  centres (135, 175, 220, 250, 340, 475, 516, 875, 1125, 1900 kHz) and the
  link rotates the I/Q by the difference so the display still shows the
  dial. The HDR path delivers a sixteenth of the normal rate (measured; see
  below), so HDR is offered at chain rates up to 192 kHz and the link asks
  for decimation ÷16.
- **Gain.** The RF gain slider is the LNA gain reduction (0 … −84 dB); the
  link lands it on the band's nearest `LNAstate` using the specification's
  table (Settings shows the state and its dB for the current band). IF gain
  reduction (20–59 dB) and the API's AGC (off / 5 / 50 / 100 Hz) are in the
  SDRplay section; with the AGC on, the readback shows what it chose.
- **Overload.** `sdrplay_api_PowerOverloadChange` events light and clear the
  header's ADC OVF lamp (the helper acknowledges each one as the API
  requires).
- **I/Q** arrives as int16 (full scale ±32767) and is scaled to ±1.0. The API
  delivers I then Q; `SDRplayLink.conjugateIQ` flips the sense if a live
  check shows a mirrored spectrum (none did on the first run's noise floor;
  a known on-air signal is the test).

## Settings ▸ SDRplay RSPdx

| Control | API field | Notes |
| --- | --- | --- |
| Antenna A / B / C | `rspDxParams.antennaSel` | A and B are the SMA inputs (1 kHz – 2 GHz); C is the BNC for below 200 MHz. |
| LNA state | `gain.LNAstate` | Per-band table from the specification (0–12 MHz has 19 states, 60–250 MHz 27, …). Shared with the RF gain slider. |
| IF gain reduction | `gain.gRdB` | 20–59 dB; greyed while the AGC is on. |
| AGC | `agc.enable`, `setPoint_dBfs` | Off / 5 / 50 / 100 Hz loop; set-point −30 dBFS. |
| HDR mode + bandwidth | `rspDxParams.hdrEnable`, `rspDxTunerParams.hdrBw` | Below 2 MHz, chain rate ≤ 192 kHz; 200 k / 500 k / 1.2 M / 1.7 M. |
| Bias-T on ANT B | `rspDxParams.biasTEnable` | Off by default, confirmation before on, forced off when the antenna is not B. |
| AM/FM notch, DAB notch | `rfNotchEnable`, `rfDabNotchEnable` | The RSPdx's switchable broadcast notches. |
| IF bandwidth | `tunerParams.bwType` | Auto (widest inside the rate) or a narrower pin. |

Every choice is saved per device serial (the operating catalog's
`sdrplayFrontEnd`), like the NetSDR's front-end fields. The diagnostics line
shows API version, stream state, the IF and LNA gain reduction the API
reports, ADC overload, delivered rate, samples the helper dropped and helper
restarts.

Not exposed: the RSPdx has no API field for a reference output
(`sdrplay_api_RspDxParamsT` carries none; only the RSP2/RSPduo have
`extRefOutputEn`), so there is no "reference out" toggle. The RSPdx-R2 uses
the same structures and should work unchanged but has not been seen.

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

## Limits

- API 3.15 only; macOS only; one tuner (no sub-receiver hardware slice;
  SUB stays off).
- HDR mode above 192 kHz chain rate is not offered.
- The helper process is relaunched at most six times in a row per session.
- No reference-output control (not in the API for the RSPdx).
- Nothing here transmits, and nothing here can.
