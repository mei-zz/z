# Inductive Literature Audit

本报告用于确定研究边界和碰撞风险，不宣称穷尽 2026 年全部文献，也不把“未检索到同名方法”当作创新证明。

## 1. 任务定义必须先分开

归纳式链路预测至少包含四类不同问题：

1. **semi-inductive / production split**：训练期间没有使用新节点的标签，但推理图可能已经暴露部分新节点 context edges；
2. **strict cold-start**：新节点没有训练期连接，主要依靠节点特征或外部属性；
3. **fully inductive**：新的节点、边或关系在新图中同时出现；
4. **temporal inductive**：按时间预测未来边，候选和历史交互具有时间顺序。

不同定义会改变 message graph、负样本、候选集合和可用信息，不能把它们的结果直接合并。

## 2. 重点工作与具体差异

| 工作 | 年份 / 来源 | 状态对象和核心计算 | 与当前审计的关系 |
|---|---|---|---|
| **Node Duplication Improves Cold-start Link Prediction** | 2024, [arXiv](https://arxiv.org/abs/2402.09711)；[官方代码](https://github.com/snap-research/NodeDup) | 对孤立/低度节点做 duplication，并添加 duplicate correspondence edges；在 inductive split 上测试低度/新节点 | 与本轮最直接相关。它已经代表“通过节点复制修复 cold-start”的强先行方向；本轮复现实验没有得到稳定收益，因此不能把同类 duplication 再命名为新结构。 |
| **Illinois Graph Benchmark (IGB)** | 公开 benchmark，[官方代码与下载](https://github.com/IllinoisGraphBenchmark/IGB-Datasets) | 大规模 homogeneous/heterogeneous 图，支持 tiny/small/medium/large 等规模；不是单一模型 | 可作为更大规模归纳式/工业图验证入口。tiny 约 0.36 GB 可下载，但 full IGB 不属于当前低成本实验。 |
| **LEAP** | 2025, [arXiv](https://arxiv.org/abs/2503.03331)；[官方代码](https://github.com/AhmedESamy/LEAP/) | Learnable topology augmentation，为新节点/新边构造可学习拓扑上下文 | 与 V6 的 learned topology residual/augmentation 路线发生直接碰撞；本轮禁止重新提出 topology augmentation 变体。 |
| **DyTAG** | NeurIPS 2024 Datasets and Benchmarks， [官方论文 PDF](https://proceedings.neurips.cc/paper_files/paper/2024/file/a65d054a407f94c34ecfb598fb540a0d-Paper-Datasets_and_Benchmarks_Track.pdf) | 动态图未来链接预测；按时间切分，新节点出现后进行 destination retrieval，候选通常为 1000 个节点；基线包括 JODIE、DyRep、TGAT、CAWN、TCL、GraphMixer、DyGFormer | 这是清晰的 temporal inductive benchmark，但与当前静态同构 Cora/CiteSeer 不同。若转向该方向，必须接受时间状态和历史采样，不应把静态 DCDLP 直接迁移后声称同一问题。 |
| **FnF-TG** | ACL Findings 2025，[官方论文](https://aclanthology.org/2025.findings-acl.615/) | fully inductive text-attributed KG；通过 ego-graph 和文本信息处理 unseen entities/relations | 任务对象是文本知识图谱，不是当前静态无向同构图；代码/数据成本和问题定义均不同，不能作为当前低成本结构候选。 |
| **HYPER** | ICLR 2026 方向，[官方代码](https://github.com/HxyScotthuang/HYPER) | hypergraph inductive link prediction，状态对象扩展到超边/高阶关系 | 是新的任务空间而非本轮可直接复用的普通图问题；规模和依赖不适合在未确认 gap 前进入。 |
| **ILPC 2022** | [官方仓库](https://github.com/pykeen/ilpc2022) | 归纳式知识图谱 link prediction，含实体/关系归纳设定 | 公开且可复现，但属于 typed KG；不能与 Cora/CiteSeer 静态无向图指标直接比较。 |

## 3. 不能重复的结构路线

- NodeDup 的 duplication / correspondence-edge 思路不能作为新候选的起点。
- LEAP/CORE 已覆盖 learned topology augmentation / residual topology construction；不能把它改写成“可学习邻域补边”。
- V5 的 shared-middle pair propagation 已与 2-FWL/Local 2-FWL 碰撞。
- V2/V3/V4 的 target-conditioned、cross-depth、ordinary fusion 机制已经被历史控制实验否定或削弱。

## 4. 文献审计结论

文献确实表明 inductive LP 仍然活跃，且困难集中在新节点、部分历史 context、时间采样和文本/关系属性上。但这只能证明问题空间存在，不证明当前已有一个可独立命名的新 GNN 结构。

当前最可靠的研究信号不是“缺少某个传播算子”，而是：NodeDup 官方 validation 设计与 test 的 new-node composition 存在任务错配。该信号首先应通过 new-node validation、严格冷启动和更多公开 benchmark 验证；在此之前不应开发结构。

