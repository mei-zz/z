# CDPT Deepening V3 — Next Research Decision

## Judge status

**WEAK_SIGNAL**

This is not `CONFIRMED_PROMISING`: Cora's parameter-matched Late-only decoder has higher mean test MRR than CDPT, the fixed random operator has the highest Cora validation MRR delta, and CiteSeer gives CDPT an MRR lead but a small Hits@10 loss to Late-only. It is not `MECHANISM_REJECTED` because CDPT remains active and improves MRR over Parent on both datasets, and CiteSeer provides independent positive MRR evidence. It is not `INCONCLUSIVE` because the core protocol, controls, five Cora seeds, and one independent dataset are available; the remaining uncertainty is scientific evidence strength rather than missing execution.

## Researcher / Critic / Judge

### Researcher

CDPT is correctly implemented, has nonzero gradients and score contribution, improves validation MRR over Parent on all five Cora seeds, and improves independent CiteSeer test MRR over Parent and Late-only.

### Critic

The same Cora improvement is largely reproducible by a late-only parameter-matched decoder and a fixed random operator. The Cora test advantage over Parent is smaller and less stable than the validation story, and the V2 promotion used test metrics. The legacy shuffle is pair-alignment corruption rather than pure depth-order randomization, and its CiteSeer effect reverses direction. CiteSeer is only one seed and does not include B4.

### Judge

The evidence supports continued **verification**, not continued **structure expansion**. CDPT is worth a limited follow-up only if the goal is to settle attribution; it is not yet worth investing in attention/gating/loss/width variants or presenting the mechanism as established innovation.

## Decision

1. Stop the autonomous model-structure search at CDPT V3.
2. Do not implement a new CDPT V3 architecture from the current evidence.
3. Preserve the original CDPT, all five Cora seeds, CiteSeer seed 0, controls, checkpoints, hashes, and failures.
4. If one cheap falsification experiment is funded, implement a **true depth-order permutation** control that swaps the two encoder-depth pair states while preserving candidate-pair identity. Run it on Cora seed 0 under the already locked checkpoint protocol. This is a diagnostic of the remaining hypothesis, not a new candidate.
5. Only reopen structure design if a preregistered multi-seed, multi-dataset comparison shows CDPT beating both Late-only and fixed-random controls on the primary metric with the same budget.

## Falsifiable next hypothesis

“CDPT's gain requires the semantic correspondence between early and late pair states, not merely an additional quadratic score term.”

The cheapest falsifier is the true depth-order permutation control above. If it performs comparably to aligned CDPT, the cross-depth semantic interpretation should be rejected. If it collapses while B2 and B4 remain weaker on repeated independent data, the mechanism would become more credible—but still would not by itself establish publication-level novelty.

