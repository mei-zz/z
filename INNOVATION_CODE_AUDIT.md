# DCDLP 创新点—源码—证据边界审计

> 文档目的：严格按照当前仓库源码，说明五个创新点到底实现了什么、能够检验什么、不能检验什么，并给出判断创新性与客观效果提升所需的后续对照实验。
>
> 审计对象：`src/dcdlp/`、`scripts/run_phase2_selective_pipeline.py`、`scripts/run_posthoc_leakage_audit.py`、`scripts/analyze_phase2_selective_routing.py`。
>
> 结论先行：当前代码已经形成了一个有明确机制假设、可复现、可做配对干预审计的研究框架；但 M0–M3 只是 Cora 上的探索性机制筛选，不是足以支撑最终论文/正式确认性结论的完整实验。当前最有辨识度的不是某一个单独算子，而是“条件化 CN 表示 + 受控图干预 + 分数级路由 + 独立泄漏审计”的组合。要证明它既有创新性又有客观效果，仍需补齐路由基线、unrestricted 交互对照、多数据集确认和更严格的统计门槛。

## 1. 这项工作到底在研究什么

标准链路预测模型容易把多个相关但不同的结构因素混在一起：

1. 端点度数高，天然更容易拥有共同邻居；
2. 共同邻居数量高，可能只是度数造成的，也可能代表超出度数预期的局部闭合结构；
3. 模型的总分变化不一定来自它声称的分支，隐空间中的“分支分离”也不等于预测分数真的按预期响应；
4. 一个看似有效的分支可能只是在隐式记忆另一个分支的信息；
5. 普通随机负样本或普通测试指标无法证明上述机制真的被模型使用。

DCDLP 的核心研究问题不是单纯“MRR 是否更高”，而是：

> 在保持实验协议、模型容量和数据划分一致的条件下，能否把 degree、CN、residual 三种结构因素拆开，让对应结构干预主要改变对应分支的分数，同时不显著损害 HeaRT 困难负样本上的链路预测性能，并且在冻结模型后仍能通过独立 probe 观察到更少的交叉信息泄漏？

因此，最终证据应同时包含三层：

| 层次 | 要回答的问题 | 主要证据 |
|---|---|---|
| 预测效果 | 方法是否真的提升或至少不损害链路预测 | HeaRT official MRR、Hits、AUC/AP、macro/worst-group 指标 |
| 机制效果 | CN 干预是否主要作用于 CN 分支，degree 干预是否主要作用于 degree 分支 | before/after 分数差、routing selectivity、cross-sensitivity、interaction share |
| 表示审计 | 分支是否仍然可由另一种结构因素预测 | 冻结模型后的 5 类 post-hoc probe、验证集选超参、测试集只评分 |

## 2. 五个创新点的源码对照总表

| 创新点 | 当前代码中的真实实现 | 当前实验可直接检验的命题 | 当前不能直接宣称的命题 |
|---|---|---|---|
| 1. Conditional CN Residual | `ConditionalCNRegressor` 在训练划分的正边和固定训练负边上拟合 `log1p(CN)`；输入为端点度数的条件特征；CN 分支使用同宽 `selective_v1` 输入 | residual CN 是否比 raw CN 更有机制选择性，且 MRR 不明显下降 | residual 本身不是全新数学对象；也不能说模型完全没有 CN 原始信息，因为 CN 邻居集合的 pooled message 仍由共同邻居集合决定 |
| 2. Controlled Intervention | CN 使用度数向量保持不变的 2-switch；degree 使用保持目标端点 CN 集合不变的边转移；每次调用 validator | 在目标 pair 上，改变 CN 或 degree 是否引起预期的分数级响应 | 不是全图所有 pair 的 CN 集合都保持不变；当前 Phase 2 只跑目标测试边的 `+1` 干预，尚未覆盖完整 dose-response |
| 3. Score-Level Selective Routing | `score_routing_losses` 对分支分数差施加目标分支大于非目标分支的损失；routing 阶段冻结 NodeEncoder | 结构干预是否被导向目标分支分数 | M0–M3 没有“关闭 routing”或“旧隐向量 routing”基线，因此不能单独识别 score-level routing 的增益 |
| 4. Interaction Audit | `disabled/audited/unrestricted` 三态；audited 对 interaction share 和干预前后 interaction delta 加上限惩罚；disabled 将 interaction 分支精确置零并关闭参数梯度 | 禁用交互是否是有效识别对照；audited 是否在性能和交互份额间取得约束平衡 | 当前实际运行的 M0–M3 没有 M4 unrestricted；因此不能完成 audited vs unrestricted 的完整对照 |
| 5. Independent Post-hoc Leakage Audit | 冻结 checkpoint，另训 5 个 Ridge probe；验证集选 alpha，训练+验证重训，测试只评分 | residual CN/degree 分支之间的可预测泄漏是否下降，同时 target retention 是否保持 | 5 个 probe 是 5 个映射任务，不是 5 种完全不同的 probe 模型；Ridge 只能证明线性可预测性降低，不能证明所有非线性泄漏都消失 |

