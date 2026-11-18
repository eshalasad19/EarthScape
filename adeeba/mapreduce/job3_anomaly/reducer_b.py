#!/usr/bin/env python
# Pass B reducer: z-score nikalo, |z| > THRESHOLD ho to anomaly
import sys
from config import THRESHOLD

def flush(key, stats, data):
    if stats is None:
        return
    n, mean, std = stats
    if std == 0:
        return
    station, month, metric = key.split("|")
    for date, v in data:
        z = (v - mean) / std
        if abs(z) > THRESHOLD:
            print("%s,%s,%s,%s,%.2f,%.2f,%.2f" % (station, date, metric, v, mean, std, z))

current, stats, data = None, None, []
for line in sys.stdin:
    key, val = line.rstrip("\r\n").split("\t")
    if key != current:
        if current is not None:
            flush(current, stats, data)
        current, stats, data = key, None, []
    p = val.split(",")
    if p[0] == "S":
        stats = (int(p[1]), float(p[2]), float(p[3]))
    else:
        data.append((p[1], float(p[2])))
if current is not None:
    flush(current, stats, data)