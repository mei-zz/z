# Hardness distribution: A1 vs A3

Rg_per_positive is the rank percentile among the same positive's 20 train-only candidates; Rg_global_pool is the percentile among all 89,760 candidate occurrences. Top-1/5/10% are reported on both scales. Statistics are repeated for each epoch because V6.1 selections are static.

| Method | Mean Rg | Median | P90 | P95 | P99 | Max | Extreme >=.95 | Ultra >=.99 | local top 1/5/10% | global top 1/5/10% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| A1 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 100.00% | 100.00% | 100.00%/100.00%/100.00% | 18.25%/65.04%/88.28% |
| A3 | 0.973868 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 50.35% | 50.35% | 50.35%/50.35%/100.00% | 10.14%/46.11%/75.10% |

Graph raw-score quantiles and per-seed values are in results.json; epoch-level rows are in A_QTHS/A1_A3_selected_negative_statistics.csv.gz.
