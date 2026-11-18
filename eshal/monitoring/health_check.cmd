@echo off
rem health_check.cmd (Eshal) - quick system health report (screenshot it for monitoring).
echo === Java processes (need NameNode, DataNode, ResourceManager, NodeManager) ===
jps
echo.
echo === HDFS report ===
hdfs dfsadmin -report
echo.
echo === HDFS usage per folder ===
hdfs dfs -du -h /climate
echo.
echo === YARN applications (last jobs) ===
yarn application -list -appStates ALL
echo.
echo UIs:  http://localhost:9870 (HDFS)   http://localhost:8088 (YARN)