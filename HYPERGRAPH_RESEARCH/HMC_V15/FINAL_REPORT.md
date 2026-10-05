# V15 HMC Final Report

**STATUS:** EXECUTED — Stage 0 completed remotely; HMC stopped by the preregistered corrected gate.  
**CANDIDATE:** HMC — Hypergraph Motif Closure Encoder  
**ZERO_GPU_GATE:** FAIL — `SCALAR_SUFFICIENT`  
**FINAL_DECISION:** `SCALAR_SUFFICIENT`  
**SERVER JOB:** Finished; no GPU training was submitted.  
**TEST:** Sealed and not evaluated.

## Zero-GPU Cora audit

Training-only data, five-fold grouped cross-validation, and fold-local scaling/logistic regression were used. The split contains 4,488 training positives and 13,464 legal matched negatives (three per positive; every positive received matches). Reported values are mean ± sample SD across folds.

| Feature set | ROC-AUC | PR-AUC |
|---|---:|---:|
| Z0 support count / CN-like | 0.804146 ± 0.006650 | 0.595130 ± 0.017701 |
| Z1 multiplicity scalar (MS) | 0.808875 ± 0.006793 | 0.620486 ± 0.018041 |
| Z2 HRA-like scalar | **0.820960 ± 0.006949** | **0.716169 ± 0.013683** |
| Z3 real joint multiplicity summaries | 0.815152 ± 0.005981 | 0.693106 ± 0.009525 |
| Z4 cross-side shuffled summaries | 0.812516 ± 0.006160 | 0.675174 ± 0.011093 |

The real joint set beats support count by **0.011006 AUC**, below the required +0.015, and beats shuffled features by **0.002635**, below the required +0.010. It is below the HRA-like scalar by **0.005808 AUC**, so the corrected protocol marks `SCALAR_SUFFICIENT` and stops the set encoder. The positive median extra multiplicity E is 4 versus 0 for matched negatives, satisfying the distribution check; this does not override the scalar-control failure.

The informative-shuffle fraction is **14.07%**, below the 20% threshold. Mark `LOW_SHUFFLE_POWER`; the small real-versus-shuffle gap is not treated as direct evidence that same-support alignment fails. The scalar-control result independently closes the HMC gate.

## Matching and leakage checks

- Exact source split hash: `c5cec7e3bf6eaad41e12ae786246bf454a1bbcd4476286c71eb7e75b0eeba71a`.
- All 4,488 train positives received three legal training-only negatives. The matching selected 8,769 degree-bin exact pairs, 3,712 support-count exact pairs, 7,574 graph-CN exact pairs, and 4,979 exact degree plus support-count-or-CN pairs.
- Pair-specific local target subtraction matched full target-masked `raw_star` reconstruction on all **100/100** sampled train-positive checks; endpoint-swap symmetry passed.
- Validation/test identities were not used in feature construction, negative matching, folds, or normalization. Test remained sealed.

Positive versus matched-negative token audit: mean support count 9.950 vs 1.795; empty-support fraction 27.23% vs 81.18%; P[(m_u,m_v)=(1,1)] 59.96% vs 80.36%; P[max(m_u,m_v)≥2] 40.04% vs 19.64%; P[min(m_u,m_v)≥2] 12.92% vs 2.77%; mean multiplicity product 2.537 vs 1.434; median E 4 vs 0. These are descriptive train-only differences, not evidence that the learned joint set encoder adds value beyond scalar controls.

## Later stages and model cost

- **Cora Stage 1:** NOT RUN — no Stage-0 GO. Baseline, scalar arms, HMC-FLAT, HMC-SHUFFLE, and HMC-REAL training were not launched.
- **Cora Stage 2 / three-seed confirmation:** NOT RUN.
- **Cora test:** NOT RUN; sealed.
- **PubMed quick screen:** NOT RUN.
- The proposed residual encoder is analytically 49 added parameters (0.1981% over the 24,735-parameter baseline), with zero-initialized output. It was not trained or profiled; no HMC training-time or peak-memory result exists.
- The CPU Stage-0 audit completed in **27.07 seconds** on the server. It used no GPU compute. The cached feature archive is `diagnostics/stage0_train_features.npz` (212,459 bytes). The V100 was not needed because the corrected stop gate failed.

## Novelty

**`EXACT_RULE_UNVERIFIED`** after a focused source check; no exact collision was established, and this is not an exhaustive priority search. HMNE and HMRLH are close motif-based hypergraph link-prediction precedents, while several other methods predict higher-order motifs/simplices or learn general hypergraph node representations. The accessible descriptions do not establish the full support-wise joint multiplicity decoder rule; see [07_NOVELTY_NOTES.md](07_NOVELTY_NOTES.md). Do not claim “first.”

**Interpretation:** Cora Stage 0 does not support advancing the HMC set encoder: the HRA-like scalar outperforms it and the corrected margin gates fail. The experiment does not establish cross-side alignment failure because shuffle power is low. No rescue tuning or downstream training was performed.

**NEXT_EXPECTED_STEP:** Stop this HMC run. Preserve the results; a new experiment would require a new user instruction.
