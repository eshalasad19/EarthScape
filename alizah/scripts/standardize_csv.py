#!/usr/bin/env python3
"""
standardize_csv.py  (Alizah)

Converts a REAL public climate CSV (with a header row) into the shared project
schema (header-less, 11 columns, blank = missing). Edit the MAPPING section for
each source dataset, then run:

  python standardize_csv.py --input noaa_raw.csv --output C:\\earthscape-data\\std\\noaa_std.csv

Rules:
  * Missing values are left BLANK. They are NOT filled here. Adeeba's
    MapReduce job (job1_quality) handles missing data.
  * Dates are converted to YYYY-MM-DD.
"""
import argparse
import csv
from datetime import datetime

SCHEMA = ["station_id", "date", "region", "latitude", "longitude",
          "avg_temp_c", "min_temp_c", "max_temp_c", "precip_mm", "humidity_pct", "co2_ppm"]

# ---- EDIT THIS PART FOR EACH SOURCE FILE -----------------------------------
# schema column -> column name in the source file (None = not in source)
MAPPING = {
    "station_id": "STATION",
    "date": "DATE",
    "region": None,            # not in source -> use CONSTANTS below
    "latitude": "LATITUDE",
    "longitude": "LONGITUDE",
    "avg_temp_c": "TAVG",
    "min_temp_c": "TMIN",
    "max_temp_c": "TMAX",
    "precip_mm": "PRCP",
    "humidity_pct": None,
    "co2_ppm": None,
}

# fixed values for columns the source does not have (leave {} if none)
CONSTANTS = {"region": "South Asia"}

# unit conversions applied to a numeric value (example: Fahrenheit -> Celsius)
CONVERT = {
    # "avg_temp_c": lambda v: (v - 32) * 5 / 9,
    # "min_temp_c": lambda v: (v - 32) * 5 / 9,
    # "max_temp_c": lambda v: (v - 32) * 5 / 9,
}

DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y%m%d", "%d-%m-%Y"]
MISSING_VALUES = {"", "NA", "N/A", "NaN", "nan", "NULL", "null", "-9999", "-999", "-99.9", "9999"}
# -----------------------------------------------------------------------------

NUMERIC = {"latitude", "longitude", "avg_temp_c", "min_temp_c", "max_temp_c",
           "precip_mm", "humidity_pct", "co2_ppm"}


def parse_date(text):
    text = text.strip()
    for f in DATE_FORMATS:
        try:
            return datetime.strptime(text, f).date().isoformat()
        except ValueError:
            continue
    return None


def convert_value(col, raw):
    raw = (raw or "").strip()
    if raw in MISSING_VALUES:
        return ""
    if col in NUMERIC:
        try:
            v = float(raw)
        except ValueError:
            return ""
        if col in CONVERT:
            v = CONVERT[col](v)
        return str(round(v, 3 if col in ("latitude", "longitude") else 2))
    return raw.replace(",", " ")  # commas would break the CSV


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--encoding", default="utf-8-sig")
    args = ap.parse_args()

    read = written = skipped = 0
    with open(args.input, newline="", encoding=args.encoding) as fin, \
         open(args.output, "w", encoding="utf-8", newline="\n") as fout:
        reader = csv.DictReader(fin)
        for col, src in MAPPING.items():
            if src is not None and src not in reader.fieldnames:
                raise SystemExit(f"Column '{src}' (for '{col}') not found. Source columns: {reader.fieldnames}")
        for row in reader:
            read += 1
            out = []
            for col in SCHEMA:
                if col == "date":
                    d = parse_date(row.get(MAPPING["date"], ""))
                    if d is None:
                        out = None
                        break
                    out.append(d)
                elif MAPPING.get(col):
                    out.append(convert_value(col, row.get(MAPPING[col])))
                else:
                    out.append(CONSTANTS.get(col, ""))
            if out is None or not out[0]:
                skipped += 1
                continue
            fout.write(",".join(out) + "\n")
            written += 1
    print(f"read={read} written={written} skipped(bad date/station)={skipped}")


if __name__ == "__main__":
    main()