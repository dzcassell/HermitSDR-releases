# Console and runtime tools

## UTC waterfall time lines

View → Waterfall → UTC time markers (2D) offers Off (default), 15 or 30 seconds,
and 1, 5, 10 or 15 minutes. Lines and HH:mm:ssZ labels attach to stored FFT rows,
follow fractional scrolling and history compression, and remain in PNG, Postcard
and stream captures of that Metal scene. They are omitted in 3D. Labels are
thinned for spacing, with a hard 24-line budget per frame.

Live rows use acquisition time minus time-machine age. File replay uses the
recording header start plus its playhead (block resolution). No boundary is
invented across missing rows, a reverse seek/loop or a gap greater than five
seconds. This is a recording-clock display, not a calibrated sample-clock or
station-clock measurement. A frozen source keeps its labels with its rows.

## Named console layouts

View → Console Layout Presets saves the current receiver/transmitter/workspace
visibility, panel dimensions and selected workspace/decoder/transmitter tabs.
Enter a unique name (1–60 characters), then Save current as new. Up to 30
arrangements are retained. Select a row to Recall, Replace with current or Delete;
replacement and deletion have native confirmation alerts. Recall enables Console
Layout and adapts dimensions to the current window through existing size limits.

Presets do not change receiver tuning, decoder enable states, services, palettes
or TX state. The versioned local library is part of the normal settings backup.
An invalid or newer-format library is preserved and saving is refused; restore a
valid settings backup to recover it.

## Performance history

Station → Performance retains the resource budget controls and adds charts for
app CPU (% of one core, potentially greater than 100), resident memory in MiB,
and main-actor tick delay in milliseconds. Sampling begins at app launch, roughly
once per second, with a fixed 3,600-entry in-memory ring. Select 1/5/15/60-minute
ranges or Clear. Restarting also clears history. Nothing is uploaded or written
to disk.

CPU derives from cumulative user+system process time over monotonic elapsed time.
The first sample or a reset/unavailable counter has no CPU value. UI tick delay
measures lateness of a scheduled main-actor wakeup against process uptime; it
is not audio callback latency. Charts leave discontinuities
unconnected rather than synthesizing samples. These diagnostics do not validate
RF behavior or replace sequence-error/audio-health counters.

The behavior was inspired by AetherSDR's documented UTC markers, workspace presets
and runtime monitor; the implementation is original Swift/Metal using Apple Charts.
