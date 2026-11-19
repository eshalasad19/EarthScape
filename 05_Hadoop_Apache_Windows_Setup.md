# Hadoop + HDFS + Apache Server: Windows Setup Guide

**Kaun karega:** pehle Eshal aur Adeeba (Adeeba ko jobs chalani hain). Phir baqi members agar apne laptop par HDFS test karna chahein.
**Impala is guide mein nahi hai.** Wo Linux-only hai aur teacher ke jawab ke baad alag se aayega.
**Hadoop version:** 3.3.5 (isliye ke Windows ke community binaries is version ke liye milte hain). Neeche har command isi par based hai.

> Sab commands **CMD (Run as Administrator)** mein chalane hain, jab tak koi aur na likha ho.
> Har step ke baad jo "Check" likha hai wo zaroor karo. Agle step par tabhi jao jab check pass ho.

---

## PART A: Hadoop + HDFS + YARN (single node)

### Step 1: Java 8 install karo
```
winget install --id EclipseAdoptium.Temurin.8.JDK -e
```
Hadoop Windows par us path se masla karta hai jis mein **space** ho (`Program Files`). Is liye ek space-free shortcut banate hain:
```
dir "C:\Program Files\Eclipse Adoptium"
```
Jo folder dikhe (jaise `jdk-8.0.xxx-hotspot`) uska naam copy karo, aur ye chalao (naam apne folder se badal do):
```
mklink /J C:\Java8 "C:\Program Files\Eclipse Adoptium\jdk-8.0.xxx-hotspot"
```
**Check:** `dir C:\Java8\bin\java.exe` file dikhni chahiye.

### Step 2: Hadoop download aur extract
```
mkdir C:\hadoop
curl -L -o C:\hadoop-3.3.5.tar.gz https://archive.apache.org/dist/hadoop/common/hadoop-3.3.5/hadoop-3.3.5.tar.gz
tar -xzf C:\hadoop-3.3.5.tar.gz -C C:\hadoop --strip-components=1
```
Agar "Cannot create symlink" jaisi warnings aayen to ignore karo (wo Linux ki native files hain, kaam ki nahi).
**Check:** `dir C:\hadoop\bin` mein `hadoop.cmd` aur `hdfs.cmd` honi chahiye.

### Step 3: Windows binaries (winutils)
Hadoop ko Windows par chalane ke liye `winutils.exe` aur `hadoop.dll` chahiye. Ye Hadoop khud nahi deta, community repo se aate hain. Ye project ki list se bahar ek **zaroori supporting file** hai. ReadMe.doc ke "Assumptions" mein likhna.
```
git clone --depth 1 https://github.com/cdarlint/winutils C:\winutils
dir C:\winutils
```
Dekho ke `hadoop-3.3.5` naam ka folder hai. Agar nahi, to repo mein jo sab se qareeb 3.3.x folder ho wo use karo (aur Step 2 ka Hadoop version bhi wohi rakho). Phir:
```
xcopy /Y /E C:\winutils\hadoop-3.3.5\bin\* C:\hadoop\bin\
copy /Y C:\winutils\hadoop-3.3.5\bin\hadoop.dll C:\Windows\System32\
```
**Check:** `dir C:\hadoop\bin\winutils.exe` dikhni chahiye.

### Step 4: Environment variables
**PowerShell (Run as Administrator)** mein ye chalao:
```
[Environment]::SetEnvironmentVariable("JAVA_HOME","C:\Java8","Machine")
[Environment]::SetEnvironmentVariable("HADOOP_HOME","C:\hadoop","Machine")
$p=[Environment]::GetEnvironmentVariable("Path","Machine")
[Environment]::SetEnvironmentVariable("Path",$p+";C:\Java8\bin;C:\hadoop\bin;C:\hadoop\sbin","Machine")
```
Ab **sab CMD/PowerShell windows band karo** aur naya CMD (Administrator) kholo.
**Check:**
```
java -version
hadoop version
```
`java version "1.8..."` aur `Hadoop 3.3.5` dikhna chahiye.

