# Efficiency and parameter overhead

Cora GCN seed 0; same fixed 10-epoch training budget. Wall time is a single measured run per method; it is descriptive and hardware-specific.

| Method | Train seconds | Wall seconds | Selection preprocessing s | Sampling microbenchmark s/epoch | Peak CUDA allocated MiB | Trainable parameters |
|---|---:|---:|---:|---:|---:|---:|
| UNIFORM | 223.182 | 223.603 | 0.000018 | 0.000139 | 43.3 | 24735 |
| GRAPH_HARD | 225.785 | 226.219 | 0.000539 | 0.000004 | 43.4 | 24735 |
| QTHS25 | 195.418 | 195.945 | 0.024098 | 0.000004 | 43.4 | 24735 |

- Additional trainable parameters for QTHS: **0**.
- Parameter-count equality across sampling arms: **True**.
- Frozen graph-teacher candidate scoring time: {'dataset': 'Cora', 'candidate_pairs': 89760, 'wall_seconds': 12.250151271000504, 'score_hash_matches_frozen_cache': False, 'score_allclose_to_frozen_cache': True, 'allclose_rtol': 1e-05, 'allclose_atol': 1e-06, 'max_abs_difference': 3.5762786865234375e-07, 'mean_abs_difference': 2.3251024212641724e-08, 'scores_hash': '73a2394fe289159609f9ee66aefe78b5acd06384a98c7c808d5dcf6a7195ca43', 'cached_scores_hash': 'a1b01e0e2ad5cd287011862d65ade0681205d11ca99dc50cf1b763faf8a82d5c'}.
- Compute profile: {'gpu': 'Tesla V100-PCIE-16GB', 'cuda_build': '12.1', 'cpu_count': 40, 'max_workers': 6}.
