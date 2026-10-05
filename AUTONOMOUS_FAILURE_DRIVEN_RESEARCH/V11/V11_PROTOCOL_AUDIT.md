# V11 Protocol Audit

最终状态：`PROTOCOL_EFFECT_CONFIRMED`

本轮只改变 validation 划分和 checkpoint 选择规则，没有改变 GraphSAGE、NodeDup、训练负采样或 decoder 结构。

## 1. V10 官方逻辑复核

NodeDup 的 inductive 生成函数 `do_edge_split_with_ratio_large_induc` 执行以下流程：

1. 用固定 split seed `234` 抽取 10% new nodes；训练节点为 old nodes。
2. old–old 边分成 train、old–old context/validation 和 test 部分。
3. old–new、new–new 边各自保留大部分 context，抽取一部分作为 test target。
4. `training_data` 只包含 old nodes 和 old–old train edges。
5. `inference_data` 包含全体节点以及官方允许的 old–old / old–new / new–new context edges。
6. 官方 `valid['new']` 由 old–old training subgraph 上的 `RandomLinkSplit` 生成，因此 validation target 只覆盖 old–old。
7. 官方 `test['new']` 将 old–old、old–new、new–new target 按 source 组织，并为每个 source 采样 500 个负候选。

原始 validation 和 test 的差异不是模型实现错误，而是任务组成不同：validation 没有 new-node target，test 有 new-node target。

## 2. V11 固定项

- Cora、CiteSeer 原始 cache 不覆盖；原始批次结果保存在 `raw/initial_partition_seed113_invalid_coverage/`。
- repaired partition 使用结构覆盖规则：第一个 new–new 正边作为 validation anchor，第一个与其节点不相交的 new–new 正边作为 test anchor，其余节点由 seed `113` 填充。
- validation-new/test-new target node 集合互斥；跨两组的正边不作为 target，避免标签节点重叠。
- validation-new 负样本只从 old + validation-new 节点中抽取；不访问 test-new 标签。
- 每个模型/seed 固定训练 100 epochs，同一训练轨迹离线选择 A–D，不用 test 提前停止或调参。
- 模型 seed 为 1、2、3；GraphSAGE 与官方 NodeDup duplicated 均运行。

## 3. 协议单元检查

| 检查 | Cora | CiteSeer |
|---|---:|---:|
| old nodes | 2,437 | 2,994 |
| new nodes | 271 | 333 |
| validation-new nodes | 135 | 166 |
| test-new nodes | 136 | 167 |
| validation/test new-node overlap | 0 | 0 |
| validation positives: old–old / old–new / new–new | 678 / 48 / 4 | 590 / 58 / 2 |
| test positives: old–old / old–new / new–new | 936 / 50 / 8 | 800 / 42 / 2 |
| repaired manifest hash | `5ce3891accb8…` | `fff38a5f0189…` |

所有 12 个 repaired run 的 manifest hash 在同一数据集内一致，且每个 JSON 都记录 `selection_metric_test_used=false`。

## 4. 初始失败记录

第一次使用随机 partition seed `113` 时，CiteSeer 的 validation-new 没有 new–new target，因此不满足 V11 预设覆盖要求。该 12 个结果没有混入最终统计，完整保留在 `raw/initial_partition_seed113_invalid_coverage/`。修复规则只依赖结构覆盖，不依赖任何模型分数。
