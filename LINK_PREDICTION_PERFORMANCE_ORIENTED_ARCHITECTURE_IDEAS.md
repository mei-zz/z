# Link Prediction Performance-Oriented Architecture Ideas

> 检索与决策日期：2026-09-15  
> 任务边界：只做文献检索、gap analysis、架构候选排序和最小实验规划；本报告不实现代码、不报告虚构实验结果，也不改变当前 DCDLP 工程。  
> 策略重置：本轮不延续 BCPF；BCPF 的上一轮结论仍是 STOP。

## 0. 决策摘要

本轮把问题重新定义为：在链路预测（LP）中，能否从一个已有强基线的单一结构模块出发，以极小代码改动保留可扩展性，并在不同类型的节点对上减少结构估计误差或信息丢失？

最终建议先做：

1. **MPLP-VC：不确定性感知的准正交结构通道**，以 MPLP/MPLP+ 为父模型；利用多个准正交估计块的 pair-level agreement 估计结构特征不确定性，再让解码器同时看到均值和置信度。它直接针对 MPLP 论文自己指出的“图结构导致的估计方差”问题，改动小、消融清楚。
2. **NCN-CNDP：公共邻居分布池化**，以 NCN 为父模型；在公共邻居和向量求和之外保留方差/低阶矩，避免不同的公共邻居集合被压缩成同一个和向量。
3. **HL-GNN-PDG：节点对条件的多范围传播门控**，以 HL-GNN 为父模型；只给共享 backbone 增加 pair-conditioned layer gate，不复制 Link-MoE 的多专家结构。

这三个方向都遵循：

Idea → V0 最小实现 → Cora/Citeseer 三种 seed → 主指标和稳定性判断 → GO/STOP

本报告的评分是文献证据约束下的先验排序，不是实验结果。任何候选只有在与父模型完全一致的数据划分、负采样、评价指标和调参预算下复现实证提升，才可进入论文级阶段。

### 0.1 5W1H 与 SMART 研究问题

- **What**：改进 LP 中结构证据的估计、压缩或 pair-specific 融合。
- **Why**：近年的强模型反复证明公共邻居、局部结构、节点对信息和多范围传播有效，但也暴露了公共邻居缺失、sketch 方差、特征噪声、过度压缩和 pair heterogeneity 等可利用的性能瓶颈。
- **Who**：需要强指标、低实现成本和清晰消融的单人/小团队 LP 研究项目。
- **When**：先用 1–2 周完成三组 V0 小实验；只有出现可复现的主指标提升，才扩展到 OGB 规模。
- **Where**：第一阶段 Cora、Citeseer 或当前项目已有数据集；第二阶段至少覆盖一个稀疏图和一个大规模 OGB link-property benchmark。
- **How**：以已公开代码的 NCN、MPLP 或 HL-GNN 为父模型，只添加一个可隔离模块，固定协议，多 seed，按 GO/STOP 门槛筛选。

SMART 问题是：**在不改变父模型训练协议且额外计算开销不超过约 20% 的条件下，V0 是否能在 Cora 和 Citeseer 的主 LP 指标上相对父模型取得跨 3 个 seed 的稳定正提升，并在至少一个按公共邻居数/节点度分组的子集上解释提升来源？**

## 1. Current high-performing LP architectures

下面把“强”分成两类：一类是已经有公开代码、可作为复现实验父模型的成熟路线；另一类是 2025–2026 的新近工作，适合作为碰撞审查和趋势判断。论文之间的数据集、split、negative sampler 和 metric 不完全一致，不能把下表数字当成统一排行榜。

| 路线 | 已验证的有效组件 | 文献暴露的限制 | 本轮可利用的缺口 |
|---|---|---|---|
| **SEAL** | enclosing subgraph、DRNL/结构标签、pair-specific 子图编码 | 动态抽子图昂贵；大规模测试可能成为瓶颈 | 在不引入完整 Transformer 的情况下做 hop/结构组池化 |
| **Neo-GNN / BUDDY / ELPH** | 可预计算的结构启发式、sketch、节点属性与结构通道 | ELPH 的内存/规模限制；BUDDY 与 ELPH 没有在所有数据集上同一胜出；sketch 有近似误差 | 使用 sketch agreement 或 residual 作为置信度，而不只是拼接 sketch |
| **NCN / NCNC** | MPNN 节点表征后显式聚合 common-neighbor embeddings；NCNC 进一步补全缺失公共邻居 | NCN 在无 observed CN 时退化为 GAE；补全 CN 可能带入噪声；只保留 CN 的和，丢掉集合分布 | CN 分布统计、observed/completed 分离、结构—属性残差门控 |
| **MPLP / MPLP+** | 准正交向量在消息传递后估计 pair-level 结构特征，低成本替代 one-hot 标签 | 估计偏差受节点度影响；图结构导致的 estimator variance 仍存在；随机向量影响 unseen-node 泛化 | 用独立 estimator block 的 agreement 做 pair-level uncertainty calibration |
| **LPFormer** | pair-specific PPR relative positional encoding、attention、node/feature/heuristic 融合 | PPR 矩阵在 Citation2 等大图上有内存与预处理压力；组件效果强数据集依赖 | 仅把 PPR 当作轻量 CN/范围校准器，不复制完整 Transformer |
| **Link-MoE** | pair-level gate 在多个 GNN/结构/属性 experts 之间选择 | 一个适用于全部 pair 的专家集合仍有冗余；完整专家并行的工程和计算成本更高 | 单 backbone 的 pair-conditioned range/route gate |
| **HL-GNN** | 多层 local/global propagation 与自适应层权重；深层传播范围可调 | 全局 layer weight 对所有 pair 共享；深层传播仍可能把不相关远邻带入 | 让范围权重按 pair 变化，但保持共享传播主干 |
| **SIEG / TAGNN** | structure-first、邻居特征抑制或分离、pairwise heuristic/structural transformer | 结构与属性的选择仍高度依赖数据集；完整 pairwise module 容易和现有工作重叠 | 只学习 attribute residual，结构通道保持不可关闭 |
| **OCN** | 更高阶 common neighbors 的 orthogonalization 与 normalization，减少冗余和过平滑 | 直接 concat 多阶表示明显弱于其处理后的交互；正交化/归一化本身已是直接 prior | 只研究不同 order 表示之间的低秩交互，不再提出另一个 OCN |
| **GPEN** | local subgraph + global position、hierarchical tree position、boundary-aware convolution | 全局位置与边界感知已成为近期强的 subgraph 表征先验 | 不再做“local + global 拼接”；只从局部结构的可靠性统计切入 |
| **SP4LP** | 沿 shortest path 的序列建模与 GNN encoding | shortest-path sequence modeling 已是直接强 prior；复杂度和实现成本较高 | 只使用低阶 path reliability/diversity statistics 作轻量校准 |
| **IGLP（2026）** | Adaptive Neighborhood Aggregation + Common Neighborhood Awareness，按结构和属性估计邻居重要性 | “邻居重要性/选择”方向已有直接近期工作 | 避免 top-k/importance attention，转向集合二阶统计或估计不确定性 |

