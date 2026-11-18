@echo off
rem ===== HDFS snapshot commands (run in CMD as Administrator) =====
rem Hadoop (start-dfs.cmd) must be running.

rem --- Part 1: one-time setup + first manual snapshot ---
hdfs dfsadmin -allowSnapshot /climate
hdfs dfs -createSnapshot /climate snap1
hdfs dfs -ls /climate/.snapshot

rem --- Part 2: timestamped snapshot (use this one for the scheduled task) ---
rem Each snapshot needs a unique name, so the name includes date and time.
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd-HHmm"') do set TS=%%i
hdfs dfs -createSnapshot /climate snap-%TS%
hdfs dfs -ls /climate/.snapshot

rem --- Restore example (copy a deleted file back from a snapshot) ---
rem hdfs dfs -cp /climate/.snapshot/snap1/raw/historical/year=2015/2015_data.csv /climate/raw/historical/year=2015/

rem --- Delete an old snapshot ---
rem hdfs dfs -deleteSnapshot /climate snap1