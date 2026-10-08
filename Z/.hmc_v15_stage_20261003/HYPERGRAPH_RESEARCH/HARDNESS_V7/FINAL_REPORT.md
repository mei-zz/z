# V7 Final Report — Winning-Control Decomposition & Hard-Negative Regularization

## Decision

**STRONG_GO for the registered A4_QTHS25 sampler, with transfer support on Cora and Citeseer validation.** The overall primary diagnostic is `BOTH`: the A1→A3 comparison changes both raw extreme hardness and endpoint diversity, so it does not isolate hardness alone.

## Frozen controls and diagnostics

- V6.1 A1/A3 controls passed the exact split, teacher, candidate-pool, selected-negative, fixed-epoch-10, validation-candidate, and checkpoint audit. Train-only candidate-pool hash: `3d1e3ea691fc19fab65d66ad278d169cf099eb831ad0e46a439510ff5d07a7ba`; split hash: `c5cec7e3bf6eaad41e12ae786246bf454a1bbcd4476286c71eb7e75b0eeba71a`.
- A1 mean validation MRR = 0.454154; A3 shuffled-veto = 0.470656.
- A1→A3 extreme-hard fraction (Rg >= .95) falls from 100% to 50.35% (−49.65 percentage points). But unique endpoint ratio rises 6.13% relative, endpoint Gini falls 0.040123, and hub-endpoint ratio falls 5.23 points. The strict H1 isolation condition (<5% endpoint change) therefore fails; H2 diversity signal passes.
- V6.1's nominal veto ratio is 0.25, while the top-2, K=1 setup removes one candidate per positive (50% of the prepool). QTHS uses deterministic occurrence-level rounding, trimming the top candidate in half of rows.

## Validation gates

| Candidate | Result | Evidence |
|---|---|---|
| A — QTHS | **GO** | A4 mean MRR 0.474662; +0.020509 vs A1; +0.004006 vs shuffled-veto A2; wins vs A1 and A5 in 2/3 seeds each. |
| B — CBHS | **NO-GO** | B4 wins vs B0 in 0/3 and vs B3 in 1/3; mean Rg drop 0; endpoint Gini unchanged at 0.656295. |
| C — STHD | **Not run by gate** | A and B were not both GO. |

A3_BOTTOM25 and A5_MIDDLE25 are exact A1 null controls in the top-2/K=1 setup: deleting easier or middle-ranked items from the full 20-item row does not alter the Graph-hard top-2. They were reused as mathematical controls, not represented as independent samplers or retrains.

## Cora test (opened once after validation freeze)

- Shared V6.1 candidate hash: `ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92`.
- Mean MRR: Graph-hard A1 = 0.472810; shuffled-veto A3 = 0.490064; A4_QTHS25 = 0.493377.
- A4−A1 paired seed deltas: −0.001596, +0.013776, +0.049521 (2/3 wins). A4−A3 deltas: +0.004048, +0.002199, +0.003694 (3/3 wins).
- Both registered support checks passed, opening the second-dataset gate.

## Citeseer transfer validation

No dataset-specific tuning; same QTHS25 rule and fixed epoch-10 checkpoint rule. The seed-0 screen passed, so all three registered seeds were run. Mean validation MRR: Graph-hard = 0.417367 (sample SD 0.106357), Random-veto = 0.411839 (0.102857), Winner = 0.427030 (0.092571). Winner beats Graph-hard in 2/3 seeds and by +0.009663 mean MRR. The transfer gate is **SUPPORTED**. No test-split metrics were evaluated; PubMed was not needed because Citeseer loaded and passed the registered screen. Runtime was Python 3.11 / PyTorch 2.8.0+cu128 / PyG 2.5.3 on a Tesla V100. The project environment declares PyTorch 2.3.1/CUDA 12.1, so exact lockfile parity is not established; all Citeseer comparison arms used the same active runtime.

## Novelty and limitations

The focused search found adjacent work on structural/hard negative sampling for hyperlink prediction, recent hard-negative hyperedge prediction, and multi-level hardness control; it did not identify an exact match for this frozen Graph-teacher per-positive quantile trim in hypergraph link prediction. This is not an exhaustive literature claim. The proposal should be framed as a candidate sampling rule with empirical support, not as the first hard-negative method.

The primary causal limitation is the A1→A3 confounding between hardness and endpoint diversity. QTHS validation and transfer support make the sampling rule promising, but do not prove that the Cora test gain is caused by hardness reduction alone. A follow-up should separate endpoint-diversity control from hardness trim and use a less discrete prepool or K>1.

## Artifact provenance note

The active SSH account did not contain the earlier `/home/ubuntu/lchr_v2` workspace. The Cora V7 `TEST` file was also absent from the local mirror. Its captured aggregate means and paired per-seed deltas were carried forward into `test_results.json` to preserve the already-completed one-time test gate; the raw full Cora per-seed metric table could not be recovered in this session. Citeseer run records, per-seed metrics, checkpoint hashes, and diagnostics were read from the completed current-server run. No Cora test was repeated.