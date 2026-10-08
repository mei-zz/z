# TASK — V12 Autonomous Link-Prediction Innovation Search

## ROLE

你现在不是执行一个预定义候选。

你是：

**DCDLP-main 的自治研究代理。**

目标：

> 利用 autoresearch 风格的持续实验循环，在当前 link prediction 项目中自动寻找至少一个具有论文价值、可复现、具有独立机制证据、并能带来稳定指标提升的创新点。

允许的创新来源包括：

- negative sampling
- training objective
- ranking loss
- decoder
- pair representation
- GNN architecture
- graph / hypergraph interaction
- propagation
- residual design
- structural encoding
- multi-scale representation
- training dynamics
- teacher-student learning
- curriculum
- uncertainty / confidence
- optimization strategy

不要求继续沿 QTHS/CPTS。

如果新模型结构方向更强：

允许彻底转向。

---

# 0. Workspace

唯一工作区：

DCDLP-main

开始前确认：

workspace name == DCDLP-main

如果不是：

STOP。

不要在其它 workspace 执行。

---

# 1. Autoresearch 工作方式

采用 Karpathy autoresearch 的核心思想：

固定：

- evaluation harness
- dataset split
- validation metric
- experiment budget
- logging protocol

允许 agent 自动：

1. 阅读当前代码；
2. 提出实验假设；
3. 修改研究代码；
4. 执行远程实验；
5. 读取 validation；
6. 判断 KEEP / REJECT；
7. 回滚失败修改；
8. 更新 idea ledger；
9. 自动提出下一候选；
10. 持续循环。

不要只生成计划。

必须：

**立即执行研究循环。**

---

# 2. 建立 autoresearch 目录

创建：

AUTONOMOUS_LP_RESEARCH_V12/

至少包含：

program.md

BASELINE_AUDIT.md

IDEA_LEDGER.md

EXPERIMENT_LEDGER.tsv

BLACKLIST.md

NOVELTY_LEDGER.md

BEST_STATE.md

results.json

FINAL_REPORT.md

experiments/

candidate_patches/

logs/

---

# 3. program.md

把本提示词中的：

研究目标
协议
搜索空间
门控规则
停止规则

写入：

AUTONOMOUS_LP_RESEARCH_V12/program.md

之后：

把 program.md 当作本轮 autoresearch 的长期研究约束。

但：

不要只创建 program.md 后停止。

创建完成后：

立即进入实验循环。

---

# 4. 服务器

项目中已经配置服务器连接。

优先复用现有：

SSH
SCP
Paramiko
remote runner
experiment launcher

服务器无互联网。

本地机器可联网。

依赖原则：

服务器禁止：

pip online install
git clone
wget
curl external dependency

缺依赖时：

本地下载
→ 上传 wheel / source
→ server offline install

但：

优先不增加新依赖。

---

# 5. 安全

项目包含：

.env

可能包含：

IP
username
password

允许：

程序静默读取。

禁止：

cat .env

禁止：

打印 credential

禁止：

写入 log

禁止：

git add .env

禁止：

输出 credential 到实验文件。

---

# 6. 首先审计现有研究

必须读取：

HYPERGRAPH_RESEARCH/

以及已有：

AUTONOMOUS_LP_RESEARCH/

重点读取最近结果：

QTHS_V8_PAPER

RTHNL_V9

CPTS_V10

CPTS_V10_1_AUDIT

以及历史：

STRUCTURAL_V3
CONSTRUCTION_V4
COMPLEMENT_V5
NEGATIVE_V6
NEGATIVE_V6_1
CODNS_V6_2
HARDNESS_V7

提取：

baseline
protocol
dataset
split
model
loss
decoder
sampler
best validation
best test
known failures

写入：

BASELINE_AUDIT.md

---

# 7. 必须建立历史黑名单

以下方向不能简单重做：

PCHR

LCHR

SSHC

RAHC

HSA

ARHC

PMHE

ARPM

ECPH

ECNH

OWH

GHHR

CVHNM

DAF

false-negative HG veto mechanism

CODNS

AQTHS

RTHNL under K=1

CPTS true-tail detector claim

per-positive CPTS adaptivity claim

普通固定 quantile trimming 的微调

普通 SH75 window 微调

只有超参数变化、没有新机制的方案。

BLACKLIST.md 必须解释：

每个方向为什么失败。

---

# 8. 已知可靠事实

把以下事实作为研究先验：

1.

Graph-hard negative sampling 是强 baseline。

2.

Hardness region 会显著影响性能。

3.

QTHS / CPTS 能超过 Graph-hard。

4.

SH75 有时非常强。

5.

但：

固定 percentile / change-point / tail detector

尚不足以形成稳定机制。

6.

当前 training negative count：

K = 1

candidate pool：

M = 20

因此：

任何在最终 K=1 negatives 内做 weighting 的方法会退化。

7.

Raw Hypergraph 在早期实验中存在增益，

但大量：

routing
weighting
operator
construction

修改均未带来可靠进一步收益。

8.

不要假设：

“更复杂 = 更好”。

---

# 9. 本轮目标不是继续优化 QTHS

QTHS/CPTS 现在作为：

strong baselines

而不是必须继续的方向。

Agent 可以：

沿 hardness 继续，

也可以：

完全切到模型结构。

唯一要求：

候选必须有：

明确机制
matched control
novelty rationale
低成本 falsification。

---

# 10. 研究成功标准

最终希望找到：

至少一个：

PAPER_CANDIDATE

满足：

A.

相对最强相关 baseline：

稳定 validation gain。

B.

不是仅对单 seed 成立。

C.

不是仅因为参数量增加。

D.

不是仅因为训练时间增加。

E.

不是简单 hyperparameter tuning。

F.

至少存在一个 matched control，

证明关键机制。

G.

跨数据集或跨 backbone 至少得到一个额外支持。

H.

novelty search 未发现明显 exact collision。

