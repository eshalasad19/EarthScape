Hadoop config files for EarthScape eProject (Hadoop 3.3.5, Windows single node).

Copy core-site.xml, hdfs-site.xml, mapred-site.xml and yarn-site.xml
into C:\hadoop\etc\hadoop\ (replace the existing files).

Also edit C:\hadoop\etc\hadoop\hadoop-env.cmd:
  Find:    set JAVA_HOME=%JAVA_HOME%
  Replace: set JAVA_HOME=C:\Java8

Before starting Hadoop, create these folders:
  C:\hadoop-data\namenode
  C:\hadoop-data\datanode