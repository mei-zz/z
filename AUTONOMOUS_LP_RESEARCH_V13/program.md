# V13 — EVIDENCE-SEEDED AUTONOMOUS INNOVATION SEARCH

## 0. ROLE

Workspace:

DCDLP-main

你是该工作区的 autonomous research agent。

V12 已结束：

FINAL_DECISION =
NO_EXECUTABLE_IDEA_AFTER_EXHAUSTIVE_SEARCH

但是：

这个结论只代表：

V12 已探索的候选空间
+
其固定晋级门槛

没有找到 PAPER_CANDIDATE。

它不代表：

整个项目没有创新空间。

V13 的目标：

# 从 V12 的失败和强控制中提取新信息，
# 然后进入更深层、更高创新性的搜索。

最终目标不是：

找到一个 +0.001 的 tweak。

而是：

Innovation 1 confirmed

然后继续：

Innovation 2 confirmed

最后：

I1 + I2

形成：

PAPER_CORE_READY。

---

# 1. FIRST: RE-AUDIT V12

首先读取：

AUTONOMOUS_LP_RESEARCH_V12/

包括：

FINAL_REPORT.md
results.json
EXPERIMENT_LEDGER.tsv
IDEA_LEDGER.md
BLACKLIST.md
BEST_STATE.md
status.json

不要只读最终结论。

提取：

每个 candidate

每个 matched control

每个 unexpected strong control

的：

MRR
delta
params
runtime
family
mechanism。

输出：

AUTONOMOUS_LP_RESEARCH_V13/00_V12_SIGNAL_AUDIT.md

---

# 2. V12 已知正式结论

V12：

44 actual training jobs

39 / 40 Stage-1-equivalent Phase-1 budget

Innovation 1:

NOT_FOUND

Innovation 2:

NOT_SEARCHED

test:

NOT EVALUATED

因此：

V13 重新开始 Phase 1。

Test 继续封存。

---

# 3. 不允许简单重跑 V12

以下 candidate lineage：

F1
F2
F3
D1
D2R
C1
C2
G1
G2
H1
X1 candidate
X2 candidate
B2 candidate

不得原样重跑。

已经证伪的具体 mechanism：

加入 BLACKLIST。

---

# 4. 但 V12 的强 control 不进入 blacklist

重点审计以下 V12 信号：

- X1_RAW
- X2_SELF
- B2_SCALE
- D2_CROSS
- C2_COS

以及任何：

candidate < control
但 control > QTHS25

的情况。

这些不是失败垃圾。

它们是：

# CONTROL-DERIVED SIGNALS

自动记录到：

CONTROL_SIGNAL_LEDGER.md

---

# 5. Control signal promotion principle

V12 中如果：

某 control

虽然未达到正式 +0.003 gate，

但：

delta > 0

且：

不是明显随机噪声型 control

且：

来自独立信息源，

允许把它视为：

WEAK_PRIMITIVE

而不是 PAPER_CANDIDATE。

目的：

寻找：

多个弱但机制正交的 signal

是否可以形成一个统一的新方法。

---

# 6. Phase A — Control-derived composition

先不要立即再次 broad search。

先做一次：

# EVIDENCE COMPOSITION SEARCH

只允许使用 V12 已经显示正 signal 的 primitives。

---

# 7. Candidate primitives

根据当前 V12 结果审计，优先考虑：

## P1 — Raw-HG pair representation residual

来自：

X1_RAW

含义：

Raw-HG pair representation

可能有独立信息。

---

## P2 — Within-view pair self-moment

来自：

X2_SELF

含义：

pair-level second/self interaction

可能比 cross-view product 更有效。

---

## P3 — Structural scalar calibration

来自：

B2_SCALE

例如：

degree
common-neighbor

score calibration。

---

## P4 — Cross-neighborhood density

来自：

D2_CROSS

target-masked exclusive-neighborhood cross density。

---

## P5 — Raw feature cosine

来自：

C2_COS

优先级低于 P1-P4。

---

# 8. Phase A 原则

禁止：

P1 + P2 + P3 + P4 + P5

全部直接 concat。

那只是 feature soup。

