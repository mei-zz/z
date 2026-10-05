# Cheap Falsification

## 1. 预先固定的反证问题

V12 先问最便宜的三个问题：

1. M2 是否只是 D 的重命名？
2. M2 是否稳定选择一个跨数据集、跨 seed 的合理 checkpoint，而非固定训练末期？
3. M2 是否拥有独立于已有“匹配 validation + MRR”原则的新机制？

结果读取前已在 [`METHOD_DEFINITION.md`](METHOD_DEFINITION.md) 锁定 `J_M2=0.5*MRR_old-old+0.5*MRR_new` 和 earliest-tie 规则。

## 2. 结果

- M2 与 D 相同：6/12 runs；因此不是完全等价的重命名，但也没有稳定区别。
- M2 与 B 相同：0/12 runs；它不是 old-only MRR 的简单复制。
- M2 选择 epoch ≥98：7/12 runs；epoch 100：4/12 runs。
- new–new validation 正边只有 Cora 4 条、CiteSeer 2 条；V11 history 没有更细的可可靠 new–new 单独选择统计。
- M2 的独立 test：未执行，也不能从 V11 raw 合法恢复，因为 V11 没有保存 M2 epoch 的 checkpoint/prediction tensor，且 V11 test 已经被查看。

## 3. 反证解释

M2 的行为可以由两个普通因素解释：

1. new-node MRR 在训练后期继续上升，50/50 加权自然偏向末期；
2. Cora/CiteSeer 的 validation-new 样本量小，尤其 new–new 极小，复合分数的选择方差可能高。

这已经足以阻止把 M2 当作稳定的新方法。再加上文献审计已经发现“目标近似 validation 用于 shift-aware model selection”是已有方法论，独立 split 实验不再具有证明新算法的性价比。

状态：`CHEAP_FALSIFICATION_FAILED_FOR_METHOD_NOVELTY`。
