# V17.3 — R-HSPE PUBLICATION BENCHMARK AUDIT

STATUS: POST-FREEZE BENCHMARK

IMPORTANT:

Innovation 1 已冻结：

# R-HSPE

来源：

HYPERGRAPH_RESEARCH/R_HSPE_FROZEN/

V17.3 不是：

method development

不是：

hyperparameter search

不是：

R-HSPE rescue。

任务只有一个：

# 在统一协议下完成论文级 strong-baseline comparison，
# 判断冻结 R-HSPE 是否具有足够竞争力进入论文主结果表。

---

# 1. READ FROZEN ARTIFACT FIRST

读取：

HYPERGRAPH_RESEARCH/R_HSPE_FROZEN/

以及：

HYPERGRAPH_RESEARCH/HSPE_V17_2/

确认：

INNOVATION_1 = R-HSPE

STATUS = FROZEN

不得修改：

R-HSPE source
token definition
ECDF
pooling
residual
hidden size
QTHS25
epochs
optimizer
splits
evaluator。

记录：

frozen code hash
config hash
split hashes
candidate hashes。

---

# 2. OUTPUT

创建：

HYPERGRAPH_RESEARCH/R_HSPE_BENCHMARK_V17_3/

包含：

00_PROTOCOL.md

01_BASELINE_SELECTION.md

02_IMPLEMENTATION_AUDIT.md

03_CORA_RESULTS.md

04_PUBMED_RESULTS.md

05_CITESEER_RESULTS.md

06_PAPER_REPORTED_RESULTS.md

07_FAIRNESS_AUDIT.md

08_NOVELTY_POSITIONING.md

PAPER_MAIN_TABLE.csv

PAPER_MAIN_TABLE.md

results.json

FINAL_REPORT.md

---

# 3. GOLDEN RULE

禁止：

直接把不同论文的原始 MRR

与 R-HSPE 数字排名后声称：

SOTA。

只有：

# 在当前冻结 protocol 下重新运行的方法

才进入：

FAIR QUANTITATIVE TABLE。

论文原始数字只能进入：

REFERENCE-ONLY TABLE。

---

# 4. DATASETS

固定：

Cora
PubMed
Citeseer

使用：

V17.2 exact datasets

exact splits

exact candidate construction

exact evaluation。

禁止：

重新下载另一版本 dataset

重新划分

更换 preprocessing。

优先复用现有：

dataset path
split files
candidate cache。

如果某 baseline

无法适配当前 dataset representation：

记录：

NOT_FAIRLY_ADAPTABLE

不要改 dataset 来迎合 baseline。

---

# 5. PRIMARY METRICS

固定：

MRR
Hits@10
Hits@20
Mean Positive Rank

主排序指标：

MRR。

所有方法：

相同 candidate sets。

不得：

每个方法自己采样 negatives。

---

# 6. SEEDS

论文主表：

seeds 0,1,2,3,4

如果某第三方方法

单次训练极其昂贵：

最低：

3 seeds

但必须标记。

R-HSPE：

直接复用 frozen test results。

不得重新选择 checkpoint。

---

# 7. BASELINE PRIORITY

分为：

Tier A — Direct Pairwise Competitors

Tier B — Strong Graph Pairwise Baselines

Tier C — Related-but-Nonidentical Methods

---

# 8. TIER A

优先尝试：

## A1 NSLR-HMANN

原因：

pairwise link prediction

hypergraph node/hyperedge modeling

与本任务较接近。

必须优先使用：

official implementation

或作者 release。

不要：

自行重写成更强版本。

---

## A2 HMNE

如果：

official/reliable implementation

可获得，

并且能够：

在当前 pairwise split

公平评分，

则运行。

否则：

REFERENCE_ONLY。

---

## A3 HMRLH

同样原则。

能稳定复现：

进入 quantitative。

无法公平迁移：

REFERENCE_ONLY。

---

## A4 CCLPH

它与 R-HSPE novelty overlap 最接近。

先审计：

任务定义

candidate definition

是否支持 pairwise candidate scoring。

如果：

能无方法修改地适配：

优先运行。

