# Carrier Sleuth

**Decode → Carrier Sleuth** (#282) draws a narrow, sub-hertz waterfall of
every medium-wave channel in a Band DVR segment or any `.hiq` recording —
one per 9 kHz or 10 kHz channel (or a list of your own), stacked in a
scrollable grid. Over an hour, the carrier of a broadcast station is a
fingerprint: its offset from nominal, its thermal drift, its sign-on and
sign-off, the fade pattern of a co-channel station the ear cannot separate.
Nothing here touches the live receiver: the window reads a file, runs FFTs
on its own queue, and writes pictures.

## Using it

1. **Recording.** *Choose…* a `.hiq` file or pick a segment from the *Band
   DVR* menu. The recording's centre, span, rate, length and UTC start are
   shown; the channel plan below updates with it. A DVR segment rolls every
   five minutes by default, so for an hour of carriers record with
   Receiver → Record (IQ) or export a longer DVR interval first.
2. **Channels.** *9 kHz* is ITU Regions 1 and 3 (long wave 153–279 kHz and
   medium wave 531–1602 kHz); *10 kHz* is Region 2 (530–1700 kHz); *Custom*
   takes kHz separated by commas or spaces. Only channels whose whole window
   lies inside the recorded span are analysed; the readout says how many.
3. **Width** (±50, ±100, ±150, ±200 Hz) is the half-width of each channel's
   waterfall. **FFT** (2^14 … 2^24 points) sets the frequency resolution and
   the time one row spans; **Speed-up** moves the next row by that multiple
   of the FFT length — ⅛× overlaps eight rows per window, 8× skips seven
   windows between rows. The line beside the pickers shows the row length
   and the millihertz per bin for the current choice.
4. **Analyse.** Progress runs through *Fingerprinting*, *Channelising* (one
   pass over the file) and *Transforming* (the long FFTs). *Cancel* stops at
   the next block and leaves nothing behind. A recording analysed before
   with the same parameters loads from the cache in well under a second.

### Reading the grid

- Each cell is one channel: oldest row at the top, −width on the left,
  nominal carrier in the middle (the tick), +width on the right. The label
  gives the channel and, after the kHz, the carrier's **offset from
  nominal** — the median of every row's strongest bin at full FFT
  resolution. Type a **note** in the label line; notes are stored per
  recording and survive a cache clear.
- **Time markers** are drawn from the recording clock (the `.hiq` header's
  start time plus the samples consumed): hourly when the recording spans
  three hours or more, every ten minutes above twenty minutes, otherwise
  every minute, labelled `HH:MMZ`.
- Hover for the **cursor readout** in the status line: Hz offset from the
  nominal carrier and the UTC time of that row.
- **Min / Max dB** set the palette's floor and ceiling (dBFS of a unit
  carrier); *Auto* puts the floor 6 dB under the median cell and the ceiling
  at the strongest, bounded to the sliders' -160…+20 dB range with at least
  10 dB of contrast. Silence therefore stays inside the native controls
  (#292). **Up to N across** chooses the maximum columns; the grid
  uses fewer when the window or the offsets pane leaves less space. Every
  channel stays inside the scrollable grid.
- Click a cell for the **detail** view underneath: the channel at one pixel
  per column (4096 columns, ≤ 0.1 Hz each) with the same markers and readout.
- **Offsets** opens the carrier-offset table (kHz, offset, strongest level,
  rows, note); *Copy table* puts it on the clipboard as TSV.
- **Export PNG…** writes the whole grid with the title line, labels, ticks,
  markers and notes drawn in; the PNG's `Description` carries the recording
  name, UTC start, length, centre, rate, raster, width, FFT, speed-up,
  resolution, row length, channel count and fingerprint. **Copy** puts the
  same PNG on the clipboard. The export is a pure function of the cached
  result and the display settings, so exporting the same analysis twice
  gives identical bytes.

## How it works

The job (`HermitSDR/Recording/CarrierSleuth.swift`) owns one serial queue;
every buffer, file handle and FFT setup is a local of that queue's run, so a
finished or cancelled job holds nothing. Two streamed stages:

1. **Channelise.** The file is read once in blocks of L samples, where L is
   the power of two that makes L/fs ≈ 0.68 s — so every FFT bin is
   12000/8192 ≈ 1.465 Hz whatever the recorded rate (8192 points at
   12 kS/s, 2^20 at 1536 kS/s). One L-point FFT per block; for each channel
   the K bins around its carrier (96, 192, 256 or 384 for ±50…±200 Hz,
   raised-cosine-tapered from the passband edge to the channel edge) are
   inverse-transformed to K samples at fs·K/L (140.6 … 562.5 Hz) and
   appended to a per-channel spill file in the temporary directory.
   Overlap-save with a quarter-block overlap discards the circularly
   wrapped edges of each block. The carrier's residual from the bin centre
   (at most ±0.73 Hz) is corrected when the display window is cut, not by a
   per-sample mixer. Working memory is a few L-sample buffers plus a
   256 KB write buffer per channel; the spill files are removed when the
   job ends, whatever the outcome.
2. **Transform.** Channel by channel — a bounded number at a time, chosen
   so the workers' buffers (3 × N floats each) stay under 512 MB — the
   spill stream is Hann-windowed in windows of N = 2^FFT samples advanced
   by N × speed-up, FFT'd, converted to dBFS (0 dB = a unit carrier), and
   the ±width bins of each row are **max-pooled** into 4096 columns (a
   narrow carrier survives pooling; averaging would dim it) and stored as
   16-bit floats. The strongest bin of every row is kept at full
   resolution for the offset table. Rows are bounded: when a recording
   would produce more rows than fit 256 MB across all channels (at most
   1024 per channel), the hop widens and the status line says
   *rows limited by the memory budget*. A recording shorter than one
   window is zero-padded to a single row whose time is the centre of the
   data present.

Resolution and row length for the fixed decimated rates:

| Width | Rate | 2^14 | 2^16 | 2^18 | 2^20 | 2^22 | 2^24 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ±50 Hz | 140.6 Hz | 8.6 mHz · 117 s | 2.1 mHz · 7.8 min | 0.54 mHz · 31 min | 0.13 mHz · 2.1 h | 34 µHz · 8.3 h | 8 µHz · 33 h |
| ±100 Hz | 281.3 Hz | 17 mHz · 58 s | 4.3 mHz · 3.9 min | 1.1 mHz · 16 min | 0.27 mHz · 1.0 h | 67 µHz · 4.1 h | 17 µHz · 17 h |
| ±150 Hz | 375 Hz | 23 mHz · 44 s | 5.7 mHz · 2.9 min | 1.4 mHz · 12 min | 0.36 mHz · 47 min | 89 µHz · 3.1 h | 22 µHz · 12 h |
| ±200 Hz | 562.5 Hz | 34 mHz · 29 s | 8.6 mHz · 1.9 min | 2.1 mHz · 7.8 min | 0.54 mHz · 31 min | 0.13 mHz · 2.1 h | 34 µHz · 8.3 h |

The long settings (2^20 and above) suit recordings of several hours; for
a five-minute DVR segment choose 2^14–2^16 with a fractional speed-up.

### Cache

Results are written under `Application Support/HermitSDR/CarrierSleuth/`
as `<key>.sleuth` (a JSON header plus the raw cells), where the key is the
SHA-256 of the recording's **fingerprint** and the canonical parameters.
The fingerprint is the SHA-256 of the file size and 1 MiB from the start,
middle and end of the file (the header's microsecond start time is in the
first sample), so a renamed or copied recording hits and a different one
misses without hashing gigabytes. The folder is bounded to 512 MB:
after every write the least recently loaded entries are removed until it
fits (a hit refreshes an entry's date). *Clear Cache* empties it; notes
live in `CarrierSleuth/Notes/<fingerprint>.json` and are not cleared.

### Boundaries

- Receive only. The job reads one file; it never opens a socket, keys,
  tunes or touches `RadioEngine`, `RXChain`, the IQ history ring or the
  speakers (`CarrierSleuthTests.testEngineNeverTouchesTheLiveChain` pins
  the sources). It is tallied into no real-time counter.
- Nothing leaves the Mac: no upload, no network fetch; the PNG metadata
  holds only the facts listed above.
- Window preferences (raster, width, FFT, speed-up, custom list, grid
  width) persist in the app's defaults; the dB range follows each result.

## Measured (Mac mini M4 Pro, 2026-10-22, Debug `-Onone` test build)

`CarrierSleuthTests` synthesizes a 20-minute 24 kS/s recording (230 MB)
centred on 1000 kHz: three carriers 0.3 Hz apart on 1000 kHz (amplitudes
0.30 / 0.20 / 0.15, the weakest signing off at minute 10), a carrier
drifting −1 → +1 Hz on 1010 kHz, a steady carrier 0.4 Hz low on 990 kHz,
white noise at −50 dBFS per sample. With ±200 Hz, 2^16 points and ¼×
speed-up (8.6 mHz per bin, 116 s per row, 29 s hop, 40 rows holding at
least half a window): every row resolves the three carriers with ≥ 20 dB
between them, the peak bin sits on 0.00 Hz within 0.02 Hz, the drifting
carrier's peak follows the ramp within 0.15 Hz row by row, the sign-off is
visible in every row whose window starts after minute 10 (≥ 25 dB down)
and absent in none before it, the 990 kHz offset reads −0.400 ± 0.02 Hz,
and the strongest carrier reads −10.5 ± 1.5 dBFS. The whole job — one
pass over 230 MB plus 120 long FFTs — takes 0.5–0.8 s; the cache hit that
follows loads the same result in a few milliseconds and compares equal.

Memory (opt-in `HERMITSDR_SLEUTH_BIG=1`, process footprint sampled every
20 ms while the job runs, 10 kHz raster = 39 channels, ±200 Hz, 2^18, ⅛×):
a 1.08 GB 384 kS/s recording (350 s) computes in 2.3 s with a peak of
+229 MB over the test process's baseline; a 2.15 GB recording (700 s, the
issue's acceptance case) computes in 4.4 s at +290 MB. The difference is
the per-worker channel streams of stage two (twelve workers × 3.2 MB);
the stage-one buffers do not grow with the file. The first measurement
read the file through `FileHandle.read(upToCount:)` and peaked at
+1290 MB — the whole file — because that API returns autoreleased
`NSData` that a dispatch block releases only when it returns; the job now
reads and writes with `read(2)` / `write(2)` into reusable buffers
(`CarrierSleuthRawFile`).
