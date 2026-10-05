# Phase 2 Selective Routing 实验结果与创新点判断

## 1. 实验是否完成

已完成。

服务器 `10.16.126.245` 上的 Step 11 已完成全部 20 个运行：

```text
M0/M1/M2/M3 × seed 0,1,2,3,4 = 20 runs
```

每个 run 均为 `COMPLETED`，并且生成了：

- checkpoint；
- HeaRT official 困难负样本上的测试结果；
- intervention evaluation；
- before/after/delta 预测文件；
- 5 类 post-hoc probe；
- manifest 和 aggregate summary。

Step 12 原本尚未在服务器上生成，现已使用服务器 `mei_env` 对已完成结果执行，并下载回当前工作区。M1/M2/M3 相对 M0 的三个配对分析结果均为：

```text
PIVOT_TO_CALIBRATION
```

这不是实验失败，而是说明当前结果值得继续做校准/机制补实验，但尚不足以进入多数据集确认阶段。

## 2. 结果文件位置

完整结果目录：

[results/phase2_selective_local/cora5](D:/我的资料库/Documents/Downloads/DCDLP-main/results/phase2_selective_local/cora5)

三个配对决策报告：

- [M1_vs_M0 决策报告](D:/我的资料库/Documents/Downloads/DCDLP-main/results/phase2_selective_local/cora5/decision/M1_vs_M0/PHASE2_SELECTIVE_DECISION_REPORT.md)
- [M2_vs_M0 决策报告](D:/我的资料库/Documents/Downloads/DCDLP-main/results/phase2_selective_local/cora5/decision/M2_vs_M0/PHASE2_SELECTIVE_DECISION_REPORT.md)
- [M3_vs_M0 决策报告](D:/我的资料库/Documents/Downloads/DCDLP-main/results/phase2_selective_local/cora5/decision/M3_vs_M0/PHASE2_SELECTIVE_DECISION_REPORT.md)

每个模型目录都包含：`raw/`、`checkpoints/`、`predictions/`、`mechanism_audit/`、`probe/`、`aggregate/`、`logs/`、`manifest.csv`。

## 3. HeaRT 测试性能

下表是 5 个 seed 的均值。评测使用的是 Cora HeaRT official grouped candidates，不是 uniform 负样本。

| 模型 | 配置 | MRR | 相对 M0 | Macro-MRR | Worst-group MRR | Group gap |
|---|---|---:|---:|---:|---:|---:|
| M0 | raw + audited | 0.100901 | — | 0.110643 | 0.017216 | 0.192153 |
| M1 | residual + audited | 0.102602 | +0.001701（+1.69%） | 0.113091 | 0.017381 | 0.203152 |
| M2 | raw+residual + audited | 0.105816 | +0.004915（+4.87%） | 0.117079 | 0.019600 | 0.207209 |
| M3 | residual + disabled | 0.102688 | +0.001787（+1.77%） | 0.113313 | 0.017401 | 0.204860 |

### 3.1 预测结果怎么解释

表面上看，M2 的平均 MRR 最高，M1/M3 也高于 M0。但 5-seed 配对 bootstrap 区间如下：

| 比较 | MRR 平均差 | 95% bootstrap CI | 解释 |
|---|---:|---:|---|
| M1−M0 | +0.001701 | [-0.001529, 0.005270] | 方向偏正，但区间跨 0 |
| M2−M0 | +0.004915 | [-0.001172, 0.010781] | 平均提升最大，但区间仍跨 0 |
| M3−M0 | +0.001787 | [-0.001914, 0.005198] | 方向偏正，但区间跨 0 |

因此，当前可以说：

> 在 Cora 5-seed 探索实验中，三个候选的平均 HeaRT MRR 都没有下降，M2 的平均提升最大。

当前不能说：

> residual 或 disabled interaction 已经带来统计确认的预测性能提升。

原因是 seed 数量只有 5，MRR 配对区间都跨 0，而且 M2 的优势主要来自少数 seed 的大幅提升。

### 3.2 稳定性与 group robustness

M1/M2/M3 的 `worst_group_mrr` 均值略高，但区间仍跨 0。更值得注意的是，三种候选的 `group_gap` 均变大：