## 3. 创新点一：Conditional CN Residual

### 3.1 源码实现

相关代码：

- `src/dcdlp/data/pair_statistics.py`：`conditional_inputs`、`ConditionalCNRegressor`；
- `src/dcdlp/train.py`：`fit_training_cn_residualizer`；
- `src/dcdlp/models/branches.py`：`CNBranch`；
- `src/dcdlp/models/dcdlp.py`：模型组装；
- `scripts/run_phase2_selective_pipeline.py`：M0/M1/M2 的模式矩阵。

当前实际拟合不是只使用“训练正边”，而是：

```text
calibration_pairs = train_positive + fixed_train_negative(epoch=0)
target = log1p(CN)
condition = [log1p(degree_u), log1p(degree_v),
             log1p(degree_u * degree_v),
             abs(log1p(degree_u) - log1p(degree_v))]
residual = log1p(CN) - E_hat[log1p(CN) | endpoint degrees]
```

代码还明确记录 `fit_split=train`、`uses_valid_or_test=False`，并在校准前检查训练校准 pair 是否与 valid/test 重叠。因此“训练集拟合、验证/测试不参与残差器拟合”这一点实现得比较清楚。

### 3.2 等宽和参数控制是否成立

`CNBranch` 有两个 schema：`legacy` 和 `selective_v1`。当前 Phase 2 固定使用 `selective_v1`：

| 模式 | 显式 CN 输入 |
|---|---|
| raw | `[log1p(raw_CN), 0]` |
| residual | `[CN_residual, 0]` |
| raw_plus_residual | `[log1p(raw_CN), CN_residual]` |

三种模式的显式输入都为 2 维，后续 CN encoder 结构相同，因此“显式输入宽度和 CN 分支参数量一致”成立。M0/M1/M2 的总参数量也应相同，区别来自输入内容而不是层宽。

此外，当前 residual 模式没有把 `raw_log_cn` 或 `normalized_cn` 放进显式输入。这一点比旧的 `legacy` schema 更接近“residual 不偷渡 raw CN”的要求。

### 3.3 必须精确限定的地方

这里有一个不能忽略的概念边界：residual 模式虽然不输入 raw CN 标量，但 CN 分支仍然会：

```text
common = neighbors[u] ∩ neighbors[v]
pooled_sum / pooled_max = pooling(common-neighbor node messages)
```

因此 residual 模式不是“信息论意义上完全不含 CN”，而是“不把 raw CN 和 degree-normalized raw CN 作为显式统计量输入”。共同邻居集合本身仍然决定 pooled message 的数量和内容。论文中应该写成“去除显式 raw-CN 统计通道”或“显式条件残差化”，不要写成“完全消除了 CN 信息”。

另外，`ResidualBranch` 的名字容易造成歧义。它是由节点表示构造的第三个 learned branch，并不等于 `CNBranch` 中的 conditional CN residual feature。论文和图中应分别命名为：

- `CN residual feature`：条件 CN 残差；
- `residual branch`：独立的节点交互残差分支。

### 3.4 能支持的创新性判断

单独看，“用度数条件期望对 CN 做残差化”属于合理且有解释力的增量方法：它与 degree-normalized CN、Common Neighbors 等经典启发式存在明显亲缘关系。因此单独作为唯一创新点，创新性偏中等或偏弱，审稿人很可能要求说明与以下基线的差异：

- `CN / sqrt(degree_u * degree_v)` 等固定归一化；
- 线性或广义线性条件模型；
- 只输入 raw CN 的 branch；
- raw CN + residual；
- degree-matched 或 degree-stratified 的直接比较。

更有辨识度的地方是：该 residual 不是只作为一个额外 feature，而是被放进一个有参数量控制的分支矩阵，并与受控干预、分数级路由、post-hoc probe 组成一条完整的机制验证链。

### 3.5 当前 M0/M1/M2 能证明什么

