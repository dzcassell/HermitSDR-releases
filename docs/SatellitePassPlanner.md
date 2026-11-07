# Satellite Pass Planner

Open **Radio → Satellite Pass Planner** and import a local pass plan. The
window shows geometric visibility from the modeled coordinates, UTC
start and end, orbital element source and epoch, and a true-azimuth sky
plot. The plot's outer ring is the horizon and its center is the zenith.
Use the three labeled rows for the first, highest sampled, and last look
angles. A pass already in progress at an analysis boundary is marked.

Use the star to favorite a satellite by its catalog number. The app
keeps one pass plan in the station profile and preserves favorites when
you replace the plan. Compare the modeled observer coordinates with your
configured grid center. If the element epoch is more than 14 days from a
pass, the detail warns that the prediction uses distant elements.

Use the optional `tools/tle-to-satellite-passes.py` converter with a local
two-line element file and a separate Python environment containing
[Skyfield](https://rhodesmill.org/skyfield/installation.html). The app
imports the result. It does not install Python, fetch orbital elements,
or bundle the MIT-licensed library or its dependencies.
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
to validate a plan before opening it. The planner is passive. It does not
assign a transponder, tune the radio or move an antenna.

Expand **Downlink Doppler preview** and enter the satellite's nominal
downlink in MHz. The first, peak-elevation and last looks show a signed
shift and estimated receive frequency. Approaching range gives a positive
shift. New plans include Skyfield’s modeled line-of-sight range rate at
each look. Older plans estimate it from adjacent range samples. The
Doppler row’s tooltip identifies the source. Distant orbital epochs can
reduce accuracy. Use the preview for manual receive planning.
[How Doppler tracking uses range rate](https://www.jpl.nasa.gov/edu/resources/lesson-plan/exploring-the-doppler-effect-with-nasa/)

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
