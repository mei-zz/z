# Candidate A — Graph-Hard Hypergraph Residual Learning (GHHR)

**Status:** rejected on validation; Candidate B is authorized next. No test candidates were evaluated.

All arms used 10 epochs, seed 0, the matched Cora standard split, the same per-epoch uniform training negatives, and shared Raw-HG initialization. A2/A3/A4 also used identical positive-negative pairing order.

| Arm | Validation MRR | Best epoch |
|---|---:|---:|
| A1 Current Raw-HG | 0.5030120 | 10 |
| A2 Uniform residual | 0.5028183 | 10 |
| A3 Shuffled difficulty | 0.4938823 | 10 |
| A4 True Graph-hard GHHR | 0.4935003 | 10 |

A4 is 0.0095117 below A1 (−1.8909% relative), and fails the required strict comparisons against A1/A2/A3. **Decision: `REJECT`; proceed to B, skip confirmation, and keep C gated on B.** The beta scalar moved from 1 to 1.00658 in the best A4 checkpoint; that change did not translate to a validation gain.

The server-side candidate curves, per-epoch margins/difficulty values and hashes, model checkpoints, and run configs are under `candidate_runs/`. The baseline shared candidate evidence remains under `remote_evidence/baseline_10_epoch/`.
