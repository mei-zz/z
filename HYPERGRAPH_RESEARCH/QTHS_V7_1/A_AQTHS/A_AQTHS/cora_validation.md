# AQTHS Cora validation gate

All trim thresholds and per-positive tail statistics use the training candidate pool only. The global high-tail threshold is the median over Cora training positives; no model or threshold was selected on validation.

| Method | Seed 0 | Seed 1 | Seed 2 | Mean | Sample SD |
|---|---:|---:|---:|---:|---:|
| A0_GRAPH_HARD | 0.532759 | 0.328583 | 0.500069 | 0.453804 | 0.109669 |
| A1_QTHS25 | 0.530263 | 0.383612 | 0.510112 | 0.474662 | 0.079493 |
| A2_RANDOM_ADAPTIVE | 0.530402 | 0.371386 | 0.514132 | 0.471973 | 0.087490 |
| A3_DEGREE_ADAPTIVE | 0.534038 | 0.363957 | 0.498847 | 0.465614 | 0.089778 |
| A4_AQTHS | 0.528262 | 0.361870 | 0.509276 | 0.466469 | 0.091082 |

- Gate: **REJECT**; mean gain=-0.008193 (-1.726%); wins vs QTHS25=0/3, vs random adaptive=0/3.
- A2 randomly assigns the same number of 15%/35% positives as AQTHS. A3 assigns them by train-graph endpoint-degree sum. A4 assigns them by train-pool hardness-tail excess.
