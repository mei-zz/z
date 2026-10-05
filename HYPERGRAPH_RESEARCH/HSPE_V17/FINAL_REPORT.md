# HSPE V17 — execution report

**Status: HSPE_EARLY_REJECT**

Candidate: HSPE; V16 origin: C1_NHMC_SIZE. Test evaluated: false.

H1 uses the exact V16 C1 size-only set encoder: Linear(6,8), ReLU, mean/max pooling, log token/support counts, and a zero-initialized Linear(18,1) residual. No overlap inputs are used.

C1 is a zero-initialized single Linear(17,1) on 15 normalized unordered size-pair histogram bins plus log token/support counts. C2 assigns complete size-token multisets within split, exact token-count, shared-support-bin, and sorted endpoint-degree-bin strata. C3 uses the H1 encoder/head with constant [1,1,1] size descriptors and real token/support counts.

## Cora/PubMed 5E × 3 seeds

Decision: **HSPE_EARLY_REJECT**.

### Cora
Dataset gate passed: False; shuffle adequate: False.

| Seed | B0 | Histogram | Size-shuffle | Parameter-matched | HSPE-REAL |
|---:|---:|---:|---:|---:|---:|
| 0 | 0.503991 | 0.578981 | 0.581270 | 0.565360 | 0.590748 |
| 1 | 0.312618 | 0.345859 | 0.417130 | 0.419523 | 0.418909 |
| 2 | 0.412763 | 0.456210 | 0.502650 | 0.526425 | 0.505040 |

| Comparator | Mean H1−control | Wins | Gate |
|---|---:|---:|---|
| B0_BASELINE | +0.095109 | 3/3 | PASS |
| C1_HISTOGRAM | +0.044550 | 3/3 | PASS |
| C2_SIZE_SHUFFLE | +0.004549 | 3/3 | NOT REQUIRED: LOW SHUFFLE POWER |
| C3_PARAM_MATCHED | +0.001130 | 1/3 | FAIL |

### Pubmed
Dataset gate passed: True; shuffle adequate: False.

| Seed | B0 | Histogram | Size-shuffle | Parameter-matched | HSPE-REAL |
|---:|---:|---:|---:|---:|---:|
| 0 | 0.826532 | 0.838077 | 0.831056 | 0.766686 | 0.837051 |
| 1 | 0.732855 | 0.770530 | 0.772223 | 0.783949 | 0.770811 |
| 2 | 0.672499 | 0.759216 | 0.759438 | 0.708499 | 0.770896 |

| Comparator | Mean H1−control | Wins | Gate |
|---|---:|---:|---|
| B0_BASELINE | +0.048957 | 3/3 | PASS |
| C1_HISTOGRAM | +0.003645 | 2/3 | PASS |
| C2_SIZE_SHUFFLE | +0.005347 | 2/3 | NOT REQUIRED: LOW SHUFFLE POWER |
| C3_PARAM_MATCHED | +0.039875 | 2/3 | PASS |

## Cora/PubMed 10E × 3 seeds

Pending.

## Novelty and test

Novelty: PENDING_BEFORE_TEST.
Test: OFF_EARLY_REJECT.

## Artifacts

Per-seed results, control deltas, shuffle audit, code/cache hashes, and reuse provenance are in `results.json` and `experiments/`. Logs are in `logs/`.
