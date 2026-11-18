-- EarthScape: Impala external tables on /climate/processed/
CREATE DATABASE IF NOT EXISTS earthscape;
USE earthscape;

CREATE EXTERNAL TABLE IF NOT EXISTS yearly_region_avg (
  region STRING, `year` INT, avg_temp_c DOUBLE, avg_precip_mm DOUBLE, avg_co2_ppm DOUBLE)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/climate/processed/yearly_region_avg/';

CREATE EXTERNAL TABLE IF NOT EXISTS clean_data (
  station_id STRING, `date` STRING, region STRING, latitude DOUBLE, longitude DOUBLE,
  avg_temp_c DOUBLE, min_temp_c DOUBLE, max_temp_c DOUBLE,
  precip_mm DOUBLE, humidity_pct DOUBLE, co2_ppm DOUBLE)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/climate/processed/clean/';

CREATE EXTERNAL TABLE IF NOT EXISTS anomalies (
  station_id STRING, `date` STRING, metric STRING, value DOUBLE,
  mean DOUBLE, std DOUBLE, zscore DOUBLE)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/climate/processed/anomalies/';

CREATE EXTERNAL TABLE IF NOT EXISTS correlation (
  scope STRING, n BIGINT, pearson_r DOUBLE)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/climate/processed/correlation/';

-- quality_report ka output tab-separated hai (column_name <TAB> count)
CREATE EXTERNAL TABLE IF NOT EXISTS quality_report (
  column_name STRING, missing_count BIGINT)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
LOCATION '/climate/processed/quality_report/';

-- Naya data aane par:
-- REFRESH yearly_region_avg;  REFRESH clean_data;  REFRESH anomalies;
-- REFRESH correlation;        REFRESH quality_report;