# V12 signal audit for V13

Source of truth: V12 EXPERIMENT_LEDGER.tsv, checked against results.json, status.json, BEST_STATE.md, BLACKLIST.md, and final report. The ledger contains 44 completed training jobs. The ledger-reported four-decimal MRRs are not substituted for source values.

The first V12 batch used SH75 and had a weaker reference MRR (0.484076); those runs are marked as context-shifted and are not V13 QTHS25 comparisons. Subsequent registered QTHS25 runs use the frozen Cora split, train pool, and validation candidates. All V12 jobs report test disabled.

| Job | Arm | Family | Data / seed / epochs | MRR | Δ vs row baseline | Matched-control MRR | Params | Runtime (s) | Mechanism / interpretation | Context |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|
| V12-S1-01 | B0 | baseline | cora / 0 / 5 | 0.484076 | 0.000000 | 0.484076 | 24735 | 34.16 | SH75 plus BCE matched reference | SH75; context-shifted |
| V12-S1-02 | F1 | F | cora / 0 / 5 | 0.493564 | +0.009488 | 0.485650 | 24735 | 109.41 | Softplus ranking of positives against batch-top ten SH75 negatives | SH75; context-shifted |
| V12-S1-03 | F1 | F | cora / 0 / 5 | 0.485650 | +0.001574 | 0.485650 | 24735 | 112.80 | Softplus ranking of positives against random ten SH75 negatives | SH75; context-shifted |
| V12-S1-06 | C1 | B/C | cora / 0 / 5 | 0.432113 | -0.051963 | 0.437779 | 25136 | 113.21 | Symmetric endpoint product MLP residual | see source notes; non-QTHS25 |
| V12-S1-07 | C1 | B/C | cora / 0 / 5 | 0.437779 | -0.046297 | 0.437779 | 25136 | 117.19 | Same-size MLP using endpoint self-moments | see source notes; non-QTHS25 |
| V12-S1-04 | G1 | G | cora / 0 / 5 | 0.485708 | +0.001632 | 0.482967 | 24735 | 124.60 | Train-only positive closure-rank weights | see source notes; non-QTHS25 |
| V12-S1-05 | G1 | G | cora / 0 / 5 | 0.482967 | -0.001109 | 0.482967 | 24735 | 126.46 | Same positive weights under a fixed train-positive permutation | see source notes; non-QTHS25 |
| V12-S1-08 | D1 | D | cora / 0 / 5 | 0.497518 | +0.013442 | 0.486826 | 25008 | 52.91 | One-hop target-masked pair-context residual | see source notes; non-QTHS25 |
| V12-S1-09 | D1 | D | cora / 0 / 5 | 0.486826 | +0.002750 | 0.486826 | 25008 | 50.13 | Same residual using fixed node-permuted context | see source notes; non-QTHS25 |
| V12-S2-03 | S2_F1_CTRL | F1 | cora / 0 / 10 | 0.385148 | -0.145114 | 0.385148 | 24735 | 184.69 | Random-ten pairwise loss control | QTHS25 |
| V12-S2-04 | S2_D1 | D1 | cora / 0 / 10 | 0.365654 | -0.164609 | 0.521947 | 25008 | 185.91 | Target-masked one-hop ego-context residual | QTHS25 |
| V12-S2-05 | S2_D1_CTRL | D1 | cora / 0 / 10 | 0.521947 | -0.008316 | 0.521947 | 25008 | 186.65 | Node-permuted ego-context control | QTHS25 |
| V12-S2-02 | S2_F1 | F1 | cora / 0 / 10 | 0.235394 | -0.294869 | 0.385148 | 24735 | 186.75 | Batch-top ten pairwise ranking loss | QTHS25 |
| V12-S2-01 | S2_B0 | baseline | cora / 0 / 10 | 0.530263 | 0.000000 | — | 24735 | 188.56 | QTHS25 strong baseline | QTHS25 |
| V12-S1B-03 | S1B_F2_CTRL | F2 | cora / 0 / 5 | 0.515801 | -0.009819 | 0.515801 | 24735 | 96.05 | BCE plus random-ten pairwise auxiliary control | QTHS25 |
| V12-S1B-02 | S1B_F2 | F2 | cora / 0 / 5 | 0.523925 | -0.001696 | 0.515801 | 24735 | 96.19 | BCE-anchored batch-hard pairwise auxiliary loss | QTHS25 |
| V12-S1B-01 | S1B_B0 | baseline | cora / 0 / 5 | 0.525620 | 0.000000 | — | 24735 | 96.26 | QTHS25 plus BCE strong reference | QTHS25 |
| V12-S1B-05 | S1B_H1_CTRL | H1 | cora / 0 / 5 | 0.525116 | -0.000505 | 0.525116 | 24735 | 123.58 | Compute-matched label-stratified shuffled-pair consistency | QTHS25 |
| V12-S1B-04 | S1B_H1 | H1 | cora / 0 / 5 | 0.523719 | -0.001902 | 0.525116 | 24735 | 124.07 | Train-edge-dropout pair-score consistency | QTHS25 |
| V12-S1C-01 | S1C_B0 | baseline | cora / 0 / 5 | 0.525620 | 0.000000 | — | 24735 | 96.68 | QTHS25 plus BCE strong reference | QTHS25 |
| V12-S1C-04 | S1C_X1_RANDOM | X1 | cora / 0 / 5 | 0.525538 | -0.000082 | 0.527652 | 24944 | 132.41 | Same-size residual MLP after fixed random orthogonal rotation | QTHS25 |
| V12-S1C-03 | S1C_X1_RAW | X1 | cora / 0 / 5 | 0.527652 | +0.002032 | 0.527652 | 24944 | 132.59 | Same-size residual MLP on unprojected Raw-HG pair representation | QTHS25 |
| V12-S1C-05 | S1C_X1_CONCAT | X1 | cora / 0 / 5 | 0.524026 | -0.001594 | 0.527652 | 24944 | 132.95 | Same-size residual MLP on fixed-projected Graph/Raw-HG concatenation | QTHS25 |
| V12-S1C-02 | S1C_X1 | X1 | cora / 0 / 5 | 0.523703 | -0.001918 | 0.527652 | 24944 | 135.44 | Orthogonalized Raw-HG pair-representation residual | QTHS25 |
| V12-S1D-01 | S1D_B0 | baseline | cora / 0 / 5 | 0.525620 | 0.000000 | — | 24735 | 84.94 | QTHS25 plus BCE strong reference | QTHS25 |
| V12-S1D-02 | S1D_G2 | G2 | cora / 0 / 5 | 0.525049 | -0.000571 | 0.525135 | 24735 | 88.43 | EMA persistent-positive-difficulty BCE weighting | QTHS25 |
| V12-S1D-03 | S1D_G2_INSTANT | G2 | cora / 0 / 5 | 0.525049 | -0.000571 | 0.525135 | 24735 | 88.51 | Current-batch positive-difficulty weighting | QTHS25 |
| V12-S1D-04 | S1D_G2_SHUFFLE | G2 | cora / 0 / 5 | 0.525135 | -0.000486 | 0.525135 | 24735 | 88.66 | EMA difficulty under fixed positive-edge permutation | QTHS25 |
| V12-S1E-01 | S1E_B0 | baseline | cora / 0 / 5 | 0.525620 | 0.000000 | — | 24735 | 63.62 | QTHS25 plus BCE strong reference | QTHS25 |
| V12-S1E-03 | S1E_X2_SELF | X2 | cora / 0 / 5 | 0.527742 | +0.002122 | 0.527742 | 25136 | 84.41 | Same-parameter residual MLP replacing cross-view product with within-view self moments | QTHS25 |
| V12-S1E-02 | S1E_X2 | X2 | cora / 0 / 5 | 0.527739 | +0.002119 | 0.527742 | 25136 | 87.10 | Zero-initialized residual MLP on aligned Graph/Raw-HG pairwise products plus branch disagreement | QTHS25 |
| V12-S1F-02 | S1F_B2 | B2 | cora / 0 / 5 | 0.526513 | +0.000892 | 0.527789 | 24737 | 63.85 | Zero-initialized residual-branch bilinear coactivation with degree and common-neighbor branches | QTHS25 |
| V12-S1F-01 | S1F_B0 | baseline | cora / 0 / 5 | 0.525620 | 0.000000 | — | 24735 | 64.04 | QTHS25 plus BCE strong reference | QTHS25 |
| V12-S1F-03 | S1F_B2_SCALE | B2 | cora / 0 / 5 | 0.527789 | +0.002169 | 0.527789 | 24737 | 66.29 | Two-scalar degree/common-neighbor score calibration without cross-branch interaction | QTHS25 |
| V12-S1G-02 | S1G_F3 | F | cora / 0 / 5 | 0.506463 | -0.019158 | 0.505986 | 24735 | 63.75 | BCE-anchored pairwise ranking against the QTHS25 negative assigned to the same training positive | QTHS25 |
| V12-S1G-01 | S1G_B0 | baseline | cora / 0 / 5 | 0.525620 | 0.000000 | — | 24735 | 63.83 | QTHS25 plus BCE strong reference | QTHS25 |
| V12-S1G-03 | S1G_F3_SHUFFLE | F | cora / 0 / 5 | 0.505986 | -0.019634 | 0.505986 | 24735 | 66.18 | Same pairwise term with a fixed cyclic mismatch among in-batch assigned negatives | QTHS25 |
| V12-S1H-02 | S1H_D2 | D2 | cora / 0 / 5 | 0.527136 | +0.001515 | 0.524867 | 24736 | 64.93 | Zero-initialized scalar residual from target-masked cross-edge density between exclusive endpoint neighborhoods | QTHS25 |
| V12-S1H-03 | S1H_D2_WITHIN | D2 | cora / 0 / 5 | 0.524867 | -0.000753 | 0.524867 | 24736 | 64.85 | Same-parameter scalar residual from within-side exclusive-neighborhood edge density | QTHS25 |
| V12-S1H-01 | S1H_B0 | baseline | cora / 0 / 5 | 0.525620 | 0.000000 | — | 24735 | 65.89 | QTHS25 plus BCE strong reference | QTHS25 |
| V12-S1I-01 | S1I_D2R | D/E | cora / 0 / 5 | 0.525869 | +0.000249 | 0.527136 | 24736 | 46.17 | Target-masked cross-closure density minus matched within-side neighborhood density | QTHS25 |
| V12-S1I-02 | S1I_D2R_CROSS | D/E | cora / 0 / 5 | 0.527136 | +0.001515 | 0.527136 | 24736 | 48.58 | Raw cross-closure density from the first D2 screen | QTHS25 |
| V12-S1J-02 | S1J_C2_RESCALE | B/C | cora / 0 / 5 | 0.525717 | +0.000097 | 0.525717 | 24736 | 46.87 | Same-parameter scalar recalibration of the learned residual-branch score | QTHS25 |
| V12-S1J-01 | S1J_C2 | B/C | cora / 0 / 5 | 0.526290 | +0.000669 | 0.525717 | 24736 | 48.57 | Zero-initialized scalar residual from cosine similarity of raw endpoint features | QTHS25 |

