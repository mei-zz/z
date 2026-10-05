# Independent Split Audit

状态：`NOT_RUN`

## 未执行原因

V12 规定的独立检验需要至少两个真实数据集、三个独立数据划分、每个划分三个模型 seed，并在 final test 冻结后评估。该阶段没有启动，原因不是资源不足，而是前置门槛未通过：

1. 文献审计判定 V12 的核心方法论已被 distribution-shift model-selection 工作覆盖，不能作为新算法主张；
2. M2 仅在 6/12 次轨迹中等同于 D，且 7/12 次偏向 epoch ≥98，没有显示稳定的独立选择机制；
3. V11 没有保存 M2 所需的 checkpoint/prediction tensor，不能把已查看的 V11 test 结果重用为独立证据；
4. 为了证明一个已知方法论在 NodeDup 上的具体应用而追加 18 个或更多训练组合，不符合本轮“最小必要预算”和 V12 的停止规则。

## 保留的有效资产

- V11 repaired 数据协议和 manifest hash 未修改；
- V11 原始 test 和 first invalid partition 均保留；
- V12 reanalysis 的输入文件 hash 保存在 [`raw/v11_m2_selection.json`](raw/v11_m2_selection.json)；
- 没有建立新的 split、没有访问新 test、没有新增模型训练。

因此本文件不提供独立 split 的正面或负面性能结论。
