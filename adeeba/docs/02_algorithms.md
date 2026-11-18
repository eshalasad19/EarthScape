# Algorithm Explanation

## Job 2: Yearly average (combiner ke saath)
Key = region|year. Value = (sumT, cntT, sumP, cntP, sumC, cntC).
Combiner mapper-side par partial sums jama karta hai, is se shuffle ka data kam hota hai.
Reducer final sums ko count se divide karke average deta hai.

## Job 3: Anomaly detection (z-score, do pass)
Pass A: har (station, calendar month, metric) ke liye n, mean (mu) aur standard deviation (sigma).
    sigma = sqrt( (sum of x^2)/n - mu^2 )
Pass B: har reading x ke liye
    z = (x - mu) / sigma
Agar |z| > THRESHOLD (config.py, default 2.5) to row anomalies mein jati hai. sigma = 0 ho to skip.
Metrics: avg_temp_c, precip_mm, co2_ppm.

## Job 4: Pearson correlation (temperature x vs CO2 y)
Reducer in sums jama karta hai: n, Sx, Sy, Sxx, Syy, Sxy.
    r = (n*Sxy - Sx*Sy) / sqrt( (n*Sxx - Sx^2) * (n*Syy - Sy^2) )
Region-wise aur overall (scope = ALL) dono. r, -1 se +1 ke beech hota hai.