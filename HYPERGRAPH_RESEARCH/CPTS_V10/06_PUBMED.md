# PubMed

Frozen graph-teacher candidate pool; same BIC rule; GCN, fixed epoch 10, seeds 0–2. Graph-hard and QTHS25 validation results reused from V8; CPTS and SH75 trained under V10.

| Method | Seed 0 | Seed 1 | Seed 2 | Mean ± sample SD |
|---|---:|---:|---:|---:|
| GRAPH_HARD | 0.822159 | 0.769394 | 0.819564 | 0.803706 ± 0.029743 |
| QTHS25 | 0.843657 | 0.835554 | 0.853591 | 0.844267 ± 0.009034 |
| CPTS | 0.840324 | 0.828205 | 0.842333 | 0.836954 ± 0.007643 |
| SH75 | 0.798906 | 0.764467 | 0.758705 | 0.774026 ± 0.021739 |

| CPTS vs | Paired deltas | Mean delta | Wins/3 |
|---|---|---:|---:|
| GRAPH_HARD | [0.018165, 0.058812, 0.022769] | +0.033249 | 3/3 |
| QTHS25 | [-0.003332, -0.007349, -0.011258] | -0.007313 | 0/3 |
| SH75 | [0.041418, 0.063739, 0.083628] | +0.062928 | 3/3 |

Clear reversal flag: **False** (defined before continuation as CPTS mean at least 0.005 below both Graph-hard and SH75, with at most one win vs Graph-hard).
