# HermitSDR lab commands

Use the executable inside the installed app bundle. For a default release
installation it is `/Applications/HermitSDR.app/Contents/MacOS/HermitSDR`.
Use the corresponding executable path for a Debug build.

## Compare SSB audio

Pass the original voice take, a JSON recipe, and a new output directory whose
parent already exists.

```sh
"$hermit_executable" --hermit-ssb-experiment voice.wav tx.json tx-results
```

```json
{
  "schemaVersion": 1,
  "trials": [
    { "profile": "Studio SSB 2.8k", "graphicEQDb": [0, 0, 4, 0, 0, 0, 0, 0] },
    { "profile": "Studio SSB 2.8k", "graphicEQDb": [0, 0, 1, 0, 0, 0, 0, 0] }
  ]
}
```

Use two to four built-in SSB profiles or repeated instances of the same
profile. Optional graphic EQ values are absolute dB gains from −12 to +12 at
63, 125, 250, 500, 1000, 2000, 4000 and 8000 Hz. Instead of graphic EQ, a
trial can provide `parametricEQ` with `inputTrimDb`, `outputTrimDb` and an
array of up to ten `bands`. Each band specifies `enabled`, `type` (one of
`peaking`, `lowShelf`, `highShelf`), `frequencyHz`, `q` and `gainDb`.
Either recipe can also supply `compressor` with `thresholdDb`, `ratio`,
`attackMs`, `releaseMs` and `makeupDb`.

The runner uses up to 30 seconds of the take and normalizes its input peak
once. It uses the base profile plus the supplied EQ and single-band
compressor settings. Live mic gain, multiband compression, custom effects
and other live settings are outside the recipe. In the app, load a take in
**SSB Profile Lab** and choose **Audition Recipe…** to listen at a common
level without creating WAV files.

Open `comparison.json` for passbands, band balance and compressor and limiter
reduction. The numbered WAVs share a playback RMS target when the clips
contain measurable audio. Reported processing metrics describe the renders
before playback normalization. Use the WAVs for listening and the report for
objective comparisons. The recipe is a reproducible draft experiment.

## Preview receive watches on a replay

Use a .hiq capture, a Band DVR segment export or a saved IQ excerpt from
an existing decoder bookmark.

```sh
"$hermit_executable" --hermit-replay-scan capture.hiq watches.json > scan.json
```

```json
{
  "schemaVersion": 1,
  "startSeconds": 0,
  "durationSeconds": 30,
  "watches": [
    {
      "centerHz": 7195000,
      "bandwidthHz": 3000,
      "minimumPeakDbFS": -65,
      "minimumProminenceDb": 10
    }
  ]
}
```

Use one to sixteen watches inside the capture span and a window of up to 60
seconds. Watch centers are RF frequencies, including the recording's
transverter mapping when present. Minimum bandwidth is four FFT bins.
A matching peak must meet the absolute dBFS floor and the requested dB
prominence over the median bin inside that watch.

Pass a third argument naming a new clip directory to export up to eight of
the strongest events as replayable IQ clips. Each clip lasts up to one second
and the total IQ body is capped at 64 MiB. Events that received a clip include
its file name.

The report groups consecutive matching frames. Frame-center timestamps are
relative to the recording start. The strongest frame supplies the peak and
its contiguous width at −6 dB inside the watch. Bin width and frame interval
are reported. Brief activity may fall between sampled frames. The scan
estimates spectral evidence. Mode identification needs additional evidence
such as an actual decode.

## Diagnose a waterfall case

In HermitSDR, choose **Station → Performance → Start Recording**. When you
see the glitch, choose **Mark Glitch**, then **Analyze Mark** or **Export Case**.
**Open Case** reviews an exported case. The CLI can also read that JSON with
`--hermit-waterfall-report`. The case carries
up to 90 recent samples plus the mark time. Each sample records system uptime,
drawable acquisition cadence, spectrum-row cadence, cumulative link and audio
counters, sample rate, receive mode and source type. Counters may straddle a
sample boundary. A hidden or occluded panadapter can stop acquiring drawables,
so ask whether it was visible during the incident. Audio underruns count
missing output frames. A drawable measurement tracks acquisition, so use an
Instruments trace if you need to isolate GPU presentation latency.

## Compare replay decoder trials

Choose **Decode → Decode a Recording → Compare Decoders** or use the
same worker from the app executable.

```sh
"$hermit_executable" --hermit-replay-decode capture.hiq trials.json > evidence.json
```

```json
{
  "schemaVersion": 1,
  "trials": [
    { "mode": "FT8", "dialRFHz": 7074000, "sideband": "USB" },
    { "mode": "FT4", "dialRFHz": 7074000, "sideband": "USB" }
  ]
}
```

Choose one to four trials and a window up to 120 seconds. For a longer
recording, include `startSeconds` and `durationSeconds` in the recipe. The
report preserves the recording start and the actual decoded interval. Use an RF
dial within the recorded IQ span. Leave dial and sideband out for WAV audio.
Use the normal 700 Hz CW pitch and omit sideband for CW. Modes include
`PSK31`, `PSK63`, `PSK125`, the corresponding `QPSK` variants
(`-L` for lower sense), `PACKET 300` and `PACKET 1200`. The ALE skimmer
uses the full IQ span. Digital mode trials accept optional `audioCenterHz`.
Results contain bounded transcripts, spots and session status. A trial
that completes with no decode establishes only what was observed in that
recording with those settings.

## Compare transmit latency evidence

```sh
"$hermit_executable" --hermit-compare-latency baseline-run.json candidate-run.json
"$hermit_executable" --hermit-compare-latency-maps baseline-map.json candidate-map.json
"$hermit_executable" --hermit-measure-captured-latency reference-and-return.wav capture-recipe.json
```

The app has the same operations under **TX Latency → Analyze**. Keep
software-map observations, loopback runs and recorded physical endpoints
separate. Use an explicitly known calibration for stereo captures. Compare
deltas only when the source, probe and evidence type make them meaningful.
