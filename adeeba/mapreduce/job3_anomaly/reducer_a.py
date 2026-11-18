#!/usr/bin/env python
# Pass A reducer: n, mean, std (population) per station|month|metric
import sys, math
current, n, s, ss = None, 0, 0.0, 0.0
def out():
    mean = s / n
    var = max(ss / n - mean * mean, 0.0)
    print("%s\t%d,%.4f,%.4f" % (current, n, mean, math.sqrt(var)))
for line in sys.stdin:
    key, val = line.rstrip("\r\n").split("\t")
    v = float(val)
    if key != current:
        if current is not None:
            out()
        current, n, s, ss = key, 0, 0.0, 0.0
    n += 1; s += v; ss += v * v
if current is not None:
    out()