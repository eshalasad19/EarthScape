# HDFS Permissions and Role Test

Run in CMD as the user who started Hadoop (HDFS superuser = Admin).

## 1. Set permissions
```
hdfs dfs -chmod -R 755 /climate
hdfs dfs -mkdir -p /climate/admin_only
hdfs dfs -chmod 700 /climate/admin_only
hdfs dfs -ls /climate
```
755 means: owner can read/write, everyone else can only read.
700 means: only the owner can access.

## 2. Test as Analyst
Simple authentication lets us act as another user with an environment variable.
```
set HADOOP_USER_NAME=analyst
hdfs dfs -ls /climate/raw
hdfs dfs -mkdir /climate/raw/hacked
hdfs dfs -ls /climate/admin_only
```
Expected result:
- `-ls /climate/raw` works (read allowed)
- `-mkdir /climate/raw/hacked` fails with **Permission denied** (write blocked)
- `-ls /climate/admin_only` fails with **Permission denied**

Open a new CMD window (or run `set HADOOP_USER_NAME=`) to go back to Admin.

## 3. ACL example (read-only access for analyst on processed data)
Run as Admin:
```
hdfs dfs -setfacl -m user:analyst:r-x /climate/processed
hdfs dfs -getfacl /climate/processed
```
Expected: the output lists `user:analyst:r-x`.

## 4. Check the analyst cannot write to processed
```
set HADOOP_USER_NAME=analyst
hdfs dfs -mkdir /climate/processed/test
```
Expected: **Permission denied**.

## Screenshots
Screenshot yahan lagegi (baad mein):
- Permission denied on write (analyst)
- Successful read (analyst)
- `getfacl` output