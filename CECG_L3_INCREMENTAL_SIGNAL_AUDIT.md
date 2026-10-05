# CECG L3 Incremental Signal Audit

日期：2026-09-16

## 最终判定

**STOP CECG**。

本轮不实现完整 CECG GNN，不继续为 CECG 增加救援模块或模型复杂度。修正版 Stage0/first-pass probe 已经检验了唯一值得继续的问题：在 `CH2-L3/CH3-L3` 与 4-node graphlet 都进入控制组后，CECG 的 path-interaction topology 是否还能带来增量信号。结果为 `P4 < P3`，且 5 个 seed 的方向全部一致或不利，因此不满足 `P4>P3` 的进入条件。

## 1. 人工文献与逻辑审计

对候选 pair `(u,v)`，定义

```text
A = N(u) \ (N(v) ∪ {v})
B = N(v) \ (N(u) ∪ {u})
P_uv = {(a,b): a∈A, b∈B, (a,b)∈E}
```

`P_uv` 中的每个 witness 都是 `u-a-b-v` 形式的受限长度 3 路径。因此，`|P_uv|` 不是一个新的路径阶数；在简单无向图的候选非边上，它是普通长度 3 支持 `(A^3)uv` 的 exclusive/restricted 子集。它也与 Local Path 中的 `A^3` 项、L3 link predictor 及 CH2-L3/CH3-L3 处于同一局部路径家族。Local Path Index 使用 `A^2 + εA^3`；L3 工作直接以长度 3 路径建模，CH2-L3/CH3-L3 则进一步按局部社区和内部/外部连接组织这些路径。近期 BLANT-Predict 也说明 4-node graphlet/motif 计数已是直接相关的强先验。因此，“candidate edge closes a 4-cycle”本身不能作为 novelty。

相关先验：

