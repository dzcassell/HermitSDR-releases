# Importing and exporting I/Q recordings (#280, #296)

HermitSDR's own I/Q format is `.hiq` (`HermitSDR/Recording/IQFile.swift`: a
28/40-byte header — rate, centre, start time, transverter mapping — then
Float32 I,Q pairs). It is unchanged by this feature and stays canonical.
Other receivers and programs record I/Q as a **two-channel RIFF/WAVE file**
(I left, Q right) and keep the centre frequency and start time somewhere
else: a chunk, the file name, or nowhere. This document says which of those
HermitSDR reads, how a foreign file is mapped onto the `.hiq` replay path,
and the limits. Local **SigMF** metadata/sample sibling pairs are also
supported; the scoped import/export behavior is described below.

Everything in `HermitSDR/Recording/IQImport.swift` was written from the
public layouts cited below. No code, table, string or interface was taken
from any other program; the Black Cat Systems products named in the issue
were surveyed from their public web pages only and never run.

## Confirmed export selection (#301)

The native DVR and SigMF export panels show the complete on-disk sample
prefix captured for their preview. Leaving End blank saves that previewed
prefix; samples appended while the panel is open are excluded. Partial
selections use the same preview and retain their first-sample UTC.

The export worker rechecks the recording identity, header and available
sample count before copying. If the source was replaced, its header changed,
or it became shorter than the preview, saving is refused and the destination
is preserved. Preview the recording again to choose from its current content.

## Where the files open

- **File ▸ Open IQ Recording…** (and the connect sheet's *Open IQ
  Recording…*) accepts `.hiq`, `.wav`, and either member of a conventional
  `.sigmf-meta` / `.sigmf-data` pair. An imported file replays through the
  full receiver exactly like a `.hiq`: the dial tunes anywhere in the
  recorded span, the Band DVR timeline scrubs it, the time machine and the
  live decoders see it as live IQ.
- **Decode ▸ Decode a Recording…** (#264) accepts the same files and runs
  them through one decoder faster than real time. A mono WAV, or a stereo
  WAV named the way HermitSDR's own audio recorder names files
  (`yyyyMMdd-HHmmss_…`), is still audio; for a stereo WAV without an I/Q
  marker the open sheet offers **Treat as Audio**.
- **Demodulated audio export** of an imported file is the existing path:
  replay it, then record audio with the header's audio record button or
  the time machine's excerpt export (`WaveTapRecorder`, 16-bit WAV in
  `~/Documents/HermitSDR Recordings`). Nothing new was added for it.

## The open sheet

A file that carries its own centre and start (an `auxi` chunk, an SDR# /
SDR++ / KiwiSDR name, a `kiwi` stamp) opens with **no prompt** — the
receiver tunes to the recorded centre. Otherwise a small modal sheet shows
the whole-file overview — format, encoding, channels, the file's rate,
duration, and the chain rate it will play at (with the resampling ratio) —
and asks for:

- **Centre (MHz)** — the frequency at the middle of the recorded span.
- **Start (UTC)** — `yyyy-MM-dd HH:mm:ss`; pre-filled with the file's
  modification date minus its duration when nothing better is known.
- **Swap I and Q** — for recorders that write Q first (the spectrum would
  otherwise appear mirrored).

The answer is written beside the file as **`<name>.wav.hiqmeta`** (JSON:
`centerHz`, `sampleRate`, `startedAt` ISO-8601, `format`, `source`,
`swapIQ`, `version`), so the file is asked about once. Values a file
carries itself are written to the sidecar too, and a sidecar always wins
over the file. On a read-only volume the values are kept for the session
only. Delete the sidecar to be asked again.

## Formats and what is read

| Source | Marker | Centre | Start | Notes |
| --- | --- | --- | --- | --- |
| RFSpace / SpectraVue, SdrDx, HDSDR, SDRuno, Elad SW2 | `auxi` chunk | `auxi` centre field | `auxi` start SYSTEMTIME (UTC) | Stop time, A/D rate, IF and bandwidth are parsed and shown; the `fmt` rate rules. |
| SDR# | name `SDRSharp_yyyyMMdd_HHmmssZ_<Hz>_IQ.wav` | name | name (UTC) | 8-bit unsigned, 16-bit, 24-bit, 32-bit PCM or 32-bit float. |
| SDR++ | name `baseband_<Hz>Hz_HH-mm-ss_dd-MM-yyyy.wav` | name | name (local time) | A name with only the `baseband_<Hz>Hz` part gives the centre; the start is asked. |
| Perseus (Microtelecom) | `rcvr` chunk and/or a name with `<n>kHz` / `<n>Hz` | `rcvr` or name | `yyyyMMdd_HHmmss` in the name (read as UTC) | See *Perseus* below. |
| KiwiSDR browser / kiwirecorder | `kiwi` chunk(s) and/or name `<host>_yyyy-MM-ddTHH-mm-ssZ_<kHz>_iq.wav` | name (kHz) | first `kiwi` GPS stamp, else name (UTC) | Many small `data` chunks, one per packet, stream as one recording. 12 kHz plays at 48 kHz (×4). |
| Anything else | two channels | asked | asked | Written to the sidecar. |

