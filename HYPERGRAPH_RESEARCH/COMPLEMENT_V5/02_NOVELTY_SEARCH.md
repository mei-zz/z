# V5 Novelty Search — GHHR

**Search status:** focused public-web search completed locally. **Assessment:** `CONCEPTUAL_OVERLAP; EXACT_RULE_UNVERIFIED`. This is not an exhaustive systematic review and does not establish novelty.

| Work | Relevant overlap | Difference from GHHR as tested here |
|---|---|---|
| Chai et al., HMANN, *Pattern Recognition* (2024), [publisher page](https://www.sciencedirect.com/science/article/pii/S0031320324000438) | Graph and hyperedge multi-view attention for complex-network link prediction; establishes that generic graph/hypergraph fusion is prior art. | Does not document this experiment's frozen Raw-HG residual with a graph-margin-derived, stop-gradient pairwise residual loss. |
| DHGE, AAAI (2023), [paper](https://ojs.aaai.org/index.php/AAAI/article/download/25795/25567) | Dual graph/hypergraph views and cross-view tasks in hyper-relational knowledge graph learning. | Different prediction setting and objective; nearby dual-view concept, not the same graph-hard weighting rule for ordinary pairwise LP. |
| *Pairwise Learning for Neural Link Prediction* (2022), [arXiv](https://arxiv.org/abs/2112.02936) | Pairwise optimization for neural link prediction. | Generic pairwise LP supervision; no identified graph-driven weighting of a separate Raw-HG residual. |
| HeaRT / GNN link-prediction evaluation, [OpenReview paper](https://openreview.net/pdf?id=oG65SjZNIF) | Hard negatives are important in link-prediction evaluation and benchmarking. | Evaluation candidate construction is distinct from training a hypergraph residual using graph-branch difficulty. |
| *Hard Negative Sampling in Hyperedge Prediction* (2025), [arXiv](https://arxiv.org/abs/2503.08743) | Difficulty-aware negative sampling in a hyperedge-prediction task. | Predicts hyperedges, rather than ordinary pairwise links with graph-margin-weighted hypergraph residual BCE. |
| Ma et al., *Directed Hypergraph Representation Learning for Link Prediction* (2024), [PMLR paper](https://proceedings.mlr.press/v238/ma24b.html) | Hypergraph representation learning applied to link prediction. | Supports the broad task area; the focused search did not identify the GHHR training rule. |

## Novelty boundary

The broad ingredients—graph/hypergraph multi-view prediction, pairwise LP losses, hard-negative methods, and hypergraph LP—have clear precedents. The narrower rule examined is: keep the current Raw-HG operator fixed, derive a detached sigmoid difficulty from the Graph-only positive-minus-negative score margin, and weight the paired BCE of the Raw-HG residual while retaining the Graph BCE. The focused search did not find an exact match for that combination in ordinary pairwise LP, but keyword searches cannot establish priority or novelty. The contribution should be framed as a tested task-level training rule only if controlled experiments support it, and must be rechecked against broader scholarly databases before publication.

## Queries and decision

Search themes included graph-hypergraph dual-view link prediction, complementary graph/hypergraph learning, graph-hard hypergraph learning, cross-view hard-negative link prediction, disagreement-aware fusion, difficulty-aware hypergraph LP, and teacher/hard-negative graph LP. Generic overlap is confirmed; exact-rule overlap remains unverified. No novelty guarantee is made.