- M1：+0.010999；
- M2：+0.015056；
- M3：+0.012707。

如果 `group_gap` 越小代表不同 degree/CN quadrant 越公平或越稳定，那么当前候选虽然平均 MRR 上升，却伴随 group gap 恶化。不能把这次实验总结成“整体鲁棒性提升”。

## 4. Controlled intervention 结果

所有模型的干预配对覆盖率都完整：

```text
CN intervention valid rate     = 0.79 / seed
degree intervention valid rate = 1.00 / seed
M0-M1-M2-M3 的 paired intersection coverage = 1.00
```

CN 的 coverage 低于 1 不是程序错误，而是 Cora 某些 pair 无法构造满足所有 forbidden-edge 和 2-switch 约束的候选；代码将其标记为 missing，没有用零替代。这个 coverage 必须在论文中报告。

### 4.1 分支路由结果

`routing_selectivity` 越高，表示目标分支在总分支响应中占比越高。

| 比较 | CN routing delta | degree routing delta | CN target response delta | degree target response delta |
|---|---:|---:|---:|---:|
| M1−M0 | +0.000130 | **−0.050214** | **−0.006116** | +0.006326 |
| M2−M0 | **−0.029903** | **−0.007784** | +0.150010 | +0.039418 |
| M3−M0 | +0.057612 | **−0.025686** | +0.085157 | +0.011788 |

对应的 cross-sensitivity：

| 比较 | CN 干预 cross-sensitivity delta | degree 干预 cross-sensitivity delta |
|---|---:|---:|
| M1−M0 | +0.010568 | +0.009225 |
| M2−M0 | +0.070064 | +0.071509 |
| M3−M0 | **−0.075420** | +0.006929 |

### 4.2 对创新点 3 的判断

当前结果不支持“residual CN 自动带来更好的 selective routing”：

- M1 的 degree routing selectivity 在 5 个 seed 全部下降，均值下降约 0.0502；
- M1 的 CN routing 基本不变，均值只提升 0.00013；
- M2 虽然 target response 明显变大，但 cross response 也明显变大，所以 selectivity 反而下降；
- M3 的 CN routing 改善较明显，但 degree routing 仍下降。

这说明当前训练目标可能把“目标分支响应变大”和“非目标分支响应变小”混合在一起，单纯增加 target response 并没有保证选择性提高。

更重要的是，当前 M0–M3 都开启 score-level routing，没有 no-routing 或 latent-routing 基线。因此本实验不能独立证明 score-level routing 相对旧方法更好。

## 5. Interaction audit 结果

M0/M1/M2 的 audited interaction share 明显低于 0.20 cap，且本次统计的 cap violation rate 为 0；M3 的 interaction share 精确为 0。

| 配置 | CN 干预前 interaction share | degree 干预前 interaction share |
|---|---:|---:|
| M0 audited | 0.019696 | 0.021654 |
| M1 audited | 0.018154 | 0.020081 |
| M2 audited | 0.017768 | 0.019269 |
| M3 disabled | 0 | 0 |

这说明：

- disabled 的“精确为零”实现和结果一致；
- audited 模式在当前训练配置下没有让 interaction share 接近 cap；
- 但没有运行 M4 unrestricted，因此还不能证明 audited 比 unrestricted 更好，也不能证明 interaction audit 是性能/机制结果的必要原因。

此外，当前分析器对 M3 使用 audited gate 会天然判定该项失败；所以 M3 应被解释为 interaction identification control，而不能与 M1/M2 使用同一 GO 标准。

## 6. Post-hoc leakage probe 结果

当前 5 个 probe 实际上是 5 个表示—目标映射，模型均为 `StandardScaler + Ridge`。三个 probe seed 对 Ridge 回归产生了完全相同的数值，因此它们不是三次真正独立的随机 probe 重复；这不会影响代码流程，但会降低“probe seed 重复验证”的有效性。

### 6.1 R² 结果

