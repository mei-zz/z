# Final V11 Decision

最终状态：`PROTOCOL_EFFECT_CONFIRMED`

## 1. 是否确认 validation/test 错配影响模型选择？

**确认，且仅确认到协议层面。**

在相同模型、相同训练 seed、相同 100-epoch 训练轨迹和相同候选数据上：

- old–old validation 与 new-node validation 选择出的 epoch 明显不同；
- A→C（加入 new-node validation，仍用 Hits@20）在 Cora/CiteSeer、GraphSAGE/NodeDup 四种组合上 test MRR 均上升；
- A→B（只把 old–old checkpoint 指标从 Hits@20 换成 MRR）在 Cora 上产生约 `+0.126` 至 `+0.134` 的 MRR 改变；
- B→D（加入 new-node validation 并保持 MRR）影响方向不完全一致，说明协议效应不能简化为“新 validation 必然提升所有模型”。

## 2. 推荐协议

后续若继续使用该 NodeDup 任务，建议：

1. validation 必须包含与 deployment/test 相同组成的 old–old、old–new、new–new target；
2. 以 MRR 作为主要 checkpoint 指标，Hits@20 作为辅助指标；
3. 保留真正未参与选择的 final test 或新的 held-out test；
4. 分别报告三类边和 zero-context subgroup；
5. 不把 repaired validation 的收益称为模型结构收益。

## 3. 是否发现新结构需求？

没有。严格 cold-start 审计表明，zero-context 节点上 GraphSAGE 只能使用自身特征，FeatureCosine 在 CiteSeer 已较强；Cora 的弱点也没有被证明是某个缺失传播算子造成的。NodeDup 在协议修复后仍没有稳定、跨数据集的结构性优势。

因此本轮停止，不开发新 GNN 模块，也不自动启动 V12。V11 证明了评测协议会影响模型选择，但没有证明存在值得继续投入的独立网络结构创新。

## 4. 资产与失败保留

- 修复后原始 JSON：`raw/formal_repaired/`；
- 首次覆盖失败但完整保留的 JSON：`raw/initial_partition_seed113_invalid_coverage/`；
- 运行脚本：[v11_protocol_audit.py](scripts/v11_protocol_audit.py)；
- 固定规则：[PROTOCOL_LOCK.md](PROTOCOL_LOCK.md)；
- Test 从未用于 A–D 选择、超参数调整或结构方向选择。

