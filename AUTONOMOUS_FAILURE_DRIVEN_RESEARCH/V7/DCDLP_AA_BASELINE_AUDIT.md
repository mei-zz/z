# DCDLP and AA/CN/RA Baseline Audit

## 1. 历史 Cora HeaRT 对照

历史固定协议的 Cora validation MRR 为：

| model | validation MRR |
|---|---:|
| DCDLP Parent, seeds 0--2 mean ± SD | `0.09958806 ± 0.00888892` |
| CN | `0.11612312` |
| Adamic--Adar | `0.13417046` |
| Resource Allocation | `0.13236648` |

因此 AA 高于 Parent `+0.03458240`，CN 高于 Parent `+0.01653505`。后续任何 LPShift 结构实验都必须把 AA/RA/CN 当作竞争基线，不能只与 Parent 比较。

## 2. LPShift 官方候选上的固定启发式

下面的结果使用官方保存的 message graph、正边和 250 个候选负边，采用官方 `eval.py` 的 optimistic/pessimistic average rank。没有重新采样负边。

### 默认 `(1,2)`

| heuristic | valid MRR | valid Hits@10 | test MRR | test Hits@10 |
|---|---:|---:|---:|---:|
| CN | 0.3845 | 0.4329 | 0.0079 | 0.0000 |
| AA | 0.4026 | 0.4329 | 0.0079 | 0.0000 |
| RA | 0.4057 | 0.4329 | 0.0079 | 0.0000 |
| PA | 0.0391 | 0.0772 | 0.0399 | 0.0809 |

### 扩展 `(2,4)`

| heuristic | valid MRR | valid Hits@10 | test MRR | test Hits@10 |
|---|---:|---:|---:|---:|
| CN | 0.8638 | 0.9169 | 0.2991 | 0.3409 |
| AA | 0.8866 | 0.9169 | 0.3150 | 0.3409 |
| RA | 0.8866 | 0.9169 | 0.3176 | 0.3409 |
| PA | 0.0600 | 0.1356 | 0.0592 | 0.1281 |

这两组显示：LPShift 的 shift 强度和候选构造会显著改变启发式排名；默认 test 的低 CN 区域对 CN/AA/RA 极难，而 `(2,4)` 的 test 组不同。不能只用一个阈值下的 test 数字提出“普遍 GNN 失败”或“启发式失败”。

## 3. DCDLP 是否能合法支持 LPShift

当前 DCDLP 代码可以读取已准备好的 `processed/*.npz` 或官方 OGB/小型 HeaRT 数据，但不能直接识别 `ogbl-collab_CN_2_1_0_seed1Dataset` 这种 LPShift 自定义目录。若直接传入原始 `ogbl-collab`，loader 会走 OGB 原生 split，改变任务定义；这条路径不能使用。

即使建立 adapter，也必须同时保留：

1. 官方 message-passing graph 中额外的 17,880 个 context edges；
2. 正边的原始行顺序；
3. `[N,250,2]` 的 grouped negatives、重复候选及官方 false-negative 风险；
4. target-edge masking 规则；
5. 官方训练负样本和 DCDLP 自己的 uniform/degree-corrected 训练负样本差异。

现有 `GraphDataset.train_graph()` 只由 `train_pos` 构造图，因此直接复用会丢掉官方 message graph 的额外 context edges。为“跑通”而静默删除或补入这些边都会改变 LPShift 协议。本轮没有执行 DCDLP LPShift 训练，也没有把任何 DCDLP 数字冒充官方结果。

## 4. 审计结论

AA/CN/RA 已合法完成固定代理审计；DCDLP 的 LPShift 训练状态是 `NOT_RUN_PROTOCOL_MISMATCH`，不是训练失败。下一轮若要比较 DCDLP，第一步必须是 protocol-preserving adapter 和独立 masking 单测，而不是改模型。

