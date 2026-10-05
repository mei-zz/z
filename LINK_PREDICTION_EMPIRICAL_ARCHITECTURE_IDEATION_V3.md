# Link Prediction Empirical Architecture Ideation V3

## 0. 本轮结论

本轮是第三轮之后的全新创新点搜索，不延续上一轮 Top 15 的排序，也不把已经完成真实实验的候选重新包装：

| 已完成候选 | 结论 | 本轮处理 |
|---|---|---|
| MPLP-VC | STOP：USAir 低于 Shuffled；估计方差与度相关 | 永久排除 variance / uncertainty / confidence / second-moment 方向 |
| NCN-CNDP | STOP：24 runs 中只有 3/6 超过 parent；CN heterogeneity 没有清晰收益 | 永久排除简单统计 pooling、mean/max/variance 和“再加一个 CN summary” |
| HL-GNN-PDG | STOP：gate collapse，`mean |w-t|≈1.16e-9`；显存约 +37.6% | 永久排除 soft residual gate、adaptive hop、soft routing |

因此本轮只问一个问题：**高性能 link-prediction parent 是否没有显式观察到“候选边加入后，已有局部结构对象如何被改变”？**

当前最值得做 Stage0/Stage1 的假设是：

> **Candidate-Edge-Induced Cross-Neighborhood Closure Graph（CECG）**：把候选边 `(u,v)` 假设加入后，由 `u` 的独占邻域、`v` 的独占邻域之间已有的交叉边所形成的 4-cycle closure graph 作为新的 pair-level structural object；不把候选边本身作为输入。

这只是**待验证的 empirical hypothesis**，不是已经成立的模型创新。没有真实 Stage0/Stage1 证据之前，不启动第四个完整 GNN。

---

## 1. 研究问题与 5W1H

| 维度 | 本轮定义 |
|---|---|
| What | 候选非边插入 `G -> G^+_{uv}=G∪{(u,v)}` 时，局部图中新增的 cycle、edge-role、cut/block、谱子空间等结构响应 |
| Why | NCN/NCNC、MPLP/MPLP+ 等 parent 主要保留端点表示、CN/高阶 CN 或 pooled walk evidence；它们不一定保留“两个独占邻域之间的已有边如何组织” |
| Who | 静态、无向 link prediction 的 candidate pair；优先 NCN/NCNC parent，必要时用 MPLP+ 作交叉 parent |
| When | 只使用训练图/固定评估图 `G`；`G^+_{uv}` 是对候选 pair 的确定性结构变换，不读取 label |
| Where | 先在 Cora、CiteSeer、PubMed、OGB link-property 数据的固定协议中做结构支持审计；不以 Cora/CiteSeer 单独决定结论 |
| How | Stage0 结构支持 → Stage1 feature-only / conditional probe → parent+true / parent+shuffled → 通过后才做最小确定性 decoder 接入 |

### 信息增加检验

对每个候选严格回答：

1. Parent 已经看到什么？
2. Parent 没有显式看到什么？
3. 新对象究竟增加了什么结构事实？
4. 该事实为什么不能由 `CN/degree/AA/RA` 或 parent 的已有 pooled representation 直接恢复？
5. `Parent + true` 是否优于 `Parent + shuffled`？

如果只能回答“增加一个 scalar feature、再做 attention、再做 gate”，候选立即淘汰。

---

## 2. 近期文献边界与危险先行

本轮检索纳入了用户指定的 2025–2026 文献和 parent family：

