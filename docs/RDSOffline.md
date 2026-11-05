# Offline RDS and RBDS decode

HermitSDR can read station metadata from a raw FM multiplex (MPX) recording or a HermitSDR IQ recording.
For MPX, use a mono WAV sampled at 128–768 kHz, up to two minutes long. The source must
retain the 57 kHz RDS subcarrier. Use the multiplex signal before audio
low-pass filtering, stereo separation or de-emphasis.

Run the installed app executable in a terminal.

```sh
"/Applications/HermitSDR.app/Contents/MacOS/HermitSDR" \
  --hermit-decode-rds multiplex.wav
```

For a `.hiq` recording sampled at 384 kHz or higher, specify the station's
offset from the recording center in hertz. The selected station must have
at least 105 kHz of capture bandwidth on each side. A positive offset
selects a station above center.

```sh
"/Applications/HermitSDR.app/Contents/MacOS/HermitSDR" \
  --hermit-decode-rds --offset-hz 45000 --start-seconds 0.25 --seconds 8 recording.hiq
```

Both formats default to the first 30 seconds. Set `--start-seconds` and
`--seconds` to select a window of up to two minutes.

Add `--rbds` before the file to include the possible four-letter US
callsign derived from a North American PI in the direct-assignment range.
The numeric PI and programme-type code are included in either mode.
When received, the report includes programme service name, RadioText,
traffic flags, music/speech and the broadcast clock with its announced
local offset. The clock is evidence from the recording. It never changes
the Mac’s clock.

The decoder searches several bit timings, checks the position-specific
syndromes, and can correct an unambiguous burst of up to five bits once
locked. The report shows clean, corrected and rejected blocks and
synchronization losses for the selected timing. It decodes stream 0
and displays the common ASCII text subset. Use one station per capture.
The offline command opens no radio or network connection.

Synthetic multiplex tests exercised offset, noise and burst corruption
at 128, 192, 228 and 384 kHz. Separate upstream test captures recovered
the YLE YKSI service name and the MiniRDS service name and RadioText.
Live wideband FM and international broadcast character tables are
follow-up work.

[IEC modulation and baseband coding](https://webstore.iec.ch/en/publication/60236)
[NRSC RBDS reference](https://www.nrscstandards.org/standards-and-guidelines/documents/archive/nrsc-4-b-standard-2005.pdf)
[Independent test recordings](https://github.com/windytan/redsea/tree/7555c9f6259d50718697ee8c9f218ea012c6892c/test/resources)
