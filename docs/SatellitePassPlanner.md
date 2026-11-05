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
and 256 passes. The chosen elevation threshold defines the pass edges.
[Sgp4 satellite and pass documentation](https://rhodesmill.org/skyfield/earth-satellites.html)

Use the app executable's `--hermit-check-satellite-passes passes.json` mode
to validate a plan before opening it. The planner is passive. It does not
assign a transponder, correct Doppler, change the radio or move an antenna.