必须形成：

一个明确数学原则。

Autoresearch 必须先提出：

最多 3 个 coherent compositions。

每个 composition 回答：

为什么这些 primitive 属于同一个 mechanism？

---

# 9. 推荐的第一个 unified hypothesis

优先考虑：

# Pair Evidence Residual Calibration

核心思想：

当前 decoder 主要根据 learned embeddings 给 link score。

但 V12 weak controls 暗示：

pair-specific evidence

可能来自三个不同层次：

1.
learned pair representation

2.
local structural evidence

3.
raw / higher-order view evidence

因此：

构造：

base_score

+

small residual evidence calibrator

但要求：

每个 evidence channel：

单独标准化

零初始化 residual

最终仍输出：

scalar correction。

---

# 10. 不允许大 MLP

Phase A 的目标不是：

多加参数。

Residual calibrator：

必须很小。

优先：

linear / low-rank

或：

每 channel 一个 scalar

加：

一个 interaction term。

新增参数：

尽量 < 2% baseline。

---

# 11. Phase A Candidate A — ECR

暂称：

ECR
Evidence-Calibrated Residual

输入最多使用：

Raw-HG pair evidence

+
degree/CN structural evidence

+
cross-neighborhood density

不要一开始加入 feature cosine。

输出：

delta_score

最终：

score =
base_score + delta_score

---

# 12. ECR controls

必须运行：

A0
QTHS25 baseline

A1
Raw-HG residual only

A2
structural scalar only

A3
cross-density only

A4
same-parameter shuffled-evidence control

A5
full ECR

如果：

A5 <= max(A1,A2,A3)

则：

没有组合价值。

REJECT。

---

# 13. Additive gate

ECR 必须：

A5 - baseline >= +0.003

并：

A5 - best_single >= +0.002

才能 Stage2。

否则：

组合只是堆弱 signal。

REJECT。

---

# 14. Phase A Candidate B — Factorized Pair Calibration

如果 ECR FAIL：

测试一个更原则化的版本：

score =
base_score
+
a * semantic_pair
+
b * structural_pair
+
c * semantic_pair * structural_pair

其中：

semantic_pair

只来自 learned / Raw-HG pair representation。

structural_pair

只来自 train-only structure。

参数：

a,b,c

或小型 low-rank equivalent。

禁止：

深 MLP。

目的：

测试：

semantic × structural evidence interaction。

---

# 15. Factorized controls

B0:
baseline

B1:
semantic only

B2:
structural only

B3:
additive semantic + structural

B4:
factorized interaction

如果：

B4 <= B3

interaction 无价值。

REJECT。

---

# 16. Phase A stop

最多：

3 个 coherent composition candidates。

如果全部失败：

CONTROL_COMPOSITION_EXHAUSTED。

然后进入 Phase B。

不要围绕这些弱 controls 调几十个组合。

---

# 17. Phase B — Deep new-family search

Phase B 不再做 V12 风格的小 perturbation。

优先探索：

真正未充分验证的高信息 family。

顺序：

1.
negative hardness trajectory

2.
candidate-set ranking objective

3.
pair-state decoder

4.
graph/raw-HG cross-view distillation

5.
structural encoder innovation

---

# 18. Family T — Hardness trajectory

必须真正实现：

same negative candidate

across multiple teacher checkpoints

的 trajectory。

注意：

V12 G2 是：

positive difficulty EMA。

它不等价于：

negative candidate hardness trajectory。

所以该 family：

NOT BLACKLISTED。

---

# 19. T1 — Persistent Hardness Selection

固定：

20 candidates per positive。

保存 teacher epochs：

1...10

的 candidate ranks。

定义：

persistence(n) =
min_t rank_percentile_t(n)

选择：

max persistence candidate。

也就是：

maximin persistent hard negative。

---

# 20. T1 controls

Final snapshot hard

Mean-rank hard

Trajectory shuffled

Final-rank matched

SH75

QTHS25

如果 T1 不能：

> trajectory-shuffle
> final-rank matched

则机制失败。

---

# 21. Family L — Candidate-set objective

当前：

K=1 training negative

