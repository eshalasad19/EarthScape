#!/usr/bin/env python
import sys
def num(v):
    try:
        return float(v)
    except ValueError:
        return None
for line in sys.stdin:
    line = line.rstrip("\r\n")
    if not line or line.startswith("station_id"):
        continue
    f = line.split(",")
    if len(f) != 11 or f[2].strip() == "" or len(f[1].strip()) < 4:
        continue
    t, p, c = num(f[5]), num(f[8]), num(f[10])
    # value = sumT,cntT,sumP,cntP,sumC,cntC
    vals = []
    for x in (t, p, c):
        vals += [x if x is not None else 0.0, 1 if x is not None else 0]
    print("%s|%s\t%s" % (f[2].strip(), f[1].strip()[:4], ",".join(str(v) for v in vals)))