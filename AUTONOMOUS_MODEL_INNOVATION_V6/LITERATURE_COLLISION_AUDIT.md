# V6 文献与结构碰撞审查

审查截止：2026-09-17。审查目标不是证明“未搜到即新”，而是判断候选是否已经具有明确的数学/代码先例。

## 1. 重点先行工作

| 工作 | 年份/来源 | 核心公式或传播结构 | 官方代码 | 与 V6 的结论 |
|---|---|---|---|---|
| SEAL | NeurIPS 2018 | 对目标边抽取 h-hop enclosing subgraph，DRNL 标签后用 GNN/读出器预测：`s(u,v)=MLP(Readout(G_uv))` | [muhanzhang/SEAL](https://github.com/muhanzhang/SEAL) | 目标边局部子图已是成熟 link-centric 路线。 |
| NCN / NCNC | 2023/ICLR 2024 | 先得节点表示，再对目标对及 common-neighbor 结构做显式聚合；NCNC 进一步完成缺失 CN | [GraphPKU/NeuralCommonNeighbor](https://github.com/GraphPKU/NeuralCommonNeighbor) | CN witness 与完成机制已覆盖。 |
| OCN | 2025 | Orthogonal Common Neighbor 与高阶 CN/邻居重叠结合 | [qingpingmo/OCN](https://github.com/qingpingmo/OCN) | 高阶 CN 不是可用的新传播对象。 |
| MPLP | NeurIPS 2024 | 用近似正交随机向量做消息传播，使 `z_u^T z_v` 估计共同邻居/联合结构 | [Barcavin/efficient-node-labelling](https://github.com/Barcavin/efficient-node-labelling) | 不能把“纯传播恢复 pair statistic”重新包装成新结构；MPLP-VC 也已失败。 |
| NBFNet | NeurIPS 2021 | Neural Bellman–Ford 式路径递推，沿关系/路径更新查询相关状态 | [DeepGraphLearning/NBFNet](https://github.com/DeepGraphLearning/NBFNet) | 路径/流式状态传播与历史 R1/R3 方向碰撞。 |
| 2-WL / Local 2-WL / 2-FWL / Local 2-FWL | 2022 | 2-FWL 的局部更新显式使用 `((r,q),(p,r))` 共享中间节点对 | [GraphPKU/2WL_link_pred](https://github.com/GraphPKU/2WL_link_pred) | T2WL-INC 是直接数学碰撞，已硬停止。 |
| SLRGNN | GRaM/PMLR 2024 | 把原图边作为 line-graph 节点；共享端点的边在 line graph 中相连 | [论文与 PDF](https://proceedings.mlr.press/v251/lachi24a.html) | edge-space/line-graph 链路表示已存在。 |
| LEAP | 2025 | Learnable topology augmentation，为节点/目标关系学习额外结构上下文 | [论文](https://arxiv.org/abs/2503.03331)，[代码](https://github.com/AhmedESamy/LEAP/) | “学习额外边再传播”与直接先行工作碰撞。 |
| TAGNN | Scientific Reports 2026 | 2-hop enclosing subgraph + DRNL + target-pair structural attention + 启发式特征 | [论文/代码链接](https://doi.org/10.1038/s41598-026-48184-0) | 目标对结构编码、普通 attention/特征拼接均已覆盖，且用户明确禁止单独采用。 |
| IGLP | Knowledge-Based Systems 2026 | 对目标链接的邻居按结构/特征重要性加权，含 Adaptive Neighborhood Aggregation 与 CN awareness | [论文](https://www.sciencedirect.com/science/article/pii/S095070512600818X) | 邻居选择/重要性加权与历史邻域方向碰撞。 |
| YinYanGNN | 2024 preprint | 负边进入 forward 的节点更新，再用 Hadamard-MLP 解码 | [论文](https://openreview.net/pdf?id=2M4GAkUkjA)，[作者代码仓库](https://github.com/yxzwang/SubmissionverOfYinYanGNN) | 负关系进入传播已是已有路线；V6 不改训练负样本制造结构。 |
| CORE | TKDD 2026 | Information Bottleneck 驱动的 complete/reduce，恢复缺失边、去除噪声后再做 LP | [论文](https://doi.org/10.1145/3789200)，[预印本](https://arxiv.org/abs/2404.11032) | 拓扑增广/图编辑不是独立的 V6 网络算子。 |

补充的结构相关先例包括 [HodgeNet](https://arxiv.org/abs/1912.02354) 及其[代码](https://github.com/dmsm/HodgeNet)，以及基于补图传播的 ECGN（[论文页面](https://www.sciencedirect.com/science/article/pii/S0950705122008899)，[代码](https://github.com/wubinzzu/ECGN)）。

## 2. 三个候选及硬停止

### C1：Complement-Context Message Passing（补图上下文传播）

**假设。** 普通 GCN 只聚合邻居，可能丢失“非邻居场”的信息；在目标边 masking 后，补图邻居传播或许能区分普通局部聚合难以区分的候选。

**拟议算子。** 对无自环简单图，令 `A^c=J-I-A`，尝试 `H^{l+1}=σ(D_c^{-1/2}A^cD_c^{-1/2}H^lW_l)` 或与 `A` 的差分传播。

**碰撞/反证。** ECGN/UGCN/SComGNN 已把原图与补图作为双图传播结构；因此该状态对象不是独立的。并且未归一化时有严格恒等式：

`A^c X = (J-I-A)X = 1(1^T X)-X-AX`。

这说明补图聚合可由全局特征和普通局部聚合的简单代理得到；归一化版本只增加度缩放，不自动产生独立机制。候选状态：`NOVELTY_COLLISION_STOP`，不进入机制测试。

### C2：Edge-Cochain / Non-backtracking Transport

**假设。** 把节点状态提升为有向边或边流状态，沿不回溯的相邻边传播，能够保留节点消息传递丢失的关系方向。

**拟议算子。** 边状态可写为 `e_{i→j}^{l+1}=φ(e_{i→j}^l, Σ_{k∈N(i)\{j}} e_{k→i}^l)`，目标分数由两个端点的边状态汇聚。

**碰撞/反证。** 该对象同时落入历史 R3-01 non-backtracking、line graph/edge incidence，以及 HodgeNet 的 edge-data/Hodge-Laplacian 先例；SLRGNN 已直接把 LP 转为 line-graph 表示。它不是一个待由 Cora 最小训练发现的新计算图。候选状态：`NOVELTY_COLLISION_STOP`。

### C3：Learned Topology-Residual Propagation

**假设。** 现有 GNN 使用固定观测图，若学习一个结构残差 `Δ_θ(X,A)` 并在 `A_θ=A+Δ_θ` 上传播，也许能恢复缺边的有效上下文。

**拟议算子。** `H^{l+1}=σ(N(A+Δ_θ(X,A))H^lW_l)`，其中 `Δ_θ` 只允许非目标边候选。

**碰撞/反证。** LEAP 已将 learnable topology augmentation 直接用于 link prediction；CORE 已将补边、去噪和信息瓶颈用于 link prediction。即使把它叫作 residual propagation，状态对象仍是 learned graph editing。候选状态：`NOVELTY_COLLISION_STOP`。

## 3. 审查结论

三个候选均在进入候选选择/合成图单元测试前被停止。没有“选定模型”，没有可以诚实地称为 V6 独立结构的实现；“没有发现完全同名论文”不构成 novelty 通过。