- M0 vs M1：主要测试显式 raw CN 替换为条件 residual 后，预测性能和机制指标是否变化；这是创新点 1 的主比较。
- M2 vs M1：测试 residual 是否带来超过 raw+residual 的额外收益；如果 M2 更好，说明 residual 可能是互补信息；如果 M1 更好，说明 residual 可能具有更强的选择性或正则化作用。
- M0/M1/M2 都是 audited interaction、都开启 score routing、都冻结 routing 阶段 NodeEncoder。因此这三个比较不能分离 routing 或 audited 本身的贡献。

## 4. 创新点二：Controlled Intervention

### 4.1 CN 干预的约束

`src/dcdlp/interventions/cn_intervention.py` 的 `intervene_cn` 会：

1. 如有需要先移除目标边，防止目标 edge 泄漏；
2. 用 2-switch 候选搜索改变目标 pair 的共同邻居数；
3. 对 `+1/-1/+2/-2` 重复执行单步；
4. 通过 `validate_intervention` 检查完整 degree dictionary 不变；
5. 检查目标 pair 的 CN 差恰好等于 requested delta；
6. 检查编辑边数为 `2 * abs(delta)` 条移除和新增。

所以“CN 干预保留全体节点度数向量”在代码层面是真实约束，而不是只在统计意义上近似保留。

### 4.2 degree 干预的约束

`src/dcdlp/interventions/degree_intervention.py` 的 `intervene_degree` 通过边转移改变指定端点 `u` 或 `v` 的 degree，目标 pair 的共同邻居集合必须保持完全相等。validator 还检查：

- 指定端点 degree 差等于 requested delta；
- 目标 pair 的 CN set 完全相同；
- 编辑数量等于 `abs(delta)` 条移除和新增；
- 不添加 held-out positive，不添加 self-loop，不重复加边，不让目标端点变成孤立点。

这里必须把表述改得精确：degree 干预保持的是“目标 pair 的 CN 集合”，不是全图所有 pair 的 CN 集合。改变一条边会影响其他节点对的 CN，这是结构干预的自然副作用，也是为什么必须报告 coverage 和具体干预日志。

### 4.3 当前 Phase 2 实际运行的干预范围

虽然底层函数支持正负方向和幅度 1/2，但 `src/dcdlp/evaluate.py` 的 Phase 2 评测实际对每个测试正边最多取 100 个 pair，并只运行：

- `degree`: `degree_u +1`；
- `cn`: `CN +1`。

训练阶段也主要随机抽取这些在线干预用于损失计算。因而当前实验能检验“局部 +1 受控响应”，还不能完整检验：

- `+1` 与 `-1` 是否对称；
- `+1`、`+2` 的 dose-response 是否单调；
- 换成端点 `v` 是否得到相同结论；
- 不同编辑距离下是否仍保持路由选择性。

### 4.4 审计产物的优点和缺口

当前 evaluation 输出会记录：

- before/after 的 total、degree、CN、residual、interaction score；
- 每个分支的 delta 和 absolute delta；
- target response、cross response、routing selectivity、routing ratio；
- interaction share before/after 及 cap violation；
- pre/post degree；
- `cn_raw`、`cn_expected`、`cn_residual_feature` 的 before/after/delta；
- attempted、valid、missing、failure code 组成的 coverage。

底层每次调用都通过 validator，但 Phase 2 的 `evaluate.py` 行级 CSV 没有把 `EditLog.removed_edges` 和 `EditLog.added_edges` 完整写出；单独的 `build_intervention_cache` 能保存这些字段，但当前 Phase 2 pipeline 没有使用该 cache 作为主要产物。因此如果论文要求“每条干预可重放”，建议补充保存编辑边集合或 intervention cache hash。当前实现更准确的说法是“保存结构约束验证结果和预测前后差异”，而不是“完整保存每条图编辑细节”。

### 4.5 能支持的创新性判断

保度 2-switch 和保持局部 CN 的边转移本身并非全新图算法。创新价值主要来自它们被用于：

1. 对链路预测分支进行局部机制辨识；
2. 对 CN 与 degree 做方向相反的控制变量设计；
3. 在预测指标之外直接检查 score-level response；
4. 对干预失败率、覆盖率和 forbidden-edge 安全性进行显式记录。

因此应把它定位为“可验证的机制审计协议”或“面向链路预测分支归因的受控图干预框架”，不要把 2-switch 算法本身包装成核心原创算法。

## 5. 创新点三：Score-Level Selective Routing

### 5.1 当前代码的关键改变

