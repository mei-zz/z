# Focused novelty search: quantile and tail-adaptive negative sampling

Search date: 2026-10-02. Scope: graph link prediction and adjacent hyperlink/hyperedge prediction; queries covered quantile hard-negative sampling, trimmed/extreme-tail negatives, per-positive adaptive hardness, semi-hard sampling, DMNS, MeBNS, HNS/DNS, and self-adversarial sampling. This is a targeted search, not an exhaustive priority review.

## Findings

No exact paper match was identified for (i) trimming a frozen graph-teacher-ranked top-two negative pool per positive and (ii) setting the trim level from that positive's training-pool tail-excess statistic using a two-level 15%/35% rule. This is not evidence of priority and does not support a first-claim.

| Work | Relevant overlap | Distinction from QTHS/AQTHS |
|---|---|---|
| [MeBNS (Wang et al., 2023)](https://arxiv.org/abs/2312.04815) | Link-prediction negative selection and hard/easy sample migration; uses teacher/student and meta reweighting. | Learned/meta-learning framework; no fixed per-positive teacher-score quantile trim or tail-shape 15/35 rule. |
| [DMNS (Nguyen & Fang, WWW 2024)](https://arxiv.org/abs/2403.17259) | Graph link prediction with controllable multi-level negative hardness. | Diffusion-based latent candidate generation and hardness levels, not trimming a fixed graph-teacher candidate pool by a per-positive quantile. |
| [HeaRT (Li et al., NeurIPS 2023)](https://proceedings.neurips.cc/paper_files/paper/2023/hash/0be50b4590f1c5fdf4c8feddd63c4f67-Abstract-Datasets_and_Benchmarks.html) | Positive-conditioned, heuristic hard negatives for link-prediction evaluation. | Evaluation benchmark construction, not train-time tail trimming. |
| [ProGCL (Xia et al., ICML 2022)](https://proceedings.mlr.press/v162/xia22b.html) | Shows that the hardest graph contrastive negatives can be unreliable; estimates false-negative probability alongside similarity. | Node-level graph contrastive learning with reliability estimation, not supervised link-prediction candidate quantiles. |
| [Adaptive Hardness Negative Sampling for Collaborative Filtering (2024)](https://arxiv.org/abs/2401.05191) | Adapts hardness to individual recommendation samples. | Collaborative filtering; adaptive hardness is related, but the searched description does not match graph-link-prediction teacher-pool tail quantile trimming. |
| [Hard Negative Sampling in Hyperedge Prediction (Deng et al., 2025)](https://arxiv.org/abs/2503.08743) | Direct hard-negative work in higher-order prediction. | Synthesizes negatives in hyperedge embedding space; it rules out broad claims that hard-negative sampling itself is new. |
| [Negative Sampling for Hyperlink Prediction in Networks (Patil et al., 2020)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7206280/) | Studies negative-sample hardness distributions for hyperlink prediction. | Structural sampling strategies; not teacher-ranked per-positive quantile trimming. |
| [RotatE (Sun et al., ICLR 2019)](https://arxiv.org/abs/1902.10197) | Self-adversarial weighting emphasizes higher-scoring negatives. | Knowledge-graph embedding weighting, not tail trimming or adaptive per-positive candidate quantiles. |

## Conservative novelty status

`NO_EXACT_MATCH_IDENTIFIED_IN_FOCUSED_SEARCH`. The defensible claim, if experiments support it, is a narrow empirical contribution: a fixed graph-teacher top-two rank trim (QTHS) and a training-pool tail-shape-conditioned allocation of the trim between per-positive examples (AQTHS). Do not claim first, optimal, or universally novel. Database/citation searches and broader full-text screening remain necessary before submission.
