# Cora validation

STRICT_TRAIN_ONLY; seeds 0–2; fixed epoch 10; test disabled. Frozen V7.1/V8 arms are reused after pool, candidate and protocol hashes were confirmed by the training harness.

| Method | Seed 0 | Seed 1 | Seed 2 | Mean |
|---|---:|---:|---:|---:|
| UNIFORM | 0.485973 | 0.591476 | 0.569234 | 0.548894 |
| GRAPH_HARD | 0.532759 | 0.328583 | 0.500069 | 0.453804 |
| RANDOM_VETO | 0.531053 | 0.361110 | 0.519806 | 0.470656 |
| QTHS25 | 0.530263 | 0.383612 | 0.510112 | 0.474662 |
| SH75 | 0.494523 | 0.552162 | 0.556404 | 0.534363 |
| CPTS | 0.494901 | 0.530459 | 0.585776 | 0.537045 |
| GLOBAL_CPTS | 0.454645 | 0.345047 | 0.530634 | 0.443442 |
| MATCHED_Q | 0.499867 | 0.515114 | 0.569308 | 0.528096 |
| RANDOM_MATCHED | 0.535604 | 0.357739 | 0.530796 | 0.474713 |

## CPTS paired comparisons

| Comparator | Seed deltas | Mean delta | Wins/3 |
|---|---|---:|---:|
| GRAPH_HARD | [-0.037858, 0.201876, 0.085707] | +0.083242 | 2/3 |
| QTHS25 | [-0.035362, 0.146847, 0.075664] | +0.062383 | 2/3 |
| SH75 | [0.000378, -0.021703, 0.029372] | +0.002682 | 2/3 |
| GLOBAL_CPTS | [0.040256, 0.185412, 0.055142] | +0.093604 | 3/3 |
| MATCHED_Q | [-0.004966, 0.015345, 0.016468] | +0.008949 | 2/3 |
| RANDOM_MATCHED | [-0.040703, 0.17272, 0.05498] | +0.062333 | 2/3 |

Validation decision: **GO**. Test remains disabled in this phase.
