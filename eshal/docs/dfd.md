# Data Flow Diagrams

## Level 0 (Context diagram)
```mermaid
flowchart LR
  S["Data sources (stations, sensors, satellite)"] -->|climate data| SYS(("EarthScape Climate Analysis System"))
  AD["Admin"] -->|manage data and users| SYS
  AN["Analyst"] -->|queries, feedback| SYS
  SYS -->|dashboards, query results, alerts| AN
  SYS -->|system status, user management| AD
```

## Level 1
```mermaid
flowchart TB
  S["Data sources"] -->|raw data| P1(("1. Ingest data"))
  P1 -->|raw files| D1[("D1: HDFS raw")]
  P1 -->|readings, image metadata| D4[("D4: MongoDB")]
  D1 -->|raw files| P2(("2. Process data (MapReduce)"))
  P2 -->|cleaned data, patterns, anomalies, correlations| D2[("D2: HDFS processed")]
  D2 --> P3(("3. Query data (Impala)"))
  AN["Analyst"] -->|SQL queries| P3
  P3 -->|query results| AN
  D2 -->|processed data| P4(("4. ML and alerts"))
  P4 -->|predictions| D3[("D3: HDFS ml_output")]
  P4 -->|alerts| D4
  D2 --> P5(("5. Visualize (Tableau)"))
  D3 --> P5
  P5 -->|dashboards| AN
  P5 -->|dashboards| AD["Admin"]
  AD -->|manage users, roles| P6(("6. Users and feedback"))
  AN -->|feedback, support requests| P6
  P6 <-->|users, feedback| D4
```

## Process descriptions
| No. | Process | Input | Output |
|---|---|---|---|
| 1 | Ingest data | Historical files, simulated real-time batches, satellite images | Files in HDFS raw; records in MongoDB |
| 2 | Process data (MapReduce) | HDFS raw | Cleaned data, yearly averages, anomalies, correlations in HDFS processed |
| 3 | Query data (Impala) | HDFS processed, analyst SQL | Query results |
| 4 | ML and alerts | HDFS processed | Predictions in HDFS ml_output; alerts in MongoDB |
| 5 | Visualize (Tableau) | Processed data, predictions | Interactive dashboards |
| 6 | Users and feedback | Role management, feedback requests | Users, roles and feedback in MongoDB |