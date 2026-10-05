# Failure Analysis — V2

No V2 candidate has failed an experiment yet.

## Required F1--F10 taxonomy

- F1: implementation or reproducibility failure
- F2: data leakage or protocol violation
- F3: static resource/memory infeasibility
- F4: parent-equivalence or structural collapse
- F5: novelty collision / insufficiently distinct structure
- F6: no feature-level or mechanism-level support
- F7: ranking-protocol failure
- F8: seed instability or systematic metric regression
- F9: proxy/control defeat
- F10: insufficient dataset/support coverage

Every stopped candidate will add a dated record with evidence, the primary failure class, secondary classes, and a no-retry boundary.

## 2026-09-16 — V2-001 PCDT

- Evidence: seed 0 Parent MRR 0.09491, aligned PCDT MRR 0.11374, but shuffled-evaluation PCDT MRR 0.12120. The shuffled control also exceeded the aligned path on Hits@20/50/100 and AUC.
- Primary class: F9 (control defeat).
- Secondary class: F4 risk (the improvement was not attributable to the intended pair-to-neighborhood alignment).
- Action: STOP. Do not rescue with a gate, attention, extra depth, larger width, loss, or optimizer change. The generic pair-conditioned local-transport family is closed for this loop.

## 2026-09-16 — V2-002 CDPT seed heterogeneity

- Evidence: seed 1 decreased MRR by 0.00565 while seeds 0 and 2 improved. This is retained as a reproducibility caveat, not a candidate-level STOP, because the locked Stage 3 rule requires only 2/3 improvements and the mean ΔMRR is positive.
- Follow-up: deepening mode must report seed-wise results and validate the cross-depth mechanism with a focused ablation before any broader claim.