### Step 5: Config files
Folder: `C:\hadoop\etc\hadoop\`. Ye 4 files **poori replace** karo (VS Code mein kholo, sab select karke paste). Pehle data folders banao:
```
mkdir C:\hadoop-data\namenode
mkdir C:\hadoop-data\datanode
```

**5a. `core-site.xml`**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://localhost:9000</value>
  </property>
</configuration>
```

**5b. `hdfs-site.xml`**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>1</value>
  </property>
  <property>
    <name>dfs.namenode.name.dir</name>
    <value>file:///C:/hadoop-data/namenode</value>
  </property>
  <property>
    <name>dfs.datanode.data.dir</name>
    <value>file:///C:/hadoop-data/datanode</value>
  </property>
  <property>
    <name>dfs.permissions.enabled</name>
    <value>true</value>
  </property>
  <property>
    <name>dfs.namenode.acls.enabled</name>
    <value>true</value>
  </property>
</configuration>
```

**5c. `mapred-site.xml`**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>
  <property>
    <name>mapreduce.application.classpath</name>
    <value>%HADOOP_HOME%/share/hadoop/mapreduce/*,%HADOOP_HOME%/share/hadoop/mapreduce/lib/*</value>
  </property>
  <property>
    <name>yarn.app.mapreduce.am.env</name>
    <value>HADOOP_MAPRED_HOME=C:/hadoop</value>
  </property>
  <property>
    <name>mapreduce.map.env</name>
    <value>HADOOP_MAPRED_HOME=C:/hadoop</value>
  </property>
  <property>
    <name>mapreduce.reduce.env</name>
    <value>HADOOP_MAPRED_HOME=C:/hadoop</value>
  </property>
</configuration>
```

**5d. `yarn-site.xml`**
```xml
<?xml version="1.0"?>
<configuration>
  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
  </property>
  <property>
    <name>yarn.nodemanager.aux-services.mapreduce_shuffle.class</name>
    <value>org.apache.hadoop.mapred.ShuffleHandler</value>
  </property>
  <property>
    <name>yarn.nodemanager.resource.memory-mb</name>
    <value>4096</value>
  </property>
  <property>
    <name>yarn.scheduler.maximum-allocation-mb</name>
    <value>4096</value>
  </property>
</configuration>
```

**5e. `hadoop-env.cmd`** (find and replace)
- **Find:** `set JAVA_HOME=%JAVA_HOME%`
- **Replace with:** `set JAVA_HOME=C:\Java8`

Is file ki sab config copies apne repo ke `eshal/hadoop-config/` mein bhi rakh do.

### Step 6: HDFS format aur start
**Format sirf EK baar karna hai.** Dobara format karoge to DataNode start nahi hoga (neeche troubleshooting dekho).
```
hdfs namenode -format
start-dfs.cmd
start-yarn.cmd
```
Do-teen nayi windows khulengi (NameNode, DataNode, ResourceManager, NodeManager). Unhe band mat karo.
**Check:**
```
jps
```
Ye 4 chizen dikhni chahiye: `NameNode`, `DataNode`, `ResourceManager`, `NodeManager`.
Browser mein: `http://localhost:9870` (HDFS) aur `http://localhost:8088` (YARN). Dono ke screenshots lo (monitoring task ke liye).

Band karne ke liye: `stop-yarn.cmd` aur `stop-dfs.cmd`.

### Step 7: HDFS folder structure
```
hdfs dfs -mkdir -p /climate/raw/historical
hdfs dfs -mkdir -p /climate/raw/streaming
hdfs dfs -mkdir -p /climate/raw/satellite
hdfs dfs -mkdir -p /climate/processed
hdfs dfs -mkdir -p /climate/ml_output
hdfs dfs -mkdir -p /climate/backup
hdfs dfs -ls -R /climate
```

### Step 8: Test (MapReduce chal raha hai ya nahi)
Ek chhoti test file aur wordcount:
```
echo hello hadoop hello climate> C:\test.txt
hdfs dfs -mkdir -p /test/in
hdfs dfs -put C:\test.txt /test/in/
hadoop jar C:\hadoop\share\hadoop\mapreduce\hadoop-mapreduce-examples-3.3.5.jar wordcount /test/in /test/out
hdfs dfs -cat /test/out/part-r-00000
```
**Check:** `climate 1`, `hadoop 1`, `hello 2` aana chahiye. Ye chal gaya to YARN aur MapReduce theek hain.

