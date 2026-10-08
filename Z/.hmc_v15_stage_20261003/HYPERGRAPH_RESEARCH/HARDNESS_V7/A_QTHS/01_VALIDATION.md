# A — Quantile-trimmed hard sampling (QTHS)

- Fixed rule: alpha = 0.25 over candidate occurrences, using a Graph-teacher top-2 prepool. With K=1 and discrete rows, the rule deterministically trims the top-ranked item in 2,244 of 4,488 rows; the retained negative is the runner-up in those rows.
- Validation, 10 epochs, seeds 0/1/2: A4_QTHS25 mean MRR = 0.474662; A1 Graph-hard = 0.454154; delta = +0.020509. A4 beats A1 in 2/3 seeds and A5 in 2/3 seeds. A4 exceeds the A2 shuffled-veto control by +0.004006 mean MRR.
- Registered gate: **GO**. The validated winner is A4_QTHS25.

## Degenerate controls

A3_BOTTOM25 removes the easiest quarter of each 20-candidate row before selecting from the top-2 prepool. A5_MIDDLE25 removes the middle quarter. Neither deletion touches the top-2 candidates, so both controls are exactly equivalent to A1 Graph-hard under this prepool/K=1 setup. They were reused as mathematical null controls; they are not independent samplers or independent retrains. This discrete-pool limitation should be addressed in any follow-up experiment.

The nominal alpha is not a per-positive 25% trim: for a two-item prepool, exact per-row trimming is impossible. The occurrence-level rounding above realizes a 50% row trim and matches the selected-rank mixture of the shuffled-veto control.