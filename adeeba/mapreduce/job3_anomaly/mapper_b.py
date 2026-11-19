#!/usr/bin/env python
# Pass B mapper: input = clean data + Pass A stats (dono ek saath)
import sys
from config import METRICS
for line in sys.stdin:
    line = line.rstrip("\r\n")
    if not line or line.startswith("station_id"):
        continue
    if "\t" in line:                       # Pass A stats line
        key, val = line.split("\t")
        print("%s\tS,%s" % (key, val))
        continue
    f = line.split(",")
    if len(f) != 11 or f[0].strip() == "" or len(f[1].strip()) < 7:
        continue
    month = f[1].strip()[5:7]
    for name, idx in METRICS.items():
        try:
            v = float(f[idx])
        except ValueError:
            continue
        print("%s|%s|%s\tD,%s,%s" % (f[0].strip(), month, name, f[1].strip(), v))