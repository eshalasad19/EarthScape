# Data Contract (change karne se pehle poori team ko batao)

## Dataset
- Source: (NOAA / NASA / Kaggle, link yahan)

## Schema
record_id, source_type, station_id, region, date, temperature, humidity, rainfall, co2, sea_level

## HDFS Paths
- /earthscape/raw/<source_type>/year=YYYY/region=XX/
- /earthscape/streaming/
- /earthscape/processed/<job_name>/
- /earthscape/ml/
- /earthscape/rejected/

## Output formats
- Processed -> CSV/Parquet (decide)
- ML output -> CSV
- Anomalies -> /earthscape/processed/anomalies/