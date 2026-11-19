# Installation Instructions

Platform: Windows 10/11 (64-bit), 16 GB RAM recommended. Open PowerShell/CMD as **Administrator**.

## 1. Common tools (everyone)
```
winget install --id Git.Git -e
winget install --id Microsoft.VisualStudioCode -e
winget install --id Anaconda.Anaconda3 -e
```
Close and reopen the terminal, then check: `git --version`, `code --version`, `conda --version`, `python --version` (Python 3.10 or newer is needed).
Clone the repository and work only in your own folder (see `README.md`).

## 2. MongoDB (Alizah; others only for Compass)
```
winget install --id MongoDB.Server -e
winget install --id MongoDB.Compass.Full -e
winget install --id MongoDB.Shell -e
```
Check: `mongod --version`, `mongosh --version`. Then follow `alizah\mongodb\README.md` (collections, roles, authentication).
`mongodump` (for backups) comes with MongoDB Database Tools; install it if `mongodump --version` is not found.

## 3. R and RStudio (Wania)
```
winget install --id RProject.R -e
winget install --id Posit.RStudio -e
```
## 4. Hadoop, HDFS, YARN and Apache server (Eshal, Adeeba)
Follow `05_Hadoop_Apache_Windows_Setup.md` (Part A for Hadoop, Part B for Apache). Check with `jps` and the two web UIs.
Supporting downloads (not part of the stack list): Temurin JDK 8, winutils/hadoop.dll, Apache Lounge build of httpd.

## 5. Impala
Impala runs on Linux only. The installation method depends on the instructor's decision (see `assumptions.md`). Until then the SQL files in `adeeba\impala\` are prepared but not executed.

## 6. Tableau (Wania)
Install Tableau Desktop (student license or trial) from tableau.com. To connect to Impala, the Impala driver is needed; otherwise use CSV exports.

## 7. Python libraries
The code uses only the Python standard library. Optional (only if the instructor allows): `pip install pandas scikit-learn pymongo` for `wania\notebooks\02b_isolation_forest_optional.py`.

## 8. First run (check everything works)
1. Without Hadoop: `cd adeeba\mapreduce` then `python run_all_local.py --input ..\sample-data`
2. With Hadoop running: `integration\run_end_to_end.cmd` (from the `eshal` folder)
3. Open the Apache page `http://localhost`, the HDFS UI `http://localhost:9870` and the YARN UI `http://localhost:8088`.

## 9. Start and stop the system
Start: `start-dfs.cmd`, `start-yarn.cmd`, MongoDB service (`net start MongoDB`), Apache (`httpd.exe -k start`).
Stop: `stop-yarn.cmd`, `stop-dfs.cmd`, `net stop MongoDB`, `httpd.exe -k stop`.