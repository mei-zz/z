# V6.1 Final Report

STATUS: COMPLETE
STRICT_PROTOCOL: PASS

FILTERED_RESULTS:
- A1: 0.482796 ± 0.074947
- A3: 0.503866 ± 0.067535
- A4: 0.526094 ± 0.041756

STRICT_RESULTS:
- A1: 0.454154 ± 0.109893
- A3: 0.470656 ± 0.095036
- A4: 0.504955 ± 0.076752

VALIDATION_MEAN_STD:
- A1: 0.454154 ± 0.109893
- A3: 0.470656 ± 0.095036
- A4: 0.504955 ± 0.076752

TEST_MEAN_STD:
- A1: 0.472810 ± 0.093835
- A3: 0.490064 ± 0.093377
- A4: 0.527433 ± 0.070396

TRUE_VETO_FUTURE_POSITIVE_RATE: 0.00155971
SHUFFLED_VETO_FUTURE_POSITIVE_RATE: 0.00074272
RANDOM_VETO_FUTURE_POSITIVE_RATE: 0.00103981
ENRICHMENT_RATIO: 1.7500000000000002
ODDS_RATIO: true-vs-shuffled 1.95812; true-vs-random 1.45237
HG_PERCENTILE_MONOTONICITY: True
STRICT_MECHANISM_SIGNAL: YES
MECHANISM_SUPPORTED: NO
PERFORMANCE_SUPPORTED: YES
EFFICIENCY: cached selection 0.1975s total / 0.019751s per epoch; cold teacher scoring Graph 16.3319s, Raw-HG 21.1123s.
FINAL_DECISION: NO_MECHANISM

NEXT_EXPECTED_STEP: Stop the false-negative mechanism claim; retain any test performance result separately and require a pre-registered, adequately powered independent mechanism replication before a new method design. Do not tune from this test set.

A4 meets the predeclared test performance gate, but the requested false-negative mechanism is not statistically confirmed; report these as separate findings.

Interpretation is restricted to the measured Cora standard split and frozen V6 rule. Novelty status remains EXACT_RULE_UNVERIFIED.
