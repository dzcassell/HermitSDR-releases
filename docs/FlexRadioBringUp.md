# FlexRadio bring-up

Choose your **FlexRadio model** in HermitSDR's connection sheet when the radio and
Mac are on the same LAN. Connect your receive antenna to **ANT 1** and close
other SmartSDR clients before connecting. Select 48, 96, or 192 kHz in
HermitSDR. Start at 48 kHz if you only need a narrow view; wider rates cover
more of the band and use more CPU and network bandwidth. For an 80 m check,
tune to 3.573 MHz USB to look for FT8. Audio plays through the selected Mac
output device.

If the picker shows **In Use**, close the other client and wait for the next
radio announcement. If the radio is missing, check Local Network access in
System Settings and confirm the Mac and radio are on the same subnet.

HermitSDR opens one local DAX IQ receiver on ANT 1 from 100 kHz to 54 MHz
with SmartSDR 3 or later. The FLEX-8400 is hardware-tested. The FLEX-6300,
6400/M, 6500, 6600/M, 6700, 8400M, and 8600/M have a receive-only
preview through the same path. Their antenna and sample-rate behavior still
needs physical verification. The native receive check in the
[validation guide](FlexRadioValidation.md) accepts the advertised model via
`--model`, for example `--model FLEX-8600`.

Transmit on ANT 1 or ANT 2 is bench-validated for the FLEX-8400 running
SmartSDR 4.3.16.42034. Since 2026.1108_003 the same transmit path is
offered on every other supported model (FLEX-6300, 6400/M, 6500, 6600/M,
6700, 8400M, 8600/M) running SmartSDR 3 or later, on the assumption that
those radios follow the same SmartSDR slice, transmit, DAX TX and
interlock contract as the 8400. HermitSDR has not been tested on that
hardware: the connection sheet labels such a radio **TX ASSUMED**, and the
first keyed test on each model belongs on a dummy load with the station
ready to stop RF. Every over still verifies the radio's reported power
ceiling, antenna, mode, DAX slice rate, interlock owner and a finite radio
TX timeout before PTT, and the host ends an over after at most 55 seconds.

The driver selects USB, LSB, AM, FM, NFM, DIGU or DIGL from the console and
uses the radio's reported power limit. Microphone and Input Mixer supply the
DAX audio at the slice rate the radio reports (24 kHz on the 8400; 48 kHz
slices are also accepted). TUNE uses the radio's carrier, and TWO TONE is
available in USB and LSB. The app verifies a radio timeout of at most 60
seconds before PTT; a shorter existing radio timeout takes precedence. The
waterfall pauses during PTT and resumes after release.

CW works from the same keyer, paddles, keyboard and CAT `send_morse` path
as on the other radios, with one difference: a FLEX generates the CW
carrier itself. HermitSDR opens a CW slice, turns the radio's break-in
off for the over, sets the radio's CW pitch and speed to the HermitSDR
keyer settings, holds MOX exactly as for a voice over and sends the
radio a key-down or key-up command on every edge of the host keyer. You
hear HermitSDR's own sidetone; the radio's sidetone setting is not
changed. The radio's break-in setting is restored when the over ends.
The slice takes a moment to come up at the start of every over, so the
first elements of an over may not reach the antenna. Set a longer
transmit hang in the keyer (around one second) so an over does not end
between characters. This CW path was keyed into a dummy load on the FLEX-8400 on
2026-11-08 (see the [validation guide](FlexRadioValidation.md)); it has
not been used on the air yet.

During a Flex over the console power and SWR meters, the TX window's PWR
and SWR cells and the PA temperature cell read the radio's own transmitter
meters rather than a detector bridge. After `client gui` HermitSDR asks the
radio for its `meter list`, keeps only the transmitter (`TX`) meters named
FWDPWR, REFPWR, SWR and PATEMP, and subscribes to just those with
`sub meter <id>`; the values arrive about ten times a second on the same
UDP socket as DAX IQ and are released with `unsub meter all` at disconnect.
Forward and reflected power are converted from the radio's dBm to watts, SWR
is the radio's ratio (derived from forward and reflected power only if the
radio has no SWR meter), and PA temperature is live whenever meters are
fresh, in receive too. Power and SWR show only while HermitSDR itself holds
the over; they read zero or a dash outside it, after two seconds without a
meter packet, and after disconnect. Because the watts come from the radio,
**PWR CAL** and the detector-volt FWD/REV cells do not apply to a Flex (the
cells show a dash) and the wattmeter uses the 100 W scale. SWR protection
uses the same meters: three consecutive readings above the configured limit
at one watt or more of forward power release PTT and report the cause. The
radio's own SWR and thermal protection stay in force underneath.

