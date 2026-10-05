# Strict Cold-Start Feasibility

## 1. 信息边界

在 strict zero-history 条件下，new node 没有 inference context neighbor。Cora/CiteSeer 当前可用的信息只有：

- Planetoid 节点特征 `x`；
- 节点身份和候选边端点；
- 对非严格节点允许的 context graph（严格节点不应从中取得历史邻居）；
- 没有时间、文本描述、用户属性或其他外部 side information。

因此不能把人为添加的拓扑边当作 strict cold-start 的原始信息。

## 2. 严格 zero-context 节点审计

按 V11 inference graph 的 degree=0 定义严格 zero-context new node：

| 数据集 | new nodes | zero-context new nodes | strict test positives | FeatureCosine test MRR / H@10 / H@20 |
|---|---:|---:|---:|---:|
| Cora | 271 | 12 | 12 | .1749 / .3333 / .5000 |
| CiteSeer | 333 | 30 | 24 | .4418 / .5833 / .5833 |

strict validation FeatureCosine 为 Cora `.4696/.7000/.8000`（10 positives），CiteSeer `.5085/.5714/.6071`（28 positives）。这些 subgroup 很小，只用于可行性审计，不作论文级显著性结论。

## 3. GraphSAGE 的严格边界

对 degree=0 节点，SAGEConv 没有邻居消息可聚合；其输出只经过自身特征的 root transformation、非线性和 dropout。因此在 strict zero-context 子群上，GraphSAGE 的可用信息本质上退化为 feature-only 函数，不能从不存在的历史 topology 恢复额外信息。

这不是新结构缺口的证据：如果 FeatureCosine 或 feature-only MLP 已能解决该子群，增加拓扑传播没有独立输入；如果它们失败，也需要外部信息或重新定义任务，不能凭空从 message passing 中创造历史边。

## 4. 判断

CiteSeer 的 feature proxy 在严格子群上较强，Cora 较弱，说明问题对数据集特征分布敏感。当前没有统一、跨数据集、可由新 GNN 解决而简单 feature-only baseline 无法解释的 strict cold-start 缺口。

