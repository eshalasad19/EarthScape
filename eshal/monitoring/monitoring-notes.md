# Monitoring Notes

## HDFS: NameNode UI (http://localhost:9870)
| Where | What to check |
|---|---|
| Overview | Cluster status, configured capacity, DFS used, live DataNodes (should be 1) |
| Datanodes | DataNode is "In Service", last contact is recent |
| Utilities > Browse the file system | `/climate` folders exist, file sizes, replication, block size |

## YARN: ResourceManager UI (http://localhost:8088)
| Where | What to check |
|---|---|
| Cluster Metrics (top) | Apps submitted/completed/failed, memory used |
| Applications | Each MapReduce job: State, FinalStatus, Elapsed Time |
| Nodes | NodeManager is RUNNING |

## Command line checks
```
jps
hdfs dfsadmin -report
hdfs dfs -du -h /climate
```
`jps` must list NameNode, DataNode, ResourceManager, NodeManager.

## Impala UI
To be added after the Impala environment decision.

## Screenshots (Screenshot yahan lagegi, baad mein)
- [ ] NameNode Overview
- [ ] NameNode Datanodes tab
- [ ] NameNode Browse the file system (`/climate`)
- [ ] YARN Applications list with finished jobs
- [ ] YARN Cluster Metrics
- [ ] `jps` output
- [ ] `hdfs dfsadmin -report` output

## Monitoring routine
- Before every demo or job run: check `jps`, then both UIs.
- After every job: note its elapsed time in `performance-table.md`.
- Weekly: check free disk space for HDFS (Overview > DFS Remaining).