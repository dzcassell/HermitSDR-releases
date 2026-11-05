#!/usr/bin/env python3
"""Convert an operator's point-to-point ITURHFProp -c report to HermitSDR JSON."""
import argparse
import csv
from datetime import datetime, timezone
import io
import json
import math
from pathlib import Path, PureWindowsPath
import re
import sys


MAX_BYTES = 262_144
KEY_VALUE = re.compile(r'^\s*([A-Za-z0-9_.]+)\s+(?:"([^"]*)"|([^\s]+))')
REFERENCE = "https://github.com/ITU-R-Study-Group-3/ITU-R-HF"


def read_text(path):
    with path.open("rb") as stream:
        data = stream.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("Input exceeds 256 KiB")
    return data.decode("utf-8-sig")


def parse_input(text):
    required = {
        "PathTXName", "PathRXName", "Path.L_tx.lat", "Path.L_tx.lng",
        "Path.L_rx.lat", "Path.L_rx.lng", "Path.year", "Path.month",
        "Path.SSN", "Path.txpower", "Path.BW", "Path.SNRr", "Path.hour", "Path.frequency",
        "TXAntFilePath", "RXAntFilePath", "Path.ManMadeNoise", "Path.Modulation", "Path.SorL",
        *(corner + "." + axis for corner in ("LL", "LR", "UL", "UR") for axis in ("lat", "lng")),
    }
    settings = {}
    for line in text.splitlines():
        match = KEY_VALUE.match(line)
        if not match or match[1] not in required:
            continue
        key, quoted, unquoted = match.groups()
        if key in settings:
            raise ValueError(f"Duplicate input setting {key}")
        if key in ("Path.hour", "Path.frequency"):
            settings[key] = line.strip()[len(key):].split("//", 1)[0].strip()
        else:
            settings[key] = quoted if quoted is not None else unquoted
    missing = sorted(required - settings.keys())
    if missing:
        raise ValueError("Missing input settings: " + ", ".join(missing))

    def endpoint(role):
        return {
            "name": settings[f"Path{role.upper()}Name"].strip(),
            "latitude": float(settings[f"Path.L_{role}.lat"]),
            "longitude": float(settings[f"Path.L_{role}.lng"]),
        }

    tx, rx = endpoint("tx"), endpoint("rx")
    for item in (tx, rx):
        if not (-90 <= item["latitude"] <= 90 and -180 <= item["longitude"] <= 180):
            raise ValueError("Endpoint is outside the coordinate range")
    for corner in ("LL", "LR", "UL", "UR"):
        lat = float(settings[f"{corner}.lat"])
        lon = float(settings[f"{corner}.lng"])
        if not (math.isclose(lat, rx["latitude"], abs_tol=1e-5)
                and math.isclose(lon, rx["longitude"], abs_tol=1e-5)):
            raise ValueError("Use a point-to-point run with all four corners at Path.L_rx")

    def antenna(key):
        return PureWindowsPath(settings[key].rstrip("/\\")).name or "unspecified"

    assumptions = {
        "year": int(settings["Path.year"]), "month": int(settings["Path.month"]),
        "solarIndexR12": int(settings["Path.SSN"]),
        "transmitPowerWatts": 1000 * 10 ** (float(settings["Path.txpower"]) / 10),
        "bandwidthHz": float(settings["Path.BW"]), "requiredSNRDb": float(settings["Path.SNRr"]),
        "transmitterAntenna": antenna("TXAntFilePath"), "receiverAntenna": antenna("RXAntFilePath"),
        "receiverNoise": settings["Path.ManMadeNoise"], "path": settings["Path.SorL"],
        "modulation": settings["Path.Modulation"],
    }
    if not (1900 <= assumptions["year"] <= 2100 and 1 <= assumptions["month"] <= 12):
        raise ValueError("Use one model month and year")
    hours = [int(value) for value in settings["Path.hour"].split(",")]
    frequencies = [float(value) for value in settings["Path.frequency"].split(",")]
    if (not 1 <= len(hours) <= 24 or len(set(hours)) != len(hours)
            or not all(1 <= hour <= 24 for hour in hours)
            or not 1 <= len(frequencies) <= 16 or not all(1.6 <= frequency <= 30 for frequency in frequencies)
            or len({round(frequency * 1_000_000) for frequency in frequencies}) != len(frequencies)):
        raise ValueError("Use distinct hours and up to sixteen distinct HF frequencies in the model input")
    return tx, rx, assumptions, set(hours), frequencies


