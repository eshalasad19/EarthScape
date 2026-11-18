#!/usr/bin/env python
"""Local test runner: Hadoop ke bina saari jobs chalata hai (map -> sort -> reduce).
Sirf standard library.

  python run_local.py                      -> sample data par check, expected files se compare
  python run_local.py --input BIG.csv      -> bade data par chalao, rows aur runtime table dikhao
"""
import argparse, os, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLE = HERE.parent / "sample-data"
J1, J2, J3, J4 = (HERE / "job1_quality", HERE / "job2_yearly_avg",
                  HERE / "job3_anomaly", HERE / "job4_correlation")

counters = {}

def run(script, cwd, data):
    p = subprocess.run([sys.executable, script], cwd=str(cwd), input=data,
                       capture_output=True, text=True, encoding="utf-8")
    if p.returncode != 0:
        sys.exit("ERROR in %s:\n%s" % (script, p.stderr))
    for line in p.stderr.splitlines():
        if line.startswith("reporter:counter:"):
            key = line.split(":", 2)[2].rsplit(",", 1)[0]
            counters[key] = counters.get(key, 0) + 1
    return p.stdout

def shuffle(text):
    lines = [l for l in text.splitlines() if l]
    lines.sort()
    return "\n".join(lines) + ("\n" if lines else "")

def mapreduce(cwd, mapper, reducer, data, combiner=None):
    m = shuffle(run(mapper, cwd, data))
    if combiner:
        m = shuffle(run(combiner, cwd, m))
    return run(reducer, cwd, m)

def lines(t):
    return [l.strip() for l in t.splitlines() if l.strip()]

def timed(label, table, fn, rows_in):
    t0 = time.time()
    out = fn()
    table.append((label, rows_in, len(lines(out)), time.time() - t0))
    return out

def pipeline(clean_input, anomaly_input, table, with_combiner=True):
    q = timed("job1_quality", table, lambda: mapreduce(J1, "mapper.py", "reducer.py", clean_input),
              len(lines(clean_input)))
    clean = timed("job1_clean", table, lambda: mapreduce(J1, "clean_mapper.py", "clean_reducer.py", clean_input),
                  len(lines(clean_input)))
    j2 = timed("job2_yearly_avg" + (" (combiner)" if with_combiner else ""), table,
               lambda: mapreduce(J2, "mapper.py", "reducer.py", clean,
                                 "combiner.py" if with_combiner else None), len(lines(clean)))
    stats = timed("job3_pass_A", table, lambda: mapreduce(J3, "mapper_a.py", "reducer_a.py", anomaly_input),
                  len(lines(anomaly_input)))
    j3 = timed("job3_pass_B", table, lambda: mapreduce(J3, "mapper_b.py", "reducer_b.py",
                                                       anomaly_input.rstrip("\n") + "\n" + stats),
               len(lines(anomaly_input)) + len(lines(stats)))
    j4 = timed("job4_correlation", table, lambda: mapreduce(J4, "mapper.py", "reducer.py", clean),
               len(lines(clean)))
    return q, clean, j2, j3, j4

def check(name, got, path):
    if not path.exists():
        print("SKIP  %-18s (%s nahi mili)" % (name, path.name))
        return True
    ok = sorted(lines(got)) == sorted(lines(path.read_text(encoding="utf-8", errors="replace")))
    print("%s  %-18s vs %s" % ("PASS" if ok else "FAIL", name, path.name))
    return ok

def print_table(table):
    print("\n%-28s %10s %10s %10s" % ("job", "rows_in", "rows_out", "seconds"))
    for label, rin, rout, sec in table:
        print("%-28s %10d %10d %10.2f" % (label, rin, rout, sec))
    if counters:
        print("\nCounters:", counters)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", help="bada CSV (repo ke bahar rakho)")
    ap.add_argument("--out", help="output folder (default: earthscape-data/local_out)")
    a = ap.parse_args()
    table = []
    if a.input:
        data = Path(a.input).read_text(encoding="utf-8")
        out = Path(a.out) if a.out else (Path("C:/earthscape-data/local_out") if os.name == "nt"
                                         else Path.home() / "earthscape-data" / "local_out")
        out.mkdir(parents=True, exist_ok=True)
        q, clean, j2, j3, j4 = pipeline(data, data, table, True)
        counters.clear()
        timed("job2_yearly_avg (NO combiner)", table,
              lambda: mapreduce(J2, "mapper.py", "reducer.py", clean), len(lines(clean)))
        for name, text in (("quality_report.txt", q), ("clean.csv", clean), ("yearly_region_avg.csv", j2),
                           ("anomalies.csv", j3), ("correlation.csv", j4)):
            (out / name).write_text(text, encoding="utf-8")
        print("Outputs: %s" % out)
        print_table(table)
        return
    sample = (SAMPLE / "sample.csv").read_text(encoding="utf-8")
    anomaly = (SAMPLE / "sample_anomaly.csv").read_text(encoding="utf-8")
    q, clean, j2, _, j4 = pipeline(sample, anomaly, table)
    stats = mapreduce(J3, "mapper_a.py", "reducer_a.py", anomaly)
    j3 = mapreduce(J3, "mapper_b.py", "reducer_b.py", anomaly.rstrip("\n") + "\n" + stats)
    results = [
        check("job1_quality", q, SAMPLE / "expected_job1_quality.txt"),
        check("job1_clean", clean, SAMPLE / "clean_out.csv"),
        check("job2_yearly_avg", j2, SAMPLE / "expected_job2.csv"),
        check("job3_anomaly", j3, SAMPLE / "expected_job3.csv"),
        check("job4_correlation", j4, SAMPLE / "expected_job4.csv"),
    ]
    print("\nALL PASS" if all(results) else "\nKUCH FAIL HUA")

if __name__ == "__main__":
    main()
    