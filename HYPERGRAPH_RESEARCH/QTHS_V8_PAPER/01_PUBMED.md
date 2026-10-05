# PubMed validation and test

Frozen QTHS25; STRICT_TRAIN_ONLY; fixed epoch 10; Graph-hard, Random-veto and QTHS25 share the same split, candidate pool and evaluation candidates.

## Validation MRR

| Method | Seed 0 | Seed 1 | Seed 2 | Mean ± sample SD |
|---|---:|---:|---:|---:|
| GRAPH_HARD | 0.822159 | 0.769394 | 0.819564 | 0.803706 ± 0.029743 |
| RANDOM_VETO | 0.849126 | 0.827578 | 0.853028 | 0.843244 ± 0.013706 |
| QTHS25 | 0.843657 | 0.835554 | 0.853591 | 0.844267 ± 0.009034 |

## Test MRR

| Method | Seed 0 | Seed 1 | Seed 2 | Mean ± sample SD |
|---|---:|---:|---:|---:|
| GRAPH_HARD | 0.815277 | 0.749911 | 0.810697 | 0.791962 ± 0.036489 |
| RANDOM_VETO | 0.850609 | 0.803583 | 0.844440 | 0.832877 ± 0.025557 |
| QTHS25 | 0.839578 | 0.817003 | 0.841788 | 0.832789 ± 0.013716 |

- QTHS25 − Graph-hard paired test deltas: [0.024300746526899064, 0.06709231933224735, 0.03109074160316494]
- QTHS25 mean test delta: +0.040828; wins: 3/3.
- PUBMED_SUPPORTED: **YES** (requires mean test MRR above Graph-hard and at least 2/3 seed wins).
- Shared test candidate hash: 1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b.