The command-line probe is available for discovery and identity checks.
With the radio powered on and the Mac on the same LAN, run these commands
in Terminal. Substitute the address from discovery or SmartSDR and adjust
the application path if you installed it elsewhere.

```sh
"/Applications/HermitSDR.app/Contents/MacOS/HermitSDR" --hermit-flex-probe discover
"/Applications/HermitSDR.app/Contents/MacOS/HermitSDR" --hermit-flex-probe info 192.168.1.40
```

Discovery listens on UDP 4992 for four seconds. An empty array means no
valid announcement arrived during that window. Check the same subnet and
macOS Local Network access. The probe reports the source address of the
announcement and does not follow the advertised address. Identity opens
TCP 4992 to the supplied local IPv4 address and sends only `info` and
`version`. It reports the API version, the model if reported, and component versions and
closes the connection. When sharing discovery output, omit the serial.

Live bring-up confirmed UDP discovery and read-only TCP identity on a
FLEX-8400 running SmartSDR 4.3.16.42034 with protocol 1.4.0.0.

HermitSDR registers its UDP port on its own SmartSDR GUI connection and
routes the selected DAX IQ stream into the same receiver, waterfall and Mac
audio paths used by the other supported radios. It tracks the panadapter
and stream IDs returned by the radio and removes those resources on
disconnect. The radio performs USB modulation from the app’s processed DAX TX audio.

The live 48 kHz test used ANT 1 and a 3.570 MHz center. The radio initially
restored a saved 3.800 MHz center after panadapter creation. A subsequent
explicit center command returned 3.570 MHz. The stream creation reply
returned a bare hexadecimal ID, while status reported the same ID with
a `0x` prefix. Both stream and panadapter removals were acknowledged.

The production decoder accepted 9,070 class `0x02E4` packets with 176
little-endian I/Q pairs per packet and no gaps visible in the four-bit
packet sequence. At 3.573 MHz USB, HermitSDR decoded 11 FT8 messages in
33.26 seconds from the original I/Q order and zero after conjugation.
The decoder's division by 32,768 yielded a complex RMS of 0.0256 and a
peak component of 1.026. Absolute RF level was not calibrated.

The live receiver check used the FLEX-8400, ANT 1 and the 80 m dipole.
At 3.573 MHz USB, the production engine delivered 2,674 IQ packets in ten
seconds with no sequence errors. The isolated Metal view received 289
spectrum rows and acquired 708 drawables. Steady row gaps stayed under
40 ms. A 500 Hz center change paused rows for about 243 ms before updates
resumed. The Mac's output mixer produced 10.2 seconds of audio at 44.1 kHz.
The mixer tap measured a peak of 0.064 and RMS of 0.025 at the test volume.
Core Audio reported one shortfall and reprime during the retune interval.

A follow-up hardware test switched from 48 to 96 to 192 kHz and back to
48 kHz without disconnecting. All four intervals delivered live Metal
waterfall rows and IQ, with zero packet sequence errors. The radio can
briefly send old-rate packets after acknowledging a rate change; HermitSDR
drops them before the new DSP chain. Rate changes paused new waterfall rows
for up to 442 ms, and a center retune paused them for 223 ms in this run.
Mac audio resumed after brief output ring reprimes.

An eight-minute link test at 192 kHz delivered 523,963 IQ packets with no
gaps detected by the packet sequence. A reconnect at 48 kHz delivered another
8,254 packets in 30 seconds with no detected gaps. The normal app then
discovered the radio and recorded 35 seconds at 3.573 MHz USB and 96 kHz.
The recording had the expected 96 kHz header, and HermitSDR found six FT8
spots when decoding it offline. The Mac mixer produced audio during the
native app run.

FlexRadio's API documentation covers control framing and DAX stream
commands. The vendor's current SDK resolves discovery-port ambiguity in
the older wiki and provides a reference for the packet formats. The Swift
implementation adds no SDK dependency or vendor source.