可能是根本瓶颈。

允许：

保持最终 sampler protocol 不变，

但训练 objective 可以观察：

20-candidate pool。

这不是：

简单增加 20 个 independent negatives。

而是：

对 candidate set 建模。

---

# 22. L1 — Setwise Rank Calibration

对于每个 positive：

positive score:

s+

20 candidate scores:

s1...s20

设计：

parameter-free / low-param

setwise rank surrogate

目标：

直接提升：

positive relative rank

而非：

20 个独立 BCE。

---

# 23. L1 compute control

因为 L1 看 20 candidates，

必须有：

C1:
20-candidate independent BCE

C2:
20-candidate random-set listwise

C3:
same compute repeated K=1 BCE

如果：

L1 gain 只是更多 negatives / compute：

REJECT。

---

# 24. L1 metric alignment

目标是 MRR。

候选 loss 必须解释：

为什么 surrogate

比 binary BCE

更接近：

positive rank。

禁止：

只换成 generic contrastive loss。

---

# 25. Family P — Pair-state decoder

V12 C1：

simple symmetric product MLP

失败。

这不意味着：

pair representation family exhausted。

但禁止：

另一个 generic concat MLP。

---

# 26. P1 — Explicit Pair State

构造一个：

pair state

而不是：

node embeddings 直接 decoder。

pair state 至少包含：

symmetric difference

Hadamard product

以及：

one structural evidence channel。

通过：

low-rank symmetric transformation

输出 score。

---

# 27. P1 parameter control

必须：

same-parameter generic MLP

same-dimension concat decoder

base decoder

三者比较。

如果：

P1 <= generic MLP

REJECT。

---

# 28. Family V — Cross-view distillation

历史证明：

Raw Hypergraph 是一个有用 view。

但：

routing
veto
orthogonal residual

都失败。

新的方向：

不要 fusion representation。

改成：

# pair-score distillation / disagreement regularization

---

# 29. V1 — Pair-score Cross-view Distillation

Graph branch

和 Raw-HG branch

分别产生：

pair score。

主 decoder：

只使用最终目标 branch。

辅助：

让两 branch

只在：

高置信 training pairs

上保持局部 rank consistency。

不是：

直接 feature concatenation。

---

# 30. V1 controls

same compute shuffled pair alignment

score mean matching

feature-level alignment

no distillation

如果：

V1 <= shuffled

REJECT。

---

# 31. Family S — Structural encoder

只有 Phase B 前四 family 没有候选进入 Stage2，

才进入。

不要一开始烧大量 GPU。

允许：

new encoder structure

但必须：

不是旧 hypergraph operator variation。

---

# 32. Structural candidates

优先考虑：

edge-centric / pair-centric message passing

而不是：

node-centric GNN 加一层。

例如：

pair-aware residual propagation

line-graph-like local edge state

target-masked edge context

但：

不能直接复刻 SEAL/DRNL 经典结构。

先做 novelty search。

---

# 33. Phase B Autoresearch budget

每 family：

最多：

4 independent candidates

每 candidate：

最多 1 targeted revision。

Phase B 总：

最多 50 Stage1-equivalent。

如果一个 family：

连续 4 个 candidate

都没有：

delta >= +0.002

则：

FAMILY_EXHAUSTED。

转下一 family。

---

# 34. Stage1

Cora

seed0

5 epochs

QTHS25 strong baseline

test disabled。

Candidate 必须比较：

baseline

candidate

matched control。

---

# 35. Stage1 gate

Promotion：

candidate - QTHS25

>= +0.003 absolute

或：

>= +1% relative

并且：

candidate > matched control。

保持严格。

不要降低门槛。

---

# 36. Near-signal exception

V13 唯一允许的 near-signal exception：

如果：

delta in [+0.002,+0.003)

并且：

matched-control margin >= +0.002

并且：

机制非常清晰

允许：

一次 10-epoch seed0 confirmation。

标记：

NEAR_SIGNAL_CONFIRMATION。

每 family 最多一次。

---

# 37. Stage2

Cora

seed0

10 epochs。

候选必须：

>= +0.003

或：

>= +1%

相对：

