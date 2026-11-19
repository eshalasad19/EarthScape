# Scalability and Load Balancing

## Storage scalability (HDFS)
- Files are split into blocks and spread across DataNodes. Storage grows by adding DataNodes (horizontal scaling), without changing applications.
- Our lab setup uses one node with replication factor 1. A production cluster would use replication factor 3, so data survives node failures.
- Partitioning by year (`year=YYYY`) lets jobs read only the data they need.

## Processing scalability (MapReduce on YARN)
- Each job is split into parallel map tasks (one per block) and reduce tasks.
- More nodes mean more tasks run at the same time, so processing time drops as data grows.
- Optimizations used: combiners (less shuffle data) and tuned reducer counts. Results are in `monitoring/performance-table.md`.

## Query scalability (Impala)
- Impala runs queries in parallel across the nodes holding the data and reads data directly from HDFS.
- Parquet/partitioned tables can be added to speed up large queries.
- (Impala deployment details depend on the environment decision.)

## Load balancing (Apache server)
- Apache `mod_proxy_balancer` distributes incoming requests across several backend servers using the `byrequests` method.
- Configuration is in `apache/httpd-changes.txt`. In this project it is a demonstration for the documentation site.
- In a production setup the same approach would sit in front of multiple application or dashboard servers.

## Growth plan
| Stage | Change |
|---|---|
| Current (lab) | 1 node, replication 1 |
| Next | Add DataNodes and NodeManagers, set replication to 3 |
| Later | Add NameNode high availability, more Impala nodes, balancer in front of web services |