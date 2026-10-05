# Final Research Decision

## Decision

**NO_SUPPORTED_INNOVATION_FOUND**

## Direct answers

- **What was found?** A stable Cora HeaRT Parent failure: HL/LL train-observable subgroups have very low MRR across seeds 0–2.
- **What explains it?** Existing AA/RA and feature-similarity proxies explain substantial ranking signal. Parent validation MRR mean was 0.09959; fixed AA was 0.13417 and fixed CN was 0.11612.
- **Was real training completed?** Yes. Parent A5 was trained remotely for seeds 0, 1 and 2. No new architecture was trained because no candidate passed the collision/proxy gate.
- **Were all three scenarios completed?** No. C was executable and audited. A and B were feasibility-audited but not run because compatible public data/protocols were unavailable remotely; a CoraFull download stalled and was interrupted. This limitation is explicitly recorded, not hidden.
- **Was a positive mechanism found?** No.
- **Should CDPT or another failed family be reopened?** No. The V4 mechanism verdict remains unsupported.
- **Should another module be added now?** No. The evidence does not separate a new mechanism from a stronger existing proxy or pair-aware baseline.

## Why this is a meaningful negative result

The audit changed the decision boundary. A stable error subgroup is not automatically a new-architecture opportunity. In this case, simple train-graph statistics and supplied node features already provide competing explanations, while the obvious neural remedies collide with established link-prediction families. Continuing to add modules would repeat the exact failure mode of V1–V5.

## Next permitted research action

The next cycle may resume only after one of the following is made runnable on the remote server:

1. an official or explicitly predeclared incomplete/noisy benchmark with PULL/CORE controls;
2. a node-disjoint inductive benchmark with GraphSAGE/NCN/LEAP controls; or
3. LPShift or an equivalent fixed distribution-shift benchmark with protocol-aligned strong baselines.

Until then, STOP architecture search. Do not call the current Parent weakness an information-theoretic bottleneck, and do not claim SCI novelty or publication readiness.

## Evidence files

- [`HISTORY_FAILURE_MAP.md`](HISTORY_FAILURE_MAP.md)
- [`PROBLEM_GAP_AUDIT.md`](PROBLEM_GAP_AUDIT.md)
- [`BASELINE_FAILURE_EVIDENCE.md`](BASELINE_FAILURE_EVIDENCE.md)
- [`LITERATURE_COLLISION.md`](LITERATURE_COLLISION.md)
- [`CANDIDATE_LEDGER.md`](CANDIDATE_LEDGER.md)
- [`EXPERIMENT_LEDGER.md`](EXPERIMENT_LEDGER.md)
- [`FAILURE_ANALYSIS.md`](FAILURE_ANALYSIS.md)
- [`BEST_SUPPORTED_CANDIDATE.md`](BEST_SUPPORTED_CANDIDATE.md)