| Probe | 角色 | M0 | M1 | M2 | M3 |
|---|---|---:|---:|---:|---:|
| `z_cn → degree` | cross leakage | -68.084 | 0.440 | 0.423 | 0.451 |
| `z_residual → degree` | cross leakage | 0.161 | 0.146 | 0.117 | -0.083 |
| `z_degree → cn_residual` | cross leakage | 0.001 | -0.001 | 0.006 | -0.006 |
| `z_degree → degree` | target retention | 0.877 | 0.877 | 0.876 | 0.877 |
| `z_cn → cn_residual` | target retention | 0.217 | 0.916 | 0.917 | 0.933 |

### 6.2 对 probe 的专业解释

有利信号：

- `z_residual → degree` 的 R²：M1、M2、M3 均下降，M3 降幅最大；
- `z_degree → degree` 基本保持不变，说明 degree branch 的目标信息没有明显丢失；
- `z_cn → cn_residual` 大幅上升，说明 residual CN branch 对其目标结构量的保留能力增强。

必须谨慎的信号：

- `z_cn → degree` 从 M0 的 -68.084 变为 M1/M2/M3 的约 0.42–0.45。这个变化不是“泄漏下降”，而是相反地显示候选 CN 表示变得更能线性预测 degree；
- M0 的 -68.084 是异常大的负 R²，表明该 probe 存在严重的分布/尺度/小样本不稳定性，不能把它当作“没有泄漏”的可靠基准；
- 由于至少一个关键 cross probe 明显恶化，不能用“任意一个 probe R² 下降”就宣称整体 leakage 下降。

因此，当前 post-hoc audit 的结论只能是：

> residual/disabled 候选对 `z_residual → degree` 的线性交叉预测有降低，但 CN branch 到 degree 的结果异常且方向相反；整体交叉泄漏没有得到干净、单调、稳定的证明。

正式实验前应检查 probe 的目标尺度、分割分布、R² 的异常负值，并加入 permutation/null probe、非线性容量受控 probe 和更稳健的标准化/分层报告。

## 7. 三个 Step 12 决策的准确含义

### M1 vs M0：`PIVOT_TO_CALIBRATION`

M1 的优点：

- 平均 MRR 小幅上升；
- degree branch target response 略升；
- `z_residual → degree` 泄漏下降；
- audited interaction share 很低且没有 cap violation。

M1 的主要问题：

- degree routing selectivity 在所有 seed 下降；
- CN target response 略降；
- CN/degree cross-sensitivity 都上升；
- `z_cn → degree` probe 从异常负值变成正值，不能判定为泄漏改善；
- group gap 上升。

判断：**residual CN 有预测性能和目标保留方面的潜力，但当前没有证明 selective routing 改善。**

### M2 vs M0：`PIVOT_TO_CALIBRATION`

M2 的优点：

- 平均 MRR、macro-MRR、worst-group-MRR 均为三个候选中最好；
- CN/degree target response 均明显增加；
- `z_residual → degree` 泄漏下降；
- audited interaction share 受控。

M2 的主要问题：

- CN/degree routing selectivity 都下降；
- CN/degree cross-sensitivity 都大幅上升；
- group gap 上升最多；
- `z_cn → degree` cross probe 同样从异常负值变为正值；
- raw+residual 的性能增益可能来自更多可用信息，而不是更好的可辨识路由。

判断：**M2 是当前最强的预测性能候选，但不是当前最强的机制候选；它更像“性能优先、选择性不足”的模型。**

### M3 vs M0：`PIVOT_TO_CALIBRATION`

M3 的优点：

- CN routing selectivity 提升最多；
- CN cross-sensitivity 明显下降；
- 两类 target response 都提高；
- interaction share 精确为 0；
- `z_residual → degree` probe 明显下降。

M3 的主要问题：

- degree routing selectivity 仍然下降；
- degree cross-sensitivity 略升；
- 平均 MRR 提升不具确认性；
- disabled 不是 audited 的替代证明，且没有 M4 unrestricted 对照。

判断：**M3 对“禁用交互能提高部分机制可控性”提供了初步支持，但不能证明 audited 设计优于 unrestricted，也不能证明所有结构因素都能被选择性路由。**

## 8. 对五个创新点的最终判断