---

# 11. Strong baseline

每个候选不能只比较：

Uniform

必须比较其所在方向的最强 baseline。

如果候选是 sampling：

至少比较：

Graph-hard
QTHS25
SH75
CPTS

根据适用性选强者。

如果候选是模型结构：

至少比较：

当前 matched Raw / Graph architecture

以及：

parameter-matched control。

如果候选是 loss：

模型和 sampler 必须完全匹配。

---

# 12. Research families

Autoresearch 可以从以下 family 选择。

不是必须按顺序。

---

## FAMILY A — Hardness Reliability / Training Dynamics

研究：

snapshot hardness 是否可靠。

候选方向例如：

- persistent hardness
- trajectory consistency
- forgetting events
- hardness volatility
- rank stability
- cross-checkpoint consensus

注意：

不能只是：

平均多个 checkpoint score。

必须有独立机制。

---

## FAMILY B — Pair Representation

当前 node embedding → decoder

可能没有显式表示：

pair interaction structure。

允许研究：

- pair-conditioned residual
- symmetric pair interaction
- multiplicative pair features
- edge-conditioned representation
- low-rank bilinear interaction
- pair token / pair state

但是：

必须严格 target masking。

禁止：

target edge leakage。

---

## FAMILY C — Decoder Innovation

研究：

当前 decoder 是否成为瓶颈。

候选：

- calibrated bilinear decoder
- low-rank tensor interaction
- dual-path decoder
- structural residual decoder
- rank-aware decoder

要求：

parameter-matched MLP control。

如果收益只来自：

更多参数：

REJECT。

---

## FAMILY D — Multi-Scale Graph Representation

允许：

1-hop
2-hop
ego-scale
local/global

但不要重新做：

ECPH
ECNH
OWH

可以探索：

representation fusion

而不是：

重新构造 hyperedge。

---

## FAMILY E — Graph + Raw-Hypergraph Representation

Raw Hypergraph 仍然是一个有效 view。

过去失败的是：

routing
hardness veto
structural operator

不代表：

所有 representation-level interaction 都失败。

允许：

late representation interaction

pair-level cross-view feature

orthogonal residual

feature decorrelation

但：

禁止简单 attention gate。

必须设计 matched fusion control。

---

## FAMILY F — Ranking Objective

当前 metric：

MRR

训练 loss 未必与 ranking 完全一致。

允许研究：

- pairwise ranking
- listwise ranking
- margin-free ranking
- top-negative ranking
- surrogate closer to MRR

但：

必须保持：

same candidate count

same sampler

same training budget。

重点寻找：

loss / metric mismatch。

---

## FAMILY G — Positive-side Learning

过去研究大量关注 negatives。

允许研究：

positive pairs 的：

difficulty
structural confidence
positive curriculum
positive weighting
positive ranking consistency

这一方向优先级较高，

因为历史搜索很少覆盖。

注意：

不能使用 validation/test labels。

---

## FAMILY H — Representation Regularization

允许：

- pairwise consistency
- topology consistency
- embedding geometry
- oversmoothing mitigation
- branch decorrelation
- residual normalization

但：

必须直接关联 link prediction mechanism。

不要做 generic dropout tweak。

---

# 13. 禁止低价值搜索

不允许将以下作为“创新”：

learning rate tweak

dropout tweak

hidden dimension tweak

weight decay tweak

batch size tweak

epoch tweak

random seed trick

negative count tweak

简单换 activation

简单 LayerNorm

简单 residual

这些可以作为支持配置，

不能成为 PAPER_CANDIDATE。

---

# 14. Idea generation

每次只维护：

最多 5 个 active ideas。

每个 idea 写入：

IDEA_LEDGER.md

包含：

ID

NAME

FAMILY

HYPOTHESIS

MECHANISM

WHY_NOW

EXPECTED_GAIN

COST

NOVELTY_RISK

CONTROLS

FAILURE_CONDITION

STATUS

不要一次生成 50 个想法。

---

# 15. Candidate scoring

进入实验前，

对 candidate 做内部优先级评分。

评分维度：

Novelty potential

Expected performance gain

Mechanistic clarity

Engineering cost

Control quality

Compatibility with current pipeline

Paper-story value

不要把评分写成最终论文结论。

只是 autoresearch 排序工具。

---

# 16. 快速筛选预算

历史已经证明：

1 epoch

对于结构创新不可靠。

因此 Stage 1：

Cora
seed 0
5 epochs

validation only

Test disabled。

对于：

只改变 sampling / loss

如果现有经验表明：

5 epochs 足够，

也保持 5 epochs。

固定所有其它 budget。

---

# 17. Stage 1 promotion

相对：

strongest relevant baseline

要求：

absolute MRR gain >= 0.003

或：

relative >= 1%

同时：

候选必须胜过其关键 matched control。

否则：

REJECT。

不要调参数救。

---

# 18. Stage 2

Stage 1 GO：

运行：

Cora
seed0
10 epochs

候选

strong baseline

matched control

如果：

candidate gain 消失：

REJECT。

如果：

candidate > strong baseline

且：

absolute >= 0.003

或：

relative >= 1%

进入 Stage 3。

---

# 19. Stage 3

运行：

Cora

seed0
seed1
seed2

10 epochs。

需要：

candidate > strong baseline

至少：

2/3 seeds

且：

mean gain > 0

且：

matched control

不能解释主要收益。

达到：

LOCAL_GO。

---

# 20. Test policy

任何候选：

Stage1
Stage2
Stage3

全部：

test disabled。

只有：

LOCAL_GO

才允许：

一次性 Cora test。

禁止：

根据 test

调整方法。

---

# 21. Stage 4 — External confirmation

如果 Cora test 支持：

优先运行：

PubMed

3 seeds。

然后：

Citeseer

如果：

PubMed 完全失败，

不要立即调方法。

先分析。

至少：

Cora + 一个额外 dataset

