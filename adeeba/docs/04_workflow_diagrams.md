# MapReduce Workflow Diagrams

Job 1 quality : input CSV -> mapper (khali fields -> column,1) -> shuffle/sort -> reducer (sum) -> quality_report/
Job 1 clean   : input CSV -> mapper (key station|YYYY-MM) -> shuffle -> reducer (month avg se fill, flag) -> clean/
Job 2 yearly  : clean/ -> mapper (region|year, partial sums) -> combiner -> shuffle -> reducer (averages) -> yearly_region_avg/
Job 3 anomaly : clean/ -> mapper A -> shuffle -> reducer A (n, mean, std) -> stats
                clean/ + stats -> mapper B -> shuffle -> reducer B (z-score, threshold) -> anomalies/
Job 4 corr    : clean/ -> mapper (region|ALL, x,y) -> shuffle -> reducer (sums -> Pearson r) -> correlation/