| 创新点 | 当前实验结论 | 可行性判断 |
|---|---|---|
| 1. Conditional CN Residual | M1 平均 MRR略升、CN target retention显著增强，但 degree routing和部分 cross probe 不理想 | **可行，但需要校准和直接基线；尚未证明全面优于 raw CN** |
| 2. Controlled Intervention | validator、coverage、before/after/delta 正常；干预结果有区分度 | **实现可行，作为机制审计工具成立；还需补负方向、+2和random-rewire** |
| 3. Score-Level Selective Routing | 当前结果没有同时改善 CN 和 degree selectivity，且缺少 no-routing/latent-routing 对照 | **方法设计可行，但本轮未验证其独立增益** |
| 4. Interaction Audit | disabled 精确零；audited share受控；但没有 unrestricted M4 | **控制机制实现可行，必要性和优越性尚未验证** |
| 5. Independent Post-hoc Leakage Audit | 冻结、验证选参、测试评分流程成立；部分 probe 改善，部分 probe 异常恶化 | **审计流程可行，但当前 probe 结果不足以支持“整体泄漏下降”** |

## 9. 当前创新点是否“足够创新”

基于代码和本次真实结果，最客观的判断是：

1. 单独的 CN residual、2-switch、interaction layer 都更像已有思想的组合或增量改造，不宜单独声称“基础算法首次提出”。
2. score-level routing 加上 frozen Stage B 是较有潜力的方法学点，但本次没有直接 routing baseline，尚未形成证据闭环。
3. 最有辨识度的是完整组合：条件 CN 残差化、受控结构反事实、分支 score 级路由、interaction 三态审计、冻结后的独立 probe。
4. 本次结果说明“预测性能”和“机制选择性”存在明显 trade-off：M2 的预测最好，但 routing selectivity 变差；M3 的部分机制最好，但不是全面改善。

因此创新点可以继续做，但当前不应表述为“已经证明创新有效”。更准确的定位是：

> 这是一个有潜力的链路预测机制可辨识框架；当前 Cora 实验验证了工程链路和部分机制现象，但尚未证明所有创新组件共同带来稳定、可泛化的客观收益。

## 10. 下一步必须做什么

### 10.1 先修正/增强分析，再扩数据集

1. 检查 `z_cn → degree` 的异常负 R²，确认是否为 probe 训练/验证/测试分布或目标尺度问题。
2. 将 probe seed 改为真正改变采样或模型随机性的重复，而不是 Ridge 中实际上不起作用的 seed。
3. 将 cross leakage 改为联合门槛：不能只要任一 probe 下降就算改善；至少要求主要 cross probe 不恶化。
4. 单独报告 M3 的 disabled identification 结果，不要让它走 audited interaction GO gate。

### 10.2 补齐决定性对照

必须增加：

- M4：residual + unrestricted；
- R0：关闭 score routing；
- R1：旧 latent intervention routing；
- R2：score routing + encoder low-lr；
- R3：当前 score routing + encoder frozen；
- CN `+1/-1/+2/-2`、degree 两端点正负方向；
- edit-count-matched random rewire。

### 10.3 最终确认标准

只有当后续实验同时满足以下条件，才建议把创新点写成“有效”：

- HeaRT MRR 或 macro/worst-group 指标在多个数据集上不下降；
- CN 与 degree 两类 routing selectivity 都不恶化，最好多数 seed 改善；
- target response 增加不是以 cross-sensitivity 增加为代价；
- 主要 cross probe 均不恶化，target-retention 保持；
- audited vs unrestricted 显示明确的性能—机制权衡；
- 结果在预注册配置和多数据集上重复出现。

## 11. 最终结论

本轮实验已经完成，但结论不是“创新点已被证实”，而是：

> M2 是当前预测性能最好的候选，M3 在部分机制选择性指标上最好，M1 处于两者之间；然而没有任何一个候选同时在预测、CN 路由、degree 路由、cross-sensitivity 和全部 leakage probe 上稳定胜出。因此当前最合理的决策是 `PIVOT_TO_CALIBRATION`：保留这条研究路线，先校准 probe 和 routing loss，补齐 M4/R0/R1/R2/R3 及完整干预对照，再进入多数据集正式确认。

本轮结果支持“研究方向可行”，不支持“创新点已经被客观证明有效”。