应该有正向 signal。

---

# 22. Backbone confirmation

如果候选属于：

sampling
loss
training dynamics
decoder

应尝试：

GCN
GraphSAGE
GAT

至少两个 backbone。

如果候选本身是：

新 encoder architecture

则不用做这个 gate。

改为：

多个 dataset。

---

# 23. Parameter matching

任何增加参数的候选：

必须有：

parameter-matched control。

例如：

候选新增：

+5k params

则 control：

增加同量普通 MLP / projection params。

如果：

candidate <= parameter control

REJECT。

---

# 24. Compute matching

任何增加：

forward passes
teacher
layers
message passing

的 candidate：

必须报告：

training time
inference time
GPU memory

必要时：

使用 compute-matched control。

不能把：

更多算力

包装成：

创新收益。

---

# 25. Novelty check

每一个进入 Stage 2 的 candidate：

必须做 focused novelty search。

本地联网机器执行。

服务器不联网。

搜索：

candidate exact mechanism

+ graph link prediction

+ negative sampling / GNN / decoder / ranking

记录：

closest works

overlap

difference

year

venue

NOVELTY_STATUS：

CLEAR_ENOUGH
/
EXACT_RULE_UNVERIFIED
/
CONCEPTUAL_OVERLAP
/
NOVELTY_CONFLICT

如果：

NOVELTY_CONFLICT

停止候选。

---

# 26. Literature 不允许替代实验

不能因为：

“看起来 novel”

就继续。

性能 gate 优先。

同样：

不能因为：

“性能提高”

就忽略 novelty。

最终 PAPER_CANDIDATE：

两者必须都过。

---

# 27. Autoresearch keep/revert

每轮实验结束：

如果 candidate FAIL：

git / patch 回滚候选修改。

保留：

experiment log
result
failure analysis

不要让失败代码污染下一实验。

如果 candidate PASS：

创建：

candidate checkpoint / commit / patch

记录：

BEST_STATE.md

然后：

下一 candidate

从：

best validated state

或：

clean baseline

出发，

根据研究问题决定。

不要无控制叠加多个改动。

---

# 28. 禁止无解释叠加

不能：

candidate A + B + C

只因为指标高。

必须先证明：

A 独立有效

B 独立有效

之后才允许：

A+B

并测试：

是否 additive。

论文创新不能来自：

随机堆模块。

---

# 29. 自动组合规则

如果找到：

Candidate A = LOCAL_GO

然后找到：

Candidate B = LOCAL_GO

且：

机制正交

允许测试：

A+B

要求：

A+B > max(A,B)

至少：

+0.002 MRR

否则：

不要把组合包装成第三创新。

---

# 30. Search priority

推荐 autoresearch 初始优先级：

1.

Training-dynamics / persistent-hardness

因为：

与 QTHS/CPTS 正交，

当前几乎未验证。

2.

Ranking-objective mismatch

因为：

目标是 MRR，

当前训练 objective 可能不是最匹配。

3.

Positive-side learning

历史搜索明显不足。

4.

Pair representation / decoder

可能直接提升 LP 表达力。

5.

Graph + raw-HG late representation

只在明确机制下尝试。

6.

全新 encoder structure。

但：

agent 可以根据代码审计重新排序。

---

# 31. 第一批最多 5 个候选

开始时：

生成最多 5 个候选。

要求来自：

至少 3 个不同 FAMILY。

不能五个全是 sampler。

优先：

一个 dynamics

一个 loss/ranking

一个 pair/decoder

一个 positive-side

一个 structural/model candidate

如果代码不支持：

调整。

---

# 32. 第一批建议候选模板

这些只是 seed ideas。

允许 agent 改进或替换。

---

## Candidate A — Persistent Hardness

使用 teacher checkpoints 的：

rank persistence

选择：

持续 hard

而非：

snapshot hard。

必须有：

trajectory shuffle
final-rank matched

controls。

---

## Candidate B — Listwise Positive-vs-Negatives Ranking

保持 sampler 不变。

对：

positive + 20 candidate scores

使用：

listwise objective

优化：

positive ranking

而不是独立 BCE。

必须比较：

BCE
pairwise ranking
parameter-free listwise

目标：

更贴近 MRR。

---

## Candidate C — Positive Difficulty Calibration

根据：

training positive

在 Graph teacher 下的：

margin / rank difficulty

调整：

positive-side learning

而不是 negative selection。

禁止：

validation labels。

必须有：

shuffled-positive-difficulty control。

---

## Candidate D — Low-Rank Pair Interaction Decoder

当前 node embeddings：

z_u
z_v

引入：

symmetric low-rank interaction

但参数量严格控制。

比较：

same-param MLP decoder。

如果只是参数增加：

REJECT。

---

## Candidate E — Graph/Raw-HG Orthogonal Pair Residual

不是 gate。

不是 routing。

构造：

graph pair feature

hypergraph pair feature

只让 HG 分支学习：

与 Graph pair representation 正交的 residual component。

必须有：

same-dim concatenation
random orthogonal projection
parameter-matched residual

controls。

---

# 33. Candidate A/B/C/D/E 不是强制

Autoresearch 在阅读当前代码后：

如果发现：

某 candidate 不兼容

或：

历史已经等价失败

应替换。

但必须解释：

为什么替换。

---

# 34. 每个实验时间控制

目标不是：

一个候选训练几个小时。

单个 Stage1：

应尽量控制为：

几分钟到十几分钟。

如果候选：

Stage1 明显需要 >30 min

且没有强理论原因：

降低优先级。

V100 要用于：

大量快速 falsification。

---

# 35. 持续实验

Autoresearch 不要在：

第一个 candidate fail

后停止。

持续：

IDEA
→ EXPERIMENT
→ RESULT
→ KEEP/REJECT
→ NEXT IDEA

直到触发停止条件。

---

# 36. 研究循环停止条件

只有以下情况允许停止：