### Step 9: Hadoop Streaming (Adeeba ke Python jobs ke liye)
Python system PATH mein hona chahiye, kyunke YARN containers apna environment use karte hain. Check: `where python`. Agar Anaconda ka Python PATH mein nahi, to command mein `python` ki jagah python.exe ka poora path likho.
Test (apne `mapper.py` aur `reducer.py` wale folder mein):
```
hadoop jar C:\hadoop\share\hadoop\tools\lib\hadoop-streaming-3.3.5.jar -files mapper.py,reducer.py -mapper "python mapper.py" -reducer "python reducer.py" -input /test/in -output /test/streaming_out
```
Output dobara chalane se pehle purana folder delete karna parta hai: `hdfs dfs -rm -r /test/streaming_out`.

### Step 10: Roles/permissions test (Eshal ka Task 4)
Windows par Linux jaisa user/group system nahi hota, is liye simple tareeqa:
```
hdfs dfs -chmod -R 755 /climate
hdfs dfs -mkdir -p /climate/admin_only
hdfs dfs -chmod 700 /climate/admin_only
```
Analyst ban kar test karo (current CMD window mein):
```
set HADOOP_USER_NAME=analyst
hdfs dfs -ls /climate/raw
hdfs dfs -mkdir /climate/raw/hacked
```
Pehla command chalna chahiye (read allowed), doosra **"Permission denied"** dega. Ye aapka test evidence hai, screenshot lo.
ACL ka misaal (analyst ko processed folder par sirf read):
```
set HADOOP_USER_NAME=%USERNAME%
hdfs dfs -setfacl -m user:analyst:r-x /climate/processed
hdfs dfs -getfacl /climate/processed
```
(Pehli line wapas apne user par aane ke liye hai. Ya naya CMD kholo.)
**Note:** ye "simple authentication" mode hai, asli security nahi. Documentation mein ye limitation likhna.

### Step 11: Snapshot backup (Eshal ka Task 6)
```
hdfs dfsadmin -allowSnapshot /climate
hdfs dfs -createSnapshot /climate snap1
hdfs dfs -ls /climate/.snapshot
```

### Troubleshooting
| Masla | Hal |
|---|---|
| `Could not locate executable ... winutils.exe` | `C:\hadoop\bin\winutils.exe` check karo, aur `HADOOP_HOME` ke baad naya CMD kholo |
| `JAVA_HOME is incorrectly set` | `hadoop-env.cmd` mein `set JAVA_HOME=C:\Java8` check karo, aur path mein space na ho |
| DataNode start nahi hota (clusterID mismatch) | Sab band karo (`stop-dfs.cmd`), `C:\hadoop-data\datanode` aur `namenode` ke andar ka sab kuch delete karo, dobara `hdfs namenode -format` (HDFS ka data khali ho jayega) |
| YARN job mein symlink/permission error | CMD ko **Administrator** ke taur par kholo (YARN ko symlink banane ke liye ye chahiye) |
| `MRAppMaster` class nahi mili | `mapred-site.xml` ke classpath aur env wali properties dobara check karo |
| Port already in use | `netstat -ano | findstr 9870` se dekho kaun use kar raha hai |
| Hadoop bilkul nahi chal raha | Screenshot aur poora error mujhe bhejo |

### Encryption (HDFS encryption zone) par note
Is ke liye Hadoop KMS chahiye, jo Windows par practically setup karna bohat mushkil hai. Aap pehle 30 minute koshish karo, na chale to documentation mein likho: *"HDFS encryption zones need KMS which is not supported in our Windows setup; data is protected by HDFS permissions/ACLs and MongoDB authentication"*, aur ReadMe assumption mein bhi.

---

## PART B: Apache Server (Windows)

Apache.org Windows ke binaries khud nahi deta. Windows build **Apache Lounge** (apachelounge.com/download) se milta hai (ye bhi ek supporting download hai, assumption mein likhna).

