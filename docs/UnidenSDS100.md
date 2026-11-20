# Uniden SDS100 USB receive control and RDF (development)

Open **Radio → Uniden SDS100…**, or choose **Uniden SDS100 → Open controls…**
in the connection panel, then **Connect**. The connection-panel entry remains
visible when USB setup is needed and refreshes passive detection every two seconds. This independent scanner instrument can run
alongside the primary SDR receiver; it does not replace its IQ/audio connection.
Connect the SDS100's **mini-USB PC data** jack to the Mac using a data cable.
At the scanner's USB prompt press **./no** for **Serial Port**. Mass Storage
is for SD-card access, not this connection. Refer to the connector label and
shape rather than an upper/lower description.

Discovery is passive IOKit matching of VID:PID `1965:001a`, product name
`SDS100 Serial Port` and a callout serial interface. Connect verifies `MDL,SDS100`
and reads `VER`/`GSI`; it never opens the D75, MOTU M4 or the scanner's other
USB interface. The measured macOS interface was `/dev/cu.usbmodem103201`.
No third-party driver or package dependency is added.

## Receive controls and data

Connecting only reads status. **Tune / hold** sends `QSH` with the Uniden
100 Hz frequency units, enters Quick Search Hold and verifies frequency
readback. Hardware band restrictions still apply. Volume/squelch controls
address the scanner itself, range 0–15, and verify their readback. Disconnect
leaves the scanner's chosen receive state in place; it does not attempt to
reconstruct an earlier scan session or alter Favorites/avoids. No programming,
power-off, recording, discovery/database write or raw-DSP command is allowed.

The scanner panel reports its current frequency, channel, system, department,
site, modulation, squelch state, raw RSSI, and available digital/talkgroup/unit-ID
metadata. GSI XML is size/depth/attribute bounded; external entities/DTDs are
refused. Status is polled at 4 Hz on a private serial queue. Wire receipt uptime
is retained across the UI callback so delayed main-actor delivery cannot make
old power look fresh. Lost USB or invalid status disconnects explicitly.

Firmware 1.23.15 returned RSSI −95/−96 on NWS 162.475 MHz and −999 while scanning
without a usable strength reading. The −999 sentinel stays in raw metadata
and is never plotted or exported as measured power. The public specification
also shows older RSSI representations. RSSI is therefore retained in a separate
**scannerRSSI (unqualified)** unit, not labelled dBm or dBFS. No noise-floor,
SNR, physical RF gain, filter width or IQ sample rate is invented. Unknown
filter/rate/gain fields are qualified in the journal and blank in CSV exports.

Audio plays on the scanner's own speaker, as chosen by the operator. The
initial status read had volume 0. Use the scanner's knob or native volume
control for listening. This implementation supplies no USB live audio/IQ
stream or software DMR/P25 decoder. Uniden's public SDS specification marks
raw discriminator output removed on SDS100. Licensed waterfall FFT and
recorded-audio transfer interfaces need separate validation; this integration
does not synthesize a waterfall from RSSI or buy/enable scanner upgrades.

## Additional RDF receiver layer

Connecting the scanner registers its own snapshot provider with the RDF model.
Open RDF, select the desired signal, reuse a speaker tag, start a session and
press **Sample here** to save the primary receiver and connected SDS100 in one
host-time batch. **Select this signal in RDF…** chooses the scanner's reported
channel as the target without tuning the primary radio. A receiver on another
frequency stays flagged off-target. This does not separate co-channel speakers
or turn a radio unit-ID number into a verified person's identity.

By default enter the SDS100 antenna's own coordinates and uncertainty in its
window. The scanner's configured `LCR`/ZIP-based scanning location is not read
as a live GPS fix. Alternatively explicitly check that both antennas are
**co-located with the primary RDF antenna**. Only that choice shares the
primary session's GPS/manual position and age/source; the row records which
receiver supplied the shared position. With a missing/stale primary fix,
the scanner row remains a gap as well. No position is silently borrowed. The scanner can also record with its own
entered coordinates while the primary SDR is disconnected; the inactive
primary remains a flagged gap instead of requiring fabricated coordinates.

The default map **Per receiver** units can show D75 IF dBFS and SDS100 RSSI
as separate named, independently scaled overlays. Receiver/signal/tag/setup
filters keep comparisons scoped. Never compare their colors as calibrated
absolute field strength. Receiver metadata, measured-unit labels, batch IDs,
position-sharing provenance and quality flags survive journal save/reopen,
CSV and GeoJSON. Older journals remain readable by the new app; older preview
versions can reject new multi-source/unknown-filter records.

## Evidence and limits

Live on 2026-11-20: USB enumeration, `MDL,SDS100`, `VER,Version 1.23.15`, GSI/GST
status and repeated native background polling were verified without changing
scanner tuning/volume/squelch. The production scanner model fed real RSSI and
metadata through the actual RDF recorder/journal and reopened them with
`noPosition` flags, not fabricated coordinates. The D75 weather preview stayed
running. Protocol/parser, unknown-unit/export and explicit-co-location tests
cover data admission; production views use inert display fixtures for renders.
Live tune/hold and changed speaker settings, satellite fixes, drive surveys,
calibration and a combined interactive app session still need operator checks.

A live receive-only acceptance tool is available:

```
tools/sds100-receive-live-smoke.sh
```

It requires exactly one SDS100 in Serial Port mode, sends only identification/
status queries, exercises native polling and a temporary no-position RDF journal,
and leaves receive settings unchanged. It must not run while the native scanner
window owns that serial port. CI runs pure tests/render fixtures instead.

Primary references: [Uniden owner's manual](https://www.uniden.info/download/ompdf/SDS100om.pdf)
and [SDS-series remote command specification v2.00](https://info.uniden.com/twiki/pub/UnidenMan4/SDS100FirmwareUpdate/SDS_Series_RemoteCommand_Specification_V2_00.pdf).