## STOP A — Strong candidate found

找到候选满足：

- Cora 3 seeds GO
- Cora test support
- 至少一个额外 dataset positive
- mechanism control passed
- novelty not conflict

标记：

PAPER_CANDIDATE_FOUND。

如果 user goal 是继续寻找第二创新，

仍可继续。

---

## STOP B — Two orthogonal innovations found

找到：

Innovation 1
Innovation 2

均为 LOCAL/STRONG GO

且组合：

有 additive gain。

标记：

PAPER_CORE_READY。

停止本轮 autonomous search。

---

## STOP C — Experiment cap

最多：

40 个 Stage1 equivalent experiments

如果没有 candidate 达到 Stage2：

停止：

NO_SIGNAL_AFTER_BROAD_SEARCH

---

## STOP D — Research family exhausted

至少：

5 个 orthogonal families

都尝试，

均没有可重复 signal。

停止：

NO_EXECUTABLE_IDEA_AFTER_EXHAUSTIVE_SEARCH

---

# 37. 不要提前停止

以下不是停止理由：

第一个想法失败

第二个想法失败

一条 family 失败

某论文撞车

某 seed 失败

只要：

实验预算未耗尽

继续自主研究。

---

# 38. Idea mutation

失败候选只有在：

出现明确局部信号

且：

matched control 支持机制

时：

允许一个 targeted revision。

每个 candidate family：

最多：

1 次 targeted revision。

禁止：

连续调 10 个参数救同一想法。

---

# 39. Strong unexpected controls

如果某个 control：

显著超过 candidate

不要忽略。

自动：

把该 control

升级为：

NEW_SIGNAL。

像过去：

Graph-hard control

变成真正研究方向一样。

必须分析：

为什么 control 强。

如果它具备：

机制
novelty
可验证性

允许作为新的 candidate lineage。

---

# 40. Metrics

主指标：

MRR

同时记录：

Hits@1
Hits@3
Hits@10

如果项目已有。

但：

promotion gate

仍以：

MRR

为主。

不要挑指标。

---

# 41. 数据泄漏

严格：

STRICT_TRAIN_ONLY

训练 candidate / graph / hypergraph / teacher：

不能使用：

validation positive identity
test positive identity

除非：

protocol 明确仅用于 evaluation。

增加/保留 leakage tests。

任何 candidate：

一旦存在泄漏：

实验作废。

---

# 42. Evaluation integrity

每个候选记录：

split hash

candidate-pool hash

teacher hash

checkpoint hash

seed

epoch

git commit / patch id

runtime

GPU memory

params

这样：

所有结果可复现。

---

# 43. 实验日志

EXPERIMENT_LEDGER.tsv：

至少列：

exp_id

timestamp

candidate_id

family

parent_state

dataset

seed

epochs

change_summary

baseline_mrr

candidate_mrr

delta

control_mrr

params

runtime

decision

novelty_status

notes

---

# 44. Idea ledger

IDEA_LEDGER.md：

必须持续更新。

状态：

PROPOSED

RUNNING

REJECTED

PROMOTED

GO

BLACKLISTED

每个 rejection：

写一句明确 failure reason。

---

# 45. Blacklist

任何经过：

matched experimental rejection

的机制：

加入：

BLACKLIST.md

避免 agent 后续重新发明：

同义词版本。

---

# 46. 自动代码检查

任何 patch：

先运行：

unit tests
shape tests
leakage tests
smoke test

再上服务器。

失败：

修复代码问题。

不要把：

runtime bug

当成：

research failure。

---

# 47. Autoresearch 分支

如果 git 当前干净：

创建：

autoresearch/v12-lp

如果已存在：

创建：

autoresearch/v12-lp-<timestamp-safe-tag>

不要覆盖旧研究分支。

每个：

PROMOTED candidate

创建 commit。

失败 candidate：

允许保留 patch file，

但代码回滚。

---

# 48. 不修改核心 evaluation harness

类似 autoresearch：

固定 ground-truth evaluator。

确认当前项目中：

dataset split
metrics
evaluation negatives
MRR calculation

对应文件。

标记为：

IMMUTABLE_EVAL_FILES

Autoresearch 不允许修改。

如果确实需要修改 evaluator：

STOP

记录：

EVALUATION_CHANGE_REQUIRED

不能悄悄改指标。

---

# 49. Autoresearch 可修改范围

允许修改：

model modules
decoder
sampler
loss
training code
candidate-specific configs

不允许修改：

dataset labels
split
evaluation metric
test protocol

---

# 50. Novelty-driven prioritization

如果两个候选性能预期相近：

优先：

更清晰
更简单
更容易控制
更新颖
更少参数

的方法。

不要优先复杂模型。

---

# 51. 论文价值评分

候选进入 Stage3 后，

写：

PAPER_VALUE.md

回答：

Problem:

为什么现有方法有缺陷？

Mechanism:

新方法做什么？

Evidence:

哪个 control 证明机制？

Novelty:

和最近工作区别是什么？

Cost:

额外参数 / 时间？

Generalization:

数据集/backbone？

Story:

能否形成一段清晰 Introduction？

如果写不清：

即使性能略涨，

也不直接 promotion 为最终 innovation。

---

# 52. 当前第一创新的处理

现有：

QTHS
CPTS

不删除。

它们作为：

strong empirical baselines

以及：

hardness-region family evidence。

但：

不要默认论文最终必须包含它们。

如果 autoresearch 找到：

更强、更清晰、更 novel

的方法：

允许替换它们。

---

# 53. 如果模型结构候选胜出

如果新 architecture：

稳定明显超过：

current model

且：

parameter/compute controls passed

则：

优先作为论文 Innovation 1。

QTHS/CPTS：

可转成：

training enhancement

或完全不进入主文。

论文目标：

不是保护旧创新，

而是找到：

最强、最干净的创新。

---

# 54. 如果 sampling 候选胜出

必须：