matched QTHS25

并保持：

mechanism-control win。

---

# 38. Stage3

Cora

seeds 0/1/2

10 epochs。

需要：

candidate > QTHS25

至少：

2/3 seeds

mean gain >0

并：

mechanism control passed。

达到：

LOCAL_GO。

---

# 39. Test

只有：

LOCAL_GO

才允许：

Cora test。

一次性。

不根据 test 调方法。

---

# 40. Cross dataset

Cora test supported：

PubMed

3 seeds

然后：

Citeseer

如果必要。

至少一个额外 dataset

必须有正 signal。

---

# 41. Innovation 1 freeze

找到满足：

Cora 3-seed

Cora test

one extra dataset

mechanism control

novelty acceptable

的 candidate：

冻结：

INNOVATION_1。

写：

INNOVATION_1.md

commit

hash

protocol

results

novelty

mechanism。

---

# 42. 找到 Innovation 1 后不要停

立即进入：

# PHASE 2 — Innovation 2 Search

Phase2 的规则：

沿用 V12 supplement。

但增加：

Innovation 2

必须优先来自：

与 I1 不同 family。

---

# 43. Phase2 priority

如果 I1 是：

trajectory / sampling

I2 优先：

setwise objective
pair decoder
encoder

如果 I1 是：

loss

I2 优先：

pair decoder
structural representation
sampling

如果 I1 是：

decoder

I2 优先：

trajectory
loss
positive-side learning。

---

# 44. I2 experiment matrix

每个 I2 Stage1：

Baseline

I1

I2

I1+I2

matched control

全部：

same Cora seed0
5 epochs。

---

# 45. I2 gate

Independent:

I2 - Baseline >= +0.003

或 relative >=1%

或：

Additive:

I1+I2 - I1 >= +0.002

并胜 matched control。

---

# 46. I2 confirmation

Stage2：

10 epoch seed0

Stage3：

3 seeds

Test：

only after LOCAL_GO

Cross dataset：

one additional dataset。

---

# 47. PAPER_CORE_READY

最终优先停止条件：

I1 confirmed

I2 confirmed

I1+I2

>= max(I1,I2)

至少：

+0.002 mean MRR

至少：

2/3 seeds

并：

extra dataset support

combined novelty acceptable

paper story coherent。

---

# 48. 新增重要规则：Baseline context consistency

V12 暴露了：

candidate 在 SH75 环境有信号

换 QTHS25 后失败。

V13 开始：

所有 Stage1 candidate：

从第一步就必须使用：

同一个 frozen strong baseline context。

当前默认：

QTHS25。

禁止：

弱 sampler 上筛选
→ 强 sampler 上确认

这种 context shift。

除非：

candidate 本身研究 sampler。

---

# 49. Sampler innovation 特例

如果 candidate 本身是 sampler：

比较：

Graph-hard
QTHS25
SH75
CPTS

candidate

matched control。

不能把 QTHS25 固定在 candidate 上。

---

# 50. Training budget consistency

Stage1：

明确写：

5 epochs。

Stage2：

10 epochs。

记录：

实际 epoch count。

如果：

checkpoint metadata

和 requested epochs 不一致：

实验无效。

这点必须加 assertion。

---

# 51. Automated assertions

每次 experiment 启动前检查：

sampler context

seed

epoch count

dataset split hash

train pool hash

validation candidate hash

test disabled

strong baseline identity。

任何不匹配：

INVALID_EXPERIMENT

不要进入 ledger performance comparison。

---

# 52. Candidate collision audit

进入 Stage2 前：

focused literature search。

特别检查：

candidate 是否只是：

已知 SEAL feature
known heuristic decoder
known listwise LP loss
known hard-negative trajectory method

换名字。

如果 exact：

BLACKLIST。

---

# 53. Experiment parallelization

V12 每个 job 显存很小。

V13 可以更积极并发。

先 benchmark：

1 job
2 jobs
4 jobs
8 jobs

记录：

wall-clock throughput

GPU utilization

memory

如果：

4/8 jobs

不显著降低 throughput

则：

Stage1 batch

并发执行。

目标：

最大化：

