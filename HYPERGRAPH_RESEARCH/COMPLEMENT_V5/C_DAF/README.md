# Candidate C — Disagreement-Aware Fusion (DAF)

**Status:** rejected on validation. This was the final registered candidate. No test candidates or three-seed confirmations were run.

| Arm | Validation MRR |
|---|---:|
| C0 Graph-only | 0.4960557 |
| C1 Raw-HG | 0.5030120 |
| C2 Simple average | 0.4962589 |
| C3 Global learned scalar | 0.4961378 |
| C4 Parameter-matched gate without disagreement | 0.4968151 |
| C5 DAF | 0.4969030 |

C5 was 0.0061090 below C1 (−1.2145% relative) and failed the mandatory strict comparisons with C1/C2/C3/C4. **Decision: `REJECT`; final V5 decision is `NO_TASK_LEVEL_SIGNAL`.**

The model expresses the existing Raw-HG score as `s_h`, alongside `s_g` from the same A5 decoder on `node_state`. Fusion is residual: `s_g + a_h(q) * (s_h-s_g)` with an independent sigmoid gate. The Raw-star membership and incidence operator are unchanged.

C5 uses `[s_g, s_h, |s_g-s_h|, margin_g, margin_h]`. Each margin is the candidate score minus the corresponding 90th-percentile score from the seed-matched initial model's train-negative set. The thresholds are computed from train negatives only, saved in the checkpoint config, and reused unchanged for inference. C4 has the same five-input gate parameterization with the disagreement/margin input slots set to zero. C2–C5 used matched Raw-HG initialization, standard train negatives, 10 epochs, seed 0, and validation-only checkpoint selection.

Configs, validation curves, thresholds, checkpoints, runner status, and logs are in `candidate_runs/`. C2–C5 checkpoints passed a load/config round-trip check.
