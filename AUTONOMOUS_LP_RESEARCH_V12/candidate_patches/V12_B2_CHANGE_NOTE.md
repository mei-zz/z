# V12-B2 experiment patch note

Implementation is isolated in `AUTONOMOUS_LP_RESEARCH_V12/run_v12.py`. It does not edit the core DCDLP source, split, evaluator, negative pool, or test artifacts.

## Mechanism

The current decoder adds a degree/common-neighbor interaction but scores the residual branch additively. B2 adds two scalar-weighted pair interactions:

`s_B2(e) = s_base(e) + a <z_degree(e), z_residual(e)> / sqrt(d) + b <z_cn(e), z_residual(e)> / sqrt(d)`

The coefficients `a,b` start at zero, preserving the baseline logit at initialization. The control adds the same two trainable scalars as offsets to degree and common-neighbor branch score calibration, without cross-branch products.

## Registered screen

- `S1F_B0`: QTHS25 + BCE baseline.
- `S1F_B2`: residual/structural branch bilinear coactivation.
- `S1F_B2_SCALE`: two-scalar branch-score calibration control.
- Cora, seed 0, five epochs, fixed validation candidates; test remains disabled.
- Promotion requires `MRR(B2) − MRR(baseline) ≥ 0.003` or at least 1%, and B2 must exceed the matched calibration control.

The exact runner source hash and per-arm patch IDs are stored in the result JSON.