正面比较：

Graph-hard
QTHS
SH75
CPTS

不能只比 Uniform。

---

# 55. 如果 loss 候选胜出

必须：

在：

同 sampler

下比较。

例如：

Graph-hard + BCE
vs
Graph-hard + new loss

以及：

SH75 + BCE
vs
SH75 + new loss

判断：

loss 是否独立有效。

---

# 56. 如果 architecture 候选与 sampler 都有效

测试：

Architecture only

Sampler only

Architecture + Sampler

如果：

组合 additive：

这是理想论文结构：

Innovation 1:
representation/model

Innovation 2:
training/sampling

Innovation 3:
combined mechanism / analysis

---

# 57. Autonomous novelty search

每个 PROMOTED candidate：

自动进行 focused literature search。

不要搜索整个领域。

查询：

exact mechanism

closest keyword

link prediction

graph neural networks

2022–2026

记录：

5–10 个最接近工作。

如果互联网受限：

本地机器执行。

---

# 58. 服务器状态

每轮训练前：

检查：

GPU idle / available。

训练完成：

确认：

无残留进程。

不要：

无限后台监控。

只在实验执行过程中监控。

最终：

释放 GPU。

---

# 59. 最终交付

FINAL_REPORT.md 必须包含：

STATUS

TOTAL_EXPERIMENTS

TOTAL_GPU_TIME

FAMILIES_EXPLORED

BEST_BASELINE

BEST_VALIDATION_MRR

BEST_TEST_MRR

BEST_CANDIDATE

BEST_CANDIDATE_FAMILY

GAIN_OVER_STRONG_BASELINE

SEED_STABILITY

CROSS_DATASET

BACKBONE_GENERALIZATION

MECHANISM_CONTROL

PARAMETER_OVERHEAD

RUNTIME_OVERHEAD

NOVELTY_STATUS

REJECTED_MAJOR_IDEAS

BLACKLIST_SUMMARY

PAPER_CANDIDATE

SECOND_INNOVATION

COMBINATION_RESULT

FINAL_DECISION

NEXT_EXPECTED_STEP

---

# 60. 最终决策枚举

最终只允许：

PAPER_CORE_READY

PAPER_CANDIDATE_FOUND

ONE_STRONG_INNOVATION_FOUND

NO_SIGNAL_AFTER_BROAD_SEARCH

NO_EXECUTABLE_IDEA_AFTER_EXHAUSTIVE_SEARCH

BLOCKED_BY_INFRASTRUCTURE

---

# 61. 最终 C2C HANDOFF

最终返回：

STATUS: EXECUTED

AUTORESEARCH_RUN:
...

EXPERIMENTS:
...

FAMILIES_EXPLORED:
...

BEST_CANDIDATE:
...

BEST_FAMILY:
...

STRONG_BASELINE:
...

VALIDATION:
...

TEST:
...

CROSS_DATASET:
...

BACKBONE:
...

MECHANISM_CONTROL:
...

NOVELTY_STATUS:
...

SECOND_CANDIDATE:
...

COMBINATION:
...

DECISION:
...

FAILURE_REASON:
...

NEXT_EXPECTED_STEP:
...

并给出：

FINAL_REPORT.md
results.json
IDEA_LEDGER.md
EXPERIMENT_LEDGER.tsv
BLACKLIST.md
BEST_STATE.md

路径。

---

# 62. 最重要的自治研究原则

不要为了：

“证明某个我预先想好的方法”

而实验。

你的目标是：

**发现事实。**

如果：

control 比 candidate 强，

研究 control。

如果：

旧 baseline 比所有创新强，

接受事实并换 family。

如果：

新 architecture 强，

放弃 sampling 主线也可以。

如果：

简单方法强于复杂方法，

优先简单方法。

如果：

一个机制连续失败，

进入 blacklist。

整个过程：

持续、自动、可回滚、可审计。

---

# 63. 开始执行

现在立即：

1. 审计当前 workspace；
2. 创建 autoresearch branch；
3. 创建 AUTONOMOUS_LP_RESEARCH_V12/program.md；
4. 固定 evaluation harness；
5. 建立 baseline；
6. 生成第一批最多 5 个跨 family candidates；
7. 启动 Stage1；
8. 根据结果自主循环；
9. 不等待人工确认；
10. 直到触发正式停止条件。

立即开始。--- V12 SUPPLEMENT OVERRIDE ---
# V12 SUPPLEMENT — PAPER-CORE CONTINUATION MODE

## IMPORTANT OVERRIDE

本补充规则优先级高于前述 V12 中：

`PAPER_CANDIDATE_FOUND` 后停止

相关规则。

从现在开始：

# 找到第一个 PAPER\_CANDIDATE 后，不停止 autoresearch。

而是：

冻结 Innovation 1

并自动进入：

# PHASE 2 — Innovation 2 Search

最终优先停止目标改为：

# PAPER\_CORE\_READY

即：

至少找到两个具有独立实验支持、机制正交、能够形成统一论文故事的创新点。

---

# 1\. 第一创新找到后的行为

当某 candidate 达到：

PAPER\_CANDIDATE\_FOUND

即满足：

- Cora 3-seed support
- Cora test support
- 至少一个额外 dataset positive
- matched mechanism control passed
- novelty 无明显 conflict

立即执行：

## FREEZE\_INNOVATION\_1

记录：

Innovation ID

method name

exact implementation

hyperparameters

git commit

patch

training protocol

validation results

test results

cross-dataset results

backbone results

mechanism controls

runtime

parameter count

novelty status

写入：

AUTONOMOUS\_LP\_RESEARCH\_V12/INNOVATION\_1.md

同时更新：

BEST\_STATE.md

状态：

INNOVATION\_1\_FROZEN

---

# 2\. Innovation 1 冻结原则

一旦冻结：

禁止为了寻找 Innovation 2：

重新调 Innovation 1 的核心参数。

