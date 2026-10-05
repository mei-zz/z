# Citeseer V7.1 results

- Split hash: `5a1a177685a1c3a4852f7e3034ea05ffd35b59aaf05fa58578cd40b0f1c46d36`; train pool hash: `e2b8d6babecc441e57b34fe2397238c9143e5a92786cf59affd0338c4015054f`; validation candidate hash: `419f7e31c9320e435b210d3b05614f7d202d95ea9968765df8ceb9f9bdd875c5`; test candidate hash: `48b69dc30431358d9c47d9792d1e1604a327a1d40c9fa440b53ed3c688470a26`.
- Runtime: `2.3.1+cu121`; fixed epoch: 10; evaluation candidates shared across all methods.

## Validation MRR

| Method | Seed 0 | Seed 1 | Seed 2 | Mean | Sample SD |
|---|---: | ---: | ---: | ---: | ---:|
| C1_GRAPH_HARD | 0.357579 | 0.540164 | 0.354335 | 0.417359 | 0.106364 |
| C2_RANDOM_VETO | 0.355210 | 0.530566 | 0.349741 | 0.411839 | 0.102857 |
| C3_QTHS25 | 0.375841 | 0.533890 | 0.371326 | 0.427019 | 0.092580 |

## Test MRR

| Method | Seed 0 | Seed 1 | Seed 2 | Mean | Sample SD |
|---|---: | ---: | ---: | ---: | ---:|
| C1_GRAPH_HARD | 0.354028 | 0.543725 | 0.420088 | 0.439280 | 0.096294 |
| C2_RANDOM_VETO | 0.366330 | 0.546049 | 0.384412 | 0.432264 | 0.098955 |
| C3_QTHS25 | 0.373869 | 0.543822 | 0.397860 | 0.438517 | 0.091982 |

- Transfer assessment: `{'positive_mean_on_validation': True, 'positive_mean_on_test': False, 'validation_wins_vs_graph_hard': 2, 'test_wins_vs_graph_hard': 2, 'supported': True, 'fully_reverse': False, 'rule': 'positive if validation OR test mean beats Graph-hard; report both without tuning'}`.
