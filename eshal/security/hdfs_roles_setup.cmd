@echo off
rem hdfs_roles_setup.cmd (Eshal) - applies the Admin/Analyst permission model and tests it.
rem Run as the user who started Hadoop (= HDFS superuser = Admin). CMD as Administrator.
rem See access-control-matrix.md for the model.

echo === 1. permissions: everyone can read, only the owner can write ===
hdfs dfs -chmod -R 755 /climate
hdfs dfs -chmod 700 /climate/admin_only

echo === 2. ACL: analyst may read processed data ===
hdfs dfs -setfacl -m user:analyst:r-x /climate/processed
hdfs dfs -getfacl /climate/processed

echo === 3. test as ANALYST (screenshot this part) ===
set HADOOP_USER_NAME=analyst
echo --- read raw (should work):
hdfs dfs -ls /climate/raw
echo --- write to raw (should say Permission denied):
hdfs dfs -mkdir /climate/raw/hacked
echo --- read admin_only (should say Permission denied):
hdfs dfs -ls /climate/admin_only
echo --- write to processed (should say Permission denied):
hdfs dfs -mkdir /climate/processed/test
set HADOOP_USER_NAME=

echo === done. Back to Admin in this window ===