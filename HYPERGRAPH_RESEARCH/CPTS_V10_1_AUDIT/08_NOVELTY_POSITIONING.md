# Novelty positioning

Search date: 2026-10-02. Status: **EXACT_RULE_UNVERIFIED**. A focused search does not establish priority. No claim of "first" is supported.

| Primary source | Existing contribution | Consequence for CPTS claims |
|---|---|---|
| [AHNS, AAAI 2024](https://arxiv.org/abs/2401.05191) | Adaptive negative hardness for collaborative filtering, including a relationship between positive and negative scores. | Per-sample adaptive hardness is already an explicit paradigm; it cannot be claimed as CPTS novelty. |
| [DMNS, WWW 2024](https://arxiv.org/abs/2403.17259) | Conditional diffusion generates controllable negative difficulty levels for graph link prediction. | Graph LP difficulty control already exists; CPTS selects a frozen pool rather than generating negatives. |
| [ProGCL, ICML 2022](https://proceedings.mlr.press/v162/xia22b.html) | Reliability of hard graph-contrastive negatives, estimating true-negative probability using a mixture model and weighting/mixing. | Distribution modeling and unreliable hard-negative correction already exist; CPTS is a segmented selection rule for ordinary supervised graph LP. |
| [Negative Sampling From the Ground Up: A Redesign for Recommendations, ICML 2026](https://proceedings.mlr.press/v306/wang26db.html) | Principled approximation of an underlying true negative distribution for bipartite recommendation graphs. | A general claim that negative distribution design should be principled is established prior work. The objective and graph setting differ from this audit. |
| [PSP-NS, 2026 preprint](https://arxiv.org/abs/2602.18206) | Positive-pair construction with a negative sampling plugin for implicit CF, with margin-improvement analysis. | A theoretical hardness or ranking story must distinguish its assumptions and objective from CPTS. |

Searches included adaptive hardness negative sampling, per-instance hardness, adaptive semi-hard mining, change-point negative sampling, hard-negative distribution segmentation, BIC/MDL negative sampling, and 2026 negative sampling theory. Exact full-rule equivalence was not identified in this limited search. Broad terminology is not a novelty claim.

The only candidate narrow distinction is **explicit per-positive hardness-distribution segmentation via change-point model selection for ordinary graph link prediction**. Whether it is a useful and valid mechanism depends on the null, shuffled/reversed pairing, fixed-quantile and generalization audits. If null detection is indiscriminate, describe the rule as empirical hardness-region regularization, not detection of a real extreme-tail regime. Final claim permission is in PAPER_CLAIM_MATRIX.md after the experiment finishes.