- [Local Path Index 的矩阵形式](https://pmc.ncbi.nlm.nih.gov/articles/PMC7698359/)
- [L3、CH2-L3 与 CH3-L3 的定义与实验](https://pmc.ncbi.nlm.nih.gov/articles/PMC9945744/)
- [BLANT-Predict：graphlet/motif-based link prediction](https://pmc.ncbi.nlm.nih.gov/articles/PMC13366520/)

仍可审计的最小创新点只能是：构造 witness-pair interaction graph `I_uv`，其中节点是 `P_uv` 中的 witness pair `(a_i,b_i)`；边定义为：

- A-edge：两个 witness 共享同一个 `a`；
- B-edge：两个 witness 共享同一个 `b`；
- 可选 C-edge：`(a_i,a_j)∈E` 或 `(b_i,b_j)∈E`。

本轮只提取无参数拓扑描述符，不使用 learnable attention、GNN、gate 或 expert。这样可以直接测试 interaction topology 是否超出普通 L3/graphlet 的解释范围。

## 2. Stage0 数据与支持度

实验在服务器的 Cora HeaRT 官方处理数据上完成，使用 seeds `0–4`。每个 seed 为 `2708` 个节点、`4488` 个 train positives、`263` 个 validation positives、`527` 个 test positives；test support 统计使用全部 `527 × 500` 个官方 negative candidates。当前服务器仓库只有 Cora HeaRT seeds，未伪造 CiteSeer/PubMed 或更大数据集结果。

表中 L3 support 指 exclusive witness count `|P_uv|`，不是 P1 中使用的 full ordinary L3 特征。

| 数据集 | 标签 | candidates | `L3>0` | `L3≥2` | `L3≥5` | mean `|P_uv|` |
|---|---:|---:|---:|---:|---:|---:|
| Cora | positive | 2,635 | 945 (35.86%) | 455 (17.27%) | 115 (4.36%) | 0.8558 |
| Cora | negative | 1,317,500 | 131,575 (9.99%) | 61,620 (4.68%) | 12,100 (0.92%) | 0.2229 |

支持度不是零，因此本次 STOP 不是由“完全没有 witness”触发；判死点是控制后没有增量预测信号。

## 3. 受控 probe 协议

全部 probe 都是标准化特征上的 logistic regression；没有 GNN。

| Probe | 特征组成 |
|---|---|
| P0 | CN + AA + RA + degree product/log-degree controls |
| P1 | P0 + full ordinary L3 + Local Path `A^3` |
| P2 | P1 + CH2-L3 + CH3-L3 |
| P3 | P2 + 4-node graphlet proxy |
| P4 | P3 + CECG `I_uv` topology descriptors |

关键协议修正：最终版本的 `P3` 是 `P2 + graphlet`，不是早期草稿中的 `P1 + graphlet`。因此下面的 P4/P3 比较是按审计要求的严格控制比较。

### 5-seed aggregate

| Probe | AUC mean ± std | AP mean ± std |
|---|---:|---:|
| P0 | 0.415770 ± 0.003538 | 0.465844 ± 0.003617 |
| P1 | 0.501145 ± 0.012553 | 0.531962 ± 0.007160 |
| P2 | 0.475697 ± 0.011254 | 0.516946 ± 0.004783 |
| P3 | 0.441681 ± 0.011912 | 0.497645 ± 0.011266 |
| P4 | 0.435730 ± 0.012067 | 0.490377 ± 0.010717 |

`P4 − P3`：AUC `−0.005951`，AP `−0.007268`。

### Per-seed P4 − P3

| seed | ΔAUC | ΔAP |
|---:|---:|---:|
| 0 | −0.004677 | −0.005203 |
| 1 | −0.004720 | −0.007223 |
| 2 | −0.007250 | −0.010136 |
| 3 | −0.004395 | −0.005090 |
| 4 | −0.008711 | −0.008688 |

5 个 seed 没有一个出现正向的 overall P4 increment。

### 按 exclusive L3 support 分层

validation probe 按 `|P_uv|` 分为 `0`、`1`、`2–3`、`4–7`、`≥8` 五层；每层每个 seed 的样本数分别为 `255/102/83/50/36`。各层跨 seed 的 ΔAUC 均值如下：

| `|P_uv|` bin | mean ΔAUC | seed-level range |
|---|---:|---:|
| 0 | −0.000848 | −0.001932 to +0.000093 |
| 1 | −0.007615 | −0.013846 to −0.003077 |
| 2–3 | −0.012907 | −0.024419 to −0.003488 |
| 4–7 | −0.003922 | −0.014260 to 0.000000 |
| ≥8 | −0.009091 | −0.019481 to 0.000000 |

这说明失败不是只由低 support 区域造成；在有多个 witness 的层中也没有可见的 topology 增量。

## 4. 退出条件检查

- 支持度过低：未触发；Cora 上有非零且有多 witness 的 candidates。
- `P4>P3`：**未满足**；aggregate AUC/AP 均下降，5 个 seed 均不利。
- matched L3 后仍有增量：**未满足**；各 support strata 的 ΔAUC 均值均不为正。
- true topology > shuffled topology：未执行。因为 P4 已在更早的硬门槛失败，继续做 shuffle 不会产生 GO 依据，避免无价值的救援实验。
- 完整 CN×degree propensity matching：未执行。本轮已完成 L3 分层；P4 在此之前已经失败，因此不启动额外匹配或模型救援。
- ≥2 datasets/regimes：未满足。当前只有 Cora HeaRT 真实 Stage0 结果，且单数据集已失败。

## 5. 结论与后续边界

当前证据支持的结论是：CECG 的 path-interaction topology 在已控制 CN、degree、full L3/Local Path、CH2-L3、CH3-L3 和 4-node graphlet 后，没有显示可复现的增量 link-prediction signal。继续实现完整 CECG GNN 会把一个未通过增量信号审计的统计特征包装成更复杂的模型，缺乏实验依据。

**最终动作：STOP CECG。** 不进入 Stage1，不实现完整 CECG GNN，不继续为该候选添加 attention/gate/expert/更大模型。

## 6. 可复现实验文件

- [审计脚本](D:/我的资料库/Documents/Downloads/DCDLP-main/scripts/audit_cecg_l3.py)
- [原始 Stage0 JSON](D:/我的资料库/Documents/Downloads/DCDLP-main/results/cecg_l3_stage0/CECG_L3_STAGE0_SUMMARY.json)

