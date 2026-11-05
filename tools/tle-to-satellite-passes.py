#!/usr/bin/env python3
"""Generate HermitSDR pass-planning JSON from local LEO TLEs and Skyfield."""
import argparse
from datetime import datetime, timedelta, timezone
import json
import math
from pathlib import Path
import stat
import sys


def utc(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("The planning start needs an explicit UTC offset.")
    result = parsed.astimezone(timezone.utc).replace(microsecond=0)
    if not 1957 <= result.year <= 2099:
        raise ValueError("The start year must be 1957–2099.")
    return result


def stamp(value):
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def validate_tle(line, number):
    if len(line) != 69 or not line.startswith(f"{number} ") or not line[-1].isdigit():
        raise ValueError("Each TLE requires two numbered, 69-column lines.")
    checksum = sum(int(char) if char.isdigit() else char == "-" for char in line[:-1])
    if checksum % 10 != int(line[-1]):
        raise ValueError("A TLE failed its checksum.")


def load_elements(path, time_scale, constructor):
    if not stat.S_ISREG(path.stat().st_mode):
        raise ValueError("Choose a regular local TLE file.")
    with path.open("rb") as source:
        data = source.read(32_769)
    if len(data) > 32_768:
        raise ValueError("TLE file exceeds 32 KiB.")
    lines = [line.rstrip() for line in data.decode("ascii").splitlines() if line.strip()]
    satellites = []
    seen = set()
    while lines:
        name = None
        if not lines[0].startswith("1 "):
            name = lines.pop(0).removeprefix("0 ").strip()
            if not 1 <= len(name) <= 80 or not name.isprintable():
                raise ValueError("Satellite names must be printable and up to 80 characters.")
        if len(lines) < 2 or len(satellites) == 16:
            raise ValueError("Use one to sixteen complete TLE records.")
        first, second = lines.pop(0), lines.pop(0)
        validate_tle(first, 1)
        validate_tle(second, 2)
        if first[2:7] != second[2:7]:
            raise ValueError("A TLE pair identifies different catalog objects.")
        satellite = constructor(first, second, name or f"NORAD {first[2:7].strip()}", time_scale)
        identity = satellite.model.satnum
        if identity in seen:
            raise ValueError("Use one set of orbital elements for each satellite.")
        mean_motion = satellite.model.no_kozai
        period = 2 * math.pi / mean_motion if mean_motion > 0 else math.inf
        if not 70 <= period <= 150 or not 0 <= satellite.model.ecco <= 0.2:
            raise ValueError(f"{satellite.name}: this converter supports low Earth orbits of 70–150 minutes.")
        seen.add(identity)
        satellites.append(satellite)
    if not satellites:
        raise ValueError("The file contains no TLE records.")
    return satellites


def visible_intervals(satellite, station, time_scale, start, end, minimum):
    # Pad the search so a pass crossing either user boundary still has
    # its original rise, culmination and set in the search window.
    search_start = start - timedelta(hours=3)
    search_end = end + timedelta(hours=3)
    t0 = time_scale.from_datetime(search_start)
    t1 = time_scale.from_datetime(search_end)
    look = satellite - station
    begins_visible = look.at(t0).altaz()[0].degrees >= minimum
    active = search_start if begins_visible else None
    peaks = []
    times, events = satellite.find_events(station, t0, t1, altitude_degrees=minimum)
    for time, event in zip(times, events):
        at = time.utc_datetime()
        if event == 0 and active is None:
            active = at
            peaks = []
        elif event == 1 and active is not None:
            peaks.append(at)
        elif event == 2 and active is not None:
            yield active, at, peaks
            active = None
    if active is not None and look.at(t1).altaz()[0].degrees >= minimum:
        yield active, search_end, peaks


def pass_rows(satellite, station, time_scale, start, end, minimum):
    for rise, setting, peaks in visible_intervals(satellite, station, time_scale, start, end, minimum):
        first = math.ceil(max(start, rise).timestamp())
        last = math.floor(min(end, setting).timestamp())
        duration = last - first
        if duration < 1:
            continue
        if duration > 3_600:
            raise ValueError(f"{satellite.name}: a predicted LEO window exceeded one hour.")
        # Include each reported culmination and evenly spaced path points.
        offsets = {round(duration * step / 32) for step in range(33)}
        offsets.update(round(peak.timestamp()) - first for peak in peaks if first <= peak.timestamp() <= last)
        offsets = sorted(offsets)
        if len(offsets) > 64:
            raise ValueError("A predicted pass has too many distinct culminations.")
        times = time_scale.from_datetimes([datetime.fromtimestamp(first + offset, timezone.utc) for offset in offsets])
        el, az, distance = (satellite - station).at(times).altaz()
        samples = []
        for offset, bearing, elevation, km in zip(offsets, az.degrees, el.degrees, distance.km):
            bearing, elevation, km = float(bearing), float(elevation), float(km)
            if not all(map(math.isfinite, (bearing, elevation, km))):
                raise ValueError(f"{satellite.name}: orbital propagation failed in the requested window.")
            samples.append({"offsetSeconds": offset, "azimuthDegrees": round(bearing, 3) % 360,
                            "elevationDegrees": round(elevation, 3), "rangeKM": round(km, 3)})
        yield {
            "catalogNumber": satellite.model.satnum, "startsAt": stamp(datetime.fromtimestamp(first, timezone.utc)),
            "endsAt": stamp(datetime.fromtimestamp(last, timezone.utc)),
            "startsInProgress": rise < start, "endsInProgress": setting > end, "samples": samples,
        }


def observer_coordinates(args):
    if args.grid is None:
        if args.latitude is None or args.longitude is None:
            raise ValueError("Supply both observer coordinates or one Maidenhead grid.")
        return args.latitude, args.longitude
    if args.latitude is not None or args.longitude is not None:
        raise ValueError("Choose either a Maidenhead grid or decimal coordinates.")
    grid = args.grid.strip()
    if not grid.isascii():
        raise ValueError("Use a four- or six-character Maidenhead grid.")
    grid = grid.upper()
    if (len(grid) not in (4, 6) or not all("A" <= char <= "R" for char in grid[:2])
            or not grid[2:4].isdigit() or not all("A" <= char <= "X" for char in grid[4:])):
        raise ValueError("Use a four- or six-character Maidenhead grid.")
    longitude = (ord(grid[0]) - ord("A")) * 20 - 180 + int(grid[2]) * 2
    latitude = (ord(grid[1]) - ord("A")) * 10 - 90 + int(grid[3])
    if len(grid) == 4:
        return latitude + 0.5, longitude + 1
    return latitude + (ord(grid[5]) - ord("A") + 0.5) / 24, longitude + (ord(grid[4]) - ord("A") + 0.5) / 12


def convert(args):
    try:
        import skyfield
        from skyfield.api import EarthSatellite, load, wgs84
    except ImportError as error:
        raise ValueError("Install Skyfield in a separate Python environment to run the converter.") from error
    start = utc(args.start)
    source = args.source.strip()
    latitude, longitude = observer_coordinates(args)
    if not (-90 <= latitude <= 90 and -180 <= longitude <= 180
            and -500 <= args.elevation_m <= 9_000 and 0 <= args.minimum_elevation <= 80
            and 1 <= args.hours <= 72 and 1 <= len(source.encode("utf8")) <= 160 and source.isprintable()):
        raise ValueError("Check observer coordinates, elevation, source, 1–72 planning hours and 0–80° threshold.")
    end = start + timedelta(hours=args.hours)
    time_scale = load.timescale(builtin=True)
    satellites = load_elements(args.tle, time_scale, EarthSatellite)
    station = wgs84.latlon(latitude, longitude, elevation_m=args.elevation_m)
    passes = []
    for satellite in satellites:
        passes.extend(pass_rows(satellite, station, time_scale, start, end, args.minimum_elevation))
        if len(passes) > 256:
            raise ValueError("The plan exceeds 256 passes. Use fewer satellites or a shorter window.")
    return {
        "schemaVersion": 1,
        "model": "Skyfield SGP4",
        "modelVersion": skyfield.__version__,
        "elementSource": source,
        "generatedAt": stamp(datetime.now(timezone.utc)),
        "windowStart": stamp(start),
        "windowEnd": stamp(end),
        "minimumElevationDegrees": args.minimum_elevation,
        "observer": {"latitude": latitude, "longitude": longitude, "elevationM": args.elevation_m},
        "satellites": [{"catalogNumber": satellite.model.satnum, "name": satellite.name,
                        "elementsAt": stamp(satellite.epoch.utc_datetime())} for satellite in satellites],
        "passes": sorted(passes, key=lambda item: (item["startsAt"], item["catalogNumber"])),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tle", type=Path, help="local two- or three-line elements, up to sixteen satellites")
    parser.add_argument("--source", required=True, help="provenance label for the TLE file")
    parser.add_argument("--grid", help="four- or six-character Maidenhead observer grid")
    parser.add_argument("--latitude", type=float)
    parser.add_argument("--longitude", type=float)
    parser.add_argument("--elevation-m", type=float, default=0)
    parser.add_argument("--start", required=True, help="start date and time with explicit UTC offset")
    parser.add_argument("--hours", type=int, default=24)
    parser.add_argument("--minimum-elevation", type=float, default=10)
    args = parser.parse_args()
    try:
        text = json.dumps(convert(args), indent=2, allow_nan=False)
        if len(text.encode("utf8")) > 1_048_575:
            raise ValueError("The generated plan exceeds 1 MiB. Use fewer satellites or a shorter window.")
        print(text)
    except (OSError, ValueError, OverflowError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
