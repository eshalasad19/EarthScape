# MapReduce Performance Table

Numbers are provided by Adeeba after each job run (runtime from the YARN UI at http://localhost:8088, Applications > Elapsed Time).

| Job | Input size | Rows | Runtime (before combiner) | Runtime (after combiner) | Reducers |
|---|---|---|---|---|---|
| Job 1: Data quality and cleaning | | | | | |
| Job 2: Yearly/region averages | | | | | |
| Job 3: Anomaly detection (Pass A: mean/std) | | | | | |
| Job 3: Anomaly detection (Pass B: flagging) | | | | | |
| Job 4: Correlation (temperature vs CO2) | | | | | |

## Optimization notes (fill after runs)
- Combiner effect:
- Reducer count tested:
- Other observations: