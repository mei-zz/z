# Stage 0 — Zero-GPU Signal Audit

Decision: SCALAR_SUFFICIENT
Matched legal negatives: 13464; positives with matches: 4488.
Informative shuffle fraction: 0.140653 (LOW_SHUFFLE_POWER).
Median E: positives 4.000000; matched negatives 0.000000.

| Feature set | ROC-AUC mean ± sample SD | PR-AUC mean ± sample SD |
|---|---:|---:|
| Z0 support count | 0.804146 ± 0.006650 | 0.595130 ± 0.017701 |
| Z1 MS scalar | 0.808875 ± 0.006793 | 0.620486 ± 0.018041 |
| Z2 HRA-like | 0.820960 ± 0.006949 | 0.716169 ± 0.013683 |
| Z3 real joint | 0.815152 ± 0.005981 | 0.693106 ± 0.009525 |
| Z4 shuffled | 0.812516 ± 0.006160 | 0.675174 ± 0.011093 |

## Gate checks

- real_auc_gt_cn_plus_0_015: FAIL
- real_auc_gt_shuffle_plus_0_010: FAIL
- real_auc_at_least_both_scalar_controls: FAIL
- positive_median_E_gt_matched_negative_median_E: PASS
- informative_shuffle_fraction_at_least_0_20: FAIL

Interpretation: A scalar MS or HRA-like control beats the real joint feature set; the HMC set encoder fails the scalar-residual gate. LOW_SHUFFLE_POWER; real≈shuffle is not interpreted directly.

Local subtraction matched full target-masked raw_star rebuild on 100 sampled training positives. Endpoint symmetry passed. Validation/test identities were not used; test is sealed. No GPU training ran in Stage 0.
