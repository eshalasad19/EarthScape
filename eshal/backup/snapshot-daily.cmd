@echo off
rem snapshot-daily.cmd (Eshal) - one timestamped HDFS snapshot. Used by Task Scheduler.
rem One-time setup first (run once):  hdfs dfsadmin -allowSnapshot /climate
rem Copy this file to C:\earthscape-backups\snapshot-daily.cmd (see backup-plan.md).
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd-HHmm"') do set TS=%%i
hdfs dfs -createSnapshot /climate snap-%TS%
echo %date% %time% snapshot snap-%TS% result=%errorlevel% >> C:\earthscape-backups\snapshot-log.txt
rem keep the 7 newest snapshots, delete older ones
powershell -NoProfile -Command "$s = (hdfs dfs -ls /climate/.snapshot | Select-String 'snap-' | ForEach-Object { ($_ -split '/')[-1].Trim() } | Sort-Object); if ($s.Count -gt 7) { $s | Select-Object -First ($s.Count - 7) | ForEach-Object { hdfs dfs -deleteSnapshot /climate $_ } }"