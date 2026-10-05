# Link Prediction Architecture Innovation Search

> 研究主题：Link Prediction 的架构级信息流缺陷与原创结构设计  
> 检索截止：2026-09-15  
> 任务边界：static / attributed / homogeneous LP 优先；temporal、heterophilic 作为补充。  
> 本报告不延续 DCDLP、N2 gradient conflict、degree/CN disentanglement、negative sampling、PU、calibration、generic OOD/robustness 或新 loss。

## 0. 结论先行

当前最值得做一日证伪的方向是：

**Boundary-Conserved Pair Field / Schur-Interface Link Predictor（BCPF/SILP）**。

核心原则不是“给 SEAL 加全局特征”，而是：

> 对每个查询 pair 的 enclosing subgraph，不能把 cut 外部的图直接删除；应把外部图对 cut boundary 的影响编码为一个 boundary transfer operator，并在 pair-specific message passing 中持续作用于内部状态。

它试图修复的是 **subgraph truncation 的不可逆信息丢失**，而不是增加一个更强 decoder。当前检索没有发现已在 LP 中明确采用“外部图 Schur-complement / transfer-operator 作为 pair-specific boundary condition”的论文；但 GPEN、LLwLC、NBFNet、CORE 已分别覆盖 global position、spectral boundary constraints、query-conditioned path propagation、edge-level target influence，因此原创性只能标为**暂定 8/10，必须先做 one-day existence test 和定向查重**。

如果首日测试不能证明“同一内部 k-hop 子图、不同外部边界上下文”会造成标签或最优预测差异，立即放弃。若 GPEN/LLwLC 或未检索到的工作已经实现同一 boundary transfer principle，也应降级为 L2/L3，并停止该方向的论文投资。

本报告中的“未发现”只表示截至本轮检索未在公开标题、摘要和可检索全文中发现同构核心，不等于专利式的新颖性保证。

## 1. Architecture literature landscape

| 谱系 | 代表工作 | 信息流 | 已暴露的架构问题 | 本轮判断 |
|---|---|---|---|---|
| Node-centric GNN | GCN / GraphSAGE / GAE / VGAE | `G -> h_u,h_v -> decoder` | 节点独立编码，pair 关系在最后才出现；pair-specific 结构可能已经丢失 | 这是最明确的基础 failure，但已经被大量 link-centric 工作指出 |
| Enclosing-subgraph | SEAL、GraIL-like、SE4LP、BS-SubGNN | `pair -> k-hop subgraph -> GNN -> graph/link score` | 信息更贴近 pair，但 fixed radius、硬 boundary、重复子图、pooling 压缩与成本问题 | 仍有 boundary 空白，但不能再做“更大子图”或“子图+Transformer” |
| Structural-feature | Neo-GNN、NCN、NCNC、ELPH、BUDDY、MPLP | `SF` 与 MPNN 以不同顺序进入 pair representation | CN 与 higher-order CN 的冗余、图不完整、预计算与节点表征耦合 | SF→MPNN、MPNN→SF、SF||MPNN 已有明确先例 |
| Pair-centric / path | NBFNet、2D-WL、line-graph GNN、TNCN | pair/link 直接作为传播单位或查询条件 | 更强 pair expressiveness 往往伴随 O(n²)、路径聚合或局部化成本 | “pair-conditioned propagation” 本身不能直接宣称新颖 |
| Adaptive / mixture | LPFormer、Link-MoE、IGLP、TAGNN | 对 pair 选择 pairwise factor、邻居或专家 | 自适应 pairwise information、邻居重要性、结构/特征融合已拥挤 | 不能再以“不同 pair 使用不同信息”作为贡献 |
| Expressiveness theory | 2-WL LP、relational WL、NeurIPS 2025 link expressiveness、AAAI 2026 LLwLC | 直接研究 link-level distinguishability | 很多“节点无法区分”的论点已被形式化；新方法必须给出新的信息流而非更强 MLP | 是查重底线 |

关键证据：

