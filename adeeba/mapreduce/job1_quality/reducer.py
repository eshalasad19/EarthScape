#!/usr/bin/env python
import sys
current, total = None, 0
for line in sys.stdin:
    key, val = line.rstrip("\r\n").split("\t")
    if key != current:
        if current is not None:
            print("%s\t%d" % (current, total))
        current, total = key, 0
    total += int(val)
if current is not None:
    print("%s\t%d" % (current, total))