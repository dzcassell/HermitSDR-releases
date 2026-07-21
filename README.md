# HermitSDR

A native macOS client for openHPSDR software-defined radios —
**Hermes-Lite 2 / SquareSDR** (Protocol 1) and **Apache Labs ANAN**
Orion-class radios (Protocol 2). Built for Apple silicon: SwiftUI +
Metal on the outside, Accelerate/vDSP DSP and a lock-free audio path on
the inside.

This is the **download home** for HermitSDR. Grab the latest signed,
notarized build from the [**Releases**](../../releases/latest) page.

> **Availability**: HermitSDR is not made available for use in the
> Russian Federation while Russia's war against Ukraine continues.
> Слава Україні. 🇺🇦

## Download & install

1. Open the [latest release](../../releases/latest) and download
   **`HermitSDR-<version>.dmg`** (or the `.zip`).
2. Open the `.dmg` and drag **HermitSDR** to your Applications folder.
3. Launch it. The build is signed with an Apple Developer ID and
   notarized by Apple, so it opens without any "unidentified developer"
   warning.
4. On first launch, grant the **Local Network** permission when macOS
   asks — discovery and streaming need it.

## Requirements

- Apple silicon Mac (M1 or newer)
- macOS 15 (Sequoia) or newer
- An openHPSDR radio on your LAN (Ethernet recommended):
  **Hermes-Lite 2 / SquareSDR**, or an **Apache Labs ANAN / Orion-class**
  radio on Protocol 2 firmware (an ANAN-7000DLE MK2 on fw 2.2.10 is the
  reference)

## What it does

- **Two radio families, one app** — dual-protocol discovery, receive and
  transmit on both stacks (transmit validated on a dummy load;
  on-air use is yours to enable)
- **Demodulation** — USB, LSB, CW, AM, and synchronous AM, at sample
  rates up to 1536 kHz on Protocol 2
- **A GPU waterfall** — an 8192-bin Metal display with phosphor
  persistence, bloom, seventeen palettes, and a 3D height-field mode
  with a live-aurora sky driven by the real planetary K-index
- **Decoders** — FT8/FT4 (with PSKReporter uploads), SSTV (14 modes),
  weather fax, CW, and configurable RTTY, plus **OmniSkimmer**, a GPU
  channelizer that skims every CW and RTTY signal across the whole span
  at once
- **Spotting & logging** — a multi-node DX cluster client with a
  waterfall ticker, LoTW badges and TQSL upload, and an in-app QSO log
- **A full transmit chain** — broadcast-grade audio processing, TX
  metering, two-tone IMD analysis, and hamlib CAT for WSJT-X
- **Instruments** — an analog multimeter, GPU TX meters, a lightning
  static-crash watch, an RF "time machine" that replays the last few
  minutes of the band, and an optional Discord integration

## Privacy

HermitSDR sends one anonymous usage ping per day (turn it off in
Settings ▸ Privacy): a random install ID, the app version, the macOS
version, and the CPU type — nothing else. No callsigns, frequencies,
audio, or radio data ever leave your Mac.

---

Built by **WU1T**. Questions and bug reports are welcome on the
[issue tracker](../../issues).