| 工作 | 已覆盖的结构信息 | 对本轮的直接约束 |
|---|---|---|
| [TAGNN, Scientific Reports 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13234321/) | 去除邻居属性、pair-specific structural attention/RSA、长程结构 | 不再把“删 neighbor feature + pair attention/long-range encoding”当新点 |
| [IGLP, Knowledge-Based Systems 2026](https://doi.org/10.1016/j.knosys.2026.116092) | Adaptive Neighborhood Aggregation、Common Neighborhood Awareness、邻居重要性 | 不再提出 neighbor importance、adaptive aggregation 或 attention pooling |
| [BS-SubGNN, AAAI 2026](https://ojs.aaai.org/index.php/AAAI/article/view/38490) | bicentric sphere labeling 与 sphere-wise attention pooling | 不再提出 sphere/radius pooling、仅改变节点标签或池化 |
| [Cross-Scale Subgraph + Line Graph, Physica A 2026](https://doi.org/10.1016/j.physa.2026.131663) | multi-scale enclosing subgraph、line graph、cross-scale contrastive learning | line graph alone、multi-scale subgraph、contrastive fusion 直接降为 collision |
| [GPEN, ICML 2025](https://proceedings.mlr.press/v267/wu25l.html) | hierarchical global position encoding、boundary-aware convolution | global position、boundary-aware global aggregation 不再作为新点 |
| [SP4LP, 2025](https://arxiv.org/abs/2507.07138) | shortest-path sequence model，显式利用 pair 的最短路径 | “把一条最短路径序列喂给模型”直接淘汰；本轮只能研究 path-family interaction |
| [OCN, NeurIPS 2025](https://arxiv.org/abs/2505.19719) | higher-order CN 的 orthogonalization 与 normalization | 不再把 higher-order CN、去冗余、归一化或 CN order stacking 当新点 |
| [NodeDup, TMLR 2025](https://research.snap.com/publications/node-duplication-improves-cold-start-link-prediction.html) | low-degree node duplication、multi-view cold-start augmentation | 不做节点复制、低度增强或 cold-start augmentation |
| [Link-MoE, NeurIPS 2024](https://arxiv.org/abs/2402.08583) | 多种 pairwise predictor/expert 及 pair-specific mixture | 不做 expert、mixture、soft route、pairwise gate |
| [MPLP, NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/hash/85970f7bbc821852c1d17052b88c2451-Abstract-Conference.html) | quasi-orthogonal message passing 估计 CN，且讨论 estimation variance | 不做 variance/confidence readout；需把“结构对象”与 MPLP 的估计器清楚区分 |
| [NCN/NCNC, ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/file/3efb4bdc6bfe13e1ff95b4407c37961d-Paper-Conference.pdf) | MPNN-then-SF、CN pooling、common-neighbor completion | 新点不能只是 CN completion、CN sum、CN feature + MLP |
| [Graphlet/motif LP, Patterns 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13366520/) | graphlet orbit-pair frequency、higher-order motifs、clique completion | generic motif count / graphlet orbit frequency 直接列为高危 collision |
| [LLwLC, AAAI 2026](https://ojs.aaai.org/index.php/AAAI/article/view/39044) | induced subgraph eigenbasis、vertex-deleted subgraph、Neumann eigenvalue constraints | 本轮谱候选必须是“candidate insertion operator response”，不能复现 vertex-deleted/eigenbasis 主线 |
| [Edge Proposal Sets, 2021](https://arxiv.org/abs/2106.15810) | 通过添加 proposal edges 改变整个图的拓扑以增强 predictor | 不把“先加预测边再训练”冒充 candidate-edge response |

这意味着本轮的可接受新对象必须满足：

`existing graph object A` → `candidate-conditioned structural response object B`

而不是：

`existing scalar features` → `MLP/attention/gate`

---

## 3. 全部 20 个候选（Stage 0 输出）

以下候选都以 `G^+_{uv}` 为概念参照，但**不把中心候选边 `(u,v)` 本身喂给 predictor**；只保留它使已有边、路径或局部算子发生的结构响应。`Signal probability` 是实验前先验评分，不是已测结果。

| ID | 候选结构对象 | Parent | Parent 缺失信息 / Information Addition Test | 提取成本 | 最危险 prior / 初判 |
|---|---|---|---|---:|---|
| E01 | **CECG：独占邻域交叉闭合图**。`A=N(u)\\N(v)`、`B=N(v)\\N(u)`，保留已有 `E(A,B)`；把每条 `a-b` 解释为插入 `uv` 后的 4-cycle witness，并保留 cross-edge 的连通/角色结构 | NCN/NCNC | Parent 有 CN/higher-order pooled evidence，但没有保留 `A-B` 之间哪些已有边彼此相连；`true` 应优于 pair-shuffled，且控制 CN/degree/AA/RA 后仍有增量 | 中 | IGLP 的 neighbor importance、OCN 的 higher-order CN；**结构对象不同，暂保留** |
| E02 | **CFI：cycle-family intersection graph**。插入 `uv` 后所有受影响的 `u-v` 路径成为 cycles；节点为 canonical path，边为路径共享内部边/节点 | NCN/NCNC + SP4LP control | Parent 可能看一条 shortest path 或 path count，但不看多条 route 的交叠/独立性 | 中高 | SP4LP；只保留“path family intersection”，不保留单一路径序列 |
| E03 | **ECR：affected-edge cohort response**。找出因 `uv` 插入而与中心边共同形成新 cycle/新局部 edge-role 的已有边，构成 rooted edge-incidence graph | NCN/NCNC | Parent 以 node/pair 为主，未显式建模“哪些已有边共同响应”；`true` vs edge-cohort shuffle | 中高 | line-graph LP / CSLG；不是 line graph alone，而是 candidate-conditioned affected-edge subgraph |
| E04 | **2ECB：two-edge-connected block response**。在 pair-local graph 中比较插入前后的 bridge tree / biconnected blocks，记录由 `uv` 连接或改变的 block 关系 | NCN/NCNC | Parent 没有 edge-connectivity / block membership 的 pair-local object；控制 connected/disconnected 和 SPD | 高 | persistent homology、global connectivity；需证明不是简单 reachability |
| E05 | **LSPR：local spectral projector response**。对 candidate-local adjacency/Laplacian 计算低阶 eigenspace projector `P_k(G^+)-P_k(G)`，保留子空间响应而非单一 eigenvalue | NCN/NCNC | Parent 不显式看到局部算子扰动；`true` vs eigenvector/projector shuffle | 高 | LLwLC、TopoLink；只在 vertex-deleted/eigenbasis collision audit 通过后保留 |
| E06 | **KCR：k-core peeling response**。插入 `uv` 后被重新纳入/升级的 core-peeling dependency forest，而非单个 core number | MPLP+/NCN | Parent 可能携带 degree，但不携带“插入一条边触发的 peeling dependency”；需控制 degree 和 component | 中高 | degree/community proxy；若 forest 退化为 scalar `Δcore` 则淘汰 |
| E07 | **NBR：non-backtracking operator response**。在局部 edge-state graph 上构造插入前后的 non-backtracking transition response，排除立即回退 walk | MPLP+ | MPLP/OCN 看 overlap/walk-like signal，但不显式保留 edge-state、tailless route structure | 高 | MPLP、OCN、higher-order path；必须与 ordinary walk 及 shortest path 对照 |
| E08 | **DEP：disjoint-route packing response**。插入后局部 `u-v` route 的 edge-disjoint / internally-disjoint packing decomposition，保留 route packing object | NCN/NCNC | Parent 看不到 routes 是否共享瓶颈；不是 route count，而是 packing/dependency | 高 | 2ECB、path-based LP；若只剩最大数量则淘汰 |
| E09 | **CCH：chordless-cycle response**。只保留插入 `uv` 后被 chord 化或新闭合的 induced chordless-cycle family 及其共享关系 | NCN/NCNC | CN 看到 triangles，OCN 看到 higher-order overlap，但不保留 inducedness/chord status | 高 | motif/cycle LP、BLANT-Predict；高危，先做 collision kill search |
| E10 | **BCR：boundary-cut response**。以 pair-local boundary 为对象，比较插入前后 local cut-tree / boundary edge partition，而非 community label 或 conductance scalar | NCN/NCNC | Parent 没有 candidate-specific boundary partition；控制 global component、degree、community proxy | 高 | GPEN/global position、community detection；只接受 partition object |
| E11 | **NCH：neighborhood cross-incidence hypergraph**。把 `A`、`B`、cross edges 与候选 closure 关系构成带 side-label 的 incidence hypergraph，保留 hyperedge overlap | NCN/NCNC | CN 是一个交集，NCH 保留 exclusive-side 的多元 incidence | 中高 | motif/hypergraph LP；禁止退化成 hyperedge count |
| E12 | **EOM：edge-orbit transition under insertion**。对 pair-local 4/5-node graphlet，记录已有边从 orbit `o_before` 到 `o_after` 的 transition multiset | NCN/NCNC | Parent 没有 edge-role transition；但不主张普通 orbit frequency | 中高 | BLANT-Predict 2026；**初筛不推荐，作为强 negative control** |
| E13 | **TFR：treewidth/fill-in response**。对 pair-local approximate tree decomposition，记录添加 `uv` 触发的 fill-in edge set 与 separator change | NCN/NCNC | Parent 不显式看到局部 separator / fill-in structure | 很高 | graphlet/subgraph methods；成本和稳定性风险大 |
| E14 | **HBR：homology barcode response**。对 candidate-local clique/flag complex 比较插入前后的 cycle-space/barcode change | NCN/NCNC | Parent 没有 topological complex object | 很高 | persistent-homology LP、TopoLink；直接 collision 风险高，不进入 Top5 |
| E15 | **EAS：edge-attachment signature**。以已有 edge `f` 到 `(u,v)` 的两端 attachment pattern 为节点，构成 candidate-rooted edge attachment graph，不计算全局 line graph | MPLP+/NCN | Parent 不保存“已有边如何分别挂到 u-side/v-side”；可检验 zero-CN pairs | 中 | edge-centric/line graph；若实现只做 edge embedding，淘汰 |
| E16 | **RSC：role-switch closure graph**。插入后，已有节点/边在 `u-side`、`v-side`、cross、cycle-interior 四类结构角色之间的迁移图 | NCN/NCNC | Parent 端点/邻域 pooling 不保存 role transition | 中 | TAGNN/BS-SubGNN 的 structural labels；必须是 insertion-induced transition，不是 static labels |
| E17 | **MCC：minimal closure complex**。从 `uv` 出发递归收集最小的边闭合结构，直到遇到重复 boundary；输出 canonical rooted complex | SEAL/NCN | Parent 的 fixed-hop pool 可能丢失“闭合后最小结构边界” | 中高 | SEAL/SE4LP/GPEN；必须证明不是普通 enclosing subgraph |
| E18 | **PIR：pairwise incidence rewiring**。将 `u`、`v` 的独占邻域作为两侧节点，加入已有 adjacency incidence；比较插入前后 side-to-side incidence topology | NCN/NCNC | Parent 没有独占邻域之间的 direct edge relation | 中 | E01 的等价表述风险高；只有在 hypergraph/role object 真不同才保留 |
| E19 | **SPF：shortest-path family, not sequence**。不是取一条 shortest path，而是对等长最短路径集合构造 intersection/edge-disjointness graph | NCN/NCNC + SP4LP control | Parent/SP4LP 可能只使用单一路径；family topology 是新增对象 | 中高 | SP4LP；与 E02 高度相关，二者最终只留一个 |
| E20 | **GSR：global structural response**。比较候选插入对全图低秩 connectivity/spectral response 的变化 | MPLP+/NCN | 形式上是 candidate-conditioned global operator | 很高 | GPEN、LLwLC、TopoLink；全局且昂贵，淘汰 |

### Stage0 前的即时淘汰

- E12 只有在“orbit transition 而非 orbit frequency”能显著区分时才不被 [BLANT-Predict](https://pmc.ncbi.nlm.nih.gov/articles/PMC13366520/) 直接覆盖。
- E14 与 persistent-homology 路线过近，默认淘汰。
- E17 若只是 SEAL enclosing subgraph 的另一种命名，淘汰。
- E18 若与 E01 产生同构的 `A-B` incidence object，合并，不允许两个名字重复占位。
- E19 与 E02 合并候选，不并行开发两个 shortest-path family 版本。
- E20 默认淘汰：global structural response 成本高，且与 GPEN/LLwLC/TopoLink 的危险碰撞过强。

---

## 4. Stage0：结构支持审计（尚未产生真实结果）

当前仓库没有完整下载的 Cora/CiteSeer/PubMed/OGB 原始图，因此本报告不填写任何虚构的结构计数。服务器认证未完成，Stage0 必须在固定服务器环境中执行后才能把候选升级。

### 4.1 每个候选必须输出的统计

对每个 dataset × protocol × split × seed，使用与 parent 完全相同的 candidate pairs，输出：

| 检查 | 必须记录 |
|---|---|
| 支持率 | 正/负 pair 中新对象非空的数量与比例；不能只报全体平均 |
| 结构规模 | object node/edge 数、连通块数、最大块占比、最大路径共享度等分布 |
| regime support | CN=0/1/>=2、degree tertile、SPD、component status 各 regime 的样本数 |
| label separation | 仅 train split：正负之间的 AUROC、AUPR、MRR/Hits proxy；不能碰 test label 做选择 |
| null control | node-side shuffle、edge-cohort shuffle、within-regime graph rewiring；保持 degree/CN 尽可能不变 |
| cost | 每 1k candidate 的 wall time、peak memory、缓存大小 |

### 4.2 Stage0 GO / KILL 门槛

候选只有同时满足以下条件才进入 Stage1：

1. 至少一个非 Cora/CiteSeer 数据集存在非空结构支持；
2. 目标 regime 内 train 正/负各不少于 200 个 pair，或明确使用全实体排名而非强行分箱；
3. 新对象在 CN=0 与 CN>0 至少有一个 regime 具有足够样本；
4. feature-only probe 相对 `CN + degree + AA + RA` 有稳定增量，且不是单一 seed；
5. shuffle/rewire control 的增量接近 0；
6. 新对象抽取成本不超过 parent inference 成本的 2 倍，除非增量证据明显；
7. 若新对象在所有 regime 都为空，直接 KILL，不用换模型拯救。

### 4.3 服务器执行命令约束

真实运行时应使用仓库既有的固定 split 与官方 candidate protocol，并写入新的隔离目录，例如：

```text
<fresh-remote-root>/structural_change_v3/stage0/
<fresh-remote-root>/structural_change_v3/stage1/
```

禁止复用 legacy manifest、禁止用 uniform negatives 替代 HeaRT/OGB candidates、禁止把 test label 用于结构阈值或候选选择。

---

## 5. Top 5：只保留“新结构对象”而不是旧模块变体

评分采用指定公式：

`Score = 0.25 Novelty + 0.35 EmpiricalSignalProbability + 0.20 ImplementationEase + 0.10 ExperimentalClarity + 0.10 PaperPotential`

这些分数是**检索后的先验排序**，不是实证结果。

| Rank | Candidate | New structural evidence | Parent | Existing info missing | Feature-probe potential | Collision | Score |
|---:|---|---|---|---|---|---|---:|
| 1 | E01 CECG | 独占邻域之间已有 cross-edge 的闭合图与连通/角色结构 | NCN/NCNC | CN 给出 shared witness，但不给 `A-B` direct relation | 高；尤其 CN=0/低 CN 的 4-cycle regime | IGLP/OCN/BLANT；可通过“cross-edge topology ≠ importance/count”区分 | **8.22** |
| 2 | E02 CFI | candidate insertion 后 cycle family 的路径交叠图 | NCN/NCNC | shortest path/count 不给 route overlap structure | 中高；需与 SP4LP 严格对照 | SP4LP、cycle LP | **7.83** |
| 3 | E03 ECR | candidate insertion 影响的已有 edge cohort 及 edge-incidence topology | NCN/NCNC | node pooling 不保留哪些已有边共同响应 | 中；edge-level signal 明确 | line graph/CSLG | **7.48** |
| 4 | E04 2ECB | bridge/biconnected block 的 candidate-conditioned response | NCN/NCNC | endpoint/CN 不给 edge-connectivity block structure | 中；可能只在稀疏/桥接 regime 有效 | persistent homology、community/connectivity | **7.24** |
| 5 | E05 LSPR | local Laplacian eigenspace 的 insertion response projector | NCN/NCNC | parent 不显式看到局部算子扰动 | 中；需更大图和稳定谱计算 | LLwLC/TopoLink/谱方法 | **7.08** |

### 为什么 E01 暂列 Top1

- 它确实改变了 structural object：从 shared-node/walk summary 变成 rooted `A-B` cross-edge graph；
- 它对 CN=0 pair 仍可能非空：`u-a-b-v` 是 3-hop route，插入 `uv` 后形成 4-cycle；
- 不需要 learnable gate、attention、expert 或额外传播深度；
- 可用确定性 graph-kernel/WL color refinement 生成固定维结构向量；
- 可在现有 parent 上做严格 `true / shuffled / degree-CN-matched` 控制，实验解释清楚；
- 成本主要是局部边枚举，不需要完整 line graph 或全局谱分解。

### E01 的主要风险

1. 在高同配 citation graph 中，`E(A,B)` 可能稀疏，信号不足；
2. SP4LP 或 SEAL 可能间接捕获部分 4-cycle route，必须做直接控制；
3. 若只使用 `|E(A,B)|` 或 component count，容易退化成被禁止的 scalar statistic；
4. 若 `Parent + CECG` 只在 Cora 上有效，不能升级为 architecture idea。

---

## 6. Top 3：只做 Stage0 / Stage1，不做完整新 GNN

### Top 1：E01 CECG

#### Stage0

对每个 query pair `(u,v)`：

```text
A = N(u) \ (N(v) ∪ {v})
B = N(v) \ (N(u) ∪ {u})
E_cross = {(a,b) ∈ E : a ∈ A, b ∈ B}
H_uv = (A ∪ B, E_cross, side-label A/B)
```

将 `E_cross` 解释为：在假设插入 `uv` 后，每条已有 cross-edge `a-b` 都与 `u-a`、`v-b` 一起形成 4-cycle witness `u-a-b-v-u`。不把 `uv` 自身加入 `H_uv` 的 readout。

固定输出：

- 2-step deterministic WL colors / side-aware color histograms；
- cross-edge induced connected components 的 rooted structure；
- 每个 cross-edge 的 endpoint-side role 与 shared-component relation；
- object size 只作为审计字段，不作为唯一模型输入。

Probe：

1. `CECG -> logistic regression`；
2. `CN + degree + AA + RA -> logistic regression`；
3. `CECG + CN + degree + AA + RA -> logistic regression`；
4. 在 matched CN/degree strata 内比较；
5. 对 `A`、`B`、cross-edge incidence 做 within-regime shuffle。

#### Stage1

固定 parent checkpoint/training protocol，比较：

```text
Parent
Parent + CECG(true)
Parent + CECG(within-regime shuffled)
Parent + raw cross-edge count only
Parent + one shortest-path control
```

只允许训练一个小型线性 decoder 或固定维 MLP probe；不加 attention/gate/expert/residual route。验收顺序：

1. `CECG -> label` 的 feature-only probe 在至少两个数据集/结构 regime 有增量；
2. `Parent + CECG(true)` 的增量高于 shuffled 与 raw-count control；
3. CN/degree/AA/RA 条件控制后仍存在；
4. 不以单一 Hits@K 支撑结论，同时报告 MRR、Hits@10/50/100、AUC、AP；
5. 结果不是由 candidate sampling 或 degree bias 单独解释。

### Top 2：E02 CFI

Stage0 只保留 canonical simple paths / shortest-path ties，构造：

```text
P_uv = {canonical u-v paths in the allowed local radius}
I_uv: path-nodes are P_uv; two path-nodes connect when they share an interior node/edge
```

Stage1 比较 `Parent + CFI(true)`、`Parent + CFI(path-family shuffle)`、`Parent + one-SP4LP path control`。若 CFI 只在 shortest-path length 或 path count 控制中消失，STOP；若只能靠 Transformer/sequence model 才有增量，也不进入第四个候选。

### Top 3：E03 ECR

Stage0 构造 rooted affected-edge graph：已有边是节点；两条已有边共享 endpoint、同属 candidate-induced closure、或在同一 local block 中则连边。中心候选边不作为节点输入。

Stage1 比较 `Parent + ECR(true)`、`Parent + edge-cohort shuffle`、`Parent + line-graph-only control`。只有当 ECR 的 candidate-conditioned affected-edge relation 高于 line graph alone 且不依赖 generic edge attention 时才继续。

---

## 7. Top1 研究卡：CECG

### 中文 / English title

**候选边诱发的独占邻域交叉闭合图用于链路预测**  
**Candidate-Edge-Induced Cross-Neighborhood Closure Graphs for Link Prediction**

### Parent

首选 **NCN/NCNC**；以 **MPLP+** 作为独立 parent control。NCN/NCNC 的直接 parent 事实来自其 MPNN-then-structural-feature、CN pooling 与 common-neighbor completion 设计；MPLP 的直接 parent 事实来自其用 message passing 估计 CN 的方法。

### 新增信息

对 candidate pair `(u,v)`，不是只问“有几个 common neighbors”，而是问：

> `u` 的非公共邻域与 `v` 的非公共邻域之间，已有边以什么拓扑组织起来？如果把 `(u,v)` 假设加入，这些已有 cross-edges 会形成怎样的 candidate-rooted 4-cycle closure graph？

形式上：

```text
A_uv = N(u) \ (N(v) ∪ {v})
B_uv = N(v) \ (N(u) ∪ {u})
H_uv = G[A_uv ∪ B_uv]
       restricted to edges crossing A_uv ↔ B_uv
```

CECG 的 readout 是 `H_uv` 的 side-aware rooted structural representation；`(u,v)` 只定义 root 和 hypothetical transformation，不作为一条普通输入边送入 readout。

### 为什么 parent 不能显式看到

- CN/NCN 只聚合 `N(u)∩N(v)` 的 witness；它不保存 `N(u)\\N(v)` 与 `N(v)\\N(u)` 之间的已有边关系；
- NCNC 解决的是 observed CN 的缺失/补全，不等于保留 exclusive-side cross-edge topology；
- MPLP 估计 pairwise overlap/walk-like structural values，但估计一个 overlap 不等于显式表示 cross-edge induced graph；
- degree、AA、RA 只提供 endpoint 或 witness weighting，不能恢复 side-labeled cross-edge connectivity；
- SP4LP 可作为“单条最短路径”控制，但 CECG 表达的是全部 cross-edge witness 的关系图。

### Exact difference

不是：

```text
old = CN / higher-order-CN scalar or pooled vector
new = old + cross-edge count / MLP / attention / gate
```

而是：

```text
old object = shared-witness / walk aggregation
new object = candidate-rooted, side-labeled cross-edge closure graph
```

### Deterministic extraction algorithm

1. 从固定 split 的 adjacency hash 取 `N(u)`、`N(v)`；
2. 构造 `A_uv`、`B_uv`，排除端点和已知 candidate edge；
3. 遍历较小侧的邻接表，枚举 `E_cross`；
4. 只在 `E_cross` 上建 `H_uv`，不构造完整 line graph；
5. 执行固定 2-step side-aware WL color refinement；
6. 输出固定维 color histogram、rooted component relation 和 edge-role transition；
7. 对 `H_uv` 做 deterministic within-regime shuffle 作为 null，不训练新 routing module。

复杂度近似为 `O(∑_{a∈A_uv} deg(a))` 或从较小侧枚举 adjacency，内存为 `O(|A|+|B|+|E_cross|)`；需要用缓存和 profiling 验证实际常数。

### Stage0

最低可接受输出不是一个总平均，而是：

- 每个 dataset/protocol/seed 的 `E_cross` 非空率；
- `|E_cross|`、component structure、WL representation 的分布；
- CN=0/1/>=2、degree tertile、SPD、component regime 的支持数；
- feature-only probe 的 AUROC/AUPR/MRR proxy；
- `CN+degree+AA+RA` 条件增量与 shuffled null；
- 1k candidate 的时间/峰值内存。

### Stage1

固定 parent，不改 split、negative candidate、loss、epoch budget 和 model seed matrix。至少运行：

```text
Parent
Parent + CECG(true)
Parent + CECG(within-regime shuffle)
Parent + raw |E_cross| control
Parent + one-shortest-path control
```

### Stage2（只有 Stage0/1 GO 后才允许）

最小架构只允许：

```text
h_parent(u,v) = frozen/standard NCN pair representation
r_cecg(u,v)   = deterministic CECG structural vector
score(u,v)    = Linear([h_parent(u,v), r_cecg(u,v)])
```

第一版不允许 gate、attention、expert、adaptive hop、auxiliary loss、contrastive objective、Transformer 或新的 message-passing branch。若必须增加复杂模块才能产生效果，则说明 CECG 本身没有被识别为独立证据，应停止。

### Compute budget

- Stage0：CPU local enumeration + cache；目标是比 parent inference 低常数级；
- Stage1：parent 的小规模复现 + probe，最多 2 个高 headroom 数据集、3 seeds；
- Stage2：仅在 Stage1 满足 GO 后，使用 parent 同等 epoch/batch/negative protocol；
- 不为候选单独构造完整 line graph，不做全图谱分解，不增加多专家副本。

### Success thresholds

CECG 只有在以下条件同时满足时才从“候选”升级为“值得第四模型”的方向：

1. feature-only probe 在至少 2 个数据集或 2 个明确结构 regime 中有正向增量；
2. `Parent + CECG(true)` 在至少 4/6 dataset-seed 配对中优于 Parent，且均值提升不是由单个 seed 驱动；
3. `Parent + CECG(true)` 明显优于 `Parent + shuffled` 与 raw-count control；
4. 控制 `CN/degree/AA/RA`、one-shortest-path 和 candidate sampling 后仍有增量；
5. 至少一个 Hits@10/50/100、MRR、AUC/AP 指标改善，不能只改善一个 saturated Hits@100；
6. 峰值内存增量 ≤10%，额外推理时间 ≤25%，除非收益在多个数据集上稳定且显著。

### Kill thresholds

命中任何一条即 STOP CECG：

- `E_cross` 在 headroom 数据集几乎总为空；
- feature-only probe 在控制变量后无增量；
- parent+true 与 shuffled 无差异；
- 所有收益都可由 `|E_cross|`、degree、CN 或 shortest-path proxy 解释；
- 只在 Cora/CiteSeer 单一 seed 或单一 negative sampler 上有效；
- 需要 attention/gate/expert/Transformer 才能产生增量；
- 额外成本超过门槛且没有跨 dataset 的收益；
- 直接被 SP4LP、SEAL、IGLP、BLANT-Predict 或新的 edge-centric prior 解释为同一 object。

---

## 8. Headroom 与数据选择

不能继续只依赖 Cora/CiteSeer 的 saturated primary metric。Stage0 先统计 parent 的 headroom：

- Hits@10、Hits@50、Hits@100、MRR、AUC、AP；
- hard-negative / fixed-candidate protocol；
- CN=0、CN=1、CN>=2 和 SPD regime；
- dataset 的实际 CECG support，而不是凭直觉选择数据集。

若某 dataset 的 parent primary metric 已超过 95%，只把它作为辅助稳定性检查，并增加 Hits@10/50、MRR、AUC/AP；不改变 test protocol。若 E01 的 cross-neighborhood support 在目标数据上不足，立即换数据集或换候选，不通过改阈值制造 support。

---

## 9. 最终阶段门

```text
Stage0 结构支持与 headroom 审计
  ├─ 无 support / 无 headroom / 高 collision → STOP
  └─ support 足够
       ↓
Stage1 feature-only + Parent/True/Shuffle/Proxy
  ├─ 无 incremental signal → STOP
  └─ 有 signal 且 null 通过
       ↓
Stage2 parent + deterministic structural object
  ├─ 未跨 dataset/seed 达标 → STOP
  └─ 达标后才允许设计第四个完整模型
```

本文件到此为止：**没有批准启动第四个完整 GNN，也没有把任何候选宣称为已证实创新。**

---

## 10. References used for this round

- [MPLP — Pure Message Passing Can Estimate Common Neighbor for Link Prediction](https://proceedings.neurips.cc/paper_files/paper/2024/hash/85970f7bbc821852c1d17052b88c2451-Abstract-Conference.html)
- [NCN/NCNC — Neural Common Neighbor with Completion for Link Prediction](https://proceedings.iclr.cc/paper_files/paper/2024/file/3efb4bdc6bfe13e1ff95b4407c37961d-Paper-Conference.pdf)
- [Link-MoE — Mixture of Link Predictors on Graphs](https://arxiv.org/abs/2402.08583)
- [OCN — Effectively Utilizing Higher-Order Common Neighbors for Better Link Prediction](https://arxiv.org/abs/2505.19719)
- [SP4LP — GNNs Meet Sequence Models Along the Shortest-Path](https://arxiv.org/abs/2507.07138)
- [GPEN — Global Position Encoding Network for Enhanced Subgraph Representation Learning](https://proceedings.mlr.press/v267/wu25l.html)
- [NodeDup — Node Duplication Improves Cold-start Link Prediction](https://research.snap.com/publications/node-duplication-improves-cold-start-link-prediction.html)
- [IGLP — Importance-guided Neighborhood Aggregation for Link Prediction](https://doi.org/10.1016/j.knosys.2026.116092)
- [TAGNN — Topology-aware Graph Neural Network Framework for Link Prediction](https://pmc.ncbi.nlm.nih.gov/articles/PMC13234321/)
- [BS-SubGNN — Subgraph Encoding with Bicentric Sphere Node Labeling and Pooling](https://ojs.aaai.org/index.php/AAAI/article/view/38490)
- [Cross-Scale Contrastive Learning with Subgraph and Line-Graph Views](https://doi.org/10.1016/j.physa.2026.131663)
- [Graphlet- and Motif-based Link Prediction in Large Networks](https://pmc.ncbi.nlm.nih.gov/articles/PMC13366520/)
- [LLwLC — Spectral Basis Learning for Expressive GNNs in Link Prediction](https://ojs.aaai.org/index.php/AAAI/article/view/39044)
- [Edge Proposal Sets for Link Prediction](https://arxiv.org/abs/2106.15810)
