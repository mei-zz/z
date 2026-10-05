# Final V12 Decision

最终状态：`NOVELTY_KILL`

## 决策依据

1. V11 的 repaired protocol 和历史结果有效保留，确认 validation/test 任务错配会影响 checkpoint 选择；
2. 预注册 M2 的廉价 reanalysis 已完成，但 M2 只在 6/12 次运行中等同于 D，且 7/12 次偏向 epoch ≥98；
3. V11 没有保存 M2 checkpoint/prediction tensor，V11 test 又已被查看，因此没有合法的 M2 独立 test 结果；
4. “使 validation 更接近目标分布以进行 shift-aware model selection”已被 2023–2024 的 domain-generalization、temporal-shift 和 validation-split 工作覆盖；
5. NodeDup、semi-inductive LP benchmark 和 HeaRT 已经覆盖当前任务定义、冷启动场景和 link-prediction protocol audit 的主要组成。

## 最终回答

- 是否发现独立的 V12 方法创新：**没有**。
- V11 的协议发现是否真实：**是，限于协议/模型选择层面**。
- M2 是否完成真实独立验证：**没有**。
- 是否开发新 GNN：**没有**。
- 是否值得继续把该规则包装成论文方法：**不值得**。
- 是否启动 V13：**不启动**。

V12 的全部 raw、脚本、历史结果和 NOT_RUN 记录均保留。