## Frozen QTHS25 reference

- Cora, seed 0, Raw-HG DCDLP, QTHS25, BCE, fixed epoch 5: MRR 0.5256204671690727.
- Split hash c5cec7e3bf6eaad41e12ae786246bf454a1bbcd4476286c71eb7e75b0eeba71a; training-pool hash 3d1e3ea691fc19fab65d66ad278d169cf099eb831ad0e46a439510ff5d07a7ba; validation-candidate hash aca455fc094f2b037a812d62a4fcb79fd8d48102d021d72418aea1ab0b65b455.
- Selected QTHS25 train-negative hash 1ada7e01d1b3fa788db9d8312167290d4191344ace2db40bb787ab78e027c758.

## V13-relevant weak signals and controls

| Signal | V12 row | MRR | Δ vs QTHS25 | Params | Runtime (s) | Evidence source | Paired comparison |
|---|---|---:|---:|---:|---:|---|---|
| X1_RAW | V12-S1C-03 | 0.527652 | +0.002032 | 24944 | 132.59 | Same-size residual MLP on unprojected Raw-HG pair representation | matched-control MRR 0.5276520613059302
| X2_SELF | V12-S1E-03 | 0.527742 | +0.002122 | 25136 | 84.41 | Same-parameter residual MLP replacing cross-view product with within-view self moments | matched-control MRR 0.5277424882449662
| B2_SCALE | V12-S1F-03 | 0.527789 | +0.002169 | 24737 | 66.29 | Two-scalar degree/common-neighbor score calibration without cross-branch interaction | matched-control MRR 0.5277890892403717
| D2_CROSS | V12-S1H-02 | 0.527136 | +0.001515 | 24736 | 64.93 | Zero-initialized scalar residual from target-masked cross-edge density between exclusive endpoint neighborhoods | matched-control MRR 0.5248674249276082
| C2_COS | V12-S1J-01 | 0.526290 | +0.000669 | 24736 | 48.57 | Zero-initialized scalar residual from cosine similarity of raw endpoint features | matched-control MRR 0.5257171702125438

