#!/usr/bin/env python
import sys
NUM = [5, 6, 7, 8, 9, 10]   # avg,min,max temp, precip, humidity, co2

def to_float(v):
    try:
        return float(v)
    except ValueError:
        return None

def flush(rows):
    sums = [0.0] * 11
    cnt = [0] * 11
    parsed = [r.split(",") for r in rows]
    for f in parsed:
        for i in NUM:
            x = to_float(f[i].strip())
            if x is not None:
                sums[i] += x
                cnt[i] += 1
    for f in parsed:
        flagged = False
        for i in NUM:
            if to_float(f[i].strip()) is None:
                if cnt[i] > 0:
                    f[i] = "%.2f" % (sums[i] / cnt[i])
                else:
                    f[i] = ""
                    flagged = True
        if flagged:
            sys.stderr.write("reporter:counter:quality,flagged_rows,1\n")
        print(",".join(f))

current, rows = None, []
for line in sys.stdin:
    key, row = line.rstrip("\r\n").split("\t", 1)
    if key != current and current is not None:
        flush(rows)
        rows = []
    current = key
    rows.append(row)
if current is not None:
    flush(rows)