# V12 Literature and Collision Audit

审计日期：2026-09-18。检索范围：2022–2026 年公开论文、会议页面、arXiv 原文和官方代码；重点覆盖 inductive / semi-inductive link prediction、distribution shift validation、checkpoint/model selection 和 link-prediction benchmarking。

## 1. 核心判断

V12 所称的 **Task-Aligned Model Selection for Inductive Link Prediction** 的核心规则是：把 validation 的任务组成改成接近部署/test 的任务组成，并据此选择 checkpoint；M2 进一步使用 old–old 与 new-node validation MRR 的预先固定加权。

这个核心思想已经被已有工作覆盖，虽然没有检索到完全相同的 NodeDup repaired split 和 0.5/0.5 公式。因此不能把本轮规则称为独立的模型选择算法，也不能把“未找到同一实现”当成全球未发表证明。结论：`NOVELTY_KILL`。

## 2. 主要先行工作

| 工作 | 年份 / venue | 已有任务或方法 | 与 V12 的碰撞结论 |
|---|---|---|---|
| **Node Duplication Improves Cold-start Link Prediction** | 2024, arXiv；[官方论文](https://arxiv.org/abs/2402.09711)，[官方代码](https://github.com/snap-research/NodeDup) | 研究低度/冷启动节点，使用 NodeDup augmentation；仓库明确提供 production/inductive 脚本 | 直接覆盖当前 benchmark、任务和强 baseline；V12 不是新的 inductive LP 模型。 |
| **A Benchmark for Semi-Inductive Link Prediction in Knowledge Graphs** | 2023, arXiv；[论文原文](https://arxiv.org/abs/2310.11917)，代码链接见论文 | 明确区分 transductive、k-shot、0-shot；控制 unseen entity 的 context 和 long-tail 分布 | 说明“新节点任务组成、可用 context 和 split”本身就是 benchmark 设计问题；V12 的任务对齐属于协议修复范式。 |
| **Evaluating Graph Neural Networks for Link Prediction: Current Pitfalls and New Benchmarking** | 2023, NeurIPS Datasets and Benchmarks；[官方页面](https://proceedings.neurips.cc/paper_files/paper/2023/hash/0be50b4590f1c5fdf4c8feddd63c4f67-Abstract-Datasets_and_Benchmarks.html)，[论文 PDF](https://papers.nips.cc/paper_files/paper/2023/file/0be50b4590f1c5fdf4c8feddd63c4f67-Paper-Datasets_and_Benchmarks.pdf) | 系统指出 split、指标和 easy negative 等 link-prediction 评测陷阱，并用 HeaRT hard negatives 改善评测现实性 | 直接覆盖“链接预测需要任务/候选/指标对齐”的评测论证；V12 是该原则在 NodeDup 上的具体审计，而不是新的结构或通用算法。 |
| **Towards Optimization and Model Selection for Domain Generalization: A Mixup-guided Solution** | 2023, KDD'23 Workshop；[PMLR 页面](https://proceedings.mlr.press/v218/lu23a.html)，[PDF](https://proceedings.mlr.press/v218/lu23a/lu23a.pdf) | 明确研究 model selection under distribution shift，并生成更接近 target distribution 的 validation data | 与 V12 的“用更接近部署分布的 validation 选择模型”是核心同构思想；差别是领域和实现，不足以构成独立方法。 |
| **Model Assessment and Selection under Temporal Distribution Shift** | 2024, ICML / PMLR 235；[官方页面](https://proceedings.mlr.press/v235/han24b.html)，[PDF](https://raw.githubusercontent.com/mlresearch/v235/main/assets/han24b.pdf) | 在 temporal shift 下估计目标风险并进行候选模型选择，使用 rolling-window 和 pairwise comparison | 说明 shift-aware model selection 已是独立研究主题；V12 的复合 validation MRR 是其在图任务上的朴素特例。 |
| **Clustering-Based Validation Splits for Model Selection under Domain Shift** | 2024, arXiv；[原文](https://arxiv.org/abs/2405.19461) | 用 MMD / kernel k-means 构造与训练分布有控制差异的 validation split，以服务 domain-shift model selection | 直接覆盖“改变 validation split 以匹配/暴露目标 shift”的方法论层面；V12 没有新的 split-selection theory。 |

## 3. 数学对象对比

已有 domain-generalization 工作把选择写成在候选模型集合上最大化目标近似 validation 风险，例如在 source validation 上选择 `argmax_h E_{(x,y) in D_val^S}[metric(h(x),y)]`，并进一步构造更接近 target 的 validation 集。V12 的 M2 只是把此原则用于两个图边类型：

```text
J_M2(t) = 0.5 MRR_old-old(t) + 0.5 MRR_new(t)
```

状态对象仍是已有模型在 epoch `t` 的 checkpoint；传播规则、消息状态、decoder 和训练损失均未改变。因而它不是一个新的 GNN 状态空间，也不是新的 link-prediction scoring function。

## 4. 直接重合、部分重合和不确定性

- **直接覆盖核心思想：** 分布偏移下使用目标近似 validation 进行模型/epoch 选择；这由 Lu et al. 2023、Han et al. 2024 和 Napoli–White 2024 共同覆盖。
- **部分重合：** semi-inductive LP benchmark 和 HeaRT 覆盖新节点任务定义、context、候选和评测协议，但不等于 V12 的具体 M2 公式。
- **未发现完全相同实现：** 未发现“NodeDup Cora/CiteSeer + old/new MRR 0.5/0.5”的同一代码实现；这一点只能支持一个可复现实证审计题目，不能支持独立算法创新。

因此 V12 不能进入“新方法证明”路线。后续若保留结果，应按 benchmark/protocol reproducibility note 或评测审计撰写，而不是按一项新的模型选择算法投稿。
