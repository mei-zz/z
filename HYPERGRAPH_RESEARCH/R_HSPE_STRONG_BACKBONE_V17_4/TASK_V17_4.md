# V17.4 — R-HSPE STRONG-BACKBONE TRANSFER

STATUS: INNOVATION_1_FINAL_COMPETITIVENESS TEST

GOAL:

验证已经冻结的：

# R-HSPE

是否能够作为：

# hypergraph-specific pair-context plug-in

为现有强 pairwise link-prediction backbone：

NCN
NCNC

提供额外、稳定、跨数据集的增益。

本实验：

不是 Innovation 2。

不是重新设计 R-HSPE。

不是为了调到超过 NCNC 而修改方法。

---

# 1. PRIOR STATE

读取：

HYPERGRAPH_RESEARCH/R_HSPE_FROZEN/

HYPERGRAPH_RESEARCH/HSPE_V17_2/

HYPERGRAPH_RESEARCH/R_HSPE_BENCHMARK_V17_3/

确认：

R-HSPE = FROZEN

V17.3 competitiveness:

WEAK

原因：

R-HSPE standalone

明显低于：

NCN / NCNC。

---

# 2. CORE QUESTION

V17.4 只回答：

\[
\boxed{
NCNC + R\text{-}HSPE
>
NCNC\ ?
}
\]

以及辅助问题：

\[
NCN + R\text{-}HSPE
>
NCN\ ?
\]

如果成立：

说明 R-HSPE

提供了 strong graph pairwise predictor

尚未充分编码的：

# hypergraph-specific candidate context。

此时 R-HSPE 可以作为：

backbone-compatible plug-in

而不是 standalone SOTA predictor。

---

# 3. HARD FREEZE R-HSPE

必须 exact reuse：

V17.2 frozen R-HSPE。

冻结：

training-only ECDF

size-rank descriptors

token construction

shared-support construction

set encoder

mean/max pooling

explicit count features

hidden dimension

residual head

zero initialization

parameter count

target masking。

禁止任何修改。

记录：

source hash
config hash。

如果无法与：

R_HSPE_FROZEN

一致：

STOP。

---

# 4. STRONG BACKBONES

使用 V17.3 已经公平重跑的：

# NCN

和：

# NCNC

exact implementation。

必须复用：

same official source

same adapter

same training protocol

same dataset split

same candidates

same evaluator

same graph projection

same hyperparameters。

不要：

重新调 NCN/NCNC。

---

# 5. INTEGRATION RULE

只允许一种 integration：

假设 strong backbone

输出 pre-sigmoid logit：

s_backbone(u,v)

R-HSPE 输出：

delta_h(u,v)

则：

s_final(u,v)
=
s_backbone(u,v)
+
delta_h(u,v)

R-HSPE final residual layer：

zero initialization。

因此 initialization 时：

s_final
==
s_backbone

最大绝对误差：

<= 5e-7。

---

# 6. DO NOT CONCAT EMBEDDINGS

禁止：

把 R-HSPE embedding

拼进：

NCN node embedding

NCNC common-neighbor embedding

或者修改：

NCN/NCNC message passing。

本轮只测试：

# decoder-level residual plug-in。

这样能保持：

R-HSPE

作为独立模块。

---

# 7. TRAINING POLICY

主实验采用：

# joint training under identical backbone protocol

也就是说：

NCN baseline

和：

NCN + R-HSPE

使用完全相同：

initialization seed
optimizer
LR
epochs
training examples
negative samples。

NCN+R-HSPE：

唯一增加：

frozen-definition R-HSPE module。

NCNC 同理。

“frozen R-HSPE”

表示：

方法定义和超参冻结，

不是参数停止学习。

R-HSPE 参数仍按照训练目标学习。

---

# 8. ARMS

正式 arms：

## N0
NCN

## N1
NCN + R-HSPE

## C0
NCNC

## C1
NCNC + R-HSPE

此外增加一个：

## C2
NCNC + PARAMETER-MATCHED NULL RESIDUAL

用于排除：

只是额外参数 / residual pathway

产生增益。

---

# 9. PARAMETER-MATCHED NULL

C2：

使用与 R-HSPE

完全相同：

新增 trainable parameter count

和 residual-head depth。

但输入：

固定常量 vector。

禁止访问：

hyperedge context

size rank

token count

support count

node degree

candidate structure。

它最多学习：

generic residual calibration。

要求：

added parameters

与 C1

完全相同

或误差 <= 1 parameter。

---

# 10. DATASETS

第一阶段：

Cora

PubMed

不要先跑 Citeseer。

原因：

快速决定是否值得继续。

所有数据：

复用 V17.3。

禁止：

重新下载 dataset

重新划 split

重新构造 alternative negatives。

---

# 11. REUSE BASELINES

如果 V17.3 中：

N0 NCN

C0 NCNC

与当前协议：

dataset
seed
epochs
split
candidate hash
source hash
hyperparameters

完全相同，

允许直接复用。

不要重复训练。

任何 mismatch：

重新运行对应 baseline。

---

# 12. PHASE A — FAST TRANSFER SCREEN

