# V12-F3 experiment patch note

Implementation is isolated to the V12 experiment runner; the DCDLP training loop source, negative candidate pool, split, evaluator, and test files remain untouched.

## Mechanism

The sampler assigns one QTHS25 training negative `n_i` to each train positive `p_i`. In each minibatch, define `I_b` as the positive identities for which both `p_i` and their assigned `n_i` appear in that batch. Keep the baseline BCE over every sampled edge and add:

`L_F3 = BCE(all sampled edges) + 0.1 * mean_{i∈I_b} softplus(s(n_i) − s(p_i))`

The control uses the same BCE and pairwise term, but cyclically shifts the assigned negative scores across eligible in-batch positives. Thus it preserves the batch, sampler, compute pattern, and negative score distribution while breaking the positive-specific assignment.

## Registered screen

- `S1G_B0`: QTHS25 + BCE baseline.
- `S1G_F3`: identity-aligned positive/negative pair ranking auxiliary.
- `S1G_F3_SHUFFLE`: cyclic pair-mismatch control.
- Cora, seed 0, five epochs; same one-negative-per-positive selection, fixed validation candidates, test disabled.
- Promotion requires `MRR(F3) − MRR(baseline) ≥ 0.003` or at least 1%, and F3 must beat the mismatch control.

The exact source hash and arm patch IDs are recorded in the stage result JSON.
