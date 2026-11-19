# 03_correlation.R  (Wania)  -  correlation analysis in RStudio, base R only (no packages)
# Input : clean.csv (Adeeba Job 1b) and yearly_region_avg.csv (Job 2), header-less CSV
#   hdfs dfs -getmerge /climate/processed/clean ..\notebooks\data\clean.csv
#   hdfs dfs -getmerge /climate/processed/yearly_region_avg ..\notebooks\data\yearly_region_avg.csv
# In RStudio: open this file, set the working directory (Session > Set Working Directory > To Source File Location)
# and click Source.

data_dir <- Sys.getenv("DATA_DIR", unset = "../notebooks/data")
if (!file.exists(file.path(data_dir, "clean.csv"))) {
  data_dir <- "../../adeeba/mapreduce/local_output"      # development fallback
}
out_dir <- "output"
dir.create(out_dir, showWarnings = FALSE)

cols <- c("station_id", "date", "region", "latitude", "longitude",
          "avg_temp_c", "min_temp_c", "max_temp_c", "precip_mm", "humidity_pct", "co2_ppm")
clean <- read.csv(file.path(data_dir, "clean.csv"), header = FALSE, col.names = cols, stringsAsFactors = FALSE)
yearly <- read.csv(file.path(data_dir, "yearly_region_avg.csv"), header = FALSE,
                   col.names = c("region", "yr", "avg_temp_c", "avg_precip_mm", "avg_co2_ppm"),
                   stringsAsFactors = FALSE)

# 1) correlation matrix of the numeric daily variables
num_cols <- c("avg_temp_c", "precip_mm", "humidity_pct", "co2_ppm")
cm <- cor(clean[, num_cols], use = "pairwise.complete.obs")
print(round(cm, 3))
write.csv(round(cm, 4), file.path(out_dir, "correlation_matrix.csv"))

# 2) temperature vs CO2 (daily data) with a significance test
ct <- cor.test(clean$avg_temp_c, clean$co2_ppm)
cat("\nDaily temperature vs CO2: r =", round(ct$estimate, 4), " p-value =", signif(ct$p.value, 3), "\n")

# 3) temperature vs CO2 on yearly averages (the long-term trend is clearer here)
yearly <- yearly[!is.na(yearly$avg_temp_c) & !is.na(yearly$avg_co2_ppm), ]
ct_y <- cor.test(yearly$avg_temp_c, yearly$avg_co2_ppm)
cat("Yearly temperature vs CO2: r =", round(ct_y$estimate, 4), " p-value =", signif(ct_y$p.value, 3), "\n")

# 4) simple linear model: yearly temperature explained by CO2, per region
res <- do.call(rbind, lapply(split(yearly, yearly$region), function(d) {
  if (nrow(d) < 5) return(NULL)
  m <- lm(avg_temp_c ~ avg_co2_ppm, data = d)
  data.frame(region = d$region[1], n_years = nrow(d),
             r = cor(d$avg_temp_c, d$avg_co2_ppm),
             slope_c_per_ppm = coef(m)[2], r_squared = summary(m)$r.squared)
}))
print(res)
write.csv(res, file.path(out_dir, "yearly_temp_vs_co2_by_region.csv"), row.names = FALSE)

# 5) plot (saved as PNG for the documentation)
png(file.path(out_dir, "temp_vs_co2_yearly.png"), width = 900, height = 600)
plot(yearly$avg_co2_ppm, yearly$avg_temp_c, pch = 19, col = "steelblue",
     xlab = "Average CO2 (ppm)", ylab = "Average temperature (C)",
     main = "Yearly average temperature vs CO2")
abline(lm(avg_temp_c ~ avg_co2_ppm, data = yearly), col = "red", lwd = 2)
dev.off()
cat("\nresults saved in the 'output' folder\n")