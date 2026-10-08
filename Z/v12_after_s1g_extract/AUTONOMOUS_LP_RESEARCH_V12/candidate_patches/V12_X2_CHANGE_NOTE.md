# V12-X2 experiment patch note

Candidate implementation is isolated in `AUTONOMOUS_LP_RESEARCH_V12/run_v12.py`; no project model, split, evaluator, candidate pool, or test artifact is edited.

## Mechanism

Let `g(e)` and `h(e)` be the concatenated degree, common-neighbor, and residual branch representations for the same queried edge `e`, computed by the existing Graph-only and Raw-HG model states. X2 appends a zero-initialized scalar residual head to the frozen baseline logit:

`r(e) = MLP([g(e) ⊙ h(e), |g(e) − h(e)|])`

The matched control substitutes the cross-view product with the within-view self moment:

`r_self(e) = MLP([0.5(g(e)² + h(e)²), |g(e) − h(e)|])`

Both heads have identical dimensions, parameter count, initialization, training data, sampler, epoch count, and evaluator. Only the multiplicative same-edge cross-view term differs.

## Registered screen

- `S1E_B0`: QTHS25 + BCE baseline.
- `S1E_X2`: bilinear same-edge cross-view residual.
- `S1E_X2_SELF`: parameter-matched self-moment mechanism control.
- Cora, seed 0, five epochs, fixed validation candidates; test remains disabled.
- Promotion requires `MRR(X2) − MRR(baseline) ≥ 0.003` or at least 1%, and X2 must exceed the self-moment control.

The executable source hash and per-arm patch IDs are recorded in the result JSON after the screen.
