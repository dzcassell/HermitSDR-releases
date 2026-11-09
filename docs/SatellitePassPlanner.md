# Satellite Pass Planner

Open **Radio → Satellite Pass Planner** and choose **Import TLE…** to predict
passes directly from a local two-line element file, or **Import Pass Plan…**
to open a plan computed elsewhere. The window shows geometric visibility
from the modeled coordinates, UTC start and end, orbital element source and
epoch, and a true-azimuth sky plot. The plot's outer ring is the horizon and
its center is the zenith. Use the three labeled rows for the first, highest
sampled, and last look angles. A pass already in progress at an analysis
boundary is marked.

Use the star to favorite a satellite by its catalog number. The app
keeps one pass plan in the station profile and preserves favorites when
you replace the plan. Compare the modeled observer coordinates with your
configured grid center. If the element epoch is more than 14 days from a
pass, the detail warns that the prediction uses distant elements.

## Importing a TLE file

**Import TLE…** opens a local two- or three-line element file (an optional
name line, then the two numbered 69-column lines; the `0 ` name prefix is
accepted). The sheet starts the observer at the center of the configured
station grid, or asks for WGS84 latitude, longitude and elevation when no
grid is set, and takes the planning window (1–72 hours from now, default 24)
and the minimum elevation that defines the pass edges (0–80°, default 10°).
The element provenance line records the file name and the import date.

The predictor is HermitSDR's own near-Earth SGP4 implementation, written
from Vallado, Crawford, Hujsak and Kelso, *Revisiting Spacetrack Report #3*
(AIAA 2006-6753) with WGS72 constants, and checked against the nine
near-Earth cases of that paper's published verification set to within a
centimetre. TEME states rotate through IAU 1982 Greenwich mean sidereal time
(UT1 taken as UTC) into the Earth-fixed frame; look angles, range and
range rate are topocentric for the WGS84 observer. Passes are found by
sampling the elevation every 10 seconds, refining each threshold crossing
by bisection and each peak by golden-section search, then recording 33
evenly spaced looks plus the peak with the modeled line-of-sight range rate.

The predictor verifies each line's checksum and supports up to 16
satellites with periods of 70–150 minutes and eccentricity up to 0.2;
deep-space objects (periods of 225 minutes or more) are refused with a
reason, as are plans beyond 72 hours, 256 passes or 1 MiB. The app never
fetches orbital elements: obtain the TLE file yourself and keep it fresh.

## Using the Skyfield converter instead

