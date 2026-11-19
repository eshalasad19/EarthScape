# Access Control Matrix

Two roles are defined: **Admin** and **Analyst**.
HDFS access is controlled with permissions/ACLs. MongoDB access is controlled with built-in roles (created by Alizah).

| Resource | Admin | Analyst |
|---|---|---|
| HDFS `/climate/raw` | Read / Write | Read |
| HDFS `/climate/processed` | Read / Write | Read |
| HDFS `/climate/ml_output` | Read / Write | Read |
| HDFS `/climate/admin_only` | Read / Write | No access |
| MongoDB data (`sensor_readings`, `satellite_metadata`) | Read / Write | Read |
| MongoDB `feedback` | Read / Write / Update | Insert only |
| MongoDB `alerts` | Read / Write | Read |
| MongoDB `users` and role management | Full | No access |

## Notes
- Admin is the user that starts Hadoop (HDFS superuser) and the MongoDB `admin` user.
- Analyst is a restricted user: can read data and dashboards, cannot modify or delete data.
- HDFS runs in simple authentication mode, so these rules control access by user name only (see `encryption-note.md` for limitations).
- MongoDB rows to be confirmed with Alizah after her roles are created.