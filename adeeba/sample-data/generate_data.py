#!/usr/bin/env python
"""Bada test data banata hai (shared schema). Sirf standard library.
Usage: python generate_data.py OUTPUT.csv [--stations 20] [--start 2020] [--end 2023]
Output ko repo ke bahar rakho, misaal C:\\earthscape-data\\big_test.csv
"""
import argparse, csv, datetime, math, random

REGIONS = {  # region: (base temp, latitude, longitude)
    "North": (12.0, 34.0, 72.0), "South": (26.0, 24.9, 67.0),
    "East": (20.0, 31.5, 74.3), "West": (22.0, 30.2, 66.9),
    "Central": (18.0, 31.0, 70.0),
}

def maybe_missing(value, p, rng):
    return "" if rng.random() < p else value

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("output")
    ap.add_argument("--stations", type=int, default=20)
    ap.add_argument("--start", type=int, default=2020)
    ap.add_argument("--end", type=int, default=2023)
    ap.add_argument("--missing", type=float, default=0.05)
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    names = list(REGIONS)
    stations = []
    for i in range(a.stations):
        r = names[i % len(names)]
        stations.append(("ST%03d" % (i + 1), r))
    rows = 0
    with open(a.output, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["station_id", "date", "region", "latitude", "longitude", "avg_temp_c",
                    "min_temp_c", "max_temp_c", "precip_mm", "humidity_pct", "co2_ppm"])
        d = datetime.date(a.start, 1, 1)
        end = datetime.date(a.end, 12, 31)
        while d <= end:
            season = math.sin((d.timetuple().tm_yday - 80) / 365.0 * 2 * math.pi)
            for sid, region in stations:
                base, lat, lon = REGIONS[region]
                t = base + 10 * season + rng.gauss(0, 1.2)
                if rng.random() < 0.003:            # kabhi kabhi outlier (anomaly test ke liye)
                    t += rng.choice([-1, 1]) * 15
                co2 = 405 + 2.5 * (d.year - a.start) + 0.3 * t + rng.gauss(0, 1.0)
                precip = max(0.0, rng.gauss(2, 3)) if rng.random() < 0.4 else 0.0
                hum = min(100, max(10, 60 - 0.8 * (t - base) + rng.gauss(0, 6)))
                p = a.missing
                w.writerow([sid, d.isoformat(), region, lat, lon,
                            maybe_missing(round(t, 1), p, rng),
                            maybe_missing(round(t - 5 - abs(rng.gauss(0, 1)), 1), p, rng),
                            maybe_missing(round(t + 5 + abs(rng.gauss(0, 1)), 1), p, rng),
                            maybe_missing(round(precip, 1), p, rng),
                            maybe_missing(round(hum), p, rng),
                            maybe_missing(round(co2, 1), p, rng)])
                rows += 1
            d += datetime.timedelta(days=1)
    print("%d rows -> %s" % (rows, a.output))

if __name__ == "__main__":
    main()