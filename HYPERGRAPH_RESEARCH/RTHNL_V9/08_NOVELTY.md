# Focused novelty search

Search was bounded to the five prescribed overlaps: (1) bounded-influence or robust weighting of hard negatives, (2) gradient weighting in graph link prediction, (3) per-positive robust centers, (4) false-negative-aware negative selection, and (5) semi-hard/rank-window selection. Queries also tested the exact combination of a detached sigmoid-BCE gradient, per-positive median, upper-tail `2c/(c+g)` rule, and mean normalization.

| Work | Relevant overlap | Difference from the exact V9 rule |
|---|---|---|
| [DMNS, Diffusion-based Negative Sampling on Graphs for Link Prediction](https://arxiv.org/abs/2403.17259) | Generates link-prediction negatives at controllable difficulty levels. | Diffusion-based candidate generation; not the fixed graph-teacher pool with a per-positive median-gradient tail weight. |
| [Affinity Uncertainty-based Hard Negative Mining in Graph Contrastive Learning](https://arxiv.org/abs/2301.13340) | Weights graph contrastive negatives using learned affinity uncertainty. | Self-supervised contrastive objective and learned uncertainty; not the supervised BCE local-gradient formula. |
| [ProGCL: Rethinking Hard Negative Mining in Graph Contrastive Learning](https://proceedings.mlr.press/v162/xia22b.html) | Addresses unreliable hard negatives in graph contrastive learning. | Contrastive setting and reliability modeling differ from the proposed per-positive median rule. |
| [Hard negative sampling in hyperedge prediction](https://arxiv.org/abs/2503.08743) | Studies hard-negative selection for higher-order prediction. | Hyperedge candidate construction, not this pairwise fixed-pool weighting formula. |
| [Negative Sampling for Hyperlink Prediction in Networks](https://pmc.ncbi.nlm.nih.gov/articles/PMC7206280/) | Analyzes negative-sampling strategy and hardness for hyperlink prediction. | Sampling strategy study; no exact match to the V9 continuous gradient-tail weighting rule confirmed. |

**NOVELTY_STATUS: EXACT_RULE_UNVERIFIED.** This bounded search did not confirm an exact match. It is not an exhaustive priority review and supports no “first” claim. The method was rejected before empirical validation, so no novelty claim is warranted.