- SIEG 明确指出 node-centric neighborhood aggregation 缺少 target-node structural relationship，并以去除邻居属性、加入 Binary Structural Transformer 补足结构信息。[AAAI 2024 SIEG](https://ojs.aaai.org/index.php/AAAI/article/view/29417)
- ELPH/BUDDY 已将 subgraph 的 link features 通过 hashing/sketching 近似到 full-graph，并解决了显式子图的冗余与扩展性。[ELPH/BUDDY](https://arxiv.org/abs/2209.15486)
- NCN 已明确区分 `SF-then-MPNN`、`MPNN-then-SF` 和 `SF-and-MPNN`；NCNC 进一步做 common-neighbor completion。[NCN/NCNC](https://arxiv.org/abs/2302.00890)
- 2-WL LP 直接以 2-tuples 作为 message-passing unit，已经杀死“第一次把 node pair 作为传播单位”的宽泛主张。[2-WL LP](https://arxiv.org/abs/2206.09567)
- Link-MoE 已证明同一数据集内不同 pair 需要不同 pairwise information，并以 pair-level gating 选择专家。[Link-MoE](https://proceedings.neurips.cc/paper_files/paper/2024/hash/1d0bcb52067128f826c86db234280dce-Abstract-Conference.html)
- NeurIPS 2025 工作给出统一的 `k_phi-k_rho-m` link-representation expressiveness 框架和 LR-EXP，说明不能只用“更 expressive”作为创新。[Link representation expressiveness](https://papers.nips.cc/paper_files/paper/2025/hash/b1cd72276feff8173462e3f733ac66f8-Abstract-Conference.html)
- GPEN 已做 global position encoding 与 boundary-aware convolution；它是本报告 Top 1 的最危险近邻之一。[GPEN](https://proceedings.mlr.press/v267/wu25l.html)
- 2025 的 SGCG 已专门讨论 enclosing-subgraph-induced oversmoothing 和相似 receptive fields；因此“子图冗余/更多节点更坏”不能单独包装成新意。[SGCG](https://doi.org/10.1016/j.neucom.2025.130666)
- 2026 的 TAGNN 已把 subgraph sampling、结构 GNN、pairwise structure encoding 和 decoder fusion 放进一个 LP 框架；“局部 GNN+全局 pair Transformer”已不是空白。[TAGNN](https://www.nature.com/articles/s41598-026-48184-0)

## 2. Architecture taxonomy

把 LP 拆成六个可能发生不可逆压缩的位置：

```text
G, X
  │
  ├─ (A) structure extraction / subgraph cut
  │       └─ fixed k-hop、sampling、sketch、boundary deletion
  │
  ├─ (B) node or edge encoder
  │       └─ h_v, h_e；通常 query-agnostic
  │
  ├─ (C) pair lifting / pair-conditioned propagation
  │       └─ 是否让 (u,v) 在 message passing 期间持续存在
  │
  ├─ (D) pair constructor
  │       └─ concat、Hadamard、dot、bilinear、set pooling、path sum
  │
  ├─ (E) decoder
  │       └─ 是否能读取方向、witness identity、hop、外部边界影响
  │
  └─ (F) score / training
          └─ 本轮不以 loss、sampler、calibration 为创新点
```

本轮只接受改变 A–E 信息流的设计。一个新的 MLP、attention head、residual、loss、negative sampler 或多分支拼接，不算核心架构创新。

## 3. 20+ architecture failure hypotheses

下面的 `Evidence` 是“论文明确陈述、理论结果或可复现实验现象”，不是把未来工作句子直接当作 gap。`Fundamental` 针对指定架构族，而不是对所有 LP 模型作绝对断言。

| ID | Failure | Evidence | Affected models | Why existing solutions insufficient | Fundamental? | One-day test? |
|---|---|---|---|---|---|---|
| F1 | `G -> h_u,h_v` 先独立压缩，pair 才出现；同一个 `h_u` 必须服务所有候选 v | 2-WL LP、SIEG、NeurIPS 2025 expressiveness 都指出 node-to-link 断裂 | GCN/GraphSAGE/GAE/VGAE、普通 GNN decoder | 更强 decoder 不能恢复 node encoder 已删除的 pair-specific witness | YES（对 node-centric） | YES |
| F2 | Hadamard/dot/低阶 concat 只保留有限交互，可能丢方向、对应关系和高阶组合 | 2-WL、directed pair encoding、link expressiveness work | GAE/VGAE、点积/MLP decoder、部分 BUDDY-style predictor | 换 decoder 只能诊断或局部补救，无法恢复早期 pair 信息 | PARTIAL | YES |
| F3 | 最终 decoder 只能读最终 node embedding，读不到各 hop 的证据来源 | GAE pipeline、KDD 2025 LP pretraining 对 node/edge module 的区分 | GCN/SAGE/GAE、简单 NCN 变体 | late fusion 仍是在末端合并，不会让 decoder 看到已被汇聚的 witness | PARTIAL | YES |
| F4 | Message passing 对 query-agnostic；u 对 v1、v2 使用同一邻域更新 | NBFNet、2-WL、NCN 反向证明了 pair-conditioned 或 pairwise signal 的价值 | 普通 node-centric GNN | LPFormer/Link-MoE 只在 pair factor/专家选择上自适应，不等于每条 message 都被 target pair 条件化 | YES（对普通 MPNN） | YES |
| F5 | 所有 pair 使用同一 hop/radius，但有效结构半径可能不同 | adaptive receptive-field 文献、SIEG、GPEN、长程 LP 结果 | GNN 固定层数、SEAL 固定 k-hop | LPFormer 的 adaptive pairwise encoding 不是 adaptive subgraph radius；Link-MoE 也不是可解释的 pair-specific depth | PARTIAL | YES |
| F6 | 结构特征与 node embedding 的处理顺序决定能否互相调制 | NCN 明确系统比较 `SF->MPNN`、`MPNN->SF`、并行 | Neo-GNN、NCN、NCNC、ELPH/BUDDY | 这个问题本身已被研究，不能再把任意顺序交换称为原创 | NO/PARTIAL | YES |
| F7 | 手工/预计算 SF 与 learned representation 在两个坐标空间，交互只发生在末端 | SIEG、TAGNN、KDD 2025 late fusion | SIEG、BUDDY、TAGNN、预训练 LP | 直接 concat 或 late fusion 是成熟解法，缺少新 principle 才有价值 | PARTIAL | YES |
| F8 | pair state 只在初始化或 decoder 出现，传播中没有 persistent pair memory | 2-WL 与 NBFNet 将 pair/link 作为传播对象 | GAE、SEAL 的部分 node-GNN 实现、NCN | 简单加 pair token 会撞 2-WL/line-graph；必须解决成本和信息保真 | PARTIAL | YES |
| F9 | 对 common neighbors、paths、subgraph nodes 做 sum/mean/global pooling，witness identity 与相互对应关系消失 | SEAL、BUDDY、NBFNet 的聚合形式；link-level expressiveness theory | SEAL、BUDDY、NBFNet、NCN | set encoder/2-WL/path model 已部分缓解；需要独特的保留原则 | PARTIAL | YES |
| F10 | 多条共享边/共享中间节点的路径被重复计数，看似更多结构但提供的是同一证据 | OCN 明确发现 higher-order CN redundancy；ELPH/BUDDY 讨论 subgraph redundancy | OCN 前的 high-order CN、path aggregation、SEAL | OCN 已解决高阶 CN redundancy，任意“去冗余”会高碰撞 | YES（对一般 path family），但研究拥挤 | YES |
| F11 | high-order CN 不同 order 之间重复并导致过平滑 | OCN 2025 明确提出 orthogonalization + normalization | OCN 之前的 NCN/NCNC/high-order CN | 已有直接工作 | NO | YES |
| F12 | SEAL 类 hard k-hop cut 删除 boundary 外的边；如果标签依赖“从内部穿过 boundary 的外部结构”，删除是不可逆的 | SEAL/SE4LP 的 enclosing-subgraph 定义；GPEN 明确补 global context；LLwLC 显式使用 boundary constraints | SEAL、GraIL-like、SE4LP、固定 radius subgraph GNN | 加大 k 增加成本和噪声；global position 不是外部图对当前 boundary 的 transfer operator | PARTIAL（但有新架构空间） | YES |
| F13 | 不同 target link 的 enclosing subgraph 因重复邻域而相似，pair discriminability 被 subgraph-level smoothing 破坏 | SGCG 2025 直接报告类似 receptive fields 和 subgraph-induced oversmoothing | SEAL/SGNN 家族 | coarse-graining 已直接处理，不能只做去 hub 或 residual | NO/PARTIAL | YES |
| F14 | 多条 long-range structural paths 在 node/pair pooling 中被 squash 成 fixed vector | over-squashing survey、NBFNet、GPEN、long-range LP work | deep MPNN、path aggregation、全图 GNN | 通用 rewiring/加深层数不等于 LP-specific witness preservation | PARTIAL | YES |
| F15 | edge/pair propagation 过深时先破坏 pair discriminability，而不是单纯 node smoothing | EdgeConvNorm 直接研究 link representation normalization；OCN 研究 higher-order CN smoothing | line graph/2-WL/high-order CN | normalization/residual 已是常见修补，缺少新的 pair-state conservation law | NO/PARTIAL | YES |
| F16 | pair-level computation 没有共享机制；显式 2-WL/SEAL 对每个 pair 重复算相近 context | ELPH/BUDDY 以 sketch/precompute 解决效率；2-WL 论文讨论 O(n²) 风险 | 2-WL、SEAL、NBFNet、SE4LP | 这是成本问题；不能伪装成准确率创新，除非重新定义可共享信息流 | NO/PARTIAL | YES |
| F17 | easy pair 与 hard pair 使用同样计算深度 | adaptive receptive field、LPFormer、Link-MoE、IGLP 已部分体现 pair heterogeneity | 固定深度 GNN/SEAL | “不同 pair 需要不同信息”已经被 LPFormer/Link-MoE 直接占用 | NO | YES |
| F18 | topology 与 attributes 的融合时机固定，导致结构先验无法决定哪些 feature message 应被保留 | SIEG、TAGNN、Revisiting LP data perspective、KDD 2025 fusion study | GNN4LP、SIEG、TAGNN | early/intermediate/late fusion 已有，不能只换融合位置 | NO/PARTIAL | YES |
| F19 | 无向 pair constructor 对 `(u,v)` 与 `(v,u)` 结构相同，不能表达 directed/role-asymmetric relation | 2-WL、direction-aware pair encoding、relational WL | undirected dot/Hadamard/对称 pooling | directed encoder、bilinear、2-WL 已是直接先例 | NO/PARTIAL | YES |
| F20 | 没有 CN 的 pair 没有显式 witness，结构分支可能退化为 node similarity | NCN/NCNC、ELPH/BUDDY 讨论 structural features 的价值 | CN-enhanced LP、sparse graph LP | 只能做全局 path/feature evidence；不是新缺陷，需与 F12/F14 区分 | PARTIAL | YES |
| F21 | edge-centric/line-graph 化保留了 link identity，却可能丢回原节点的 rich attributes 与未入 line graph 的 context | Line Graph NN、Line Graph Contrastive Learning | line-graph LP | node-edge dual representation 很容易变成双分支拼接，且不是新 principle | PARTIAL | YES |
| F22 | temporal LP 把事件顺序压成 static neighborhood，导致相同结构但不同 temporal path 的 pair 表示相同 | TNCN、TPNet、TGB-Seq 等 | staticized temporal GNN、部分 temporal CN methods | 时间顺序架构已有大量直接工作，本轮不优先 | NO/PARTIAL | YES |

### 3.1 关键筛选

真正可能成为新架构的不是 F1、F2、F4、F8、F14 的宽泛表述：它们会直接撞 2-WL、NBFNet、line-graph 和 2025 expressiveness hierarchy。当前最干净的组合是：

```text
F12 hard boundary truncation
  + F14 long-range evidence squash
  - 不扩大每个 subgraph
  - 不引入普通 global position
  - 不做新 loss
  => preserve external influence as a boundary transfer operator
```

## 4. 10 architecture redesign candidates

### C1. Boundary-Conserved Pair Field（BCPF / SILP）

- **来源 failure**：F12 + F14。
- **Design principle**：subgraph cut 不是“删除外部图”，而是一个 open-boundary problem；内部 message passing 必须接收外部图作用于 boundary 的 transfer operator。
- **Architecture**：对 query `(u,v)` 取 interior `I` 和 cut boundary `B`；预计算或近似 `T_B = A_BB + A_BO(I-αA_OO)^(-1)A_OB`，只把 `T_B` 作用到 B 的 boundary state，再在 I∪B 上传播。使用普通 BCE 与普通 pair decoder，不增加训练目标。
- **不是普通 global feature**：global position 只告诉节点“在哪里”；`T_B` 告诉当前 query 的 boundary “外部结构如何把证据流回内部”。
- **Most dangerous prior**：GPEN；它加入 global position 与 boundary-aware convolution，但没有以 target-pair cut 的 external transfer operator 作为边界状态演化规则。LLwLC 使用 spectral/Neumann constraints 表达 subgraph/link，但不是 learned external transfer message。
- **Collision**：F=L1；P=L1；flow=L1；pair representation=L1；training=L0；evaluation=L0。综合 **L1**。
- **One-day test**：构造一组 synthetic graphs，使 target pair 的 k-hop induced subgraph 完全相同、只改变 boundary 外部连接；比较 SEAL/GNN、GPEN-like global encoding 与 BCPF 是否能区分 label/score。PASS 条件：外部改变与标签存在稳定关联，且 standard SEAL 对外部交换不敏感。
- **Kill criterion**：外部 boundary swap 不改变标签/最优 score，或 `T_B` 与简单 global position/2-hop expansion 等价；立即放弃。
- **Scores**：engineering 3/5；novelty **8/10 provisional**；feasibility 7/10；SCI Q2/Q3 potential 8/10。

### C2. Pair-Indexed Evidence Ledger（PIEL）

- **来源 failure**：F9。
- **Design principle**：pair evidence 不能一次 sum-pool；在 decoder 前保留按 hop、witness class、endpoint role 索引的 evidence cells，再做一次 pair readout。
- **Architecture**：将每个中间 witness 写入固定大小的 typed slots，slot 更新由 `(distance-to-u, distance-to-v, local edge role)` 决定；不是普通 attention pooling。
- **Dangerous prior**：SEAL sort/global pooling、2-WL tuple state、NBFNet path sum、BS-SubGNN。它们已保留了不同程度的 pair/subgraph identity。
- **Collision**：F=L2；P=L2；flow=L2；pair=L2；training=L0；eval=L0；综合 **L2**。
- **Reviewer answer**：只有在 synthetic witness-swap test 显示 ordinary sum 对同计数不同 witness 不能区分，而 ledger 可以，才有价值；否则是 set encoder 换皮。
- **One-day / kill**：构造同 `CN/path count`、不同 witness arrangement 的 pairs；若 stronger set/2-WL decoder 已同样区分，放弃。

### C3. Query-Conditioned Message Field（QCMF）

- **来源 failure**：F4 + F8。
- **Design principle**：target pair condition 必须进入每层 message，而不是只进入 decoder。
- **Architecture**：`m_{x->y}^{(l)} = M(h_x^{(l)}, h_y^{(l)}, q_{uv}, e_{xy})`，其中 q 是当前 target pair state；对同一 source node 的不同 target 使用不同 message。
- **Dangerous prior**：NBFNet 的 indicator/message/aggregate、2-WL、relational C-MPNN、GraIL、SP4LP。它们已经把 query 或 pair 置于传播环中。
- **Collision**：F=L3；P=L3；flow=L3；pair=L3；training=L0；eval=L0；综合 **L3**。
- **Decision**：淘汰，不进入 Top 5。

### C4. Reversible Node-to-Pair Lifting（RNPL）

- **来源 failure**：F1 + F8。
- **Design principle**：node state 进入 pair state 后不能只有不可逆 pooling；保留 endpoint-conditioned lift，使 pair state 可以回写 node-side evidence。
- **Architecture**：建立可逆/信息保真的 pair lift 与 tied inverse update，而非 `h_u,h_v -> one vector`。
- **Dangerous prior**：2-WL、EdgeConvNorm、line-graph GNN、NeurIPS 2025 expressiveness framework。
- **Collision**：F=L3；P=L2；flow=L3；pair=L3；training=L0；eval=L0；综合 **L3**。
- **Decision**：淘汰；“可逆”若没有严格证明只是 residual/2-WL 的重新命名。

### C5. Witness-Intersection Quotient Message Passing（WIQ）

- **来源 failure**：F10。
- **Design principle**：不是按 path 数量聚合，而是先按共享 edge/node 的 intersection pattern 形成 evidence quotient，再对独立 path families 聚合。
- **Architecture**：在 pair-specific propagation 中维护 path-family identity；共享前缀的路径只产生一次 message，分叉后再分开聚合。
- **Dangerous prior**：OCN 的 higher-order CN orthogonalization、NBFNet 的 semiring path aggregation、ELPH/BUDDY sketches。
- **Collision**：F=L2；P=L2；flow=L2；pair=L2；training=L0；eval=L0；综合 **L2**。
- **One-day / kill**：在长环、共享前缀树、重复 motif synthetic graph 上测 path-count versus independent-family；若 OCN/NBFNet/普通 sketch 同样完成，放弃。

### C6. Boundary-First Structural Propagation（BFSP）

- **来源 failure**：F5 + F12。
- **Design principle**：先决定“外部 boundary 如何作用于当前 pair”，再决定 interior receptive field；radius 不是超参数而是由 boundary transfer 的稳定性决定。
- **Architecture**：先计算 boundary interface state，再在内部传播；停止扩大 subgraph，使用 boundary state 作为条件。
- **Dangerous prior**：GPEN、adaptive receptive field GNN、NBFNet、TAGNN。与 C1 高度相近。
- **Collision**：F=L1；P=L1；flow=L1；pair=L1；training=L0；eval=L0；综合 **L1**，但与 C1 同构。
- **Decision**：并入 C1，不作为独立方向。

### C7. Non-Commutative Pair Decoder（NCPD）

- **来源 failure**：F2 + F19。
- **Design principle**：pair constructor 应保留 ordered role interaction，而非对称 dot/Hadamard。
- **Architecture**：使用方向感知的 relation algebra / bilinear operator，使 `(u,v)` 与 `(v,u)` 可不同。
- **Dangerous prior**：directed structural encoding、relational WL、2-WL、DistMult/ComplEx 类 decoder、TAGNN RST。
- **Collision**：F=L3；P=L3；flow=L3；pair=L3；training=L0；eval=L0；综合 **L3**。
- **Decision**：淘汰。

### C8. Pair-Adaptive Computation Halting（PACH）

- **来源 failure**：F5 + F17。
- **Design principle**：easy pair 与 hard pair 不应共享固定深度；由 pair state 的结构稳定性决定是否继续传播。
- **Architecture**：每层输出 pair-state change；稳定时结束，未稳定时继续，使用 hard architectural depth，不引入 halting loss。
- **Dangerous prior**：LPFormer、Link-MoE、adaptive receptive field GNN、IGLP、query-adaptive graph learning。
- **Collision**：F=L3；P=L2；flow=L3；pair=L2；training=L0；eval=L0；综合 **L3**。
- **Decision**：淘汰；“动态深度”本身已不够新。

### C9. Edge-State Context Injection（ESCI）

- **来源 failure**：F21。
- **Design principle**：edge state 在 line graph 传播时不能与原节点属性断开；每个 edge state 需要一个不复制全图的 context injection。
- **Architecture**：line-graph edge state 通过 endpoint context operator 接收原节点的局部 sufficient statistic，再回到 link score。
- **Dangerous prior**：Line Graph Neural Networks、Line Graph Contrastive Learning、EdgeConvNorm、2-WL。
- **Collision**：F=L3；P=L3；flow=L3；pair=L3；training=L0；eval=L0；综合 **L3**。
- **Decision**：淘汰。

### C10. Boundary-Selective Attribute Transport（BSAT）

- **来源 failure**：F7 + F18 + F12。
- **Design principle**：attributes 不应独立在全图传播后再进入 pair；只有穿过 query boundary 的 attribute transport 被允许进入 interior。
- **Architecture**：用 graph cut 上的 transport map 选择属性 message，内部 topology message 保持原状态。
- **Dangerous prior**：SIEG 去除邻居属性、TAGNN 结构编码、SFGCN early/intermediate/late fusion、GPEN boundary-aware conv、IGLP structural-feature importance。
- **Collision**：F=L2；P=L2；flow=L2；pair=L2；training=L0；eval=L0；综合 **L2**。
- **Decision**：仅作为 C1 的 attributed-graph ablation，不单独立题。

## 5. Collision matrix

| Candidate | Failure | Principle | Information flow | Pair representation | Training | Evaluation | Overall | Status |
|---|---|---|---|---|---|---|---|---|
| C1 BCPF/SILP | L1 | L1 | L1 | L1 | L0 | L0 | **L1** | Top 1 provisional |
| C2 PIEL | L2 | L2 | L2 | L2 | L0 | L0 | **L2** | Top 5 only if witness test passes |
| C3 QCMF | L3 | L3 | L3 | L3 | L0 | L0 | **L3** | Reject |
| C4 RNPL | L3 | L2 | L3 | L3 | L0 | L0 | **L3** | Reject |
| C5 WIQ | L2 | L2 | L2 | L2 | L0 | L0 | **L2** | Top 5 only if OCN/NBFNet fail diagnostic |
| C6 BFSP | L1 | L1 | L1 | L1 | L0 | L0 | **L1** | Merge into C1 |
| C7 NCPD | L3 | L3 | L3 | L3 | L0 | L0 | **L3** | Reject |
| C8 PACH | L3 | L2 | L3 | L2 | L0 | L0 | **L3** | Reject |
| C9 ESCI | L3 | L3 | L3 | L3 | L0 | L0 | **L3** | Reject |
| C10 BSAT | L2 | L2 | L2 | L2 | L0 | L0 | **L2** | C1 ablation only |

## 6. Top 5 ranking

| Rank | Direction | Clear failure | Architecture originality | Engineering | Feasibility | Q2/Q3 potential | Main risk |
|---|---|---|---:|---:|---:|---:|---|
| 1 | C1 Boundary-Conserved Pair Field | hard boundary deletes external causal structural influence | **8/10 provisional** | 3/5 | 7/10 | 8/10 | GPEN/LLwLC/hidden boundary-aware prior |
| 2 | C5 Witness-Intersection Quotient | repeated path evidence is counted as independent | 7/10 | 4/5 | 6/10 | 7/10 | OCN/NBFNet/sketching may already subsume it |
| 3 | C2 Pair-Indexed Evidence Ledger | pooling destroys witness arrangement | 7/10 | 3/5 | 7/10 | 7/10 | set/2-WL/SEAL pooling collision |
| 4 | C10 Boundary-Selective Attribute Transport | feature transport ignores query cut | 6/10 | 3/5 | 7/10 | 7/10 | SIEG/TAGNN/IGLP collision |
| 5 | C6 Boundary-First Structural Propagation | receptive field should be determined by boundary influence | 7/10 | 3/5 | 6/10 | 7/10 | effectively C1; do not make a second paper |

Top 5 中真正可独立推进的只有 C1；C5/C2 需要通过一日诊断后再决定，C6/C10 应当作为 C1 的机制消融，不应堆成多分支模型。

## 7. Top 3 deep novelty audit

### Top 1：C1 BCPF/SILP

**Failure**：标准 enclosing-subgraph pipeline 在 cut 处把外部图当成不存在；如果目标 link 的形成机制依赖 boundary 外部路径、桥接或社区上下文，内部 GNN 永远看不到这部分信息。

**Principle**：外部图不是额外 global feature，而是作用在 boundary state 上的 transfer operator。这个 operator 进入 query-specific propagation，并保留到 pair readout。

**Why not existing papers**：

- SEAL/GraIL/SE4LP：编码目标 link 的局部子图，但 hard crop/induced subgraph 仍删除 cut 外部传播。
- ELPH/BUDDY：用 sketch/precomputation 高效近似子图结构，但不是 external-to-boundary transfer dynamics。
- NCN/NCNC/OCN：重点是 CN/higher-order CN、completion、redundancy，不处理 enclosing subgraph 的 open boundary。
- 2-WL/NBFNet：直接 pair/path propagation，理论上更 expressive，但不是“局部内部 + 外部 boundary operator”的可扩展架构。
- GPEN：global position + boundary-aware convolution，是最危险近邻；它的 global position 是节点位置编码，本报告方案的对象是针对每个 query cut 的外部 transfer map。

**One-day existence test**：

1. 生成 2,000 个 synthetic graph pairs；每一对共享完全相同的 query-centered k-hop interior，只有 boundary 外部连接不同。
2. 让 link label 依赖外部 boundary community/bridge state，同时控制 degree、CN、interior edge count。
3. 比较 GAE、SEAL-style GNN、BUDDY/ELPH-like sketch、NBFNet、GPEN-style global position 与 BCPF。
4. 观察 `score(interior fixed, exterior changed)`、AUC、boundary-swap sensitivity、runtime。

**PASS**：标准局部模型对外部 swap 不敏感；BCPF 能区分，且在固定参数/相同 interior 上有稳定收益。  
**FAIL/kill**：label 对外部 swap 不敏感；或 2-hop expansion/global position 已完全复现 BCPF；或 transfer map 只能带来参数增加而无 boundary-specific gain。

### Top 2：C5 WIQ

**Failure**：path count 并不等于 independent evidence；大量共享 prefix/suffix 的 path 会使模型过度相信重复 motif。

**Principle**：按 path-intersection structure 建立 evidence quotient，再聚合独立 path families，而不是简单 count、sum、orthogonalize high-order CN。

**危险先行**：OCN 已处理 higher-order CN redundancy；NBFNet 已做 semiring path aggregation；ELPH/BUDDY 已用 sketch 压缩子图。若 WIQ 只是在这些方法前增加“去重”，应淘汰。

**首日测试**：构造同一 path count 但不同 intersection graph 的 synthetic pairs；比较 NBFNet、OCN、sketch 和 WIQ 是否产生不同 score/排序。只有 WIQ 在 NBFNet/OCN 无法区分的 family-level cases 上有效，才保留。

### Top 3：C2 PIEL

**Failure**：同样数量、同样 hop 的 witnesses 经过 sum/mean 后得到相同 pair vector，但 witness 的 endpoint-role arrangement 不同。

**Principle**：把 evidence 作为有限 typed ledger 延迟压缩；pair decoder 读取按 role/hop/intersection 的 cells，而不是一个 pooled vector。

**危险先行**：SEAL 的结构标签与 pooling、2-WL pair state、BS-SubGNN、set transformer 都可能隐含解决此问题。必须证明 PIEL 不是“加几个 attention slots”。

**首日测试**：创建 `same counts / different arrangement` 图对，冻结同一个 GNN encoder，比较 sum、DeepSets、2-WL-lite、PIEL 的 distinguishability。若 PIEL 没有独特分离能力，放弃。

## 8. Reviewer attack：Top 3

### C1 可能的攻击

1. **“GPEN 已经 boundary-aware。”**  回答：GPEN 编码 global position 并做 boundary-aware convolution；C1 的边界状态是 query-specific cut 上的 external transfer operator，输入是外部图如何作用于该 boundary，而非节点在全图中的位置。必须用 boundary-swap experiment 证明差异。
2. **“只是参数更多。”**  回答：固定参数预算、固定 interior、固定训练步数；比较 `no-transfer / scalar boundary summary / full transfer`，并报告 boundary-swap sensitivity，不只报告 AUC。
3. **“直接换更强 backbone 就行。”**  回答：在相同 backbone 上只替换 hard crop 为 transfer boundary；若 NBFNet/2-WL 在不扩大预算下能完全解决，C1 应 kill。
4. **“Attention 可以自动学到。”**  回答：attention 只能重加权已看到的节点；被 cut 删除的 outside nodes 不在 key/value 中。只有加入 boundary operator，信息才进入计算图。
5. **“Decoder 可以补救。”**  回答：decoder 输入只包含 interior pooled representation；两个 external contexts 产生相同输入时，任何 decoder 都不能区分。
6. **“Failure 不存在。”**  回答：首日 synthetic same-interior/different-exterior test 是先决条件；不通过不做论文。
7. **“只在 Cora 有效。”**  回答：至少覆盖 Cora、Citeseer、PubMed、OGBL-Collab、OGBL-PPA，并加入 controlled boundary-swap synthetic benchmark。

### C5 可能的攻击

核心攻击是“OCN/NBFNet 已经做了去重/路径聚合”。若不能证明 path-intersection quotient 超出 high-order CN redundancy，直接撤回。

### C2 可能的攻击

核心攻击是“这只是 set transformer/2-WL/SEAL pooling 的换名字”。必须做 same-count/different-arrangement 的 expressiveness test，而不是只做随机 benchmark。

## 9. One-day existence tests

| Candidate | 一日最小实验 | PASS | Kill |
|---|---|---|---|
| C1 BCPF/SILP | same interior / different exterior boundary swap；比较 standard crop 与 transfer operator | 外部变化对 label/optimal score 有影响，且 standard crop 看不到 | 外部不影响，或 global position/2-hop 已等价 |
| C2 PIEL | same witness count / different role arrangement；冻结 encoder 比较 pooled vs ledger | ledger 能分离 pooled/DeepSets/2-WL-lite 不能分离的 pair | 任何强 set/pair baseline 已同样分离 |
| C3 QCMF | 同一 u 对不同 v 的 neighbor attribution/edge masking 是否不同 | 有稳定 target-dependent neighbor evidence | NBFNet/2-WL 已完全覆盖，或 attribution 不稳定 |
| C4 RNPL | 测 node-to-pair lift 前后 information probes 与 pair distinguishability | lift 前信息存在、普通 constructor 后消失，且 reversible lift 恢复 | 2-WL/strong decoder 已无差，或“可逆”只是 residual |
| C5 WIQ | same path count / different intersection graph | WIQ 超过 OCN/NBFNet/sketch | OCN/NBFNet 已同样分离 |
| C6 BFSP | 比固定 k-hop 与 boundary-first operator 的 marginal gain | 不扩大 subgraph 仍保留外部增益 | 只是 adaptive hop 的等价实现 |
| C7 NCPD | directed role-swap synthetic graph，比较 symmetric decoder | 只在 directed role case 有结构增益 | directed 2-WL/bilinear 已完全解决 |
| C8 PACH | 统计不同 pair 的 optimal depth 与 early-stop depth 分布 | depth 明显异质且能省算力 | optimal depth 集中在同一值 |
| C9 ESCI | line-graph context ablation，固定 link state | context injection 解决 node-feature loss 且非双分支收益 | EdgeConv/2-WL 已等价 |
| C10 BSAT | 同 topology、不同 boundary attribute transport；比较 SIEG/TAGNN/BSAT | 只有 boundary-transport condition 有收益 | global feature/IGLP 已等价 |

## 10. Final Top 1

### Chinese title

**边界守恒的成对链接预测图神经网络：通过外部图传输算子修复 enclosing-subgraph 截断信息丢失**

### English title

**Boundary-Conserved Pair Fields for Link Prediction: Preserving External Structural Influence Across Enclosing-Subgraph Cuts**

### Existing architecture

典型 SEAL-like LP：

```text
query pair (u,v)
  -> extract induced k-hop enclosing subgraph S_k(u,v)
  -> structural labels / node attributes
  -> node GNN on S_k
  -> pooling or pair constructor
  -> MLP / score
```

问题在于 `S_k` 是 induced subgraph；所有从 `S_k` 的 boundary 向外、再返回 boundary 或影响 boundary state 的结构都在 extraction 时被删除。

### Failure

存在两张图 `G_a,G_b`，对 query `(u,v)` 有完全相同的 `S_k(u,v)`，但 `S_k` 外部通过 boundary 连接到不同 community、bridge 或 long-cycle。标准 subgraph encoder 对二者输入完全相同，因此输出必然相同，即使 link formation mechanism 不同。

### Why irreversible

若 encoder 输入相同：

```text
S_k(G_a,u,v) = S_k(G_b,u,v)
```

则后续任何 decoder `D(z_u,z_v)`、更强 MLP、attention 或 bilinear 都只能得到同一结果。扩大 decoder 的函数类不能恢复 extraction 阶段已经删除的外部信息。这是比“decoder 不够强”更早的一次不可逆压缩。

### New architecture principle

> **Treat the target-pair enclosing subgraph as an open graph. Replace hard deletion at its cut boundary with a pair-specific external transfer operator that summarizes how omitted graph structure acts on boundary states.**

### Proposed information flow

```text
Old:
G -> induced S_k(u,v) -> node GNN -> pool -> decoder
       X (outside graph deleted)

New:
G -> interior I and cut boundary B for (u,v)
  -> external transfer T_B(G \ (I∪B))
  -> boundary state update on B using T_B
  -> message passing on I∪B with boundary condition retained
  -> pair readout from interior + boundary states
  -> ordinary decoder
```

一个可实现的近似是：

```text
T_B^(K) = sum_{r=0..K} α_r (A_external)^r
m_B^(l) = AGG_inside(B, I) + T_B^(K) h_B^(l)
```

更强但更昂贵的版本使用 boundary Schur complement / low-rank Neumann approximation。第一版不要追求精确矩阵逆，只要验证“external transfer 作为 state transition”这个 principle。

### Closest 5 papers

1. **SEAL / enclosing-subgraph LP**：通过 pair-specific local subgraph 学习结构启发式；差异是 hard induced crop，不保留外部 transfer。
2. **ELPH/BUDDY**：用 hashing/sketching 高效近似 subgraph features；差异是 sketch of structural features，不是 boundary-conditioned state transition。[ELPH/BUDDY](https://arxiv.org/abs/2209.15486)
3. **NBFNet**：以 query indicator 初始化，并沿路径做 generalized Bellman-Ford；差异是全图/关系路径传播，不是 fixed interior + external boundary interface。[NBFNet](https://arxiv.org/abs/2106.06935)
4. **GPEN**：global position encoding + boundary-aware convolution；差异是 node global position 与通用 boundary integration，不是 query-specific external transfer operator。[GPEN](https://proceedings.mlr.press/v267/wu25l.html)
5. **LLwLC / Spectral Basis Learning**：用 Neumann 与 vertex-deleted constraints 提升 LP expressiveness；差异是 spectral basis constraint，不是可学习的外部图到当前 pair boundary 的信息流。[LLwLC](https://ojs.aaai.org/index.php/AAAI/article/view/39044)

补充的直接比较对象：NCN/NCNC、OCN、LPFormer、Link-MoE、TAGNN、SE4LP。它们分别覆盖 structural feature order、higher-order redundancy、adaptive pairwise encoding、pair-level expert routing、结构/特征融合和 subgraph-to-pair architecture，但没有在本轮检索中发现与 C1 同构的 external transfer boundary state。

### Most Dangerous Prior Work

**最危险论文：GPEN（ICML 2025）**。

- **它做了什么**：对 subgraph representation 引入 global position encoding，并使用 boundary-aware convolution 选择性整合 global structural information。
- **为什么差点杀死 C1**：它已经同时触及“局部 subgraph 不够”和“boundary 可能需要 global context”，reviewer 很容易认为 C1 只是把 GPEN 换到 LP。
- **精确差异**：GPEN 的 global position 是对节点的全局位置描述；C1 的 `T_B(u,v)` 是对每个 query cut 计算的外部 transfer rule，改变的是 boundary state 的演化方程。C1 不增加一个全局位置通道，也不以 global position 作为 node feature。
- **如果 reviewer 引用它**：必须给出同-interior/different-exterior boundary-swap case：GPEN-style position、SEAL、global feature 不能稳定区分，而 C1 的 transfer operator 能区分；如果做不到，接受 reviewer 判断并撤回 C1。

### Exact novelty sentence

> **We introduce an open-boundary link encoder that preserves the omitted graph’s influence as a target-pair-specific boundary transfer operator, so external structural evidence is injected into enclosing-subgraph message passing without enlarging the subgraph or adding a second prediction branch.**

### Minimal prototype

只改 SEAL-like encoder 的 subgraph boundary：

1. 保留现有 `k=2` enclosing-subgraph extractor。
2. 标记 interior、boundary、outside-neighbor incidence。
3. 预计算一个稀疏 `K=1/2` external transfer sketch；不要一开始实现精确 Schur complement。
4. 每层在 boundary state 上加入 transfer message。
5. 仍使用原来的 node GNN、pooling、MLP、BCE、negative protocol 和 decoder。

因此最小代码变化是：`subgraph extraction / boundary message`，不是重写整个 LP system。

### One-day existence test

**Synthetic diagnostic**：

- 生成带两个 community 的 SBM、长环+bridge、以及 same-interior/different-exterior graph pairs。
- 选定 query `(u,v)`，固定 `S_2(u,v)` 的全部节点、边、属性、DRNL label。
- 只改变 boundary 外部的 community membership、bridge connection 和 length-3 return paths。
- 保持 degree、CN、interior edge count、node-feature marginal 尽量匹配。
- 训练/评估：SEAL-style crop、2-hop expanded crop、global-position baseline、NBFNet-lite、BCPF-lite。

**首日通过条件**：

1. 标准 crop 在 same-interior pair 上输出几乎相同；
2. 外部上下文与 label 有可重复关系；
3. BCPF-lite 的 boundary-swap sensitivity 显著高于 crop，同时不依赖更多参数；
4. 该增益在至少两种外部结构机制上出现，而不是单一 synthetic trick。

### Full experiment

**Datasets**：Cora、Citeseer、PubMed（可控小图）；OGBL-Collab、OGBL-PPA（规模与结构多样）；一个长程 synthetic benchmark；若扩展 temporal，再加入 TGB 数据，但不作为第一版主结论。

**Baselines**：CN/AA/RA；GCN/GraphSAGE/GAE；SEAL；ELPH/BUDDY；Neo-GNN；NCN/NCNC；MPLP；OCN；LPFormer；Link-MoE；NBFNet；2-WL-lite；GPEN-style boundary/global context；TAGNN；以及同 backbone 的 no-transfer ablation。

**Metrics**：保持标准 Hits@K / MRR / AUC；增加诊断指标但不把它包装成新 metric：boundary-swap sensitivity、same-interior distinguishability、performance vs external path length、runtime/memory。

### Ablations

```text
A0 standard induced subgraph
A1 retain only outside-neighbor count/scalar summary
A2 global position only
A3 fixed 1-hop external transfer
A4 fixed K-step transfer
A5 learned transfer operator
A6 remove boundary state update
A7 transfer without query pair conditioning
A8 same parameter budget / same backbone
```

关键判据是 `A5 > A4 > A1/A2 > A0` 不一定必须严格成立，但必须显示“transfer dynamics”而不是“多一个 feature”是收益来源。

### Engineering cost and scores

- Engineering cost：**3/5**（第一版只需 boundary index、稀疏 transfer 和 message update；精确 Schur complement 为后续可选版本）。
- Architecture originality：**8/10 provisional**。
- Feasibility：**7/10**；CPU/单 GPU 可以做小图 PoC，大 OGB 需要 sketch/precompute。
- SCI Q2/Q3 potential：**8/10**，前提是 synthetic failure + 多数据集机制验证成立。

### Kill criterion

满足任一条件立即停止，不再添加 attention、residual、extra loss 或更多分支：

1. same-interior/different-exterior test 中外部 boundary 对 label 没有稳定影响；
2. standard 2-hop expansion、GPEN-style global position 或 NBFNet-lite 已完全解决同一 failure；
3. transfer 只在增加参数/计算后提升，parameter-matched no-transfer 无差异；
4. boundary transfer 在真实数据集上只提升 Cora，且在 PubMed、OGBL-Collab、OGBL-PPA 无机制一致性；
5. 定向查重发现已有论文实现了同一 `external graph -> query boundary transfer operator -> pair-specific propagation` 信息流。

## 11. Rejected ideas and reasons

| Idea | Reject reason |
|---|---|
| Transformer + GNN | 模块堆叠；没有新的 failure/principle |
| Transformer + CN | NCN/LPFormer/Link-MoE/OCN 直接碰撞 |
| GCN + residual / deeper GNN | generic oversmoothing remedy，且不是 LP-specific |
| SEAL + Transformer | TAGNN、GPEN、SEAL+ 等近邻太多；只换 backbone |
| Degree/CN disentanglement | 明确超出本轮优先范围，且已有大量工作 |
| Conditional CN residual | NCN/NCNC/OCN/IGLP 近邻；属于 structural feature branch |
| hard negative / sampler / PU / calibration | 明确不属于本轮 architecture-only 核心 |
| pair-conditioned message passing（宽泛版本） | NBFNet、2-WL、GraIL、relational C-MPNN 已占用 |
| adaptive hop/depth | LPFormer、Link-MoE、adaptive receptive field、IGLP 已使 collision 至少 L2/L3 |
| stronger pair decoder | 2-WL、directed pair encoding、link expressiveness work；必须先证明 encoder 信息已存在 |
| higher-order CN 去冗余 | OCN 2025 已直接解决 |
| subgraph coarse-graining | SGCG 2025 已直接处理 subgraph-induced oversmoothing |
| generic boundary-aware convolution | GPEN 已直接使用；只有 external transfer operator 才可能保留 C1 |
| line graph + node branch | Line Graph NN/EdgeConvNorm/2-WL，且容易退化为 dual branch |
| temporal static-to-dynamic add-on | TNCN、TPNet、TGB-Seq 等已有直接路线；不适合当前低成本优先级 |

## Final decision

按严格门槛，**C1 当前是“暂定合格、尚未获得投资许可”**：architecture originality 暂定 8/10，但必须先通过 boundary-swap existence test 和 GPEN/LLwLC/NBFNet 定向查重。若测试或查重失败，则应严格判定为“本轮未发现合格架构创新”，而不是继续包装增量模块。

### 如果只能选择一个方向投入 3–6 个月

我会选择 **C1 BCPF/SILP**，但只在第一天通过后投入。

1. **真正新的 principle**：把 enclosing-subgraph 的 cut 当成 open boundary，用 query-specific external transfer operator 持续改变 boundary state；不是把 global feature、CN、attention 或 Transformer 拼上去。
2. **最危险论文**：GPEN（ICML 2025）；次危险是 LLwLC（AAAI 2026）和 NBFNet。
3. **精确差异**：GPEN 是 global position + boundary-aware convolution；LLwLC 是 spectral/constraint basis；NBFNet 是全图 query-conditioned path propagation。C1 是局部 pair subgraph 内的 external-to-boundary transfer dynamics。
4. **为何实现风险低于 Degree/CN disentanglement**：不需要定义 degree/CN 因果语义、不需要新 loss、不需要负样本策略、不需要双/三分支；先在 SEAL-like code 中改 boundary message 即可，失败也能局部撤销。
5. **第一天只做什么**：same-interior/different-exterior synthetic boundary-swap test；不先写完整模型，不先跑 Cora SOTA，不先加模块。
6. **立即放弃条件**：外部 swap 对 label 无稳定影响；或 GPEN/global position/2-hop/NBFNet-lite 已等价；或收益只来自参数与计算增加；或发现已有论文采用同一 external transfer operator。
