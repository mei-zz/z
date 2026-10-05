# Next Architecture Research

## 当前决定

暂不开发新结构。当前结论是：`BENCHMARK_PARTIALLY_READY`，因此不满足“可以无条件进入下一轮结构创新”的门槛。

## 已经确认的真实现象

1. LPShift 官方构造能够在远程 V100 上稳定完成数据生成和 GCN 训练。
2. CN 阈值确实产生可测的 distribution shift；默认 `(1,2)` 的 CN/AA/RA 在 test 上几乎失效，而 `(2,4)` 的 test MRR 恢复到约 0.30。
3. 官方 GCN 在默认组 validation MRR 0.0712、test MRR 0.0578；训练 random negatives 几乎饱和，说明训练候选和评测困难候选之间存在明显差异。
4. AA/RA 在 LPShift 中仍然是非常强的协议基线，任何新结构若不能在 validation 上超过它们，不能声称解决了 GNN 失败。

## 尚未确认的问题

- DCDLP 在保留官方额外 context edges 后是否能合法运行；
- GCN、DCDLP、AA/RA 的差距是否跨随机 seed 复现；
- shift 强度改变的是模型的信息瓶颈，还是只改变了候选 CN 分布；
- 官方负样本中少量原始 positive overlap 和重复候选对排名的影响。

## 下一轮的最小必要工作

1. 写一个不改任务定义的 LPShift adapter，显式存储 `message_edge_index` 与 `train_pos` 两个对象，不能继续只用 `GraphDataset.train_graph()`。
2. 为 adapter 写 target masking、候选行顺序、负样本哈希和 message graph hash 单测。
3. 在 `(1,2)` 与 `(2,4)` 上对官方 GCN、DCDLP Parent、AA、RA 做配对 seeds；validation MRR 负责选择，test 仅最后报告。
4. 先判断强启发式是否已经解释全部收益。只有在它们和 DCDLP 都留下稳定、可定位的 failure subgroup 后，才允许提出结构假设。

## 禁止事项

- 不把普通 OGB split 称为 LPShift；
- 不过滤官方 negatives 后继续声称是同一 benchmark；
- 不用 test 选择阈值、结构或超参数；
- 不以 AA/RA 未比较为由继续添加 attention、gate、loss 或 hidden size；
- 不把单 seed GCN 结果写成稳定提升。

当前没有足够证据支持任何新架构候选。下一阶段应先完成协议 adapter 和多 seed baseline audit；若强基线已经解释错误，继续结构搜索应停止。

