# Diversity analysis: A1 vs A3

Endpoint Gini includes all Cora nodes, including unused nodes. Hub endpoints are exactly the top 10% of nodes by train-graph degree, ties broken by node ID.

| Method | unique pair ratio | unique endpoint ratio | Gini | max endpoint frequency | top-1% coverage | top-10% contribution | hub endpoint ratio | pair reuse max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A1 | 100.000% | 17.803% | 0.656295 | 26.0 | 5.626% | 38.681% | 27.195% | 1.0 |
| A3 | 100.000% | 18.895% | 0.616172 | 21.666666666666668 | 5.028% | 34.641% | 21.962% | 1.0 |

- H1 raw extreme-hardness signal: present; isolated H1 condition (unique-endpoint difference <5%): False; extreme-hard decrease 49.65%; unique-endpoint difference 6.13%.
- H2: DIVERSITY_SHIFT; thresholds Gini drop >=.01, unique endpoint gain >=10%, or hub ratio drop >=5pp.
- Adjacent-epoch overlap is 1.0 and per-positive distinct negatives across epochs is 1.0 because the historical V6.1 sampler was static.
