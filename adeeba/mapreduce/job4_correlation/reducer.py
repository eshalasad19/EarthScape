#!/usr/bin/env python
# Pearson r = (n*Sxy - Sx*Sy) / sqrt((n*Sxx - Sx^2) * (n*Syy - Sy^2))
import sys, math
current, a = None, [0, 0.0, 0.0, 0.0, 0.0, 0.0]   # n,Sx,Sy,Sxx,Syy,Sxy
def out():
    n, sx, sy, sxx, syy, sxy = a
    den = (n * sxx - sx * sx) * (n * syy - sy * sy)
    r = (n * sxy - sx * sy) / math.sqrt(den) if den > 0 else float("nan")
    print("%s,%d,%.4f" % (current, n, r))
for line in sys.stdin:
    key, val = line.rstrip("\r\n").split("\t")
    x, y = [float(t) for t in val.split(",")]
    if key != current:
        if current is not None:
            out()
        current, a = key, [0, 0.0, 0.0, 0.0, 0.0, 0.0]
    a[0] += 1; a[1] += x; a[2] += y
    a[3] += x * x; a[4] += y * y; a[5] += x * y
if current is not None:
    out()