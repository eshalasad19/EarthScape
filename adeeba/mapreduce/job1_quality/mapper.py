#!/usr/bin/env python
import sys
COLS = ["station_id","date","region","latitude","longitude","avg_temp_c",
        "min_temp_c","max_temp_c","precip_mm","humidity_pct","co2_ppm"]
for line in sys.stdin:
    line = line.rstrip("\r\n")
    if not line or line.startswith("station_id"):
        continue
    f = line.split(",")
    if len(f) != 11:
        sys.stderr.write("reporter:counter:quality,bad_rows,1\n")
        continue
    print("TOTAL_ROWS\t1")
    for name, val in zip(COLS, f):
        if val.strip() == "":
            print("%s\t1" % name)