如果必须：

改变原方法核心

才能适配当前 protocol：

不要伪造 baseline。

记录：

REFERENCE_ONLY / TASK_MISMATCH。

---

# 9. TIER B

## B1 NCN

使用：

official implementation。

将 Raw-HG 数据

转换为：

与当前 pairwise relation一致的 ordinary graph representation

必须使用：

预先定义的 frozen projection rule。

优先：

与 B0 graph side

一致的 graph construction。

---

## B2 NCNC

同上。

NCNC 是重要：

candidate-specific pairwise LP

思想 baseline。

---

# 10. OPTIONAL EXISTING PROJECT BASELINES

检查当前项目历史结果。

如果存在：

已验证 strong baseline

且使用：

相同 split/evaluator/candidates，

可以进入主表。

但必须：

hash-compatible。

否则：

重新运行。

---

# 11. TIER C — DO NOT FORCE INTO MAIN TABLE

以下方法主要用于：

related-work / novelty comparison：

OFSH / OHAA

HP2PH

Hyperedge Copy Model

HNHN

HGNN

HYPER

Hypergraph Motif Representation Learning

以及任务不是：

ordinary pairwise link prediction

的方法。

只有它们能：

在不改变方法本质的情况下

输出当前 candidate pair score

才允许进入 main quantitative table。

否则：

REFERENCE_ONLY。

---

# 12. DOWNLOAD POLICY

服务器离线。

禁止：

server-side:

pip install from internet

git clone

wget

curl。

如果缺少第三方代码或依赖：

本地机器：

下载 source / wheel / dependency

然后上传服务器。

不要读取或打印：

.env

credentials。

优先：

official GitHub / author release

publisher supplementary material。

---

# 13. IMPLEMENTATION FIDELITY

对于每个第三方 baseline：

记录：

source URL / DOI

commit hash

official config

required changes

compatibility wrappers。

允许：

dataset loader adapter

evaluation adapter

output score adapter。

禁止：

修改：

architecture

loss

hidden dimension

paper-specific algorithm

来人为增强或削弱 baseline。

---

# 14. HYPERPARAMETER POLICY

原则：

使用：

paper-recommended

或：

official code default。

如果 paper 有：

Cora-like dataset config

优先使用。

禁止：

针对 test 调参。

如果必须选择：

只允许：

validation。

记录：

search space

selection criterion。

R-HSPE：

完全不参与重新调参。

---

# 15. FAIR EVALUATION

所有可比较方法：

必须在：

same test positives

same per-positive negatives

same grouping

same MRR evaluator

same Hits evaluator

下评分。

如果 baseline 原本只输出：

embedding

则：

使用其官方 downstream scorer。

如果没有：

不要擅自发明一个强 decoder。

记录：

NO_CANONICAL_SCORER。

---

# 16. TRAINING INFORMATION

所有 baseline：

只能使用：

training-visible graph / hypergraph。

禁止：

heldout positive leakage。

尤其检查：

message graph

incidence construction

hyperedge construction

negative filtering。

---

# 17. MAIN TABLE

输出类似：

| Method | Type | Cora MRR | PubMed MRR | Citeseer MRR | Params | Fair protocol? |
|---|---|---:|---:|---:|---:|---|

每格：

mean ± std。

突出：

best
second-best。

但：

不要自动声称 SOTA。

---

# 18. SECONDARY TABLE

Hits@10

Hits@20

Mean Rank

单独报告。

注意：

PubMed R-HSPE：

MRR 提升

但 Hits@10

相对 B0 略降。

必须完整展示。

禁止：

只报告有利 metric。

---

# 19. REFERENCE-ONLY TABLE

对于无法公平重跑的方法：

记录论文报告：

dataset
task
metric
reported score
split
negative protocol
candidate size

如果 protocol 不可比较：

明确：

NOT DIRECTLY COMPARABLE。

绝不：

用颜色/粗体制造排名。

---

# 20. PAPER COMPETITIVENESS DECISION

定义：

## STRONG

如果 R-HSPE：

在 3 datasets 中：

至少 2 个 MRR best/second-best

且：

第三个没有明显落后

