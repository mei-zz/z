# V6.2 CODNS Final Report

STATUS: EXECUTED

PROTOCOL: STRICT_TRAIN_ONLY

CHECKPOINT_RULE: FIXED_EPOCH_10

CANDIDATE: Cross-Order Disagreement Negative Sampling (CODNS), λ=0.5

MECHANISM_SUPPORTED: **NO**

M1−M3 = -0.001412 (2/3 seed wins); M1−M4 = -0.002760 (1/3).

| Arm | Validation MRR mean ± sample SD | Seed 0, 1, 2 |
|---|---:|---|
| M0 | 0.454120 ± 0.109871 | 0.532759, 0.328583, 0.501019 |
| M1 | 0.454988 ± 0.116133 | 0.533261, 0.321555, 0.510147 |
| M2 | 0.459226 ± 0.112204 | 0.536393, 0.330511, 0.510775 |
| M3 | 0.456400 ± 0.105395 | 0.532440, 0.336090, 0.500670 |
| M4 | 0.457747 ± 0.111084 | 0.537036, 0.330783, 0.505422 |

CODNS: **NOT RUN**

TEST: **NOT RUN**

SECOND_DATASET: **NOT RUN**

NOVELTY_STATUS: EXACT_RULE_UNVERIFIED

DECISION: **DISAGREEMENT_MECHANISM_NOT_SUPPORTED**

FAILURE_REASON: The pre-registered M1 comparisons did not pass both seed-win and positive-mean gates under Graph-hardness matching.

STRUCTURAL_CHARACTERIZATION: see [03_STRUCTURAL_CHARACTERIZATION.md](03_STRUCTURAL_CHARACTERIZATION.md)

EFFICIENCY: see [04_EFFICIENCY.md](04_EFFICIENCY.md)

PAPER_CORE_INNOVATION: CODNS remains a candidate only if the mechanism and CODNS gates pass; no false-negative claim is made.

NEXT_EXPECTED_STEP: Report the matched mechanism result first. If unsupported, stop this line; if supported, retain λ=0.5 and interpret CODNS/test/cross-dataset outcomes without tuning.
