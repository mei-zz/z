# Attempt 003 — Literature audit

Working name: Non-Backtracking Continuation Profile (NBCP)

## New object

For a candidate pair `(u,v)`, enumerate legal non-backtracking `u-a-b-c-v` continuations and retain the distribution of how many legal completions each intermediate state offers. This keeps continuation concentration/dispersion instead of only the total L4 count.

## Novelty-kill result

- Exact/synonym queries covered non-backtracking link prediction, Hashimoto link prediction, non-backtracking paths, continuation profiles, and the same terms in KGE/recommender/graph classification/matching.
- Strong neighboring work: non-backtracking operators and line-graph models, WalkPool, NBFNet/path reasoning, MPLP and existing Local Path/L3 controls.
- Collision: `L1/L2`; non-backtracking walks are a known primitive, so this candidate is retained only as a cheap incremental probe of a specific continuation-distribution object. It cannot be described as a new non-backtracking operator or line-graph architecture.
- In this round’s search scope, no complete isomorphic link-prediction method using this exact continuation profile was found.