证据来源： [NCN/NCNC（ICLR）](https://proceedings.iclr.cc/paper_files/paper/2024/file/3efb4bdc6bfe13e1ff95b4407c37961d-Abstract-Conference.html)、[MPLP（NeurIPS）](https://proceedings.neurips.cc/paper_files/paper/2024/hash/85970f7bbc821852c1d17052b88c2451-Abstract-Conference.html)、[OCN](https://arxiv.org/abs/2505.19719)、[ELPH/BUDDY](https://arxiv.org/abs/2209.15486)、[LPFormer](https://arxiv.org/abs/2310.11009)、[Link-MoE（NeurIPS）](https://proceedings.neurips.cc/paper_files/paper/2024/hash/1d0bcb52067128f826c86db234280dce-Abstract-Conference.html)、[HL-GNN](https://arxiv.org/abs/2406.07979)、[GPEN（ICML 2025）](https://proceedings.mlr.press/v267/wu25l.html)、[TAGNN（2026）](https://doi.org/10.1038/s41598-026-48184-0)、[IGLP（2026）](https://doi.org/10.1016/j.knosys.2026.116092)。

## 2. Structural components with proven empirical gains

### 2.1 反复出现的正向证据

1. **显式 pair-level common-neighbor evidence**：NCN 的消融显示，在 GAE 上加入 CN 已能带来显著提升，NCN 再通过 MPNN 后的 CN 表征取得额外收益。其关键不是更深的普通 MPNN，而是保留“哪些节点同时连接两端”的 pair-specific 证据。
2. **结构估计优于盲目增加 MPNN 深度**：MPLP 说明 quasi-orthogonal signatures 可以低成本估计链接结构量；NCN 也报告高阶邻域在加入 MPNN 后的边际收益有限。意味着下一步更值得修复结构读出质量，而不是继续堆层。
3. **结构冗余与过平滑需要同时处理**：OCN 的 orthogonalization 和 normalization 都有实证价值；其消融中简单 concat 多阶 CN 明显较弱。这为“结构通道之间的交互/不确定性”留下空间，但不能再把 OCN 的正交化换个名字重复一次。
4. **不同节点对确实需要不同信息**：Link-MoE 的 pair-level gating、LPFormer 的 pair-specific PPR/RPE、HL-GNN 的局部—全局消融共同支持 pair heterogeneity。剩余机会是把 gate 放在更低成本的共享 backbone 上。
5. **节点特征有条件地有效**：LPFormer、SIEG、TAGNN 和异配图 LP 研究均表明，邻居特征的收益随数据集和 homophily 变化；不能默认把所有邻居属性与结构求和到同一向量。
6. **结构通道在稀疏/冷启动场景尤其重要**：NodeDup 报告低度和孤立节点上的显著改善；NCNC 说明 graph incompleteness 会直接损失 CN。低 CN、低度、跨社区和 noisy-neighbor 子群应成为第一轮误差分组。
7. **效率本身是架构可用性的约束**：SEAL 的动态子图、LPFormer 的 PPR 处理和 ELPH 的内存边界说明，任何“可能提升”的模块若需要额外全图 pair matrix 或每条边完整子图，都不适合本轮 performance-first 快速筛选。

### 2.2 证据到设计空间的映射

| 已知收益 | 不能直接重复的做法 | 剩余可测试设计 |
|---|---|---|
| CN 的显式聚合 | 再做一个 CN branch 或 CN attention | CN 集合分布、可靠性、observed/completed 语义分离 |
| 多阶 CN | 再做 orthogonalization、normalization 或 raw concat | 阶间低秩交互、按 pair 的 order mixing |
| pair-specific gate | 再做多专家 ensemble 或 heuristic attention | 单共享 backbone 的轻量 range gate |
| local + global | 再拼接全局位置与局部子图 | 只用低维 global statistic 校准局部证据 |
| 节点属性与结构融合 | 再把两者 concat | 结构主通道 + 只在必要时开启的 attribute residual |
| sketch / random signatures | 再增加 sketch 维度 | 用 estimator agreement 估计置信度和异方差 |

### 2.3 明确的 gap 类型

- **方法 gap**：强 structural estimator 仍把 pair-dependent variance 当作普通 feature；模型知道数值，却不知道数值是否可靠。
- **表示 gap**：CN 聚合普遍偏向 sum/concat，集合内部的异质性、离散度和 witness redundancy 被压扁。
- **融合 gap**：已有方法证明 pair heterogeneity，但许多 gate 仍作用于完整 experts 或完整 Transformer，单 backbone 的低成本实现研究不足。
- **数据条件 gap**：observed CN、completed CN、远程 path 和邻居 attribute 的可靠性不同，现有系统常用同一个解码器直接混合。
- **实验 gap**：论文常报告总体指标，较少把提升分解到 CN=0/1/多、低度/高度、同社区/跨社区等子群；这是判断是否是真正结构改进而非整体调参的必要审计。

## 3. Remaining exploitable architecture gaps

### 3.1 优先保留的五条缺口

**G1：pair-level structural uncertainty。** MPLP 的理论分析明确指出 estimator variance 依赖图结构，单纯 DotHash/增加 signature dimension 并不能消除所有结构方差。最小可行问题是：同一 pair 的独立估计块是否可作为可靠性信号？

**G2：common-neighbor set distribution。** NCN 的 CN sum 很有效，但只给和向量会让“少量高度一致的 witness”和“大量相互无关的 witness”难以区分。最小可行问题是：在固定 MPNN 和 decoder 的情况下加入二阶矩，是否能在 CN-rich/heterogeneous 子群获益？

**G3：shared-backbone pair-adaptive range。** HL-GNN 的全局层权重和 Link-MoE 的 pair gate 都说明范围/信息类型应因 pair 而异，但两者之间仍有一条低成本路线：共享每一层表示，只让 pair 决定读出混合比例。

**G4：observed/completed evidence semantics。** NCNC 的补全解决了 graph incompleteness，但 observed CN 与 inferred CN 的证据强度不同。将二者强行求和会把补全误差传播给结构通道；分离是比“再设计一个补全器”更小的架构问题。

**G5：structure-first attribute residual。** SIEG、TAGNN 和 heterophily LP 结果表明邻居特征既可能有用，也可能是噪声。可把结构 evidence 作为永不关闭的主通道，把属性只作为可被 pair profile 调节的 residual；这比完全删除 neighbor feature 或建立完整双塔更容易作清晰消融。

### 3.2 本轮不再作为主线的方向

以下方向已有直接或高度相似的强 prior，除非后续实验发现完全不同的失败模式，否则不应作为“新创新点”包装：

- 仅把 GNN、Transformer、PPR、shortest path、attention 做普通拼接；
- 仅对高阶 CN 做 orthogonalization、normalization 或 concat；
- 仅做 pair-level multi-expert gating；
- 仅做 local subgraph + global positional encoding；
- 仅把 shortest path 变成 sequence encoder；
- 直接复现 NodeDup 的全局节点复制；
- 继续推进 BCPF；
- 只增加深度、hidden dimension 或随机投影维度而没有新的可检验机制。

## 4. 15 performance-oriented architecture ideas

### 4.1 参考文献缩写

下列卡片中的“最近 5 篇”使用这些缩写，链接集中列出以避免重复长 URL：

- **[NCN]** [Neural Common Neighbor](https://arxiv.org/abs/2302.00890)；**[NCNC]** 同一工作中的 Common Neighbor Completion。
- **[MPLP]** [Message Passing Link Prediction（NeurIPS 2024）](https://proceedings.neurips.cc/paper_files/paper/2024/hash/85970f7bbc821852c1d17052b88c2451-Abstract-Conference.html)。
- **[OCN]** [Orthogonalized Common Neighbors](https://arxiv.org/abs/2505.19719)。
- **[ELPH/BUDDY]** [Efficient Link Prediction with Hashing / BUDDY](https://arxiv.org/abs/2209.15486)。
- **[LPFormer]** [Link Prediction with Transformer](https://arxiv.org/abs/2310.11009)。
- **[Link-MoE]** [Link-MoE（NeurIPS 2024）](https://proceedings.neurips.cc/paper_files/paper/2024/hash/1d0bcb52067128f826c86db234280dce-Abstract-Conference.html)。
- **[HL-GNN]** [Heterogeneous Long-range GNN for LP](https://arxiv.org/abs/2406.07979)。
- **[SIEG]** [Structure Information Enhanced Graph Neural Networks](https://ojs.aaai.org/index.php/AAAI/article/view/29417)。
- **[TAGNN]** [Topology-aware Graph Neural Network for LP（2026）](https://doi.org/10.1038/s41598-026-48184-0)。
- **[GPEN]** [Global Position Encoding Network（ICML 2025）](https://proceedings.mlr.press/v267/wu25l.html)。
- **[Hetero-LP]** [Link Prediction with Heterophily（NeurIPS 2024）](https://proceedings.neurips.cc/paper_files/paper/2024/hash/79353864175b6b8c3d073cde84d7014a-Abstract-Conference.html)。
- **[NodeDup]** [Node Duplication Improves Cold-start Link Prediction（TMLR 2025）](https://research.snap.com/publications/node-duplication-improves-cold-start-link-prediction.html)。
- **[SP4LP]** [GNNs Meet Sequence Models Along the Shortest-Path](https://arxiv.org/abs/2507.07138)。
- **[IGLP]** [Importance-guided Link Prediction（2026）](https://doi.org/10.1016/j.knosys.2026.116092)。
- **[Cross-links]** [Cross-links Matter for Link Prediction（NeurIPS 2023）](https://proceedings.neurips.cc/paper_files/paper/2023/hash/fba4a59c7a569fce120eea9aa9227052-Abstract-Conference.html)。
- **[LP pitfalls]** [Evaluating GNNs for Link Prediction: Current Pitfalls and New Benchmarking](https://proceedings.neurips.cc/paper_files/paper/2023/hash/0be50b4590f1c5fdf4c8feddd63c4f67-Abstract-Datasets_and_Benchmarks.html)。

评分含义：Novelty、Implementation Ease、Improvement Probability、Experimental Clarity、Paper Potential 均为 0–10；“Collision”是与最接近工作的概念碰撞风险，不是审稿结论。

### Idea 1 — MPLP-VC：不确定性感知的准正交结构通道

- **Parent model**：MPLP/MPLP+。
- **核心架构**：将同一 propagated signature 划成 K 个独立块，对每个节点对计算 q_k(u,v)；解码器接收 μ=mean(q_k)、log σ²=log(var(q_k)+ε) 和可选的标准化得分 μ/(σ+ε)。V0 不改消息传递、不增加 loss，只改 pair readout；V1 再加入一个小型 heteroscedastic gate。
- **Performance Rationale**：MPLP 已证明准正交向量能有效承载 link-level structural features，同时明确分析了 pair degree 和 graph structure 引起的 estimator bias/variance。把“估计值”和“估计可靠性”分开输入，最直接地针对这个已公开 failure mode；稀疏图、低 CN pair 和度分布长尾 pair 最可能受益。
- **Expected Gain**：中高；预期首先体现为 MRR/Hits 的稳定性和低 CN 子群提升，而不保证所有数据集同幅度提高。
- **Minimum code change**：只改 signature-to-pair estimator 与 decoder input shape；K 个 block 共享同一消息传递。V0 约为一个统计量层；V1 才增加 gate。
- **V0 / V1**：V0 mean + logvar；V1 inverse-variance weighted mean + learned confidence gate，仍不引入新专家。
- **Closest 5**：MPLP、ELPH/BUDDY、NCN、OCN、LPFormer。
- **Most dangerous prior**：MPLP 自身的 use_degree/minimum_degree_onehot 与 DotHash variance reduction。
- **Exact difference**：不是提出新的 quasi-orthogonal vector，也不是再加 degree one-hot；而是用同一次传播中的 independent estimator agreement 构造 pair-level uncertainty channel。
- **Collision**：L1（强邻近扩展，需明确强调 confidence calibration 是独立贡献）。
- **Scores**：Novelty 7.5；Ease 9.0；Improvement Probability 8.0；Clarity 9.0；Paper Potential 7.5。

### Idea 2 — NCN-CNDP：公共邻居分布池化

- **Parent model**：NCN；可在 NCNC 上做第二版。
- **核心架构**：保留 sum_{w∈CN(u,v)} h_w，同时计算逐维二阶矩/方差 Var({h_w})，用 [endpoint interaction, CN sum, CN variance] 替换原 CN readout。V0 仅加逐维 variance；V1 再加入低秩 covariance 或按 witness role 分组的矩。
- **Performance Rationale**：NCN 证明 CN embedding 本身比纯 CN count 更有用，但 sum 会丢掉 witness 集合的离散度。两个 pair 即使 CN 数相同、sum 接近，CN 的语义一致性和结构角色也可能不同。该方向利用第一阶 CN 的已知收益，避开 OCN 的“高阶 CN 正交化”重复。
- **Expected Gain**：中高；在 CN-rich 且公共邻居质量异质的数据集上更有希望，低 CN 数据集可能接近零收益。
- **Minimum code change**：CN pooling 函数内多一个 streaming second-moment accumulator；不需要保存全部 CN 节点，也不增加全图 pass。
- **V0 / V1**：V0 sum + variance；V1 sum + variance + low-rank cross-moment。
- **Closest 5**：NCN/NCNC、OCN、IGLP、LPFormer、SIEG。
- **Most dangerous prior**：IGLP 的邻居重要性/选择和 OCN 的结构冗余处理。
- **Exact difference**：不是对每个 CN 做 attention/top-k，也不是按重要性选择邻居；只增加 permutation-invariant 的集合二阶统计，保留所有 CN。
- **Collision**：L1–L2。
- **Scores**：Novelty 7.0；Ease 9.0；Improvement Probability 7.5；Clarity 9.0；Paper Potential 7.5。

### Idea 3 — HL-GNN-PDG：节点对条件的多范围传播门控

- **Parent model**：HL-GNN。
- **核心架构**：HL-GNN 产生共享的多层表示 H^1...H^L；用低维 pair profile（CN、AA/RA、SPD、PPR 或 feature similarity 中固定的一小组）生成 β_l(u,v)，只在 link decoder 前做 pair-conditioned layer mixture：z_uv=Σ_l β_l(u,v)·readout_l(u,v)。
- **Performance Rationale**：HL-GNN 的 local-only/global-only 消融支持 adaptive range mixing；Link-MoE 说明 pair-specific information selection 有效。把 gate 放在共享层输出上，可得到相同方向的 pair heterogeneity，而不付出多专家并行成本。
- **Expected Gain**：中高；对局部同配 pair 与跨社区/长程 pair 的混合分布最有希望。
- **Minimum code change**：把 HL-GNN 当前全局 β_l 改为 batch pair 的 β_l(u,v)，不改变每层 propagation。
- **V0 / V1**：V0 一个 softmax pair gate；V1 分开 structural-range gate 与 attribute-range gate。
- **Closest 5**：HL-GNN、Link-MoE、LPFormer、TAGNN、NBFNet/SEAL 类 pair-specific LP。
- **Most dangerous prior**：Link-MoE 的 pair-level expert gating。
- **Exact difference**：没有多个完整 GNN experts，也不学习 heuristic expert ensemble；只有一个共享 backbone 的 pair-conditioned readout range gate。
- **Collision**：L2（概念相邻，但实现粒度不同）。
- **Scores**：Novelty 6.5；Ease 8.0；Improvement Probability 8.5；Clarity 9.0；Paper Potential 7.5。

### Idea 4 — NCN-STR：结构主通道 + 属性残差门

- **Parent model**：NCN/NCNC。
- **核心架构**：CN structural branch 始终保留；把 1-hop neighbor feature 与 endpoint feature 先分离编码，只把 attribute residual 按 pair profile 门控后加到 NCN score 上。属性门不允许关闭结构分支。
- **Performance Rationale**：SIEG/TAGNN 和 heterophily LP 结果均说明邻居特征可能是噪声，也可能在特定数据集有大收益；Link-MoE/LPFormer 的消融同样呈现数据集依赖。结构-first residual 比完全删除 feature 或完整双塔更容易验证因果贡献。
- **Expected Gain**：中高；属性同质性弱、结构启发式强的图上更可能提升。
- **Minimum code change**：增加一个 attribute MLP 和一个 scalar/vector gate；NCN 结构分数和主 decoder 保持不变。
- **V0 / V1**：V0 scalar gate；V1 以 CN=0/1/多和度分桶使用 channel-wise gate。
- **Closest 5**：SIEG、TAGNN、Hetero-LP、NCN、Link-MoE。
- **Most dangerous prior**：SIEG/TAGNN 的 structure-first 或 neighbor-feature removal/separation。
- **Exact difference**：不是删除 neighbor features，也不是构建完整双流 Transformer；只学习被结构 profile 调节的属性 residual。
- **Collision**：L2。
- **Scores**：Novelty 7.0；Ease 8.0；Improvement Probability 8.0；Clarity 8.0；Paper Potential 7.5。

### Idea 5 — NCNC-OCC：observed/completed CN 分离通道

- **Parent model**：NCNC。
- **核心架构**：observed CN pooling 与 completed CN pooling 不再直接相加，分别得到 s_obs 和 s_comp，另加 completion confidence c_uv；decoder 学习 s_obs + g(c_uv)·s_comp。
- **Performance Rationale**：NCNC 的核心动机是 graph incompleteness 会让真实 CN 在观测图中消失；但 observed 和 inferred witness 的证据强度不同。将它们分离，可能在稀疏图上保留补全收益，同时限制错误 completion 的污染。
- **Expected Gain**：中高；稀疏图、CN=0/1 和补全召回高但精度不稳定的子群优先。
- **Minimum code change**：复用 NCNC 的 candidate CN/completion 结果，只拆分两次 sum 并加一个 gate。
- **V0 / V1**：V0 两个 sum + 一个 confidence；V1 用 held-out completion calibration 学习 confidence mapping。
- **Closest 5**：NCNC、NCN、PPNC/common-neighbor completion、OCN、IGLP。
- **Most dangerous prior**：PPNC 类 common-neighbor completion 与 NCNC 本身。
- **Exact difference**：不提出新的 CN completion algorithm；贡献点是 observed/inferred evidence 的 decoder-level semantic separation。
- **Collision**：L1（较高风险）。
- **Scores**：Novelty 6.5；Ease 8.5；Improvement Probability 8.0；Clarity 8.5；Paper Potential 7.0。

### Idea 6 — BUDDY-SAC：sketch agreement confidence

- **Parent model**：BUDDY/ELPH。
- **核心架构**：把已有 hash/sketch feature 划成多个独立子空间，计算各子空间 pair feature 的 agreement/variance，并把相对误差 proxy 作为 confidence gate；不只是把 sketch 维度加大。
- **Performance Rationale**：BUDDY/ELPH 说明预计算结构特征可以获得很好的性能/效率折中，但 sketch 是近似估计。若同一 pair 的子 sketch 明显不一致，直接把其值当作确定性 feature 会增加 decoder noise；agreement channel 是针对近似误差的低成本修复。
- **Expected Gain**：中等到中高；在结构稀疏、度长尾或 sketch collision 较多的图上更可能看到收益。
- **Minimum code change**：只改 sketch feature aggregation 和 predictor input；不改变预计算图遍历。
- **V0 / V1**：V0 append mean/variance；V1 confidence-aware residual correction。
- **Closest 5**：ELPH/BUDDY、MPLP、NCN、OCN、LPFormer。
- **Most dangerous prior**：ELPH/BUDDY 的 sketch design 与 MPLP 的 multi-dimensional random estimator。
- **Exact difference**：不增加新的 sketch family；显式使用已有独立子 sketch 的 disagreement 作为 uncertainty feature。
- **Collision**：L1。
- **Scores**：Novelty 7.0；Ease 8.0；Improvement Probability 7.5；Clarity 8.5；Paper Potential 7.5。

### Idea 7 — SEAL-HGP：hop-gated structural pooling

- **Parent model**：SEAL。
- **核心架构**：按 DRNL/hop/role 对 enclosing subgraph 节点做分组池化，得到 hop-wise states 和 cross-hop difference；用轻量 pair gate 选择 hop mixture，不引入 full graph Transformer。
- **Performance Rationale**：SEAL 的 pair-specific enclosing subgraph 仍是强结构基线，但其信息通常被统一 pooling 压缩；HL-GNN 的多范围证据支持分层读出。按 hop 保留结构层次有望减少近邻和远邻的互相污染。
- **Expected Gain**：中等到中高；适合规模较小且 SEAL 本身较强的数据集。
- **Minimum code change**：在 SEAL pooling 前增加 hop buckets；训练流程不变。
- **V0 / V1**：V0 hop mean/max + gate；V1 增加 hop-difference token。
- **Closest 5**：SEAL、NCN、HL-GNN、LPFormer、TAGNN/GPEN。
- **Most dangerous prior**：TAGNN/GPEN 的局部结构层级、global position 和 boundary-aware encoding。
- **Exact difference**：只做 enclosing subgraph 的 hop-wise low-cost pooling，不做 global position tree，也不做 shortest-path sequence Transformer。
- **Collision**：L2，且工程成本高于前六项。
- **Scores**：Novelty 6.5；Ease 8.0；Improvement Probability 7.5；Clarity 9.0；Paper Potential 7.0。

### Idea 8 — NCN-CNIT：公共邻居诱导拓扑 token

- **Parent model**：NCN/NCNC。
- **核心架构**：除了 CN 节点 embedding sum，计算 CN 集合内部的 induced-edge density、component count、triangle/overlap 等低维统计，形成一个 CN-topology token，与 CN pooled state 做 bilinear interaction。
- **Performance Rationale**：当前 CN sum 只描述 witness 的节点状态，未描述 witness 之间是否互相连接、是否来自同一局部团簇。两个相同 CN count 的 pair 可能对应非常不同的 CN-induced topology；低维统计可在不构建完整 enclosing subgraph 的情况下恢复这部分信息。
- **Expected Gain**：中等；图中 triadic closure/community structure 明显时更有希望。
- **Minimum code change**：在 pair statistics preprocessing 中新增少量 CN-induced counts；decoder 加一个 token MLP。
- **V0 / V1**：V0 三个统计量；V1 一个小型 CN-induced graph encoder。
- **Closest 5**：NCN/NCNC、OCN、SEAL、LPFormer、TAGNN。
- **Most dangerous prior**：OCN 的高阶 common-neighbor interaction 与 SEAL 的 enclosing-subgraph encoding。
- **Exact difference**：不是增加 endpoint 的高阶 CN order；是描述“当前 CN witness 彼此之间”的低维拓扑。
- **Collision**：L1–L2。
- **Scores**：Novelty 7.0；Ease 7.5；Improvement Probability 7.0；Clarity 8.5；Paper Potential 7.5。

### Idea 9 — OCN-XO：多阶结构的低秩交互

- **Parent model**：OCN。
- **核心架构**：保留 OCN 已有 orthogonalized/normalized order representations r_1...r_K，在 decoder 中加入相邻阶的低秩 bilinear interaction r_k^T U_k r_{k+1}，替代简单 raw concat。
- **Performance Rationale**：OCN 的消融指出简单 concatenation 明显低于其结构处理版本；这说明“多阶信息存在”不等于“直接拼接有效”。低秩阶间交互可能利用 complementary signal，同时控制参数和冗余。
- **Expected Gain**：中等到中高；高阶结构确实有信号且 OCN 现有读出成为瓶颈时最有希望。
- **Minimum code change**：只在 OCN predictor 添加一个或少量 low-rank interaction；不改变正交化和传播。
- **V0 / V1**：V0 相邻阶一项 interaction；V1 pair-conditioned interaction weight。
- **Closest 5**：OCN、NCN、NCNC、Link-MoE、LPFormer。
- **Most dangerous prior**：OCN 本身；任何 order-wise interaction 都必须与其原始 decoder 做逐项差异说明。
- **Exact difference**：不重新设计 higher-order CN estimator，只改已处理 order representations 的 cross-order readout。
- **Collision**：L1。
- **Scores**：Novelty 6.0；Ease 7.5；Improvement Probability 7.5；Clarity 8.0；Paper Potential 7.0。

### Idea 10 — Path-Rel：路径可靠性/多样性通道

- **Parent model**：NCN/Neo-GNN/HL-GNN。
- **核心架构**：不直接建模 shortest-path sequence，而加入低维 path length histogram、edge-disjoint path count、bottleneck/bridge proxy、path redundancy 等统计；作为结构 readout 的 calibration token。
- **Performance Rationale**：MPLP 的多层传播与 LPFormer 的 PPR 说明远程 walk/path 有信息；SP4LP 和 TAGNN 已把 path/shortest-path 做成更强的序列或 pairwise encoder。更小的 gap 是：路径数量相同但互相高度重复与彼此独立时，证据可靠性不同。
- **Expected Gain**：中等；适合跨社区、长程和没有直接 CN 的 pair。
- **Minimum code change**：复用已有 BFS/shortest-path statistics 或离线预处理，decoder 增加 2–5 个 path features。
- **V0 / V1**：V0 固定统计量；V1 轻量 path reliability MLP。
- **Closest 5**：SP4LP、LPFormer、HL-GNN、NCN、TAGNN。
- **Most dangerous prior**：SP4LP 的 shortest-path sequence modeling、TAGNN 的 shortest-path/RST。
- **Exact difference**：不做路径序列编码，只做路径冗余/可靠性摘要。
- **Collision**：L2。
- **Scores**：Novelty 6.5；Ease 7.5；Improvement Probability 7.0；Clarity 8.0；Paper Potential 7.5。

### Idea 11 — NCN-EgoSep：ego 与 neighbor 的结构/属性分离

- **Parent model**：NCN；参考 SIEG、TAGNN 和 Hetero-LP。
- **核心架构**：endpoint ego embedding、neighbor aggregate、CN aggregate 使用独立 projection；只在 pair decoder 处做交互，不在早期 MPNN 中无条件混合。
- **Performance Rationale**：异配图 LP 结果支持 ego/neighbour separation；SIEG/TAGNN 也显示 neighbor feature removal/separation 可能改善结构主导数据集。NCN 的 MPNN state 若混入过多邻居属性，可能削弱 pair-specific CN signal。
- **Expected Gain**：中等到中高；异配、跨社区或 neighbor features 噪声大的图上更可能提升。
- **Minimum code change**：给已有 hidden states 增加两组小 projection；传播层保持不变，避免重写 backbone。
- **V0 / V1**：V0 endpoint/neighbor 两路 MLP；V1 由 pair profile 控制 attribute interaction。
- **Closest 5**：SIEG、TAGNN、Hetero-LP、NCN、Link-MoE。
- **Most dangerous prior**：SIEG/TAGNN 的结构优先和 feature separation。
- **Exact difference**：不直接删邻居特征，也不引入完整 structural transformer；重点是 decoder 前的 ego-neighbor channel separation。
- **Collision**：L2。
- **Scores**：Novelty 6.5；Ease 8.5；Improvement Probability 7.5；Clarity 8.0；Paper Potential 7.0。

### Idea 12 — Motif-Routed NCN：轻量 motif route

- **Parent model**：NCN。
- **核心架构**：单一共享 encoder 产生 CN、path、attribute 三种低维 evidence，使用一个三路 softmax gate 选择 readout 比例；不复制完整 GNN experts。
- **Performance Rationale**：Link-MoE 证明不同 pair 需要不同 pairwise information；NCN 已有强 CN branch，因此更小的测试是只增加 path/attribute residual，并验证 gate 是否只在 CN 不充分时启用其他证据。
- **Expected Gain**：中高，但主要依赖 gate 是否学到真实子群分工；若 gate 退化为固定权重，则停止。
- **Minimum code change**：一个 gate MLP 和两个轻量 residual statistic；不增加多个 backbone。
- **V0 / V1**：V0 三路 gate；V1 增加 gate entropy/route audit，但不优先加新 loss。
- **Closest 5**：Link-MoE、NCN、LPFormer、IGLP、OCN。
- **Most dangerous prior**：Link-MoE 的 pair-level gating，且 IGLP 已研究 importance-guided route。
- **Exact difference**：是共享 backbone 上的三路低维 residual routing，不是多专家 MoE。
- **Collision**：L2，审稿人很可能要求直接对比 Link-MoE。
- **Scores**：Novelty 5.5；Ease 8.0；Improvement Probability 8.0；Clarity 8.0；Paper Potential 6.5。

### Idea 13 — Pair-NodeDup：低度节点对的局部复制增强

- **Parent model**：GraphSAGE/NCN；参考 NodeDup。
- **核心架构**：只在训练 pair 的局部 computation graph 中，对低度 endpoint 建立 role-specific duplicate state，并共享原节点属性；不改全图 adjacency，不对所有节点做全局复制。
- **Performance Rationale**：NodeDup 已报告 cold-start/low-degree LP 的强收益，说明低度节点的 representation bottleneck 是现实问题。局部 pair-conditioned 版本可能降低全局图扰动和额外存储，但收益预期集中在低度子集。
- **Expected Gain**：低度/冷启动子群高；总体平均提升不确定。
- **Minimum code change**：sampler/mini-batch graph view + 一个 duplicate projection；需要非常谨慎地防止 train/test leakage。
- **V0 / V1**：V0 只对 degree≤d 的 endpoint 开启；V1 按 pair role 共享/不共享 duplicate state。
- **Closest 5**：NodeDup、SIEG、Hetero-LP、NCN、SEAL。
- **Most dangerous prior**：NodeDup 本身。
- **Exact difference**：不是全局节点复制或 cold-start 专项模型；是按 target pair 触发的局部、role-specific augmentation。
- **Collision**：L1，且实验协议风险高。
- **Scores**：Novelty 6.0；Ease 8.0；Improvement Probability 8.5；Clarity 8.0；Paper Potential 7.0。

### Idea 14 — CrossLink-Ego：跨社区/内部边双通道

- **Parent model**：GCN/GraphSAGE；可迁移到 NCN 的 MPNN branch。
- **核心架构**：根据 local structural role、community proxy 或 cross-link score，把 message 分成 internal-edge 与 cross-edge 两个通道；endpoint pair decoder 同时读取两者。
- **Performance Rationale**：Cross-links Matter 指出 cross-cluster links 和数据偏差会影响 LP；Hetero-LP 说明 homophily 假设并不稳固。分开两类邻居可以减少把跨社区信号当成普通同质邻居平均的问题。
- **Expected Gain**：中等；跨社区显著或异配图更有希望。
- **Minimum code change**：边路由/两个 aggregation accumulator；需要额外审计 role proxy 是否泄漏标签。
- **V0 / V1**：V0 两个固定通道；V1 pair-conditioned channel mixing。
- **Closest 5**：Cross-links、Hetero-LP、SIEG、TAGNN、Link-MoE。
- **Most dangerous prior**：Cross-links Matter 的 twin-structure/debiased embedding 框架。
- **Exact difference**：不建 twin teacher 或 debiasing objective；只在 LP message passing 中分离 cross/internal edge channel。
- **Collision**：L1–L2。
- **Scores**：Novelty 6.5；Ease 7.5；Improvement Probability 7.5；Clarity 7.5；Paper Potential 7.0。

### Idea 15 — PPR-CN-Adapter：PPR 仅校准 CN 通道

- **Parent model**：NCN/NCNC。
- **核心架构**：不建立 LPFormer 的完整 PPR relative-position Transformer，只用 pair-level PPR summary（如 endpoint-to-CN-set mass 或 low-rank PPR score）调节 CN pooled representation 的 gate。
- **Performance Rationale**：LPFormer 的 PPR/RPE、attention、feature 和 count 消融说明 pair-specific diffusion context 有价值；NCN 的 CN channel 则更便宜。把 PPR 限制到 CN calibration，可测试“远程 context 是否只需校准局部 witness”的窄假设。
- **Expected Gain**：中等；PPR 可计算且远程结构重要的数据集上更可能受益。
- **Minimum code change**：增加一个 pair PPR scalar/low-dimensional adapter；不存完整 PPR matrix。
- **V0 / V1**：V0 scalar gate；V1 sparse/low-rank PPR adapter。
- **Closest 5**：LPFormer、NCN、NCNC、Link-MoE、HL-GNN。
- **Most dangerous prior**：LPFormer 的 pair-specific PPR RPE。
- **Exact difference**：PPR 只作用于 NCN CN channel 的 calibration，不做 Transformer、全局 RPE 或完整 attention。
- **Collision**：L1–L2。
- **Scores**：Novelty 5.5；Ease 8.0；Improvement Probability 7.5；Clarity 8.0；Paper Potential 6.5。

## 5. Novelty collision check

### 5.1 碰撞等级

- **L0：直接复现**。核心模块、输入、训练目标和结论都与现有方法相同，不能作为创新点。
- **L1：强邻近扩展**。父模型和信息来源相同，只改变一个读出/校准操作；可以做性能研究，但必须把贡献写成明确的 failure-mode repair，不能声称全新范式。
- **L2：功能相邻但机制不同**。解决相近问题，但输入、作用位置或计算约束不同；需要系统对比最近 prior。
- **L3：较低碰撞**。当前检索没有发现直接同构实现，但仍需在正式投稿前做最近三个月检索。

### 5.2 15 个候选的风险矩阵

| ID | 候选 | 最高风险 prior | Collision | 必须证明的差异 |
|---|---|---|---|---|
| 1 | MPLP-VC | MPLP/DotHash | L1 | independent-block agreement 是 uncertainty readout，不是 degree feature 或新 signature |
| 2 | NCN-CNDP | NCN、IGLP、OCN | L1–L2 | permutation-invariant second moment，不做 neighbor importance/top-k |
| 3 | HL-GNN-PDG | Link-MoE | L2 | shared backbone readout gate，不是多专家 ensemble |
| 4 | NCN-STR | SIEG/TAGNN | L2 | attribute residual gate，不是 feature removal 或 full dual branch |
| 5 | NCNC-OCC | NCNC/PPNC | L1 | 不改变 completion algorithm，只区分 observed/inferred evidence |
| 6 | BUDDY-SAC | ELPH/BUDDY | L1 | 利用已有 sketch disagreement，不新增 sketch family |
| 7 | SEAL-HGP | GPEN/TAGNN/HL-GNN | L2 | hop pooling，不做 global position 或 path sequence |
| 8 | NCN-CNIT | OCN/SEAL | L1–L2 | CN witness 内部拓扑，不是 endpoint higher-order CN |
| 9 | OCN-XO | OCN | L1 | 只改 order readout 为 low-rank interaction |
| 10 | Path-Rel | SP4LP/TAGNN | L2 | path reliability statistics，不做 sequence encoder |
| 11 | NCN-EgoSep | SIEG/TAGNN | L2 | decoder-level separation，不删除 neighbor feature |
| 12 | Motif-Routed NCN | Link-MoE/IGLP | L2 | 单 backbone 低维 residual route，不是 experts |
| 13 | Pair-NodeDup | NodeDup | L1 | pair-local role-specific augmentation，不是全局 duplication |
| 14 | CrossLink-Ego | Cross-links Matter | L1–L2 | message channel split，不是 twin debiasing objective |
| 15 | PPR-CN-Adapter | LPFormer | L1–L2 | PPR 只校准 CN，不做 Transformer/RPE |

### 5.3 最危险的撞车点

1. **MPLP-VC**：若实现只是 raw score + degree one-hot + MLP，会被视为 MPLP 已有配置；必须使用独立 block agreement 或可校准的 estimator variance，并做 reliability subgroup 分析。
2. **NCN-CNDP**：若实现只是 sum + max，容易被视为普通 pooling trick；至少要说明为何二阶矩对应 witness-set heterogeneity，并与 count、max、attention、OCN 逐项消融。
3. **HL-GNN-PDG**：若引入多个独立 experts，就会撞到 Link-MoE；保持单 backbone，并把新增参数、推理成本和 gate 的 pair-level 行为报告清楚。
4. **NCNC-OCC**：若同时重新设计 CN completion，会直接撞 NCNC/PPNC；第一版只允许拆分已有 observed/completed signals。
5. **PPR-CN-Adapter / Path-Rel**：必须把“使用 PPR/shortest path”降级为已知输入，把贡献放在它如何校准已有 CN/结构通道，而不是声称首次使用路径信息。

## 6. Improvement-probability ranking

### 6.1 评分公式

Score = 0.25·Novelty + 0.30·ProbabilityOfImprovement + 0.20·Feasibility + 0.15·ExperimentalClarity + 0.10·PaperPotential

ProbabilityOfImprovement 权重最高，原因是本轮目标是先得到可观测的 metric improvement；Novelty 不能用来抵消一个几乎不可能提升的复杂架构。分数为先验，不能替代真实 seed 结果。

### 6.2 全部候选排序

| Rank | ID | 候选 | N | P(improve) | Feasibility | Clarity | Paper | Weighted score | 快速判断 |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1 | 1 | MPLP-VC | 7.5 | 8.0 | 9.0 | 9.0 | 7.5 | **8.13** | 首选：针对已知 variance gap |
| 2 | 2 | NCN-CNDP | 7.0 | 7.5 | 9.0 | 9.0 | 7.5 | **7.90** | 首选结构 pooling 消融 |
| 3 | 3 | HL-GNN-PDG | 6.5 | 8.5 | 8.0 | 9.0 | 7.5 | **7.88** | 高概率但需防 Link-MoE 撞车 |
| 4 | 4 | NCN-STR | 7.0 | 8.0 | 8.0 | 8.0 | 7.5 | **7.70** | 属性噪声场景有优势 |
| 5 | 5 | NCNC-OCC | 6.5 | 8.0 | 8.5 | 8.5 | 7.0 | **7.70** | 稀疏图优先 |
| 6 | 6 | BUDDY-SAC | 7.0 | 7.5 | 8.0 | 8.5 | 7.5 | **7.63** | 适合效率/稳定性叙事 |
| 7 | 13 | Pair-NodeDup | 6.0 | 8.5 | 8.0 | 8.0 | 7.0 | **7.55** | 低度子群高，整体不确定 |
| 8 | 7 | SEAL-HGP | 6.5 | 7.5 | 8.0 | 9.0 | 7.0 | **7.53** | SEAL 强但工程较重 |
| 9 | 11 | NCN-EgoSep | 6.5 | 7.5 | 8.5 | 8.0 | 7.0 | **7.48** | 异配图优先 |
| 10 | 8 | NCN-CNIT | 7.0 | 7.0 | 7.5 | 8.5 | 7.5 | **7.38** | 社区/三角结构明显时测试 |
| 11 | 12 | Motif-Routed NCN | 5.5 | 8.0 | 8.0 | 8.0 | 6.5 | **7.23** | 性能可能好，创新风险高 |
| 12 | 14 | CrossLink-Ego | 6.5 | 7.5 | 7.5 | 7.5 | 7.0 | **7.20** | 需跨社区数据 |
| 13 | 10 | Path-Rel | 6.5 | 7.0 | 7.5 | 8.0 | 7.5 | **7.18** | 低成本但 prior 多 |
| 14 | 9 | OCN-XO | 6.0 | 7.5 | 7.5 | 8.0 | 7.0 | **7.15** | 适合 OCN 已复现后再做 |
| 15 | 15 | PPR-CN-Adapter | 5.5 | 7.5 | 8.0 | 8.0 | 6.5 | **7.08** | 与 LPFormer 距离过近 |

## 7. Top 5

| Top | 方案 | 父模型 | 预期主要受益子群 | 额外开销 | 核心风险 | 结论 |
|---:|---|---|---|---|---|---|
| 1 | MPLP-VC | MPLP/MPLP+ | 低 CN、度长尾、估计不稳定 pair | 低；固定 signature 总维度时近似只增加 readout | 被视为 degree normalization | 最值得先做 |
| 2 | NCN-CNDP | NCN | CN-rich、witness heterogeneity | 低；一次 streaming variance | 被视为普通 pooling trick | 第二优先 |
| 3 | HL-GNN-PDG | HL-GNN | local/global 混合 pair、跨社区 pair | 低到中；pair gate | 撞 Link-MoE | 第三优先 |
| 4 | NCN-STR | NCN/NCNC | 异配、neighbor feature noisy | 低；小型 residual MLP | 撞 SIEG/TAGNN | 若属性噪声明显则上调 |
| 5 | NCNC-OCC | NCNC | 稀疏、CN 缺失、completion 不确定 | 低；拆分两个 pool | 撞 NCNC/PPNC | 稀疏图专项备选 |

## 8. Top 3 fast experiment plans

### 8.1 Plan A：MPLP-VC

**目标**：验证 estimator agreement 是否能在不改 backbone 的情况下提升结构 readout 的有效性和稳定性。

**父模型与代码定位**：从 MPLP 官方实现开始；预计只触及 structural estimator/pair predictor、model config 和 train/evaluation entry。当前 DCDLP 工程不修改；若本地没有 MPLP 官方代码，应在独立实验目录复现。

**V0**：

1. 固定父模型的 signature 总维度和 propagation 层数。
2. 将 signature 划为 K=4 个 block，得到 q_1...q_4。
3. 输入 decoder 的结构部分改为 [mean(q), log(var(q)+1e-8)]，先不加 learned gate。
4. 保持 optimizer、negative sampling、early stopping、batch size 和 tuning budget 与父模型完全一致。

**V1（仅当 V0 有正向信号）**：

- 加入 g_uv=sigmoid(MLP([logvar, logdeg(u), logdeg(v), CN]))；输出 g_uv·mean(q) 与原始 mean 的 residual，而不是替换原分数。
- 做 K∈{2,4,8} sensitivity；如果只有 K=8 才提升，应把 compute/variance trade-off 作为主要结果。

**第一轮数据与 protocol**：

- Cora、Citeseer；优先沿用父模型支持的标准 LP split。如果父仓库没有这两个数据集，则用当前项目已有数据集做第一轮，并把 OGB protocol 留到复现稳定后。
- 每个配置 seed 0/1/2；主指标使用父模型原指标，同时报告 AUC/AP 或 MRR/Hits（取决于 split 定义），不能把不同 benchmark 指标混算。
- 额外分组：CN=0、CN=1、CN≥2；endpoint degree 的低/中/高分位；报告均值、标准差和每个 seed。

**GO**：3 个 seed 中至少 2 个主指标优于 parent，且三 seed 均值为正；低 CN 或高方差子群至少有一个有一致改善；额外显存/时间不超过约 20%。

**STOP**：均值≤0 且所有子群无改善；或只有单个 seed 大幅提升、方差明显放大；或优势完全由新增 degree feature 而非 estimator agreement 解释。

### 8.2 Plan B：NCN-CNDP

**目标**：验证 CN witness 的二阶分布信息是否补足 NCN 的 sum pooling。

**父模型与代码定位**：NCN 官方代码的 CN pooling/common-neighbor predictor、config 和 evaluation script；不改当前 DCDLP。

**V0**：

1. 保留 NCN 的 endpoint interaction 和 CN sum。
2. 对 h_w 做 streaming second moment，计算逐维 var_cn。
3. decoder 输入改为 [endpoint_pair, cn_sum, var_cn]；参数量只通过一个线性 projection 对齐。
4. 做三个控制组：sum only、sum + count、sum + variance；禁止第一轮加入 attention、top-k 或新 completion。

**V1**：

- 若 V0 正向，在 CN embedding 先做固定的 role projection，再计算两组 variance；或者加一个低秩 cross-moment。二者只选一个，避免把 V1 变成新模型集合。

**第一轮数据与 protocol**：

- Cora、Citeseer；父模型 split、负样本和 decoder 保持不变。
- seed 0/1/2；按 CN count、CN embedding variance、节点度分组。
- 重点记录 CN=0：该分组理论上没有 CN variance，应退化为原 NCN；如果整体提升来自 CN=0，说明贡献可能只是 decoder/训练扰动，需谨慎。

**GO**：sum+variance 相对 sum only 在至少一个数据集的总体主指标均值提升，并在 CN≥2 子群有一致方向；没有显著拖累 CN=0。

**STOP**：只在 max/attention 控制组提升；variance 组无提升；或二阶矩使模型对 CN-rich 图过拟合而 CN=0/1 明显下降。

### 8.3 Plan C：HL-GNN-PDG

**目标**：验证 pair-specific range selection 能否以单共享 backbone 的成本获得 Link-MoE/HL-GNN 所暗示的异质 pair 收益。

**父模型与代码定位**：HL-GNN 的 layer aggregation/readout、config 和 train/evaluation entry；预计不修改传播算子，只修改全局 layer weights 的使用方式。

**V0**：

1. 先计算一组固定 pair profile：CN、AA/RA、shortest-path bucket 或 PPR summary、endpoint feature similarity；第一轮最多 4–5 个输入。
2. 一个小型 MLP 输出 softmax(β_1...β_L)。
3. 对同一 batch 的 pair 组合各层 endpoint readout；不复制 experts、不加 MoE loss。
4. 与三组控制对比：global β、uniform β、pair β。

**V1**：

- 只在 V0 提升且 gate 不塌缩时，把 β 分成 structural-range 与 attribute-range 两组；不引入 Link-MoE 的多个完整专家。

**第一轮数据与 protocol**：

- Cora、Citeseer 或父模型已有的两个小图；seed 0/1/2。
- 除总体主指标外，报告 gate 熵、不同 CN/degree/path 子群的平均 β，以及训练/推理时间。
- 若使用 PPR，必须报告预处理与显存；若这一步超过预算，退回只用 CN+SPD。

**GO**：pair β 相对 global β 在至少两个 seed 有正向主指标，且 gate 在不同 pair 子群呈现可解释差异；额外开销可控。

**STOP**：gate 接近常数、只复现 global β；或性能提升完全来自新增 PPR/heuristic features；或与 Link-MoE 对比后没有成本/性能优势。

## 9. Final Top 1 recommendation

### 9.1 推荐标题

- 中文：**不确定性感知的准正交消息传递链路预测**
- English：**Uncertainty-Calibrated Quasi-Orthogonal Message Passing for Link Prediction**
- 工作简称：**MPLP-VC**。

### 9.2 研究对象与父模型

- **Baseline**：MPLP 或 MPLP+；优先使用官方实现和其原始协议。
- **已知 weakness**：MPLP 的结构 estimator 虽然高效且有强性能，但论文讨论了 degree-induced bias、random signature 对 unseen-node generalization 的影响，以及 graph-structure-dependent variance。官方代码也提供 degree-related controls；因此“再加 degree one-hot”不能算新贡献。
- **待验证假设**：对同一个 pair 使用多个 independent quasi-orthogonal estimator blocks，block disagreement 是 link score uncertainty 的有效 proxy；把该 proxy 显式输入 decoder，能减少不可靠 structural evidence 对排序的干扰。

### 9.3 架构

令传播后的 signature 为 z_u,z_v，将其分为 K 个 block：

~~~text
q_k(u,v) = <z_u^(k),z_v^(k)>
μ_uv     = mean_k q_k(u,v)
s²_uv    = var_k q_k(u,v)
r_uv     = μ_uv / sqrt(s²_uv + ε)
score_uv = Decoder([existing_MPLP_features, μ_uv, log(s²_uv + ε), r_uv])
~~~

V0 只使用 μ 和 log variance，并保持原 decoder 的其他输入不变。V1 再测试：

~~~text
g_uv     = sigmoid(MLP([log variance, log degree_u, log degree_v, CN_uv]))
score_uv = base_score_uv + g_uv · residual_structural_score_uv
~~~

这里 degree、CN 只作为 confidence context；它们不是方法本身。核心贡献必须来自 multi-estimator agreement → pair-level uncertainty → calibrated structural readout 这条链。

### 9.4 为什么它最值得先做

1. **问题由父论文直接暴露**：不是凭空制造 failure case，而是将 MPLP 的 variance limitation 转成可测的 architecture hypothesis。
2. **改动最小**：不重写 graph encoder、不构造 enclosing subgraph、不增加全图 PPR matrix、不引入多专家。
3. **实验因果清楚**：MPLP、MPLP + degree controls、MPLP-VC mean、MPLP-VC mean+variance、MPLP-VC V1 gate 可以逐级对比。
4. **可解释子群明确**：若方法有效，应该优先改善低 CN、高度不平衡或 block disagreement 大的 pair；这比只看一个总体指标更能支撑 mechanism claim。
5. **失败也有价值**：如果 variance proxy 不提升，可以明确说明 MPLP decoder 已能吸收该信息，或 block disagreement 不是有效 uncertainty；停止成本低，不会陷入大型架构工程。

### 9.5 最近 5 篇与最危险 prior

最近 5 篇直接参考：**MPLP、ELPH/BUDDY、NCN/NCNC、OCN、LPFormer**。其中最危险的是 MPLP 自己的 degree controls 和随机估计设计；其次是 ELPH/BUDDY 的 sketch approximation。正式论文中必须做以下区分：

- 不是增加 quasi-orthogonal vector 的维度；
- 不是增加 degree one-hot；
- 不是把多个随机向量简单 concat；
- 不是用一个通用 MLP 重新拟合原 MPLP score；
- 而是利用 independent estimator 的 disagreement 作为显式 confidence/variance channel，并验证 calibration 与 subgroup improvement。

### 9.6 最小实现与资源预估

- **V0 改动**：structural estimator、predictor input、一个 config 开关、evaluation subgroup logging。
- **不改动**：data split、negative sampling、message passing depth、loss、optimizer 和主训练流程。
- **额外计算**：若总 signature dimension 固定，只是 K 个 block 的向量内积和统计量，预计低开销；若为了保持每 block 维度而扩大总维度，需单独报告显存和时间。
- **预计工程量**：半天到 1 天完成 V0，1 天完成 protocol/seed/subgroup audit；这里是工程估计，不是已执行时间。

### 9.7 第一实验与 GO/STOP

**第一实验**：Cora + Citeseer；若父模型仓库不支持，则使用当前项目已有的标准 LP 数据集作为替代。每个配置 seed 0/1/2；父模型与 V0 使用完全相同的 split、negative sampler、early stopping 和调参预算。报告总体主指标、每 seed、均值±标准差，并分 CN=0/1/≥2 与 degree quantile。

**GO 条件**：

- V0 在至少一个数据集上相对 parent 的三 seed 均值为正，且至少 2/3 seed 改善主指标；
- 提升不能只来自改变训练随机性，且 mean+variance 要优于 mean only 与 degree-control 对照；
- 至少一个“高 variance / 低 CN / degree imbalance”子群有一致改善；
- 额外显存、训练或推理开销没有超过预先设定预算。

**STOP 条件**：

- 两个数据集三 seed 均值均不提升；
- 只有 degree feature 对照提升，而 variance channel 不提升；
- block variance 与错误/低置信 pair 没有关系，且 subgroup 结果无机制支持；
- 需要不断增加 K、额外 loss、attention 或新 expert 才能挽救，否则停止，不继续扩大架构。

### 9.8 最终判断

**MPLP-VC 是当前最实用的 Top 1：它不承诺理论突破，而是把一个强、可复现、低成本父模型的已知经验限制转成可直接证伪的结构读出改进。** 先做 V0；只有 V0 通过 GO，才做 V1 和更大 OGB benchmark。当前不建议直接在 DCDLP 主工程里实现这三个候选，以免把策略筛选和既有项目实验混在一起。

## 参考与协议提醒

- 大规模 benchmark 的 metric 和 split 应遵循 [OGB link property tasks](https://ogb.stanford.edu/docs/linkprop/)；Cora/Citeseer 的随机 split/AUC 结果不能直接与 OGB 的 MRR、Hits@K 或 ROC-AUC 混合排名。
- 评估协议必须参考 [LP benchmarking pitfalls](https://proceedings.neurips.cc/paper_files/paper/2023/hash/0be50b4590f1c5fdf4c8feddd63c4f67-Abstract-Datasets_and_Benchmarks.html)，尤其是 hard negatives、split leakage、metric 和 baseline coverage。
- 本报告引用的论文状态混合了正式发表、期刊文章和 arXiv/under-review 工作；正式投稿前应对 Top 1 及其最近 5 篇做一次截至投稿日的检索，并核验作者、版本、代码和实验协议。