`src/dcdlp/models/losses.py` 的 `score_routing_losses` 计算的是每个分支的分数差：

```text
delta_degree = |score_degree_cf - score_degree_orig|
delta_cn = |score_cn_cf - score_cn_orig|
delta_residual = |score_residual_cf - score_residual_orig|
delta_interaction = |score_interaction_cf - score_interaction_orig|
```

对于 CN 干预：

```text
target = delta_cn
cross = delta_degree + delta_residual + interaction_weight * delta_interaction
loss = ReLU(margin + cross - target) + target_floor_penalty
```

对于 degree 干预则交换 target 和 cross。也就是说，训练目标不是让 `z_original` 和 `z_counterfactual` 的距离满足关系，而是让最终 additive decoder 的分支 score response 满足关系。这一点与旧的 `intervention_losses` 明确不同。

### 5.2 Stage B 的冻结策略

`train_model` 在 `epoch == pretrain_epochs` 时调用 `_enter_routing_finetune_stage`。当前 Phase 2 配置为：

```text
pretrain_epochs = 5
routing_epochs = 5
score_routing_enabled = True
routing_finetune_encoder = "frozen"
lambda_score_route = 0.03
lambda_target_response = 0.03
target_floor_cn = target_floor_degree = 0.05
```

因此后 5 个 epoch 中 NodeEncoder 参数 `requires_grad=False`，encoder optimizer group 的学习率变为 0；branch heads、interaction 参数和 bias 仍可训练。当前 pipeline 还把旧的 `lambda_inv`、`lambda_route`、`lambda_adv`、`lambda_orth`、`lambda_degrob` 设为 0，所以 M0–M3 的路由识别主要来自 score-level routing，而不是旧 latent intervention loss 或 adversarial loss。

### 5.3 当前实验不能隔离的贡献

M0–M3 全部使用：

- `score_routing_enabled=True`；
- 相同的 routing loss 权重；
- 相同的 frozen encoder 策略。

所以 M0 vs M1/M2/M3 可以回答“在 score-level routing 框架内，CN 表示/interaction 改变后机制指标如何变化”，但不能回答“score-level routing 相比不做 routing 或旧 latent routing 是否更好”。

要验证创新点 3，至少应增加：

| 对照 | 说明 |
|---|---|
| R0 | 完全关闭 score routing，只保留 link prediction + audited interaction |
| R1 | 旧的 latent `intervention_losses`，不使用 score-level loss |
| R2 | score-level routing，但 encoder low-lr 而不是 frozen |
| R3 | score-level routing + frozen encoder，即当前方案 |

这四者应在相同 CN 模式、相同 interaction mode、相同随机种子下成组比较。

### 5.4 能支持的创新性判断

“把结构干预目标直接施加到分支分数差，而不是隐向量距离”是五个点中相对更容易形成方法学差异的部分，因为它直接对齐最终预测解释层。但它能否成为有说服力的创新，取决于实验是否显示：

- score-level routing 比 latent routing 更少 cross-sensitivity；
- 在相同 MRR 下 target response 更强；
- 冻结 encoder 后仍能完成路由，说明不是靠重写整个表征空间取得的；
- 与简单 branch score regularizer 或 post-hoc 分解相比有额外收益。

没有这些直接对照，目前只能称为“已实现的机制训练设计”，还不能称为“已被验证的新方法”。

## 6. 创新点四：Interaction Audit

### 6.1 三种状态的实际含义

`src/dcdlp/models/dcdlp.py` 中 interaction score 为：

```text
score_interaction = interaction_scale * (z_degree @ interaction * z_cn).sum / sqrt(dim)
```

三种状态分别是：

| 状态 | forward 行为 | 正则行为 | 研究含义 |
|---|---|---|---|
| disabled | `score_interaction` 精确为零；interaction matrix 和 scale 无梯度 | 不加 interaction 正则 | 识别对照，测试不依赖交互项时的结果 |
| audited | 允许 interaction，但训练惩罚 `share > 0.20` 和干预前后 interaction delta 超过 `0.20` | 有 share/delta 惩罚 | 受控交互 |
| unrestricted | 允许 interaction，不加上述审计惩罚 | 无正则 | 性能控制组，测试自由交互是否提高预测但破坏可解释性 |

disabled 的实现相对干净：不仅输出被置零，参数也被 `requires_grad_(False)`，因此它不是“只在报告阶段忽略 interaction”，而是训练图中也不会通过 interaction 路径获得梯度。

