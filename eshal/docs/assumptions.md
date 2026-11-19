# Assumptions and Limitations

These are copied into ReadMe.doc.

1. **Real-time ingestion is simulated.** The stack has no streaming tool, so small batch files are dropped into HDFS at fixed intervals by a script.
2. **Hadoop runs on Windows (single node, pseudo-distributed)** using Hadoop 3.3.5. This needs `winutils.exe` and `hadoop.dll` from a community repository, which are not part of the approved stack list.
3. **Apache server** for Windows is downloaded from Apache Lounge, since apache.org provides no Windows binaries.
4. **Impala** runs only on Linux. Its deployment method is subject to the instructor's decision. (Update this line once decided.)
5. **Python/R libraries** (pandas, pymongo, scikit-learn and similar) are used inside Jupyter/RStudio, subject to the instructor's confirmation. (Update this line once decided.)
6. **HDFS encryption zones are not enabled** because Hadoop KMS is not supported in the Windows setup. Data is protected with HDFS permissions/ACLs and MongoDB authentication.
7. **HDFS authentication is "simple" mode.** Roles are enforced by user name only; there is no Kerberos.
8. **Datasets are public climate datasets** (sources listed in Alizah's documentation); the satellite data is a small set of sample images with metadata.
9. **Tableau** needs Tableau Desktop and an Impala driver to connect to Impala. If this is unavailable, CSV exports from Impala/HDFS are used instead.
10. **Email alerts** (if used) rely on Python's built-in `smtplib`; otherwise alerts are stored in MongoDB and written to a log.
11. **Uptime of 99%** is a design target; the lab runs on a single machine.
12. **Replication factor is 1** in the lab; production would use 3.