experiments / hour。

---

# 54. 不允许等待人工确认

只要：

budget 未耗尽

且：

没有 PAPER_CORE_READY

自动继续。

不要：

在一个 family 失败后停止。

---

# 55. Search budget

V13 Phase1：

最多：

Phase A 组合：
10 Stage1-equivalent

Phase B：
50 Stage1-equivalent

总：

60 Stage1-equivalent

GO candidates：

Stage2/3/test 不计入该 Stage1 cap。

Phase2：

找到 I1 后

额外：

30 Stage1-equivalent

寻找 I2。

---

# 56. Stop conditions

优先：

PAPER_CORE_READY

其次：

ONE_STRONG_INNOVATION_FOUND

只有当：

I1 confirmed

但 Phase2 30 budget exhaust

才允许。

如果：

Phase1 60 budget exhaust

至少 5 deep families explored

仍无 I1：

NO_EXECUTABLE_IDEA_AFTER_DEEP_SEARCH。

---

# 57. 不再接受 broad micro-tweak search

V13 禁止：

再生成 20 个：

small scalar
minor weight
simple cosine
tiny residual

的同义候选。

如果一个 candidate：

没有新的 information source

没有新的 optimization principle

没有新的 representation primitive

则：

IDEA_REJECT_PREEXPERIMENT。

---

# 58. 每个 candidate 必须回答

NEW_INFORMATION:

这个方法使用了 baseline 没使用的什么信息？

OR

NEW_PRINCIPLE:

它改变了什么训练/推理原则？

如果两者都答不出来：

不跑。

---

# 59. 最终输出目录

创建：

AUTONOMOUS_LP_RESEARCH_V13/

program.md

00_V12_SIGNAL_AUDIT.md

CONTROL_SIGNAL_LEDGER.md

IDEA_LEDGER.md

EXPERIMENT_LEDGER.tsv

EXPERIMENT_QUEUE.tsv

BLACKLIST.md

BEST_STATE.md

INNOVATION_1.md

INNOVATION_2.md

PAPER_STORY.md

NOVELTY_LEDGER.md

results.json

FINAL_REPORT.md

---

# 60. FINAL_REPORT

输出：

STATUS:

V12_LEARNINGS:

CONTROL_SIGNALS:

PHASE_A:
...

PHASE_B:
...

FAMILIES_EXPLORED:

TOTAL_STAGE1_EQUIVALENTS:

TOTAL_TRAINING_JOBS:

BEST_CANDIDATE:

BEST_BASELINE:

VALIDATION:

TEST:

CROSS_DATASET:

MECHANISM_CONTROL:

NOVELTY:

INNOVATION_1:

INNOVATION_2:

I1_I2_COMBINATION:

ADDITIVE_GAIN:

PAPER_STORY:

FINAL_DECISION:

PAPER_CORE_READY
/
ONE_STRONG_INNOVATION_FOUND
/
NO_EXECUTABLE_IDEA_AFTER_DEEP_SEARCH
/
BLOCKED_BY_INFRASTRUCTURE

NEXT_EXPECTED_STEP:

---

# 61. C2C HANDOFF

最终返回：

STATUS: EXECUTED

AUTORESEARCH:
V13

V12_SIGNAL_MINING:
...

PHASE_A:
...

PHASE_B:
...

INNOVATION_1:
...

INNOVATION_1_EVIDENCE:
...

INNOVATION_2:
...

INNOVATION_2_EVIDENCE:
...

COMBINATION:
...

CROSS_DATASET:
...

NOVELTY:
...

TOTAL_EXPERIMENTS:
...

GPU_TIME:
...

DECISION:
...

NEXT_EXPECTED_STEP:
...

---

# 62. 最重要原则

V12 已经证明：

“广撒小 tweak”

对当前强 QTHS25 baseline

收益很低。

V13 必须改变搜索策略：

# 先利用 V12 暴露的弱控制信号寻找 coherent composition，
# 再进入真正未充分探索的高信息 family，
# 找到 I1 后继续找正交 I2。

目标不是：

更多实验。

目标是：

更高的信息增益 / 每次实验。

现在立即开始 V13。