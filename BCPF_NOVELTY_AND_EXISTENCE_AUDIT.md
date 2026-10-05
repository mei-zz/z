# BCPF / SILP Novelty and Existence Audit

审计日期：2026-09-15  
候选：Boundary-Conserved Pair Field（BCPF / SILP）  
范围：只做定向文献查重与小规模 synthetic diagnostic；不实现 learnable BCPF，不运行完整真实数据，不修改 DCDLP。

## A. Novelty verdict

**PASS（仅指 Part A 的“未发现核心同构”；投资许可仍为 FAIL）**。

本轮没有发现一篇工作同时具备以下四个条件：

```text
query-specific target pair
+ external graph reduction/elimination
+ boundary response/transfer operator
+ operator-conditioned local pair propagation
```

但这不是“Schur complement 新颖”。Schur/Kron、vertex elimination、Gaussian elimination、spectral graph reduction 和 boundary constraints 都是已知工具。BCPF 若有剩余新意，只能是非常具体的 information flow：对每个 `(u,v)` 的 enclosing-subgraph cut，把外部 `O` 对 boundary `B` 的作用压缩成 pair-specific response，并在内部 message passing 的每一层持续更新 boundary state。

Part A 的主要风险不是发现了完全同构论文，而是 GPEN、Fahrbach 和 NBFNet 分别覆盖了 BCPF 的三个关键面：global/boundary context、Schur reduction + link prediction、query-conditioned propagation。因此 novelty 只能算“暂定通过、强风险”，不能据此直接写论文。

