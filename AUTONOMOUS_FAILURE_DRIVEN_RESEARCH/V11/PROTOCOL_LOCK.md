# V11 Protocol Lock

本文件在读取 V11 结果前锁定。

## Scope

只审计 NodeDup inductive split 的 validation/test 任务错配，不实现新的 GNN、decoder、loss 或数据增强机制。

## Data

- 使用 V10 已恢复的 Cora/CiteSeer cache，不覆盖原始 cache。
- 原始 train/inference graph、原始 old–old validation candidates 和原始 test candidates 保留为独立对照。
- 将原始 official new nodes 按固定规则划分为 validation-new 与 test-new：按 node id 排序的第一个 new–new 正边作为 validation anchor，按 node id 排序的第一个与其节点不相交的 new–new 正边作为 test anchor，其余节点由 `new_node_partition_seed=113` 填充；二者不重叠。该规则只使用结构覆盖约束，不使用任何模型指标。
- 仅将完全由 validation-new 节点构成的 old–new/new–new 正边放入 validation-new；完全由 test-new 节点构成的正边放入 test-new；跨 validation-new/test-new 的正边不作为目标标签，避免节点重叠。
- validation-new 的负样本只从 old + validation-new 节点中固定抽取；不读取 test-new 目标标签。
- inference context 仍只使用 V10 inference graph 中已公开的 context edges；任何 validation/test target edge 不因重新选择 checkpoint 而加入 context。

## Model and training

- Plain GraphSAGE (`augment=none`) 和官方 NodeDup (`augment=duplicated`)。
- 两层 SAGE，hidden/output 256，sum predictor，dropout 0.5，Adam；Cora lr `5e-4`，CiteSeer lr `1e-4`。
- 训练 seeds 1、2、3；split seed 234，new-node partition seed 113。
- 每个模型/seed 使用完全相同的 100 epoch training trajectory；不在训练过程中用任何 validation 提前终止，以便对 A–D 只改变 checkpoint 选择规则。

## Selection rules

- A: 原始 old–old validation，Hits@20 最大。
- B: 原始 old–old validation，MRR 最大。
- C: 原始 old–old + validation-new，Hits@20 最大。
- D: 原始 old–old + validation-new，MRR 最大。

Test 只在 epoch 和规则冻结后评估。所有 test 结果为描述性泛化结果，不参与规则、模型或超参数选择。
