# V8 Protocol Unit Tests

## Result

Both fixed datasets passed all ten adapter checks. The tests were run remotely in `mei_env` and the JSON artifacts are:

- `raw/v8_adapter_tests_2_1.json`
- `raw/v8_adapter_tests_2_4.json`

| # | Check | A | B |
|---:|---|---:|---:|
| 1 | Node count and feature dimension | PASS | PASS |
| 2 | Message-graph edge set and shape match official data | PASS | PASS |
| 3 | All train positives retained in message graph | PASS | PASS |
| 4 | Validation/test positives absent from message graph | PASS | PASS |
| 5 | Target mask removes both directions | PASS | PASS |
| 6 | Non-target context edges are retained | PASS | PASS |
| 7 | Positive candidate order is unchanged | PASS | PASS |
| 8 | Negative grouping and order are unchanged | PASS | PASS |
| 9 | Official tensor/file hashes match | PASS | PASS |
| 10 | Training view exposes no held-out labels | PASS | PASS |

The initial B hash-check failure was a typo in the expected literal in the test (`...9400e`); the actual official hash was `...940e`. After correcting the test literal, B passed 10/10. No data file was modified.

## Target-mask checks

The unit test constructs a directed edge list containing both `(u,v)` and `(v,u)`, masks the unordered target pair, and verifies that both disappear. A separate context edge remains. This directly tests the masking operation rather than inferring it from a metric.

## Optimized decoder equivalence

`raw/v8_dcdlp_fast_equivalence.json` records a 512-pair comparison between the direct neighbor-set decoder and the sparse cached implementation:

| Output | max absolute error |
|---|---:|
| logit | `5.96e-7` |
| degree score | `0` |
| CN score | `4.32e-7` |
| residual score | `3.58e-7` |
| interaction score | `4.47e-8` |
| raw CN | `0` |

The optimized path is therefore accepted as a computational optimization, not a changed model.

## Smoke checks

A seed-1, 512-pair training smoke completed with finite loss (`0.6844` in the retained smoke artifact), finite gradients, output shape `[512]`, and approximately `3.34 GB` peak GPU memory. Formal DCDLP runs also recorded finite losses, validation metrics, prediction files, checkpoint hashes, runtime, and CUDA peak memory.

## What the tests do not prove

They prove protocol and implementation invariants, not model superiority. Official duplicate candidates and possible false negatives are intentionally retained. The official GCN and DCDLP still differ in target masking and training-negative sampling, which is reported in `MULTI_SEED_BASELINES.md` rather than hidden by the tests.
