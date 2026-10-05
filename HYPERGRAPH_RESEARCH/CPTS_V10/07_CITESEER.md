# Citeseer

Frozen train-only graph-teacher pool; same BIC rule; GCN, fixed epoch 10, seeds 0–2. Graph-hard validation reused from V7.1.

| Method | Seed 0 | Seed 1 | Seed 2 | Mean ± sample SD |
|---|---:|---:|---:|---:|
| GRAPH_HARD | 0.357579 | 0.540164 | 0.354335 | 0.417359 ± 0.106364 |
| CPTS | 0.475844 | 0.500430 | 0.430847 | 0.469040 ± 0.035287 |
| SH75 | 0.505302 | 0.507931 | 0.434373 | 0.482535 ± 0.041730 |

| CPTS vs | Paired deltas | Mean delta | Wins/3 |
|---|---|---:|---:|
| GRAPH_HARD | [0.118265, -0.039734, 0.076512] | +0.051681 | 2/3 |
| SH75 | [-0.029458, -0.007501, -0.003526] | -0.013495 | 0/3 |

Citeseer is descriptive; neutral performance is allowed and no rule changes are permitted.
