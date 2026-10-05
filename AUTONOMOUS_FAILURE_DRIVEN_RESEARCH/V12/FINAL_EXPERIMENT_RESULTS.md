# V12 Final Experiment Results

## 1. 完成状态

| 阶段 | 状态 | 证据 |
|---|---|---|
| V10/V11 历史与源码审计 | DONE | V10/V11 reports、`V11/scripts/v11_protocol_audit.py`、12 个 repaired JSON |
| 文献碰撞审计 | DONE | [`LITERATURE_NOVELTY_AUDIT.md`](LITERATURE_NOVELTY_AUDIT.md) |
| V11 A–D 重新分析 | DONE / exploratory | [`V11_REANALYSIS.md`](V11_REANALYSIS.md) |
| 预注册 M2 廉价反证 | DONE | [`CHEAP_FALSIFICATION.md`](CHEAP_FALSIFICATION.md)、raw JSON |
| 新独立划分 | NOT_RUN | [`INDEPENDENT_SPLIT_AUDIT.md`](INDEPENDENT_SPLIT_AUDIT.md) |
| 新 GNN / 新 loss / 新训练 | NOT_RUN | 本轮禁止 |

## 2. 可报告数字

M2 epoch 与 D 的重合数为 6/12：

- Cora GraphSAGE：1/3；Cora NodeDup：2/3；
- CiteSeer GraphSAGE：1/3；CiteSeer NodeDup：2/3。

M2 选择 epoch ≥98 的次数为 7/12，epoch 100 的次数为 4/12。由于没有 M2 checkpoint，不能报告 M2 test MRR、Hits@10/20/50，也不能计算 M2 相比 D 的 test delta。

## 3. 历史结果的使用限制

V11 A–D 的 test 数字在 [`V11_REANALYSIS.md`](V11_REANALYSIS.md) 中完整列出，用来保留历史失败和解释 V11 协议效应；它们不是 V12 独立检验。V12 不宣称 M2 在 test 上提升。

## 4. 数据与代码路径

- V11 source JSON：`../V11/raw/formal_repaired/`；
- V11 protocol code：`../V11/scripts/v11_protocol_audit.py`；
- V12 analysis script：`scripts/reanalyse_v11_m2.py`；
- V12 analysis JSON：`raw/v11_m2_selection.json`。

没有覆盖 V1–V11 文件，也没有删除任何失败实验。
