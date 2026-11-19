#!/usr/bin/env python
import sys
current, acc = None, [0.0] * 6
def avg(s, n):
    return "%.2f" % (s / n) if n > 0 else ""
def out():
    region, year = current.split("|")
    print("%s,%s,%s,%s,%s" % (region, year, avg(acc[0], acc[1]),
                              avg(acc[2], acc[3]), avg(acc[4], acc[5])))
for line in sys.stdin:
    key, val = line.rstrip("\r\n").split("\t")
    if key != current:
        if current is not None:
            out()
        current, acc = key, [0.0] * 6
    for i, v in enumerate(val.split(",")):
        acc[i] += float(v)
if current is not None:
    out()