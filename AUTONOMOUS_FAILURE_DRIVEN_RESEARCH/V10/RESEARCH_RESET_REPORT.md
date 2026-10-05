# Research Reset Report

状态：`NO_NEW_STRUCTURE_PROBLEM`

本轮关闭 V9 的 LPShift A/B 结构增强分支，未实现新的 GNN 模块。审计重点转向归纳式 / cold-start link prediction，先恢复公开协议，再用强基线和简单代理确认是否存在独立的信息瓶颈。

## 1. 历史失败映射

| 阶段 | 假设 / 方向 | 直接证据与结论 | 不可重复边界 | 尚未解决的问题 |
|---|---|---|---|---|
| V1 | 静态局部结构特征和局部路径统计能够形成独立收益 | Cora HeaRT 上最佳候选 R4-12 被简单 Proxy 在排序指标上击败；多种 degree/CN/residual/path 方向没有稳定增益 | 不再把 CN、degree、L3、路径计数、社区/边界等重新包装成新模块 | 真实分布偏移下，节点特征与拓扑是否出现可重复冲突 |
| V2 | PCDT 的目标条件传播能修正目标边表示 | seed 0 的 shuffled-eval 控制反而更高，F9 控制否定了目标对应机制 | 不再研究 target-conditioned message passing 的同类变体 | 需要先确认是否存在超出简单 edge score 的信息缺口 |
| V3 | CDPT 的跨深度张量交互优于单深度或普通融合 | Late-only test MRR 高于 CDPT；CiteSeer 仅有单 seed 局部信号；历史 test 选择偏差已记录 | 不再增加 attention/gate/更宽 hidden size 救 CDPT | 不把“多层表示融合”作为独立机制前提 |
| V4 | CDPT 机制可由 Early×Late 保持 | Early×Early 在五个 Cora validation seed 上压过 CDPT，固定随机算子具有竞争力 | CDPT family 关闭；不再改 decoder、loss 或融合 | 结构增益必须经过随机算子、参数匹配和简单代理共同排除 |
| V5 | T2WL-INC 能以共享中间节点 pair update 提供新表达能力 | 与 2-FWL / Local 2-FWL 的状态对象和更新模式发生核心碰撞，停止 GPU 实验 | 不再研究 pair-state、共享中间节点二阶传播的改名版本 | 需要避免已知 WL/局部 pair propagation 路线 |
| V6 | 三个网络内部候选可形成全新传播算子 | complement propagation、non-backtracking/cochain、learned topology residual 分别与 ECGN/UGCN、line graph/Hodge/SLRGNN、LEAP/CORE 等先行工作碰撞 | 不再从“补图、非回溯、拓扑残差/增强”直接生成候选 | 先从公开 benchmark 的真实失败场景反推问题 |
| V7–V8 | LPShift 分布偏移能暴露需要新结构的稳定缺陷 | LPShift 已恢复；官方 GCN、DCDLP、CN/AA/RA 协议可运行。V8 最终为 `BENCHMARK_READY_NO_GAP` | 不把 LPShift 的任何 rank drop 自动解释为结构缺口 | 需要区分 benchmark 协议错配、采样变化和真正表达瓶颈 |
| V9 | feature-only / topology-only 之外存在独立的 feature–topology interaction gap | FeatureCosine 或 RA 在若干设置已达到/超过 DCDLP；参数匹配融合没有稳定优势；最终 `NO_INDEPENDENT_GAP` | 不再继续修改融合模块、decoder、传播结构 | 需要换到定义清楚的归纳式任务，先做基线审计 |

## 2. 跨阶段失败的共同原因

这些失败不是简单的“模型容量不够”，而是研究流程中的可识别性问题：

1. 许多候选计算的有效输入已经被 CN、RA、degree、MLP 或已有 GNN 表达。模型变复杂并没有新增可辨识信息。
2. 仅有总体 MRR 或单个 seed 的提升不足以支持机制因果性；CDPT 的随机算子和单深度控制已经展示了这一点。
3. Cora HeaRT 的局部结构信号较强，复杂传播容易退化为已有统计量的平滑或重新加权。
4. 多次工作都暴露出 validation/test 任务不一致或历史 test 选择偏差的风险。若先看 test 再设计结构，后续的增益无法作为独立证据。
5. 文献碰撞往往发生在数学状态对象和传播规则层面，而不是模型名称层面；V5/V6 说明“换一个名字”不能构成创新。

## 3. 本轮归纳式审计问题

本轮选择公开的 NodeDup inductive split，使用 Cora 和 CiteSeer。它不是严格的零边冷启动：新节点占 10%，训练图只含 old–old train edges；测试包含 old–old、old–new 和 new–new 候选，推理图还包含部分已公开的 new-node context。这个边界在报告中保持原样，没有把它称为 strict zero-shot。

已完成：

- 官方 NodeDup 代码和数据生成逻辑审计；
- Cora、CiteSeer 的固定 split 恢复；
- Plain GraphSAGE 与官方 duplicated baseline，各数据集 3 个模型 seed；
- CN、RA、FeatureCosine 的 validation/test 描述性代理；
- test 未参与 checkpoint、超参数或问题选择。

## 4. 结论

发现了一个可重复的现象：旧节点 validation 与混合新节点 test 的任务分布不一致，且 degree-0/低 CN 子群在两个数据集上明显更难。但目前没有发现“强基线无法解释、且必须依靠新网络结构”的独立缺口：

- Plain GraphSAGE 在两个数据集的整体 test 表现都优于 NodeDup duplicated baseline；
- NodeDup 在 Cora validation Hits@20 较高，却在 test MRR/Hits@10 下降，说明 validation checkpoint 不能代表新节点泛化；
- CiteSeer 上 NodeDup validation 和 test 均下降；
- 低度子群的失败由简单难度分层、CN/RA/特征相似度和现有 GraphSAGE 共同解释，尚不能归因于缺失的传播机制。

因此，下一步不进入结构创新。若未来继续该方向，首先应建立 new-node validation 或严格 cold-start 的预注册协议，并在该协议下重新比较已有方法；这属于 benchmark/protocol 修复，不是当前已证实的新 GNN 方向。

