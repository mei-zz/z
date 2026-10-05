# Graph–Hypergraph Complementarity Sprint V5 — Final Report

**STATUS:** EXECUTED  
**FINAL_DECISION:** `NO_TASK_LEVEL_SIGNAL`  
**TEST_EVALUATED:** false  
**SERVER_RUNS:** complete; V100 idle and no V5 runner remains active

## Matched complementarity audit

The Cora standard seed-0 Graph-only and current Raw-HG A5 models used 10 epochs, shared initialization, matching train negatives, the same optimizer/decoder/dimensions, and the same 263 validation positives with 20 negatives each.

| Measure | Result |
|---|---:|
| GRAPH_ONLY_MRR | 0.4960556573 |
| RAW_HYPERGRAPH_MRR | 0.5030120049 |
| ORACLE_MRR | 0.5316997510 |
| ORACLE_GAIN | +0.0286877462 |
| HYPERGRAPH_WIN_RATE | 33.4601% |
| GRAPH_WIN_RATE | 19.3916% |
| HARD_TERTILE_GRAPH_MRR | 0.088809 |
| HARD_TERTILE_HG_MRR | 0.107958 |

The oracle gate passed `STRONG_COMPLEMENTARITY`, so A, B, then C ran in the registered order. This oracle is a diagnostic upper bound; it did not translate into a candidate that passed its matched controls.

## Candidate results

| Candidate/arm | Validation MRR | Decision |
|---|---:|---|
| A1 Current Raw-HG | 0.5030120 | Baseline |
| A2 Uniform residual | 0.5028183 | Control |
| A3 Shuffled difficulty | 0.4938823 | Control |
| A4 GHHR | 0.4935003 | **REJECT**; below A1/A2/A3 |
| B0 Standard uniform Raw-HG | 0.5030120 | Baseline |
| B1 Graph-hard only | 0.5334446 | Highest observed arm, but a control |
| B2 Hypergraph-hard only | 0.5138018 | Control |
| B3 Random matched pool | 0.4982336 | Control |
| B4 Balanced cross-view | 0.5326926 | **REJECT**; 0.0007520 below B1 |
| C0 Graph-only | 0.4960557 | Baseline |
| C1 Raw-HG | 0.5030120 | Baseline |
| C2 Simple average | 0.4962589 | Control |
| C3 Global scalar fusion | 0.4961378 | Control |
| C4 Parameter-matched gate without disagreement | 0.4968151 | Control |
| C5 DAF | 0.4969030 | **REJECT**; −0.0061090 (−1.2145%) vs C1 |

The best observed MRR was B1 Graph-hard-only at 0.5334446 (+0.0304326, +6.0501% vs Raw-HG), but B1 is a required B control, not the B4 candidate. B4 failed the strict requirement to exceed every control, so this is not a winning candidate.

All candidate arms ran 10 epochs on seed 0 and used validation only. The actual trainer samples one training negative per train positive per epoch; the configured 20 negatives are for ranking evaluation. For B, the implementation preserved the audited one-negative training budget and selected from a 20-candidate train-only pool; B4 balanced the three categories across positive links each epoch and rotated assignments across epochs.

## Required final fields

- **A_GHHR:** REJECT
- **B_CVHNM:** REJECT
- **C_DAF:** REJECT
- **WINNING_CANDIDATE:** NONE
- **BEST_VALIDATION_MRR:** 0.5334446 (B1 control; not a winner)
- **ABSOLUTE_GAIN:** +0.0304326 vs Raw-HG for the best observed control; C5 candidate gain was −0.0061090
- **RELATIVE_GAIN:** +6.0501% for the best observed control; C5 candidate relative gain was −1.2145%
- **NOVELTY_STATUS:** `CONCEPTUAL_OVERLAP; EXACT_RULE_UNVERIFIED`
- **FINAL_DECISION:** `NO_TASK_LEVEL_SIGNAL`
- **NEXT_EXPECTED_STEP:** Stop V5. No 3-seed confirmation or test evaluation is authorized because no candidate met GO.

## Verification and artifacts

The server runner completed and exited; test evaluation stayed disabled. C2–C5 checkpoints all passed a load/config round-trip check. Existing default-path regression tests passed: 17 tests across branch shapes, interaction modes, and hypergraph modules. Server-side syntax checks also passed.

Detailed configs, validation curves, scores, sampled-negative/pair hashes, candidate pools, checkpoints, and runner logs are preserved under `A_GHHR/`, `B_CVHNM/`, and `C_DAF/`. The architecture, complementarity, and novelty audits are in `00_ARCHITECTURE_AUDIT.md`, `01_COMPLEMENTARITY_AUDIT.md`, and `02_NOVELTY_SEARCH.md`.