The optional `tools/tle-to-satellite-passes.py` converter produces the same
plan JSON from a two-line element file using a separate Python environment
containing [Skyfield](https://rhodesmill.org/skyfield/installation.html).
Use it to cross-check the native predictor or to attach a transponder
catalog. The app does not install Python, fetch orbital elements, or bundle
the MIT-licensed library or its dependencies.
[Skyfield license](https://github.com/skyfielders/python-skyfield/blob/master/LICENSE)

    python3 tools/tle-to-satellite-passes.py satellites.tle \
      --source "Local element provider and retrieval date" \
      --latitude 42.5 --longitude -71.0 --elevation-m 40 \
      --start 2026-11-06T00:00:00Z --hours 24 --minimum-elevation 10 > passes.json

Use `--grid FN42` in place of latitude and longitude to model the center
of a four- or six-character Maidenhead grid.

The converter uses SGP4 and WGS84 observer coordinates. It checks element
checksums and supports up to 16 low-Earth satellites with periods of
70–150 minutes and eccentricity up to 0.2. The output is bounded to 72 hours
and 256 passes. Large plans use compact JSON when needed to fit the
1 MiB import limit. Open regular local files for plans, TLEs and catalogs.
The chosen elevation threshold defines the pass edges.
[Sgp4 satellite and pass documentation](https://rhodesmill.org/skyfield/earth-satellites.html)

Use the app executable's `--hermit-check-satellite-passes passes.json` mode
to validate a plan before opening it. The planner is passive apart from the
receive-only **Track** button described below. It does not assign a
transponder or move an antenna, and it never transmits.

Expand **Downlink Doppler preview** and enter the satellite's nominal
downlink in MHz. The first, peak-elevation and last looks show a signed
shift and estimated receive frequency. Approaching range gives a positive
shift. Native and converter plans include the modeled line-of-sight range
rate at each look. Older plans estimate it from adjacent range samples. The
Doppler row’s tooltip identifies the source. Distant orbital epochs can
reduce accuracy. Use the preview for manual receive planning.
[How Doppler tracking uses range rate](https://www.jpl.nasa.gov/edu/resources/lesson-plan/exploring-the-doppler-effect-with-nasa/)

## Live Doppler tracking

Live Doppler tracking is **receive only**. It moves VFO A and nothing else:
it never keys the transmitter, never sets a transmit frequency, split or
transverter transmit offset, and it refuses to start while the transmitter
is armed. The tracking state lives in the running session and is never
saved; every launch starts with tracking off.

Select a pass, check the **Nominal downlink (MHz)** field in the *Live
Doppler tracking* section (it is seeded from the local transponder catalog
when the plan has one; otherwise enter the satellite's published downlink)
and press **Track**. The button is enabled only while a radio is connected,
the transmitter is disarmed, the pass is in progress or starts within two
minutes, the orbital elements are less than 14 days old and the corrected
downlink falls inside what the connected radio — or the active transverter
profile — can receive. When it is disabled, its tooltip and the line under
it say why.

While tracking, the receiver follows the predicted downlink once a second:
`receive = nominal × (1 − ṙ/c) + nudge`, where ṙ is the modeled
line-of-sight range rate, so an approaching satellite reads above its
nominal frequency and a receding one below. Plans predicted natively keep
the imported elements beside the cached plan and propagate them at each
tick with the same SGP4 model as the predictor; a plan imported as JSON (or
one whose cached elements no longer match the satellite's epoch) falls back
to interpolating the stored looks, and the status says which. Retunes are
sent only when the target has moved more than 20 Hz since the last command,
so the dial does not chatter at the 10 Hz rounding. With a transverter
profile active, the dial is set to the IF that corresponds to the RF
downlink, with the profile's inversion honoured; a downlink outside the
profile or the radio's range is refused with a reason before anything
moves. Starting up to two minutes before AOS parks VFO A on the predicted
rise frequency and the status shows **Waiting for AOS**.

The status rows show the current shift in hertz, the corrected receive
frequency (and the IF dial when a transverter is active), elevation, time to
LOS and the nudge. Use **−100 Hz**, **+100 Hz** and **Reset**, or simply tune
the dial by hand: a move inside the receive passband is kept as the nudge
offset and carried through every later retune.

Tracking stops by itself, and the reason is shown, when:

- the pass ends (LOS);
- the radio disconnects, or a file replay replaces the live session;
- the transmitter is armed or keyed;
- the dial is tuned by hand outside the tracked passband (half the receive
  filter width, at least 250 Hz either side);
- the orbital elements become more than 14 days old, the planner's stale
  threshold;
- orbital propagation fails, or the radio refuses the retune (for example a
  linked-VFO mode);
- you press **Stop**. VFO A stays where it is.

## Local transponder catalog

Pass files can include up to 64 catalog entries, associated by NORAD
catalog number. Keep a local JSON array and pass it to the converter
with `--transponders transponders.json`. The catalog has no network source
inside HermitSDR. Record the provider and date in each entry's `source`
field. This example uses synthetic frequencies.

```json
[
  {
    "catalogNumber": 25544,
    "name": "Example linear passband",
    "source": "Synthetic planning example",
    "uplinkLowHz": 145900000,
    "uplinkHighHz": 145920000,
    "downlinkLowHz": 435800000,
    "downlinkHighHz": 435820000,
    "inverting": true
  }
]
```

Use integer hertz. A fixed-frequency entry has identical low and high
values. For a downlink-only beacon, omit both uplink fields and
`inverting`. Paired ranges have equal widths and include the inversion
flag. The app rejects entries for satellites outside the pass plan.

Open **Transponder catalog** for the selected pass. Preview the downlink
center or enter a nominal uplink within a linear passband to preview the
mapped nominal downlink. The Doppler preview applies only the downlink
estimate. The catalog and preview do not set any radio frequency.

[AMSAT's explanation of inverting and non-inverting transponders](https://www.amsat.org/wordpress/xtra/Getting%20Started%205.pdf)

For a linear transponder, enter the nominal uplink at the satellite. The
catalog shows the predicted ground uplink and receive frequencies at the
first, peak and last looks. The calculation maps the nominal frequency
through the transponder and applies first-order Doppler in each direction.
The rows are planning values and do not tune or key a radio.

## Logging a completed contact

In **Log → QSO Log**, add or edit the contact and expand **Satellite contact**.
Enable **Contact made through a satellite** only for a completed satellite QSO.
Enter the satellite name and, if known, its uplink/downlink code. ADIF export
writes `PROP_MODE=SAT`, `SAT_NAME` and the optional `SAT_MODE`. Viewing a pass or
previewing a Doppler correction does not mark any contact as satellite.

In **Worked & Confirmed**, **Satellite grids** counts explicitly tagged
satellite contacts separately from **Grids**. Both use the selected grid
precision, scope and confirmation source. An imported satellite confirmation
must name the same satellite before it can confirm the contact.
