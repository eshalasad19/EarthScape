# EarthScape Climate Agency: Big Data eProject (Draft ReadMe)

> Draft. Convert to ReadMe.doc (Word) for the final submission and fill the bracketed fields.

**Project:** Big Data climate analysis system for EarthScape Climate Agency
**Batch / Group:** [batch] / [group]
**Team:** Eshal (leader), Alizah, Adeeba, Wania

## 1. What the system does
Stores historical and (simulated) real-time climate data in HDFS, processes it with MapReduce (data quality and cleaning, yearly patterns, anomaly detection, correlation), serves it to analysts through Impala, predicts trends and detects anomalies with ML (Jupyter/RStudio), raises alerts, and shows interactive Tableau dashboards. MongoDB holds readings, satellite metadata, users, feedback and alerts. Access is role based (Admin / Analyst).

## 2. Technology stack
Jupyter Anaconda Notebook 3, RStudio, VS Code, MongoDB Compass + Shell, Hadoop + HDFS + Apache server, Tableau, Impala.

## 3. Folder structure
| Folder | Content |
|---|---|
| `eshal/` | Hadoop config, Apache page, security, backup, monitoring, integration scripts, documentation |
| `alizah/` | Data generation/standardization, HDFS loading, streaming simulator, MongoDB scripts |
| `adeeba/` | MapReduce jobs, local test runner, Impala SQL, performance results |
| `wania/` | ML notebooks, R script, alert generator, Tableau plan |

## 4. How to run
See `docs/installation-instructions.md` for installation. Quick path:
1. Start Hadoop, MongoDB, Apache.
2. Create HDFS folders: `eshal\integration\hdfs_setup.cmd`
3. Prepare data: `alizah\scripts\standardize_csv.py` (real data) or `generate_sample_data.py` (test data)
4. Load data: `alizah\scripts\load_historical.py`, then `streaming_simulator.py`
5. Process: `adeeba\mapreduce\run_all_jobs.cmd`
6. Query: `adeeba\impala\01_create_tables.sql`, `02_analyst_queries.sql`
7. ML: `wania\notebooks\04_retrain.py --pull --upload`; R: `wania\rstudio\03_correlation.R`
8. Alerts: `wania\alerts\run_alerts.cmd`
9. Dashboards: Tableau (see `wania\tableau\dashboard_plan.md`)
Everything in one go: `eshal\integration\run_end_to_end.cmd`

## 5. Login credentials
Provided in the separate credentials file inside the submission zip (not in the repository).
| System | User | Role |
|---|---|---|
| MongoDB | es_admin | Admin |
| MongoDB | es_analyst | Analyst |
| HDFS | (user that runs Hadoop) / analyst | Admin / Analyst |
| Tableau | [license user] | |

## 6. Assumptions and limitations
See `docs/assumptions.md` (copy the final list here).

## 7. Documentation index
Problem definition, architecture, DFD, scalability, uptime plan, test plan, installation instructions, access control matrix, backup plan, monitoring notes, user documentation, developer documentation.