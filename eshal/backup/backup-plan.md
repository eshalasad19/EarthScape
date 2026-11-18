# Backup Plan

## What is backed up
| Data | Method | Frequency | Location |
|---|---|---|---|
| HDFS `/climate` (raw, processed, ml_output) | HDFS snapshot | Daily | Inside HDFS (`/climate/.snapshot/`) |
| HDFS `/climate` (full copy) | `hdfs dfs -get` to local disk | Weekly | `C:\earthscape-backups\hdfs\` |
| MongoDB database `earthscape` | `mongodump` | Daily | `C:\earthscape-backups\mongo\` |
| Hadoop config and project code | Git (GitHub, `main`) | On every push | GitHub repository |

`C:\earthscape-backups\` stays outside the Git repo (backups and credentials are never pushed).

## HDFS snapshots
- Protects against accidental deletion or overwrite. Files can be restored from `/climate/.snapshot/<name>/`.
- A snapshot lives on the same disk as HDFS, so it does not protect against disk failure. That is why the weekly full copy exists.
- Commands: see `snapshot-commands.cmd`.
- Keep the last 7 daily snapshots, delete older ones with `hdfs dfs -deleteSnapshot /climate <name>`.

## HDFS full copy (weekly)
```
mkdir C:\earthscape-backups\hdfs
hdfs dfs -get /climate C:\earthscape-backups\hdfs\climate-backup
```
(Use a new folder name each week, e.g. `climate-backup-2026-11-22`.)

## MongoDB backup
Needs MongoDB Database Tools (`mongodump`). Alizah confirms it is installed.
```
mkdir C:\earthscape-backups\mongo
mongodump --db earthscape --username <admin-user> --authenticationDatabase admin --out C:\earthscape-backups\mongo\backup-2026-11-22
```
`mongodump` asks for the password in the terminal. Do not write passwords in scripts or in the repo.
Restore: `mongorestore --username <admin-user> --authenticationDatabase admin C:\earthscape-backups\mongo\backup-2026-11-22`

The final submission needs a database backup, so the last `mongodump` folder goes into the final zip.

## Automation (Windows Task Scheduler)
Daily HDFS snapshot at 2:00 AM. Save Part 2 of `snapshot-commands.cmd` (without Part 1) as `C:\earthscape-backups\snapshot-daily.cmd`, then in CMD (Administrator):
```
schtasks /Create /SC DAILY /ST 02:00 /TN "EarthScape-HDFS-Snapshot" /TR "C:\earthscape-backups\snapshot-daily.cmd" /RL HIGHEST
```
Check: `schtasks /Query /TN "EarthScape-HDFS-Snapshot"`
The task only works while Hadoop is running.

## Restore test (evidence for documentation)
1. Delete a test file from HDFS.
2. Copy it back from the snapshot (`hdfs dfs -cp ...`).
3. Take a screenshot of each step.

Screenshots yahan lagengi (baad mein).