Innovation 1 必须作为固定方法。

允许：

bug fix

reproducibility fix

efficiency-equivalent implementation

禁止：

根据 Innovation 2 的结果反过来修改 Innovation 1。

否则会造成：

joint tuning contamination。

---

# 3\. Phase 2 总目标

现在研究目标改为：

> 在 Innovation 1 已经成立的条件下，寻找一个机制上正交、单独有效，并且最好能与 Innovation 1 产生 additive gain 的第二创新。

第二创新不能只是：

Innovation 1-v2

Innovation 1 加一个新超参数

Innovation 1 更大的模型

Innovation 1 不同阈值

Innovation 1 不同 loss coefficient

必须解决：

**另一个独立 bottleneck。**

---

# 4\. Innovation 2 搜索优先级

首先判断 Innovation 1 属于哪个 FAMILY。

然后优先搜索：

与其机制正交的 family。

---

## 如果 Innovation 1 是 Sampling / Hardness

Innovation 2 优先级：

1. ranking objective
2. pair representation
3. decoder
4. positive-side learning
5. encoder / structural representation

降低优先级：

另一个 negative sampler

除非存在非常明确的新信息来源。

---

## 如果 Innovation 1 是 Ranking / Loss

Innovation 2 优先：

1. pair representation
2. decoder
3. encoder
4. sampling
5. positive-side structure

---

## 如果 Innovation 1 是 Decoder / Pair Representation

Innovation 2 优先：

1. training objective
2. negative sampling
3. positive-side learning
4. multi-scale representation
5. structural regularization

---

## 如果 Innovation 1 是 Encoder / Architecture

Innovation 2 优先：

1. loss / ranking
2. sampling
3. decoder
4. positive-side learning

---

# 5\. Phase 2 baseline 必须改变

Innovation 2 不允许只对：

Original Baseline

进行比较。

必须运行两个上下文：

## Context A — Standalone

Baseline
vs
Innovation 2

回答：

Innovation 2 是否独立有效？

## Context B — On top of Innovation 1

Innovation 1
vs
Innovation 1 + Innovation 2

回答：

Innovation 2 是否能给已经很强的 Innovation 1 继续提供增益？

这是第二创新最重要的标准。

---

# 6\. Innovation 2 Stage 1

快速筛选：

Cora

seed 0

5 epochs

运行至少：

Baseline

Innovation 1

Candidate 2

Innovation 1 + Candidate 2

matched control

Test disabled。

---

# 7\. Innovation 2 Stage 1 Promotion

Candidate 2 至少满足一个：

## Standalone signal

Candidate2 - Baseline

absolute MRR \>= +0.003

或 relative \>= +1%

并胜 matched control。

以及最好满足：

## Additive signal

## Innovation1+Candidate2

Innovation1

absolute \>= +0.002

如果：

Candidate2 standalone 很强

但 additive \< +0.002

仍可进入 Stage2，

因为可能成为论文 alternative contribution。

如果：

standalone 无信号

且 additive 无信号：

REJECT。

---

# 8\. Innovation 2 Stage 2

Cora

seed0

10 epochs

比较：

Baseline

Innovation1

Candidate2

Innovation1+Candidate2

matched control。

Promotion：

Candidate2 standalone 或 additive signal

必须仍然存在。

优先要求：

Innovation1 + Candidate2

> Innovation1

至少：

+0.002 MRR。

---

# 9\. Innovation 2 Stage 3

Cora：

seed0
seed1
seed2

10 epochs。

要求：

## Independent validity

Candidate2 \> Baseline

至少 2/3 seeds

mean gain \> 0

并且：

## Additive validity

Innovation1+Candidate2

>

Innovation1

至少 2/3 seeds

mean additive gain \> 0。

如果同时满足：

INNOVATION\_2\_LOCAL\_GO。

---

# 10\. 强 additive 标准

定义：

STRONG\_ADDITIVITY

如果：

## mean(<br />Innovation1+Innovation2

max(Innovation1, Innovation2)
)

>= +0.002 MRR

且：

至少 2/3 seeds 为正。

如果达到：

这是非常强的论文核心证据。

---

# 11\. Test policy for Innovation 2

只有：

INNOVATION\_2\_LOCAL\_GO

才一次性运行 Cora test：

Baseline

Innovation1

Innovation2

Innovation1+Innovation2

matched control。

禁止根据 test 修改 Innovation 2。

---

# 12\. Cross-dataset confirmation

如果 Cora test 支持：

在至少一个额外 dataset：

优先 PubMed

然后 Citeseer

运行：

Baseline

Innovation1

Innovation2

Innovation1+Innovation2

至少 3 seeds。

目标：

确认第二创新不是：

Cora-specific。

---

# 13\. 最终 Innovation 2 成功标准

Innovation 2 成为正式论文创新需要：

A.

独立有效：

Candidate2 \> Baseline

B.

机制 control 通过

C.

至少 Cora + 一个额外 dataset 有正向证据

D.

novelty 无明显 conflict

E.

最好：

Innovation1 + Candidate2

>

Innovation1

如果 A-D 全部成立，

但 E 不成立：

标记：

ORTHOGONAL\_BUT\_NONADDITIVE

可作为独立 contribution，

但不是最优论文组合。

如果 A-E 全部成立：

标记：

INNOVATION\_2\_CONFIRMED。

---

# 14\. Paper Core Ready

如果：

Innovation 1 confirmed

且：

Innovation 2 confirmed

且：

combination additive

最终：

FINAL\_DECISION = PAPER\_CORE\_READY

此时停止大范围创新搜索。

不要继续寻找：

Innovation 3

除非还有非常充足计算预算，

且第三创新来自真正不同机制。

论文两个算法创新已经足够。

---

# 15\. 如果 Innovation 2 搜索失败

不要因为第一个第二创新失败而停止。

继续 autonomous search。

Innovation 1 冻结后：

允许最多探索：