### 6.2 audited 惩罚的准确含义

`interaction_share` 定义为：

```text
abs(interaction score)
--------------------------------------------
abs(degree)+abs(CN)+abs(residual)+abs(interaction)
```

audited 只对超过 cap 的部分用 ReLU 惩罚；它不是把 interaction share 硬裁剪到 0.20，也不是保证每一条边都不超过 0.20。delta cap 也同样是软惩罚。报告时必须同时给：mean、median、P90、cap violation rate，而不是只给均值。

### 6.3 当前 M0–M3 对 innovation 4 的覆盖范围

Phase 2 的模型矩阵在代码中定义了 M4：

```text
M4 = residual + unrestricted
```

但当前启动命令是 M0、M1、M2、M3，未包含 M4。因此已经跑的实验只包含：

- M0/M1/M2：audited；
- M3：disabled。

这足以做“disabled 识别对照”，不足以做“audited 相对于 unrestricted 的控制收益”判断。并且 `analyze_phase2_selective_routing.py` 当前 decision gate 的 `interaction_ok` 明确要求 candidate 是 audited 且 interaction share 非零、均值不超过 cap。因此 M3 作为 disabled identification control 不适合直接套用同一 GO gate；即使 M3 的实验结果合理，也会因为 `modes_audited=False` 而无法通过该项。这是分析器设计上的语义不一致，应在最终统计中把 M3 作为单独的识别对照报告，而不是和 M1/M2 使用同一决策状态解释。

### 6.4 能支持的创新性判断

三态交互控制的价值在于把“无交互”“受控交互”“自由交互”分开，形成可识别的性能—机制权衡。单独的乘积交互层并不新；比较有价值的是：

- share 被定义在最终分支分数层；
- interaction delta 被纳入干预审计；
- disabled 是精确零、无梯度的识别对照；
- unrestricted 作为性能控制而不是被误当作主方法。

但这一点的证据链必须包含 M4，否则只能说“代码支持 audited/unrestricted 三态”，不能说“实验验证了 audited 的必要性”。

## 7. 创新点五：Independent Post-hoc Leakage Audit

### 7.1 实际 probe 任务

`scripts/run_posthoc_leakage_audit.py` 中实际定义了五个映射：

| Probe | 表示 | 目标 | 角色 |
|---|---|---|---|
| `z_cn_to_degree` | `z_cn` | degree score | cross leakage |
| `z_residual_to_degree` | `z_residual` | degree score | cross leakage |
| `z_degree_to_cn_residual` | `z_degree` | conditional CN residual | cross leakage |
| `z_degree_to_degree` | `z_degree` | degree score | target retention |
| `z_cn_to_cn_residual` | `z_cn` | conditional CN residual | target retention |

所有 probe 当前都使用 `StandardScaler + Ridge`，在验证集上选择 alpha，在 train+valid 上重训，在 test 上只计算 R²、MAE、Spearman。checkpoint 加载后所有模型参数被冻结，metadata 记录 `model_frozen=True` 和 `test_not_used_for_selection=True`。

### 7.2 “独立”的准确解释

这个 post-hoc audit 相对于训练期 adversarial probe 的独立性是成立的：

- 不参与 checkpoint 训练梯度；
- 不更新 DCDLP；
- 不是训练时的 `lambda_adv`；
- 有独立的 probe seed；
- 验证集选超参，测试集只打分。

但它不是“完全独立数据集”：它仍然使用同一个 Cora 数据划分、同一个 train graph、同一个冻结 checkpoint。论文中应写为“independent post-hoc frozen-checkpoint audit”，而不要写成“independent external validation”。

另外，5 类是 5 个表示—目标映射，不是 5 种模型族；Ridge 主要测试线性可预测泄漏。如果要声称“交叉信息被消除”，还需要至少增加一个容量受控的非线性 probe 或 mutual-information proxy，并报告 probe capacity sensitivity。

## 8. 当前 Step 11/Step 12 的实验身份

### 8.1 Step 11 实际做什么

`run_phase2_selective_pipeline.py` 的 Cora 配置是：

```text
训练负样本：uniform
评测负样本：HeaRT official grouped candidates
每个模型：5 个 pretrain epoch + 5 个 routing epoch
hidden_dim=128, branch_dim=64, num_layers=2, dropout=0.3
score routing：开启
Stage B encoder：frozen
probe：每个 split 最多 512 pair，probe seed=0,1,2
干预评测：最多 100 个 test positive，每类 +1
```

模型矩阵：