### RFSpace `auxi` chunk

Layout as published in the SpectraVue user guide's "RIFF WAVE file
format" appendix (chunk id `auxi`, 164 bytes, little-endian):

| Offset | Size | Field |
| --- | --- | --- |
| 0 | 16 | start time — Windows SYSTEMTIME: eight UInt16 (year, month, day-of-week, day, hour, minute, second, millisecond), UTC |
| 16 | 16 | stop time, same layout |
| 32 | 4 | centre frequency, Hz |
| 36 | 4 | A/D sample frequency, Hz |
| 40 | 4 | IF frequency, Hz |
| 44 | 4 | bandwidth, Hz |
| 48 | 4 | I/Q offset |
| 52 | 4 | dB offset |
| 56 | 4 | maximum value |
| 60 | 8 | unused |
| 68 | 96 | next file name |

HermitSDR needs the first 48 bytes and accepts a chunk that stops there.
An all-zero start time means "no clock" and the start is asked for. A
centre below 1 kHz is ignored (an unset field).

### KiwiSDR `kiwi` chunk

kiwirecorder's `--kiwi-wav` layout, also written by the browser recorder
when GPS timestamps are on: a 10-byte `kiwi` chunk ahead of each `data`
chunk — UInt8 last GPS solution, UInt8 pad, UInt32 GPS seconds, UInt32 GPS
nanoseconds. The first stamp dates the recording. Both second encodings are
accepted: seconds since the GPS epoch (1980-01-06, converted to UTC with
the 18 leap seconds in force) and seconds within the GPS week, resolved
against the date in the file name. Without a usable stamp the file name's
time is used.

### Perseus

Microtelecom's own file notes were not available to this implementation.
What is supported is therefore conservative and documented as such:

- A `rcvr` chunk is read as four little-endian Int32 fields — centre
  frequency (Hz), sampling-rate index, start and stop time — of which
  **only the centre is used**, and only when it is between 1 kHz and
  7.5 GHz. The sample rate always comes from the `fmt` chunk.
- The file name's `<n>kHz` or `<n>Hz` token supplies the centre when the
  chunk is absent or implausible, and a `yyyyMMdd_HHmmss` stamp supplies
  the start, read as UTC. Anything the file does not say is asked in the
  sheet and remembered in the sidecar.

### Generic rules

- `RIFF`/`WAVE` little-endian only: `RIFX` (big-endian) and `RF64`/`BW64`
  (64-bit RIFF) are refused with that reason.
- `fmt `: WAVE_FORMAT_PCM at 8/16/24/32 bits or WAVE_FORMAT_IEEE_FLOAT at
  32 bits, directly or through WAVE_FORMAT_EXTENSIBLE (the SubFormat GUID's
  first word). Other tags and widths (µ-law, 12-bit, 64-bit float, …) are
  refused with the tag and width. Exactly two channels; a frame
  (`blockAlign`) must hold both samples and may carry padding.
- Scaling: 8-bit unsigned `(v − 128) / 128`, 16-bit `/ 32768`, 24-bit
  sign-extended `/ 2²³`, 32-bit `/ 2³¹`, float as-is with NaN/Inf zeroed at
  ingest (one bad pair would otherwise poison every averaging stage).
- Chunks are word-aligned: an odd payload carries one pad byte. Unknown
  chunks (`LIST`, `cue `, …) are skipped. A `data` size of 0, 0xFFFFFFFF or
  one that overruns the file (an interrupted writer, or a writer that
  cannot count past 4 GiB) is clamped to what is actually present.
- The chunk walk reads headers and the small metadata chunks only (at most
  4 KiB per chunk, 2²⁰ data chunks, 2²¹ chunks), never the sample body: a
  2 GiB file probes in a handful of reads with no measurable memory growth
  (`IQImportTests.testTwoGigabyteSparseFileProbesWithoutBeingRead`).

## Mapping onto the replay path

The receiver's chains run at 48 kHz × 2ⁿ (`HPSDRSampleRate`: 48, 96, 192,
384, 768, 1536 kHz). `IQImportPlan` picks the chain rate:

