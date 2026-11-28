# 1090 MHz Mode S / ADS-B Decoder

HermitSDR includes a receive-only **1090 MHz Mode S / ADS-B** Extended Squitter decoder (`Decode ▸ Text & Messaging ▸ ADS-B (1090 MHz)`).

> **Sources & Provenance:**
> - **How it was written:** The decoder (`ADSBProtocol.swift`, `ADSBModem.swift`, `ADSBEngine.swift`, `ADSBView.swift`, the wideband raw-IQ tap, the map layer, offline decode and the tests) was written with AI coding assistants under the direction of the contributor, rezolytics: Google Antigravity / Gemini for the first version, and Cursor for the fixes after the first review. It was written from general knowledge of the public Mode S / Extended Squitter specifications (**ICAO Annex 10 Volume IV** and **RTCA DO-260B / EUROCAE ED-102A**).
> - **No third-party decoder source:** The contributor states that no third-party ADS-B decoder source (`dump1090`, `readsb`, `pyModeS`, `rtl_adsb` and the like) and no GPL `librtlsdr` / `rtl_tcp` source was read, copied or put into prompts. A separate `rtl_tcp` program, built outside this repository, ran the USB dongle during his live test.
> - **Later fixes:** The changes made on this branch after his last commit (the test messages, the position gates, the hover help and smaller items) were made by the integrator's AI agent from the review notes, under the same rule: no third-party decoder source was opened.
> - **Test messages:** The known-answer messages in `Tests/DSPTests/ADSBDecoderTests.swift` are constructed in that file from field values chosen there, with the expected results worked out by hand from the field layout in a comment above each one. They are not taken from a book, a decoder or a recording. The contributor's first version reused four worked examples that also appear in Junzi Sun, *The 1090 Megahertz Riddle: A Guide to Decoding Mode S and ADS-B Signals*, 2nd edition, TU Delft OPEN Publishing, 2021, DOI [10.34641/mg.11](https://doi.org/10.34641/mg.11), <https://mode-s.org/1090mhz/>. That book is licensed CC BY-NC-SA 4.0 (attribution, non-commercial, share-alike), not CC BY 4.0, so those four messages were replaced before merge. The 64-character table in `ADSBProtocol.swift` is the 6-bit character set of the identification message, with `#` standing for unused codes.

> **Verification status:** Pre-review build was **live-verified on hardware (2026-11-27)** at `rtl_tcp://127.0.0.1:1234` on a Realtek RTL2838UHIDIR (`SN: 00000001`, Rafael Micro R820T tuner) — connecting at `1,536,000 Hz` for smooth receive audio and switching the dongle to `2,000,000 Hz` (`2000000.052982 Hz` reported by `rtl_tcp`) when tuned to `1,090,000,000 Hz` with `Decode ADS-B` active, yielding live 1090 MHz decodes. Post-review fixes (`e25b8772` and later commits), SDRplay single-tuner `3.072 MS/s` raw IQ tap, and offline `.hiq` ADS-B decoding are verified on synthetic fixtures and unit tests only.

---

## Architecture & Sample-Rate Tap

1090 ES frames use 2 Mbps Manchester-encoded Pulse Position Modulation (1 µs bit cell with a 0.5 µs pulse), preceded by an 8 µs four-pulse preamble (`0.0, 1.0, 3.5, 4.5 µs`). Reliable demodulation requires at least a **2.0 MS/s** complex envelope around **1090.000 MHz**.

- **RTL-SDR (`rtl_tcp://`):** While `Decode ADS-B` is active, `RTLTCPLink` requests a `2_000_000 Hz` device sample rate and forwards raw converted I/Q blocks to `ADSBEngine` before DC removal and CIC decimation down to the host waterfall/audio rate. **Reduced network rate does not lower that.** With ADS-B on, a 48 kHz host rate stays at 2.0 MS/s on the dongle instead of dropping to 240 kS/s. Disconnecting clears the tap, so the next connection is not left at 2.0 MS/s.
- **SDRplay (single-tuner):** While `Decode ADS-B` is active on a single-tuner session, `SDRplayLink` runs the hardware ADC/front-end at `3_072_000 Hz`, taps raw I/Q blocks into `ADSBEngine`, and decimates in host DSP down to the selected panadapter/audio rate. `ADSBDetector` resamples ≥ 2.0 MS/s envelopes down to its 2.0 MS/s slicer timeline.
- **Panadapter and audio invariance:** Changing the ADS-B toggle leaves your host waterfall/audio sample rate unchanged, and no real-time audio/DSP thread ever waits on `ADSBEngine` (`0.5 s` bounded chunk queue with drop counter).