def parse_rows(text, month, hours, frequencies):
    reader = csv.DictReader(io.StringIO(text, newline=""))
    fields = reader.fieldnames or []
    metrics = {
        "BCR": ("reliabilityPercent", 0, 100),
        "SNR": ("medianSNRDb", -300, 300),
        "OPMUF": ("operationalMUFMHz", 0, 100),
    }
    if (len(set(fields)) != len(fields) or not {"month", "hour", "frequency"} <= set(fields)
            or not (metrics.keys() & set(fields))):
        raise ValueError("Expected an ITURHFProp -c CSV with month, hour, frequency and BCR, SNR or OPMUF")

    results, keys = [], set()
    for row in reader:
        if None in row or any(value is None for value in row.values()):
            raise ValueError(f"Bad column count on CSV line {reader.line_num}")
        if int(row["month"]) != month:
            raise ValueError(f"CSV month differs from the model input on line {reader.line_num}")
        hour, reported = int(row["hour"]), float(row["frequency"])
        # ITURHFProp's CSV prints frequencies rounded to hundredths of a
        # MHz. Recover the actual model input only when it is unambiguous.
        matching = [frequency for frequency in frequencies if abs(frequency - reported) <= 0.0050000001]
        if hour not in hours or len(matching) != 1:
            raise ValueError(f"CSV hour or rounded frequency does not identify one configured cell on line {reader.line_num}")
        frequency = matching[0]
        key = hour, round(frequency * 1_000_000)
        if key in keys:
            raise ValueError(f"Duplicate frequency and hour on CSV line {reader.line_num}")
        keys.add(key)
        values = {"hourUTC": hour, "frequencyMHz": frequency}
        for column, (name, lower, upper) in metrics.items():
            if column in row and row[column].strip():
                value = float(row[column])
                if not lower <= value <= upper:
                    raise ValueError(f"Invalid {column} on CSV line {reader.line_num}")
                values[name] = value
        if len(values) == 2:
            raise ValueError(f"Missing predictions on CSV line {reader.line_num}")
        results.append(values)
    if len(results) != len(hours) * len(frequencies):
        raise ValueError("CSV does not contain every configured hour and frequency")
    return sorted(results, key=lambda row: (row["hourUTC"], row["frequencyMHz"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="the input used for the model run")
    parser.add_argument("report", type=Path, help="the CSV produced by ITURHFProp -c")
    parser.add_argument("--model-version", required=True, help="the P.533 implementation version used")
    parser.add_argument("--solar-index-month", help="optional R12 input data month, YYYY-MM")
    parser.add_argument("--generated-at", help="optional model run time in ISO 8601 with offset")
    args = parser.parse_args()
    try:
        tx, rx, assumptions, hours, frequencies = parse_input(read_text(args.input))
        if args.solar_index_month:
            if not re.fullmatch(r"(?:19[0-9]{2}|20[0-9]{2}|2100)-(?:0[1-9]|1[0-2])", args.solar_index_month):
                raise ValueError("Use YYYY-MM for the solar input data month")
            assumptions["solarIndexMonth"] = args.solar_index_month
        rows = parse_rows(read_text(args.report), assumptions["month"], hours, frequencies)
        provider = {"model": "ITU-R P.533 / ITURHFProp", "version": args.model_version,
                    "referenceURL": REFERENCE}
        if args.generated_at:
            date = datetime.fromisoformat(args.generated_at.replace("Z", "+00:00"))
            if date.tzinfo is None:
                raise ValueError("Model run time must include a UTC offset")
            provider["generatedAt"] = date.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        document = {"schemaVersion": 1, "provider": provider, "transmitter": tx,
                    "receiver": rx, "assumptions": assumptions, "rows": rows}
        print(json.dumps(document, indent=2, sort_keys=True, allow_nan=False))
    except (ValueError, OverflowError, OSError, csv.Error) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
