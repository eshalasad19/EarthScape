#!/usr/bin/env python3
"""
streaming_simulator.py  (Alizah)

SIMULATED real-time ingestion (the approved stack has no streaming tool).
Every INTERVAL seconds it takes the next BATCH_SIZE rows from stream_source.csv,
  1) writes them as a small batch file,
  2) uploads that file to HDFS /climate/raw/streaming/,
  3) (optional) inserts the same readings into MongoDB sensor_readings
     through mongosh,
  4) logs the batch.

Run (examples):
  python streaming_simulator.py --source ..\\data-sample\\stream_source.csv --batch-size 100 --interval 15
  python streaming_simulator.py --source stream_source.csv --max-batches 3 --interval 2 --mongo
  python streaming_simulator.py --source stream_source.csv --no-hdfs --max-batches 2 --interval 0   (test without Hadoop)

MongoDB: set the connection string first (password is NOT stored in the script):
  set MONGO_URI=mongodb://es_admin:YOUR_PASSWORD@localhost:27017/earthscape?authSource=earthscape
"""
import argparse
import json
import os
import subprocess
import time
from datetime import datetime

NUM_COLS = {5: "avg_temp_c", 6: "min_temp_c", 7: "max_temp_c", 8: "precip_mm", 9: "humidity_pct", 10: "co2_ppm"}


def log(msg, logfile):
    line = f"{datetime.now().isoformat(timespec='seconds')} {msg}"
    print(line)
    with open(logfile, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def to_doc(parts):
    doc = {"station_id": parts[0], "date": parts[1], "region": parts[2],
           "latitude": float(parts[3]) if parts[3] else None,
           "longitude": float(parts[4]) if parts[4] else None}
    for i, name in NUM_COLS.items():
        doc[name] = float(parts[i]) if parts[i] else None
    return doc


def write_mongo_js(rows, path):
    docs = [to_doc(r.split(",")) for r in rows]
    js = ('db = db.getSiblingDB("earthscape");\n'
          f"const docs = {json.dumps(docs)};\n"
          "docs.forEach(d => d.date = new Date(d.date));\n"
          "const r = db.sensor_readings.insertMany(docs);\n"
          "print('inserted ' + Object.keys(r.insertedIds).length);\n")
    with open(path, "w", encoding="utf-8") as f:
        f.write(js)


def run(cmd):
    return subprocess.run(cmd, shell=(os.name == "nt"), capture_output=True, text=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="stream_source.csv (header-less, shared schema)")
    ap.add_argument("--batch-size", type=int, default=100)
    ap.add_argument("--interval", type=float, default=15, help="seconds between batches")
    ap.add_argument("--max-batches", type=int, default=0, help="0 = until the source file ends")
    ap.add_argument("--hdfs-dir", default="/climate/raw/streaming")
    ap.add_argument("--no-hdfs", action="store_true", help="skip HDFS upload (testing)")
    ap.add_argument("--mongo", action="store_true", help="also insert into MongoDB (needs MONGO_URI and mongosh)")
    ap.add_argument("--work-dir", default="stream_batches")
    ap.add_argument("--log", default=os.path.join("logs", "streaming.log"))
    args = ap.parse_args()

    os.makedirs(args.work_dir, exist_ok=True)
    os.makedirs(os.path.dirname(args.log) or ".", exist_ok=True)
    mongo_uri = os.environ.get("MONGO_URI", "")
    if args.mongo and not mongo_uri:
        raise SystemExit("MONGO_URI is not set (see the header of this script).")

    with open(args.source, encoding="utf-8") as f:
        rows = [ln.rstrip("\r\n") for ln in f if ln.strip()]
    log(f"source rows={len(rows)} batch_size={args.batch_size} interval={args.interval}s", args.log)

    batch_no, pos = 0, 0
    while pos < len(rows):
        batch = rows[pos:pos + args.batch_size]
        pos += len(batch)
        batch_no += 1
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = f"batch_{stamp}_{batch_no:04d}.csv"
        local = os.path.join(args.work_dir, name)
        with open(local, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(batch) + "\n")

        hdfs_status = "SKIPPED"
        if not args.no_hdfs:
            run(["hdfs", "dfs", "-mkdir", "-p", args.hdfs_dir])
            res = run(["hdfs", "dfs", "-put", "-f", local, args.hdfs_dir + "/"])
            hdfs_status = "OK" if res.returncode == 0 else "FAILED " + res.stderr.strip()[:120]

        mongo_status = "SKIPPED"
        if args.mongo:
            js = os.path.join(args.work_dir, name.replace(".csv", ".js"))
            write_mongo_js(batch, js)
            res = run(["mongosh", mongo_uri, "--quiet", "--file", js])
            mongo_status = "OK" if res.returncode == 0 else "FAILED " + (res.stderr or res.stdout).strip()[:120]

        log(f"batch={batch_no} rows={len(batch)} file={name} hdfs={hdfs_status} mongo={mongo_status}", args.log)
        if args.max_batches and batch_no >= args.max_batches:
            break
        if pos < len(rows):
            time.sleep(args.interval)
    log("finished", args.log)


if __name__ == "__main__":
    main()