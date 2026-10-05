# Candidate A — ARHC falsification

## Decision

**REJECT.** Candidate A did not reach GO. Test scoring was never run. Since A3 was not the best F1 arm, the preregistered A4 shuffled-anchor run was skipped. Candidate B was then started.

## Protocol

Cora, standard split, seed 0, uniform training negatives, 20 evaluation negatives per positive, A5 decoder/branches, hidden dimension 16, branch dimension 8, 2 layers, dropout 0, batch size 4096, V100 / `mei_env`. F0 used 1 epoch and F1 used 5 epochs. Every stage reran Raw at the same epoch budget. `evaluate_test=false` for all runs. F1 selection used the best validation checkpoint and validation MRR only.

## Validation results

| Arm | Operator | F0 best val MRR | F1 epoch curve (val MRR) | F1 best val MRR |
|---|---|---:|---|---:|
| A0 | Raw global hypergraph | 0.162793 | 0.162793, 0.287014, 0.399852, 0.463626, 0.487678 | **0.487678** |
| A1 | Parameter-matched symmetric branch | 0.164558 | 0.164558, 0.286976, 0.400191, 0.463380, 0.487579 | 0.487579 |
| A2 | Anchor/member split, symmetric return | 0.162603 | 0.162603, 0.286933, 0.399513, 0.463669, 0.487406 | 0.487406 |
| A3 | Full role-split interaction + separate return | 0.164557 | 0.164557, 0.287164, 0.400040, 0.463421, 0.487407 | 0.487407 |

F0 passed the fast screen because A3 was not more than 0.005 below A0. In F1, A3 was 0.000271 below A0, and A2 was 0.000272 below A0. Neither A3 nor the role-only fallback exceeded Raw and the matched control by the required +0.003 absolute or +2% relative. A1's F0 lift did not persist in F1 and the symmetric branch does not encode anchor identity.

## Cost and mechanism

At hidden dimension 16 the shared ARHC branch adds 2,097 trainable parameters, about 8.48% over the 24,735-parameter raw model. F1 training time was 36.3 s for Raw and 39.6 s for A3 (+9.1% in this single run). A3's learned residual gamma was −0.00589. Coverage checks retained every incidence; no target edge was used to build the stars.

Novelty status: broad role-aware hypergraph convolution has prior art (`NOVELTY_CONFLICT`); the specific graph-induced star anchor/member operator remains `NOVELTY_UNVERIFIED`. See `../01_NOVELTY_SEARCH.md`.