则：

PAPER_COMPETITIVE_STRONG。

---

## ACCEPTABLE

如果：

R-HSPE 不一定第一，

但：

三个数据集整体稳定竞争

至少 2 个 dataset

处于 strong baseline range

且：

参数开销明显低

则：

PAPER_COMPETITIVE_ACCEPTABLE。

---

## WEAK

如果：

多个直接 competitor

在相同 protocol

稳定大幅超过 R-HSPE，

则：

PAPER_COMPETITIVE_WEAK。

注意：

WEAK

也不能回头调 R-HSPE。

只能：

在论文定位

或之后 Innovation 2

解决。

---

# 21. PARAMETER EFFICIENCY

R-HSPE 只增加：

75 parameters

这一点非常重要。

对所有 baseline

记录：

trainable params

training time

inference time

peak GPU memory

如果官方实现允许。

论文可能存在：

accuracy-efficiency tradeoff。

---

# 22. EFFECT SIZE

除了平均 MRR，

报告：

paired R-HSPE vs strongest comparable baseline

per-seed deltas

median delta

wins。

如果 baseline seeds

不是同一 RNG 语义：

不要假装是严格 paired statistical test。

---

# 23. STATISTICS

不要做：

大量 significance fishing。

如果候选完全共享：

可报告：

paired bootstrap CI。

否则：

主要使用：

mean±std

median

effect size。

---

# 24. NOVELTY POSITIONING

使用：

V17.2 NOVELTY_MATRIX

作为冻结基础。

不重新扩大 R-HSPE claim。

最终 contribution wording：

# candidate-specific hyperedge-pair context encoder

with:

training-only rank-normalized cardinality descriptors

and:

permutation-invariant decoder residual。

禁止：

first hyperedge size

first candidate hyperedge context

size causes performance。

---

# 25. STOP CONDITION

V17.3 完成后：

不得：

根据 baseline table

修改 R-HSPE。

Innovation 1

继续保持：

FROZEN。

即使：

某 baseline 更高，

也不要：

调参救第一创新。

---

# 26. FINAL PAPER READINESS

最后输出：

INNOVATION_1_METHOD_VALIDATED:
YES

TEST_GENERALIZATION:
YES/NO

THIRD_DATASET:
YES/NO

NO_EXACT_COLLISION_IN_FOCUSED_AUDIT:
YES/NO

FAIR_BASELINE_BENCHMARK:
COMPLETE/PARTIAL

COMPETITIVENESS:
STRONG/ACCEPTABLE/WEAK

PAPER_READY_INNOVATION_1:
YES/NO

---

# 27. FINAL REPORT

FINAL_REPORT.md 必须包含：

R_HSPE_FROZEN:
TRUE

CORA_R_HSPE:
...

PUBMED_R_HSPE:
...

CITESEER_R_HSPE:
...

NSLR_HMANN:
...

NCN:
...

NCNC:
...

HMNE:
...

HMRLH:
...

CCLPH:
...

DIRECTLY_COMPARABLE_METHODS:
...

REFERENCE_ONLY_METHODS:
...

BEST_ON_CORA:
...

BEST_ON_PUBMED:
...

BEST_ON_CITESEER:
...

R_HSPE_RANK:
...

PARAMETER_EFFICIENCY:
...

NOVELTY_STATUS:
...

COMPETITIVENESS:
...

PAPER_READY_INNOVATION_1:
...

NEXT_EXPECTED_STEP:
...

---

# 28. C2C HANDOFF

STATUS: EXECUTED

DIRECTION:
R_HSPE_PUBLICATION_BENCHMARK

R_HSPE:
FROZEN

FAIR_METHODS_RUN:
...

REFERENCE_ONLY:
...

CORA_RANK:
...

PUBMED_RANK:
...

CITESEER_RANK:
...

STRONGEST_COMPETITOR:
...

PARAMETER_COMPARISON:
...

NOVELTY:
...

COMPETITIVENESS:
...

PAPER_READY_INNOVATION_1:
...

NEXT_EXPECTED_STEP:
...

完成后停止。

不要自行开始 Innovation 2。