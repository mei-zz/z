# V3 novelty search

**Workflow:** multi-source search across primary publisher, conference, and preprint records. Search window emphasized 2020–2026.

## Candidate A — ARHC

Queries covered anchor-aware and center-aware hypergraph convolution, role-aware/typed incidence, star or ego hypergraphs, position-aware link prediction, and anchor/member message passing.

| Work | Relevant evidence | Relation to ARHC |
|---|---|---|
| Chodrow & Mellor, *Annotated hypergraphs: models and applications* (2020) | Defines roles on node–hyperedge incidences. [Applied Network Science](https://appliednetsci.springeropen.com/articles/10.1186/s41109-020-00224-2) | Direct precedent for typed incidence as a general data representation; broad role labels are not novel by themselves. |
| Li et al., *RAHG: A Role-Aware Hypergraph Neural Network for Node Classification in Graphs* (2023) | Combines role and adjacency representations using graph-derived hypergraphs and hypergraph convolution. [IEEE TNSE author copy](https://zhenhuascut.github.io/pdfs/RAHG_A_Role-Aware_Hypergraph_Neural_Network_for_Node_Classification_in_Graphs.pdf) | Close conceptual precedent. Its roles describe structural similarity for node classification; this task uses the known generator center versus neighbor members in each fixed ego/star edge for pairwise link prediction. |
| Chen et al., *PosKHG: A Position-Aware Knowledge Hypergraph Model for Link Prediction* (2023) | Explicitly models role/position semantics in n-ary knowledge hyperedges. [Springer](https://link.springer.com/article/10.1007/s41019-023-00214-x) | Strong overlap at the task-family/position-aware level; knowledge-hyperedge tuple roles differ from graph-induced ego-star anchor identity and incidence convolution. |
| Huang et al., *HYPER: A Foundation Model for Inductive Link Prediction with Knowledge Hypergraphs* (ICLR 2026) | Encodes entities with their positions within varying-arity knowledge hyperedges. [ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/hash/cdf80d651420b47da80f789f2631b1b5-Abstract-Conference.html), [arXiv](https://arxiv.org/abs/2506.12362) | Recent position-aware link prediction makes a broad role-aware novelty claim unsafe; setting and operator differ from this graph-induced star experiment. |

**Status:** `NOVELTY_CONFLICT` for the broad claim “role-aware hypergraph convolution”; the narrower graph-induced anchor/member operator is `NOVELTY_UNVERIFIED` after this focused search. The intended contribution, if the experiments support it, must be stated as the specific star-anchor incidence operator and validated against the symmetric and shuffled-anchor controls. This is not a novelty guarantee.

## Candidates B and C

### Candidate B — PMHE (reached after A rejection)

Queries covered pairwise/moment hypergraph aggregation, efficient second-order hyperedge statistics, and pairwise interactions inside hyperedge encoders.

| Work | Relevant evidence | Relation to PMHE |
|---|---|---|
| Srinivasan et al., *Learning over Families of Sets* (SDM 2021) | Learns permutation-invariant, variable-size hyperedge representations and higher-order expansion tasks. [SIAM proceedings](https://epubs.siam.org/doi/10.1137/1.9781611976700.85), [arXiv](https://arxiv.org/abs/2101.07773) | Establishes expressive set encoders as a broad precedent; no exact normalized Hadamard pair-moment link-prediction operator identified. |
| *Hyperedge Interaction-aware Hypergraph Neural Network* (2024) | Explicitly models interactions among hyperedges during convolution. [arXiv](https://arxiv.org/abs/2401.15587) | Interaction is between hyperedges, whereas PMHE summarizes within-hyperedge member pairs. |
| *Wasserstein Hypergraph Neural Network* (ICLR 2026 submission) | Uses distribution-based pooling and describes edge-dependent encoders that account for pairwise interactions. [OpenReview PDF](https://openreview.net/pdf/9f911e2e834a28256e1132cc81304361eee5df1a.pdf) | Close general precedent for pairwise-aware hyperedge encoding; different mechanism, not the closed-form O(kd) Hadamard cross-moment. |
| Huang et al., *HYPER* (ICLR 2026) | Positional relation interactions for knowledge-hypergraph link prediction. [ICLR](https://proceedings.iclr.cc/paper_files/paper/2026/hash/cdf80d651420b47da80f789f2631b1b5-Abstract-Conference.html) | Confirms pair/position-aware link prediction is established in knowledge hypergraphs; data construction and operator differ. |

The broad claim “pairwise interaction hypergraph encoder” is `NOVELTY_CONFLICT`. The exact sum-square identity applied as a normalized, linear-time moment branch for graph-induced stars in pairwise link prediction is `NOVELTY_UNVERIFIED`; this focused search does not establish a novelty guarantee.

### Candidate C — ARPM (reached after B rejection)

Queries covered anchor-conditioned hypergraph interaction, center-conditioned hyperedge encoders, and relational/position-aware link prediction.

| Work | Relevant evidence | Relation to ARPM |
|---|---|---|
| Huang et al., *HYPER* (ICLR 2026) | Knowledge-hypergraph link prediction encodes entities with their positions in each hyperedge. [ICLR](https://proceedings.iclr.cc/paper_files/paper/2026/hash/cdf80d651420b47da80f789f2631b1b5-Abstract-Conference.html), [arXiv](https://arxiv.org/abs/2506.12362) | Strong general precedent for position-conditioned interaction in hypergraph link prediction; it addresses ordered relation positions in knowledge hyperedges, not a graph-generated star center conditioning member-pair moments. |
| Lu et al., *Neighborhood overlap-aware heterogeneous hypergraph neural network for link prediction* (2023) | Uses neighborhood overlap and heterogeneous event hyperedges to support pairwise link prediction. [Pattern Recognition](https://www.sciencedirect.com/science/article/pii/S0031320323005162) | Same broad task family and neighborhood structure, but it does not use a known per-star anchor to condition a within-star pair moment. |
| *Link Prediction with Relational Hypergraphs* (2024) | Uses relation and position context in message passing over relational hypergraphs. [arXiv](https://arxiv.org/abs/2402.04062) | Another broad contextual/positional precedent; relational hypergraph setting differs from the fixed graph-induced stars here. |

**Status:** `NOVELTY_CONFLICT` for broad claims around anchor-/position-conditioned hypergraph link prediction. The specific combination of graph-induced star anchors with an anchor-conditioned, closed-form member pair moment remains `NOVELTY_UNVERIFIED` in this focused search; this is not a novelty guarantee.
