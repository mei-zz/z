# Next Problem Decision

最终状态：`NO_NEW_STRUCTURE_PROBLEM`

## 1. 直接回答

**没有找到目前足以进入网络结构创新阶段的新研究问题。**

找到的是一个值得继续做“基准/协议审计”的问题，而不是已经被证实的结构缺口：NodeDup 的 old-node validation 与 mixed new-node test 组成不同，且 degree-0/低 CN 子群稳定更难。

## 2. 关键证据

以下指标均为官方 NodeDup inductive protocol；baseline 表中为百分数，均值和标准差来自模型 seeds 1–3，test 未参与选择。

| 数据集 / 模型 | Test MRR | Hits@10 | Hits@20 | AUC |
|---|---:|---:|---:|---:|
| Cora GraphSAGE | 34.49 ± 0.71 | 57.59 ± 0.82 | 66.00 ± 1.36 | 91.35 ± 0.41 |
| Cora NodeDup | 33.30 ± 0.85 | 56.42 ± 0.81 | 67.11 ± 1.35 | 92.89 ± 0.25 |
| CiteSeer GraphSAGE | 37.42 ± 1.37 | 59.31 ± 1.19 | 68.80 ± 1.48 | 91.92 ± 0.37 |
| CiteSeer NodeDup | 31.87 ± 0.70 | 54.23 ± 0.68 | 64.02 ± 0.95 | 92.54 ± 0.23 |

主要观察：

- Cora NodeDup validation Hits@20 均值约 67.85%，高于 GraphSAGE 65.09%，但 test MRR 低约 1.19 个百分点，Hits@10 低约 1.17 个百分点。
- CiteSeer NodeDup validation Hits@20 均值约 59.60%，低于 GraphSAGE 60.57%；test MRR 低约 5.55 个百分点。
- Cora 的 degree-0 test 子群，GraphSAGE MRR 约 25.63%，NodeDup 约 24.22%；CiteSeer 对应约 32.18% 与 22.40%。NodeDup 没有稳定修复低度子群。
- CiteSeer 的 FeatureCosine test MRR 为 36.84%，接近但略低于 GraphSAGE 37.42%，并明显高于 CN/RA；但其 validation MRR 只有 1.36%，说明直接优化 feature proxy 也不能解决 split mismatch。
- Cora 的 RA test MRR 31.30%，明显低于 GraphSAGE；CiteSeer 的 FeatureCosine 和 GraphSAGE 各自覆盖不同区域，显示的是数据集/分割依赖，而不是一个已确认的统一传播缺陷。

## 3. Researcher–Critic–Judge

**Researcher：** 新节点和低度节点缺少训练期结构上下文，可能导致 message passing 的邻域估计不稳定；NodeDup 在 Cora validation 的 Hits@20 改善说明某种训练目标或表示偏置可能有帮助。

**Critic：** 至少有四个替代解释：

1. validation 只看 old–old，而 test 混合 new-node 候选，checkpoint 选择目标错配；
2. degree-0/低 CN 是候选难度和可观测结构稀疏造成的，不代表需要新传播算子；
3. NodeDup 的 duplication 可能改变优化分布，却没有保留对真实新节点的充分信息；
4. Cora 与 CiteSeer 的特征可预测性不同，FeatureCosine 的反转结果说明数据集特异性和 split composition 很重要。

**Experimentalist：** 最便宜的证伪实验不是开发模块，而是固定 NodeDup 数据生成逻辑，新增与 test 构成匹配的 new-node validation；同时报告 old–old、old–new、new–new 三组，并在相同 checkpoint 规则下比较 GraphSAGE、NodeDup、FeatureCosine、CN/RA。若收益只在 old–old validation 出现，结构假设应停止。

**Judge：** 当前证据只支持“归纳式 LP 的评测协议需要更严格的 validation 设计”，不支持独立的新 GNN 机制。进入 V11 结构创新会把协议问题误当成表达能力问题，因此本轮停止。

## 4. 下一步边界

除非先完成 new-node validation / strict cold-start 的协议修复并发现跨数据集、跨 seed 且简单代理无法解释的稳定缺陷，否则不继续设计新 GNN。尤其不应重新尝试：NodeDup/LEAP 类拓扑增强、feature–topology 普通融合、attention/gate、更宽 hidden、换 loss 或重新包装 V1–V9 失败模块。

