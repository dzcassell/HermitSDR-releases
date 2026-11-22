# Kenwood TH-D75 USB receive and data (development)

Connect the TH-D75 directly by USB. Select **Kenwood TH-D75** in the normal
connection sheet. No Kenwood Windows driver or SDR dongle is needed on macOS.
The adapter matches the USB serial and mono audio interfaces by USB location;
it never substitutes the default microphone or another USB sound card.

The adapter enters Band B / single-band / IF output and uses the radio's
48 kHz mono USB audio stream. A 12 kHz quadrature mixer and image-rejection
filter feed the ordinary HermitSDR I/Q, demodulator, waterfall and recording
paths. The useful RF bandwidth is approximately 15 kHz; the 48 kHz engine
sample rate does not imply a 48 kHz RF window. Start at ×4 zoom (12 kHz).

The radio itself normally shows AM in IF mode and restricts its MODE key.
Choose FM/NFM, USB/LSB, AM/SAM or CW in **HermitSDR**. FM weather reception is
software-demodulated on the Mac while the D75 remains in IF output mode.
WFM broadcast stereo and wideband spectrum scanning cannot fit this IF.
The radio's normal FM audio is available after disconnecting and restoring
its previous output mode.

Tuning uses the D75's CR-terminated `FQ 1,<ten-digit Hz>` command and verifies
readback; it is not the semicolon-terminated desktop Kenwood CAT dialect.
The adapter enables 20 Hz hardware fine tuning. It places the physical IF
center on that grid and uses the ordinary digital mixer for smaller dial
offsets, so the app need not issue off-grid serial commands.
Every tune recenters the narrow IF. The radio's knob is polled once per second
and follows into the app. Receiver failures and lost USB audio disconnect the
session with an explanation; no fallback input is selected.

USB CDC replies require DTR/RTS asserted on the measured D75. These are USB
connection-control signals here, not transmitter controls. An exact command
allowlist excludes PTT, beacons, TNC writes, power control and programming mode.
The profile is receive-only, all transmitter methods are inert, and ARM is
unavailable. Prior IF/band/display state is restored on a normal disconnect.
Opening/closing the serial port alone does not restore state after a crash.

Backlight is set to On during the receiver session and restored on normal
disconnect. The radio's native Auto (DC-IN) setting applies to the DC jack,
not USB. This is an app-session feature, not a setting for every USB charger.

## Levels and RDF

The console reports **USB IF dBFS**, not calibrated antenna dBm. Internal
receiver gain and menu 91A USB audio level affect the samples. Keep menu 91A,
antenna, receiver settings and cabling fixed during a survey. Absolute RF
power and linear relative field-strength tracking are not yet qualified.
The RDF feed preserves raw levels/configuration and flags the D75's unknown
hardware gain; do not use these as calibrated locating evidence.

**Radio → RDF Session → Position → TH-D75 GPS (USB)** reuses the existing
local `.hrdf` journal, offline map, optional Apple Maps and CSV export. Set
menu **981 PC Output (GPS)** to **USB**. New session explicitly enables the
radio's GPS and GGA/RMC output; Stop/disconnect restores its prior GPS output
and sentence mask. Opening a window or connecting RX does not start location
sharing. Coordinates are stored locally only after starting an RDF session.

Missing/invalid/stale fixes become flagged gaps. NMEA checksum, fix status,
coordinate ranges and UTC dates are validated. Altitude, speed and course of
travel are retained when available; course is not antenna heading. GGA HDOP
is not a measured horizontal accuracy. D75 positions carry an explicit unknown
uncertainty flag (the shared location schema uses its conservative 100 km
sentinel), and cannot silently become trusted locating evidence. The map can
still plot the logged route. CSV leaves measured accuracy blank and preserves
quality flags; the map omits an uncertainty circle for this source.

