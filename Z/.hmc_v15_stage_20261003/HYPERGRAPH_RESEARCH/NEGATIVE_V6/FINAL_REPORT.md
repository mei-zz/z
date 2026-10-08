# V6 Hypergraph-Verified Graph-Hard Negative Mining — Final Report

**STATUS:** COMPLETE  
**B1_REPRODUCED:** YES  
**FINAL_DECISION:** STRONG_SIGNAL  
**TEST_EVALUATED:** true

## Required summary

| Field | Result |
|---|---:|
| RAW_HG_MRR | 0.5030120048647342 |
| GRAPH_HARD_MRR | 0.5334445819888557 |
| A_HG_VETO | GO |
| B_DISAGREEMENT | NOT_RUN |
| C_CURRICULUM | NOT_RUN |
| BEST_CONTROL | A3: 0.5364482303219076 |
| BEST_CANDIDATE | A4: 0.5404283040301416 |
| ABSOLUTE_GAIN_OVER_GRAPH_HARD | 0.006983722 |
| RELATIVE_GAIN | 1.309175% |
| HARD_TERTILE_GAIN | 0.043061374089290616 |
| SAMPLING_OVERHEAD | {'A1_graph_hard_train_seconds': 74.1820285548456, 'A1_sampling_rule_seconds': 0.06272422010079026, 'A4_sampling_rule_seconds': 0.08052047714591026, 'extra_hypergraph_teacher_score_seconds_once': 15.951832163147628, 'extra_rule_selection_seconds': 0.01779625704512, 'estimated_A4_increment_over_A1_fraction_of_training_time': 0.21527624319933222, 'estimated_A4_increment_over_A1_percent': 21.52762431993322, 'A4_training_seconds': 80.67643470410258, 'peak_gpu_mb_by_diagnostic_arm': {'A0': 43.32763671875, 'A1': 58.29248046875, 'A2': 58.24365234375, 'A3': 58.24951171875, 'A4': 58.20068359375, 'A5': 58.29345703125}, 'definition': "Shared pool generation excluded; B1's Graph teacher score cost is common. Extra Raw-HG teacher scoring plus measured veto-selection delta is compared with B1 training time."} |
| NOVELTY_STATUS | EXACT_RULE_UNVERIFIED |
| GRAPH_HARD_BASELINE_SIGNAL | STRONG |

## Gate outcomes

- B1 stored MRR: 0.5334445819888557; reproduced MRR: 0.5334445819888557; absolute error: 0.0; tolerance: 0.003.
- Candidate A MRR: {"A0": 0.5030120048647342, "A1": 0.5334445819888557, "A2": 0.5355843158758731, "A3": 0.5364482303219076, "A4": 0.5404283040301416, "A5": 0.536054529510456}
- Candidate B MRR: {}
- Candidate C MRR: {}
- Test rule: test was only eligible after the explicit 3-seed Candidate-A STRONG_SIGNAL gate. No validation/test outcomes entered training-negative hardness rankings.

## Three-seed validation confirmation

| Seed | A1 Graph-hard | A3 shuffled veto | A4 true HG veto | A4 − A1 |
|---:|---:|---:|---:|---:|
| 0 | 0.533444582 | 0.536448230 | 0.540428304 | +0.006983722 |
| 1 | 0.396701062 | 0.426216725 | 0.479058784 | +0.082357722 |
| 2 | 0.518241220 | 0.548932135 | 0.558793630 | +0.040552410 |
| Mean | 0.482795621 | 0.503865697 | 0.526093573 | +0.043297951 |

A4 beats A1 on 3/3 seeds; mean gain is +0.043297951. The task's STRONG_SIGNAL validation gate is met. Frozen seed-0 Graph/Raw-HG teachers were reused for seed-1/2 learners.

## Authorized test results

| Arm | Test MRR | AUC | AP |
|---|---:|---:|---:|
| A1 | 0.550403658 | 0.691224719 | 0.425475074 |
| A3 | 0.562830050 | 0.700012962 | 0.420405875 |
| A4 | 0.550651843 | 0.740242287 | 0.413158127 |

Shared test candidate hash: ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92. A4−A1 = +0.000248185; A4−A3 = -0.012178207.

The independent test set ranks A3 above A4. Thus the validation STRONG_SIGNAL gate passed, but the test does not show that true HG veto transfers better than the shuffled-veto control; A4's test MRR is also nearly tied with A1.

## Selected training negatives

Ranks are per-positive percentiles in the fixed training candidate pool. The realized selection statistics are not ground-truth false-negative labels.

| Arm | Mean Rg | Mean Rh | Mean |Rg−Rh| |
|---|---:|---:|---:|
| A1 | 0.9753 | 0.8958 | 0.0921 |
| A2 | 0.9502 | 0.8565 | 0.1111 |
| A3 | 0.9505 | 0.8581 | 0.1100 |
| A4 | 0.9393 | 0.7717 | 0.1720 |
| A5 | 0.9607 | 0.9447 | 0.0473 |

## Efficiency

There were 11 new V6 training runs totaling 816.48s (13.61 min); peak GPU allocation was 58.31 MiB. A0 reused the V5 matched Raw-HG/uniform run (historical training 75.06s) and was not retrained. A4 pure selection rule time was 0.0805s across 10 epochs versus 0.0627s for A1. The additional one-time Raw-HG teacher scoring was 15.95s, estimated at 21.53% of A1's training time. This cold-cache estimate exceeds the <15% efficiency target; reusing the already saved V5 teacher-score pool would remove most of that incremental scoring cost.

## Mechanism readout

For A4, Q1 Graph-high/HG-high negatives beat their paired positive in 32.8% of candidate comparisons and occur on 53.2% of queries; Q2 Graph-high/HG-low rates are 19.1% and 26.2%. The validation hard-Graph-tertile MRR gain over A1 is 0.043061374089290616.

**NEXT_EXPECTED_STEP:** Keep B/C stopped. The task's validation signal was met, but the test ranking favors A3 over A4; analyze this A4–A3 transfer gap before treating HVGH as a reliable improvement.

## Interpretation

Graph-hard is a sampler control. HVGH is not called a false-negative detector: Q1/Q2 analyses are score-rank diagnostics only. The focused novelty review found nearby hard-negative, dynamic-sampling, false-negative-filtering, and hyperedge-prediction work, but no exact rule in the searched sources; priority is unverified.

See 00_B1_AUDIT.md, 01_NOVELTY_SEARCH.md, 02_QUADRANT_ANALYSIS.json, results.json, training_negative_diagnostics.json, and the per-arm configs, curves, hashes, checkpoints, and logs.
