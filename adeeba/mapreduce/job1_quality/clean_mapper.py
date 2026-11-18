#!/usr/bin/env python
import sys
for line in sys.stdin:
    line = line.rstrip("\r\n")
    if not line or line.startswith("station_id"):
        continue
    f = line.split(",")
    if len(f) != 11 or f[0].strip() == "" or len(f[1].strip()) < 7:
        sys.stderr.write("reporter:counter:quality,bad_rows,1\n")
        continue
    # key = station + month (YYYY-MM)
    print("%s|%s\t%s" % (f[0].strip(), f[1].strip()[:7], line))