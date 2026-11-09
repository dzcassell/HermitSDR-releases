# Offline RDS and RBDS decode

HermitSDR can read station metadata from a raw FM multiplex (MPX) recording or a HermitSDR IQ recording.
For MPX, use a mono WAV sampled at 128–768 kHz, up to two minutes long. The source must
retain the 57 kHz RDS subcarrier. Use the multiplex signal before audio
low-pass filtering, stereo separation or de-emphasis.

Open **Decode → Decode a Recording… → FM Station Info…** for a native
file inspector. Choose the recording, select RDS or North American RBDS,
and set the start and length. Enter a signed offset from capture center
for HermitSDR I/Q. The sheet shows station metadata, traffic and music/speech
flags, the announced UTC clock and local offset, and block and synchronization
statistics. Clock and group-specific flags appear when their groups are received.
Use **Cancel Decode** to stop the file scan.

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
callsign derived from a North American PI in the direct-assignment range
and to interpret programme-type (PTY) codes using the North American RBDS
table. The default uses the RDS table. The JSON includes the numeric code
in `programType` and an English label in `programTypeName` when the code
has an assigned meaning. The numeric PI is included in either mode.
When received, the report includes programme service name, RadioText,
traffic flags, music/speech and the broadcast clock with its announced
local offset. The clock is evidence from the recording. It never changes
the Mac’s clock.

The decoder searches several bit timings, checks the position-specific
syndromes, and can correct an unambiguous burst of up to five bits once
locked. The report shows clean, corrected and rejected blocks and
synchronization losses for the selected timing. The tracked block error rate
divides corrected plus rejected blocks by all tracked blocks and excludes
unlocked search. When block B cannot be decoded, the decoder also counts
the unclassifiable C block as rejected. The per-group totals count fully
decoded groups by type and version, including groups with repaired blocks.
JSON includes these as `trackedBlockErrorRate` (fraction) and `groupCounts`.
The decoder handles stream 0
and displays the basic RDS character set, including accented station names,
Euro and dollar symbols and RadioText line breaks. Use one station per capture.
See [IEC 62106-4 Table 4](https://standards.theiteh.com/catalog/standards/iec/a9170081-7d7e-4d69-b316-231429d024c0/iec-62106-4-2018)
and the [NRSC metadata handbook](https://www.nrscstandards.org/standards-and-guidelines/documents/guidelines/nrsc-g304.pdf).
The offline command opens no radio or network connection.

Synthetic multiplex tests exercised offset, noise and burst corruption
at 128, 192, 228 and 384 kHz. Separate upstream test captures recovered
the YLE YKSI service name and the MiniRDS service name and RadioText.
The same decoder runs live on the receiver's **WFM** mode — see
[Broadcast FM](BroadcastFM.md) for the live path, the stereo decoder and
the region setting. International broadcast character tables remain
follow-up work.

[IEC modulation and baseband coding](https://webstore.iec.ch/en/publication/60236)
[RDS and RBDS programme type tables, Annex F](https://www.nrscstandards.org/standards-and-guidelines/documents/archive/nrsc-4-1998.pdf)
[NRSC RBDS reference](https://www.nrscstandards.org/standards-and-guidelines/documents/archive/nrsc-4-b-standard-2005.pdf)
[Independent test recordings](https://github.com/windytan/redsea/tree/7555c9f6259d50718697ee8c9f218ea012c6892c/test/resources)

## Export FM audio

Use **Export Audio WAV…** from the FM Station Info sheet to save the
selected interval as 48 kHz, 16-bit stereo PCM. It uses the same MPX or
tuned HIQ input as station decoding. With a usable 19 kHz pilot, the
export reconstructs the 38 kHz stereo difference signal. If pilot
reception weakens, the decoder blends toward mono. The sheet reports
how much of the interval held stereo. Choose **RDS** for 50 µs
de-emphasis or **RBDS (North America)** for 75 µs.

```sh
"/Applications/HermitSDR.app/Contents/MacOS/HermitSDR" \
  --hermit-export-fm-audio --deemphasis-us 50 --start-seconds 0 --seconds 10 \
  multiplex.wav new-audio.wav
```

An HIQ input can specify `--offset-hz` relative to the recording center.
The exporter creates a new file only after conversion. The IQ channel
filter needs a few input samples to settle, so an IQ export may be a
few PCM samples shorter than the selected duration. The receipt gives
the exact frame count.

Synthetic MPX and wideband IQ tests verify left/right orientation,
pilot offset, mono fallback, fade recovery, de-emphasis and WAV
integrity. This export processes files offline. Qualification of a
live broadcast receive path still needs a VHF source.
[ITU-R BS.450-4 pilot-tone system](https://www.itu.int/rec/R-REC-BS.450-4-201910-I).
