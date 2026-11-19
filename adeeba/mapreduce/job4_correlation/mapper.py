#!/usr/bin/env python
# x = avg_temp_c, y = co2_ppm. Region-wise aur overall (ALL) dono emit.
import sys
for line in sys.stdin:
    line = line.rstrip("\r\n")
    if not line or line.startswith("station_id"):
        continue
    f = line.split(",")
    if len(f) != 11 or f[2].strip() == "":
        continue
    try:
        x, y = float(f[5]), float(f[10])
    except ValueError:
        continue
    print("%s\t%s,%s" % (f[2].strip(), x, y))
    print("ALL\t%s,%s" % (x, y))