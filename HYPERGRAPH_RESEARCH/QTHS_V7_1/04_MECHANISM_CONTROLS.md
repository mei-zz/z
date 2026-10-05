# V7.1 mechanism controls

Validation only. The Graph-hard, random-veto and QTHS25 rows reuse the locked Cora checkpoints; HMC and DMC are newly trained at fixed epoch 10.

| Method | Seed 0 | Seed 1 | Seed 2 | Mean | Sample SD |
|---|---:|---:|---:|---:|---:|
| GRAPH_HARD | 0.532759 | 0.328583 | 0.500069 | 0.453804 | 0.109669 |
| RANDOM_VETO | 0.531053 | 0.361110 | 0.519806 | 0.470656 | 0.095036 |
| HMC | 0.525253 | 0.350907 | 0.517232 | 0.464464 | 0.098425 |
| QTHS25 | 0.530263 | 0.383612 | 0.510112 | 0.474662 | 0.079493 |
| DMC | 0.539790 | 0.376838 | 0.531618 | 0.482749 | 0.091812 |

- Mechanism class: **INCONCLUSIVE**.
- QTHS25 beats HMC in 2/3 seed comparisons; beats DMC in 1/3.
- Per-seed HMC hardness quantile matching and DMC diversity/hardness deviations are in results.json.
