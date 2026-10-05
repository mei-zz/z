# Focused novelty search: graph-hard negatives verified by a hypergraph

**Search date:** 2026-10-02. **Scope:** public web search for hypergraph-verified graph-hard negative mining, graph/hypergraph negative mining, cross-view purification, disagreement sampling, DMNS, MeBNS, dynamic negative sampling, and false-negative filtering. This is a focused overlap check, not a systematic review or a claim of priority.

## Closest relevant work found

| Work | Task and mechanism | Relationship to V6 rule |
|---|---|---|
| DMNS, Diffusion-based Negative Sampling on Graphs for Link Prediction (TheWebConf 2024) | Generates multi-level hard negatives in a latent space using conditional diffusion for ordinary graph link prediction. [Paper](https://arxiv.org/abs/2403.17259) | Strong overlap on graph link prediction and hardness-aware negative sampling. It does not describe a frozen graph proposer followed by a hypergraph plausibility veto. |
| MeBNS, Not All Negatives Are Worth Attending to (2023 preprint) | Uses a teacher-student/meta-learning framework to reweight hard samples and address migration between easy and hard negatives. [Paper](https://arxiv.org/abs/2312.04815) | Overlaps in the motivation that not all hard negatives are useful. Its mechanism is dynamic meta-weighting, not rank-based graph proposal plus cross-view hypergraph rejection. |
| Hard Negative Sampling in Hyperedge Prediction (2025 preprint) | Synthesizes hard negatives in a hyperedge embedding space for higher-order hyperedge prediction. [Paper](https://arxiv.org/abs/2503.08743) | Directly concerns hypergraph negatives, but predicts whole hyperedges and does not use a hypergraph score to filter graph-proposed pairwise negatives. |
| Negative Sampling for Hyperlink Prediction in Networks (2020) | Studies uniform and structure-based sampling of non-hyperlinks, characterizing negative hardness for higher-order prediction. [Article](https://pmc.ncbi.nlm.nih.gov/articles/PMC7206280/) | Establishes prior work on hard negatives in hypergraph/link prediction, but its task and sampling mechanisms differ from the V6 pairwise proposer-verifier rule. |
| False Negative Sample Detection for Graph Contrastive Learning (FD4GCL) | Detects false negatives using attribute- and structure-aware signals in graph contrastive learning. [Article](https://www.sciopen.com/article/10.26599/TST.2023.9010043) | Related to filtering unreliable negatives, but is contrastive representation learning and does not match ordinary pairwise LP with a hypergraph veto. |
| LinkFND | Defines and uses false negatives in recommendation with graph contrastive learning. [Publication record](https://pure.dongguk.edu/en/publications/linkfnd-simple-framework-for-false-negative-detection-in-recommen/) | Related to false-negative detection, but different objective/task and no graph-hard proposer plus hypergraph verifier. |

## Assessment

The focused search found substantial conceptual overlap with (i) hard/dynamic negative sampling in graph link prediction, (ii) filtering or down-weighting potentially unreliable negatives, and (iii) negative sampling for hyperedge prediction. It did not identify an exact source implementing the same rule: per-positive Graph-score rank proposes the top 2K pairwise non-edges, then a separate frozen Raw-HG-score rank vetoes the top 25% of HG-plausible candidates, while the unmodified Raw-HG pairwise LP model trains on the remaining Graph-hard candidates.

**NOVELTY_STATUS: EXACT_RULE_UNVERIFIED.** No exact overlap was identified in this focused search, but coverage is limited and the rule should not be described as the first. The stronger novelty risk is that the method may be viewed as a straightforward cross-view hard-negative filter unless later work demonstrates a clear mechanism and robust multi-seed benefit.

## Query log

- hypergraph verified hard negative sampling; graph hypergraph negative mining
- cross-view negative purification link prediction; hard negative false negative filtering graph
- multi-view hard negative filtering link prediction; disagreement negative sampling graph
- MeBNS; dynamic negative sampling; hard negative sampling in hyperedge prediction
- graph link prediction false-negative-aware filtering; hypergraph score veto for pairwise link prediction

The search was limited to publicly indexed pages and paper records. It did not exhaustively search all conference proceedings, patents, preprints, or non-English literature.
