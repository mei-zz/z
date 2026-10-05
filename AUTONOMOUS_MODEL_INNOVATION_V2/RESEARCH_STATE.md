# Autonomous Model-Structure Innovation Search V2

## Current state

- Status: `FOUND_PROMISING_INNOVATION`
- Current stage: `DEEPENING_MODE`
- Current candidate: `V2-002 Cross-Depth Pair Tensor Decoder (CDPT)`
- Current family revision: `0/2`
- Dataset available for executable validation: Cora HeaRT seed 0--4 on the audited remote environment.
- Parent: the repository's native DCDLP implementation with target-pair edge masking.
- Selection policy: no test-label-driven idea selection; validation is used only after the candidate protocol is locked.

## Inherited evidence

The previous `AUTONOMOUS_LP_RESEARCH` loop stopped with `NO_EXECUTABLE_IDEA_AFTER_EXHAUSTIVE_SEARCH`. Its feature families and all prior failure artifacts remain authoritative. V2 must not retry degree/CN disentanglement, variance/confidence, CN second moments, soft gates, CECG/L3, degree-shell roles, block-cut, non-backtracking, exclusive-neighborhood matching/expansion/cohesion, neighbor alignment, fixed spectral bands, vertex-disjoint paths, or community-boundary profiles.

The inherited evidence points to a structural limitation rather than a missing scalar statistic: DCDLP computes candidate-independent node states and only introduces pair interaction after the encoder. The V2 search evaluated changes to interaction timing, pair-conditioned message transport, and cross-depth structural computation. CDPT passed the locked three-seed gate on the available Cora HeaRT benchmark; broad search is now closed.

## Decision gates

1. Static audit: parameter delta, asymptotic and measured memory/latency, leakage, exchange symmetry, parent-equivalence and collapse tests.
2. Researcher/Critic/Experimentalist/Judge record before implementation.
3. Stage 1: minimal parent-versus-candidate implementation with shuffled and simple-proxy controls.
4. Stage 2: one dataset, one seed, short training. Kill unless the locked criterion is met.
5. Stage 3: three seeds; require mean ΔMRR > 0, at least two seed improvements, and no systematic Hits decline.

## Stop policy

The search reached `FOUND_PROMISING_INNOVATION` after Stage 3 and controls passed. Deepening is limited to mechanism ablations, reproducibility checks, and broader-data validation; no optimizer/depth/width rescue is authorized. The result is promising but not yet a claim of general benchmark superiority because only Cora HeaRT was executable in this environment.
