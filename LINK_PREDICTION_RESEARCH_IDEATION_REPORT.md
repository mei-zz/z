# Link Prediction Research Ideation Report

> 研究方向：复杂网络 / 图机器学习 / Link Prediction  
> 检索截止：2026-09-15（Asia/Shanghai）  
> 本报告性质：研究启动期的文献检索、问题发现、创新构思、碰撞审查与排序  
> 明确边界：本轮不修改 DCDLP 源码、不训练模型、不报告新的实验结果。

## 0. 先给结论

最值得优先做的方向是：

**观测过程感知的时序链路预测：把“关系没有形成”和“关系形成但没有被观测到”分开建模**  
**Observation-Process-Aware Temporal Link Prediction: Separating Relation Formation from Interaction Observability**

它不是把 degree、Common Neighbors、残差、路由或 hard negative 再组合一次，而是重新定义任务中的一个更基础的问题：在真实时序网络中，未出现的边往往不是可靠负例；边的形成风险和被记录/暴露的概率可能是两个不同过程。已有工作分别研究了 exposure bias、PU learning、部分观测网络和动态链路预测，但尚未形成一个面向公开 CTDG 链路预测基准、带可检验观测过程假设和严格风险集评估的统一问题设定。最接近的工作是 ICML 2021 的 exposure bias 方法、AAAI 2025 的 PULL，以及 2026 年关于 missingness 下 conformal link prediction 的统计工作；它们与本方向相关，但任务设定、时序风险集、模型目标和验证方式不同。[Correcting Exposure Bias for Link Recommendation](https://proceedings.mlr.press/v139/gupta21c.html)、[Accurate Link Prediction for Edge-Incomplete Graphs via PU Learning](https://ojs.aaai.org/index.php/AAAI/article/view/33966)、[Conformal network link prediction with false discovery rate control under unstructured missingness](https://doi.org/10.1080/10618600.2026.2719794)

建议的候选顺序：

1. **Exposure-Process-Aware TLP**：优先启动，创新性和问题原创性最好。
2. **Support-Conditioned Selective Link Prediction**：把 OOD 从“整体准确率下降”收窄为“哪些候选对不应被系统强行预测”，但必须避开已有动态拒答和 conformal prediction 的直接复现。
3. **Neighborhood-Ingress Mismatch Repair**：围绕“新进入的邻居改变了节点上下文组成”做时序表示错配研究，链路预测特异性强，但与 ICLR 2024 TC、CRAFT 和 TGB-Seq 有中等碰撞。
4. **Risk-Set / Eligibility-Aware TLP**：研究动态网络中候选目的地集合定义错误的问题，实验清楚，但受到 2026 年 all-entity ranking 工作的强约束。
5. **Disagreement-Calibrated Link Prediction**：把 predictive multiplicity 从 KGE 扩展到图 LP，可作为可靠性方向的备选；需证明不是普通 ensemble + calibration。

不建议优先投入：通用 hard-negative sampling、degree/CN 长尾修补、heuristic/GNN routing、generic OOD augmentation、target-link leakage correction、generic PU/static missing-edge、generic higher-order subgraph、generic dynamic repeat/unseen、generic fairness、generic metric correction。这些方向已有直接或近直接工作，或与既有 DCDLP 思路高度重叠。

---

## 1. 检索与筛选协议

### 1.1 检索范围

- 时间：2022–2026，重点核查 2024–2026；必要时回溯 2021 及更早的奠基工作。
- 主题：static LP、temporal/continuous-time LP、OOD/generalization、negative sampling、evaluation、PU/missingness、noise、heterophily、uncertainty/calibration、cross-network transfer、fairness、explainability、scalability。
- 来源优先级：NeurIPS、ICLR、ICML、KDD、WWW、WSDM、AAAI、IJCAI、PMLR、ACL/EMNLP、PNAS/Nature 系列、ACM/IEEE/Elsevier 正式页面；预印本仅用于补充最新碰撞线索。
- 数据优先级：OGB、TGB/TGB 2.0、TGB-Seq、Wikipedia、Reddit、MOOC、LastFM、UN Trade、Canadian Parliament、Cora/Citeseer/PubMed、OGBL-DDI 等公开数据。

### 1.2 查询族

本轮采用多轮、多同义词检索，而不是只搜索“link prediction improvement”：

1. `link prediction pitfalls / benchmark / evaluation / easy negatives`
2. `temporal link prediction repeated edges / unseen edges / sequence dynamics`
3. `link-level OOD / graph size generalization / topology shift`
4. `neighbor ingress / topological distribution shift / temporal neighborhood`
5. `exposure bias / missing not at random / positive unlabeled / incomplete network`
6. `negative sampling / all-entity ranking / candidate set / risk set`
7. `uncertainty / calibration / conformal / abstention / selective link prediction`
8. `heterophily / structural-feature conflict / sparse link prediction`
9. `cross-graph transfer / cross-domain temporal LP / test-time adaptation`
10. `noise / missing edges / spurious edges / fairness / explainability`

### 1.3 Gap 与碰撞判定

每个方向都拆成五层：

> problem → core hypothesis → algorithm → training/model → experiments

碰撞等级：

- **L0**：没有找到有意义的直接碰撞。
- **L1**：问题相关，但核心机制不同。
- **L2**：组件或实验相似，需要明确新增贡献才能成立。
- **L3**：核心问题和机制高度相似，不建议投入。
- **L4**：基本复现或只换 backbone，不应作为新论文。

注意：这里的等级是基于本轮公开文献检索的“初步审查”，不是投稿前的最终 exhaustive novelty claim。提交前仍需按最终题目、同义词、引用网络和作者后续工作再次检查。

### 1.4 Skill 对研究流程的约束如何落实

本报告遵循 Research Ideation skill 的标准顺序：先问题地图，再证据和 gap，再候选创新，再逐层碰撞，再做 Top 3 的 reviewer attack 和最小问题存在性测试，最后才给 Top 1。没有把单篇论文的 future work 直接当作 gap，也没有把“多加一个 loss”当作创新。

---

## 2. 第一阶段：20 个可研究问题地图

表中“可观测性”指问题能否用公开数据和可复现实验直接证伪，不代表问题已经有解决方案。

| # | 问题 | 证据与现有处理 | 剩余 Gap / 重要性 | 难度 / 可观测性 |
|---|---|---|---|---|
| P1 | **评价中的 easy negatives 与 baseline 缺失**：随机负例使模型看起来过强。 | NeurIPS 2023 系统指出基线、划分、指标和负例选择不统一，并提出 HeaRT hard-negative evaluation。[Evaluating GNNs for Link Prediction](https://proceedings.neurips.cc/paper_files/paper/2023/hash/0be50b4590f1c5fdf4c8feddd63c4f67-Abstract-Datasets_and_Benchmarks.html) | 仍缺少“训练目标、候选集合和部署目标”一致的评价协议；这是所有方法结论的地基。 | 低 / 强 |
| P2 | **动态 LP 被重复边记忆支配**：模型可能只记住已经出现过的交互。 | NeurIPS 2022 发现 EdgeBank 等记忆基线很强；TGB-Seq 进一步构造低重复、重序列动力学测试。[Towards Better Evaluation for Dynamic LP](https://proceedings.neurips.cc/paper_files/paper/2022/hash/d49042a5d49818711c401d34172f9900-Abstract-Datasets_and_Benchmarks.html)、[TGB-Seq](https://proceedings.iclr.cc/paper_files/paper/2025/hash/db5ca61dbc08cf5143c05ad2d1b0b2ca-Abstract-Conference.html) | “重复/新边”已被充分揭示；新工作必须解释更细的形成机制，而不能只再做 repeat/unseen split。 | 中 / 强 |
| P3 | **采样负例使排名结论依赖 sampler**。 | 2026 年直接工作证明非均匀负例改变 Bayes-optimal ranking，有限候选集甚至改变模型相对排序，并建议 all-entity ranking。[Back to All-Entity Ranking](https://arxiv.org/abs/2607.27861) | 通用 sampler correction 已有直接碰撞；可研究的空间转为“实际风险集/候选资格如何定义”，而非再发明负采样。 | 中 / 强 |
| P4 | **超参调优带来的 test leakage**。 | 2025 预印本、2026 Physica A 研究指出用 test set 选择超参会夸大 LP 表现，部分算法过估计超过 15%。[Impacts of Data Splitting Strategies](https://doi.org/10.1016/j.physa.2026.131545) | 问题重要但更像评价规范/实证论文；不适合作为普通模型创新。 | 低 / 强 |
| P5 | **指标之间不一致**：AUC、AP、AUPR、NDCG、MRR 对模型排序可能给出不同结论。 | 2024 研究在大量网络和算法上报告指标不一致；PNAS 工作进一步指出标准评价会激励高偏差预测器。[Inconsistency among evaluation metrics](https://pmc.ncbi.nlm.nih.gov/articles/PMC11574622/)、[Bias-aware training and evaluation](https://doi.org/10.1073/pnas.2416646122) | 已有直接实证。新增论文必须提出明确 estimand，而非“多报几个指标”。 | 低 / 强 |
| P6 | **图规模 OOD**：训练小图、测试大图时，结构节点表示可能退化到随机猜测。 | NeurIPS 2022 给出 gMPNN 的非渐近理论，并构造结构 pairwise embedding。[OOD LP Generalization Capabilities](https://papers.nips.cc/paper_files/paper/2022/hash/7f88a8478c4ae97819ccffa1e80e7a7b-Abstract-Conference.html) | 理论问题明确，但已有直接方法；不能只把“size shift”换成另一个数据增强。 | 高 / 强 |
| P7 | **链路级拓扑 OOD**：训练与测试的局部结构分布变化导致 LP 泛化差。 | 2024 工作系统讨论 link-level distribution shifts；FLEX 2025 用结构条件生成与 adversarial co-training 做 OOD LP。[Understanding Generalizability](https://arxiv.org/abs/2406.08788)、[FLEX](https://arxiv.org/abs/2507.11710) | 泛 OOD augmentation 已有强碰撞；仍可研究“何时应该拒答/如何识别 pair-level support mismatch”。 | 高 / 中强 |
| P8 | **新邻居进入造成的时序邻域组成错配**。 | ICLR 2024 的 Topological Concentration 发现新加入邻居与原有邻域互动更弱，形成 topological distribution shift；边重加权有效但有限。[A Topological Perspective](https://proceedings.iclr.cc/paper_files/paper/2024/hash/5b1b0c8d00e64a408bfcbed2a26c6718-Abstract-Conference.html) | 这是很具体的 LP 失败机制，但必须超越 TC 指标和 edge reweighting，建立 pair-level 的可检验时序修复机制。 | 中高 / 强 |
| P9 | **local/global/feature 证据在不同 edge regime 中冲突**。 | ICLR 2024 将局部结构、全局结构、feature proximity 分开分析，发现 feature-dominant edges 上 GNN4LP 可能失效。[Revisiting Link Prediction](https://proceedings.iclr.cc/paper_files/paper/2024/hash/154b90fcc9ba3dee96779c05c3108908-Abstract-Conference.html) | Mixture/routing/heuristic learning 已出现；与既有 DCDLP 的路由思路也近，不宜优先。 | 中 / 强 |
| P10 | **feature heterophily 破坏普通 GNN 的 LP 表示**。 | NeurIPS 2024 正式分析 feature heterophily 对 LP 的影响，并用 ego/neighbor separation 和 decoder 适配处理。[On the Impact of Feature Heterophily](https://arxiv.org/abs/2409.17475) | 直接论文已覆盖核心问题；除非转为跨域/动态 heterophily 机制，否则碰撞高。 | 中 / 强 |
| P11 | **pair-level common-neighbor long tail**：低 CN pair 占多数且预测较差。 | LTLP 2024 直接把它定义为 LP long-tail，并通过补边和 head-tail alignment 增强 tail pair。[Optimizing Long-tailed LP](https://arxiv.org/abs/2407.20499) | 与用户既有 CN/degree 方向直接重叠，且已有直接方法，淘汰。 | 中 / 强 |
| P12 | **未观测边不是可靠负例**：静态/生物网络常是 positive-unlabeled 或 edge-incomplete。 | AAAI 2025 PULL 将未连接 pair 视为 unlabeled，学习潜在图结构；更早工作研究 PU streaming、部分观测和 misclassification。[PULL](https://ojs.aaai.org/index.php/AAAI/article/view/33966)、[Positive-Unlabeled Learning in Streaming Networks](https://www.kdd.org/kdd2016/subtopic/view/positive-unlabeled-learning-in-streaming-networks)、[Partially Observed Networks](https://doi.org/10.1080/10618600.2017.1286243) | “静态 PU”已被覆盖；更有潜力的是时序网络中关系形成过程与曝光/记录过程的分离。 | 中高 / 中强 |
| P13 | **训练图含有 missing 与 spurious edge 的混合噪声**。 | 2023 bilateral edge noise、2016 real-network noise、2024 local smoothing 等工作分别研究鲁棒 LP。[Combating Bilateral Edge Noise](https://arxiv.org/abs/2311.01196) | 通用 robust loss 或 smoothing 容易变成旧问题的常规加法；需要先证明噪声类型本身可识别。 | 中 / 强 |
| P14 | **跨图/跨域时序迁移失败**：在未见网络上关系形成规律改变。 | MiNT 2025 提供 84 个 transaction networks，跨网络测试；DyExpert/CrossLink 和 CLIP 分别建模跨域演化或因果迁移。[MiNT](https://proceedings.neurips.cc/paper_files/paper/2025/hash/c5548168cb7324f714365a971dfe76d1-Abstract-Datasets_and_Benchmarks_Track.html)、[Enhancing Cross-domain LP](https://arxiv.org/abs/2402.02168) | generic domain adaptation 已拥挤；可收窄为“无标签时判断迁移是否安全”，即 shift detection + selective adaptation。 | 高 / 中强 |
| P15 | **时序异构图的大规模可扩展性与 edge-type 依赖**。 | TGB 2.0 覆盖 8 数据集、5 领域、最高 5300 万边；简单启发式仍有竞争力，许多方法在最大规模上失败。[TGB 2.0](https://proceedings.neurips.cc/paper_files/paper/2024/hash/fda026cf2423a01fcbcf1e1e43ee9a50-Abstract-Datasets_and_Benchmarks_Track.html) | 仅做轻量模型或加速工程不足以构成机制创新；可做 accuracy–latency–coverage 的风险集研究。 | 高 / 强 |
| P16 | **LP 概率不校准、结构异质性下 coverage 不均**。 | KDD 2024 首次做 conformalized LP；ICLR 2025 处理 dynamic GNN；UAI 2025 研究结构偏差和 heteroscedasticity。[Conformalized LP](https://arxiv.org/abs/2406.18763)、[Valid CP for Dynamic GNNs](https://proceedings.iclr.cc/paper_files/paper/2025/hash/c0ea9a95e243818f62004e73d57831ca-Abstract-Conference.html)、[Residual Reweighted CP](https://proceedings.mlr.press/v286/zhang25g.html) | generic calibration/CP 已有密集碰撞；需转向结构 support mismatch 或 decision-aware selective ranking。 | 高 / 强 |
| P17 | **预测多重性**：同等准确的模型对大量 query 给出相互冲突的排序。 | EMNLP 2024 在 KGE 中发现 8–39% test queries 存在模型冲突，投票可减少冲突。[Predictive Multiplicity of KGE](https://aclanthology.org/2024.findings-emnlp.19/) | homogeneous graph LP 上仍缺少系统验证，但简单 ensemble/投票不是充分创新。 | 中 / 中强 |
| P18 | **曝光/可见性偏差和反馈回路**。 | ICML 2021 研究 citation/friend recommendation 的 exposure bias；AAAI 2026 从 dyadic barrier 之外重新讨论 LP fairness。[Correcting Exposure Bias](https://proceedings.mlr.press/v139/gupta21c.html)、[Breaking the Dyadic Barrier](https://cs.rice.edu/~al110/pubs/aaai26.pdf) | fairness 本身已有新工作；更基础且更可泛化的问题是 observation process 与 relation process 的混杂。 | 高 / 中强 |
| P19 | **解释是否忠实到 link-level 机制**。 | Self-Explainable GNNs、LinkLogic 和 interpretable LP 分别提供解释头、规则/路径解释或稀疏可解释模型。[Self-Explainable GNNs](https://arxiv.org/abs/2305.12578)、[LinkLogic](https://arxiv.org/abs/2406.00855) | “可视化 attention”不能证明因果/机制忠实；适合作为主方向的审计维度，不适合单独做普通解释模块。 | 中 / 中强 |
| P20 | **新节点、孤立节点和低观测节点的 inductive LP**。 | 新节点动态 LP 和冷启动工作大量利用 degree/CN、属性或时序记忆。[Dynamic LP for New Nodes](https://ieeexplore.ieee.org/document/10650904)、[DGLP cold-start](https://doi.org/10.1016/j.physa.2023.128546) | 与用户既有 degree/CN 方向重叠；可作为 observation/exposure 方向的 subgroup，而非单独主线。 | 中 / 强 |

### 2.1 问题地图的筛选结论

- **最具原创问题潜力**：P12 + P18 的交集，即时序 LP 的 observation/exposure process。
- **最具可证伪性**：P8 的邻域进入错配、P16 的 support-conditioned reliability、P15 的 risk-set/scalability。
- **最容易变成旧工作的修补**：P9、P10、P11、P13、P20。
- **最容易因最新工作撞车**：P2、P3、P6、P7、P14、P16。
- **必须保留为实验底线而非创新点**：P1、P4、P5。

---

## 3. 第二阶段：8 个候选创新

评分说明：engineering / compute 为 1–5，数字越小越容易；novelty、feasibility、clarity、SCI potential 为 1–10，数字越大越好。碰撞等级是本轮检索后的初步等级。

| ID | 候选 | 核心假设与机制 | 碰撞 | 工程 / 算力 | 新颖性 | 可行性 | 清晰度 | SCI 潜力 | 判断 |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| C1 | **Exposure-Process-Aware TLP** | 观测边由 relation formation 与 exposure/recording 两个过程共同产生；双过程估计和时序风险集评估能减少把未观测当负例的错误。 | L1 | 3 / 3 | 9 | 8 | 9 | 9 | **Top 1** |
| C2 | **Risk-Set / Eligibility-Aware TLP** | 候选目的地不是固定全体节点；错误风险集会改变最优排序，显式建模 eligibility 可提高部署一致性。 | L2 | 3 / 3 | 8 | 8 | 8 | 8 | Top 4 / 需避开 2026 评价工作 |
| C3 | **Support-Conditioned Selective LP** | pair-level structural support mismatch 是错误集中区；模型应在 unsupported pairs 上输出 abstain / defer，而不是强行给分。 | L2 | 3 / 3 | 8 | 8 | 8 | 8 | **Top 2** |
| C4 | **Neighborhood-Ingress Mismatch Repair** | 新邻居的进入速度和邻域一致性改变节点表示；按 neighborhood age/ingress coherence 修复上下文比按 degree/CN 路由更接近失败机制。 | L2 | 3 / 3 | 8 | 7 | 9 | 8 | **Top 3** |
| C5 | **Disagreement-Calibrated Graph LP** | 同等准确模型在困难 pair 上的预测冲突是一种可测 epistemic uncertainty；冲突感知的候选集/选择策略比单模型 confidence 更可靠。 | L1–L2 | 3 / 3 | 7 | 8 | 7 | 8 | 备选 |
| C6 | **Safe Cross-Network TLP** | 无标签目标网络上，先估计 structural regime compatibility，再决定迁移、轻量适配或 abstain，可避免无条件 transfer。 | L2 | 4 / 4 | 7 | 6 | 8 | 8 | 备选 |
| C7 | **Missing-vs-Spurious Edge Process Separation** | missing edge 与 spurious edge 对消息传递的破坏不同；先识别噪声类型再做 LP，比统一 robust loss 更可解释。 | L2–L3 | 4 / 4 | 6 | 7 | 8 | 7 | 暂缓 |
| C8 | **Mechanism-First LP Reliability Benchmark** | 以 repeat/new、support、observation、risk-set、feature/topology conflict 为正交因素，测模型到底依赖什么机制。 | L2–L3 | 2 / 2 | 6 | 9 | 9 | 7 | 可做诊断/benchmark，不宜包装成普通新模型 |

### 3.1 明确拒绝的伪创新路线

1. **只加 hard-negative sampling**：HeaRT、TGB、DMNS、Gelato、ATNSF 等已覆盖，除非提出新的 estimand 或风险集理论。
2. **degree/CN 长尾补偿**：LTLP、PNAS bias-aware 评价、TC 以及用户既有 DCDLP 线索高度相关。
3. **GNN 与 heuristic 的路由/mixture**：Mixture of Link Predictors、HL-GNN 以及旧 DCDLP routing 已形成明显碰撞。
4. **generic OOD augmentation**：gMPNN∞、graph structure extrapolation、FLEX 已覆盖 size/topology augmentation。
5. **target-link leakage 修复**：SpotTarget 等已经针对 message-passing 中 target-link inclusion 给出直接处理。
6. **generic conformal/calibration/abstention**：KDD 2024、ICLR 2025、UAI 2025，以及 2025 动态图 reject option 已构成密集先行工作。
7. **generic higher-order/subgraph/path encoder**：HOT、higher-order temporal LP、SP4LP、TGN-SEAL 类工作足以使“再加一个 higher-order encoder”碰撞过高。
8. **generic repeat/unseen temporal model**：TGB-Seq 和 CRAFT 2025 已把核心问题和强模型推到很近。

---

## 4. 候选逐项审查

### C1. Exposure-Process-Aware Temporal Link Prediction

**中文题目**：观测过程感知的时序链路预测：分离关系形成与交互可观测性  
**English title**: *Observation-Process-Aware Temporal Link Prediction: Separating Relation Formation from Interaction Observability*

**问题。** 在 CTDG 中，常见训练方式把没有记录的 pair 当作负例，或把采样到的 non-edge 当作负例。但“关系没有形成”“关系形成但未被暴露/记录”“pair 在该时刻不属于有效风险集”可能是不同状态。若 source 活跃度、destination 可见性、时间窗口、平台记录规则和历史互动共同决定观测概率，模型可能学习到 observation shortcut，而非真正的 relation formation risk。

**现象与证据。** ICML 2021 已证明 exposure bias 可导致有偏训练、偏置评价和反馈回路；PU learning 和部分观测网络工作也明确指出未观测不等于负例。最新 2026 missingness 工作进一步表明网络边的缺失机制本身需要被建模。现有证据支持问题存在，但还没有证明它在 TGB/CTDG 基准上一定占主导，因此必须先做问题存在性测试。

**核心假设。** 对时刻 `t` 的 candidate pair，观测事件可拆为：

`P(observed interaction) = P(relation forms | history) × P(observed | relation, exposure, risk set)`。

如果 exposure/observation 概率在 pair、source、time 或 domain 间异质，那么显式估计两个过程、并按真实或模拟风险集评估，会比把所有未出现 pair 当作负例更稳健，尤其是在跨时间、跨域和人为删失压力测试下。

**最小机制。**

1. relation head：预测关系形成强度或未来 hazard。
2. observation/exposure head：只用预测时可用的 activity、eligibility、历史暴露和时间信息估计观测倾向。
3. 用 PU / inverse-propensity / partial-likelihood 中的一种明确目标连接两者；不要同时堆叠多个 debias loss。
4. 输出 formation score，不把 observation propensity 直接当作 link score。

**为什么不是简单组合。** 贡献不是“加一个 exposure feature”或“给负例加权”，而是把 link prediction 的 label-generating process 改成双过程，并要求评价目标与风险集一致。最小论文故事应当先证明单过程 PN 训练在控制删失下产生系统性偏差，再证明双过程模型能够恢复 formation risk；如果删失压力测试没有造成可重复偏差，就不应继续。

**最近的 5 篇工作与精确差异。**

1. [Correcting Exposure Bias for Link Recommendation, ICML 2021](https://proceedings.mlr.press/v139/gupta21c.html)：研究推荐/引用/好友推荐的 exposure bias，并假设或学习 exposure probability；本候选聚焦 CTDG 的 pair-time risk set、关系形成与交互记录的分解，并要求在公开 temporal LP 基准上做未来事件评价。
2. [Accurate Link Prediction for Edge-Incomplete Graphs via PU Learning, AAAI 2025](https://ojs.aaai.org/index.php/AAAI/article/view/33966)：主要是静态 edge-incomplete graph 的 PU 潜变量图恢复；本候选强调时间、暴露和观测强度，不把所有 missingness 当作同一种静态机制。
3. [Temporal Positive-Unlabeled Learning for Biomedical Hypothesis Generation, NeurIPS 2020](https://proceedings.neurips.cc/paper_files/paper/2020/file/310614fca8fb8e5491295336298c340f-Paper.pdf)：将动态生物医学关系作为 temporal PU 并估计 positive prior；本候选的新增点是 general CTDG 的 observation process / risk-set separation，而非特定 biomedical hypothesis generation。
4. [Link Prediction for Partially Observed Networks, JCGS 2017](https://doi.org/10.1080/10618600.2017.1286243)：统计上处理没有可靠 negative examples 的部分观测网络；本候选加入可观测 exposure、连续时间和现代 temporal GNN 对照，并将形成风险与记录风险分开。
5. [Conformal network link prediction with false discovery rate control under unstructured missingness, 2026](https://doi.org/10.1080/10618600.2026.2719794)：处理未知异质 missingness 下的 FDR 控制；本候选不是给静态候选边做 conformal selection，而是研究时序观测过程如何改变训练目标与 future ranking。

**碰撞等级：L1（若退化为 IPW/PU 加权则降为 L2–L3）。**

**最小实验。** 在 Wikipedia、Reddit、MOOC、LastFM 中，按时间构造 train/validation/test；建立三种观测机制：随机删失、按 source activity 删失、按 destination popularity/历史暴露删失。比较 PN、PU、IPW 和双过程版本，在同一 future-positive risk set 上报告 AP/MRR、按 exposure strata 的 recall、校准误差和跨删失强度曲线。

**预期结果。** 若问题成立，PN 模型在随机删失下差距小，但在 activity/popularity-dependent censoring 下对高暴露 pair 过度自信；双过程模型在低暴露 strata、跨时间和跨域上更稳定。

**kill criterion。** 至少 3 个数据集、3 种非均匀删失机制下，PN 与双过程的风险集排名差异均小于置信区间，或 exposure head 学不到超过常数基线的可预测信号；则放弃该方向，而不是靠调 loss 找收益。

**数据 / baseline。** TGB/TGB 2.0 的 temporal datasets、Wikipedia、Reddit、MOOC、LastFM；EdgeBank、TGN、GraphMixer、DyGFormer、CAWN、简单 activity/popularity baseline、PU/IPW baseline。

**工程与算力。** engineering 3/5；compute 3/5。优先用已有 DyGLib/TGB pipeline，仅增加一个 propensity head 和删失评估器。

**评分。** novelty 9/10；feasibility 8/10；experimental clarity 9/10；SCI potential 9/10。**推荐：Top 1。**

---

### C2. Risk-Set / Eligibility-Aware Temporal Link Prediction

**中文题目**：风险集感知的时序链路预测：从全节点排名到有效候选集合  
**English title**: *Risk-Set-Aware Temporal Link Prediction under Time-Varying Candidate Eligibility*

**问题。** 动态 LP 的“负例”不仅是采样问题，还涉及某个 pair 在时刻 `t` 是否有资格成为下一条边。把所有节点都放进候选集可能加入业务上不可能、尚未出现、已失活或不满足事件类型约束的 pair；把有限随机候选当作真实评价又会改变 Bayes-optimal ranking。

**现有处理与限制。** TGB 2.0、TGB 和 NeurIPS 2022 已改进负例构造；LinkWaldo 研究候选 pair 选择；2026 年 all-entity ranking 直接证明 sampler 和候选数量会改变模型排序。因此，通用“候选集更合理”已经不是空白。

**新增假设。** 候选 eligibility 是一个随时间和事件类型变化的可估计过程，模型应先估计 risk-set membership，再在 risk set 内预测 formation。真正的论文点必须是一个可验证的 eligibility estimand 和部署一致的评价，而不是另一个负采样器。

**为什么不是简单组合。** 需要同时报告：全 catalog、oracle eligibility、estimated eligibility 三种设定下的排序差异，并证明 eligibility 误差如何影响模型比较；仅提升 MRR 不够。

**最近的 5 篇与差异。**

1. [Back to All-Entity Ranking, 2026](https://arxiv.org/abs/2607.27861)：已直接研究 sampled-vs-all-entity ranking；本候选若只做 all-entity 已是 L4，只有转向 time-varying eligibility estimand 才可能保留。
2. [TGB 2.0, NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/hash/fda026cf2423a01fcbcf1e1e43ee9a50-Abstract-Datasets_and_Benchmarks_Track.html)：提供大规模异构 temporal benchmark 和 time-aware filtered MRR；本候选研究候选资格的生成过程及其误差。
3. [Towards Better Evaluation for Dynamic Link Prediction, NeurIPS 2022](https://proceedings.neurips.cc/paper_files/paper/2022/hash/d49042a5d49818711c401d34172f9900-Abstract-Datasets_and_Benchmarks.html)：针对 recurring edges 和 easy negatives；本候选不是 repeat hard negative，而是 risk set definition。
4. [A Hidden Challenge of Link Prediction: Which Pairs to Check?, ICDM 2021](https://arxiv.org/abs/2102.07878)：从巨大 pair search space 选择 candidate pairs；本候选要求 eligibility 与时间、事件生成过程相连，而不是静态结构候选。
5. [Are We Really Measuring Progress? ... Temporal Link Prediction, 2025](https://openreview.net/pdf?id=S6BfBrrD9L)：指出 sampled metrics、filtered candidates 和指标会误导；本候选提供可学习 risk set，但不能重复其评价批评。

**碰撞等级：L2；若不提出明确 risk-set estimand 则 L3。**

**最小实验。** 先不改模型：在 4 个 CTDG 数据集上定义 activity-based、history-based、event-type-based 三种 eligibility，测 model ranking 是否因 risk set 改变；再训练一个轻量 eligibility classifier，报告 eligibility precision/recall 与下游排名变化。

**kill criterion。** oracle eligibility 与全 catalog 的排名差异接近零，或 eligibility 无法从历史信息预测，说明该数据不适合作为主线。

**工程 / 算力：3/5 / 3/5。评分：novelty 8，feasibility 8，clarity 8，SCI 8。推荐：Top 4，但要先过碰撞审查。**

---

### C3. Support-Conditioned Selective Link Prediction

**中文题目**：结构支持条件下的选择性链路预测：对 OOD pair 安全拒答  
**English title**: *Support-Conditioned Selective Link Prediction under Structural Distribution Shift*

**问题。** 现有 OOD LP 多数目标是提升整体 test accuracy；但真实系统面对的是大量候选 pair，其中有些 pair 的局部结构在训练中没有支持。模型仍然会给这些 pair 一个看似精确的分数。真正可部署的问题不是“所有 pair 都预测得更好”，而是“在固定覆盖率下，模型能否识别哪些 pair 的 ranking risk 已不可接受”。

**核心假设。** pair-level support mismatch（例如局部结构、时间邻域年龄、结构模式与训练支持的距离）比全图 OOD 标志更能预测错误。把 support score 用于 selective risk / abstention，并按 support strata 做 coverage 评估，会比单一 confidence threshold 更有效。

**机制。** 只选择一个可解释的 support representation；训练一个 selector 或 conformal-like nonconformity head；输出预测、abstain 或 defer。不能把多个结构指标拼成黑盒 uncertainty。

**为什么不是简单 calibration。** 目标不是全局 probability calibration，也不是仅仅降低 coverage 后 AUC 变高；需要证明 conditional risk-coverage、OOD subgroup coverage 和 downstream top-k precision 同时改善，并在 unseen structural regime 下验证。

**最近的 5 篇与差异。**

1. [Conformalized Link Prediction on GNNs, KDD 2024](https://arxiv.org/abs/2406.18763)：提供 distribution-free link prediction prediction sets；本候选关注 structural support-conditioned selective ranking，而不是全局 marginal coverage。
2. [Valid Conformal Prediction for Dynamic GNNs, ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/c0ea9a95e243818f62004e73d57831ca-Abstract-Conference.html)：处理动态图的 conformal validity；本候选的核心是识别 unsupported pair 并进行决策选择，不能只套其校准流程。
3. [Predict Confidently, Predict Right: Abstention in Dynamic Graph Learning, 2025](https://arxiv.org/abs/2501.08397)：直接把 reject option 接入 CTDG，并用 coverage-based abstention 提升 AUC/AP；这是最强碰撞，通用动态 abstention 应判 L3。本候选必须加入 structural-support conditional risk 与 OOD test protocol 才有区分度。
4. [Understanding the Generalizability of Link Predictors Under Distribution Shifts on Graphs, 2024](https://arxiv.org/abs/2406.08788)：分析 link-level structural shifts 和泛化下降；本候选输出 selective decision，而不是泛 OOD accuracy 方法。
5. [Subgraph Generation for Generalizing on Out-of-Distribution Links, 2025](https://arxiv.org/abs/2507.11710)：用 FLEX 生成结构条件子图和 adversarial co-training；本候选不生成数据、不做泛 OOD augmentation，而是对不支持的 pair 拒答。

**碰撞等级：L2；若只是 confidence threshold 则 L3。**

**最小实验。** 训练普通 TGN/GraphSAGE 作为固定 scorer，在结构 support 随时间或按 graph regime 改变的测试集上，比较 max-score、ensemble variance、global conformal、support-conditioned selector。核心图是 risk-coverage、conditional coverage、top-k precision vs coverage，而非只报 AUC。

**预期结果。** support-conditioned selector 在结构 OOD 和低 support strata 中能集中捕获错误；若只能通过拒答 40–50% 才改善，或比普通 confidence 无优势，则不成立。

**kill criterion。** support score 与错误/校准误差在至少 3 个数据集上相关性不稳定，或 support selector 不优于 score margin / ensemble baseline。

**工程 / 算力：3/5 / 3/5。评分：novelty 8，feasibility 8，clarity 8，SCI 8。推荐：Top 2，但必须把“support-conditioned”写进问题定义。**

---

### C4. Neighborhood-Ingress Mismatch Repair

**中文题目**：时序邻域进入错配下的链路预测表示修复  
**English title**: *Repairing Temporal Neighborhood-Ingress Mismatch for Link Prediction*

**问题。** 节点的历史表示由旧邻居集合构成；未来时刻新进入的邻居可能与旧邻域的互动方式不同，导致 message passing 学到的上下文在 test 时失配。这比“低 degree 节点难”更具体，也不等同于 CN 数量。

**核心假设。** 未来边的难度由 neighborhood ingress rate、new-neighbor age、new-old neighbor coherence 共同决定；一个按邻域进入过程构造的 pair context 能比静态邻居聚合更好地保留未来边形成信号。

**机制候选。** 用历史窗口构造 old/new neighbor 分层；增加一个 ingress coherence estimator；在训练时用时间切分模拟未来邻居进入，学习对 context freshness 的稳定表示。不要使用 degree/CN 路由，不要直接复制 TC edge reweighting。

**为什么不是简单 temporal feature。** 贡献必须是“发现并验证表示错配机制”，而不是给 TGN 加 timestamp。必须有 factorial ablation：old-only、new-only、mixed、coherence-shuffled，并检验 repair 是否只对高-ingress pair 有效。

**最近的 5 篇与差异。**

1. [A Topological Perspective on Demystifying GNN-Based LP, ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/5b1b0c8d00e64a408bfcbed2a26c6718-Abstract-Conference.html)：已发现 newly joined neighbors 的 topological distribution shift，并尝试 TC edge reweighting；本候选必须改为 pair-level temporal ingress mismatch，并证明不是重做 TC。
2. [Future Link Prediction Without Memory or Aggregation, CRAFT, NeurIPS 2025](https://proceedings.neurips.cc/paper_files/paper/2025/hash/036912a83bdbb1fd792baf6532f102d8-Abstract-Conference.html)：用 node IDs 和 target-aware cross-attention 处理 recurring/novel interactions；本候选研究 neighborhood composition failure mechanism，而不是替换 memory/aggregation。
3. [TGB-Seq Benchmark, ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/db5ca61dbc08cf5143c05ad2d1b0b2ca-Abstract-Conference.html)：强调复杂序列、低重复和 unseen dynamics；本候选关注邻域进入组成，并用机制分层而非仅换 benchmark。
4. [FakeEdge, LoG 2022](https://proceedings.mlr.press/v198/dong22a.html)：通过添加/删除 focal edges 减轻 LP dataset shift；本候选不做泛 edge augmentation，而是估计真实 temporal neighborhood ingress。
5. [DTGB, NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/hash/a65d054a407f94c34ecfb598fb540a0d-Abstract-Datasets_and_Benchmarks_Track.html)：指出结构和文本动态、长程语义与可扩展性局限；本候选不依赖文本，专注结构进入错配。

**碰撞等级：L2。** 若采用“邻居年龄加权”而没有新机制，则 L3。

**最小实验。** 在时间窗口上计算每个 source 的 old/new neighbor 比例、new-old coherence，并按四分位数报告 TGN、GraphMixer、DyGFormer 和候选修复模型的 AP/MRR。首先只做诊断，不训练新模型。

**kill criterion。** ingress 指标与错误无关，或 TC/recency baseline 已完全解释现象；则不做模型。

**工程 / 算力：3/5 / 3/5。评分：novelty 8，feasibility 7，clarity 9，SCI 8。推荐：Top 3。**

---

### C5. Disagreement-Calibrated Graph Link Prediction

**中文题目**：模型分歧校准的链路预测：从单模型置信度到多模型冲突  
**English title**: *Disagreement-Calibrated Link Prediction under Predictive Multiplicity*

**问题。** 不同模型可能有相近平均分，但在具体 pair 上给出冲突排序。单模型 score margin 或全局 calibration 无法区分“模型都确信”和“模型意见分裂”。

**核心假设。** model disagreement 是一种可测的 epistemic signal，且在结构 OOD、low support 和 observation ambiguity pair 上更高；基于 disagreement 的 selective ranking 或 candidate set 比单模型 confidence 更安全。

**为什么不是 ensemble。** 不能只平均 3 个模型。需研究 multiplicity 的 subgroup 分布、冲突与真实错误的关系、模型相关性，以及在相同计算预算下 disagreement 是否提供额外信息。算法可先用廉价异质 scorer，再做 conflict-aware selector。

**最近的 5 篇与差异。**

1. [Predictive Multiplicity of KGE in Link Prediction, Findings EMNLP 2024](https://aclanthology.org/2024.findings-emnlp.19/)：在 KGE 上量化同等性能模型的预测冲突；本候选扩展到 homogeneous graph GNN/heuristic 混合模型，并关联结构 support/OOD subgroup。
2. [Conformalized Link Prediction on GNNs, KDD 2024](https://arxiv.org/abs/2406.18763)：用 conformal 生成 prediction sets；本候选以 model disagreement 作为 uncertainty source，不直接复现 CP。
3. [Valid Conformal Prediction for Dynamic GNNs, ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/c0ea9a95e243818f62004e73d57831ca-Abstract-Conference.html)：dynamic validity；本候选研究模型冲突机制和选择性排序。
4. [Residual Reweighted Conformal Prediction for GNNs, UAI 2025](https://proceedings.mlr.press/v286/zhang25g.html)：处理 structural bias 和 heteroscedasticity；本候选不做 residual reweighting，而是显式测 multiplicity。
5. [KGE Calibrator, EMNLP 2025](https://aclanthology.org/2025.emnlp-main.1522/)：针对 KGE score calibration；本候选的对象是 cross-model disagreement，而非单一 KGE score。

**碰撞等级：L1–L2。**

**最小实验。** 固定同一 train/test protocol，训练 TGN、GraphMixer、simple heuristic、SEAL/GraphSAGE 四类 scorer；计算 per-pair variance、rank disagreement、consensus top-k，并按 disagreement 分层测 error concentration 和 risk-coverage。

**kill criterion。** disagreement 与错误无关，或简单 max-margin / ensemble variance 已完全等效且没有额外决策价值。

**工程 / 算力：3/5 / 3/5。评分：novelty 7，feasibility 8，clarity 7，SCI 8。推荐：备选。**

---

### C6. Safe Cross-Network Temporal Link Prediction

**中文题目**：安全跨网络时序链路预测：无标签目标域的迁移适配与拒答  
**English title**: *Safe Cross-Network Temporal Link Prediction with Shift Detection and Selective Adaptation*

**问题。** 跨 network transfer 中，目标图没有标签或只有很少标签；无条件复用 source 模型可能把 source-specific formation rule 当成通用规律。

**核心假设。** 目标网络的 structural regime compatibility 可以从无标签历史中估计；只有在 compatibility 足够高时迁移/适配，否则应 abstain 或退回简单 baseline。

**为什么不是普通 domain adaptation。** 论文必须把“何时不迁移”作为一等输出，采用 leave-one-network-out 和 target-label-free selection；不能只在目标域调参后报收益。

**最近的 5 篇与差异。**

1. [MiNT, NeurIPS 2025](https://proceedings.neurips.cc/paper_files/paper/2025/hash/c5548168cb7324f714365a971dfe76d1-Abstract-Datasets_and_Benchmarks_Track.html)：提供 84 个 temporal transaction networks 和跨网络 transfer benchmark；本候选研究无标签安全决策，不只是 benchmark。
2. [Enhancing Cross-domain Link Prediction via Evolution Process Modeling, WWW 2025](https://arxiv.org/abs/2402.02168)：用 DyExpert/CrossLink 建模跨域演化；本候选先做 compatibility detection 和 selective adaptation。
3. [Inductive Link Prediction on Temporal Networks through Causal Inference, Information Sciences 2024](https://doi.org/10.1016/j.ins.2024.121202)：用因果推断增强跨网络泛化；本候选的区别在于无标签目标域风险控制。
4. [DyFiLM, Neural Networks 2026](https://doi.org/10.1016/j.neunet.2025.108006)：处理 dynamic graph distribution shift，用 hypernetwork 适配；本候选强调迁移是否安全，而非固定适配器。
5. [TGB 2.0, NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/hash/fda026cf2423a01fcbcf1e1e43ee9a50-Abstract-Datasets_and_Benchmarks_Track.html)：提供多领域 temporal/heterogeneous benchmark；本候选利用其做 leave-one-domain/network-out。

**碰撞等级：L2。**

**最小实验。** 只用 target train prefix 的无标签统计，预测 source-to-target performance drop；对比 source-only、unsupervised normalization、target adaptation 和 safe selector。

**kill criterion。** source compatibility 指标不能预测 transfer gain/loss，或目标域必须用标签调参才能获得收益。

**工程 / 算力：4/5 / 4/5。评分：novelty 7，feasibility 6，clarity 8，SCI 8。推荐：备选，不如 C1。**

---

### C7. Missing-vs-Spurious Edge Process Separation

**中文题目**：缺失边与伪边的过程分离下的鲁棒链路预测  
**English title**: *Separating Missing and Spurious Edge Processes for Robust Link Prediction*

**问题。** missing edge 使真实邻域信息缺失，spurious edge 则注入错误消息；两者对 GNN 的影响方向相反，但多数 robust LP 方法用统一 noise assumption。

**核心假设。** 利用时间、重复性、局部一致性和观测强度，可以估计 edge noise type；先分离再修复比统一 smoothing/robust loss 更可靠。

**最近的 5 篇与差异。**

1. [Accurate LP for Edge-Incomplete Graphs via PU Learning, AAAI 2025](https://ojs.aaai.org/index.php/AAAI/article/view/33966)：重点是 missing/unlabeled；本候选加入 spurious process separation。
2. [Combating Bilateral Edge Noise for Robust LP, 2023](https://arxiv.org/abs/2311.01196)：已明确研究 bilateral edge noise；本候选若只换 robust objective，属于 L3。
3. [Measuring Robustness of LP Algorithms under Noisy Environment, 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4702065/)：系统比较 missing/fake/swapped noise；本候选要提出可识别的 noise process，而非再做 robustness curve。
4. [Local Graph Smoothing for LP against Universal Attack, 2024](https://doi.org/10.1016/j.cose.2024.103935)：用 smoothing 抗攻击；本候选不把攻击噪声等同于自然 missingness。
5. [Link Predictions for Incomplete Network Data with Outcome Misclassification, 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8059251/)：统计建模 latent links；本候选处理动态消息传递和两类噪声。

**碰撞等级：L2–L3。**

**最小实验。** 先在公开静态/时序图上注入可控 missing/spurious 混合噪声，测已有 edge anomaly indicators 是否能识别噪声类型；若不能识别，不进入模型阶段。

**kill criterion。** noise type classifier 接近随机，或统一 robust baseline 在所有噪声强度下已无显著差异。

**工程 / 算力：4/5 / 4/5。评分：novelty 6，feasibility 7，clarity 8，SCI 7。推荐：暂缓。**

---

### C8. Mechanism-First Link Prediction Reliability Benchmark

**中文题目**：机制优先的链路预测可靠性基准：从整体分数到失败机制  
**English title**: *A Mechanism-First Reliability Benchmark for Link Prediction*

**问题。** LP 论文通常只改变平均 AUC/AP，却不回答模型依赖的是 repeat memory、局部结构、feature similarity、可观测性还是 sampler artifact。这样会使“有效”与“为什么有效”混在一起。

**核心假设。** 将 repeat/new、support、observation、risk-set、heterophily 和 feature/topology conflict 做成正交或半正交实验因素，能比传统 ablation 更稳定地预测模型跨数据集表现。

**最近的 5 篇与差异。**

1. [Evaluating GNNs for LP: Current Pitfalls and New Benchmarking, NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/hash/0be50b4590f1c5fdf4c8feddd63c4f67-Abstract-Datasets_and_Benchmarks.html)：强调统一 benchmark 和 hard negatives；本候选增加机制正交性、failure attribution 和 reliability outcome。
2. [Inconsistency among Evaluation Metrics in LP, 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11574622/)：研究 metric disagreement；本候选研究机制因素导致的 model ranking/claim 改变。
3. [Bias-aware Training and Evaluation of LP Algorithms in Network Biology, 2025](https://doi.org/10.1073/pnas.2416646122)：揭示评价会奖励高偏差方法；本候选扩展到多个 failure mechanisms，但不能只重复 degree bias。
4. [Understanding Generalizability of Link Predictors under Distribution Shifts, 2024](https://arxiv.org/abs/2406.08788)：研究 link-level OOD generalization；本候选将 OOD 与具体 support/observation/risk-set 因素交叉。
5. [Domain matters: Towards domain-informed evaluation for LP, 2026](https://doi.org/10.1016/j.physa.2026.131551)：740 个网络、7 个领域显示跨域算法排名相关性很低；本候选关注机制分解而非只增加网络数。

**碰撞等级：L2–L3。** 与用户已有 interaction audit / controlled intervention 方向也可能重叠，因此不应作为 Top 1 模型论文。

**最小实验。** 先只实现 2×2 或 3×2 factorial evaluation：repeat/new × seen/unseen support；再加入 observation thinning。输出 effect size、interaction effect 和 model ranking stability。

**kill criterion。** 因素之间高度共线，无法解释独立机制，或结果只重复已发表 benchmark。

**工程 / 算力：2/5 / 2/5。评分：novelty 6，feasibility 9，clarity 9，SCI 7。推荐：可作为 C1/C3 的评价章节，不单独主投。**

---

## 5. Top 5 排名与选择理由

| 排名 | 方向 | 为什么排在这里 | 最大风险 | 第一关 |
|---|---|---|---|---|
| 1 | Exposure-Process-Aware TLP | 重新定义 label/observation process；与旧 degree/CN 主线最远；有 temporal PU、exposure bias、missingness 三条证据链；可用公开数据做删失压力测试。 | 公开 CTDG 没有真实 exposure label，存在可识别性风险。 | 先验证非均匀观测删失是否真的改变模型结论。 |
| 2 | Support-Conditioned Selective LP | 把 OOD 从泛 accuracy 收窄为 pair-level safe decision；实验指标清晰。 | 2025 dynamic abstention + 2024/25 conformal 工作碰撞强。 | 证明 support selector 超过普通 confidence，并非降 coverage 获益。 |
| 3 | Neighborhood-Ingress Mismatch | 有 ICLR 2024 的直接现象证据，LP-specific，机制图容易讲清。 | TC、CRAFT、TGB-Seq、recent temporal neighbor methods 形成中等碰撞。 | 验证 ingress 指标能独立解释错误，而非 degree/CN/recency 替代物。 |
| 4 | Risk-Set / Eligibility-Aware TLP | 问题很实际，评价清楚，和 all-entity ranking 可形成延伸。 | 2026 sampler-dependent evaluation 已非常接近。 | 明确定义 eligibility estimand，避免变成重新包装的 negative sampling。 |
| 5 | Disagreement-Calibrated LP | KGE multiplicity 迁移到 graph LP 有空间，计算可控。 | 简单 ensemble/variance/calibration 很容易被审稿人认为不新。 | 证明 disagreement 对 graph LP 有独立决策价值。 |

---

## 6. Top 3 第二轮深度碰撞审查

### 6.1 Top 1：Exposure-Process-Aware TLP

**同义词与检索簇。** exposure bias、observability、visibility、MNAR、missing-not-at-random、PU link prediction、edge-incomplete、censoring、propensity、risk set、event logging、relation formation、interaction hazard、selection bias。

**邻近机制。** inverse propensity weighting、PU risk estimation、latent-edge model、point-process link formation、survival/competing risk、ecological detection model、recommender exposure model。

**跨领域碰撞。**

- 推荐/引用：ICML 2021 已有 exposure correction，但依赖 exposure probability 或半合成 exposure。
- 生物医学：temporal PU 已把 future connectivity 视为 PU，但任务和机制偏 biomedical hypothesis generation。
- 网络统计：部分观测网络和 outcome misclassification 已建 latent links，但不面向现代 CTDG benchmark。
- 生态学：2026 interaction prediction 已明确区分 interaction、detection、occurrence submodels，说明“双过程”思想并非完全新；本方向必须承认这是跨领域先例，创新点应放在 CTDG link prediction 的风险集和可复现实验协议，不宣称首次提出 observation model。

**2025–2026 最新检查。** AAAI 2025 PULL 覆盖 static edge-incomplete PU；2026 conformal FDR work 覆盖 unstructured missingness；2026 all-entity work提示 risk set 定义影响评价。尚未检索到把这些因素统一为“CTDG formation vs observation”并在公开 temporal GNN benchmark 上做分层 ranking 的直接同题工作。

**作者后续与引用风险。** 需要在正式投稿前追踪 Gupta、PULL 作者、TGB/DyG 评价作者在 2025–2026 的新论文；尤其检查是否出现“observation-aware temporal LP”“exposure-aware dynamic graph learning”等不同标题。

**最终碰撞判断：L1。** 但以下版本自动降级：

- 只加 exposure feature：L3。
- 只做 IPW：L2–L3。
- 只把 unobserved 当 PU：L2。
- 只在合成数据中删边：L2。
- 不定义 formation risk 与 observed event risk 的区别：L3。

**七个 Reviewer Attack 与应对。**

1. **“你没有真实 exposure label，问题不可识别。”**  
   应对：不声称识别真实因果 exposure；先定义可观测的 observation proxy 和 controlled censoring estimand，明确结论边界。若只有合成 exposure 才有结果，论文定位为 stress-test/protocol，不宣称真实世界 debiasing。
2. **“这就是 ICML 2021 exposure bias 的图版本。”**  
   应对：逐项对照：CTDG pair-time risk set、future event ranking、temporal GNN memory、non-edge sampling、formation-vs-observation decomposition；把 ICML 2021 作为最接近工作而非回避。
3. **“你只是在做 PU/IPW。”**  
   应对：设置 PN、PU、IPW、双过程四类基线；核心贡献是 label-generating process + risk-set evaluation，不是增加一个 loss。
4. **“删失机制是你自己造的，不代表真实网络。”**  
   应对：使用三类机制：随机、activity-dependent、history/popularity-dependent；同时报告自然 temporal split。若自然 split 没有差异，诚实地只保留受控 stress-test 结论。
5. **“双过程模型复杂，收益可能来自更多参数。”**  
   应对：等参数 relation-only baseline、共享 encoder、去掉 exposure head、固定计算预算；报告参数量和 wall-clock。
6. **“评价仍然依赖负采样。”**  
   应对：对可枚举 catalog 做 all-entity 或大 risk-set evaluation；不能只沿用 random-1 AUC。
7. **“跨数据集不稳定。”**  
   应对：预注册至少 3 个数据集和删失机制；按 source activity、destination activity、history exposure 分层，接受结果只在某些网络成立。

**1–3 小时问题存在性测试。**

1. 选 Wikipedia、Reddit、MOOC、LastFM 中至少 3 个可快速读取的数据。
2. 对每个未来正事件构造相同时间窗的 candidate risk set，计算 source activity、destination activity、pair history、time gap 等预测时可用 proxy。
3. 对训练观测做 0%、20%、40%、60% 的随机和 activity-dependent thinning；保持 test future positives 不变。
4. 用 EdgeBank/activity/popularity 和现成 TGN/GraphMixer 输出，比较：模型相对排序、AP/MRR、分层 calibration、top-k overlap。
5. 如果 activity-dependent thinning 比随机 thinning 明显改变结论，且变化随模型不同而不同，问题成立；否则停止。

### 6.2 Top 2：Support-Conditioned Selective LP

**同义词与检索簇。** selective link prediction、abstention、reject option、risk-coverage、conditional coverage、pair-level OOD、support mismatch、unknown pair、uncertainty under graph shift、conformal graph LP。

**直接碰撞。** 2025 [Predict Confidently, Predict Right](https://arxiv.org/abs/2501.08397) 已把 reject option 接入 CTDG，并随 coverage 降低报告 AUC/AP 上升；KDD 2024 与 ICLR 2025 已覆盖 conformal LP/dynamic validity。因此 generic abstention 不能做。

**可能保留的 L2 版本。** selector 的输入不是普通 score margin，而是 pair-level structural support；评估的主指标不是“拒答后 AUC 变高”，而是 support strata 的 conditional risk、coverage 和 OOD top-k precision。还要包含动态拒答论文的 selector 作为强 baseline。

**跨域碰撞。** selective classification、OOD abstention、conformal prediction 已很成熟；本方向的可辩护点只能是 link-specific support and ranking decision，不应声称首次做 selective prediction。

**七个 Reviewer Attack 与应对。**

1. 你只是把置信度换成结构特征：做 feature-only、score-only、ensemble、global conformal 和 support-conditioned 的严格对照。
2. 拒答越多性能越高是数学常识：固定 coverage，报告 risk-coverage AURC、error capture rate 和 deployment utility。
3. 已有 2025 dynamic abstention：把它作为直接 baseline，并证明其 global selector 在 structural OOD 中 conditional coverage 失效。
4. support 指标是 degree/CN 的改名：剔除 degree/CN，采用训练分布密度、局部模式频率、时间邻域 support；做 partial correlation 和 shuffled control。
5. conformal coverage 不能在 graph dependence 下保证：只宣称 empirical conditional reliability，或给出明确 exchangeability/stationarity 条件。
6. 选择器可能泄漏 test structure：support 只由预测时可用 prefix 计算，不读取 target edge 或未来邻居。
7. 真实系统不能拒答太多：报告 coverage 90/80/70% 的固定 operating points，并明确 defer-to-human/heuristic 的 downstream policy。

**1–3 小时问题存在性测试。** 固定一个现成 TGN scorer；构造按结构 regime、时间窗口、local support 分层的 test bins；比较错误率、置信度和 support 的排序相关性。若 support 不能比 score margin 更早或更稳定地定位错误，不做 selector。

### 6.3 Top 3：Neighborhood-Ingress Mismatch Repair

**同义词与检索簇。** newly joined neighbors、neighbor ingress、neighborhood freshness、temporal neighborhood shift、neighbor arrival、topological distribution shift、context drift、message-passing mismatch。

**直接碰撞。** ICLR 2024 TC 是核心邻近工作；CRAFT 2025 已针对 recurring/novel interactions 设计 target-aware cross-attention；TGB-Seq 2025 已强调序列动态；2026 KDD 的 position-aware neighbor aggregation 也需要检查是否覆盖类似机制。因此该方向可做，但 novelty margin 小于 C1。

**可能保留的 L2 版本。** 先提出可证伪的 pair-level quantity：`ingress rate × new-old neighbor coherence × context age gap`；证明它独立于 degree/CN/recency；再设计最小 repair，而不是大模型。

**七个 Reviewer Attack 与应对。**

1. 这是 TC 的重新命名：逐公式区分 node-level TC 与 pair-level temporal ingress/coherence。
2. 这是 CRAFT 已解决的 novel interaction：对照 CRAFT，证明 CRAFT 的总体增益不等于解释 ingress mechanism。
3. 只是 temporal attention：使用 shuffled ingress、old/new swap、coherence destruction 反事实控制。
4. 指标依赖未来邻居：严格按时间 prefix 计算，未来只用于标签和事后诊断。
5. 只在一个数据集有效：至少用社会、通信、交易三类网络，报告 interaction effect。
6. 额外分层使模型更复杂：先做 frozen-diagnostic，再做参数匹配的小修复模块。
7. 收益很小：若机制解释强但平均收益小，定位为 failure-mechanism paper；若连 subgroup 也不稳定则放弃。

**1–3 小时问题存在性测试。** 在 3 个 temporal datasets 上按时间构造 old/new neighbor；计算 ingress/coherence，与 per-node/per-pair error 和 degree/CN/recency 做比较。若 partial correlation 和 subgroup effect 不稳定，不训练模型。

---

## 7. 最终 Top 1 研究卡

### 7.1 题目

**观测过程感知的时序链路预测：分离关系形成与交互可观测性**  
*Observation-Process-Aware Temporal Link Prediction: Separating Relation Formation from Interaction Observability*

### 7.2 一句话问题

现有 temporal LP 往往把未记录的 pair 当负例，但在 activity-dependent、history-dependent 或平台记录机制下，未记录可能代表“未形成”“未暴露”或“不在有效风险集”；模型因此可能优化 observation probability，而不是 relation formation probability。

### 7.3 核心假设

**H1：** 非均匀 observation/censoring 会改变不同 LP 模型的 ranking、calibration 和 subgroup error，而不仅仅是整体分数。  
**H2：** formation-only score 与 observation-aware score 的差异在低暴露、低 activity、少 history 和跨时间/跨域场景中最大。  
**H3：** 一个参数受控的双过程模型，在自然 temporal split 和受控非均匀删失下，比 PN、PU、IPW 和 observation-blind temporal GNN 更稳健。

### 7.4 最接近论文与精确差异

最接近的是 [Correcting Exposure Bias for Link Recommendation, ICML 2021](https://proceedings.mlr.press/v139/gupta21c.html)。它已经证明 exposure bias 会造成有偏 link recommendation 和 feedback loop，因此本方向不能宣称 exposure bias 是全新概念。

精确差异应写成：

1. 从 recommendation/citation exposure 转向公开 CTDG 的 pair-time future link prediction。
2. 从已知或半合成 exposure probability 转向预测时可用的 temporal risk-set / activity proxy，并明确可识别性边界。
3. 从单一 correction estimator 转向 formation process 与 observation process 的分解实验。
4. 从只看平均 accuracy 转向 future ranking、分层 calibration、删失敏感性和跨域稳定性。

若以上四点做不到，不能把它称为新方向，应退回 C3 或放弃。

### 7.5 最先做什么

先做问题存在性测试，不先设计复杂网络：

1. 选 3–4 个公开 temporal interaction datasets。
2. 只用历史 prefix，计算 activity、history、time gap、candidate eligibility proxy。
3. 注入随机与非均匀 observation thinning。
4. 用 EdgeBank、activity/popularity、TGN/GraphMixer 评估相对排序与分层风险。
5. 只有在结果显示 observation mechanism 会系统改变结论时，才实现双过程模型。

### 7.6 放弃标准

满足任一项就停止：

- 3 个以上数据集上非均匀删失对模型排序和分层误差都没有超过不确定性范围。
- observation proxy 不能从历史 prefix 预测观测事件，且只能靠不可用的未来/外部信息。
- 双过程模型不优于等参数 PN、PU、IPW 和简单 activity baseline。
- 主要收益只能在随机删失或人工标签设定下出现，换成自然 temporal split 即消失。
- 与 2025–2026 新论文发现直接同题同机制，无法给出清晰差异。

### 7.7 预期论文故事

1. 现有 temporal LP 的一个隐含假设：未观测 pair 可当作负例。
2. 该假设在非均匀观测过程中造成模型、指标和 subgroup 结论偏差。
3. 通过 controlled observation process 与自然 temporal data 证明问题存在。
4. 提出最小双过程模型，并与 PN/PU/IPW/temporal GNN 强基线比较。
5. 给出何时 correction 有效、何时不可识别的边界，而不是只报告平均提升。

---

## 8. 研究执行建议

### 第 0 阶段：半天问题验证

- 完成 C1 的删失压力测试。
- 同时完成 C3/C4 的诊断统计，作为备选。
- 不训练新模型，不做超参搜索，不看 test label 调参。

### 第 1 阶段：1–2 天最小基线

- 固定数据划分、risk set、负例和指标。
- 复现 EdgeBank、activity/popularity、TGN/GraphMixer。
- 记录 all-entity 或尽可能完整 risk-set 的结果，以及 sampler-dependent 结果。

### 第 2 阶段：只实现一个机制

- C1 只选一种 observation proxy 和一种 correction objective。
- 不同时加入 degree/CN、hard negatives、mixture、disentanglement 或复杂 causal module。
- 先做等参数和等计算预算比较。

### 第 3 阶段：论文级审查

- 重新检索最终题目的同义词和 arXiv 2025–2026。
- 追踪最近论文作者的后续工作和引用网络。
- 做自然 temporal split、controlled censoring、cross-domain、subgroup、seed 和 confidence interval。
- 若贡献仅是“平均 AUC 提升”，退回；必须有 problem evidence、mechanism evidence 和 boundary/kill result。

---

## 9. 关键参考文献索引

- [Evaluating Graph Neural Networks for Link Prediction: Current Pitfalls and New Benchmarking, NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/hash/0be50b4590f1c5fdf4c8feddd63c4f67-Abstract-Datasets_and_Benchmarks.html)
- [Towards Better Evaluation for Dynamic Link Prediction, NeurIPS 2022](https://proceedings.neurips.cc/paper_files/paper/2022/hash/d49042a5d49818711c401d34172f9900-Abstract-Datasets_and_Benchmarks.html)
- [TGB 2.0, NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/hash/fda026cf2423a01fcbcf1e1e43ee9a50-Abstract-Datasets_and_Benchmarks_Track.html)
- [TGB-Seq, ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/db5ca61dbc08cf5143c05ad2d1b0b2ca-Abstract-Conference.html)
- [CRAFT, NeurIPS 2025](https://proceedings.neurips.cc/paper_files/paper/2025/hash/036912a83bdbb1fd792baf6532f102d8-Abstract-Conference.html)
- [OOD Link Prediction Generalization Capabilities of gMPNNs, NeurIPS 2022](https://papers.nips.cc/paper_files/paper/2022/hash/7f88a8478c4ae97819ccffa1e80e7a7b-Abstract-Conference.html)
- [Understanding the Generalizability of Link Predictors under Distribution Shifts, 2024](https://arxiv.org/abs/2406.08788)
- [Subgraph Generation for Generalizing on Out-of-Distribution Links, 2025](https://arxiv.org/abs/2507.11710)
- [A Topological Perspective on Demystifying GNN-Based Link Prediction Performance, ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/5b1b0c8d00e64a408bfcbed2a26c6718-Abstract-Conference.html)
- [Revisiting Link Prediction: A Data Perspective, ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/154b90fcc9ba3dee96779c05c3108908-Abstract-Conference.html)
- [On the Impact of Feature Heterophily on Link Prediction, NeurIPS 2024](https://arxiv.org/abs/2409.17475)
- [Optimizing Long-tailed Link Prediction, 2024](https://arxiv.org/abs/2407.20499)
- [Accurate Link Prediction for Edge-Incomplete Graphs via PU Learning, AAAI 2025](https://ojs.aaai.org/index.php/AAAI/article/view/33966)
- [Correcting Exposure Bias for Link Recommendation, ICML 2021](https://proceedings.mlr.press/v139/gupta21c.html)
- [Conformalized Link Prediction on GNNs, KDD 2024](https://arxiv.org/abs/2406.18763)
- [Valid Conformal Prediction for Dynamic GNNs, ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/c0ea9a95e243818f62004e73d57831ca-Abstract-Conference.html)
- [Predict Confidently, Predict Right: Abstention in Dynamic Graph Learning, 2025](https://arxiv.org/abs/2501.08397)
- [Predictive Multiplicity of KGE in Link Prediction, Findings EMNLP 2024](https://aclanthology.org/2024.findings-emnlp.19/)
- [MiNT, NeurIPS 2025](https://proceedings.neurips.cc/paper_files/paper/2025/hash/c5548168cb7324f714365a971dfe76d1-Abstract-Datasets_and_Benchmarks_Track.html)
- [Back to All-Entity Ranking, 2026](https://arxiv.org/abs/2607.27861)
- [Impacts of Data Splitting Strategies, Physica A 2026](https://doi.org/10.1016/j.physa.2026.131545)
- [Domain matters: Towards domain-informed evaluation for LP, Physica A 2026](https://doi.org/10.1016/j.physa.2026.131551)

---

## 10. 最终判断

如果目标是尽快形成一篇问题清楚、可验证、计算可控、且不依赖 DCDLP 旧组件的 SCI Q2/Q3 候选论文，建议只沿 C1 推进到“问题存在性测试”这一步。C1 的价值不在于承诺一定提升多少 AUC，而在于它能给出一个可被证伪的基础命题：**temporal link prediction 的观测机制是否在改变我们以为测到的 link formation 能力。**

若问题测试失败，应立即转向 C3 或 C4 的诊断路线；若 C1 成立，再进入双过程模型和跨数据集实验。任何情况下，都不建议回到 degree/CN、heuristic routing、generic hard negative 或“多加一个 loss”的旧式增量路线。
