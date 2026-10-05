# V13 idea ledger

## V12 evidence re-audit

- Reconciled all 44 completed V12 jobs against result archives and their frozen contexts; 39/40 Phase-1 Stage-1 equivalents were consumed. No confirmed Innovation 1; Innovation 2 remained unsearched; the test set was not evaluated.
- Five control-derived primitives and four candidate-below-control failures are listed with exact rows in `00_V12_SIGNAL_AUDIT.md` and `CONTROL_SIGNAL_LEDGER.md`.
- Unchanged V12 lineages remain blacklisted.

## Phase A: Evidence-Calibrated Residual (ECR)

NEW_INFORMATION: combine a 24-dimensional pair-specific Raw-HG representation, separately standardized degree/CN evidence, target-masked cross-neighborhood density, and one Raw-HG × structure interaction.

NEW_PRINCIPLE: a zero-initialized, low-capacity additive residual calibrates the base pair logit from distinct, target-masked evidence channels. It tests whether the weak V12 signals compose beyond the best single component and a same-capacity pair-shuffled mechanism control.

Registered arms: A0 QTHS25 baseline; A1 Raw-HG only; A2 degree/CN only; A3 cross-density only; A4 shuffled evidence; A5 full ECR. Actual A5 parameter increase: 28 trainable parameters (0.1132% of baseline), with the Raw-HG branch dimension fixed to 8 (24 evidence coefficients).

Phase A result: `ECR_STAGE1_GO`. A5 MRR 0.607815 vs baseline 0.525620, best single 0.575181, and shuffled control 0.486030. Five actual epochs; all six arms share the frozen Cora split, pool, validation candidates, seed 0, QTHS25 sample hash and source hashes. Test disabled. This is a strong Stage-1 signal only, not a confirmed innovation. Proceed to a predeclared 10-epoch Stage 2 confirmation after the preliminary novelty screen.

## Candidate B: factorized pair calibration

This fallback combines a learned semantic Raw-HG pair scalar with train-only structure via direct multiplicative interaction. Run only if ECR fails its registered gate. Phase A passed, so this candidate is not run.

## Phase B / Innovation 2 search

After Innovation 1 validation, explore mechanisms from distinct families under the V13 budget and controls:

1. T — same-negative hardness persistence across teacher epochs 1–10; compare final-hard, mean-rank, trajectory-shuffle, final-rank-matched, SH75 and QTHS25.
2. L — differentiable expected reciprocal-rank objective on the frozen 20-candidate set; control independent BCE, generic listwise and repeated K=1 BCE.
3. P — symmetric pair-state decoder from endpoint difference, Hadamard product and train-only structure; include generic and linear decoder controls.
4. V — high-confidence Graph/Raw-HG pair-margin consistency; compare shuffled-margin, mean-score and feature-level controls.
5. S — edge-centric pair-context message passing only after T/L/P/V fail to enter Stage 2.

Each candidate has a single mechanism and predeclared controls, at most four independent candidates plus one targeted revision per family, and is charged against the 50 Stage-1-equivalent Phase-B budget. No broad micro-tweak batch.
