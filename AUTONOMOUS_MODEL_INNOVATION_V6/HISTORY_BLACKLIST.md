# DCDLP V6 历史复盘与永久创新黑名单

日期：2026-09-17  
范围：静态、同构、无向图链路预测；V6 不覆盖 V5 已提出的时间图问题转移。

## 1. 读取范围

已读取 V1–V5 的研究记录、候选账本、失败分析、机制对照、数据边界和最终决策文件，主要包括：

- `AUTONOMOUS_LP_RESEARCH/`
- `AUTONOMOUS_MODEL_INNOVATION_V2/`
- `AUTONOMOUS_MODEL_INNOVATION_V3/`
- `AUTONOMOUS_MODEL_INNOVATION_V4/`
- `AUTONOMOUS_MODEL_INNOVATION_V5/`

V1–V5 未被修改。V6 只在本目录写入审计交付物。

## 2. 永久黑名单

“黑名单”按数学对象和传播规则判断，而不是按候选名称判断。下表的 STOP 保留为不可重命名复活的方向。

| 方向 | 状态 | 证据与不可重试边界 |
|---|---|---|
| Degree/CN/Residual 解耦、MPLP-VC | 已实验失败 | 方差/置信度未稳定超过打乱控制；不得用新的分支名或标量特征重做。 |
| NCN-CNDP、OCN/CN 高阶变体 | 已实验或文献碰撞 | CN、CN 完成和高阶公共邻居已有直接先行工作；不能将邻居重加权当作独立网络传播。 |
| HL-GNN-PDG、普通 hop gate | 已实验失败 | gate collapse，且资源开销上升；禁止以 attention/gate 复救。 |
| CECG、L3、路径统计、exclusive-neighborhood 及 graphlet 统计 | 已实验失败/碰撞 | Cora 控制实验没有稳定排序收益；普通路径、CN、局部图模式已覆盖。 |
| 块割结构、非回溯路径 | 已实验失败/数学对象已知 | block-cut、Hashimoto/edge-incidence 家族已进入黑名单。 |
| 边界匹配、邻域扩展、角色对齐、谱特征、社区边界 | 已实验失败 | AUC 或特征探针的局部信号没有转化为稳定 MRR/AP/Hits；不得只换统计量。 |
| PCDT | 已实验失败 | shuffled evaluation 超过 aligned transport，目标对齐不是因果来源。 |
| CDPT | V4 机制证伪 | Cora 五 seed 中 CDPT 输给 Early×Early，且随机固定算子可复现/超过其收益；`MECHANISM_UNSUPPORTED`。 |
| T2WL-INC | 文献/源码碰撞 | `(i,k),(k,j) -> (i,j)` 正是 2-FWL/Local 2-FWL 的共享中间节点更新；没有 V5 GPU 实验。 |
| Temporal ONTM、PTALP、EAPU-LP | V5 分别 HOLD/碰撞/机制停止 | 它们改变问题为时间或 PU；不属于本轮静态同构图结构创新。 |

## 3. 历史证据边界

- V1 的静态 Cora HeaRT 搜索已记录 `NO_EXECUTABLE_IDEA_AFTER_EXHAUSTIVE_SEARCH`。早期正向 feature-only probe 不能升级为网络结构创新。
- V2-002 CDPT 的早期三 seed 正信号不能覆盖 V3/V4 的后续机制失败。
- V3/V4 中的 test 指标只可作为历史诊断；V6 不用历史 test 排序来选择候选。
- `AUTONOMOUS_MODEL_INNOVATION_V5/01_HISTORY_AND_BLACKLIST.md` 与 V4/V5 决策文件是本表的来源，所有失败结果均保留。

## 4. V6 no-retry 规则

不得对上述方向添加 attention、gate、loss、宽度、深度、训练轮数或重新命名后再报“新结构”。下一候选必须改变状态对象或传播规则，并且需要通过公式级碰撞审查、简单代理反证和目标边 masking 审查。