The next field preview adds a pinned 27.385 MHz LSB target/capture workflow,
three-second GPS freshness, per-receiver fixed color scales and an estimated
within-IF channel/background contrast. See [field controls](RDFSession.md#field-controls-next-preview-after-20261120_001).
This contrast is exploratory and does not qualify RF AGC or antenna power.

## Hardware evidence

2026-11-20: macOS enumerated USB VID:PID `2166:9023`, serial
`/dev/cu.usbmodem3101`, audio `ADC stream IN`, mono Float32 48 kHz. Firmware
reported 1.03. Identification, FQ tuning/readback, IF setup, backlight On,
GPS output/restore and no-fix GGA/RMC sentences were exercised on the user's
radio. Eight-second USB captures returned about 384,000 samples with zero
inbox drops. A Debug app connected at 162.475 MHz FM and displayed live IQ.
The operator confirmed both tuning and intelligible weather audio.
Valid satellite fixes, drive-around recording, antenna-power calibration and
road performance remain field checks. See the session handoff for final
software checks and human listening feedback.

Primary references: [Kenwood manual](https://manuals.jvckenwood.com/download/files/B5A-4505-00_01_EN.pdf),
[Kenwood IF specifications](https://www.kenwood.com/usa/com/amateur/th-d75a/),
and [LA3QMA's command documentation](https://github.com/LA3QMA/TH-D74-Kenwood).
D74 notes are leads only: actual D75 behavior wins where they differ.
MD `2` is the observed AM mode. `DL 1` means single-band; BC/DL/MD queries
are refused in IF mode, so an already-active IF session skips them.
MD/IO are never used to select software FM demodulation.


## Native packet / APRS console

Open **Radio → TH-D75 Packet / APRS**. This is a separate exclusive USB
session. The normal receiver profile remains receive-only, and the existing
TCP KISS server remains receive-only; external clients cannot acquire TX.

Disconnect IF reception first. On the radio, select AF instead of IF output
(menu 102), choose the data band (506, default A), tune a permitted packet
channel in FM, select Data Speed (505: 1200 or 9600 bps), choose USB for KISS
(983), then enter KISS with **[F], [LIST]**. Connect USB in the console.
USB CDC line coding and over-the-air data speed are independent. The console
does not send CAT or TNC configuration commands and cannot read back the
actual data-band frequency or speed in KISS mode.

For one packet, enter your callsign/SSID, destination and optional comma-
separated digipeater path. Raw AX.25 UI text accepts 1–256 printable ASCII
bytes. APRS status adds `>` and accepts 1–62 ASCII characters excluding
`|` and `~`, following APRS101. This is a status report, not an addressed
message exchange. Frames use UI control and no-layer-3 PID, with address
extension/C/H bits, KISS escaping and no host FCS; firmware handles RF framing.

Confirm the actual radio frequency, data speed, selected power, TX antenna/
jack and dummy load versus on-air antenna, plus that STA/TX are clear. These
facts are not restored from settings. ARM authorizes one explicit Send via
`TXCoordinator`. Initial frequency scope is 144–148 and 430–450 MHz, further
restricted by the existing operator policy, TX inhibit, build expiry and
station interlocks. The radio's firmware remains responsible for its hardware
protection; KISS supplies no trustworthy SWR/RF-power telemetry.

Sending means **submitted to TNC**, not confirmed on air or delivered.
Firmware can buffer a packet while waiting for a clear channel. Disarm,
disconnect, lost USB and app exit cannot cancel an already queued packet.
The console latches after every submission attempt, including USB write
errors; check the radio's STA (queued data) and TX indicators before explicitly
clearing the latch and reconfirming the next session. No automatic retry,
beacon, message ACK, digipeater or internet forwarding is implemented.

Incoming KISS port-0 data is parsed with a bounded streaming decoder. The
console displays AX.25 source/destination/path and recognizes APRS status,
message, telemetry and standard uncompressed position formats. Ambiguous,
compressed and Mic-E positions are left undecoded. Unsupported frame types
remain visible in the bounded raw log. Up to 250 decoded UI packets and 100
log events remain in memory; there is no automatic disk recording or upload.
Explicit JSON/CSV export saves the retained UI packets, receive timestamps,
raw AX.25 hex and any station-reported coordinates. CSV text neutralizes
spreadsheet formula prefixes. Station-reported positions are not the D75's
GPS fix and never become RDF receiver locations.

Closing the window disarms new submissions but leaves USB reception open.
Disconnect USB before returning the radio from KISS to the IF receiver.
Packet framing, interlocks, queue uncertainty and the native view are tested
locally with fixtures. Actual KISS reception, RF submission and delivery on
the D75 remain operator-assisted hardware tests, requiring session approval.

Primary data references: [Kenwood KISS TNC manual](https://kasc.kenwood.com/files/prod/3692/5/THD75E_User_manuals_English.pdf),
[APRS101](https://www.aprs.org/doc/APRS101.PDF), and
[KISS specification](https://www.ka9q.net/papers/kiss.html).


### Development connection recovery

Receive settings now save per `d75:/dev/cu.usbmodem…` endpoint in the existing
operating catalog. LSB/USB and filter choices survive reconnect/relaunch on that
endpoint. This is a USB endpoint preference, not a verified radio serial: changing
ports/endpoints may create a new first-use profile, and replacing a radio on the
same endpoint can reuse it. New endpoints still start with the original FM default.

The audio watchdog distinguishes nonzero receiver noise from exact-zero-only or
missing capture. It attempts at most two same-device audio restarts, clearing the
old inbox/converter, and disconnects with an explanation if input stays unusable.
It does not choose another microphone, change gain, transmit or restart the app.
The updater-launched all-zero failure observed on November 20 has no established
OS/TCC root cause; this bounded recovery/detection needs operator acceptance on
that launch path. A normal quit/reopen remains the advised fallback if needed.