# 25 个 Stage-1-equivalent Innovation-2 experiments

或者：

至少 4 个与 Innovation 1 正交的 research families。

例如：

ranking
decoder
positive-side
architecture

全部尝试。

只有满足其一才允许停止：

NO\_SECOND\_INNOVATION\_AFTER\_BROAD\_SEARCH

---

# 16\. Innovation 2 family budget

避免一个方向无限调。

每个 family：

最多：

3 个独立候选

每个候选：

最多 1 次 targeted revision。

例如：

Ranking family：

Candidate R1
Candidate R2
Candidate R3

全部失败：

RANKING\_FAMILY\_EXHAUSTED。

进入下一 family。

---

# 17\. Innovation 1 周边深挖

找到 Innovation 1 后，

允许围绕其研究发现生成 Innovation 2，

但不能只是改变同一个参数。

允许的“沿 Innovation 1 继续创新”包括：

发现 Innovation 1 暴露的新 bottleneck。

例如：

如果 Innovation 1 改善 negative selection，

可以研究：

positive ranking
decoder calibration
pair representation
training objective

如果 Innovation 1 改善 decoder，

可以研究：

representation-decoder alignment

如果 Innovation 1 改善 architecture，

可以研究：

architecture-aware training objective。

要求：

第二创新具有独立 mathematical operation

以及独立 matched control。

---

# 18\. Failure-driven innovation generation

Phase 2 每次失败后：

不要只随机生成下一个方法。

先分析失败：

optimization bottleneck？

representation bottleneck？

sampling bottleneck？

generalization bottleneck？

ranking mismatch？

positive-side bottleneck？

然后：

下一 candidate

必须针对失败暴露的问题。

在：

IDEA\_LEDGER.md

记录：

PREVIOUS\_FAILURE

NEW\_HYPOTHESIS

WHY\_THIS\_IS\_DIFFERENT。

---

# 19\. Strong control promotion

如果 Innovation 2 实验中：

某 control

显著超过：

Innovation1

或：

Innovation1+Candidate2

则自动：

CONTROL → NEW\_CANDIDATE

不要忽略。

重复使用之前：

Graph-hard 意外成为强 signal

的经验。

---

# 20\. Combination Matrix

一旦找到 Innovation 1 和 Innovation 2，

强制运行完整 2×2 ablation：

| Model | I1 | I2 |
| --- | --- | --- |
| Baseline | OFF | OFF |
| I1 | ON | OFF |
| I2 | OFF | ON |
| I1+I2 | ON | ON |

全部：

same split
same seed
same epochs
same compute policy。

这是论文最重要的 ablation。

---

# 21\. Interaction Analysis

计算：

Delta1 =
I1 - Baseline

Delta2 =
I2 - Baseline

Delta12 =
I1+I2 - Baseline

AdditivityResidual =

Delta12 - max(Delta1, Delta2)

以及：

SynergyResidual =

Delta12 - (Delta1 + Delta2)

不要要求：

SynergyResidual \> 0。

只要求：

I1+I2

稳定优于单独最好方法。

---

# 22\. 参数量控制

如果 I1 或 I2 增加参数：

组合实验必须增加：

parameter-matched combined control。

例如：

I1 + I2

多 10k parameters，

control：

Baseline + 同量普通 projection / MLP。

如果组合收益可被参数量解释：

PAPER\_CORE\_READY 不成立。

---

# 23\. Compute control

如果组合：

增加多次 forward

额外 teacher

额外 message passing

报告：

GPU time

memory

inference cost。

论文需要明确：

performance / cost tradeoff。

---

# 24\. 服务器利用策略

服务器 GPU 是研究资源，

需要充分利用。

允许：

并行运行互相独立的：

different seeds

different candidates

different controls

前提：

GPU memory 足够

且：

不会影响可复现性。

优先并行：

Stage1 candidate batch

3-seed confirmations

control arms。

---

# 25\. GPU 利用率

如果：

GPU memory \< 40%

且实验互相独立，

可以安全并行多个 jobs。

逐步增加并发，

观察：

OOM

runtime degradation。

不要：

为了达到 100% utilization

导致：

OOM
swap
experiment interference。

目标：

最大化：

completed experiments / wall-clock hour

不是：

单纯 GPU utilization %。

---

# 26\. Server queue

维护：

AUTONOMOUS\_LP\_RESEARCH\_V12/EXPERIMENT\_QUEUE.tsv

字段：

job\_id

candidate

stage

dataset

seed

priority

estimated\_cost

status

gpu\_mem\_estimate

start\_time

end\_time

result

优先级：

P0:
confirmation of strong signal

P1:
mechanism control

P2:
new Stage1 ideas

P3:
diagnostics。

---

# 27\. 不要 GPU 空闲等待人工确认

只要：

没有达到正式 STOP CONDITION

且：

存在可执行 candidate

自动：

继续下一实验。

不要：

“等待用户决定”。

不要：

因为一个候选完成

让 GPU 长时间闲置。

---

# 28\. 但禁止无限后台循环

整个 autonomous run

必须由当前 autoresearch process 管理。

最终达到停止条件后：

退出所有训练进程

清理 queue

确认 GPU idle

输出最终 HANDOFF。

不要留下：

永久 monitor daemon。

---

# 29\. 搜索预算修改

原 V12：

40 Stage1-equivalent

修改为：

## Phase 1

最多：

40 Stage1-equivalent

目标：

找到 Innovation 1。

一旦 Innovation 1 找到：

Phase1 budget 停止计数。

## Phase 2

额外：

25 Stage1-equivalent

专门寻找 Innovation 2。

因此总预算上限：

约 65 Stage1-equivalent

但：

真正 GO candidate 的：

Stage2/Stage3/test

允许额外运行，

不因为达到 Stage1 budget 而中断确认。

---

# 30\. 如果 Phase 1 很快成功

例如：

第 6 个实验

就找到 Innovation 1。

