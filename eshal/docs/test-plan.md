# Test Plan

Test data: synthetic sample data from `alizah/scripts/generate_sample_data.py` (development) and the real standardized dataset (final run).
Fill the **Result** and **Evidence** columns while testing (Pass/Fail, screenshot name).

| ID | Module | Test | Steps | Expected result | Result | Evidence |
|---|---|---|---|---|---|---|
| T01 | Infrastructure | Hadoop services start | `start-dfs.cmd`, `start-yarn.cmd`, `jps` | NameNode, DataNode, ResourceManager, NodeManager listed | | |
| T02 | Infrastructure | HDFS folders exist | `integration\hdfs_setup.cmd` | `/climate/raw/...`, `processed`, `ml_output`, `backup` listed | | |
| T03 | Infrastructure | MapReduce works | wordcount test (guide Step 8) | Output `climate 1`, `hadoop 1`, `hello 2` | | |
| T04 | Security | Analyst cannot write to HDFS raw | `security\hdfs_roles_setup.cmd` | Permission denied for analyst write | | |
| T05 | Security | Analyst can read HDFS raw | same script | Listing is shown | | |
| T06 | Security | MongoDB analyst role | `mongodb\05_auth_tests.js` as `es_analyst` | Read ALLOWED, insert sensor_readings DENIED, insert feedback ALLOWED | | |
| T07 | Security | MongoDB admin role | `05_auth_tests.js` as `es_admin` | Everything ALLOWED | | |
| T08 | Backup | HDFS snapshot | `backup\snapshot-daily.cmd` | New snapshot in `/climate/.snapshot` | | |
| T09 | Backup | Snapshot restore | delete a test file, copy it back from snapshot | File restored | | |
| T10 | Backup | MongoDB backup | `backup\mongo_backup.cmd es_admin` | Backup folder created | | |
| T11 | Ingestion | Data generation / standardization | `generate_sample_data.py` or `standardize_csv.py` | Files in the shared schema (11 columns) | | |
| T12 | Ingestion | Historical load | `load_historical.py --input ...` | `year=YYYY` folders in HDFS, `hdfs dfs -du -h` shows sizes | | |
| T13 | Ingestion | Simulated real-time | `streaming_simulator.py --max-batches 3` | 3 batch files in `/climate/raw/streaming`, log lines written | | |
| T14 | Ingestion | MongoDB readings | run simulator with `--mongo` | `sensor_readings` count increases | | |
| T15 | MongoDB | Collections and indexes | `01_setup_collections.js` | 5 collections exist | | |
| T16 | MongoDB | Feedback system | `03_feedback.js`, query open issues | 5 sample feedback documents, query returns open ones | | |
| T17 | MapReduce | Job 1a quality report | `run_all_jobs.cmd` | `quality_report` shows missing % per column | | |
| T18 | MapReduce | Job 1b cleaning | same | `clean` has no blanks where a station-month mean exists; counter `ImputedValues` > 0 | | |
| T19 | MapReduce | Job 2 yearly averages | same | One row per region+year | | |
| T20 | MapReduce | Job 3 anomalies | same | `anomalies` rows with |zscore| >= 2.5 | | |
| T21 | MapReduce | Job 4 correlation | same | `overall` and one row per region, r between -1 and 1 | | |
| T22 | MapReduce | Batch + streaming together | new streaming file, rerun jobs | New rows included in the outputs | | |
| T23 | Impala | Tables and queries | `01_create_tables.sql`, `02_analyst_queries.sql` | 10 queries return results | | |
| T24 | ML | Trend prediction | `01_trend_prediction.py` | `predictions.csv` for the next 10 years, metrics in `model_log.csv` | | |
| T25 | ML | Anomaly comparison | `02_anomaly_detection.py` | `anomaly_comparison.txt` written | | |
| T26 | ML | Correlation in RStudio | `03_correlation.R` | `correlation_matrix.csv` and PNG created | | |
| T27 | ML | Retraining | `04_retrain.py --pull --upload` | New rows in `model_log.csv`, files in `/climate/ml_output` | | |
| T28 | Alerts | Alert generation | `alert_generator.py --input ...` | `alerts.csv`, log line, Critical/Warning counts | | |
| T29 | Alerts | Alerts in MongoDB | `--mongo` | `alerts` collection filled; rerun does not create duplicates | | |
| T30 | Tableau | Dashboards | open the 4 dashboards | Filters work, data matches Impala/CSV | | |
| T31 | Apache | Documentation site | open `http://localhost` | Documentation page loads | | |
| T32 | Integration | End to end | `integration\run_end_to_end.cmd` | All 7 steps finish, no failure message | | |

## Defect log
| ID | Date | Found by | Test | Description | Fixed by | Status |
|---|---|---|---|---|---|---|
| | | | | | | |