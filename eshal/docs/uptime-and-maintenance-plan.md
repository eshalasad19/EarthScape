# Uptime and Maintenance Plan

## Target
99% availability. That allows about 7.2 hours of downtime per 30-day month.

## How the design supports it
- Daily HDFS snapshots and MongoDB backups (see `backup/backup-plan.md`)
- Monitoring of HDFS and YARN health (see `monitoring/monitoring-notes.md`)
- Documented start/stop and recovery procedure
- Scalability path to a multi-node cluster (see `scalability-and-load-balancing.md`)

## Planned maintenance
- Window: a fixed low-usage slot each week (for example Sunday, 2:00 AM - 4:00 AM).
- Notice: users are informed at least 24 hours in advance through a notice on the Apache documentation page and by message to the user group.
- Steps: take a snapshot -> stop services (`stop-yarn.cmd`, `stop-dfs.cmd`) -> do the work -> start services -> run `jps` and check both UIs -> announce completion.

## Unplanned downtime (recovery)
1. Run `jps` and open the NameNode and YARN UIs to find the failed service.
2. Restart the failed service (`start-dfs.cmd` / `start-yarn.cmd`).
3. If data is damaged, restore from the latest snapshot or backup.
4. Note the cause and downtime in an incident log.

## Incident log (template)
| Date | Start | End | Duration | Cause | Fix |
|---|---|---|---|---|---|
| | | | | | |

## Limitation
Our lab environment is a single node, so a true 99% guarantee is a design target, not something one machine can promise. Production would need a multi-node cluster with NameNode high availability.