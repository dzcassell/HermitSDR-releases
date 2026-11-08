# FlexRadio receive validation

HermitSDR 2026.1108_002 adds a receive-only preview for the FLEX-6300,
6400/6400M, 6500, 6600/6600M, 6700, 8400M, and 8600/8600M. Use SmartSDR 3
or later. The FLEX-8400 is the hardware-tested reference. See the
[bring-up guide](FlexRadioBringUp.md) for installation and troubleshooting.

## On a physical radio

1. Put the Mac and radio on the same LAN, connect the receive antenna to
   ANT 1, and close other SmartSDR clients.
2. Check that HermitSDR discovers the expected model. Connect and tune a
   known signal. Check the waterfall, tuning direction and Mac receive audio.
3. Repeat at 48, 96, and 192 kHz. Check that the waterfall and audio remain
   steady and that disconnecting frees the radio for another client.
4. If a check fails, record the radio model, SmartSDR version, HermitSDR
   version, selected sample rate, and the point of failure. Omit serial
   numbers and local network addresses from reports.

The installed application's `--hermit-flex-probe discover` and
`--hermit-flex-probe info <local-ip>` commands report discovery and
identity details without opening a receive stream.

## Automated receive check for developers

From a source checkout, build the Debug app and use the isolated native
receive check with the radio idle.

```sh
python3 tools/flexradio-app-smoke.py --model FLEX-8600 --host <local-ip> '<path-to-HermitSDR Dev.app>'
```

Replace both placeholders before running the command. The check records
IQ and Mac mixer audio without transmitting.
