# Novelty search

Search date: 2026-10-02. Search terms included change-point hard-negative sampling, BIC/MDL negative sampling, adaptive per-positive hardness distributions, graph link prediction, DMNS, and ProGCL.

## Findings

- No exact-match paper was identified in this focused search for the full combination used here: a fixed graph-teacher candidate pool for each supervised link, the ordered per-positive score vector, a BIC comparison between one segment and two contiguous mean segments, and removal of the inferred upper tail before selecting one candidate.
- **EXACT_RULE_UNVERIFIED** is the appropriate status. Search coverage is not exhaustive, so this is not a priority claim and does not support writing “first.” A broader systematic search and expert review are still needed before publication.
- Closest conceptual neighbors are adaptive hardness selection for collaborative filtering and mixture based reliability estimation in graph contrastive learning. The former adapts hardness by positive during training, but operates in implicit recommendation; the latter estimates true-negative probability from a mixture model and weights or mixes examples in unsupervised graph contrastive learning. Neither is the same selection rule or task protocol.
- DMNS is a particularly relevant graph-link-prediction neighbor: it uses conditional diffusion to generate negatives at controllable hardness levels. CPTS instead re-ranks a frozen pool of 20 existing candidates and does not synthesize negatives.

## Scope distinctions to preserve

- **DMNS:** controllable multi-level negative generation in graph link prediction. **CPTS:** training-only selection within a fixed candidate pool, using a per-positive structural boundary.
- **Semi-hard / SH75:** predefined rank interval. **CPTS:** BIC decides whether an upper tail exists and estimates its boundary from each positive's scores.
- **QTHS25:** fixed top-quartile trimming. **CPTS:** per-positive tail size varies with the local score shape.
- **ProGCL:** mixture based estimation of whether graph-contrastive negatives are likely false negatives, with weighting/mixing. **CPTS:** supervised pairwise link prediction; segmented tail detection and candidate selection.

## Primary sources checked

- Nguyen & Fang, “Diffusion-based Negative Sampling on Graphs for Link Prediction,” The Web Conference 2024: https://smufang.github.io/paper/TheWebConf24_DMNS.pdf
- Xia et al., “ProGCL: Rethinking Hard Negative Mining in Graph Contrastive Learning,” ICML 2022: https://proceedings.mlr.press/v162/xia22b.html
- Lai et al., “Adaptive Hardness Negative Sampling for Collaborative Filtering,” AAAI 2024: https://ojs.aaai.org/index.php/AAAI/article/view/28709
