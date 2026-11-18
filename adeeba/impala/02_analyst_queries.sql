USE earthscape;

-- Q1: Har region ka sab se garam saal
SELECT y.region, y.`year`, y.avg_temp_c
FROM yearly_region_avg y
JOIN (SELECT region, MAX(avg_temp_c) AS mx FROM yearly_region_avg GROUP BY region) m
  ON y.region = m.region AND y.avg_temp_c = m.mx
ORDER BY y.region;

-- Q2: Top 10 anomalies (|zscore| ke hisab se)
SELECT * FROM anomalies ORDER BY ABS(zscore) DESC LIMIT 10;

-- Q3: Region-wise temperature trend (saal ke saath)
SELECT region, `year`, avg_temp_c
FROM yearly_region_avg
ORDER BY region, `year`;

-- Q4: Missing data ka percentage per column
SELECT q.column_name, q.missing_count,
       ROUND(100.0 * q.missing_count / t.missing_count, 2) AS missing_pct
FROM quality_report q
CROSS JOIN (SELECT missing_count FROM quality_report WHERE column_name = 'TOTAL_ROWS') t
WHERE q.column_name <> 'TOTAL_ROWS'
ORDER BY missing_pct DESC;

-- Q5: Temperature aur CO2 ki correlation per region
SELECT scope, n, pearson_r
FROM correlation
WHERE scope <> 'ALL'
ORDER BY pearson_r DESC;

-- Q6: Har mahine ke anomalies ki ginti
SELECT SUBSTR(`date`, 1, 7) AS month, COUNT(*) AS anomaly_count
FROM anomalies
GROUP BY SUBSTR(`date`, 1, 7)
ORDER BY month;

-- Q7: Metric ke hisab se anomalies
SELECT metric, COUNT(*) AS anomaly_count
FROM anomalies
GROUP BY metric
ORDER BY anomaly_count DESC;

-- Q8: Sab se zyada anomalies wale stations
SELECT station_id, COUNT(*) AS anomaly_count
FROM anomalies
GROUP BY station_id
ORDER BY anomaly_count DESC
LIMIT 10;

-- Q9: Har region ka sab se zyada CO2 wala saal
SELECT y.region, y.`year`, y.avg_co2_ppm
FROM yearly_region_avg y
JOIN (SELECT region, MAX(avg_co2_ppm) AS mx FROM yearly_region_avg GROUP BY region) m
  ON y.region = m.region AND y.avg_co2_ppm = m.mx
ORDER BY y.region;

-- Q10: Cleaning ke baad bhi jin rows mein temperature ya CO2 khali reh gayi (flagged rows)
SELECT region, COUNT(*) AS flagged_rows
FROM clean_data
WHERE avg_temp_c IS NULL OR co2_ppm IS NULL
GROUP BY region
ORDER BY flagged_rows DESC;