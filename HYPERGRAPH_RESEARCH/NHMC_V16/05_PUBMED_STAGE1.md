# PubMed Stage 1 transfer

**State: COMPLETE — `NHMC_STAGE1_REJECT`.** Seed 0, five epochs, validation only, Tesla V100. Validation used 2,216 positives × 20 fixed candidates. Test evaluation was OFF.

All six arms used the same train-pool hash, QTHS25 selected-negative hash, and validation-candidate hash. The train-side shuffle power was 0.4396 (adequate), so the strict H1–C2 margin was active. Validation shuffle power was 0.0887.

| Arm | Validation MRR | Hits@10 |
|---|---:|---:|
| B0_BASELINE | 0.826532 | 0.988718 |
| B1_HRA | 0.826108 | 0.988267 |
| B2_NATIVE_SCALAR | 0.832276 | 0.987365 |
| C1_NHMC_SIZE | 0.837051 | 0.986462 |
| C2_NHMC_SHUFFLE | 0.838108 | 0.985108 |
| H1_NHMC_REAL | **0.833945** | **0.986011** |

| Promotion comparison | Required | H1 minus control | Result |
|---|---:|---:|---|
| H1 − B0 | ≥ 0.003 | +0.007412 | Pass |
| H1 − B1 | ≥ 0.002 | +0.007837 | Pass |
| H1 − B2 | ≥ 0.002 | +0.001668 | Fail |
| H1 − C1 SIZE | ≥ 0.002 | −0.003106 | Fail |
| H1 − C2 SHUFFLE | ≥ 0.002 | −0.004163 | Fail |

H1 adds 75 trainable parameters (0.7648% of the 9,807-parameter baseline), within the 2% cap. H1 training time was 789.1 s. The run completed with no test scoring.

**Interpretation:** PubMed Stage 1 fails the frozen promotion gate. NHMC-REAL beats B0 and HRA, but does not meet the required margin over Native Scalar and trails both SIZE-only and the correctly shuffled control. Since PubMed had token variation and was suitable for transfer, this is a transfer failure rather than a fallback-dataset condition. No rescue, Stage 2, or multi-seed run was triggered by this result.

Artifacts: `experiments/stage1_pubmed/results.json`, the six per-arm JSON files, `diagnostics/stage1_pubmed_status.json`, and H1 arm diagnostics are copied locally. The raw result records `test_evaluated: false`.