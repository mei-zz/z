# Candidate C — ARPM falsification

## Decision

**REJECT.** C3 did not exceed the raw, PMHE, or anchor-conditioned mean controls and did not reach the absolute or relative gain threshold. The optional C4 shuffled-anchor diagnostic was run because server compute was available; it does not change the primary rejection. Test evaluation was not run.

## Protocol and operator

Cora, standard split, seed 0, A5, uniform training negatives, 20 evaluation negatives per positive, hidden dimension 16, branch dimension 8, 2 layers, dropout 0, batch size 4096. F0 used 1 epoch and F1 used 5 epochs, with each stage rerunning Raw. C3 computes the exact pair moment over the star members excluding its anchor, conditions the moment on the anchor, and returns a residual with zero-initialized gamma. All screening runs set `evaluate_test=false`.

## Results

| Arm | Definition | F0 best val MRR | F1 best val MRR |
|---|---|---:|---:|
| C0 | Raw global hypergraph | 0.162793 | **0.487678** |
| C1 | PMHE pair-moment control | 0.164560 | 0.487705 |
| C2 | Anchor-conditioned member mean | 0.162636 | 0.487655 |
| C3 | Anchor-conditioned member pair moment | 0.164546 | 0.487629 |
| C4 | Shuffled-anchor ARPM diagnostic | — | 0.487465 |

C3 was −0.000048 MRR vs Raw, −0.000075 vs C1, and −0.000026 vs C2. It fails both the primary ordering condition and the +0.003 / +2% effect threshold. The optional C4 score was 0.000164 below C3, which is consistent with a small true-anchor contribution relative to the shuffled diagnostic, but the absolute performance remains below all required primary comparators.

Added parameters: **1,073** (4.34% over the 24,735-parameter raw model). F1 training time: Raw 36.7 s; C3 39.3 s (+7.1%); supplemental C4 35.7 s. C3 learned `gamma = −0.00993`. No test metrics were computed.

Novelty status: broad anchor-/position-conditioned hypergraph link prediction has prior work (`NOVELTY_CONFLICT`); this exact star-anchor-conditioned moment remains `NOVELTY_UNVERIFIED`. See `../01_NOVELTY_SEARCH.md`.