文献入口： [Fahrbach et al., ICML 2020](https://proceedings.mlr.press/v119/fahrbach20a.html)、[GPEN, ICML 2025](https://proceedings.mlr.press/v267/wu25l.html)、[NBFNet, NeurIPS 2021](https://arxiv.org/abs/2106.06935)、[LLwLC, AAAI 2026](https://ojs.aaai.org/index.php/AAAI/article/view/39044)、[ELPH/BUDDY](https://arxiv.org/abs/2209.15486)、[SEAL](https://arxiv.org/abs/1802.09691)。

## B. Fahrbach 2020 collision

### Their method

Fahrbach et al. 将任务中的 **relevant vertices** 作为 terminals 保留，把 **irrelevant vertices** 逐步消去；消去过程使用 Gaussian elimination / Schur complement，得到包含 terminals 的更小加权图。论文证明该 coarsening 能保留与 terminal 相关的随机游走性质，并用于 graph embedding 的效率与空间压缩。其 link prediction 实验是在 terminal 集合上删除一部分 terminal-terminal edges，再用 LINE、NetMF 等 embedding 加 Hadamard 或 weighted-L2 edge embedding，最后用 logistic regression 预测边/非边；不是 query-specific enclosing-subgraph GNN。

### Our proposed method

```text
query pair (u,v)
  -> pair-specific interior I and cut boundary B
  -> outside O = G \ (I ∪ B)
  -> T_B(u,v), e.g. Schur/Kron boundary response
  -> update h_B at every local propagation layer
  -> message passing on I ∪ B
  -> pair score
```

### Exact same

- 都承认 Schur complement 可以消去不需要显式保留的顶点。
- 都用 reduced representation 保留某些 terminal/boundary 上的图性质。
- 都把图缩减与 link prediction / graph embedding 的效率或表示有关联。

### Exact different

- Fahrbach 的 terminal set 是全局 coarsening 的保留对象，目标是减少顶点、时间和空间；不是为每个目标 link 修复一个 enclosing-subgraph cut。
- Fahrbach 的 reduced graph 是 embedding 的输入；没有 `external reduced operator -> boundary state -> local pair message passing` 这条动态信息流。
- BCPF 的 `B`、`O` 和 operator 随目标 pair `(u,v)` 变化；Fahrbach 的核心算法不是为每个候选 link 构造不同的 pair-indexed boundary response。
- Fahrbach 的 LP 实验使用 LINE/NetMF 和 edge embedding + logistic regression，不是局部 pair GNN 中的 boundary condition。

### Reviewer attack

攻击句子：

> This work merely applies classical Schur-complement graph coarsening to a query-specific subgraph for link prediction.

若反驳只有“数据集不同、GNN 不同、每个 pair 单独计算”，则确实是 **COLLISION TOO STRONG**。目前唯一可成立的反驳是：BCPF 的研究对象不是 reduced graph 本身，而是将被截断的外部图作用转换成当前 query 的 boundary state transition，并持续进入 local pair propagation；这必须由 same-interior/different-exterior 实验和 parameter-matched ablation 证明。本轮 synthetic 结果没有证明该机制优于现有全局位置或 Schur-free 方案，因此不能把这个反驳当作已验证贡献。

## Collision Table

符号：`✓` 明确具备；`△` 部分接近但不是同一机制；`✗` 未发现。`Link prediction` 表示该工作是否直接把 LP 作为任务/实验，而不是仅可泛化。

| Prior Work | Problem | Schur/Kron | Query-specific | Boundary operator | During message passing | Link prediction | Collision |
|---|---:|---:|---:|---:|---:|---:|---|
| Fahrbach et al. 2020 | ✓ | ✓ | △ terminal set，非每个 pair | △ retained-terminal reduced graph，非 DtN state | ✗ | ✓ | L2：Schur + LP 很近，但不是 C1 信息流 |
| GPEN 2025 | ✓ | ✗ | ✓ subgraph instance | △ boundary-aware convolution，但不是外部等效算子 | ✓ | ✗ 直接 LP 不是其主任务 | L2：最强概念近邻，缺少 external-to-boundary reduction |
| NBFNet 2021 | △ | ✗ | ✓ query indicator | △ boundary condition 是初始化，不是 Schur boundary response | ✓ | ✓ | L2/L3：query-conditioned path propagation 已被占用 |
| LLwLC 2026 | ✓ vertex-deleted subgraph expressiveness | ✗ | ✓ query LP 的 `S/δS` | △ Neumann spectral boundary constraint | △ spectral basis/message representation | ✓ | L2：boundary + LP + spectral，但无外部 transfer dynamics |
| SEAL | ✓ local enclosing subgraph | ✗ | ✓ | ✗ hard crop | ✓ local GNN | ✓ | L1：只覆盖 query crop，不覆盖外部边界作用 |
| ELPH/BUDDY | ✓ redundancy/efficiency | ✗ | ✓ target-pair sketches | ✗ | △ sketch messages，不是 boundary operator | ✓ | L1/L2：高效保留结构统计，但无 DtN/Kron flow |

## C. GPEN collision

GPEN 的输入是整个图 `G` 与子图 `S`。它先通过 degree-based random walk 和层级树为节点构造 global position encoding，再使用 boundary-aware convolution，通过节点差分向量选择性地把全局结构信息整合到子图表示中，避免 global aggregation 破坏局部结构。[GPEN 官方论文页](https://proceedings.mlr.press/v267/wu25l.html)；其公开 PDF 的框架图明确显示了 `entire graph G + subgraph S`、global position encoding 与 boundary-aware convolution。[GPEN PDF](https://openreview.net/pdf?id=7QFmZ7i7sr)

### Exact overlap

- 都针对 local subgraph 不能表达远距离结构的问题。
- 都在 boundary 附近保留/控制全局结构影响。
- 都让外部信息在 subgraph representation 阶段发挥作用，而不是只在最终 decoder 之后出现。

### Exact non-overlap found

- GPEN 使用的是节点 global position 和 difference-vector gating；没有发现 `L_BB - L_BO L_OO^† L_OB` 或等价 Kron/DtN/network-response matrix。
- GPEN 的 boundary-aware convolution 不是针对每一个 link 的 outside graph elimination，也没有证明对每个 `(u,v)` 生成一个 boundary equivalent interaction。
- GPEN 主要是 subgraph representation learning，而不是 BCPF 所要求的 open-boundary LP diagnostic。

### Decision

GPEN 没有形成 Part A 的 exact core collision，但它已经覆盖“全图上下文 + boundary-aware integration”这一宽泛叙事。因此，BCPF 不能再声称“首次让 boundary 感知 global context”；唯一剩余的窄主张必须写成 **query-pair-specific external response operator**。本轮 GPEN-like proxy 在 synthetic test 上达到 aggregate AUC `0.8333`，已经足以使 BCPF 的实用独特性受到否定性压力。

## D. NBFNet collision

NBFNet 把 query indicator 注入传播，并将 pair representation 视为所有路径表示的 generalized sum；每条路径由 edge representation 的 generalized product 组成，整体通过 generalized Bellman-Ford 实现。[NBFNet](https://arxiv.org/abs/2106.06935)

它与 BCPF 的共同点是：预测目标会影响 message propagation，而不是只在最终 decoder 才出现。不同点是：NBFNet 做全图/关系路径传播，没有先把外部图消去为 boundary response，也没有 BCPF 的 `I/B/O` open-boundary decomposition。

synthetic 中的 NBFNet-lite 是透明的 path-count surrogate，不是声称复现训练好的 NBFNet。它在 Case A external return path 上达到 AUC `1.0000`，aggregate AUC `0.7778`。这已经说明“外部路径影响必须由 Schur boundary 才能访问”不成立；全图 query-conditioned path propagation 可以访问其中一类 failure。虽然它没有在本构造上完整解决三类外部差异，因此不是单独的“完全解决” kill 条件，但 BCPF 必须先超越它才能继续。

## E. LLwLC collision

LLwLC（Spectral Basis Learning for Expressive GNNs in Link Prediction）在 LP 中处理 vertex-deleted subgraphs，并显式定义 subgraph `S` 与 vertex boundary `δS`；其 Neumann eigenvalue constraints 使用 query 周围的局部区域和边界来提升 link-level expressiveness。[AAAI 2026 官方页面](https://ojs.aaai.org/index.php/AAAI/article/view/39044)、[论文 PDF](https://ojs.aaai.org/index.php/AAAI/article/download/39044/43006)

重合之处是：LP、vertex-deleted/local subgraph、boundary、谱数学和 expressiveness 都出现。关键差异是：LLwLC 约束/学习谱基，不是消去 `O` 后构造 `B` 上的 Schur/Kron response，也不是把外部 reduced operator 作为每层 boundary state update。故为 L2 collision，而不是 C1 exact isomorphism。

## F. Exact remaining novelty

如果只从文献信息流中提炼，剩余候选句子是：

> 对每个目标 pair `(u,v)`，把 enclosing-subgraph 外部图 `O` 对 cut boundary `B` 的影响压缩为 query-specific boundary response operator，并把该 operator 作为 boundary state transition 持续注入内部 pair message passing；它不是全局位置特征、静态 adjacency preprocessing 或普通 graph coarsening。

这句话满足了“Schur/Kron 本身不作为创新”的要求，也与 Fahrbach、GPEN、NBFNet、LLwLC 做了层级区分。但 Part B 未证明这条信息流在现有替代方案之上具有稳定、必要且可泛化的预测价值。因此它是 **remaining hypothesis**，不是可投资的 novelty claim。

## G. Synthetic construction

### Paired graph

每个 query 固定为 `(u,v)=(0,1)`。局部模板固定为：

```text
(0,2), (1,2),
(0,3), (3,7), (1,4), (4,7),
(0,5), (5,8), (1,6), (6,8)
```

其中节点 `2` 是唯一 common neighbor，`7,8` 是 distance-2 boundary。每张图总共 15 个节点，外部节点为 `9..14`。paired graphs 在以下方面完全相同：

- `S2` 节点数：9；
- `S2` 内部边数：10；
- interior edges、boundary nodes、DRNL-like distance roles；
- endpoint degree：`deg(0)=deg(1)=3`；
- common neighbors：`CN(0,1)=1`；
- 局部节点特征与 query role。

只改变 `7,8` 之外的外部拓扑，并在每个 case 内保持外部节点数、外部边数、boundary external degree 与外部 degree multiset 尽量匹配。测试集含 240 对图（480 graphs），训练/测试按 seed 分组，paired variants 不跨 split。

### Three external rules

1. **Case A — external return path**：`y=1` 当且仅当存在 `7-x-8` 的两边外部 return path；`y=0` 使用 `7-x-y-8` 的三边路径，同时匹配 degree multiset。
2. **Case B — external community coupling**：`y=1` 当且仅当外部节点 `9,10` 在 `O` 中属于同一 connected component；`y=0` 为两个外部三角社区。
3. **Case C — external bridge context**：`y=1` 当且仅当外部节点 `9,10` 的 edge connectivity 为 1；`y=0` 使用相同节点数、边数和 degree sequence 的 cycle-plus-chord，edge connectivity 大于 1。

标签由外部图性质计算，不使用 `if graph=A` 的图 ID 标签，也不改变 local term。这个 construction 成功产生 240/240 对 opposite labels，且 240/240 对 `SEAL k=2` signatures 完全相等。

## H. Baseline results

这些是可复现的 feature-level diagnostic，不是完整 SOTA 复现。所有学习型比较都使用同一 train/test split 和同一 logistic readout；没有实现 learnable Schur neural network。

| Method | AUC | Accuracy | Pair-MRR | mean D |
|---|---:|---:|---:|---:|
| CN | 0.5000 | 0.5000 | 0.5000 | 0.000000 |
| AA | 0.5000 | 0.5000 | 0.5000 | 0.000000 |
| RA | 0.5000 | 0.5000 | 0.5000 | 0.000000 |
| GCN-2 fixed diffusion | 0.5000 | 0.5000 | 0.5000 | 0.000000 |
| GraphSAGE-2 fixed diffusion | 0.5000 | 0.5000 | 0.5000 | 0.000000 |
| SEAL k=1 | 0.5000 | 0.5000 | 0.5000 | 0.000000 |
| SEAL k=2 | 0.5000 | 0.5000 | 0.5000 | 0.000000 |
| SEAL k=3 | 0.7222 | 0.6667 | 0.6667 | 0.219646 |
| SEAL k=4 | 0.7778 | 0.6667 | 0.6667 | 0.326143 |
| boundary scalar summary | 0.5000 | 0.5000 | 0.5000 | 0.000000 |
| GPEN-like global position proxy | 0.8333 | 0.6667 | 0.8333 | 0.354722 |
| NBFNet-lite walk counts, L=10 | 0.7778 | 0.6667 | 0.6667 | 0.333141 |
| A4 exact Schur boundary graph | 0.6111 | 0.5000 | 0.8333 | 0.231929 |
| A4 + SEAL k=2, same readout | 0.6111 | 0.5000 | 0.8333 | 0.232142 |

Accuracy 使用统一 `0.5` threshold；Pair-MRR 是每对 `(G0,G1)` 中正确标签的二候选排序诊断。`D=|s(G_1,u,v)-s(G_0,u,v)|`，并不是传统 benchmark metric。

## I. Same-interior distinguishability

形式化检查结果：

```text
all_k2_signatures_equal   = True
all_pair_labels_opposite   = True
n_pairs_checked            = 240
mean_k2_nodes              = 9.0
mean_k2_interior_edges     = 10.0
```

这证明了一个有限架构 failure：只接收 `S2` 的方法，不论 decoder 多强，都不能从输入中区分 paired graphs。CN/AA/RA、GCN-2、GraphSAGE-2、SEAL k=1/2 和 boundary scalar 的 `D=0`。

但这只证明“hard crop 会丢失可影响标签的外部变量”，不证明“Schur response 是必要的唯一修复”。GPEN-like proxy 的 `mean D=0.354722` 高于 A4 的 `0.231929`；A4 的 operator 确有逐 pair 非零差异，但没有形成稳定的全局标签方向。

## J. k-hop expansion comparison

| Crop | AUC | mean nodes/query | mean edges/query | runtime ms/query | peak Python memory MB |
|---|---:|---:|---:|---:|---:|
| SEAL k=1 | 0.5000 | 7.000 | 6.000 | 1.0754 | 0.1058 |
| SEAL k=2 | 0.5000 | 9.000 | 10.000 | 1.2788 | 0.0996 |
| SEAL k=3 | 0.7222 | 10.833 | 12.500 | 1.3334 | 0.1120 |
| SEAL k=4 | 0.7778 | 13.500 | 16.500 | 1.6276 | 0.1581 |

`k=3` 只稳定解决了 Case A：它能够看到 return-path 的第一层外部节点，但对 Case B/C 的 deeper external topology 仍不足。`k=4` 继续增加节点、边和开销，仍不能解决三类 case。故“直接扩大 k”不是在本构造上一次性完整解决，但它已经提供了相当便宜的部分修复；BCPF 若继续推进，必须证明在真实规模上其 boundary response 明显优于不断扩展 receptive field。

## K. Simple-boundary-summary comparison

使用以下 scalar：

```text
outside node count
outside edge count
boundary external neighbor count
boundary external degree
boundary-external edge count
total node/edge count
```

因为 paired graph 在这些统计量上被控制为相同，结果为：

```text
A2 boundary scalar summary: AUC=0.5000, mean D=0.000000
```

因此本 construction 支持 **P3：这些简单 scalar 不够**。但是这不能自动支持 BCPF，因为 GPEN-like global position 不是这些 scalar 的简单拼接，并且 aggregate AUC 达到 `0.8333`。逐 case 结果是：

| Method | A return path | B community | C bridge |
|---|---:|---:|---:|
| boundary scalar | 0.5000 | 0.5000 | 0.5000 |
| GPEN-like global position proxy | 1.0000 | 1.0000 | 0.5000 |
| NBFNet-lite | 1.0000 | 0.5000 | 0.5000 |
| A4 exact Schur | 1.0000 | 1.0000 | 0.0000 |

这里的 GPEN-like 结果是 PageRank/root-distance proxy，不应写成“官方 GPEN 在该 synthetic 上 AUC 0.8333”；它的用途是测试 global-position 类替代方案是否已经能够恢复外部信息。

## L. Exact Schur baseline

对 `B=(7,8)`、`O=(9..14)` 构造外部 Laplacian blocks：

$$
L_{\mathrm{eff}}=L_{BB}-L_{BO}L_{OO}^{\dagger}L_{OB}.
$$

未学习 operator；使用 Moore-Penrose inverse 处理外部图块，并将 `L_eff` 的 entries/effective coupling 作为 A4 boundary graph representation，使用与其他 feature baseline 相同的 logistic readout。典型 effective coupling 如下：

| Case | y=0 coupling | y=1 coupling | observation |
|---|---:|---:|---|
| A return path | 0.3333 | 0.5000 | Schur 可见两边/三边外部通道差异 |
| B community coupling | 0.0000 | 0.2857 | Schur 可见外部是否连通 |
| C bridge context | 0.3846 | 0.3333 | bridge 标签方向与前两类相反 |

Schur operator 在每个 case 内通常有非零 distinguishability，但 aggregate AUC 只有 `0.6111`，低于 GPEN-like proxy `0.8333`、SEAL k=4 `0.7778`；A4 + SEAL k=2 仍为 `0.6111`，没有产生额外收益。

更严重的是 cross-case representation collision：Case A 的 `y=0` coupling `0.3333` 与 Case C 的 `y=1` coupling `0.3333` 相同。仅观察这个 exact 2-boundary Schur operator，无法从这两个样本恢复标签。这个结果直接否定了“只要把 outside 压成 exact Schur boundary graph 就足够”的普遍主张。

因此 P6 不通过：本轮 A4 没有显著优于 A1/A2/A3，且在统一 readout 下弱于 A3。没有理由继续实现 learnable transfer operator。

## M. Runtime / memory

以下测量来自 480 个 test graphs 的小规模 CPU diagnostic；`peak Python memory` 是 `tracemalloc` 峰值，不等价于生产系统 RSS/GPU memory，不能外推到大图，仅用于相对比较。

| Method | nodes/query | edges/query | runtime ms/query | peak Python MB |
|---|---:|---:|---:|---:|
| CN | 15.000 | 17.333 | 0.0038 | 0.0007 |
| AA | 15.000 | 17.333 | 0.0069 | 0.0007 |
| RA | 15.000 | 17.333 | 0.0068 | 0.0007 |
| SEAL k=2 | 9.000 | 10.000 | 1.2788 | 0.0996 |
| SEAL k=3 | 10.833 | 12.500 | 1.3334 | 0.1120 |
| SEAL k=4 | 13.500 | 16.500 | 1.6276 | 0.1581 |
| boundary scalar | 15.000 | 17.333 | 0.2512 | 0.1258 |
| GPEN-like position proxy | 15.000 | 17.333 | 12.1789 | 0.0537 |
| GCN-2 | 15.000 | 17.333 | 0.4297 | 0.0279 |
| GraphSAGE-2 | 15.000 | 17.333 | 0.5262 | 0.0158 |
| NBFNet-lite | 15.000 | 17.333 | 0.1282 | 0.0090 |
| A4 exact Schur | 8.000 | 7.333 | 0.2894 | 0.0067 |

A4 的 operator 计算在此小图上便宜，但“便宜”不等于“有用”：它没有在相同 readout 下产生超过 global position 或更大 crop 的预测增益。真实大图还需考虑每个 pair 的 outside extraction、Laplacian solve/pseudoinverse、缓存和近似误差；本轮不对这些工程外推做正面假设。

## N. Final verdict

**STOP BCPF**