不要浪费剩余 34 个 Phase1 quota

继续随机找第一创新。

立即：

冻结 I1

切换 Phase2。

这样计算资源用于：

找到论文第二贡献。

---

# 31\. 如果出现比 Innovation 1 更强的新方法

Phase2 中：

如果某 Candidate2：

不仅机制正交，

而且 standalone：

明显 \> Innovation1

不要自动替换 Innovation1。

首先判断：

它们是否可以组合。

如果：

I1+Candidate2

最好：

保留两者。

如果：

Candidate2 完全支配 I1

且：

组合无增益，

允许：

Candidate2 升级为新的 Innovation1

然后：

重新搜索正交 Innovation2。

记录：

INNOVATION\_REPLACEMENT。

---

# 32\. 第二创新不能降低第一创新可信度

如果：

Innovation2 只有在改变：

I1 的关键 protocol

dataset split

evaluation setting

negative count

training budget

后才有效：

不能作为正式 I2。

I2 必须：

在冻结的 I1 protocol 下兼容。

---

# 33\. Novelty Pair Check

I1 和 I2 分别通过 novelty search 后，

还必须搜索：

I1 + I2 的组合是否已有高度相同工作。

例如：

一个论文可能已经同时：

新 decoder
+
新 loss

即使两个模块单独看都还好。

因此：

最终 PAPER\_CORE\_READY 前

执行：

COMBINED\_NOVELTY\_CHECK。

---

# 34\. Paper story coherence

I1 / I2 不能只是：

“两个能涨点的模块”。

最终必须能形成：

一个统一问题链。

创建：

PAPER\_STORY.md

回答：

Main Problem:

Bottleneck 1:

Innovation 1:

Remaining Bottleneck:

Innovation 2:

Why I2 naturally follows I1:

Why combination helps:

Evidence:

Controls:

Generalization:

如果不能写成一个自然故事：

PAPER\_STORY\_COHERENCE = LOW。

继续寻找更合适的 I2。

---

# 35\. 理想论文结构示例

不是强制。

如果 I1 是：

persistent-hardness sampler

I2 可以是：

ranking objective

故事：

更可靠 negatives
+
更匹配 MRR 的 objective。

如果 I1 是：

pair interaction decoder

I2 可以是：

hard negative training。

故事：

better pair representation
+
better supervision。

如果 I1 是：

new encoder

I2 可以是：

structure-aware ranking objective。

优先：

互补机制。

---

# 36\. Final stop condition override

从现在起：

`PAPER_CANDIDATE_FOUND`

不是最终 stop。

它只触发：

PHASE\_2\_START。

最终优先停止条件：

# PAPER\_CORE\_READY

定义：

Innovation1 confirmed

Innovation2 confirmed

combination tested

combination \>= best single innovation

并最好：

additive gain \>= +0.002 MRR

至少：

2/3 seeds

且：

cross-dataset support

novelty acceptable

paper story coherent。

---

# 37\. Secondary stop conditions

如果 Phase2 budget 用尽：

允许：

ONE\_STRONG\_INNOVATION\_FOUND

条件：

Innovation1 完整确认

但没有找到合格 Innovation2。

不要因此否定 Innovation1。

如果：

I1 后续正式复现失败：

撤销冻结，

返回 Phase1。

---

# 38\. 最终 FINAL\_REPORT 增加

在原字段基础上增加：

PHASE1\_EXPERIMENTS:

PHASE2\_EXPERIMENTS:

INNOVATION\_1:

I1\_FAMILY:

I1\_VALIDATION:

I1\_TEST:

I1\_CROSS\_DATASET:

I1\_MECHANISM:

I1\_NOVELTY:

INNOVATION\_2:

I2\_FAMILY:

I2\_VALIDATION:

I2\_TEST:

I2\_CROSS\_DATASET:

I2\_MECHANISM:

I2\_NOVELTY:

I1\_I2\_ORTHOGONALITY:

COMBINATION\_VALIDATION:

COMBINATION\_TEST:

ADDITIVE\_GAIN:

PARAMETER\_CONTROL:

COMPUTE\_CONTROL:

COMBINED\_NOVELTY:

PAPER\_STORY\_COHERENCE:

FINAL\_DECISION:

---

# 39\. 最终 HANDOFF

最终返回：

STATUS: EXECUTED

AUTORESEARCH:
V12

PHASE1:
...

INNOVATION\_1:
...

INNOVATION\_1\_EVIDENCE:
...

PHASE2:
...

INNOVATION\_2:
...

INNOVATION\_2\_EVIDENCE:
...

COMBINATION:
...

ADDITIVE\_GAIN:
...

CROSS\_DATASET:
...

BACKBONE:
...

NOVELTY:
...

PAPER\_STORY:
...

TOTAL\_EXPERIMENTS:
...

TOTAL\_GPU\_TIME:
...

DECISION:
PAPER\_CORE\_READY
/
ONE\_STRONG\_INNOVATION\_FOUND
/
NO\_SECOND\_INNOVATION\_AFTER\_BROAD\_SEARCH
/
NO\_EXECUTABLE\_IDEA\_AFTER\_EXHAUSTIVE\_SEARCH

NEXT\_EXPECTED\_STEP:
...

---

# 40\. 最终自治目标

你的任务不再是：

“找到一个能涨点的方法”。

你的任务是：

# 找到一个可以成为论文主贡献的 Innovation 1，

# 然后围绕它寻找一个独立有效、机制互补的 Innovation 2，

# 最后验证两者组合是否带来额外收益。

优先：

简单
清晰
可解释
有控制
可复现
可组合

而不是：

复杂。

在正式达到：

PAPER\_CORE\_READY

之前：

只要实验预算仍允许，

服务器继续进行下一项有价值的实验。

立即将这些规则合并进：

AUTONOMOUS\_LP\_RESEARCH\_V12/program.md

然后继续执行 V12 autoresearch。
