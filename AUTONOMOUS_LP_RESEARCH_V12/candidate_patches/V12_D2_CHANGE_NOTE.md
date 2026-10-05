# V12-D2 experiment patch note

Implementation is isolated in the V12 experiment runner. The project model source, split, evaluator, training candidate pool, and test files are unchanged.

## Mechanism

For candidate endpoints `(u,v)`, use the already target-masked train-graph neighborhoods and form `A=N(u)\N(v)` and `B=N(v)\N(u)`. Every observed edge between `A` and `B` would close a length-4 cycle if `(u,v)` were added. D2 computes its density:

`cross_density = |E(A,B)| / max(|A||B|, 1)`

and adds a zero-initialized learned scalar times that density to the baseline logit. Its matched control uses the within-side edge density over pairs inside `A` or inside `B`, with the same single scalar and initialization. The feature is built from the training message graph only; for training positives, target edges are removed before neighborhoods are read.

## Registered screen

- `S1H_B0`: QTHS25 + BCE baseline.
- `S1H_D2`: exclusive-neighborhood cross-closure density residual.
- `S1H_D2_WITHIN`: same-parameter within-side density control.
- Cora, seed 0, five epochs; same selected training negatives and validation candidates; test disabled.
- Promotion requires `MRR(D2) − MRR(baseline) ≥ 0.003` or at least 1%, and D2 must beat the control.

The per-run source hash and arm patch IDs are recorded in the Stage 1H JSON.
