# LPShift Data Protocol Audit

## 1. 数据来源

LPShift 使用 OGB `ogbl-collab` 的图和节点特征，再用官方 `gen_synth.py` 按启发式分数重新构造 train/validation/test。它不是 OGB 原始 temporal split，也不是普通随机 link split。OGB 的官方 link-prediction 说明见 [OGB link prediction](https://ogb.stanford.edu/docs/linkproppred/)。

`ogbl-collab` 图有 235,868 个节点、128 维节点特征，原始 message graph `edge_index` 形状为 `[2,2358104]`。原始 OGB 图的 canonical unique positive pair 数为 967,632。

## 2. Shift 定义

对候选边 `(u,v)` 计算 Common Neighbors：

`CN(u,v) = |N(u) ∩ N(v)|`。

官方默认命令是：

`python gen_synth.py --data_name ogbl-collab --valid_rat 1 --test_rat 2 --inverse`

在 `inverse` 模式下，低 CN 区域被推向 test，中间 CN 区域为 validation，高 CN 区域为 train；随后官方流程再执行节点范围过滤和最多 100,000 的中间候选上限。最终默认数据为：

| split | positive edges |
|---|---:|
| train | 1,697,336 |
| valid | 23,669 |
| test | 9,048 |

扩展审计使用 `(valid_rat=2,test_rat=4,inverse)`，数据为：valid 24,097、test 11,551。该扩展只用于检查 shift 难度，不用于挑选模型或阈值。

扩展组的 train/valid/test positive hash 分别为：

`9e876f00d0da73d7bb1229a9aee50ecf8ff9f1f3221eb932fbb9ec5f2c62c048`、
`f8ee3623440863545e162b38f4a6ff29cf35b8891ac49d81e8568e562895f42b`、
`cd34f4b513f4d581e64afa405f9df384031d7b5de960153af7b65317fc992ed9`。

## 3. Message-passing 信息边界

官方生成器从原始图中移除最终 valid/test 目标边，再保留其它原始 context edge 和 train edge。默认保存的训练 message graph 为 `[2,1,733,096]`，即 866,548 个 canonical context edges；train positive 的 canonical unique pair 数为 848,668，二者相差 17,880 个 context edges。这个差异很重要：直接把 `train_pos` 作为 DCDLP 的图会改变 LPShift 官方 GCN 的输入图。

默认审计确认：valid/test positives 不在保存的 message graph 中；train positives 全部存在于 message graph 中。

## 4. 负样本与候选组

默认官方文件：

- `heart_valid_samples.npy`: `[23669,250,2]`
- `heart_test_samples.npy`: `[9048,250,2]`

每个正边有 250 个按官方 HeaRT/LPShift 生成逻辑得到的困难候选。GCN 训练阶段并不使用这些固定负样本，而是按官方 `main_gnn.py` 随机生成 `torch.randint` 边；这与评测候选必须区分。

默认候选文件哈希：

| 文件 | SHA256 |
|---|---|
| valid negatives | `24ee3173d984974fd9c9fef4cb133a0e04722b6f8f28415b4fd7c2dafbf0f51d` |
| test negatives | `10bd6bd21860ffd4a9b3c525205bfc6919be607e7b3534e1b8d135f575d313d4` |

## 5. 泄漏与协议风险

审计结果：

- train/valid/test positive canonical overlap：均为 0；
- valid/test target positives 不在 message graph：是；
- valid negatives 进入 train message graph：0；
- test negatives 进入 train message graph：0；
- valid negatives 与原始 OGB positive graph 有 112 个 pair；test 有 36 个；
- valid negatives 与目标 split positive union 有 43 个 pair；test 有 3 个；
- flattened negative rows 中存在重复：valid 5,605，test 1,858。

扩展 `(2,4)` 同样没有 train/valid/test positive overlap，valid/test 不在 message graph，负样本进入 message graph 均为 0；其 negative 与原始 OGB positive overlap 为 valid 173、test 85，flattened duplicate rows 为 valid 5,549、test 2,217。完整字段保存在 `raw/lpshift_dataset_audit_2_4.json`。

这些不是本轮擅自删除的错误，而是官方生成结果的审计发现。为了保持官方协议，本轮没有过滤它们；后续若做“cleaned sensitivity”必须另建数据版本，不能把清理版结果冒充官方 LPShift。

当前没有发现训练阶段访问最终目标边的直接路径；但生成器在原始完整 OGB 图上计算启发式并保留其它 context edge，故论文级使用时必须明确“shift 构造器使用 full source graph，再删除目标边”的信息边界。
