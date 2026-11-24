# Airspy HF+ Discovery, Airspy R2, and Airspy Mini

HermitSDR drives **Airspy HF+ / HF+ Discovery** (`0x03EB:0x800C`) and
**Airspy R2 / Airspy Mini** (`0x1D50:0x60A1`) directly over native macOS USB
(`IOUSBHost`) with **no external driver libraries** (`libairspyhf`,
`libairspy`, or `libusb` are not required), no background daemon, and no
helper process.

All Airspy receivers are **receive-only**: there is no transmitter in the
hardware (`RadioProfile.supportsTX == false`), so ARM, PTT, TUNE, and TX
drive controls remain closed.

## Supported Hardware & Validation Status

| Model | USB VID:PID | Tuning Range | Chain Sample Rates | Hardware Validation |
| --- | --- | --- | --- | --- |
| Airspy HF+ / HF+ Discovery | `0x03EB:0x800C` | 9 kHz – 31 MHz and 64 – 260 MHz on HF+ Discovery | 48, 96, 192, 384, 768 kS/s | **Live-validated** (`hardwareValidated`) on Airspy HF+ Discovery (`R3.0.2-BB`, `SN:C8524E5D8B224A3B`) — see measured results below |
| Airspy R2 | `0x1D50:0x60A1` | 24 MHz – 1.7 GHz | 48, 96, 192, 384, 768, 1536 kS/s | Unvalidated (`conservativeUnknown`) — implemented from BSD-3-Clause wire protocol + clean-room Fs/4 DSP |
| Airspy Mini | `0x1D50:0x60A1` | 24 MHz – 1.7 GHz | 48, 96, 192, 384, 768, 1536 kS/s | Unvalidated (`conservativeUnknown`) — implemented from BSD-3-Clause wire protocol + clean-room Fs/4 DSP |

## Live Hardware Validation (Airspy HF+ Discovery, 2026-11-23)

Verified end-to-end through `AirspyDiscovery`, `AirspyLink`, and `IOUSBHostAirspyTransport` against a live Airspy HF+ Discovery (`0x03EB:0x800C`, firmware `R3.0.2-BB`, antenna connected, receive-only):

- **Discovery & Handshake**: Enumerated at 480 Mbps High-Speed USB; decoded `calPPB = -152`, sample rates `[768000, 384000, 256000, 192000]`, architectures `[Zero-IF, Low-IF, Low-IF, Low-IF]`, and handled stalled optional opcodes (`GET_FREQ_DELTA`, `GET_ATT_STEPS`, `GET_BIAS_TEE_COUNT`) cleanly.
- **Sample Rates**: Streamed fixed 256-sample complex frames cleanly across all 5 chain rates (`48, 96, 192, 384, 768 kHz`) with live switching while streaming.
- **Tuning & Sideband Orientation (`+f = USB`)**: Verified on-air against WBZ (`1030.0 kHz`, 31–34 dB SNR) at both Low-IF (`192 kHz`: `@1030.0k = 0.0 Hz`, `@1030.4k = -375.0 Hz`, `@1040.0k = -9984.4 Hz`) and Zero-IF with `+5 kHz` DSP offset (`768 kHz`: `@1030.0k = 0.0 Hz`, `@1040.0k = -9937.5 Hz`).
- **Front-End Controls & Lifecycle**: Verified monotonic manual attenuation (`0 / -24 / -48 dB` → `-52.3 / -74.0 / -95.7 dBFS`), `+6 dB` HF preamp (`-52.3 → -46.5 dBFS`), and clean `stopStream` → `disconnect` → immediate reconnect.

## Connect and configure

1. Plug the receiver directly into the Mac or a high-speed USB hub.
2. Open HermitSDR’s Connect sheet and select the Airspy USB entry.
3. Use **Settings → Hardware** for gain, attenuation and supported bias-T controls.

HF+ Discovery has separate HF and VHF bands. Stay within the applicable hardware
band when tuning. The HF+ Dual Port and the Discovery use the same USB family.
The hardware measurements here were taken on the Discovery.

## Architecture

1. **Registry-Only Discovery (`AirspyDiscovery`)**: Polls macOS IOKit USB
   descriptors via `USBRegistryProbe` (`kUSBVendorID` / `kUSBProductID`),
   parsing `AIRSPYHF SN:...` / `AIRSPY SN:...` serials into stable
   `airspy:hf:<serial>` or `airspy:one:<serial>` addresses and deterministic
   12-hex pseudo-MACs so per-radio operating profiles track each unit across
   USB ports.
2. **Native User-Space USB Transport (`IOUSBHostAirspyTransport`)**: Opens USB
   Interface 0 directly through Apple's `IOUSBHostInterface`, switches Alternate
   Setting 1 for HF+, clears stalls on Bulk IN endpoint `0x81`, and queues
   deep asynchronous DMA read requests without third-party dependencies.
3. **HF+ / Discovery Link (`AirspyLink`)**:
   - Decodes factory flash calibration (`CONFIG_READ`, `calibration_ppb`) and
     sub-kHz tuning offset (`SET_FREQ` big-endian kHz + fine NCO rotation).
   - Measured on `R3.0.2-BB`: rates `[768000, 384000, 256000, 192000]`,
     architectures `[Zero-IF, Low-IF, Low-IF, Low-IF]`, `calPPB = -152`, and
     wire I/Q pairs `Int16[0] = Q (im)`, `Int16[1] = I (re)` verified on live
     MW/HF carriers (`+f = USB`).
   - Handles optional firmware opcodes (`GET_FREQ_DELTA`, `GET_ATT_STEPS`,
     `GET_BIAS_TEE_COUNT`) gracefully when stalled by older firmware.
   - Zero-IF (`768 kS/s`) offsets the hardware LO `+5 kHz` when DSP shift is
     enabled and removes it digitally to keep DC spike feedthrough away from
     the dial centre.
4. **R2 / Mini Link (`AirspyOneIQConverter` + `ComplexRationalResampler`)**:
   - Uses a clean-room original Accelerate/Swift DC blocker + `Fs_adc / 4`
     43-tap Blackman half-band FIR converter emitting complex I/Q at
     `Fs_iq = 2.5 MS/s` (R2) or `3.0 MS/s` (Mini), followed by half-band
     `ComplexDecimator` stages and HermitSDR's polyphase `ComplexRationalResampler`
     (`384/625` on R2, `64/125` on Mini) into fixed 256-sample frames.
   - Supports 22-step **Linearity** and **Sensitivity** gain tables as well as
     **Manual** LNA / Mixer / VGA sliders and LNA/Mixer AGC toggles.

## Bias-T Safety

- **Bias-T defaults OFF** on all models and never enables automatically on
  connect or restore.
- Enabling Bias-T in **Settings → Hardware** requires fresh confirmation each connection in an
  alert warning about DC voltage on the antenna port.
- Disconnecting an Airspy receiver automatically sends a best-effort Bias-T OFF
  command before closing the USB interface.

Airspy host protocol and gain table attribution is bundled in **About HermitSDR → Licenses**.