- a file within 0.2 % of a chain rate, or of a chain rate ÷ 2…8, plays as
  exactly that (KiwiSDR 12 000 / 12 001 Hz → 48 kHz ×4; 24 kHz → 48 kHz ×2);
- otherwise the smallest chain rate at or above the file rate (Perseus
  125 kHz → 192 kHz ×192/125; 250 kHz → 384 kHz; 1 MHz → 1536 kHz), or
  1536 kHz when the file is wider (SDR# 2.4 MHz → ×16/25; Elad 3.072 MHz
  → ÷2; 6.144 MHz → ÷4, the outer span is lost);
- ratios needing more than 1024 polyphase branches, and rates outside
  1 kHz–100 MHz, are refused with the reason.

The 0.2% nominal-rate tolerance applies to WAV only. SigMF's declared clock
is authoritative: its exact rational ratio is used, or refused when it needs
more than 1024 branches. A 48,001 Hz SigMF file is therefore refused rather
than silently played as 48,000 Hz. Fractional sample rates are not supported.

`IQImportStream` reads the body in 20 ms blocks (seeking per block, so
KiwiSDR's chunk list and any `data` chunk layout are handled alike),
unpacks to Float planes, resamples through `ComplexRationalResampler`
(64 taps per branch, Blackman window; the outer ~3 % of the span rolls
off) and hands out chain-rate frames. It is seekable by output frame — a
seek resets the resampler history, a ≤ 64-sample transient. On top of it:

- `IQImportPlayer` implements `IQReplayPlayer` (the protocol `IQFilePlayer`
  also implements): 50 ticks a second, one chain-rate block per tick, loops
  at end of file, seeks for the DVR scrubber. `RadioEngine.replay(imported:)`
  installs it exactly where a `.hiq` player goes and `RadioState` adopts
  the `.hiq`-shaped header (chain rate, centre, start; no transverter).
- `OfflineRecordingInfo.probe` recognises an I/Q WAV (marker, sidecar, or
  an unmarked stereo file) and `OfflineDecodeJob` feeds the chain from the
  stream; `sampleRate` / `frameCount` are the chain-rate figures and the
  recording clock advances with them.

A `.hiqmeta` sidecar next to a `.hiq` is never consulted; `.hiq` files are
read exactly as before.

## SigMF sibling pairs

SigMF separates interleaved samples (`name.sigmf-data`) from a small JSON
description (`name.sigmf-meta`). Keep the two files together with the same
base name when moving or sharing them. Either member can be selected in
**File ▸ Open IQ Recording…** or **Decode ▸ Decode a Recording…**. This is
local file interchange; HermitSDR does not fetch datasets or upload samples.

The first implementation reads the SigMF core 1.0–1.2 subset, writes 1.2.6,
and supports:

- One complex channel: little-endian Float32 I,Q (`cf32_le`) or signed
  Int16 I,Q (`ci16_le`, divided by 32768). The first scalar is I; Q follows.
  Float NaN/Inf values are zeroed by the existing import unpacker.
- One fixed whole-number sample rate, 1 kHz–100 MHz, within the exact
  resampling-ratio limit above. The declared rate is never guessed.
- Zero or one capture entry. A capture starts at `core:sample_start`, relative
  to the absolute index `core:offset` of the first sample stored in the dataset.
  Samples preceding that capture are skipped. Its `core:datetime` dates the
  retained first sample; no offset is added to that timestamp a second time.
  An empty captures array needs operator-supplied frequency and UTC.
- `core:frequency` in nonnegative RF Hz (up to 7.5 THz), and a UTC `Z`
  timestamp with optional fractional seconds, between 1980 and 2200. Missing
  values open the existing confirmation sheet; invalid supplied values fail
  with a reason. The file's declared frequency/time win over a sidecar.
  Values supplied by the capture are read only in that completion sheet.
  SigMF UTC fields accept `2027-01-15T08:00:14.1234567Z` as well as the
  ordinary `yyyy-MM-dd HH:mm:ss` input.

Fractional UTC is retained to Foundation `Date` precision (approximately a
microsecond across this date range); writing nine fractional digits does not
claim nanosecond clock precision.

Only a matching conventional data sibling is opened. Metadata is capped at
1 MiB and validated before the sample file is opened. Metadata and samples
must be regular files, not symlinks or named pipes. A dataset field may name
only that exact sibling: absolute paths, alternate filenames and URLs are
refused. Sample bytes must contain complete I/Q pairs; a replacement or
size change between probe and stream open requires reopening, and a short
read while streaming fails. Bounds checks cover offset/capture/annotation
indices and resampler arithmetic.

Multiple captures (including retunes), multiple channels, per-capture rates,
nonzero header/trailing bytes, metadata-only records, other datatypes and
unknown **required** extensions are refused explicitly. Optional extensions
and valid annotation entries are ignored; annotations are not mapped into
decoder bookmarks. Optional checksums are not verified. Collections, archives
and remote datasets are unsupported; leap-second timestamps are not represented.
Export one constant-frequency interval from a more complex dataset first.

Only confirmed missing values and the I/Q swap choice are remembered in
`name.sigmf-meta.hiqmeta`; fractional UTC is preserved. A complete pair opens
without writing a sidecar. A remembered SigMF sidecar must match its format
and sample rate. Correction files must also be bounded regular files; links
and named pipes are ignored without blocking. Read-only folders can still be
used for the current session.

### Export a portable interval

Choose **File ▸ Export IQ Recording as SigMF…** for an existing `.hiq`, or
use a Band DVR segment's export menu and choose **SigMF**. Start/end offsets
use the same inward whole-pair rounding as native `.hiq` export; blank end
means all complete samples currently on disk. The save panel previews
duration, sample count, combined pair size, RF center and first-sample UTC.

The new pair contains `cf32_le` IQ, one capture starting at zero, sample
rate, RF center, first-sample UTC and the software name HermitSDR. Callsign,
location, receiver identity, hardware details and annotations are omitted.
For a transverter recording the IF center is mapped to RF; an inverted
mapping conjugates Q so the imported spectrum has the same RF orientation.
The original `.hiq` header, mapping, samples and timestamps are preserved.

Choose a new basename: **neither sibling may already exist**, even if the
save panel offers replacement. Export uses a bounded buffer and an opened
snapshot of complete on-disk samples. Later appends are excluded; DVR pruning
of the original name does not invalidate an already-open snapshot. Buffered
recorder samples are excluded. DVR exports must be outside its rolling shelf.

Samples and metadata are written and synchronized in temporary files in the
destination folder. Exclusive hard links publish data first and metadata
last; the metadata name is the completion marker. On a write error or task
cancellation, the worker removes its temporary files and any data sibling
it published. Existing files are never overwritten. The destination filesystem
must support hard links. An abrupt process or power loss can leave temporary
files or an orphan data sibling; it cannot promise a two-file filesystem
transaction. A finished pair is readable only after metadata publication.

This is original native Swift code written from the
[SigMF specification/schema v1.2.6](https://github.com/sigmf/SigMF/tree/v1.2.6).
No libsigmf, SDRangel code, schema assets or third-party dependencies are
bundled. The `.hiq` recorder remains the canonical live recording format.

## Limits

- Files larger than 4 GiB: RIFF sizes are 32-bit, so writers either stop
  at 4 GiB or write a wrong size. HermitSDR follows the `data` chunk to the
  end of the file whatever the size field says, so a single-`data`-chunk
  file of any length plays; RF64 is not read.
- Real-time replay of a 6 MHz-wide float file reads ~49 MB/s from disk;
  Decode a Recording at "Max" is bounded by the resampler and chain, not
  the file.
- Perseus support is name-and-chunk best effort as described above.
- LinRad raw files (no header) are not read; export them as WAV first.
- The whole-file waterfall overview with drag-select is not part of this
  change; the open sheet shows the textual overview (format, encoding,
  rate, duration, centre, start, chain rate) and the Band DVR timeline
  scrubs the replay.

## Measured

See the `IQ-IMPORT` lines `IQImportTests` prints: a synthetic FT8 slot
(`CQ W1AW FN31`, 0.3 full scale, white noise) embedded in every format —
`auxi` 24-bit at 96 kHz, SDR# 16-bit at 250 kHz (→ 384 kHz), SDR++ float at
48 kHz, Perseus 16-bit at 125 kHz (→ 192 kHz), KiwiSDR 16-bit at 12 kHz in
47 packet-sized `data` chunks (→ 48 kHz), and a generic 16-bit file with a
sidecar — decodes through `OfflineDecodeJob` with the slot time taken from
the file's clock. In the Debug (`-Onone`) test build on the Mac mini M4 Pro
(2026-10-22, other builds running alongside): 16.5 s of recording decoded
in 0.6–0.9 s at 48 kHz, 1.3–2.3 s for 24-bit at 96 kHz, 0.7–1.4 s for the
KiwiSDR 12 → 48 kHz case, 2.6–4.8 s for Perseus 125 → 192 kHz and 5.0–8.7 s
for SDR# 250 → 384 kHz; the decoder reported 15.5–16 dB S/N for the 0.3
full-scale tone over the −54 dBFS noise. The 2 GiB sparse probe took under
a millisecond with no resident-memory growth.
