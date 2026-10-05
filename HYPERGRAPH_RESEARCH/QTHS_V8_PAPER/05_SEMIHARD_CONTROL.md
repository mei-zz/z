# Matched semi-hard and random-hard controls

SH75 samples uniformly from each positive's graph-teacher hardness ranks [50%,75%] within the shared 20-item train pool. RANDOM_HARD50 samples uniformly from the top 50% of the same pool. All runs are Cora, GCN, STRICT_TRAIN_ONLY, fixed epoch 10, 3 seeds.

| Method | Seed 0 | Seed 1 | Seed 2 | Mean ± sample SD |
|---|---:|---:|---:|---:|
| SH75 | 0.494523 | 0.552162 | 0.556404 | 0.534363 ± 0.034567 |
| QTHS25 | 0.530263 | 0.383612 | 0.510112 | 0.474662 ± 0.079493 |
| RANDOM_HARD50 | 0.539313 | 0.501937 | 0.598117 | 0.546455 ± 0.048486 |

- QTHS25 − SH75 paired deltas: [0.03573957461716598, -0.16854991250481494, -0.046291887784724706].
- Paired mean delta: -0.059701; QTHS25 wins 1/3.
- Gate: **QTHS25_NOT_ABOVE_SH75**.

- Existing-baseline audit: no ready DNS, self-adversarial or DMNS implementation was found in the project. Those methods were not reimplemented from scratch; RANDOM_HARD50 and SH75 provide the registered matched controls.
