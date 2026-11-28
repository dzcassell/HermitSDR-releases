# rtl_tcp network receiver

HermitSDR can receive from an **rtl_tcp-compatible server**: a small program
that sits next to an RTL-SDR dongle (often on a Raspberry Pi at the antenna)
and sends its samples over the network. The dongle does not have to be
plugged into the Mac.

This is the first part of "network receivers" (#472). KiwiSDR / Web-888 is
a separate connect scheme (`kiwi://…`, see [KiwiSDR.md](KiwiSDR.md)).
SpyServer is not built yet.

It is **receive-only**. No transmitter object exists for an rtl_tcp server:
ARM, PTT, TUNE and drive stay closed.

> **Heard on a local server (2026-11-27).** Pre-review build was heard live
> against `rtl_tcp://127.0.0.1:1234` with a Realtek RTL2838UHIDIR (`SN:
> 00000001`, R820T tuner) at `1.536 MS/s` for normal receive and `2.0 MS/s`
> (`2000000.052982 Hz` reported by the dongle) while `Decode ADS-B` was active
> at `1090 MHz`, including live 1090 MHz decodes. Post-review changes are tested
> against the loopback server and synthetic IQ only. Expect differences; please
> report them.

## Connect

1. Start the server on the machine with the dongle, listening on an address
   the Mac can reach. Most servers listen only on the machine itself unless
   told otherwise.
2. In HermitSDR open **Connect** and type the address into **Direct IP
   connection**, with the `rtl_tcp://` prefix:

   | You type | Meaning |
   | --- | --- |
   | `rtl_tcp://192.168.1.50` | port 1234, the usual default |
   | `rtl_tcp://shack-pi.local:1235` | a name and another port |
   | `rtl_tcp://[fe80::1]:1234` | an IPv6 address |

   The prefix is what tells HermitSDR this is not an openHPSDR radio. There
   is no discovery: the address is always typed.
3. Press Return. The address is remembered.

An rtl_tcp server serves **one client at a time**. If another program is
connected, the server accepts the connection and then says nothing; HermitSDR
gives up after three seconds and says so.

Connecting can hold the window for a few seconds if the server does not
answer (up to 2 s to look up a name, 4 s to connect, 3 s for the greeting).

## What to expect

- **Tuning range** is whatever the dongle's tuner covers, typically about
  24 MHz to 1.7 GHz. For HF, turn on **Direct sampling** (below) or use an
  upconverter. HermitSDR lets you tune from 10 kHz to 2.2 GHz and leaves the
  limits to the server.
- **Sample rates** 48 kHz to 1536 kHz. The server usually runs at 1.536 MS/s
  and the Mac decimates. The samples are only 8-bit, and every halving of the
  rate recovers about 3 dB of dynamic range, so narrower spans are cleaner.
  **Reduced network rate** asks for 240 kS/s at 48 kHz or 288 kS/s at 96 kHz.
  While ADS-B is on, the dongle stays at 2.0 MS/s and that switch does not
  lower the rate.
- **Network load** is about 3 MB/s (25 Mbit/s) at 1.536 MS/s. On Wi-Fi or a
  remote link turn on **Reduced network rate**.
- **The S-meter is not calibrated** for this receiver: the tuner's gain in dB
  is not known, so the reading is relative.
- The console's **RF gain slider does nothing** here. Gain is in Settings.

## Settings › Hardware › rtl_tcp server

The section appears while an rtl_tcp server is connected. Settings are
remembered per server address.

| Control | What it does |
| --- | --- |
| Status line | Server, the tuner type number and gain-step count from its greeting, the two sample rates, ADC overload, and samples dropped. |
| Manual tuner gain | Off: the tuner's own automatic gain. On: a gain step from lowest to highest. The server reports how many steps there are, not their values. |
| RTL2832 digital AGC | The chip's own digital gain correction. Usually off. |
| Direct sampling | Off, I input or Q input. Bypasses the tuner for reception below about 24 MHz. Which input is wired depends on the dongle. |
| Correction | Crystal error in ppm, −200 to +200. |
| Swap I/Q | For a mirrored spectrum. |
| Remove DC | Removes the spike in the middle of the span. |
| Reduced network rate | At 48 and 96 kHz asks the server for 240 or 288 kS/s: about a sixth of the traffic, roughly 8 dB less dynamic range. While ADS-B is on, the dongle stays at 2.0 MS/s. |
| Bias tee | DC on the dongle's antenna jack. See below. |

Everything is off or automatic until you change it.

### Bias tee

The bias tee puts DC on the antenna jack to power an active antenna or LNA.
It can damage a passive antenna, splitter or transformer.

- It is **off at every connection**: HermitSDR sends "off" as part of
  connecting, even if the server was started with it on.
- Turning it on asks for confirmation each time, and the confirmation counts
  only for the connection you are looking at.
- It is never saved, and HermitSDR sends "off" when you disconnect.
- The server does not report whether the dongle has a bias tee or whether the
  command worked. If the Mac loses the network while it is on, it stays on at
  the dongle until the server is restarted or another client turns it off.

## When things go wrong

| What you see | Meaning |
| --- | --- |
| "…sent no rtl_tcp greeting" | Another client is connected, or it is not an rtl_tcp server. |
| "…is not an rtl_tcp server" | Something else is listening on that port. |
| "The rtl_tcp server closed the connection." | The server stopped or dropped this client. Connect again. |
| "The connection to the rtl_tcp server was lost: …" | The network path failed or the server reset the connection. Connect again. |
| "The rtl_tcp server stopped sending samples." | Nothing arrived for 5 seconds. |
| "samples dropped" in the status line, Seq errors climbing | The Mac could not keep up, so it threw samples away rather than fall behind. Use a lower sample rate. |

HermitSDR does not reconnect by itself.

If the Mac falls behind, at most half a second of samples waits in memory;
anything more is dropped in whole blocks and counted. Each burst of drops
counts as one sequence error in the status bar and clears the time-machine
history, because the timeline has a hole.

Changing the sample rate throws away what was already on its way at the old
rate (0.3 s after the server is told). On a very slow link a little old-rate
data could still slip through as a brief burst of noise.

## What is not there

- Auto-reconnect, discovery, and a list of saved servers.
- Tuner names: the greeting carries a tuner type *number*, and no public
  non-GPL description of the numbering was found, so the number is shown.
- Gain in dB: only the number of gain steps is known.
- IF-stage gain, offset tuning, test mode and the crystal-frequency commands.
- A network receiver as the SUB receiver beside a local radio (#472).
- Checks against a real server or dongle, including I/Q order, whether sample
  alignment survives a rate change, and the bias-tee command.

## For developers

- `HermitSDR/Protocol/RTLTCP/RTLTCPProtocol.swift`: greeting and command
  codec, address parsing, rate plan, 8-bit conversion, `RTLTCPIngress`.
- `HermitSDR/Protocol/RTLTCP/RTLTCPLink.swift`: the `HPSDRLink`.
- `Tests/DSPTests/RTLTCPLoopbackServer.swift` and `RTLTCPTests.swift`.

The wire protocol as implemented: the server sends 12 bytes (`RTL0`, tuner
type, gain count; 32-bit big-endian) and then interleaved unsigned 8-bit I, Q
(127.5 is zero). The client sends 5-byte commands, one id byte and a 32-bit
big-endian value:

| Id | Command | Value |
| --- | --- | --- |
| 0x01 | Centre frequency | Hz |
| 0x02 | Sample rate | I/Q pairs per second |
| 0x03 | Tuner gain mode | 0 automatic, 1 manual |
| 0x04 | Tuner gain | tenths of a dB (used only when no gain list is reported) |
| 0x05 | Frequency correction | ppm, two's complement |
| 0x08 | RTL2832 digital AGC | 0 / 1 |
| 0x09 | Direct sampling | 0 off, 1 I, 2 Q |
| 0x0d | Tuner gain by index | index into the tuner's gain list |
| 0x0e | Bias tee | 0 / 1 |

**Licensing.** rtl-sdr, librtlsdr and rtl_tcp are GPL. Their source was not
read. The table above comes from public prose descriptions of the protocol.
Sending a negative correction as two's complement is this project's reading
of "correction in ppm", not something a description states.