运行：

Cora
PubMed

seeds:

0
1
2

epochs:

5

validation only

test OFF。

需要的新训练：

N1
C1
C2

以及不能合法复用的：

N0/C0。

---

# 13. PRIMARY COMPARISON

最重要：

# C1 vs C0

即：

NCNC + R-HSPE
vs
NCNC。

对每个 dataset

报告：

Delta_NCNC =
MRR(C1)-MRR(C0)

per seed

mean

median

std

wins。

---

# 14. SECONDARY COMPARISON

报告：

Delta_NCN =
MRR(N1)-MRR(N0)。

它用于判断：

R-HSPE

是否：

backbone-independent。

但最终第一创新生死

优先看：

NCNC。

---

# 15. NULL CONTROL

报告：

Delta_null =
MRR(C1)-MRR(C2)。

如果：

C1 <= C2

则说明：

强 backbone 上的提升

可能由：

generic residual capacity

解释。

这是严重警告。

---

# 16. PHASE A GO RULE

对于：

Cora

和：

PubMed

分别要求：

NCNC + R-HSPE

相比 NCNC：

至少：

2/3 seeds positive

且：

mean Delta_NCNC > 0

且：

median Delta_NCNC > 0。

同时：

C1 > C2

至少：

2/3 seeds

且：

mean(C1-C2) > 0。

不再硬要求：

+0.002。

原因：

NCNC 当前 MRR 已接近高位，

本轮目标是检测：

稳定的 complementary gain，

而不是 arbitrary absolute threshold。

---

# 17. CROSS-DATASET PHASE A

只有：

Cora PASS

AND

PubMed PASS

才进入：

Phase B。

如果：

只有一个 dataset PASS：

输出：

STRONG_BACKBONE_TRANSFER_DATASET_DEPENDENT

停止。

如果：

两个都 FAIL：

输出：

R_HSPE_REDUNDANT_TO_NCNC

停止。

禁止 rescue。

---

# 18. NCN INTERPRETATION

如果：

NCN + R-HSPE

也在：

Cora + PubMed

同时 positive，

标记：

BACKBONE_INDEPENDENT_TRANSFER_SUPPORTED。

如果：

只有 NCNC positive：

也不阻止晋级。

最终论文可以：

以 NCNC

作为 host backbone。

---

# 19. PHASE B — FORMAL CONFIRMATION

Phase A GO 后：

运行：

Cora
PubMed

seeds:

0
1
2
3
4

epochs:

10

validation only。

arms：

N0
N1
C0
C1
C2。

能合法复用：

V17.3 exact baselines

则复用。

---

# 20. FORMAL NCNC GATE

每个 dataset：

C1 > C0

至少：

4/5 seeds

mean delta > 0

median delta > 0。

同时：

C1 > C2

至少：

3/5 seeds

mean margin > 0。

如果满足：

STRONG_BACKBONE_TRANSFER_CONFIRMED。

---

# 21. WHY NO ABSOLUTE +0.002 GATE

不要使用：

固定 +0.002

作为最终硬门槛。

因为：

NCNC baseline

已经处于高 MRR 区域，

incremental complementarity

应通过：

paired consistency

effect direction

mean/median

来判断。

但必须完整报告：

absolute delta。

如果增益：

极小到实际无意义，

在 FINAL_REPORT

明确标记：

STATISTICALLY_DIRECTIONAL_BUT_SMALL。

---

# 22. THIRD DATASET

只有：

Cora + PubMed

正式通过：

才运行：

Citeseer。

使用：

exact V17.3 protocol。

seeds：

0
1
2

epochs：

10

validation only。

主要：

C0 NCNC

C1 NCNC+R-HSPE

C2 Null。

---

# 23. CITESEER SUPPORT

要求：

C1 > C0

至少：

2/3 seeds

mean > 0。

如果通过：

THREE_DATASET_TRANSFER_SUPPORTED。

如果不通过：

保留：

Cora+PubMed transfer

但标记：

THIRD_DATASET_TRANSFER_FAIL。

不 rescue。

---

# 24. TEST POLICY

直到：

Phase B Cora+PubMed

正式通过前：

TEST OFF。

如果通过：

integration configuration

完全冻结。

然后：

one-shot test。

---

# 25. TEST — CORA

使用：

10-epoch final frozen integration。

seeds0..4

arms：

C0
C1
C2。

以及：

N0/N1

如果正式 validation

NCN transfer 有意义。

---

# 26. TEST — PUBMED

同样：

C0
C1
C2

5 seeds。

禁止：

test-driven adjustment。

---

# 27. TEST — CITESEER

如果：

Citeseer validation positive，

运行：

3 seeds

one-shot test。

---

# 28. FINAL TEST SUPPORT

Cora：

C1 > C0

至少：

4/5

mean >0

median >0。

PubMed：

C1 > C0

至少：

3/5

mean >0

median >0。

Citeseer：

如果运行，

至少：

2/3 positive

mean >0。

---

# 29. METRICS

全部报告：

MRR

Hits@10

Hits@20

Mean Positive Rank。

Primary：

MRR。

不得：