### Step 1: Install
1. apachelounge.com/download se **Apache 2.4.x Win64** zip download karo. Saath wala **Visual C++ Redistributable (VS17 / latest)** bhi install karo (page par link hota hai).
2. Zip ke andar `Apache24` folder ko `C:\Apache24` mein extract karo.

### Step 2: Chalao aur check karo
```
C:\Apache24\bin\httpd.exe -t
C:\Apache24\bin\httpd.exe -k install
C:\Apache24\bin\httpd.exe -k start
```
Browser mein `http://localhost` kholo. "It works!" dikhna chahiye.
Agar port 80 busy ho to `C:\Apache24\conf\httpd.conf` mein:
- **Find:** `Listen 80`
- **Replace with:** `Listen 8080`

Aur `ServerName` line:
- **Find:** `#ServerName www.example.com:80`
- **Replace with:** `ServerName localhost`

Config badalne ke baad: `C:\Apache24\bin\httpd.exe -k restart`.

### Step 3: Documentation page host karo
`C:\Apache24\htdocs\index.html` ko replace karo (light background, saaf design):
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>EarthScape Climate Agency - Documentation</title>
<style>
  body { font-family: Arial, sans-serif; background: #f7f7f8; color: #222; margin: 0; }
  main { max-width: 800px; margin: 40px auto; background: #fff; padding: 32px; border-radius: 8px; }
  h1 { margin-top: 0; }
  a { color: #1a5fb4; }
</style>
</head>
<body>
<main>
  <h1>EarthScape Climate Agency</h1>
  <p>Big Data climate analysis system: Hadoop, MapReduce, Impala, ML and Tableau.</p>
  <h2>Documentation</h2>
  <ul>
    <li><a href="user-guide.html">User Guide</a></li>
    <li><a href="faq.html">FAQ</a></li>
    <li><a href="tutorials.html">Tutorials</a></li>
    <li><a href="demo.mp4">Demo Video</a></li>
  </ul>
</main>
</body>
</html>
```
`user-guide.html`, `faq.html`, `tutorials.html` jab sab ka kaam ready ho tab banenge. Is page ki copy `eshal/apache/` mein repo mein rakho.

### Step 4: Load balancing ka demo (optional, sirf documentation ke liye)
`httpd.conf` mein in modules ke aage se `#` hata do (uncomment karo):
```
LoadModule proxy_module modules/mod_proxy.so
LoadModule proxy_http_module modules/mod_proxy_http.so
LoadModule proxy_balancer_module modules/mod_proxy_balancer.so
LoadModule slotmem_shm_module modules/mod_slotmem_shm.so
LoadModule lbmethod_byrequests_module modules/mod_lbmethod_byrequests.so
```
Aur file ke aakhir mein ye jod do (do backend servers ke darmiyan requests baantne ka concept dikhata hai, jaise HDFS/Impala nodes ke samne laga hota):
```
<Proxy "balancer://climatecluster">
    BalancerMember "http://localhost:8081"
    BalancerMember "http://localhost:8082"
    ProxySet lbmethod=byrequests
</Proxy>
ProxyPass "/app" "balancer://climatecluster"
ProxyPassReverse "/app" "balancer://climatecluster"
```
Ye sirf concept ka demo hai. Agar 8081/8082 par kuch chal nahi raha to `/app` error dega, isliye jab tak backends nahi hain is block ko comment rakho. Documentation mein sirf config aur uska maqsad likhna kaafi hai.

### Repo mein kya rakhna hai (`eshal/` folder)
- `hadoop-config/`: 4 XML files + `hadoop-env.cmd` ki copy
- `apache/`: `index.html` aur `httpd.conf` mein jo badla uski copy
- `security/`: Step 10 ke screenshots
- `monitoring/`: `localhost:9870` aur `localhost:8088` ke screenshots
- `backup/`: snapshot commands

---

## Aakhri note
Ye guide Hadoop 3.3.5 + Windows 10/11 ke community-tested steps par based hai. Windows par Hadoop kabhi kabhi laptop-specific masle dikhata hai. Koi step fail ho to **poora error message copy karke mujhe bhejo**, hum mil kar theek kar lenge.
