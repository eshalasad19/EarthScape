#!/usr/bin/env python3
"""
load_historical.py  (Alizah)

Splits standardized CSV file(s) by year and uploads them to HDFS:
  /climate/raw/historical/year=YYYY/<file>.csv

Needs Hadoop running (start-dfs.cmd) and 'hdfs' on PATH.

Run:
  python load_historical.py --input C:\\earthscape-data\\std\\noaa_std.csv
  python load_historical.py --input ../data-sample/historical --dry-run
(--input can be a file or a folder; folders are searched recursively for *.csv)
"""
import argparse
import glob
import os
import subprocess
import sys


def hdfs(args, dry):
    cmd = ["hdfs", "dfs"] + args
    print(">", " ".join(cmd))
    if dry:
        return 0
    return subprocess.run(cmd, shell=(os.name == "nt")).returncode


def find_files(path):
    if os.path.isdir(path):
        return sorted(glob.glob(os.path.join(path, "**", "*.csv"), recursive=True))
    return [path]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--work-dir", default=os.path.join(os.path.expanduser("~"), "earthscape_by_year"))
    ap.add_argument("--hdfs-base", default="/climate/raw/historical")
    ap.add_argument("--dry-run", action="store_true", help="split locally, only print the HDFS commands")
    args = ap.parse_args()

    handles = {}
    counts = {}
    for src in find_files(args.input):
        base = os.path.splitext(os.path.basename(src))[0]
        with open(src, encoding="utf-8") as f:
            for line in f:
                parts = line.split(",", 2)
                if len(parts) < 3 or len(parts[1]) < 4 or not parts[1][:4].isdigit():
                    continue
                year = parts[1][:4]
                key = (year, base)
                if key not in handles:
                    folder = os.path.join(args.work_dir, f"year={year}")
                    os.makedirs(folder, exist_ok=True)
                    handles[key] = open(os.path.join(folder, f"{base}.csv"), "w", encoding="utf-8", newline="\n")
                    counts[key] = 0
                handles[key].write(line if line.endswith("\n") else line + "\n")
                counts[key] += 1
    for h in handles.values():
        h.close()

    failures = 0
    for (year, base), n in sorted(counts.items()):
        local = os.path.join(args.work_dir, f"year={year}", f"{base}.csv")
        target = f"{args.hdfs_base}/year={year}"
        print(f"year={year} file={base} rows={n}")
        failures += hdfs(["-mkdir", "-p", target], args.dry_run) != 0
        failures += hdfs(["-put", "-f", local, target + "/"], args.dry_run) != 0
    if not args.dry_run:
        hdfs(["-ls", "-R", args.hdfs_base], False)
    if failures:
        print(f"{failures} HDFS command(s) failed. Is Hadoop running?")
        sys.exit(1)
    print("done")


if __name__ == "__main__":
    main()