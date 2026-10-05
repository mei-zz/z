# Candidate B — Cross-View Hard Negative Mining (CVHNM)

**Status:** rejected on validation. No test candidates were evaluated.

| Arm | Validation MRR | Best epoch |
|---|---:|---:|
| B0 Standard uniform Raw-HG | 0.5030120 | 10 |
| B1 Graph-hard only | 0.5334446 | 6 |
| B2 Hypergraph-hard only | 0.5138018 | 7 |
| B3 Random matched pool | 0.4982336 | 6 |
| B4 Balanced cross-view | 0.5326926 | 7 |

B4 improved over B0 by +0.0296806 (+5.9006%), but it failed the mandatory strict comparison with B1 by 0.0007520. **Decision: `REJECT`; proceed to C.** B1 is a control and cannot be reported as a winning candidate.

## Matched negative budget

The existing trainer draws one uniform training negative per train positive per epoch; its configured 20 negatives are used for ranking evaluation. To preserve the current optimization budget, all B arms train with one selected negative per positive. B1–B4 use a shared pool of 20 training-only candidates per positive. B4 assigns G-hard, H-hard, and joint-hard categories in equal thirds across positive links each epoch, rotating category assignments across epochs so each positive sees all three views.

The pool excludes known positive links through the standard sampler. Matched seed-0 Graph and Raw-HG teacher checkpoints score only the training candidate pool. Validation/test labels were not used for hardness or selection. Pool, score, per-epoch negative hashes, validation curves, configurations, and checkpoints are under `candidate_runs/`.
