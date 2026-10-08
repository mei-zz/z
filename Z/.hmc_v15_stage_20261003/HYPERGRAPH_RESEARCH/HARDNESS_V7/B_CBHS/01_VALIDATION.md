# B — Concentration-balanced hard sampling (CBHS)

- Fixed rule: lambda = 0.1; greedy endpoint-frequency penalty within the Graph-teacher top-2 prepool.
- Validation, 10 epochs, seeds 0/1/2: B4 wins against B0 Graph-hard in 0/3 seeds and against B3 shuffled concentration in 1/3. Mean hardness percentile remains 1.000 (drop 0.000); endpoint Gini is unchanged at 0.656295.
- Registered gate: **NO-GO**. The method neither reduces endpoint concentration nor improves the required validation comparisons.

The C candidate is not run because the pre-registered C gate requires both A and B to pass. See results.json for per-seed selection statistics and validation values.