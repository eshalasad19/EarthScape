# Missing Data Handling Rule (Job 1)

Input shared schema: station_id,date,region,latitude,longitude,avg_temp_c,min_temp_c,max_temp_c,precip_mm,humidity_pct,co2_ppm
Date format assumption: YYYY-MM-DD.

## Quality report
Mapper har khali field ke liye (column name, 1) emit karta hai aur har row ke liye (TOTAL_ROWS, 1).
Reducer inka total deta hai. Output: /climate/processed/quality_report/

## Cleaning rule
1. Numeric columns (avg_temp_c, min_temp_c, max_temp_c, precip_mm, humidity_pct, co2_ppm) mein khali value
   us station ki usi mahine (YYYY-MM) ki average se fill hoti hai.
2. Agar us station-month mein koi value hi nahi, field khali rehti hai aur row "flagged" hoti hai
   (Hadoop counter: quality / flagged_rows). Schema 11 columns hi rehta hai.
3. Agar station_id ya date missing ho (ya row mein 11 fields na hon), row skip hoti hai (counter: bad_rows).
Output: /climate/processed/clean/