因为 PubMed Hits@10

与 MRR方向不同

而隐藏 Hits@10。

---

# 30. PAPER MAIN TABLE

如果成功：

新增最终方法：

# NCNC + R-HSPE

加入 V17.3 main table：

B0

R-HSPE standalone

NCN

NCNC

NCN + R-HSPE

NCNC + R-HSPE。

重新计算：

rank。

---

# 31. SUCCESS INTERPRETATION

如果：

NCNC+R-HSPE

在：

Cora

PubMed

Citeseer

稳定高于 NCNC，

则创新定位修改为：

> R-HSPE is a lightweight hypergraph-specific
> candidate-context plug-in that provides
> complementary structural information
> to strong pairwise graph link predictors.

这是最理想结果。

---

# 32. VERY IMPORTANT CLAIM

即使成功：

不要声称：

hyperedge size itself causes the gain。

保留：

MECHANISM =
CONTEXT_DRIVEN

SIZE_CAUSAL_CLAIM =
NOT_SUPPORTED。

新的强证据是：

# complementarity to strong pairwise graph backbone

而不是：

size causality。

---

# 33. IF IT FAILS

如果：

NCNC + R-HSPE

在 Cora/PubMed

不能稳定胜：

NCNC，

则：

输出：

# R_HSPE_REDUNDANT_TO_STRONG_PAIRWISE_BACKBONE

解释：

R-HSPE 对弱 hypergraph baseline

有效，

但其信息可能已被：

NCN/NCNC

强 pairwise representation

间接覆盖。

不要：

修改 R-HSPE

来 rescue。

---

# 34. NO RESCUE

禁止：

改变 ECDF

改 token

增加 hidden size

attention

gating

learned fusion

concat NCNC embeddings

tune residual weight

新增 hypergraph features

调整 sampler

换 loss。

只能：

固定 additive residual。

---

# 35. PARAMETER REPORT

记录：

NCN params

NCNC params

NCN+R-HSPE params

NCNC+R-HSPE params

added parameters

percentage overhead。

重点报告：

R-HSPE

相对 NCNC

额外参数比例。

---

# 36. COST REPORT

记录：

training time

inference time

feature-cache time

peak GPU memory。

如果：

R-HSPE 增益成立

且成本很低，

这是论文的重要优势。

---

# 37. OUTPUT DIRECTORY

创建：

HYPERGRAPH_RESEARCH/R_HSPE_STRONG_BACKBONE_V17_4/

包含：

00_AUDIT.md

01_INTEGRATION.md

02_PHASE_A.md

03_PHASE_B.md

04_CITESEER.md

05_TEST.md

06_MAIN_TABLE.md

07_INTERPRETATION.md

results.json

FINAL_REPORT.md

---

# 38. FINAL DECISION STATES

允许：

R_HSPE_REDUNDANT_TO_NCNC

STRONG_BACKBONE_TRANSFER_DATASET_DEPENDENT

STRONG_BACKBONE_TRANSFER_CONFIRMED

BACKBONE_INDEPENDENT_TRANSFER_SUPPORTED

THREE_DATASET_TRANSFER_SUPPORTED

STATISTICALLY_DIRECTIONAL_BUT_SMALL

INNOVATION_1_PAPER_READY

---

# 39. INNOVATION 1 PAPER-READY RULE

只有：

Cora test：

NCNC+R-HSPE > NCNC

且：

PubMed test：

NCNC+R-HSPE > NCNC

都满足正式 consistency gate，

并且：

C1 > parameter-matched null

验证支持，

才允许：

# INNOVATION_1_PAPER_READY

Citeseer positive：

作为额外强化证据。

---

# 40. FINAL REPORT

必须输出：

R_HSPE_FROZEN:
TRUE

NCN_BASELINE:
...

NCN_PLUS_R_HSPE:
...

NCNC_BASELINE:
...

NCNC_PLUS_R_HSPE:
...

PARAM_NULL:
...

CORA_DELTA:
...

PUBMED_DELTA:
...

CITESEER_DELTA:
...

SEED_WINS:
...

TEST:
...

PARAMETER_OVERHEAD:
...

RUNTIME_OVERHEAD:
...

BACKBONE_INDEPENDENT:
...

COMPLEMENTARY_SIGNAL:
SUPPORTED / NOT_SUPPORTED

MAIN_TABLE_RANK:
...

INNOVATION_1:
PAPER_READY / NOT_PAPER_READY

NEXT_EXPECTED_STEP:
...

---

# 41. C2C HANDOFF

STATUS: EXECUTED

DIRECTION:
R_HSPE_STRONG_BACKBONE_TRANSFER

R_HSPE:
FROZEN

PHASE_A:
...

PHASE_B:
...

CORA:
...

PUBMED:
...

CITESEER:
...

NCN_TRANSFER:
...

NCNC_TRANSFER:
...

NULL_CONTROL:
...

TEST:
...

PARAMETER_COST:
...

COMPETITIVENESS:
...

INNOVATION_1:
...

DECISION:
...

NEXT_EXPECTED_STEP:
...

完成后停止。

# 不要自动开始 Innovation 2。