# V11 Reanalysis for V12

## 1. 输入和边界

输入是 V11 `raw/formal_repaired/*.json` 的 12 条完整 100-epoch 训练轨迹。数据协议、manifest hash、候选顺序和模型训练均不改变；V12 只重新计算 checkpoint 选择分数。可复现脚本为 [`scripts/reanalyse_v11_m2.py`](scripts/reanalyse_v11_m2.py)，逐运行原始文件 hash 和明细保存在 [`raw/v11_m2_selection.json`](raw/v11_m2_selection.json)。

V11 test 曾被查看，因此下面重复列出的 A–D test 结果只能作为历史探索性证据，不能作为 V12 的独立验证。M2 没有保存的 checkpoint/prediction tensor，故没有伪造 M2 test 数值。

## 2. V11 四规则的历史结果（探索性）

| 数据集 | 模型 | A old Hits@20 | B old MRR | C mixed Hits@20 | D mixed MRR |
|---|---|---:|---:|---:|---:|
| Cora | GraphSAGE | .19067±.01227 | .32438±.00219 | .30650±.02726 | .32929±.01170 |
| Cora | NodeDup | .20235±.13027 | .32813±.00342 | .28273±.08733 | .32843±.00618 |
| CiteSeer | GraphSAGE | .24720±.07334 | .26632±.02408 | .28996±.03862 | .32386±.06165 |
| CiteSeer | NodeDup | .27666±.03492 | .27796±.02785 | .28734±.03613 | .26695±.03424 |

这些均值/标准差来自模型 seeds 1–3 的 repaired V11 test。它们支持 V11 的协议结论：A→B、A→C、B→D 对模型选择的影响并不等价；但不能证明 M2 的独立泛化。

## 3. M2 选择 epoch

| 数据集 / 模型 | M2 epoch（seed 1,2,3） | D epoch（seed 1,2,3） | M2=D |
|---|---|---|---:|
| Cora / GraphSAGE | 99, 94, 100 | 93, 94, 81 | 1/3 |
| Cora / NodeDup | 95, 100, 85 | 95, 90, 85 | 2/3 |
| CiteSeer / GraphSAGE | 99, 100, 98 | 81, 36, 98 | 1/3 |
| CiteSeer / NodeDup | 100, 42, 33 | 82, 42, 33 | 2/3 |
| **合计** | — | — | **6/12** |

M2 在 12 次运行中有 7 次选择 epoch ≥98，有 4 次选择 epoch 100；没有一次与 B 完全相同。它确实改变了选择行为，但方向主要是把 checkpoint 推向固定 100-epoch 预算的末端，而不是显示出跨运行稳定的、可独立解释的目标风险估计。

## 4. 因果分解

- **A→B：** 只改 old–old 选择指标；Cora GraphSAGE/NodeDup 的历史 test MRR 分别增加约 .13371/.12578，说明 Hits@20 选择很不稳定。
- **A→C：** 只加入 new-node validation，四个数据集/模型组合的历史 test MRR 均上升；这确认 V11 的 validation/test 任务错配效应。
- **B→D：** 保持 MRR、加入 new-node validation，Cora GraphSAGE +.00491、Cora NodeDup +.00030、CiteSeer GraphSAGE +.05754、CiteSeer NodeDup −.01101；效应不一致。
- **M2：** 用预注册的 macro-style old/new MRR 选择，现有轨迹只能说明它与 D 有时相同、有时偏向末期。没有保存 M2 checkpoint，不能回答它是否超过 D。

结论：V11 的直接证据支持“协议影响 checkpoint 选择”，不支持“一个新的 task-aligned selection algorithm 已经有效”。
