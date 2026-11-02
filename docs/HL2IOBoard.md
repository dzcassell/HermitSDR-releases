# N2ADR IO Board band-follow (Hermes-Lite 2)

HermitSDR can write the transmit frequency to the **N2ADR IO Board** inside a
Hermes-Lite 2 over the radio's Protocol 1 I2C bridge. The board's firmware
turns that frequency into band data for whatever is wired to it — an
amplifier's CAT port, open-collector band lines, FT-817 / Xiegu band volts,
an antenna switch or a transverter. The option is **off by default** and it
never keys, arms or changes drive: the only thing HermitSDR writes is the
frequency.

Requested by Justin AI5OS (public issue #11), who runs an HL2 with the IO
Board's `m0hpf_spe` firmware driving an SPE Expert 2K-FA. Everything below
about the register path was verified against the board's published firmware
and reference software; the first hardware run with HermitSDR is his.

## What is written, and when

| Event | What HermitSDR sends |
|---|---|
| Option turned on, or a radio connected with it on | Identity probe: read I2C address `0x41`, register 0. A board answers `0xF1` (hardware version 1). Then the firmware version is read from `0x1D` registers 9–10 and the current transmit frequency is written. |
| Any transmit-frequency change — VFO tune, band jump, split on/off or VFO B tune while split, XIT, CAT tune, transverter profile change | One burst of five single-byte writes to `0x1D` registers **0, 1, 2, 3, 4**: the frequency in hertz as a 40-bit integer, most significant byte first. Register 4 is written last; that is the write the Pico acts on. |
| Stream restart or reconnect | Probe again and resend the frequency once the board answers. |
| Receive-only operation | Same as above. The amplifier follows the dial before the first key-down and in radios whose transmitter is closed. |

Bursts are coalesced: while you spin the dial the newest frequency goes out
at most every 50 ms, so the amplifier is never asked to change band twenty
times a second. Bridge frames are only sent while receiving, never during
the key-down sequence or while keyed, and at most one per control-register
cycle, so the normal filter-board, LNA and NCO registers keep their timing.
With the option **off**, not one byte of the wire changes.

The frequency written is the **RF** transmit frequency: VFO A, or VFO B when
split is on, plus XIT when it is engaged, with the transverter offset
included when a transverter profile is active (the IO Board README asks for
the frequency "including the transverter offset").

### Protocol detail (for the curious)

HL2 gateware exposes two I2C buses through control registers `0x3C` (bus 1)
and `0x3D` (bus 2). The IO Board sits on bus 2 (the 2x20 companion header).
A write frame is `C0 = 0x7A`, `C1 = 0x06` (write cookie), `C2 = 0x1D`
(7-bit address), `C3 = register`, `C4 = data`. The identity probe is
`C0 = 0xFA` (request bit set), `C1 = 0x07` (read cookie), `C2 = 0x41`,
`C3 = 0x00`; the radio answers in a status frame with bit 7 of C0 set and
the four bytes read in C1–C4. Sources: the HL2 wiki *Protocol* page,
`gateware/rtl/i2c_bus2.v`, and `i2c_registers.h`, `i2c_slave_handler.c`
and `software/hermeslite.py` in the IO Board repository
(github.com/jimahlstrom/HL2IOBoard).

## Setup

1. **Fit the IO Board** on the HL2's 2x20 header (above the N2ADR filter
   board if one is installed). It replaces the jumper that connects the main
   board to the filter board; the two boards are independent.
2. **Flash firmware** for your application (`build/main.uf2` in the matching
   folder of the IO Board repository): power the HL2 off, hold the Pico's
   button, plug its USB into a computer, copy the `.uf2` to the drive that
   appears, unplug, power the HL2 on. The Pico LED flashes slowly when the
   firmware runs and faster when it receives I2C traffic from HermitSDR.
3. **Wire the board** for your firmware. For `m0hpf_spe` (SPE Expert over
   RS-232): J4 pin 1 (Out1) → TTL-in and J8 pin 1 (In1) ← TTL-out of a
   MAX3232 module (HW-027 or similar), its RS-232 side to the DB-9 (J7 pins
   2 / 3 / 5). Cable: DB-15 (amplifier) pin 1 → DB-9 pin 2, pin 9 → pin 3,
   pin 4 → pin 5 — the same wiring as an SPE Yaesu CAT cable.
4. **Amplifier settings** used by AI5OS on the SPE Expert 2K-FA, input 1:
   CAT type **YAESU, FTxxxx 2007+**, **19200 baud** (the firmware README
   also lists FLEX). The firmware sends a Kenwood-style
   `IF…;` frequency string whenever the frequency changes and answers the
   amplifier's `IF;` polls.
5. In HermitSDR, connect to the HL2, open **Settings › Radio** and turn on
   **N2ADR IO Board band-follow (TX frequency over I2C)**. The line under
   the switch shows the probe result:
   - *IO Board detected — hardware v1, firmware 1.1 — last sent 14.200000 MHz*
   - *IO Board not detected* — the `0x41` identity register did not answer.
   - *Looking for the IO Board…* — the probe is in flight (a second at most).

   The choice is remembered per radio; a radio that has no saved choice
   starts with it off.

## Troubleshooting

- **Not detected.** Check that the board is fully seated on the 2x20 header
  and that the HL2 gateware is a recent build (the I2C bridge has been in
  the gateware since well before 70; AI5OS runs 74.2). The identity register
  is answered by the board's hardware even when no firmware is loaded, so
  "not detected" is a seating or bus problem, not a firmware one.
- **Detected, firmware "not reported".** The Pico has no firmware or an
  older one that does not set `firmware_version_major/minor`. Flash the
  firmware for your application.
- **Detected, amplifier does not follow.** Watch the Pico LED: it should
  flicker on every tune. If it does, the I2C path is fine and the problem is
  the firmware's output — wiring from Out1/In1 to the level converter, the
  DB-9 cable, or the amplifier's CAT type / baud rate. With `m0hpf_spe` the
  string goes out at 19200 8N1; the amplifier must be set the same.
- **Band changes while transmitting.** HermitSDR holds band-follow writes
  while the transmitter is keyed and sends the newest frequency after
  unkey. If the amplifier changes band under RF, something else is driving
  it.
- **Diagnostics.** The unified log (`log show --predicate 'subsystem ==
  "com.hermitsdr.app" AND category == "hpsdr"' --info`) records every probe
  result and every frequency written ("IO Board: TX frequency … Hz written
  to 0x1D registers 0–4").

## What this is not

The option writes accessory band data and nothing else. It does not key,
arm or set drive, it does not read the amplifier back, and it does not use
the IO Board's antenna-tuner, fan or RX-input registers. The N2ADR filter
board is still driven through the open-collector bits (Settings › Radio ›
Filter Board); the two never interfere. Band-data drivers for amplifiers on
a Mac USB-serial adapter remain in Station Devices.