| 模型 | CN 模式 | Interaction | 当前用途 |
|---|---|---|---|
| M0 | raw | audited | baseline |
| M1 | residual | audited | innovation 1 主候选 |
| M2 | raw+residual | audited | residual 互补性/额外增益 |
| M3 | residual | disabled | innovation 4 识别对照 |
| M4 | residual | unrestricted | 代码已定义，但本轮未运行 |

HeaRT official candidates 缺失时，`grouped_official_negatives` 和 `evaluate_checkpoint` 会直接报错，不会用 uniform 顶替。这使评测协议比普通 pilot 更可信。

### 8.2 Step 12 实际做什么

`analyze_phase2_selective_routing.py` 按 `(dataset, seed)` 配对，并检查：

- dataset、seed、train/eval protocol 一致；
- split hash、test positive hash、candidate hash 一致；
- prediction positive pair 顺序一致；
- 预测指标 delta；
- 干预机制指标 delta；
- probe 指标 delta。

当前 decision gate 的主要规则包括：

- mean MRR 相对下降不超过 1%；
- CN 和 degree 两类 routing selectivity 均值为正，且多数 seed 改善；
- target response 均值不下降；
- cross-sensitivity 或 cross-leakage probe R² 至少一类改善；
- candidate 必须是 audited 且 interaction share 均值在 cap 内；
- 所有 5-seed 统计标记为 `exploratory_5_seed_screening`，`confirmatory_claim_allowed=False`。

因此 Step 12 是一个冻结门槛式筛选器，不是最终显著性检验器。它可以决定“哪条路线值得继续”，不能仅凭 `GO_TO_MULTI_DATASET_CONFIRMATION` 写成“创新点已被证实”。

### 8.3 分析器当前的三个解释风险

1. `cross_sensitivity` 或 probe R² 只要有一类改善就可满足 `support_ok`，缺少多重指标联合门槛。
2. probe 改善使用“aggregate cross R² 中任意一项 `<0`”，没有要求效应量超过最小重要差异，也没有把置信区间纳入 gate。
3. interaction gate 不检查 delta-cap violation rate，且 M3 disabled 天然无法通过“audited candidate”条件。

所以 decision JSON 很有用，但它是工程筛选逻辑，不应被当作统计证明。正式分析时应另外输出预先指定的主指标、最小效果阈值、置信区间和多重比较处理。

## 9. 当前实验能验证哪些创新点

### 可以部分验证

**创新点 1：可以做第一轮验证。**

M0/M1/M2 具备相同 selective_v1 CN 输入宽度，数据和训练/评测协议一致，能够观察 residual 替换 raw CN 后的 prediction、routing、probe 变化。它是当前矩阵最完整的一条比较链。

**创新点 2：可以做局部 +1 干预验证。**

CN 和 degree 的结构约束、validator、before/after/delta/coverage 都有实现，能检验目标 pair 上的局部结构因果响应。但范围还不是完整干预实验。

**创新点 4：可以做 disabled identification control。**

M1 vs M3 能观察在相同 residual CN、相同 routing 配置下，禁用 interaction 后性能和机制指标怎么变。它可以回答“交互项是否带来额外响应/泄漏/性能权衡”。

**创新点 5：可以做冻结后独立线性泄漏审计。**

5 个 probe 的数据流和选择流程符合 post-hoc frozen-checkpoint audit 的定义。

### 当前不能完整验证

**创新点 3 不能被 M0–M3 单独识别。**

因为所有 M0–M3 都使用 score-level routing，没有 no-routing 或 latent-routing 对照。当前只能说“在已开启 score routing 时，不同 CN/interaction 配置的机制表现不同”。

**创新点 4 不能完成 audited vs unrestricted 比较。**

因为本轮没有 M4。M3 只能证明 disabled 的识别控制，不足以证明 audited 比 unrestricted 更好。

**五个创新点的整体有效性尚未被证明。**

目前仍没有结果层面的 paired delta、置信区间、跨数据集复现和足够种子数量的确认性证据；代码结构完整不等于实验结论成立。

## 10. 创新性是否足够：基于源码的客观判断

### 10.1 单点创新性

