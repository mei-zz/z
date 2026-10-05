# V12 Method Definition and Pre-registration

状态：`LOCKED_FOR_AUDIT`

## 1. 目的与边界

V12 审计的对象不是新 GNN，而是 checkpoint/model-selection rule。现有模型、训练轨迹、数据划分、候选边和 test 均不改变。该规则若有效，也只能被描述为 NodeDup 归纳式链路预测的协议方法；它不能被包装成传播结构创新。

## 2. 预注册规则

对 V11 每个已完成的 100-epoch trajectory，在每个 epoch `t` 计算：

```text
J_M2(t) = 0.5 * MRR_old-old(t) + 0.5 * MRR_new(t)
```

其中 `MRR_new` 是 validation-new 中 old–new 与 new–new 候选的合并 MRR。选择 `J_M2` 最大的 epoch；若并列，选择较早 epoch。M2 的权重在读取 V12 reanalysis 前固定为 0.5/0.5，理由是 deployment 组成未知且希望同时保护 old–old 和 new-node 任务，而不是用 V11 test 估计权重。

不使用：

- V11 test 指标；
- test 子群结果；
- 任何新的超参数、模型宽度、loss 或训练策略；
- new–new 的单独权重，因为修复后的 validation 只有 Cora 4 条、CiteSeer 2 条 new–new 正边，独立估计不稳定。

## 3. 预注册比较

- A：old–old validation Hits@20；
- B：old–old validation MRR；
- C：old–old + validation-new Hits@20；
- D：old–old + validation-new MRR；
- M2：上式的 macro-style old/new MRR。

M2 的廉价筛选只报告 validation trajectory、选择 epoch 和与 D 的重合情况。V11 没有保存 M2 选择 epoch 的 model checkpoint/prediction tensor，因此不能把 V11 已查看的 test 结果伪装成 M2 的独立 test 结果。

## 4. 成功条件（不能事后放宽）

只有同时满足以下条件，才允许追加独立划分：

1. M2 在两个数据集和多个 seed 上表现出区别于 D 的稳定选择行为，而不是偶然末期选择；
2. M2 的 validation 证据不能仅由 tiny new–new 子集驱动；
3. 机制上能提出 test 未参与的、可证伪的协议假设；
4. 文献审计没有发现核心规则已被直接覆盖。

即使通过上述廉价门槛，也必须使用新的 validation/test 划分，三次独立数据划分、每个划分三个模型 seed，且 final test 在规则冻结后才可使用。

锁定日期：2026-09-18。
