# Focused novelty search (2026-10-02)

## Search scope

Searches covered graph link-prediction extreme/semi-hard negatives, graph contrastive hard-negative mining, negative-sample diversity and endpoint concentration, and negative sampling for hypergraph/hyperedge prediction. The search was used to identify overlap, not to establish an exhaustive priority claim.

## Closest primary work and overlap

| Work | Relevant overlap | Difference from this experiment |
|---|---|---|
| Patil, Sharma & Murty, “Negative Sampling for Hyperlink Prediction in Networks” (PAKDD 2020) | Studies uniform, size-, motif-, and clique-based negative sampling for hyperlink prediction; defines hardness from subgraph density and analyzes its distribution. | It does not rank train negatives with a frozen graph teacher and trim the extreme part of a per-positive teacher-ranked pool, nor balance endpoint reuse by greedy counts. |
| Deng, Zhou & Bi, “Hard negative sampling in hyperedge prediction” (arXiv:2503.08743, 2025) | Directly studies hard-negative sampling for hyperedge prediction and reports performance/robustness motivations. | It synthesizes negatives in hyperedge embedding space; it does not use this experiment’s graph-teacher candidate pool, quantile trimming, or endpoint concentration penalty. This rules out broad “first hard-negative sampling for hypergraph prediction” language. |
| Nguyen & Fang, “Diffusion-based Negative Sampling on Graphs for Link Prediction” (WWW 2024) | Generates negatives at controllable, multiple hardness levels for graph link prediction. | It uses conditional diffusion to generate latent-space negatives, rather than pruning a fixed graph-teacher-ranked candidate pool for hypergraph link prediction. |
| Li et al., “Evaluating Graph Neural Networks for Link Prediction: Current Pitfalls and New Benchmarking” (NeurIPS 2023; HeaRT) | Constructs personalized difficult evaluation negatives using multiple heuristics. | The focus is evaluation candidate construction, not train-time negative selection or hardness regularization. |
| Xia et al., “ProGCL: Rethinking Hard Negative Mining in Graph Contrastive Learning” (ICML 2022) | Shows that selecting the hardest graph negatives can be harmful when false negatives are common; uses estimated negative reliability. | It concerns node-level graph contrastive learning and reliability weighting, rather than supervised pairwise link prediction with a frozen teacher. |
| Wang et al., “Not All Negatives Are Worth Attending to: Meta-Bootstrapping Negative Sampling Framework for Link Prediction” (arXiv:2312.04815) | Studies movement between easy and hard negatives and changes sample weighting for link prediction. | It is an adaptive meta-learning framework, not fixed-rank quantile trimming or endpoint-frequency coverage balancing. |

## Novelty decision

**No exact match was identified in this focused search.** There is substantial adjacent prior art for hard/semi-hard negatives, multi-level hardness, false-negative-aware graph sampling, and hyperedge negative sampling. Therefore:

- Do not claim that “hard but not too hard” is new.
- Do not claim the first hard-negative sampler for hypergraph/hyperedge prediction.
- If validation and the gated test support QTHS, the defensible narrow framing is train-only per-positive quantile trimming of a frozen graph-teacher-ranked pool for hypergraph link prediction, with its rank mixture matched to the shuffled-veto control.
- If validation and test support CBHS, the narrow framing is a greedy endpoint-frequency penalty applied within a graph-teacher hard-negative prepool in this hypergraph link-prediction setup.
- These are candidate-specific empirical contributions, not priority claims. Broader database, citation, and code searches remain necessary before making a first/novel claim.

## Primary sources

- [Negative Sampling for Hyperlink Prediction in Networks (PAKDD 2020)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7206280/)
- [Hard negative sampling in hyperedge prediction (arXiv, 2025)](https://arxiv.org/abs/2503.08743)
- [Diffusion-based Negative Sampling on Graphs for Link Prediction (WWW 2024)](https://arxiv.org/abs/2403.17259)
- [HeaRT / NeurIPS 2023 paper](https://proceedings.neurips.cc/paper_files/paper/2023/hash/0be50b4590f1c5fdf4c8feddd63c4f67-Abstract-Datasets_and_Benchmarks.html)
- [ProGCL: Rethinking Hard Negative Mining in Graph Contrastive Learning (ICML 2022)](https://proceedings.mlr.press/v162/xia22b.html)
- [Meta-Bootstrapping Negative Sampling for Link Prediction (arXiv)](https://arxiv.org/abs/2312.04815)
