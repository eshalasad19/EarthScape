#!/usr/bin/env python3
"""
04_retrain.py  (Wania)  -  one command to refresh all ML results ("models are updated regularly").

  python 04_retrain.py                 -> runs 01_trend_prediction.py and 02_anomaly_detection.py
  python 04_retrain.py --pull          -> first copies the latest data from HDFS into .\\data
  python 04_retrain.py --pull --upload -> also uploads results to /climate/ml_output on HDFS

Run it again whenever new data (for example new streaming batches) has been processed by Adeeba's jobs.
Each run appends its metrics to output/model_log.csv.
"""
import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NT = os.name == "nt"
PULL = {"clean": "data/clean.csv", "yearly_region_avg": "data/yearly_region_avg.csv", "anomalies": "data/anomalies.csv"}


def run(cmd):
    print(">", " ".join(cmd))
    return subprocess.run(cmd, cwd=HERE, shell=NT).returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pull", action="store_true")
    ap.add_argument("--upload", action="store_true")
    a = ap.parse_args()

    if a.pull:
        os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
        for folder, target in PULL.items():
            t = os.path.join(HERE, target)
            if os.path.exists(t):
                os.remove(t)
            run(["hdfs", "dfs", "-getmerge", f"/climate/processed/{folder}", target])

    for script in ("01_trend_prediction.py", "02_anomaly_detection.py"):
        if run([sys.executable, script]) != 0:
            raise SystemExit(f"{script} failed")

    if a.upload:
        for folder in ("predictions", "ml_anomalies"):
            src = os.path.join("output", "hdfs", folder)
            run(["hdfs", "dfs", "-mkdir", "-p", f"/climate/ml_output/{folder}"])
            run(["hdfs", "dfs", "-put", "-f", src + os.sep + "*", f"/climate/ml_output/{folder}/"])
        print("uploaded to /climate/ml_output")
    print("retraining finished. Metrics: output/model_log.csv")


if __name__ == "__main__":
    main()