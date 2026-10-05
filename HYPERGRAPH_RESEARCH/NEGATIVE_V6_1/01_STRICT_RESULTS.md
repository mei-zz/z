# V6.1 Strict Results

Validation uses the unchanged V6 fixed candidate tensor. Values are MRR mean ± sample SD over seeds 0/1/2.

| Protocol | A1 Graph-hard | A3 shuffled veto | A4 true HG veto |
|---|---:|---:|---:|
| STRICT_TRAIN_ONLY | 0.454154 ± 0.109893 | 0.470656 ± 0.095036 | 0.504955 ± 0.076752 |
| FILTERED_ALL_POSITIVE (reused V6) | 0.482796 ± 0.074947 | 0.503866 ± 0.067535 | 0.526094 ± 0.041756 |

## Per-seed strict validation MRR

| Seed | A1 | A3 | A4 | A4−A1 | A4−A3 |
|---:|---:|---:|---:|---:|---:|
| 0 | 0.532759 | 0.531053 | 0.532958 | +0.000199 | +0.001906 |
| 1 | 0.328583 | 0.361110 | 0.418133 | +0.089550 | +0.057023 |
| 2 | 0.501120 | 0.519806 | 0.563773 | +0.062653 | +0.043967 |

STRICT_MECHANISM_SIGNAL validation gate: **YES** (3/3 A4 wins vs A1; 3/3 vs A3; both mean deltas must be positive).

Strict checkpoints use the fixed final epoch because validation-based checkpoint selection is disallowed in STRICT_TRAIN_ONLY.
