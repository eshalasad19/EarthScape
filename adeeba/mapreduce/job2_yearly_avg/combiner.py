#!/usr/bin/env python
import sys
current, acc = None, [0.0] * 6
def out():
    print("%s\t%s" % (current, ",".join(str(v) for v in acc)))
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