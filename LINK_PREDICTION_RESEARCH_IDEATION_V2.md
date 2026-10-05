# Link Prediction Research Ideation Report V2

## Adversarial Novelty Search：反向否证第一轮候选

> 研究主题：Link Prediction（静态、时序、属性图、异构图均允许）  
> 检索截止：2026-09-15（Asia/Shanghai）  
> 本轮性质：问题优先、对抗式新颖性检索、候选淘汰与最小存在性测试  
> 工作边界：本轮只做文献与研究设计，不修改 DCDLP 源码、不训练模型、不声称已经得到新的实验结果。

## 0. 先给严格结论

本轮没有继续沿用第一轮 Top 1。第一轮的 C1–C8 全部暂时降级，原因不是它们一定没有价值，而是它们的“核心问题—核心机制—目标”已经被新文献直接或近直接覆盖，不能再把原来的表述当作原创性结论。

本轮重新生成 15 个、与 C1–C8 不同的候选。经过逐个 Kill Search：

- 10 个候选直接淘汰；
- 5 个候选进入初筛 Top 5，但这不等于已经合格；
- 对初筛 Top 3 做 Reverse Novelty Test 后，N1 与 N3 被淘汰；
- N2 暂时通过最严格的一轮，N4、N5 仍只是未完成验证的备选；
- 当前可以作为“值得做一日存在性测试”的 Top 1 是 **N2：Regime-Conditional Gradient Conflict in Link Prediction**。

这不是“再设计一个 loss”。N2 的拟议贡献是一个可证伪的失败机制与诊断协议：**同一个训练目标下降时，不同 pair-level structural regimes 的梯度是否发生系统性冲突，从而造成局部 ranking 变差或模型排序反转。** 如果这个现象在控制 degree、负例分布和模型随机性后消失，N2 立即放弃。

因此，本轮最终状态是：

> **Qualified Top 1（条件性）：N2，仅在一日测试证明其独立于 degree、negative sampling 和普通 ranking-loss 效应后成立。**

这比强行把一个已经被撞过的 observation、abstention、risk-set 或 routing 方案继续包装成新论文更可靠。

## 1. 本轮必须纳入的直接否证

### 1.1 MTGN 已覆盖“缺失事件 + 时序链路预测”的核心组合