| 单点 | 初步创新性判断 | 主要原因 |
|---|---|---|
| 条件 CN residual | 中等偏增量 | residualization 合理，但与度数归一化 CN、条件校准、统计残差等已有思想相近 |
| 2-switch / CN-set-preserving intervention | 中等偏增量 | 图编辑本身不新，价值在于用于分支级机制识别和严格审计 |
| score-level routing | 中等，有潜力成为核心方法点 | 直接把干预目标施加到分支 score response，并冻结 encoder；需要直接 baseline 才能成立 |
| audited interaction | 中等偏增量 | 交互层常见，三态控制和 share/delta audit 提升了可识别性；必须运行 unrestricted |
| post-hoc leakage audit | 方法学贡献潜力较大，但偏 protocol | 独立冻结后 probe、验证选参、测试只评分是好的审计设计；需要证明比训练期 probe 更能发现问题 |
| 五点组合 | 中等偏上，取决于实验与相关工作 | 单点都不一定足够新，但组合形成了结构因素归因—受控干预—分数路由—冻结审计闭环 |

### 10.2 应该怎样表述创新

比较稳妥的主张是：

> 提出一个面向链路预测的机制可辨识框架：先对 CN 做条件残差化，再用保持互补结构量不变的图干预构造局部 counterfactual，直接在分支 score 层训练选择性路由，并用冻结 checkpoint 后的独立 probe 审计交叉泄漏。

不建议现在就表述为：

- “首次提出 CN residual”；
- “完全消除了 CN 与 degree 的耦合”；
- “证明了因果关系”；
- “五个创新点均显著提升性能”；
- “probe 低 R² 就证明没有非线性泄漏”。

真正的论文新颖性仍需和相关工作做系统比对；仅凭本地源码，能够判断实现差异和实验可辨识性，不能单独完成“领域首次”的文献新颖性判定。

## 11. 是否能客观证明“有效果提升”

答案是：**实验设计具备客观检验能力，但当前 M0–M3 尚不能预先保证会有提升，也不能在结果出来前把提升写成事实。**

### 11.1 需要同时看的四类结果

| 结果维度 | “有效”应观察到什么 | 不能只看什么 |
|---|---|---|
| 预测 | MRR/Hits/AUC/AP 不显著下降，最好 MRR 或 worst-group/macro 指标改善 | 只看平均 MRR |
| 目标路由 | CN 干预时 CN score response 上升；degree 干预时 degree score response 上升 | 只看 total logit 变化 |
| 交叉敏感性 | 非目标分支和 interaction response 下降，或至少不恶化 | 只看 target response 增加 |
| 泄漏 | cross-leakage probe R²/相关性下降，target-retention probe 不明显下降 | 只看一项 probe |

一个可信的正结果应类似于：

```text
M1 相比 M0：
MRR 下降不超过预设容忍区间，最好 macro/worst-group 不下降；
CN/degree 两类 routing selectivity 在多数 seed 上提升；
cross-sensitivity 至少一个预注册主指标下降且置信区间支持方向；
cross-leakage probe 下降，target-retention 不同步崩溃；
干预 coverage 足够且不是只在容易构造的 pair 上有效。
```

### 11.2 结果解释矩阵

| 结果 | 应如何解释 |
|---|---|
| MRR ↑、routing ↑、leakage ↓ | 最强的正向信号，值得进入多数据集确认 |
| MRR ≈、routing ↑、leakage ↓ | 机制改进成立，即使不是预测性能提升，也可作为可解释性/可控性贡献 |
| MRR ↑、routing ≈、leakage ≈ | 可能只是普通性能收益，不能证明五个机制创新 |
| MRR ↓、routing ↑、leakage ↓ | 方法有机制价值但存在性能代价，需转向 calibration/pareto 分析，不能宣称普遍提升 |
| MRR ↑、routing ↓ 或 leakage ↑ | 可能是交互或 shortcut 提升了预测，创新机制未被支持 |
| 只有单个 seed 或单个 probe 改善 | 只能作探索性现象，不能形成结论 |

## 12. 正式确认实验前必须补齐的对照

### 12.1 用于验证 CN residual

至少增加：

1. degree-normalized CN；
2. linear/GAM residualizer；
3. raw CN、residual CN、raw+residual 的等宽比较；
4. degree-stratified 或 degree-matched 结果；
5. residualizer 的 out-of-sample calibration 误差；
6. 检查 CN pooled message 是否成为 raw CN 的隐式替代通道。

### 12.2 用于验证 controlled intervention

至少增加：

1. CN `+1/-1/+2/-2`；
2. degree 对 `u/v` 的正负变化；
3. edit-count-matched unconstrained random rewire；
4. 按可构造性/coverage 分层报告；
5. 把 removed/added edges、validator 结果、前后结构 hash 写入审计产物；
6. 报告干预对目标 pair 和非目标 pair 的副作用边界。