- [SmartSDR TCP/IP API](https://github.com/flexradio/smartsdr-api-docs/wiki/SmartSDR-TCPIP-API)
- [Discovery protocol](https://github.com/flexradio/smartsdr-api-docs/wiki/Discovery-protocol)
- [Client and resource ownership commands](https://github.com/flexradio/smartsdr-api-docs/wiki/TCPIP-client)
- [DAX stream commands](https://github.com/flexradio/smartsdr-api-docs/wiki/TCPIP-stream)
- [FlexLib 4.3.16 vendor reference](https://www.flexradio.com/software/smartsdr-v4-x-api-flexlib/)

## Station accessories: TX relays, antenna tuner, TX filter

These three features drive the radio's own accessory hardware over the
SmartSDR API. They are assumed from the API documentation and FlexLib's
command forms and have **not** been checked on a radio yet (see the
validation guide); the loopback mock exercises every command and read-back.
All three are offered only when the connected model is transmit-eligible.

**TX relays.** A FlexRadio has no host-driven open-collector pins. Its rear
panel offers the TX1, TX2 and TX3 RCA relays and the ACC connector's TX
line, which the radio closes on its own PTT once each is enabled. HermitSDR
maps its per-radio OC output matrix (Settings ▸ OC outputs) onto those
enables while it is connected: OC1 → TX1, OC2 → TX2, OC3 → TX3 and OC4 →
ACC TX, taken from the *transmit* row for the current band (the receive row
has no relay to drive, and OC5–OC7 have no Flex equivalent). While a TUNE
pulse is asserted the TUNE mask is ORed in exactly as on the openHPSDR
radios, so an auto-tuner start line wired to a relay behaves the same way,
and the relay opens again when the pulse ends. The link writes only the
enables that differ from what the radio reports, one `interlock
tx1_enabled=<0|1>` … `acc_tx_enabled=<0|1>` command each, before every over
and whenever the band or the matrix changes, and reads the interlock status
back; an unconfirmed write is logged, never fatal. On disconnect the enables
the radio had before the session are put back, so SmartSDR's own station
setup survives a HermitSDR session (a cable pull cannot restore them). The
relay sequencing delays (`tx1_delay` …) and the RCA/ACC TX *request* inputs
are never written — set those in SmartSDR; the OC tune-pulse durations are
pulse lengths, not lead times, so they are not mapped onto the delays.

**Antenna tuner.** When the radio reports a fitted internal tuner
(`atu_present=1` on the radio-wide status, after `sub radio all` and `sub atu
all`), the TX controls gain **ATU TUNE** and **ATU BYPASS** beside TUNE and
2 TONE, with the radio's status word (`ATU READY`, `ATU TUNING`, `ATU
MATCHED (MEM)`, `ATU BYPASS`, `ATU FAILED` …) beside them. ATU TUNE is RF:
the *radio* keys its own tune carrier through the tuner at the TUNE drive
setting, so it takes the same gates as TUNE — ARM on, policy clear, nothing
else keyed. SmartSDR requires a transmit slice and a READY interlock for
`atu start`, so the link prepares the cycle exactly like a TUNE over (slice
at the TX frequency and jack, `tunepower` at the drive setting, inhibit
released), sends `atu start`, watches the `atu status` word until it leaves
`TUNE_IN_PROGRESS` (5 s if the tuner never starts, 30 s hard limit followed
by `atu bypass`), and then releases exactly like an over: inhibit, power and
timeout restored, slice removed, receiver reopened. A HermitSDR over cannot
start while the tuner runs and the tuner cannot start during an over. ATU
BYPASS sends `atu bypass`; it keys nothing. Tuner memories are left as
SmartSDR has them.

**TX filter.** For a voice or data over in USB, LSB, DIGU or DIGL the link
programs the radio's transmit filter from the TX profile passband the
TXChain is filtering with — `transmit set filter_low=<Hz> filter_high=<Hz>`,
for example 300–2900 Hz for the Studio SSB profiles or 200–3000 Hz for the
Digital profile — and requires the `transmit lo=… hi=…` read-back to match
before PTT and throughout the over. The radio's previous edges are restored
at release together with `rfpower`, `tunepower` and `dax`. AM, FM and NFM
have no operator-programmable TX filter in SmartSDR and are left alone, as
are TUNE and TWO TONE. Lab profiles wider than the API's 10 kHz bound are
clamped to it; if the radio reports different edges than requested the over
is refused rather than sent with the wrong filter.

