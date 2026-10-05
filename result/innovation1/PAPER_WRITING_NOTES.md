# PAPER WRITING NOTES — R-HSPE

## Contribution wording

### 中文建议稿

我们提出 R-HSPE，一种面向 pairwise link prediction 的轻量级超图上下文插件。对每个候选节点对，R-HSPE 枚举共享支持点两侧的 incident hyperedge-pair token 多重集，使用训练集 ECDF 归一化超边大小，并通过 permutation-invariant mean/max set encoder 生成零初始化的解码残差。在冻结的 V17.4 fixed-final-epoch 测试协议下，该插件相对 NCNC 在 Cora 与 PubMed 上分别获得 +0.025852682660934833 与 +0.007136914679784767 的 paired MRR 增益，两个数据集均为 5/5 seed wins。Citeseer strong-backbone transfer 未获支持，因此本文将该方法定位为有数据集与协议范围限定的 complementary plug-in，不声称普遍迁移或独立 SOTA。

### English draft

We introduce R-HSPE, a lightweight hypergraph-context plug-in for pairwise link prediction. For each candidate pair, it constructs a multiset of incident hyperedge-pair tokens through shared support nodes, encodes training-only ECDF-normalized cardinality descriptors with a permutation-invariant mean/max set encoder, and adds a zero-initialized decoder residual. Under the frozen V17.4 fixed-final-epoch test protocol, R-HSPE improves paired MRR over NCNC by +0.025852682660934833 on Cora and +0.007136914679784767 on PubMed, with wins on all five paired seeds for both datasets. Transfer to the Citeseer strong-backbone setting is not supported; we therefore present R-HSPE as a protocol-scoped complementary plug-in rather than a universal replacement backbone or standalone state-of-the-art predictor.

以上是建议措辞，提交前应按目标 venue 的术语、空间与引用格式调整；不可扩写为 first-use 或因果结论。

## Method section outline

### 3.1 Problem Setup
定义 pairwise link prediction、training-visible graph/hypergraph、候选端点、训练/验证/测试关系隔离及目标边移除。

### 3.2 Candidate-Specific Hyperedge Context
定义 shared support、两侧 incident hyperedge sets、target-masked effective cardinalities、按 (w,e,f) 枚举的 multiset。说明 identity multiplicity 是枚举拓扑与 token 重复次数，不是学习 hyperedge ID embedding。

### 3.3 Training-Only Rank Normalization
给出训练 active hyperedges 上拟合的 right-continuous ECDF；测试候选沿用训练 ECDF，不用验证/测试大小重新拟合。明确 6D token 的前 3 个 rank interaction 通道及后三个零通道。

### 3.4 Permutation-Invariant Pair Encoder
说明共享 Linear(6,8)+ReLU、逐候选 mean/max pooling、空 token 集合零池化、log1p token/support counts 与 18D 表示。

### 3.5 Residual Integration with Strong Backbones
说明零初始化 Linear(18,1) 残差如何加到 Raw-HG DCDLP、NCN、NCNC logits。区分 standalone 和 strong-backbone adapter 的配置；以表格报告参数数与开销。

## Experiment section outline

### 4.1 Experimental Setup
数据集、split、训练图隔离、固定候选、20 negatives/query、seed pairing、optimizer、epoch/checkpoint protocol。将 V17.3 与 V17.4 明确列为不同实验协议。

### 4.2 Standalone Evaluation
以 METRIC_TABLES Table 1 报告 V17.2 test 上相对 B0 的 MRR、Hits@10、Hits@20、mean positive rank 与 seed-paired delta。另用 Table 4 报 V17.3 standalone benchmark 和 rank，并说明其 standalone competitiveness WEAK 及计算预算差异。

### 4.3 Strong-Backbone Complementarity
以 Table 2 报告 V17.4 NCN/NCNC 插件结果和 NULL75 控制。主文重点为 NCNC+R-HSPE 在 Cora/PubMed 的 paired test 效果；如报告 NCN，要保留同一协议的 seed pairing 与 metrics。

### 4.4 Ablation and Mechanism Analysis
以 Table 5 报告 V17.1 validation controls 与 V17.2 final context-arm test contrast。将其描述为诊断性机制对照；保留 CONTEXT_DRIVEN 和 SIZE_CAUSAL_CLAIM NOT_SUPPORTED，不写因果 decomposition。

### 4.5 Generalization and Limitations
报告 standalone Citeseer test 支持与 strong-backbone Citeseer validation transfer failure 是不同发现；明确后者 test 未运行。列出20负例评估、focused novelty audit 范围、Cora 原始数据归档问题和 protocol-specific claim。

## Discussion：为什么 standalone 不是 NCN/NCNC 的替代品，仍有研究价值？

V17.3 standalone table 显示 R-HSPE 在该 benchmark 的 MRR rank 为 Cora 4、PubMed 4、Citeseer 3，弱于 NCN/NCNC；因此不应把贡献写成新 backbone 的竞争性替代。V17.4 则在 fixed-final-10 paired protocol 下显示 R-HSPE correction 可以在 NCNC logits 上补充有用信号，并由 NULL75 控制排除“只增加同等参数量”这一简单解释。其研究价值是**在已存在的强 pairwise graph predictor 上提供候选特定 hypergraph context**，而不是独自解决链路预测。该价值目前只由 Cora/PubMed 插件 test 支持；Citeseer validation 结果说明它不具普遍性。

## Limitations wording

- “The Citeseer strong-backbone gate failed on validation (mean paired ΔMRR = −0.02737937803369254; 0/3 wins), and no test evaluation was conducted.”
- “The experiments do not identify a causal contribution from hyperedge-size content; the frozen mechanism label remains CONTEXT_DRIVEN.”
- “The novelty assessment is a focused audit and does not establish publication priority.”
- “The standalone benchmark and strong-backbone plug-in table use intentionally different epoch and checkpoint protocols and must not be combined into one ranking.”
- “Evaluation uses 20 sampled negatives per positive query rather than all-node ranking.”
- “The processed Cora input is hash-identified, but the raw-data directory recorded in the frozen limitations is incomplete; public reproduction should archive the canonical source and preprocessing recipe.”

## Figures / supplementary material to prepare later

1. Method diagram matching the frozen token construction, ECDF, set encoder, pooling, counts, and residual.
2. A protocol table separating V17.2 standalone test, V17.3 benchmark, and V17.4 plug-in test.
3. Seed-level paired MRR plots from stored results, preserving Cora/PubMed and Citeseer validation labels.
4. Supplementary novelty matrix and source-hash manifest; do not turn the focused audit into a priority claim.
