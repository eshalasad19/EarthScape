#!/usr/bin/env python3
"""
generate_sample_data.py  (Alizah)

Creates SYNTHETIC climate data in the shared project schema.
Use it ONLY as a stand-in so everyone can develop and test before the real
public dataset is ready. Replace it with real data for the final submission
(see standardize_csv.py).

Output (header-less CSV, 11 columns, blank = missing value):
  station_id,date,region,latitude,longitude,avg_temp_c,min_temp_c,max_temp_c,
  precip_mm,humidity_pct,co2_ppm

Layout:
  <out>/historical/year=YYYY/data_YYYY.csv   -> goes to /climate/raw/historical
  <out>/stream_source.csv                    -> used by streaming_simulator.py

Run:
  python generate_sample_data.py --out C:\\earthscape-data\\sample
  python generate_sample_data.py --out ../data-sample --stations 4 --start 2020 --end 2023
"""
import argparse
import math
import os
import random
from datetime import date, timedelta

# region, code, base temp C, seasonal amplitude, lat, lon, humidity base, rain probability
REGIONS = [
    ("South Asia", "SA", 26.0, 7.0, 24.9, 67.0, 62, 0.18),
    ("Europe", "EU", 11.0, 10.0, 48.8, 2.3, 72, 0.35),
    ("North America", "NA", 12.0, 12.0, 39.0, -98.0, 60, 0.25),
    ("Africa", "AF", 25.0, 4.0, 1.3, 32.5, 66, 0.30),
    ("Oceania", "OC", 18.0, 8.0, -33.9, 151.2, 65, 0.28),
]

MISSING_RATE = 0.03      # per numeric field
ANOMALY_RATE = 0.002     # temperature spikes (so anomaly detection has something to find)


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def fmt(v, nd=2):
    return "" if v is None else str(round(v, nd))


def make_stations(per_region, rng):
    stations = []
    for name, code, base, amp, lat, lon, hum, rain in REGIONS:
        for i in range(1, per_region + 1):
            stations.append({
                "id": f"{code}{i:03d}", "region": name, "base": base, "amp": amp,
                "lat": lat + rng.uniform(-1.5, 1.5), "lon": lon + rng.uniform(-1.5, 1.5),
                "hum": hum, "rain": rain, "offset": rng.uniform(-1.0, 1.0),
            })
    return stations


def day_row(st, d, start_year, rng):
    doy = d.timetuple().tm_yday
    season = math.sin(2 * math.pi * (doy - 80) / 365.25)
    if st["lat"] < 0:
        season = -season
    temp = (st["base"] + st["offset"] + st["amp"] * season
            + 0.03 * (d.year - start_year) + rng.gauss(0, 1.8))
    if rng.random() < ANOMALY_RATE:
        temp += rng.choice([-1, 1]) * rng.uniform(10, 15)
    tmin = temp - rng.uniform(3, 6)
    tmax = temp + rng.uniform(3, 6)
    precip = rng.expovariate(1 / 8.0) if rng.random() < st["rain"] else 0.0
    humidity = clamp(st["hum"] - 8 * season + rng.gauss(0, 8), 5, 100)
    co2 = 370 + 2.1 * (d.year - 2000 + doy / 365.0) + 3 * math.sin(2 * math.pi * doy / 365.0) + rng.gauss(0, 0.5)

    vals = [temp, tmin, tmax, precip, humidity, co2]
    vals = [None if rng.random() < MISSING_RATE else v for v in vals]
    return [st["id"], d.isoformat(), st["region"], fmt(st["lat"], 3), fmt(st["lon"], 3),
            fmt(vals[0]), fmt(vals[1]), fmt(vals[2]), fmt(vals[3], 1), fmt(vals[4], 1), fmt(vals[5])]


def main():
    ap = argparse.ArgumentParser(description="Generate synthetic climate data (test stand-in).")
    ap.add_argument("--out", required=True, help="output folder")
    ap.add_argument("--stations", type=int, default=4, help="stations per region (5 regions)")
    ap.add_argument("--start", type=int, default=2000, help="first year")
    ap.add_argument("--end", type=int, default=2023, help="last historical year")
    ap.add_argument("--stream-days", type=int, default=90, help="days in stream_source.csv (year end+1)")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    stations = make_stations(args.stations, rng)
    total = 0

    for year in range(args.start, args.end + 1):
        folder = os.path.join(args.out, "historical", f"year={year}")
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, f"data_{year}.csv")
        d = date(year, 1, 1)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            while d.year == year:
                for st in stations:
                    f.write(",".join(day_row(st, d, args.start, rng)) + "\n")
                    total += 1
                d += timedelta(days=1)
        print(f"wrote {path}")

    stream_path = os.path.join(args.out, "stream_source.csv")
    d = date(args.end + 1, 1, 1)
    n = 0
    with open(stream_path, "w", encoding="utf-8", newline="\n") as f:
        for _ in range(args.stream_days):
            for st in stations:
                f.write(",".join(day_row(st, d, args.start, rng)) + "\n")
                n += 1
            d += timedelta(days=1)
    print(f"wrote {stream_path}")
    print(f"historical rows: {total}, stream rows: {n}, stations: {len(stations)}")


if __name__ == "__main__":
    main()