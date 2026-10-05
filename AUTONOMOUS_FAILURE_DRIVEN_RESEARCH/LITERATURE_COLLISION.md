# Literature Collision Audit

## Audit rule

Collision was checked at the level of state object, propagation rule and data assumption, not by names. A candidate is not allowed to enter GPU work when its main computation is already an existing pair-state, common-neighbor, topology-editing, missing-edge/noise, or inductive-topology mechanism.

| Work | Year / venue | State or data assumption | Core computation | Collision implication |
|---|---|---|---|---|
| SEAL | 2018 / NeurIPS workshop-era line | Enclosing subgraph around a target pair | Subgraph labeling plus GNN for each target pair | A proposed pair-conditioned local-subgraph reranker is not independent unless its state/propagation is materially different |
| NCN / NCNC | 2023 and follow-up code | Node embeddings plus common-neighbor / CNC pair features | Explicit common-neighbor aggregation and pair predictor | Hard-negative candidate reranking from CN neighborhoods is a direct partial collision |
| MPLP | 2023 | Pairwise node-labeling and link predictor | Efficient node labeling / pair representation | A learned pair-local structural decoder is not automatically new |
| 2-FWL / Local 2-FWL | 2023–2024 code and follow-up | Ordered/unordered node-pair states | Pair-state updates through intermediate nodes | T2WL-INC and any `(i,k),(k,j)->(i,j)` proposal are already covered |
| SLRGNN | 2024 / ICML workshop-era PMLR publication | Line-graph / link representation | Message passing in edge space | Edge/cochain propagation is a collision family, not a free new direction |
| PULL | 2025 / AAAI | Edge-incomplete graph, observed nonedges unlabeled | PU learning with latent missing-edge treatment | A missing-edge-aware proposal must differentiate its data model and estimator |
| LEAP | 2025 preprint | Inductive link prediction | Learnable topology augmentation | “Learned topology correction” is not independent by name change |
| LPShift | 2024 preprint, KDD 2025 Datasets & Benchmarks | Controlled structural distribution shift | Benchmark split construction and evaluation | A hard-negative shift claim must use a declared split and cannot call Cora HeaRT LPShift |
| CORE | 2026 / ACM TKDD | Missing-edge completion and noisy topology | Topology completion/noise reduction | A denoising/completion candidate requires a genuinely different estimator and benchmark |
| OCN / later common-neighbor lines | 2025 and follow-up | Pair scores driven by overlap and neighborhood structure | Explicit overlap/common-neighbor computation | A “hard-negative-aware CN” branch is already high-risk collision |

## Rejected pre-candidates

### H1: hard-negative-conditioned local reranker

Researcher value: could target the stable HL/LL error groups.

Critic objection: the information is already exposed by CN/AA/RA, feature similarity, NCN/NCNC, SEAL-like enclosing subgraphs, or a pair MLP. The new object would be a target-pair decoder, directly repeating the failed PCDT/CDPT family.

Experimentalist control: first compare the fixed proxies and a protocol-aligned NCN/SEAL baseline. This control was not available under the same HeaRT adapter; therefore no architecture was implemented.

Judge: **STOP before implementation**. The candidate has no defensible independent state object.

### H2: uncertainty-aware topology denoiser

Researcher value: could protect propagation from missing/spurious edges.

Critic objection: PULL and CORE already alter the observed-edge assumption, while LEAP covers learned topology augmentation. A small denoising branch would be a direct collision and would also require a proper incomplete/noisy benchmark, which is not present remotely.

Experimentalist control: obtain the public PULL/CORE-compatible data, predeclare edge corruption, and compare against their official implementations. Remote data acquisition did not complete.

Judge: **HOLD/NOT_EXECUTED**, not a valid V6 candidate.

## Sources

- [SEAL paper search anchor](https://arxiv.org/abs/1802.09691)
- [NCN/NCNC official code](https://github.com/GraphPKU/NeuralCommonNeighbor)
- [MPLP official code](https://github.com/Barcavin/efficient-node-labelling)
- [2-WL official code](https://github.com/GraphPKU/2WL_link_pred)
- [SLRGNN PMLR record](https://proceedings.mlr.press/v251/lachi24a.html)
- [PULL official code](https://github.com/snudatalab/PULL)
- [LEAP paper](https://arxiv.org/abs/2503.03331)
- [LPShift paper](https://arxiv.org/abs/2406.08788)
- [LPShift code](https://github.com/revolins/LPShift)
- [CORE DOI record](https://doi.org/10.1145/3789200)
- [OCN paper/code anchor](https://github.com/qingpingmo/OCN)