---

## Decoded Frames & Fields

- **CRC-24:** Generator polynomial `0xFFF409` plus single-bit error correction on 112-bit DF17 / DF18 frames via syndrome lookup.
- **DF11 (All-Call Reply):** 24-bit ICAO address discovery and capability bits.
- **DF17 / DF18 (Extended Squitter):**
  - **TC 1–4:** Aircraft callsign and emitter category.
  - **TC 5–8:** Surface position (CPR even/odd), ground speed, and track.
  - **TC 9–18:** Airborne position with Compact Position Reporting (CPR) and barometric altitude (Q-bit 25 ft increments or Gillham Mode C decoding).
  - **TC 19:** Subtypes 1–2 are ground speed and track. Subtypes 3–4 are airspeed and heading; they are not stored as a ground speed or a track. Vertical rate is in fpm.
  - **TC 20–22:** Airborne position with GNSS height. The 12-bit field uses the same Q-bit 25 ft encoding as barometric altitude.
  - **DF5 / DF21 squawk:** 13 bits, MSB first, `C1 A1 C2 A2 C4 A4 X B1 D1 B2 D2 B4 D4`. `0x0AAA` is 7700.
  - **Emitter category:** `(3,3)` is Parachutist. `(3,4)` is Ultralight.
- **CPR:** The first position comes only from an even frame and an odd frame within 10 s (global, airborne). A later single frame may resolve locally against that aircraft's own last fix, but only while that fix is less than 300 s old. After that the decoder waits for a new even/odd pair. One frame plus the station grid is not a position. Surface global CPR is not implemented, so a surface track does not get a first fix from CPR. A southern surface reference folds latitude by 90° only when the folded value is closer to the reference. A fix more than 500 km from the station grid, or one that implies more than 1,200 kt since the previous fix (with 2 s of allowance on the interval), is dropped. When a position from a pair contradicts the stored fix it is held back, and if the next pair agrees with it the stored fix is replaced and the trail restarts there, so one bad fix cannot lock out the right ones.
- **Frame times:** Each frame is timed from its place in the sample stream, not from the moment the decoder got round to it, so frames decoded in one batch keep their real spacing.
- **DF4 / DF5 / DF20 / DF21** are accepted only when that ICAO was heard on an unrepaired DF11 or DF17 in the last 60 seconds. A single-bit repair does not create a new aircraft.

---

## UI, Map, Offline Decode & Export

- **ADS-B (1090 MHz) window:** Displays tuned frequency status (with a one-click `Tune 1090 MHz` helper if off frequency), live frame/preamble/CRC/drop statistics, an **Aircraft** table (`ICAO`, `Callsign`, `Alt (ft)`, `Spd (kt)`, `Hdg`, `V/S`, `Dist / Brg`, `Lat / Lon`, `Msgs`, `SNR`, `Age`), and a **Messages** tab showing raw hex frames and parsed summaries. Exports aircraft tables as **CSV** and **JSON**.
- **Stations Heard map:** Adds a toggleable **ADS-B** layer (`teal` oriented aircraft symbols with short flight trails and altitude labels).
- **Decode a Recording:** Select `.adsb` (`ADS-B (1090 MHz)`) on IQ recordings captured at ≥ 1.9 MS/s sample rate.

---

## Receive only

HermitSDR never transmits on 1090 MHz. The preamble detector, the pulse-position slicer, the CRC-24 and single-bit repair, and the CPR position solver are Swift in this repository. No third-party ADS-B library is linked (see **Sources & Provenance** above).