V12 controls remain eligible as weak primitives only; none is a PAPER_CANDIDATE. V13 Phase A tests whether independent evidence channels compose under a predeclared residual-calibration principle.

## Control > QTHS25 while candidate < control

| Candidate | Control | Candidate MRR | Control MRR | Baseline MRR | Candidate Δ | Control Δ | Interpretation |
|---|---|---:|---:|---:|---:|---:|---|
| S1C_X1 | S1C_X1_RAW | 0.523703 | 0.527652 | 0.525620 | -0.001918 | +0.002032 | Orthogonalized X1 failed; raw-HG representation control is a weak positive signal. |
| S1E_X2 | S1E_X2_SELF | 0.527739 | 0.527742 | 0.525620 | +0.002119 | +0.002122 | Cross-view product did not improve over within-view self moments. |
| S1F_B2 | S1F_B2_SCALE | 0.526513 | 0.527789 | 0.525620 | +0.000892 | +0.002169 | Branch coactivation failed; degree/CN score calibration is a weak positive signal. |
| S1I_D2R | S1I_D2R_CROSS | 0.525869 | 0.527136 | 0.525620 | +0.000249 | +0.001515 | Excess-density subtraction removed the raw cross-density signal. |

The C2 treatment exceeded its same-parameter score-rescaling control (0.526290 vs 0.525717), but both were subthreshold; this is retained as low-priority evidence rather than a control-derived primitive.
