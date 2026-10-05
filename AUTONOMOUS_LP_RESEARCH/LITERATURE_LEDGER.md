# Literature Ledger — Round 1

Search date: 2026-09-16. Search scope: 2022–2026, primary conference/publisher/arXiv pages, with emphasis on 2024–2026. Novelty wording is deliberately limited to “no complete isomorphic method found in this round’s search scope.”

## Core and dangerous prior work

| Method | Year / venue | What it explicitly contributes | Audit relevance |
|---|---|---|---|
| SEAL | 2018 / NeurIPS | enclosing-subgraph node-labeling and subgraph learning for LP | strong collision for local enclosing-subgraph objects |
| NBFNet | 2021 / NeurIPS | neural Bellman-Ford style path reasoning for LP/KG reasoning | strong collision for path-family/flow objects |
| Neo-GNN | 2021 / ICLR | neuralized topology heuristics | collision for degree/CN/heuristic combinations |
| ELPH / BUDDY | 2022–2023 / arXiv, WWW | scalable hashing/sketching plus structural features for LP | collision for cheap structural profiles and sketches |
| HeaRT | 2023 / NeurIPS workshop / arXiv | hard negative and evaluation protocol for LP | protocol must not be mixed with random-negative metrics |
| NCN / NCNC | 2023–2024 / ICLR | MPNN followed by explicit common-neighbor aggregation/completion | parent and strongest collision for witness-based objects |
| LPFormer | 2023 / arXiv | transformer-style LP with structural encoding | collision for generic pair attention/encoding |
| HL-GNN | 2024 / arXiv | higher-order/local structural propagation for LP | collision for adaptive hop/propagation mechanisms |
| MPLP | 2024 / NeurIPS | quasi-orthogonal message passing to estimate joint structural features | parent and collision for path/count estimates; variance branch blacklisted |
| Link-MoE | 2024 / NeurIPS | mixture-of-experts for LP | generic routing is not a new structural object |
| Structural Information Enhanced Graph Representation / BST | 2024 / AAAI | binary structural transformer and structure-focused encoding | dangerous collision for local structural relation encoding |
| SLRGNN | 2024 / GRaM workshop | line-graph transformation for structural link representation | dangerous collision for edge-centric/line-graph objects |
| PULL | 2025 / AAAI | positive-unlabeled learning for edge-incomplete graphs | related incomplete-observation mechanism, not structural object |
| Open Your Eyes | 2025 / ICML | vision-style structural features for MPNN LP | collision for generic external structural feature injection |
| GPEN | 2025 / ICML | scalable graph positional/structural encoding for LP | collision for generic positional encoding |
| CRAFT | 2025 / NeurIPS | target-aware matching for temporal future LP | relevant only to temporal candidate objects |
| Scalable Pretraining Framework for LP | 2025 / KDD | pretraining and efficient adaptation | not a direct collision; parent/protocol concern |
| Sub-Graph Based Diffusion Model for LP | 2025 / LoG | conditional likelihood over enclosing subgraphs | strong collision for generic enclosing-subgraph generative models |
| Graph2Video | 2026 / AAAI | link-centric memory for dynamic graph evolution | dynamic/temporal collision only |
| UniHR | 2026 / AAAI | hierarchical inter-/intra-fact structure for KG LP | KG-specific structural hierarchy collision |
| CORE | 2026 / TKDD | information-bottleneck data augmentation for LP | augmentation/control reference, not direct collision |

## Primary-source URLs

- [NCN/NCNC, ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/file/9dd67d30e0edd53581363c1b49006e1d-Paper-Conference.pdf)
- [MPLP, NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/hash/85970f7bbc821852c1d17052b88c2451-Abstract-Conference.html)
- [Structural Information Enhanced Graph Representation, AAAI 2024](https://ojs.aaai.org/index.php/AAAI/article/view/29417)
- [SLRGNN, PMLR 2024 workshop](https://proceedings.mlr.press/v251/lachi24a.html)
- [PULL, AAAI 2025](https://ojs.aaai.org/index.php/AAAI/article/view/33966)
- [Open Your Eyes, ICML 2025](https://proceedings.mlr.press/v267/wei25m.html)
- [GPEN, ICML 2025](https://proceedings.mlr.press/v267/wu25l.html)
- [CRAFT, NeurIPS 2025](https://proceedings.neurips.cc/paper_files/paper/2025/hash/036912a83bdbb1fd792baf6532f102d8-Abstract-Conference.html)
- [Scalable Pretraining Framework for LP, KDD 2025](https://doi.org/10.1145/3711896.3736822)
- [Sub-Graph Based Diffusion Model for LP, LoG 2025](https://proceedings.mlr.press/v269/li25a.html)
- [Graph2Video, AAAI 2026](https://ojs.aaai.org/index.php/AAAI/article/view/38557)
- [UniHR, AAAI 2026](https://ojs.aaai.org/index.php/AAAI/article/view/38569)
- [CORE, TKDD 2026](https://doi.org/10.1145/3789200)

## Novelty-kill search policy

Before a candidate reaches Stage0, search its exact name, synonyms, structural primitive, and the same mechanism in link prediction, KGE, recommender systems, graph classification, and graph matching. Candidate status must be L0, L1, L2, or L3 with a short collision explanation. L0 candidates are discarded; L1 candidates require a sharply stated distinction and strong empirical reason.
