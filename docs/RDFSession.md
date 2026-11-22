# RDF session recorder — development

**Radio → RDF Session…** records where and how the tuned channel was measured.
It is a local field notebook, measurement map and replay viewer. It does not
identify a transmitter, separate co-channel signals, estimate a source location,
move the receiver or propose a route. Channel activity is not signal identity.

Available from 2026.1120_001. GPS field operation and RF calibration remain
operator acceptance checks; the map displays sampled antenna positions.

Public operator guide: [How To RDF With HermitSDR](https://hermitsdr.com/support.html?article=how-to-rdf-with-hermitsdr).

## Start a session

1. Set the radio, antenna, filter and gain yourself. **Tune target** explicitly
   applies the selected receive frequency/mode through the existing RX controls;
   capture alone never tunes, connects, arms or keys a radio. Its receiver readout
   shows the current reported level and whether a fresh live meter is present.
2. Enter a name, target frequency in Hz and antenna/field notes. The target
   field initially follows the tuned frequency until filled. **Use current
   signal** selects the tuned channel for later snapshots without retuning it;
   each observation keeps a stable signal reference and its actual context.
3. Choose **Manual position**, **iPhone GPS**, or **TH-D75 GPS (USB)**, then **New session…** and
   choose a new `.hrdf` file. Existing files are refused rather than overwritten.
   Opening the window alone starts no recording or location sharing.
4. **Manual:** enter signed decimal latitude/longitude (north/east positive)
   and an uncertainty radius in meters. **Place pin** lets a map click fill the
   coordinates. **Sample here** confirms the antenna is at that position and
   saves exactly one observation. A manual pin is never sampled automatically
   while driving. Invalid coordinates cannot be captured. The initial setup
   and each changed setup need one second to settle.
5. **iPhone:** pair using **Radio → iPhone Location…** first. **Sample here
   button** is the default capture mode, including GPS sources: position updates
   do not create measurements. Press Sample here when the chosen signal/speaker
   is audible. Optional **Continuous 1 Hz GPS** records once per second. It saves explicit quality flags during
   missing/stale GPS or receiver readings, instead of reusing an old position
   or inventing zero power. The phone can be in the car, but an antenna offset
   and GPS uncertainty still limit where a measurement was made.
6. Add a note for the next observation as needed. **Stop** closes the session;
   closing the window leaves an explicitly started session running. Stop ends
   RDF recording only; stop location sharing in the phone app separately when
   finished. Quitting the app stops capture; a pending final write may need prefix recovery.

Positions and receiver data are written locally only after New session. The
session file contains sensitive location history. No upload or telemetry of
its contents is added. The optional **Apple Maps (online)** checkbox loads
Apple's map tiles for the viewed area; it starts off. The offline measurement
map works without network services or location permission on the Mac.

## What an observation means

Power is the receiver's existing **pre-AGC S-meter value**, including its current
calibration, applied RF gain and digital attenuation. It is channel power, not
the isolated power of a selected transmitter. It can include noise and every
signal sharing the filter. A strong point is not a transmitter location.

The noise floor reuses Signal History's panadapter percentile estimate, scaled
to the actual receive-filter width. It needs several rows to acquire and can
be biased by a crowded span or peak display averaging. Missing floor/SNR stays
unknown, not zero. SNR is reported channel power minus that estimate.

The timestamp is the Mac's **host observation time**, with monotonic elapsed
session time and meter age. The underlying meter integrates about 100 ms and
publishes about ten times a second; this is not sample-clock synchronized IQ
capture. A measurement uses the latest available iPhone fix with its original
capture timestamp and both wall/monotonic age. There is no interpolation or
claim of phase/timing precision suitable for TDOA.

Each observation retains:

- UTC observation time, monotonic elapsed time, sequence number and note;
- position source, coordinates, reported/entered uncertainty, fix capture time
  and age, plus altitude, speed and course when the phone supplies them;
- physical radio identity and calibration-profile provenance, reported dBm and
  raw dBFS, meter age, estimated floor and SNR;
- RF frequency including RIT/transverter mapping, mode, filter width/shift,
  sample rate, receive antenna, applied RF gain, attenuation, meter conversion
  offset and front-end/blanker/manual-notch context;
- setup group, exclusion flags, coarse channel-activity state and burst number.

The antenna field records the selected radio input; put physical antenna
placement/orientation details in field notes. Calibration provenance describes
the receiver profile, not proof that its S-meter was calibrated for this hunt.
Values should be checked against a known source before relying on absolute
power. The recorder does not calibrate the radio. Keep RF-anchored notches and other
unrecorded DSP/hardware settings fixed, or describe those changes in notes;
this first recorder does not capture every receive-chain control.

### Excluded evidence

Transmit/tail, ADC overload, setup settling, receiver replay/time shift, missing
or stale meter (>0.5 s), off-target frequency (>0.5 Hz), missing/stale phone
position (older than the saved policy: 3 s for new sessions, 10 s for legacy journals), uncertainty >50 m and a backwards wall-clock step are flagged.
SDRplay hardware AGC is excluded because it can change front-end gain; use
manual hardware gain for this first version. Reported power can remain in an
excluded row for diagnosis, but it cannot produce a colored usable map symbol.

Every changed receiver context starts a new setup and a one-second settling
period. Reconnect starts a fresh setup as well. The view follows the latest
setup independently for each receiver by default; explicitly choose **All setups** to inspect the combined
history. Filter widths, antennas or calibration changes can make groups
incomparable even when both report dBm.

"Active" uses a coarse 6 dB open / 3 dB close SNR threshold on qualified rows.
A gap/quality failure or a sampling pause over 2.5 seconds breaks the burst.
Unknown floor means unknown activity. One-second sampling can miss short bursts;
a burst number is only an energy grouping, never a transmitter fingerprint.

## Map, playback and export

The offline map fits the observations in a local geographic plot with a north
arrow and coordinate range. It contains no road/building data. Apple Maps adds
street context and normal pan/zoom, plus **Fit**. Turn off **Place pin** to
inspect measurements; the list also supplies accessible selection controls.
A purple draft pin has not been captured. Uncertainty is shown numerically;
the selected point also gets an uncertainty circle in Apple Maps.

With Strength overlay disabled, usable points use a fixed blue (−120 dBm) →
green (−75) → red (−30) scale;
excluded points are gray with ×. Missing/stale positions are not plotted. Route
lines break at gaps, long sampling pauses, source/setup changes and the dateline.
They join observation positions only, not a navigation route. The optional sample-centered strength overlay adds colored halos at measured
positions; it does not interpolate coverage or source probability.

The map draws at most 500 measurement symbols plus 500 overlay samples,
preserving endpoints, selection and each
bucket's strongest usable reading; the journal keeps every observation. The
list shows the newest 100 rows in the current replay/setup view. A selected
observation shows its original setup, power, quality, position and note.

**Open…** reads a stopped or recoverable session without starting a receiver or
GPS link. The slider and **Play history** reveal a prefix of its measurements
(five observations per second, not real-time audio or IQ). Playback changes the
map only; it cannot tune a radio. Setup filtering still applies during playback.

**Export CSV…** writes all recorded observations and flags, not merely the
sampled map symbols or current replay prefix. Unknown numeric fields are blank;
text is quoted and formula-like text is protected for spreadsheet use. The
journal itself and aliases of it cannot be selected as the CSV destination.

## Storage and threading

The `.hrdf` file is a version-1 newline-delimited JSON journal: one header,
ordered observations, then an end marker. One append is fsynced per observation.
If the final line was interrupted, Open recovers the complete prefix and says
so. A malformed complete record, unsupported header, repeated/out-of-order
sequence, invalid coordinate or trailing data after an end marker is rejected.
A missing end marker is reported as unfinished recovery. A failed Open keeps
whatever session was already displayed. This is not automatic append/resume.

Bounds: 36,000 observations, 64 MiB on disk, 16 KiB per record and bounded text
fields. The model permits one append in flight; if automatic capture overtakes
storage, it stops instead of building an unbounded write queue. Successful rows
are added to the map only after the append completes. A disk error stops
recording and preserves whatever complete prefix was saved. Load and export
run on a utility task; append/fsync runs on a dedicated actor. No radio/audio
real-time callback does file IO or map work. Session files are created with
owner read/write permissions and existing symlinks/files are not overwritten.
Imports read one regular descriptor with a size bound and refuse symlinks.

## Acceptance

Generated sessions can check flags, persistence, recovery and rendering. Field
acceptance still needs a passenger-operated laptop and a real supported radio:
verify meter calibration/gain handling, GPS position/age during a drive, manual
position changes and session recovery. Keep the phone and antenna positions in
mind. This feature does not require or authorize an RF transmission. Target
fingerprinting, multi-emitter separation, localization and guidance are later
features to build on these saved observations.

## Software verification on 2026-11-19

- Full package regression: 4,883 tests, 26 skipped, no failures. Final focused
  regression: 136 tests passed, including 15 RDF cases and the last replay-pin
  isolation change. Final presentation/privacy-copy changes were checked in the
  subsequent builds and renders.
- Signed Mac Debug and Release builds passed, with strict deep signature checks.
  The iPhone companion also compiled for simulator Debug and unsigned device
  Release; no installation or physical-device test is implied.
- The actual offline map, manual fields and saved evidence were rendered and
  visually inspected at 800×680 and 1120×820 in Dark and Light. The generated
  fixture contains 36 observations, an overload and a missing-position gap.
  The minimum-height layout scrolls instead of clipping the main controls.
- The source-reviewed meter taps use FM IF envelopes and the uncancelled AM
  channel. This is software evidence; physical power calibration remains
  unverified for the new recorder. Street-map interaction and road testing
  remain operator acceptance work.

## TH-D75 USB GPS

The TH-D75 development receiver adds **TH-D75 GPS (USB)** to Position.
It enables RMC/GGA output only for an explicitly started RDF recording and
restores the previous output on Stop/disconnect. Menu 981 must select USB.
NMEA has no measured horizontal accuracy, so those points retain an unknown
accuracy flag and omit the accuracy cell in CSV. The map does not draw a
pretend uncertainty circle. Raw IF levels/configuration are retained with
unknown receiver gain flagged; antenna-power calibration and road trials
remain outstanding. See [TH-D75 setup](KenwoodD75.md).


## Tagged signal surveys and receiver layers (2026-11-20 development)

Select **Use current signal**, enter or reuse a **speaker tag**, and press
**Sample here**. The target is a selected channel, not a fingerprint or a
promise that only that speaker is present. Tags have stable UUIDs and a label
snapshot on each observation. Manual attribution has no confidence score.
Tags can be reused across different signals and batches; the application keeps
a bounded local tag library. Optional per-observation voice-analysis method,
model/version and confidence fields provide future integration plumbing. No
voice classifier, speaker embedding, recording or identity inference is added.

One press creates a host-timestamped capture batch. Each participating receiver
gets a separate observation with its own receiver ID/label, context, meter
age, antenna position/source/age, flags and setup. A batch is a sequence of
durable records, not a synchronized RF measurement: receivers may integrate
power at different times, and no TDOA/phase-coherence claim is made. A partially
written batch remains an explicitly recoverable prefix.

The current console supplies its active receiver. `RDFSessionModel.registerReceiver`
accepts up to seven additional already-published receiver snapshot providers
(eight including the primary). A provider must return its registered ID and
its own antenna position; no secondary receiver inherits the primary GPS.
Missing/stale fixes and stale meters remain flagged gaps. The independent **Radio → Uniden SDS100** instrument now supplies one such
live additional receiver feed alongside the primary SDR. Its window can use
its own antenna coordinates or an explicit co-location choice; shared-position
provenance is saved. Other physical receiver engines and bridges from additional
HermitSDR instances still need adapters. This is not a general multi-radio IQ
connection manager or network listener. Two synthetic receiver providers
exercise simultaneous batch capture and save/reopen tests.

Map filters select receiver layers, speaker tags, signals and comparable
setups. Each receiver has a separate, named overlay; **All receiver layers**
shows up to eight. Colors are scaled independently within each receiver's
selected measurements and shown with the actual range in the legend. A layer
refuses mixed speaker tags, targets, units or receiver contexts rather than
silently averaging them. Select a signal/tag/setup when the legend requests it.
Halos are screen-size symbols, not measured coverage areas or GPS uncertainty.
Route lines are grouped per receiver and never join different antennas.

**Reported dBm** uses qualified rows only. **IF dBFS (exploratory)** can display
raw TH-D75 levels with unknown-gain/unknown-position-accuracy flags, but excludes
stale, off-frequency, settling, overload, replay and transmit rows. This is
not calibrated field strength. Each receiver's color scale can differ; use the
numeric evidence/units and calibration provenance rather than comparing hues
between receivers. The D75's measured accuracy stays unknown.

The offline map remains available without services. **Apple Maps (online)**
adds street tiles when explicitly enabled; native MapKit avoids introducing a
Google Maps key/billing dependency. The data model is provider-neutral.
**Export → GeoJSON** writes a FeatureCollection of recorded antenna positions,
with receiver/signal/tag IDs, attribution, batch ID, dBm/dBFS, quality flags and
provenance. Rows without valid positions remain counted in metadata but have
no fabricated geometry. GeoJSON and CSV can be styled/imported by another map
provider or GIS; no Google Maps account/API integration is implemented. Export
protects the authoritative journal and its filesystem aliases.

Version-1 journal compatibility is retained through optional fields. Legacy
records have no invented speaker/signal identity. New multi-receiver headers
explicitly permit different position sources; legacy headers keep their
single-source validation. CSV adds the survey/receiver columns to the right
of the existing columns. The session journal remains the complete evidence.


## Scanner RSSI and mixed-unit overlays

The SDS100 provider adds separately qualified `scannerRSSI` values and receiver
metadata (channel/system/digital/talkgroup/unit-ID fields). Its observed−999
unavailable-RSSI sentinel remains metadata, not plotted power. Filter width,
RF gain and IQ sample rate are explicitly unknown and export blank. The
**Per receiver** map option chooses appropriate units separately for each
layer, allowing D75 IF dBFS and scanner RSSI together without conversion.
Co-located antennas share position only after an explicit operator choice,
recorded as `positionSharedWithReceiverID`; otherwise each feed needs its own
position. CSV/GeoJSON retain all unit/provenance metadata. See
[Uniden SDS100](UnidenSDS100.md). No classifier or emitter localization is added.


## Field controls (next preview after 2026.1120_001)

**Field view** pins target/mode, GPS readiness, reusable speaker tag, physical
antenna/setup label and **Sample here** above the scrolling map/history.
Command-Return saves one on-demand batch. **Target → TH-D75 · 27.385 MHz LSB
setup** fills the configuration without tuning or enabling GPS. Connect the
D75 as the primary receiver, explicitly choose **Tune target**, then start a
new journal with **TH-D75 GPS (USB)** selected. Menu 981 must be USB. The D75
IF screen can show AM while HermitSDR demodulates LSB.

New sessions accept GPS positions up to three seconds old. Setup offers a
10-second policy for slower sources; the chosen policy is saved in the header
and each observation. Missing, clock-mismatched and stale fixes remain flagged
gaps without coordinates. Satellite count and HDOP describe the receiver's
recent report, not measured accuracy. Estimated/manual/simulated NMEA fixes
are refused. Acquisition satellites alone cannot create a location.

**Follow GPS** centers the map on the latest accepted primary-antenna position.
A stale fix removes that live marker. Offline view supplies a local north-up
coordinate plot; Apple Maps adds optional street tiles. Neither fabricates
measurement points between captures.

For D75 surveys, **IF contrast (estimated dB)** compares mean channel-bin
power to the median background inside the same fresh usable IF window (a
mean against a median, so a channel holding only noise reads about +1 to
+1.6 dB, not 0, and the figure is signal-plus-noise over noise), omitting
the filter skirts and a guard around the channel. It avoids treating the
48 kHz stream's rejected spectrum as a noise floor. A uniform digital level
change cancels mathematically; RF AGC behavior and changing interference can
still affect it. It is neither calibrated RF dBm nor physical SNR, and no D75
S-meter strength command has been verified. Unknown gain/position uncertainty
remain saved. Missing/stale/insufficient FFT data produces no contrast.

Use **Lock scales** to retain a separate numeric color range for each receiver
and unit; unlock to rescale. Antenna/setup labels and spectrum-averaging changes
split comparison groups. **Strongest sample** selects the strongest eligible
recorded antenna position in a single comparable layer, not an inferred
transmitter coordinate. CSV/GeoJSON preserve contrast, FFT age/bin counts,
GPS-age policy and quality flags. Existing journals remain readable.

For tonight's rubber-duck test, first establish that the interfering signal is
actually audible at 27.385 MHz LSB. Keep the antenna placement, radio settings
and display averaging fixed. Prefer **Fast** for moving snapshots; **Peak**
retains spectral history and can misrepresent the level at the current position.
Sample the same recognizable transmission and
reuse its manual tag. Field GPS acquisition, relative-level behavior and road
operation remain operator checks. The software does not establish whether a
particular transmission is jamming or identify its speaker.


## Stationary SSB stop measurements — development

For local ground-wave broadcasts, use an on-demand session, select LSB or USB,
confirm the physical antenna/setup label and position, then enable **Field view**.
Select **Fast** spectrum averaging on the D75: peak/slow display history can hold
speech through pauses. Choose 10, 15 or 20 seconds and press **Measure SSB stop**.
The receiver is not tuned or reconnected by this action. Keep the antenna still.

**Target speaking** is your listening confirmation. Leave it checked while you
hear the broadcaster and uncheck during silence or when unsure. A second energy
gate opens at 6 dB and closes below 3 dB against available channel/background
contrast. This is a speech-activity proxy, not speech recognition or transmitter
identification. There is no competing-signal classifier. D75 gating uses the
fresh in-band IF contrast; other supported primary IQ receivers use their
pre-AGC channel/noise estimate. Unknown background is unqualified, not zero.

The recorder attempts one snapshot every 200 ms (5 Hz). Each raw row includes
its stop UUID, monotonic offset and operator Target speaking state, original location/fix age, configuration,
quality flags, power and available background/contrast. One fsynced write is
allowed in flight; slow disk/UI sampling appears as reduced coverage or gaps,
never invented samples. This is host-timed sampling of published meters, not
continuous sample-clock integration, IQ recording or precision RF metrology.

A completed stop needs at least 80% qualified coverage and two seconds of active
speech. Its active median, linear-power mean, P90 and P90–P10 spread exclude
pauses. The median is used for strength overlays; contrast overlays use median
active IF contrast. The background statistic retains the original estimator's
units (D75 background is per-bin IF dB, not an RF noise-floor measurement).
D75 levels remain exploratory IF dBFS because hardware gain is unqualified.
Changing modulation, frequency, bandwidth, gain context or antenna/setup during
a stop invalidates comparison. Sampling gaps over 0.6 seconds, reported speed
over 1.5 m/s or position displacement over 20 meters also prevent a ready result.
GPS jitter can therefore reject a stationary stop. Unknown D75 horizontal
accuracy remains unknown; these checks do not certify positioning or fixed gain.

Only the primary receiver participates in an SSB stop. The SDS100 AM RSSI
remains available through ordinary **Sample here**, in its own units/layer; it
is not substituted for sideband speech power. Calibrated reported dBm, relative
IF dBFS and scanner RSSI are never numerically merged. Raw stop rows remain in
the record list/export but do not crowd the map; only the qualified summary
enters strength overlays. An insufficient, invalid or cancelled summary is
excluded. Cancel preserves already-saved raw samples. Stopping the session first
cancels/finishes the active stop and then writes the session end marker.

**Save audio excerpt** is optional and off by default. It saves processed mono
12 kHz receiver audio beside the journal as `SSB-stop-<UUID>.wav`, owner-only
permissions, without replacing an existing file. It needs live primary receive,
SUB off and TX disarmed at start. The audio follows receive processing/routing;
it is listening evidence, not the source of RF-level measurements. Fixed-size
storage bounds capture; an empty, invalid, dropped or failed excerpt is reported
unavailable without inventing a file reference or invalidating saved power data.
The summary retains the filename; CSV/GeoJSON keep the summary and its provenance.
Keep the WAV beside its journal when copying the evidence. Nothing is uploaded.

Repeat stops with an unchanged antenna/receiver setup to assess repeatability.
This feature makes no source-location, transmitter-power or ground-wave coverage
claim. Live road/GPS/SSB and receiver-gain acceptance remain operator work.
