# QRSS Grabber (#283)

QRSS, DFCW and FSKCW are very slow CW-family beacon modes: a QRSS6 dit is
six seconds long, a dash eighteen, and the whole transmission sits inside a
100 Hz window where ten or twenty stations may share the band at milliwatt
power. Nobody decodes them by ear — the "grabber" is a waterfall with
sub-hertz bins and minutes per screen whose picture is read by eye and
shared. HermitSDR's grabber lives on the demodulated audio of the selected
receiver, so it works with every radio the app supports and with file
replay.

## Where

- **Decode ▸ QRSS Grabber** opens the window (Feature catalog `qrss-grabber`,
  Decode category). Receive only — nothing here can arm or key.
- The worker starts when the window opens and stops when the last copy
  closes; while it is closed the audio tap costs one flag read per block.

## Band presets

The preset menu holds the QRSS watering holes from Scott Harden's public
QRSS frequency table, https://swharden.com/qrss/ (read 2026-10-22), which
mirrors the Knights QRSS community conventions: the centre of each ±100 Hz
window (10 m is ±200 Hz).

| Band | Window centre | USB dial (centre − 1500 Hz) |
| --- | --- | --- |
| 160 m | 1.837900 MHz | 1.836400 |
| 80 m | 3.569900 MHz | 3.568400 |
| 40 m | 7.039900 MHz | 7.038400 |
| 30 m | 10.140000 MHz | 10.138500 |
| 20 m | 14.096900 MHz | 14.095400 |
| 17 m | 18.105900 MHz | 18.104400 |
| 15 m | 21.095900 MHz | 21.094400 |
| 12 m | 24.925900 MHz | 24.924400 |
| 10 m | 28.125700 MHz | 28.124200 |
| 10 m (28.322) | 28.322000 MHz ±500 Hz | 28.320500 |

