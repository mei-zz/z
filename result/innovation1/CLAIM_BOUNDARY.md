# CLAIM BOUNDARY — R-HSPE

## 可说、且证据支持

| 建议主张 | 证据范围 / 安全限定 |
|---|---|
| R-HSPE 为 pairwise link predictor 增加 candidate-specific hypergraph context。 | 冻结方法定义与代码：按候选对枚举 incident hyperedge-pair token multiset，以训练-only ECDF 大小秩编码，mean/max pool 后加零初始化 residual。 |
| R-HSPE 是轻量 decoder-side hypergraph-context plug-in，增加 75 个可训练参数。 | 冻结参数定义；V17.4 在 NCN/NCNC 各自分数上测试。参数比例依 backbone 见 METRIC_TABLES.md。 |
| 在冻结 V17.4 fixed-final-10 test 协议下，R-HSPE 对 NCNC 在 Cora 和 PubMed 均有正 paired MRR gain。 | Cora mean Δ=0.025852682660934833，median Δ=0.03415585230049967，5/5；PubMed mean Δ=0.007136914679784767，median Δ=0.007610820161587428，5/5。表述必须带上 dataset、protocol、paired seeds。 |
| 在同一 V17.4 协议下，NCN 插件 arms 也有正的 paired MRR effects。 | Cora/PubMed 分别 5/5 seed wins；主结论仍按冻结包优先报告 NCNC 及 NULL75 对照。 |
| R-HSPE standalone 在 V17.2 test 中相对 B0 有正 mean paired MRR。 | Cora 0.14411309043713388（5/5）、PubMed 0.01294802474118606（4/5）、Citeseer 0.0887476626284336（3/3）；只能称为这些数据集和 20-negative protocol 下的结果。 |
| 冻结机制标签为 CONTEXT_DRIVEN，hyperedge-size causal claim 为 NOT_SUPPORTED。 | V17.1/V17.2 controls 不支持大小因果归因；对照是机制诊断而非因果分解。 |
| focused novelty audit 未识别 exact collision。 | 只指所检查的来源和范围；必须同时说明 focused audit 不是 exhaustive priority proof。 |

## 不可说 / 需要避免

- 不写 “first use of hyperedge size” 或 “first candidate-specific hypergraph context”，也不使用“首创/首次/优先权已证”。
- 不写 hyperedge size causes the gain；ECDF rank component 的独立因果贡献没有被识别。
- 不写 universal three-dataset transfer、普遍优于 strong backbones 或 Citeseer strong-backbone improvement。Citeseer V17.4 只有 validation，ΔMRR 为负且 gate 失败，test 没运行。
- 不把 V17.3 standalone benchmark 说成 equal-compute SOTA：其 R-HSPE rank 为 Cora 4、PubMed 4、Citeseer 3；冻结状态是 WEAK standalone competitiveness。
- 不声称 standalone SOTA 或替代 NCN/NCNC 的 backbone。
- 不将 V17.3 100-epoch/best-validation MRR 与 V17.4 10-epoch/final-checkpoint MRR 混进同一 ranking table。
- 不把 V17.1 或 V17.4 validation 结果标成 test；不把 Citeseer validation failure 改写为 test failure。
- 不将 20 negatives/query 评估称为 all-node ranking。
- 不将 focused audit 的 “NO_EXACT_COLLISION_IDENTIFIED_IN_FOCUSED_AUDIT” 改写成 “NO COLLISION EXISTS”。
- 不自行扩写 R-HSPE 的正式英文全称；frozen artifact 未定义展开名。

## Novelty risk level

| 维度 | 等级 | 解释 |
|---|---|---|
| Exact-collision risk | LOW（在已检查范围内） | focused audit 没识别 exact collision；材料不完整处标为 NR/UNKNOWN，且检索不是 exhaustive。 |
| Conceptual-overlap risk | MEDIUM | CCLPH 与 candidate hyperedge/cardinality context 接近；NCN/NCNC 已建立候选结构集合的学习式 pooling precedent。 |
| Claim safety | HIGH（仅限下述窄主张） | 只说冻结 joint construction 与 Cora/PubMed 插件结果；避免 first、causal、universal、standalone-SOTA。 |

## 推荐论文句式

**English:** “R-HSPE adds a candidate-specific hypergraph-context residual to an existing pairwise link predictor. Under the frozen V17.4 fixed-final-epoch protocol, it improves paired test MRR over NCNC on Cora and PubMed; transfer to the Citeseer strong-backbone setting is not supported.”

**中文：** “R-HSPE 在既有 pairwise link predictor 的解码端加入候选条件化的超图上下文残差。在冻结的 V17.4 固定最终轮次协议下，该插件在 Cora 与 PubMed 上相对 NCNC 获得正的配对测试 MRR 增益；Citeseer 强 backbone 迁移未获支持。”

## 关键限制

1. Citeseer plugin transfer gate 在 validation 阶段失败，test 未访问。
2. Size causality 不支持；控制对比不是因果分解。
3. novelty search 是 focused audit，不是 exhaustive literature-priority proof。
4. standalone benchmark 相对 NCN/NCNC 弱；插件结论 protocol-specific。
5. 评估每个正查询仅配 20 个负例；Cora 原始数据目录记录不完整，复现应归档上游数据与预处理配方。
