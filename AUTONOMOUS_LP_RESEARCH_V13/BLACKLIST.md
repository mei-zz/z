# V13 method blacklist

This records specific mechanisms already falsified in V12 and unchanged lineages prohibited by the V13 brief. V12 evidence and numerical source rows are in 00_V12_SIGNAL_AUDIT.md.

| Method / lineage | Status | Reason or boundary |
|---|---|---|
| F1, F2, F3, D1, D2R, C1, C2, G1, G2, H1 | DO NOT RERUN UNCHANGED | V12 registered lineages; see signal audit and V12 blacklist. |
| X1 proposed orthogonalized raw-HG residual | BLACKLISTED | Lost to raw-HG representation control; not the same as low-capacity evidence calibration. |
| X2 proposed aligned Graph/Raw-HG product | BLACKLISTED | Did not beat the within-view self-moment control. |
| B2 branch coactivation | BLACKLISTED | Failed to beat simple degree/CN score calibration. |
| D2R excess cross-closure density | BLACKLISTED | Subtracting within-side density removed the raw cross-density signal. |
| C2 raw endpoint cosine residual | BLACKLISTED | Subthreshold; no retuning permitted. |
| F1 global batch-top ranking, D1 one-hop ego residual, F2 BCE-anchored ranking, H1 edge-dropout consistency, F3 identity-aligned auxiliary | BLACKLISTED | V12 Stage 2/1 matched-control failures. |
| Positive-side difficulty weighting G2 | BLACKLISTED | No persistent-history mechanism signal. This does not blacklist negative-candidate hardness trajectories. |
| SH75 window tweaks, fixed-percentile trims, hyperparameter-only changes | BLACKLISTED | No new information source or optimization principle. |
| T1 persistent hard negative from same-candidate multi-checkpoint trajectories | ELIGIBLE | Distinct from V12 positive difficulty weighting; must beat trajectory-shuffled and final-rank-matched controls. |
| L1 setwise expected reciprocal-rank objective over 20 candidates | ELIGIBLE | Must be controlled for independent BCE, generic listwise, repeated K=1 BCE, and extra compute. |
| P1 explicit low-rank symmetric pair-state decoder | ELIGIBLE | Must beat same-parameter generic MLP, same-dimension concatenation, and baseline. |
| V1 high-confidence pair-score cross-view rank distillation | ELIGIBLE | Must beat shuffled alignment, mean matching, feature alignment, and no-distillation controls. |
| S family edge-centric pair-context message passing | ELIGIBLE ONLY AFTER T/L/P/V | Must not reproduce SEAL/DRNL or V12's one-hop ego-context residual. |

Controls P1–P5 in CONTROL_SIGNAL_LEDGER.md are retained as weak primitives and are not blacklisted.
