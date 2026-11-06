# FlexRadio 8400 bring-up

Choose **FLEX-8400** in HermitSDR's connection sheet when the radio and
Mac are on the same LAN. Connect your receive antenna to **ANT 1** and close
other SmartSDR clients before connecting. Select 48, 96, or 192 kHz in
HermitSDR. Start at 48 kHz if you only need a narrow view; wider rates cover
more of the band and use more CPU and network bandwidth. For an 80 m check,
tune to 3.573 MHz USB to look for FT8. Audio plays through the selected Mac
output device.

If the picker shows **In Use**, close the other client and wait for the next
radio announcement. If the radio is missing, check Local Network access in
System Settings and confirm the Mac and radio are on the same subnet.

This release supports one local receiver on the FLEX-8400 from 100 kHz to
54 MHz. Transmit, additional receivers and antenna inputs, SmartLink, and
other FlexRadio models have not been enabled.

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
disconnect. The receive profile disables transmit.

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
