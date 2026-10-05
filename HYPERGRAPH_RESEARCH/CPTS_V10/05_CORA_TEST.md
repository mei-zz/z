# Cora test

Frozen V8/V7.1 candidate set; evaluated once after validation GO; fixed epoch 10; seeds 0–2. Cached Graph-hard and QTHS25 checkpoints were reused; new CPTS, SH75 and matched controls were evaluated.

| Method | Seed 0 | Seed 1 | Seed 2 | Mean ± sample SD |
|---|---:|---:|---:|---:|
| GRAPH_HARD | 0.555629 | 0.370896 | 0.491130 | 0.472552 ± 0.093757 |
| QTHS25 | 0.554033 | 0.384672 | 0.541427 | 0.493377 ± 0.094352 |
| CPTS | 0.504261 | 0.542540 | 0.600427 | 0.549076 ± 0.048415 |
| SH75 | 0.502111 | 0.565111 | 0.557502 | 0.541575 ± 0.034388 |
| MATCHED_Q | 0.503532 | 0.547797 | 0.602036 | 0.551122 ± 0.049336 |
| RANDOM_MATCHED | 0.552018 | 0.367092 | 0.533784 | 0.484298 ± 0.101912 |

| CPTS vs | Paired deltas | Mean delta | Wins/3 |
|---|---|---:|---:|
| GRAPH_HARD | [-0.051368, 0.171645, 0.109297] | +0.076525 | 2/3 |
| QTHS25 | [-0.049772, 0.157869, 0.059] | +0.055699 | 2/3 |
| SH75 | [0.00215, -0.022571, 0.042925] | +0.007501 | 2/3 |
| MATCHED_Q | [0.000729, -0.005257, -0.00161] | -0.002046 | 1/3 |
| RANDOM_MATCHED | [-0.047757, 0.175448, 0.066643] | +0.064778 | 2/3 |

Cora test gate: **SUPPORTED**.