Choosing a preset puts the audio centre at 1500 Hz; **Tune** also sets
VFO A to the dial above in USB so the window lands at 1500 Hz audio (the
issue's "USB, 1.5 kHz up"). The table's own suggestion is a 1300 Hz tone;
either way the cursor readout shows the RF of whatever is under the pointer.

## Analysis

The demodulated 12 kHz audio is mixed by a complex NCO at the chosen
**Centre** (300–3000 Hz), low-pass filtered (1023-tap windowed sinc,
cut-off at 0.42 of the decimated rate) and decimated by 32 (spans to
300 Hz: a 375 Hz complex window) or 16 (400 / 500 Hz: 750 Hz). The frame is
windowed and transformed with a complex DFT of 512–16384 points at that
rate, and the bins inside ±span/2 are kept.

- **Bin** is expressed as the 12 kHz-equivalent FFT length the issue uses:
  2^14 = 0.73 Hz, 2^15 = 0.37, 2^16 = 0.18 (default), 2^17 = 0.09,
  2^18 = 0.046 Hz. Because the decimation is a power of two, the bin width
  is exactly 12000 / 2^k whatever the span (`QRSSGrabberTests` pins every
  combination).
- **Window**: Hann (default), four-term Blackman-Harris (−92 dB side
  lobes, for strong neighbours) or five-term flat-top (amplitude-accurate
  for comparing signal levels). The dB reference is 0 dBFS for a full-scale
  tone whatever the window.
- **Speed-up** (overlap) ×1, ×2 (default), ×4, ×8: rows per frame length.
  Seconds per row = 2^k / (speed-up × 12000): the default 0.18 Hz bin at ×2
  gives a row every 2.73 s; the finest bin at ×1 one every 21.8 s.
- **Span** 100–500 Hz around the centre. A span wider than 4096 bins pools
  neighbouring bins (maximum) into one stored column.

Rows are quantized to half-dB steps from −125 dBFS and kept in a ring of at
most 2048 rows × 4096 columns (8 MB).

## Display

- **Scroll**: Left (time runs left to right, newest row at the right,
  frequency up the side — the classic grabber picture), Right (newest at the
  left) or Down (time runs top to bottom, frequency across).
- **Minutes** per screen 2–30; the history ring bounds it at 2048 rows, so
  with a fast row rate the effective screen is shorter (the status line shows
  seconds per row).
- **Floor / Ceil** in dB set the palette range (black → blue → cyan →
  yellow → white). They re-paint the stored history; nothing is lost.
- UTC minute ticks (every five minutes past fifteen minutes per screen) and
  round frequency ticks are drawn on the axes. Hovering the picture reads
  back the audio frequency, the RF (dial + audio in USB / DATA-U, dial −
  audio in LSB / DATA-L, dial + audio − pitch in CW) and the UTC time of that
  row to the second.
- The status line reports the bin width, seconds per row, column count,
  the DFT size and rate, rows produced, the last DFT and paint times and
  the audio samples dropped by the input bound (normally 0).

## Pictures and timed capture

**Snapshot** writes the current picture to the capture folder
(`~/Documents/HermitSDR Recordings/QRSS` unless **Folder…** chose another)
as `QRSS-<CALL>-<yyyyMMdd-HHmmss>Z.png` with a frequency scale, the UTC
ticks and a stamp line — callsign and grid, UTC, dial and mode, the RF (or
audio) window, bin width, seconds per row and minutes per screen — repeated
in the PNG's Description field. Small pictures are scaled up by an integer
so a 2^14 screen stays readable. **Reveal** shows the last file in Finder.

**Timed capture** writes a stamped picture at every interval boundary on
the UTC grid (every 2, 5, 10, 15 or 30 minutes, the grabber community's
usual ten-minute cadence by default) while the window is open:

- arming adopts the current slot, so nothing is written the moment the box
  is ticked, and each slot fires exactly once — a late tick after the Mac
  slept fires once for the slot it lands in, never once per missed slot;
- **Keep** bounds the files: beyond N, the oldest `QRSS-…Z.png` files in
  the folder are removed (nothing else in the folder is touched);
- it is off by default, turns itself off when the window closes, and is
  never restored as on at launch.

Nothing is uploaded; publishing a grabber picture is the operator's choice.

## Ownership and cost

`QRSSAnalyzer` (`HermitSDR/DSP/QRSS/`) is fed by the raw-demod tap with
the other decoders. `feed` appends to a 4-second FIFO under one lock and
queues at most one drain on a private serial queue; when the FIFO is full
the oldest audio is dropped and counted. The queue alone owns the NCO,
decimators, DFT scratch, the row history and the rasterizer; frames cross
to the main actor through a `@Sendable` handler, coalesced to two a
second. `QRSSGrabberModel` (main actor) owns the settings (UserDefaults
`qrss.*`), the newest frame and the one-second capture timer. At the
defaults the worker does one 2048-point DFT every 2.7 s and a 375-sample
per-second decimation; the package test reports the measured cost of
60 s of audio and of a full-size paint.

## Tests

`QRSSGrabberTests`: bin width and row period for every bin / speed-up /
span choice; a full-scale tone lands in its bin at 0 dBFS; a synthesized
QRSS6 "CQ" (6 s dits, encoder in the test target) renders as eight
keyed runs with the first dash 13 columns long and the two dashes of the C
separated by the expected 13 columns at 1.37 s per row; a keyed DFCW
"HS" with a 1 Hz shift puts dits and dashes in bins the expected distance
apart; two steady carriers 0.2 Hz apart resolve at the finest bin;
`QRSSCaptureScheduler` fires exactly once per slot and once after a long
gap; the model captures once per slot through its injected writer and
trims the folder to the bound; the FIFO drop count and the disabled tap;
the stamp line and file name; cursor geometry.

## Ask The Crab

`qrss.preset` (band id; also tunes the dial), `qrss.bin` (0.7, 0.35,
0.18, 0.09, 0.05 Hz), `qrss.scroll` (Left / Right / Down), `qrss.minutes`
(2–30) and `qrss.timedCapture` (true / false while the window is open).
