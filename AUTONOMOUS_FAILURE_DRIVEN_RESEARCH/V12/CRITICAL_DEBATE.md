# Critical Debate

## Researcher

V11 的 A→C 方向在 Cora/CiteSeer、GraphSAGE/NodeDup 四个组合中均为正，说明 old-only validation 与 mixed deployment task 不一致会传递到 checkpoint 选择。M2 进一步把 old-old 与 new-node MRR 放到同一选择目标，理论上比 old-only 指标更贴近归纳式部署。

## Critic

1. **方法论已有覆盖。** 让 validation 接近目标分布、在 distribution shift 下做 model selection，已在 domain generalization、temporal shift 和 validation-split 文献中研究；V12 没有新的估计理论或选择保证。
2. **M2 权重是人为指定。** 0.5/0.5 没有来自部署频率，也没有足够 new–new 样本支持更细的三类权重。
3. **末期偏置替代解释。** M2 在 7/12 次选择 epoch ≥98，可能只是在追逐训练后期 new-node MRR，不是更准确的泛化风险估计。
4. **V11 test 已失去独立性。** 即使可以从 checkpoint 补算 M2 test，也不能把它当作未参与研究决策的 final test。
5. **协议与模型混淆风险。** V11 证明的是 validation/test composition 影响选择，不是 NodeDup 或 GraphSAGE 缺少某个结构算子。

## Experimentalist

如果没有文献碰撞，最低成本的下一步应是冻结 M2 后重新保存 checkpoint，并做两个数据集 × 三个独立 new-node partition × 三个模型 seed；同时冻结 final test。还应报告 old–old、old–new、new–new 的样本量和区间，避免用 2–4 条 new–new 边决定规则。由于文献门槛已失败，本实验在 V12 不启动。

## Judge

证据支持一个真实但已有的方法论结论：NodeDup 的 validation 需要和部署任务对齐，且 Hits@20 与 MRR 的 checkpoint 选择可能显著不同。证据不支持独立的 V12 模型选择算法，也不支持新的 GNN 结构。

最终裁决：`NOVELTY_KILL`。停止 V12，不启动 V13。