### 12.3 用于验证 score-level routing

增加 R0/R1/R2/R3：

```text
R0 = no routing
R1 = latent intervention routing
R2 = score routing + encoder low-lr
R3 = score routing + encoder frozen（当前）
```

固定同一个 CN mode 和 interaction mode，使用同一组 intervention pair，才能把 score-level routing 本身的贡献从 CN residual 与 interaction 中分离出来。

### 12.4 用于验证 interaction audit

至少运行：

```text
M3 = residual + disabled
M1 = residual + audited
M4 = residual + unrestricted
```

并比较：

- MRR/Hits；
- mean/P90 interaction share；
- share cap violation rate；
- intervention 前后 interaction delta；
- cross-sensitivity 和 probe leakage；
- 是否存在“unrestricted 性能更高但机制更差”的明确 trade-off。

### 12.5 用于验证 post-hoc audit

建议增加：

- 一个容量受控的非线性 probe；
- permutation/null probe；
- 不同 probe seed 和不同 pair sample seed；
- probe capacity sensitivity；
- 原始 z、标准化 z、branch score 三种输入的审计对照；
- 明确将 target retention 作为不可牺牲的约束，而不是只追求 cross R² 下降。

## 13. 建议的正式实验分层

### Phase A：当前 Cora 5-seed screening

目的：筛掉明显失败的路线，比较 M0/M1/M2/M3 的机制方向。输出只能叫 exploratory screening。

### Phase B：机制识别补实验

在 Cora 上补齐：

- M4 unrestricted；
- R0/R1/R2/R3 routing 对照；
- 完整正负 dose-response；
- random-rewire control；
- 更完整的 intervention log。

目的：证明每个机制组件的独立增益，而不是只证明一个大模型结果。

### Phase C：多数据集确认

将冻结后的配置和决策门槛迁移到至少 2–3 个数据集，保持：

- 预先固定的模型配置；
- 官方困难负样本；
- 同一统计报告模板；
- 不在测试集选择超参；
- 报告 seed-level paired effect、CI、效应量和失败 coverage。

只有 Phase C 才适合写“方法在多个数据集上稳定改善/保持预测性能并提高机制选择性”。

## 14. 最终判断

### 关于创新性

当前创新性不是“某一个完全前所未有的算子”，而是一个较完整的、面向可辨识链路预测机制的组合框架。最值得强化的主线是：

```text
conditional CN residual
        ↓
controlled structural counterfactual
        ↓
score-level selective routing
        ↓
audited interaction
        ↓
independent frozen-checkpoint leakage audit
```

如果补齐直接 routing baseline、M4 unrestricted、干预对照并在多数据集上复现，这个组合有机会形成有说服力的方法学贡献。以当前 M0–M3 的范围，创新性可以作为“有潜力、尚未完全坐实”，不宜写成已经充分证明。

### 关于客观效果提升

当前实验能够客观测量效果，但是否提升必须等结果出来后依据 paired delta、置信区间、seed 稳定性、coverage 和 probe trade-off 判断。最理想的证据不是单独 MRR 上升，而是：

> 在 HeaRT official 困难负样本上的预测性能不下降或改善，同时 CN/degree 受控干预显示更强的目标分支响应、更低的非目标响应和更低的独立 cross-leakage，并且这一现象在多个 seed/数据集重复出现。

当前最准确的研究状态表述是：

> 代码已经实现了五个创新点的大部分机制组件，并正在通过 Cora 5-seed M0–M3 做第一阶段探索性筛选；实验尚未完成创新性和普遍效果的确认，尤其缺少 score-routing 基线和 unrestricted interaction 对照。

## 15. 建议在论文/组会中使用的简短版本

> 本工作提出一个面向链路预测的结构机制可辨识框架。方法首先在训练划分上估计给定端点度数条件下的共同邻居期望，并将 CN 分支输入改为条件残差；随后通过度数保持的 CN 2-switch 和目标 pair 的 CN-set-preserving degree intervention 构造受控结构反事实；在模型训练中，路由损失直接作用于分支 score response，并在第二阶段冻结节点编码器；同时将 degree–CN interaction 设为 disabled/audited/unrestricted 三态，并在冻结 checkpoint 后使用独立的验证选参、测试评分 probe 审计交叉泄漏。当前 Cora M0–M3 只属于探索性机制筛选，尚需 no-routing/latent-routing、unrestricted interaction 和多数据集实验，才能支持确认性创新与效果结论。

