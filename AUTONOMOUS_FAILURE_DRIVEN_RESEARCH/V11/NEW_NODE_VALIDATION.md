# New-Node Validation

## 1. 设计

V11 将原始 official new nodes 分成互斥的 validation-new 和 test-new。validation-new target 只允许包含：

- old–new：一个端点为 old、另一个为 validation-new；
- new–new：两个端点都为 validation-new；
- old–old：沿用原始 old–old validation，作为 combined validation 的基础。

test-new target 只允许包含 test-new 节点；old–old test 仍保留。跨 validation-new/test-new 的正边不作为 validation 或 test target，避免同一个 new node 同时出现在两侧标签集合中。

推理 context 固定为 V10 inference graph 中已公开的 context edges。重新选择 checkpoint 不会把 validation/test target edge 添加进 message graph。

## 2. 数据覆盖

| 数据集 | Validation-new old–new | Validation-new new–new | Test-new old–new | Test-new new–new |
|---|---:|---:|---:|---:|
| Cora | 48 | 4 | 50 | 8 |
| CiteSeer | 58 | 2 | 42 | 2 |

combined validation 另外包含 Cora 678、CiteSeer 590 个 old–old positives；test 另外包含 Cora 936、CiteSeer 800 个 old–old positives。

## 3. 解释边界

这不是严格 zero-history new-node benchmark：推理时仍允许官方 context graph 中已经公开的部分新节点边。它是与 NodeDup 官方数据生成逻辑兼容的 new-node validation repair。严格 cold-start 另见 [STRICT_COLD_START_FEASIBILITY.md](STRICT_COLD_START_FEASIBILITY.md)。

validation-new 的目的不是产生新的训练信息，而是让 checkpoint 选择目标包含部署时会出现的 new-node ranking 组成。test-new 在所有模型/epoch/规则冻结后才计算。

