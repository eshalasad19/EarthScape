# EarthScape Climate Agency: Big Data eProject (Aptech)

Hadoop/HDFS par climate data ko store, process aur analyze karna, ML models banana aur Tableau dashboards dikhana.

## Stack (sirf ye, is se bahar kuch nahi)
Jupyter Anaconda Notebook 3, RStudio, VS Code / PyCharm, MongoDB Compass + Shell, Hadoop + HDFS + Apache server, Tableau, Impala server.

## Team aur folders
| Member | Folder | Module |
|---|---|---|
| Eshal (Leader) | `eshal/` | Hadoop/HDFS setup, security, backup, monitoring, integration, final submission |
| Alizah | `alizah/` | Data ingestion, MongoDB, users/roles, feedback system |
| Adeeba | `adeeba/` | MapReduce jobs, Impala queries |
| Wania | `wania/` | ML models, alerts, Tableau dashboards |

## Repo structure
```
README.md
.gitignore
eshal/    alizah/    adeeba/    wania/
```
Har member ke folder ka andar ka structure uski task file mein hai.

## Git rules
1. Sab seedha `main` par push karte hain (koi branch nahi).
2. Har member sirf apne folder mein kaam kare. Doosre ka folder edit nahi.
3. Push se pehle: `git pull --rebase origin main`
4. Bari data files, passwords aur credentials repo mein nahi.
5. Commit message: `folder: kya kiya` (misaal: `adeeba: job2 yearly avg added`).

## Shared data contract
**Cleaned CSV columns (is order mein):**
`station_id,date,region,latitude,longitude,avg_temp_c,min_temp_c,max_temp_c,precip_mm,humidity_pct,co2_ppm`

**HDFS folders:**
```
/climate/raw/historical/year=YYYY/
/climate/raw/streaming/
/climate/raw/satellite/
/climate/processed/      (Adeeba)
/climate/ml_output/      (Wania)
/climate/backup/
```