**Who Should I Engage with At What Time? A Missing Event Aware Temporal Graph Neural Network**（MTGN）公开版本的完整 PDF 为 15 页。论文不只是加入一个 missing-event feature：它把 observed events 与 missing events 建模为两个相互耦合的 temporal point processes，二者都依赖历史 observed events 与此前生成的 missing events；它还联合建模事件的 pair 和发生时间。[MTGN full paper](https://arxiv.org/pdf/2301.08399)

因此，以下表述已经不能作为新颖点：

1. “时序图中存在未观测事件”；
2. “同时预测 link existence 与 event time”；
3. “用一个 formation head 和一个 missing/observation head”；
4. “用生成缺失事件改善 temporal link prediction”。

如果仍要研究时序缺失，只能提出比 MTGN 更窄、可证伪且机制不同的问题；不能再把“missing events + temporal LP”当作空白领域。

### 1.2 DPU 已覆盖“真实关系机制 + 标注/观测机制”的双过程分解

**Predicting unknown viral hosts with Dynamic Positive-Unlabeled learning** 的 2025-08-05 版本是 Research Square preprint，不能等同于已正式同行评审论文；但其完整 36 页全文已经公开，且足以构成必须回应的先行工作。[DPU full preprint](https://assets-eu.researchsquare.com/files/rs-7187859/v1_covered_95e5258d-a6b6-4e28-9060-d68704b96442.pdf) [Sciety record](https://sciety.org/articles/activity/10.21203/rs.3.rs-7187859/v1)

DPU 明确区分：

- ground-truth mechanism：潜在关联是否真实存在；
- labeling mechanism：真实存在的关联以多大概率被观察、记录和标注；
- classifier：预测真实关联概率；
- propensity score model：预测一个真实关联被标注的概率。

论文还指出，两个模型会基于给定时间点数据库中的其他关联共同进行 context-aware 估计，并用 nested cross-validation、新标签和受控合成数据验证这一分解。[DPU methods/discussion](https://assets-eu.researchsquare.com/files/rs-7187859/v1_covered_95e5258d-a6b6-4e28-9060-d68704b96442.pdf)

所以，第一轮 C1 的下列表述全部降级：

- “formation probability 与 observation probability 分开建模”；
- “未观测边可能是真实负例，也可能只是未记录”；
- “时序 PU + propensity weighting 是新的统一问题”；
- “在 temporal GNN 上添加 observation head 即可形成新意”。

若未来重新使用这一主题，必须把贡献放到另一个明确问题上，例如可识别性边界、外部观测代理的可验证条件，或一种不同于 DPU/MTGN 的 estimand；否则不再作为候选。

### 1.3 其他强制纳入的碰撞底线

本轮把以下工作当成硬性 baseline 或危险先行，而不是检索结束后的补充引用：

- **Dynamic abstention**：`Predict Confidently, Predict Right: Abstention in Dynamic Graph Learning` 已将 coverage-based reject option 接入 continuous-time dynamic graph，并报告 coverage–risk / AUC / AP 权衡。[paper](https://arxiv.org/abs/2501.08397)
- **Node/pair topological failure**：ICLR 2024 的 TC 工作已经发现 newly joined neighbors 带来 topological distribution shift，并用 Topological Concentration 定位低性能节点。[paper](https://proceedings.iclr.cc/paper_files/paper/2024/hash/5b1b0c8d00e64a408bfcbed2a26c6718-Abstract-Conference.html)
- **Candidate/risk-set evaluation**：2026 年的 `Back to All-Entity Ranking` 已证明 CTDG 的 sampled-negative evaluation 会改变 Bayes-optimal ranking、模型相对排序和模块效应，并建议 all-entity ranking。[paper](https://arxiv.org/abs/2607.27861)
- **Pairwise regime variation**：`Revisiting Link Prediction: A Data Perspective` 分离 local structure、global structure 与 feature proximity；`Mixture of Link Predictors on Graphs` 已明确提出不同 node pairs 需要不同 pairwise information，并用 Link-MoE 做 pair-wise expert selection。[ICLR paper](https://proceedings.iclr.cc/paper_files/paper/2024/hash/154b90fcc9ba3dee96779c05c3108908-Abstract-Conference.html) [NeurIPS paper](https://papers.nips.cc/paper_files/paper/2024/file/1d0bcb52067128f826c86db234280dce-Paper-Conference.pdf)
- **Multiplicity / stability**：EMNLP Findings 2024 已把 predictive multiplicity 定义到 link prediction，并在 KGE 中观察到 8%–39% 测试 query 的冲突；2026 ESWC 接收工作进一步分析 seed、triple order、negative sampling、dropout 和 hardware 导致的 triple-level instability。[multiplicity](https://aclanthology.org/2024.findings-emnlp.19/) [stability](https://arxiv.org/abs/2606.03365)
- **Link-level expressiveness**：NeurIPS 2025 已系统研究 link representation expressiveness、link-level symmetry 与 dataset-aware model selection。[paper](https://papers.nips.cc/paper_files/paper/2025/hash/b1cd72276feff8173462e3f733ac66f8-Abstract-Conference.html)
- **Degree and ranking bias**：ICML 2025 已证明常见 edge sampling 对 high-degree nodes 有隐性偏置，甚至 degree-only null predictor 也可能近似最优；Gelato 已将 sparse LP、N-pair ranking 与 hard negatives 结合。[ICML paper](https://proceedings.mlr.press/v267/aiyappa25a.html) [Gelato](https://arxiv.org/abs/2412.00261)

## 2. 对第一轮 C1–C8 的重新判定

| 第一轮 | 本轮状态 | 直接或近直接否证 | 为什么不能继续沿用原表述 |
|---|---|---|---|
| C1 Exposure-Process-Aware TLP | **降级** | MTGN 2024；DPU 2025 preprint | observed/missing event coupling 与 formation/labeling 双过程均已有；不能再声称统一双过程是原创 |
| C2 Risk-Set / Eligibility-Aware TLP | **淘汰为主线** | Back to All-Entity Ranking 2026；HeaRT；TGB | “更合理的候选集”若无新 estimand，只是重新命名 negative candidate correction |
| C3 Support-Conditioned Selective LP | **降级** | Dynamic abstention 2025；conformal LP；dynamic conformal prediction | generic reject/coverage/risk 已有，不能只把 confidence 换成 support |
| C4 Neighborhood-Ingress Mismatch Repair | **降级** | ICLR 2024 TC；CRAFT；TGB-Seq；近期 temporal neighbor models | newly joined neighbor 的失败现象已被点名，改名或加 temporal attention 不够 |
| C5 Disagreement-Calibrated LP | **降级** | EMNLP 2024 multiplicity；2026 KGE instability；Link-MoE | “多个模型冲突 + voting/ensemble/calibration”已有直接路线；换 KGE 为 GNN 不足 |
| C6 Safe Cross-Network TLP | **降级** | MiNT；FLEX；Stable Prediction；Domain Matters 2026；MetaGL | generic transfer/OOD/model selection 已拥挤，需不同的可验证机制 |
| C7 Missing-vs-Spurious Edge Process Separation | **降级** | bilateral edge noise；Bayesian graph inference；MTGN/DPU | generic noise separation 与 missingness 已有；不能只是再加 noise classifier |
| C8 Mechanism-First LP Reliability Benchmark | **降级** | HeaRT；TGB/TGB 2.0；all-entity；Domain Matters | 评价协议本身有价值，但不能伪装成普通新模型；需明确新 estimand 或新实验因素 |

## 3. 对抗式检索协议

### 3.1 检索原则

本轮不把“没有搜到同名论文”当作创新证据。每个新候选都按五层检查：

> problem → phenomenon → mechanism → objective → implementable test

并使用下列查询簇：

1. 现象词：`unexpectedly`、`surprisingly`、`however`、`fails when`、`degrades under`、`inconsistent`、`limitation`、`we observe`、`counterintuitive`、`underperforms`、`unstable`、`sensitive to`；
2. pair-level 词：`pair-level difficulty`、`pair-specific failure`、`edge-level uncertainty`、`dyadic shift`、`pair topology`、`pair feature conflict`、`edge regime`；
3. 机制词：`gradient conflict`、`loss-ranking mismatch`、`order aliasing`、`structural indistinguishability`、`automorphism`、`shortcut`、`recurrence`、`community ambiguity`、`calibration`；
4. 任务替换：`link prediction`、`temporal graph`、`graph learning`、`knowledge graph completion`、`recommender`、`KGE`；
5. 反向引用：对危险先行的标题、作者、代码仓库和后续引用再次检查。

### 3.2 碰撞等级

- **L0**：暂未检出同问题、同机制、同目标的公开工作；仍不能据此声称绝对原创。
- **L1**：问题相近，但核心机制和 estimand 不同；可进入验证。
- **L2**：同问题或同机制已跨领域出现，必须给出 graph-LP-specific 的可证伪差异。
- **L3**：同问题 + 同机制 + 同目标，或只是换数据、backbone、loss、模块；淘汰。

### 3.3 接受条件

候选只有同时满足以下条件，才可从“初筛候选”升级为“合格方向”：

1. 不是已发表的同题目/同机制重述；
2. 没有跨领域的同问题 + 同机制 + 同目标直接先例；
3. 不是 old problem + new loss；
4. 不是 old model + new feature；
5. 不是两个已有模块串联；
6. 一天内可以证明问题是否存在；
7. 即使 MRR 不提升，问题发现或失败机制本身仍具有学术价值。

## 4. 第二轮重新生成的 15 个候选

以下 N1–N15 均不是第一轮 C1–C8 的重复命名。它们先以“问题假设”提出，再立刻做 Kill Search；表中的“新”只表示相对于第一轮新生成，不表示已经完成投稿级的绝对新颖性证明。

| ID | 新问题假设 | 立即执行的 Kill Search 查询簇 | 最危险先行 | 结果 |
|---|---|---|---|---|
| N1 | **Temporal-order sufficiency / order aliasing**：两个 pair-history 拥有相同事件计数、recency 和静态聚合统计，但事件顺序不同，未来 ranking 发生系统性差异；模型可能把顺序压成不可辨认的 alias。 | `temporal order link prediction permutation`; `same aggregate different event order temporal graph`; `event sequence aliasing link prediction`; `temporal walk link prediction`; `dynamic graph sequence order failure` | MTGN、TPNet、TGB-Seq、CRAFT | **初筛保留；L1–L2**。已有时序模型使用 order，但“等统计量 order-swap 的 pair-level 失败诊断”仍需验证；不允许直接提出又一个 temporal encoder。 |
| N2 | **Regime-conditional gradient conflict**：全局训练 loss 下降，但由 pair topology / feature conflict / temporal state 划分的不同 edge regimes，其 per-regime gradient 方向发生冲突，导致某些 regime 的 top-k ranking 变差。 | `gradient conflict link prediction graph`; `link prediction loss ranking mismatch`; `structural regime gradient graph neural network`; `pairwise ranking gradient link prediction`; `loss decreases ranking performance graph` | Gelato、PNAS bias-aware training/evaluation、HeaRT、all-entity ranking | **初筛保留；暂为 L0–L1**。暂未检出同一 graph-LP-specific 问题与机制的直接工作；必须先证明不是 degree、sampler 或普通 imbalance。 |
| N3 | **Symmetry-preserving decision identifiability**：即使两个 pair 的 representation 可分，top-k decision 在保持图结构等价的 permutation / automorphism-preserving perturbation 下仍可能不稳定；要区分 representation expressiveness 与 decision identifiability。 | `link prediction structural indistinguishability automorphism top-k`; `pair decision stability graph symmetry`; `equivalent enclosing subgraph link prediction`; `2-WL link prediction expressiveness` | 2D-WL LP；NeurIPS 2025 link representation expressiveness / LR-EXP | **初筛保留但高危；L2**。若只是把 symmetry metric 改写成 top-k stability，属于直接延伸，Reverse Test 很可能失败。 |
| N4 | **Edge-regime model-ranking sample complexity**：不是问哪个模型平均最好，而是问在多少 network / pair-regime 样本后，两个模型的相对排序才足以稳定；模型可能在 Cora 与 OGB 的“总体胜负”相反，但真正的驱动因素是 edge regime 构成。 | `link prediction model ranking stability sample size`; `domain matters link prediction ranking stability`; `graph model selection link prediction`; `pair regime benchmark model ranking` | Domain Matters 2026；Stable Prediction on Graphs；MetaGL；Stacking models for LP | **初筛保留但高危；L2**。如果只输出更多数据集、置信区间和一个 ranking coefficient，就是 benchmark 扩展，不够。 |
| N5 | **Explanation instability under score-preserving interventions**：两个模型或两个 checkpoint 对候选边给出近似相同分数/排名，但支持该决定的 rationale subgraph 在结构保持或 score-preserving perturbation 下明显变化；预测稳定不等于解释稳定。 | `explanation stability link prediction`; `self-explainable GNN link prediction`; `counterfactual explanation edge prediction`; `rationale stability graph neural network`; `link prediction explanation consistency` | Self-Explainable GNNs for LP；SIG；counterfactual explainability；ranking-preserving explanation | **初筛保留但高危；L2**。解释稳定性在 GNN/XAI 中已有广泛路线；只有 link-specific score-preserving protocol 可能保留。 |
| N6 | **Topology–feature conflict without routing**：冲突并不一定应该被 MoE 路由解决；可能先要检测冲突对 label semantics 的影响，并区分“真正互补”与“shortcut cancellation”。 | `topology feature conflict link prediction`; `feature structural incompatibility LP`; `conflict-aware link prediction`; `graph link prediction feature heterophily` | ICLR 2024 Data Perspective；Mixture of Link Predictors；feature heterophily LP；TAGNN | **淘汰，L3**。问题和 pair-wise expert/routing/heterophily 组合已有直接路线；不准用“加一个 conflict detector”复活。 |
| N7 | **Decoder answer-space bottleneck**：encoder 已能区分 pair，但 decoder 在大候选空间中无法保留正确 rank；性能下降来自输出空间瓶颈而非 message passing。 | `theoretical limitations embedding link prediction decoder`; `large answer space link prediction bottleneck`; `link prediction decoder expressiveness`; `all entity ranking decoder` | On Theoretical Limitations of Embedding-based LP；all-entity ranking；TGRank | **淘汰，L3**。核心瓶颈、混合 softmax 与答案空间已被直接讨论；换 GNN 或加 decoder 不构成新问题。 |
| N8 | **Persistence vs reactivation life-cycle**：同一 pair 的持续互动、沉寂后重新激活和一次性新边可能共享 repeat/new 标签，但未来 hazard 不同。 | `temporal link prediction reactivation persistence`; `recurring interaction reactivation graph`; `temporal knowledge graph recurrence link prediction`; `repeat unseen edge life cycle` | TGB-Seq；CRAFT；TIMEPLEX；MTGN | **淘汰，L3**。只是把 repeat/new 细分，仍落在已有 temporal recurrence / sequence dynamics 线上；不能以三个 label 重新命名。 |
| N9 | **Identity shortcut collapse**：transductive LP 可能使用 node identity / repeated pair identity，inductive 或 node permutation 后性能坍塌；要测的是 shortcut activation 而非普通 OOD。 | `node identity shortcut link prediction`; `transductive inductive link prediction shortcut`; `BGRL link prediction inductive`; `link prediction permutation memorization` | BGRL/T-BGRL；SIG 的 shortcut robustness；target-link inclusion pitfalls | **淘汰，L3**。identity/permutation/inductive shortcut 已有直接研究，不能只换数据集。 |
| N10 | **Community ambiguity propagation**：社区边界本身不确定时，pair score 的置信度和错误会随社区划分方案反转；问题不是社区特征有用，而是 community assignment uncertainty 进入 link decision。 | `ambiguous community structure link prediction`; `community uncertainty link prediction`; `community detection uncertainty edge prediction`; `bridge within community link prediction` | Community-structure LP studies；PNAS topological feature capability；Domain Matters 2026 | **淘汰，L2–L3**。社区结构影响 LP 已被大规模研究；不确定社区 + 新 loss 仍是旧问题加模块。 |
| N11 | **Structural-regime conditional calibration**：全局 ECE 合格不代表 pair topology regime 内可靠；尤其 feature-conflict 与 low-support pair 可能出现相反 calibration。 | `conditional calibration link prediction graph`; `edge-level calibration GNN link prediction`; `conformal link prediction structural`; `dynamic link prediction calibration` | IN-N-OUT；Conformalized LP；Valid CP for Dynamic GNNs；dynamic abstention | **淘汰，L3**。link-specific calibration、conditional coverage、dynamic CP 已有密集碰撞；换分层定义不够。 |
| N12 | **Task-irrelevant neighbor-feature contamination**：邻居属性对 node task 有益，但对 link task 是系统性干扰；应先证伪其因果相关性而非直接删 feature。 | `task irrelevant neighbor features link prediction`; `neighbor feature noise LP`; `feature-free topology link prediction`; `link-centric GNN noise` | TAGNN 2026；AAAI structural information enhanced LP；feature heterophily LP | **淘汰，L3**。TAGNN 已直接提出并验证去除邻居特征；不再提出同一现象。 |
| N13 | **Temporal window granularity aliasing**：离散窗口把连续互动的持续、同时和跨窗事件混为同一 label，模型排名随窗口宽度改变；不是普通 time encoding 问题。 | `temporal window granularity link prediction`; `continuous discrete temporal graph link prediction`; `event aggregation temporal LP`; `snapshotization bias link prediction` | TLP-CCC；MTGN continuous-time formulation；TPNet temporal walk | **淘汰，L2–L3**。离散化与连续时间的差异早已有；若只比较不同 window 是实验设置，不是机制创新。 |
| N14 | **Cross-domain ranking reversal from edge-regime composition**：不同领域的胜负不只是 domain label，而是 pair-level regime mixture 造成；目标是无标签判断某次迁移是否安全。 | `domain shift link prediction model ranking reversal`; `cross-network link prediction model selection`; `domain-informed evaluation LP`; `safe transfer graph link prediction` | Domain Matters 2026；MiNT；FLEX；MetaGL；Stable Prediction | **淘汰，L3**。问题、目标和机制都已有；把 domain feature 换成 edge-regime feature 不够。 |
| N15 | **Graph-size transition of heuristic sufficiency**：图规模增大时，local heuristic、node embedding 和 pair encoder 的相对优势可能发生相变；要估计 transition，而非只做大图 benchmark。 | `graph size scaling link prediction heuristics`; `larger test graph OOD link prediction`; `link representation graph symmetry model selection`; `local heuristic scalability LP` | NeurIPS 2022 gMPNN OOD；NeurIPS 2025 link expressiveness；TAGNN；HeaRT | **淘汰，L2–L3**。规模 OOD、pair representation 与 model selection 已有理论与实验，transition curve 仍不足以独立成稿。 |

### 4.1 淘汰统计

被明确淘汰的 N6–N15 共 10 个，达到本轮要求的“至少淘汰 10 个”。淘汰原因不是“想法不好”，而是它们分别落入以下已拥挤簇：

- topology/feature routing 或 MoE；
- decoder / answer-space bottleneck；
- repeat/new 的细分；
- identity shortcut / inductive OOD；
- community effect；
- conditional calibration / abstention；
- neighbor-feature removal；
- temporal snapshotization；
- cross-domain model selection；
- graph-size expressiveness。

## 5. 初筛后 Top 5：只保留可继续攻击的方向

这里的 Top 5 不是“已合格 Top 5”，而是经过直接 Kill Search 后仍值得做一日验证的五个方向。它们都必须携带一个最危险先行；如果无法回答该先行，立即淘汰。

### Top 1 / N2：Regime-Conditional Gradient Conflict in Link Prediction

#### Problem

常见 LP 训练把所有正负 pair 的损失平均化。即使整体 BCE、N-pair 或 sampled ranking loss 持续下降，模型可能在某类 pair 上改善、在另一类 pair 上恶化；现有报告通常只给总体 AUC/AP/MRR，不知道这种反向变化是否来自结构 regime 之间的梯度冲突。

这里的 pair regime 不能只按 degree 划分。候选划分至少包含：

- local overlap：CN / weighted overlap / enclosing-subgraph pattern；
- pair topology：shortest-path / common-neighbor diversity / bridge-vs-within-community；
- feature relation：feature agreement、feature conflict、heterophily score；
- temporal state（若用时序图）：recency、reactivation state、pair-history pattern。

#### Discovery

真正需要发现的不是“某个 loss 更好”，而是：

> 在控制负例分布与 pair 数量后，全局梯度是否会系统性牺牲某个结构 regime；这种牺牲是否先于总体指标下降而发生。

本轮精确检索 `gradient conflict + link prediction`、`loss-ranking mismatch + graph LP`、`structural regime gradient`、`pairwise ranking gradient + graph`，未检出同一 graph-LP-specific 现象、同一机制和同一诊断目标的直接论文。检索结果主要落在 degree bias、ranking loss、hard negative、multi-task gradient balancing 或 generic GNN stability 上。

#### Mechanism

对每个 regime (r) 定义 per-regime loss gradient：

\[
g_r = \nabla_\theta L_r,
\]

并定义 regime 间的梯度冲突：

\[
C(r,s)=1-\cos(g_r,g_s).
\]

关键不是 C 的绝对数值，而是同时观察三件事：

1. global loss 下降；
2. 某 regime 的 one-step ranking 或 Hits@K 下降；
3. 这种反向变化在 degree-matched、negative-count-matched 和 sampler-controlled 条件下仍存在。

#### New idea

暂不提出新的优化 loss。先提出一个 graph-LP-specific 的 **Regime-Conditional Gradient Audit（RCGA）**：

- 输入：现有模型、现有训练目标、同一批 pair；
- 输出：每个 pair regime 的梯度方向、一步更新后的 rank 变化、全局 loss 与局部 rank 的分离曲线；
- 目标：判断所谓“训练变好”是否只代表某些结构 regime 变好。

如果现象成立，后续才考虑最小的 regime-aware training；如果现象不成立，不能用新 loss 强行制造贡献。

#### Most Dangerous Prior Work

最危险的先行不是某一篇单独论文，而是三件事的合取：

1. **Gelato / Attribute-Enhanced Similarity Ranking for Sparse LP** 已把极端稀疏、N-pair ranking loss 和 hard negatives 放在一起；
2. **Implicit degree bias in LP** 已证明 sampling/evaluation 会偏向 high-degree，并提出 degree-corrected benchmark；
3. **HeaRT / Back to All-Entity Ranking** 已证明 negative sampler 和 candidate set 会改变排序结论。[Gelato](https://arxiv.org/abs/2412.00261) [degree bias](https://proceedings.mlr.press/v267/aiyappa25a.html) [HeaRT](https://proceedings.neurips.cc/paper_files/paper/2023/hash/0be50b4590f1c5fdf4c8feddd63c4f67-Abstract-Datasets_and_Benchmarks.html) [all entity](https://arxiv.org/abs/2607.27861)

它们几乎会杀死 N2，因为审稿人可以说：你看到的只是 class imbalance、degree bias、hard negative 或 sampler-dependent ranking。

#### Core same / core different

相同之处：都承认训练目标、采样和 ranking 可能让 LP 结论发生偏差。

不同之处：N2 不改 sampler、不改 candidate set、不发明 ranking loss，也不把 degree 当作 regime；它要测的是 **同一训练批次中的 pair-regime gradient interference 是否导致局部排序反转**。这必须通过 matched controls 证明，而不能只靠命名。

#### Reviewer response

审稿人若指出“这是 degree bias”，回答必须是可检验的：

- degree-matched pair bins；
- identical negatives / all-entity evaluation where feasible；
- same backbone、same loss、same budget；
- report gradient cosine and one-step rank delta；
- random-label and shuffled-regime controls；
- 如果效应在这些控制后消失，主动承认 N2 被 degree/sampler 解释，放弃。

#### One-day existence test

1. 选一个小属性图（Cora 或 Citeseer）和一个 OGB/较大图；若保留时序版本，再加一个 TGB 数据集。
2. 固定现成 GNN/heuristic baseline，不搜索新架构；使用相同正负 pair。
3. 以 CN、shortest-path、feature conflict、community bridge 等划分 pair regime，并对 degree 做 matching 或 residualization。
4. 在训练早期、中期、后期记录每个 regime 的 (g_r)、与 global gradient 的 cosine、one-step update 后的 score/rank 变化。
5. 观察是否存在：global loss 下降，但某 regime 的 ranking 下降，且该现象跨至少两个数据集或两个 backbone 重复。

#### Kill condition

满足任一项立即停止：

- 冲突只在 degree 不平衡或 hard-negative 分布不匹配时出现；
- all-entity / fixed-candidate evaluation 后冲突消失；
- 只有总体 AUC 变化，没有 pair-regime rank evidence；
- 不同随机 seed 的波动大于 regime effect；
- 现象不能在不读取 test labels 的训练/验证流程中复现；
- 贡献只能写成“加入一个 regime-aware loss 后 MRR 提升”。

### Top 2 / N1：Temporal-Order Sufficiency / Order Aliasing

#### Problem and mechanism

一些 temporal LP 模型可能对 pair-history 的总计数、最近时间和节点状态很敏感，但对更细的事件顺序不具备可辨识性。构造两个历史：

- 相同 pair count；
- 相同 last-event time；
- 相同节点 activity summary；
- 仅交换中间事件顺序。

如果真实 future ranking 或模型 ranking 对 order swap 有系统性变化，就出现 order aliasing。

#### Most Dangerous Prior Work

MTGN 已把 observed/missing event 及 event time 放进耦合 TPP；TPNet 已把 temporal walk matrix 与 time decay 统一起来；TGB-Seq、CRAFT 等已强调序列动态和 recurring/novel interactions。[MTGN](https://arxiv.org/pdf/2301.08399) [TPNet](https://proceedings.neurips.cc/paper_files/paper/2024/hash/ff7bf6014f7826da531aa50f4538ee19-Abstract-Conference.html) [TGB-Seq](https://proceedings.iclr.cc/paper_files/paper/2025/hash/db5ca61dbc08cf5143c05ad2d1b0b2ca-Abstract-Conference.html) [CRAFT](https://proceedings.neurips.cc/paper_files/paper/2025/hash/036912a83bdbb1fd792baf6532f102d8-Abstract-Datasets_and_Benchmarks.html)

#### Why it almost kills the idea

审稿人可以说：只要模型使用 temporal sequence，就已经在编码顺序；order-swap 只是普通 temporal ablation。

#### Core same / core different

相同：使用时间顺序解释 temporal LP。

不同：N1 不提出一个更深的 sequence model，而是定义 **统计量相同、顺序不同的反事实 pair histories**，测模型是否把未来 ranking 错误归因于 summary statistics。学术价值来自 failure mechanism 和 benchmark protocol，而不是换 encoder。

#### Reverse result

Reverse rejection：

> “This work is not novel because MTGN/TPNet/TGB-Seq already model temporal order; you only permute events and report another ablation.”

可用的反驳必须同时证明：

1. 现有模型在 summary-matched order swap 下出现稳定错误；
2. 该效应不是 recency、activity、repeat/new 或 missing-event 的重命名；
3. 结果能产生一个新的可证伪边界，而不是“某 encoder 更强”。

本轮认为这三个条件还不够稳，故 N1 **Reverse Test 淘汰**。

### Top 3 / N4：Edge-Regime Model-Ranking Sample Complexity

#### Problem

不同论文常用不同数据集和不同 pair 组成，最后给出“模型 A 优于模型 B”。更细的问题是：在固定 evaluation estimand 下，要积累多少 network 或 pair-regime 样本，模型相对排序才稳定？Cora/Citeseer 与 OGB/HeaRT/temporal/domain shift 中出现的 ranking inversion，可能由 edge-regime composition 而非模型整体能力造成。

#### Most Dangerous Prior Work

`Domain matters: Towards domain-informed evaluation for link prediction` 已在 740 个网络、7 个领域上讨论 domain-specific winner 与 Ranking Stability Coefficient；MetaGL 已研究无评估的 graph model selection；Stable Prediction on Graphs 直接把跨非 IID 图的平均性能和低方差作为目标。[Domain Matters](https://doi.org/10.1016/j.physa.2026.131551) [MetaGL](https://arxiv.org/abs/2206.09280) [Stable Prediction](https://proceedings.mlr.press/v218/zhang23a.html)

#### Why it almost kills the idea

审稿人可以说：这只是把 domain-level sample complexity 改成 edge-level sample complexity，再多报几个置信区间。

#### Core same / core different

相同：都研究 model ranking stability。

不同：N4 的 estimand 是 **固定 pair-regime composition 下的模型胜负可识别性**，不是寻找每个 domain 的 winner，也不是训练 model selector；它应输出 regime-stratified ranking uncertainty 与最低样本量。

#### Reverse result

Reverse rejection：

> “This work is not novel because Domain Matters and MetaGL already study domain-aware model selection and ranking stability; your contribution is only a finer partition and another coefficient.”

如果主要 rebuttal 只能说“我们用了新的数据集、新的 backbone 或新的 ranking coefficient”，这恰好触发用户设定的淘汰条件。因此 N4 目前 **不升级为合格模型创新**，仅保留为可做的 evaluation study。

### Top 4 / N3：Symmetry-Preserving Decision Identifiability

#### Problem

结构表达能力与最终 top-k decision 不是同一个对象。一个模型可能在 representation 层区分两个 link，但在候选排序、tie-breaking 或结构等价变换后仍给出不稳定 decision。

#### Most Dangerous Prior Work

2D-WL link prediction 已研究 pair representation 的表达力；NeurIPS 2025 已提出 link-level expressiveness framework、LR-EXP 和 graph symmetry metric，并将 symmetry 与 dataset-aware model selection 连接起来。[2D-WL](https://arxiv.org/abs/2206.09567) [NeurIPS 2025 expressiveness](https://papers.nips.cc/paper_files/paper/2025/hash/b1cd72276feff8173462e3f733ac66f8-Abstract-Conference.html)

#### Reverse result

Reverse rejection：

> “This work is not novel because link-level symmetry and expressiveness have already been formalized; you only move from embedding separability to top-k stability.”

这已经是同一问题的紧邻延伸，且新增内容很容易退化成新 metric。N3 **淘汰**。

### Top 5 / N5：Explanation Instability under Score-Preserving Interventions

#### Problem

不同模型可以给出相近 score 与相同 top-k，但其 explanatory subgraph 不同；若在不改变 score 或 rank 的小扰动下 rationale 大幅变化，说明“预测稳定”并不推出“机制解释稳定”。

#### Most Dangerous Prior Work

Self-Explainable GNNs 已针对 LP 设计 pair-specific explanation；SIG 已把 CTDG link prediction 与解释、shortcut robustness 结合；近期 counterfactual explainability 也把 missing-edge prediction 与解释管线耦合。[Self-Explainable LP](https://arxiv.org/abs/2305.12578) [SIG](https://arxiv.org/abs/2405.19062) [counterfactual explainability](https://arxiv.org/abs/2606.22033)

#### Initial judgment

N5 仍可作为解释审计问题，但不能声称“首次研究 LP explanation stability”。需要一个真正不同的 estimand，例如在 score-preserving intervention 下测 rationale equivalence class，而不是普通 explanation consistency。

当前不将 N5 升级为合格 Top 1；保留为第二备选，等待一日测试确认是否存在可重复的 link-specific phenomenon。

## 6. Top 3 Reverse Novelty Test 汇总

| 候选 | 最强拒稿句 | 是否有强反驳 | 最终判定 |
|---|---|---|---|
| N2 Gradient conflict | “这是 degree bias / sampler bias / ranking loss 的旧问题。” | **有条件**：若 degree-matched、all-entity、same-loss 后仍有 regime gradient interference，并且它预测局部 ranking 反转，则反驳不是数据或 backbone 差异。 | 暂时保留为条件性 Top 1 |
| N1 Order aliasing | “所有 temporal model 都已编码 order；你只是做 permutation ablation。” | **不够强**：除非证明 summary-matched counterfactual 是新 estimand，否则只是 temporal encoder 分析。 | 淘汰 |
| N4 Ranking sample complexity | “Domain Matters/MetaGL 已研究 ranking stability；你只换粒度和指标。” | **不够强**：若贡献只剩更多数据集、backbone 或 coefficient，属于用户禁止的表面差异。 | 淘汰为模型主线，保留为 evaluation 备选 |

## 7. 最终 Top 1 研究卡：N2

### Problem

Link prediction 的训练损失通常对不同 candidate pair 进行合并优化，但最终评价是 pair ranking。现有结果可能掩盖一种更具体的 failure：**全局 loss 变小，某些结构 regime 的 ranking 却变差。** 这不是简单的 global AUC 与 MRR 不一致，而是要证明：不同 pair regimes 对参数更新的方向存在系统性干扰。

### Discovery

待验证的 discovery 是：

> 在相同训练目标、相同负例和相同计算预算下，pair-level structural regimes 之间是否存在可重复的梯度方向冲突，并且该冲突能否预测下一步或下一阶段的局部 ranking deterioration。

这是一个实验命题，不是已经成立的事实。报告中不把它写成已有结果。

### Mechanism

1. 用可预测时刻的 prefix information 对 pair 分 regime；
2. 对每个 regime 单独计算 loss gradient；
3. 计算 regime-to-regime gradient cosine / conflict；
4. 用 one-step parameter update 观察各 regime 的 score 和 rank 变化；
5. 检查 global loss、global metric、regime metric 三者的时间序列是否分离。

必须控制：degree、pair count、negative distribution、candidate set、seed、backbone 和 total compute。

### New idea

提出 **Regime-Conditional Gradient Audit（RCGA）** 作为 graph-LP-specific 诊断协议，而非先提出一个新 loss。它可以产出三类学术结果：

- 若存在独立冲突：定义一个过去未被单独测量的 LP failure mechanism；
- 若只在 degree/sampler 下存在：提供对已有结果的否证，说明不应再提出 N2；
- 若只在特定数据集存在：形成边界条件，而不是虚假的普遍结论。

只有第一种或第三种具有足够证据时，才考虑后续的最小干预；干预不能成为论文的唯一贡献。

### Most Dangerous Prior

1. [Attribute-Enhanced Similarity Ranking for Sparse Link Prediction / Gelato](https://arxiv.org/abs/2412.00261)：已用 ranking loss 与 hard negatives 处理 sparse LP；
2. [Implicit degree bias in the link prediction task](https://proceedings.mlr.press/v267/aiyappa25a.html)：已证明 edge sampling 会把 LP 推向 degree-dependent solution；
3. [Evaluating GNNs for LP: HeaRT](https://proceedings.neurips.cc/paper_files/paper/2023/hash/0be50b4590f1c5fdf4c8feddd63c4f67-Abstract-Datasets_and_Benchmarks.html)：已指出 easy negatives 与评测设置问题；
4. [Back to All-Entity Ranking](https://arxiv.org/abs/2607.27861)：已证明 candidate sampler 会改变模型排序与模块效应。

### Exact difference

N2 与这些工作都承认 LP 的 ranking 可能被训练/评估过程扭曲；但 N2 的精确差异必须是：

- 不以新的 negative sampler 为贡献；
- 不以 degree correction 为贡献；
- 不以新的 ranking loss 为贡献；
- 不以换 GNN backbone 为贡献；
- 在固定或 all-entity candidate 下，研究 pair-regime gradient geometry；
- 以局部 ranking deterioration 为结果，而不仅是总体 AUC/MRR 差异。

如果最后只能实现“按 regime 加权 loss”，则 N2 自动降级为 old problem + new loss，不合格。

### One-day test

最小实验不需要大规模新模型：

1. 数据：Cora/Citeseer + 一个 OGB 或可枚举 temporal dataset；
2. 模型：固定一个轻量 GNN 与一个 heuristic/MLP baseline；
3. pair regimes：CN/shortest-path/feature-conflict/community-bridge 四类信号，不能只用 degree；
4. matching：在 degree、pair 数和负例数量上匹配；
5. 记录：per-regime loss、gradient cosine、one-step rank delta、global metric delta；
6. 结果门槛：至少两个数据集、至少两个 seed 中出现相同方向的“global loss ↓ + 某 regime ranking ↓”，且效应量大于 seed 波动；
7. 失败则停止，不继续堆模块。

### Kill condition

N2 在以下任一情况下被杀死：

- 现象由 degree-only predictor 解释；
- 现象只由 sampled-negative distribution 解释；
- all-entity 或 fixed-candidate evaluation 后消失；
- gradient conflict 与 local ranking 没有关系；
- 只有一个数据集或单个 seed 有效；
- 需要读取 test label、未来边或不可用信息才能定义 regime；
- 最终贡献退化为一个新的 regime-aware loss 和平均 MRR 提升。

## 8. 研究问题与可发表边界

### 8.1 最小研究问题

**RQ1.** 在固定 candidate/evaluation protocol 下，link-pair structural regimes 的梯度方向是否存在系统性冲突？

**RQ2.** 这种冲突是否能预测局部 ranking deterioration，而不是仅改变 loss 或 calibration？

**RQ3.** 冲突是否独立于 degree bias、negative sampling、candidate-set size 与 random seed？

**RQ4.** 冲突是否跨属性静态图与 temporal graph 复现，还是只属于某类 edge-generating regime？

### 8.2 结果解释矩阵

| 结果 | 解释 | 行动 |
|---|---|---|
| 冲突强且独立，跨数据集复现 | N2 问题成立 | 写 failure-mechanism / diagnostic paper；再设计最小干预 |
| 冲突存在但只在 degree 或 sampler 控制前 | 旧 bias 现象 | 引用 Aiyappa/HeaRT/Gelato，不做 N2 |
| 冲突只在某一模型 | 可能是 implementation/backbone artifact | 不做普遍方法论文，最多做案例分析 |
| loss 与 rank 不分离 | N2 不成立 | 停止 |
| 只有平均指标提升 | 贡献不够 | 停止，不加入新 loss |

## 9. 本轮明确不再追的方向

以下方向即使还能做实验，也不应作为 DCDLP 的下一篇“创新主线”：

1. generic missing-event + temporal LP；
2. generic formation head + observation/propensity head；
3. generic PU / IPW / PULL；
4. generic abstention / reject option / conformal calibration；
5. new-neighbor ingress / topological shift 的改名版本；
6. more reasonable candidate set / risk-set correction；
7. KGE multiplicity 直接迁移到 GNN；
8. local/global/feature routing 或 MoE 的重新组合；
9. degree/CN long-tail 与 hard-negative 组合；
10. graph-size OOD + 新 pair encoder；
11. temporal repeat/new 的再细分；
12. node-feature removal / heterophily 的再包装；
13. generic cross-network transfer/model selector；
14. generic edge uncertainty / calibration / explanation module；
15. 只以数据集、backbone、loss 或多模块拼接作为区别。

## 10. 可复用的投稿前 Novelty Checklist

在 N2 进入正式实验前，必须逐项回答：

- 是否把 `gradient conflict` 与已有 multi-task gradient balancing、degree bias、hard negative 和 ranking loss 文献逐项区分？
- 是否在 all-entity 或固定候选集下复现，而不是依赖随机负例？
- 是否把 pair regime 定义为预测时可用信息，而不是使用未来边？
- 是否包含 degree-matched、feature-shuffled、regime-shuffled 与 random-label controls？
- 是否报告每个 regime 的 ranking，而不只报平均 MRR/AUC？
- 是否进行了多 seed 与置信区间分析？
- 是否把“现象失败”作为预注册的停止条件？
- 是否能在不添加新 loss 的情况下证明问题价值？
- 是否仍有清晰的 graph-LP-specific estimand？
- 是否在投稿前重新查询 2026 年最新论文、引用网络和相关作者的后续工作？

## 11. 参考文献索引

- [Who Should I Engage with At What Time? A Missing Event Aware Temporal Graph Neural Network / MTGN](https://arxiv.org/pdf/2301.08399)
- [Predicting unknown viral hosts with Dynamic Positive-Unlabeled learning / DPU full preprint](https://assets-eu.researchsquare.com/files/rs-7187859/v1_covered_95e5258d-a6b6-4e28-9060-d68704b96442.pdf)
- [Predict Confidently, Predict Right: Abstention in Dynamic Graph Learning](https://arxiv.org/abs/2501.08397)
- [A Topological Perspective on Demystifying GNN-Based Link Prediction Performance](https://proceedings.iclr.cc/paper_files/paper/2024/hash/5b1b0c8d00e64a408bfcbed2a26c6718-Abstract-Conference.html)
- [Revisiting Link Prediction: A Data Perspective](https://proceedings.iclr.cc/paper_files/paper/2024/hash/154b90fcc9ba3dee96779c05c3108908-Abstract-Conference.html)
- [Mixture of Link Predictors on Graphs](https://papers.nips.cc/paper_files/paper/2024/file/1d0bcb52067128f826c86db234280dce-Paper-Conference.pdf)
- [Evaluating GNNs for Link Prediction: Current Pitfalls and New Benchmarking / HeaRT](https://proceedings.neurips.cc/paper_files/paper/2023/hash/0be50b4590f1c5fdf4c8feddd63c4f67-Abstract-Datasets_and_Benchmarks.html)
- [Back to All-Entity Ranking: Sampler-Dependent Evaluation in CTDGs](https://arxiv.org/abs/2607.27861)
- [Implicit degree bias in the link prediction task](https://proceedings.mlr.press/v267/aiyappa25a.html)
- [Attribute-Enhanced Similarity Ranking for Sparse Link Prediction / Gelato](https://arxiv.org/abs/2412.00261)
- [Predictive Multiplicity of Knowledge Graph Embeddings in Link Prediction](https://aclanthology.org/2024.findings-emnlp.19/)
- [Link Prediction or Perdition: the Seeds of Instability in KGE](https://arxiv.org/abs/2606.03365)
- [Bridging Theory and Practice in Link Representation with GNNs](https://papers.nips.cc/paper_files/paper/2025/hash/b1cd72276feff8173462e3f733ac66f8-Abstract-Conference.html)
- [On the Impact of Feature Heterophily on Link Prediction](https://arxiv.org/abs/2409.17475)
- [Improving Temporal Link Prediction via Temporal Walk Matrix Projection / TPNet](https://proceedings.neurips.cc/paper_files/paper/2024/hash/ff7bf6014f7826da531aa50f4538ee19-Abstract-Conference.html)
- [TGB-Seq](https://proceedings.iclr.cc/paper_files/paper/2025/hash/db5ca61dbc08cf5143c05ad2d1b0b2ca-Abstract-Conference.html)
- [CRAFT](https://proceedings.neurips.cc/paper_files/paper/2025/hash/036912a83bdbb1fd792baf6532f102d8-Abstract-Datasets_and_Benchmarks.html)
- [Domain matters: Towards domain-informed evaluation for link prediction](https://doi.org/10.1016/j.physa.2026.131551)
- [MetaGL: Evaluation-Free Selection of Graph Learning Models via Meta-Learning](https://arxiv.org/abs/2206.09280)
- [Stable Prediction on Graphs with Agnostic Distribution Shifts](https://proceedings.mlr.press/v218/zhang23a.html)
- [Self-Explainable Graph Neural Networks for Link Prediction](https://arxiv.org/abs/2305.12578)
- [SIG: Efficient Self-Interpretable GNN for CTDGs](https://arxiv.org/abs/2405.19062)

## 12. 最终判定

**本轮最终 Top 1：N2 — Regime-Conditional Gradient Audit for Link Prediction。**

它目前只是条件性合格，不是已经完成的新颖性证明。下一步只有一个：做一日存在性测试。如果测试显示其效应可以被 degree、negative sampling、candidate set 或 random seed 完全解释，则最终答案改为：

> **NO QUALIFIED IDEA FOUND**

如果测试显示独立且可重复的 pair-regime gradient interference，再进入正式研究计划；那时论文的第一贡献应是 failure mechanism / diagnostic estimand，第二贡献才可能是最小干预，绝不能把“加一个 loss”放在第一贡献位置。
