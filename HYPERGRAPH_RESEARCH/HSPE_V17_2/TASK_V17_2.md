# V17.2 — R-HSPE INNOVATION-1 FREEZE

STATUS: FINAL_CONFIRMATION_ONLY

目标：

# 不再开发 R-HSPE。
# 完成最终泛化、测试、novelty 和 artifact freeze。
# 成功后正式冻结 Innovation 1，并开始 Innovation 2。

---

## 1. PARENT

读取：

HYPERGRAPH_RESEARCH/HSPE_V17_1/

确认：

FINAL_VARIANT = R-HSPE

HSPE_VALIDATION_CONFIRMED

METHOD INTERPRETATION:

HSPE_CONTEXT_DRIVEN

SIZE_CONTENT_CAUSAL_CLAIM:

NOT SUPPORTED

不得修改任何方法定义。

---

## 2. HARD FREEZE

冻结以下全部内容：

R-HSPE token definition

training-only ECDF rank normalization

set encoder

pooling

explicit count features

residual head

zero initialization

parameter count

Raw-HG DCDLP backbone

QTHS25

optimizer

learning rate

epochs

negative sampling

target masking

validation/test evaluator。

记录全部：

source hashes
config hashes
split hashes。

如果任何值与 V17.1 final variant 不一致：

STOP。

---

## 3. NO MORE TUNING

从此禁止：

hidden-dim tuning

pooling tuning

rank transform tuning

adding size features

adding count features

attention

motifs

overlap

changing sampler

changing loss

changing epochs based on test。

---

## 4. FROZEN TEST — CORA

使用 V17.1 frozen final protocol。

Cora：

seeds 0,1,2,3,4

10 epochs / corresponding frozen final checkpoints

one-shot TEST。

运行：

B0
R-HSPE

以及：

best context-only control from V17.1

用于 claim scope。

绝不根据 test 修改模型。

报告：

MRR
Hits@10
Hits@20
mean positive rank

以及：

per-seed paired delta

mean
std
median
wins。

---

## 5. FROZEN TEST — PUBMED

完全相同：

PubMed

seeds 0..4

B0
R-HSPE
best context-only control

one-shot TEST。

---

## 6. TEST SUPPORT

Innovation 1 test support 要求：

Cora：

R-HSPE > B0

至少 4/5 seeds

mean delta > 0

median delta > 0。

PubMed：

R-HSPE > B0

至少 3/5 seeds

mean delta > 0

median delta > 0。

不设置：

R-HSPE 必须胜 context-control

的硬门槛。

context control 只限制 mechanism claim。

---

## 7. THIRD-DATASET FROZEN CHECK

使用：

Citeseer

或者当前代码中最自然、无需改变方法的第三 dataset。

不得：

针对第三数据集调任何参数。

使用：

同一个 frozen R-HSPE。

seeds:

0,1,2

10 epochs

validation first。

如果 validation 平均：

R-HSPE > B0

则允许一次 frozen test。

如果没有提升：

记录：

THIRD_DATASET_NOT_SUPPORTED

但不要回头调方法。

---

## 8. NOVELTY AUDIT

完成 focused literature audit。

重点：

OFSH / OHAA

NSLR-HMANN

NCN / NCNC

HMNE

HMRLH

HP2PH

Hyperedge Copy Model

HNHN / standard hyperedge-degree normalization

recent 2026 pairwise hypergraph link-prediction work。

建立：

NOVELTY_MATRIX.md

每篇记录：

task

representation unit

candidate-specific?

uses incident hyperedge identities?

uses hyperedge cardinality?

constructs hyperedge-size PAIRS?

set-valued pair encoder?

rank-normalization?

decoder-level or encoder-level?

exact collision?

---

## 9. CLAIM BOUNDARY

禁止 claim：

"first to use hyperedge size"

"hyperedge size is the cause of the gain"

"rank normalization alone is the primary innovation"

"first order-aware hypergraph link predictor"

允许的候选 claim：

> R-HSPE explicitly constructs a candidate-specific
> hyperedge-pair context for pairwise link prediction
> and encodes that context as a permutation-invariant
> pair representation, with training-only rank-normalized
> hyperedge cardinality descriptors reducing
> cross-graph scale sensitivity.

如果 novelty audit 找到 exact method：

标记：

NOVELTY_CONFLICT

立即汇报。

不要偷偷修改 R-HSPE。

---

## 10. FREEZE ARTIFACT

如果：

Cora test support

AND

PubMed test support

AND

no exact novelty collision

创建：

HYPERGRAPH_RESEARCH/R_HSPE_FROZEN/

包含：

R_HSPE_FROZEN.md

METHOD_DEFINITION.md

NOVELTY_MATRIX.md

TEST_RESULTS.json

FINAL_CONFIG.json

SOURCE_HASHES.json

以及必要 checkpoint references。

---

## 11. R_HSPE_FROZEN.md

必须明确记录：

INNOVATION_1:
R-HSPE

STATUS:
FROZEN

PRIMARY_CLAIM:
candidate-specific hyperedge-pair context encoding

SECONDARY_COMPONENT:
training-only rank-normalized hyperedge cardinality

MECHANISM_STATUS:
CONTEXT_DRIVEN

SIZE_CAUSAL_CLAIM:
NOT_SUPPORTED

CORA_VALIDATION:
...

PUBMED_VALIDATION:
...

CORA_TEST:
...

PUBMED_TEST:
...

THIRD_DATASET:
...

PARAMETER_OVERHEAD:
...

NOVELTY_STATUS:
...

CODE_HASH:
...

CONFIG_HASH:
...

NO_FURTHER_TUNING:
TRUE

---

## 12. FINAL DECISION

只有以下情况：

Cora test supported

PubMed test supported

no exact collision

输出：

# INNOVATION_1_FROZEN

否则：

输出明确原因：

TEST_GENERALIZATION_FAIL

或：

NOVELTY_CONFLICT。

不要 rescue。

---

## 13. SECOND-INNOVATION BASELINE FREEZE

如果：

INNOVATION_1_FROZEN

则从现在开始第二创新所有实验必须包含：

B0 = frozen original baseline

B1 = frozen R-HSPE

B2 = Innovation-2 only

B3 = R-HSPE + Innovation-2

R-HSPE：

永远使用此次冻结版本。

禁止为了 Innovation 2：

重新调 R-HSPE。

---

## 14. NEXT EXPECTED STEP

如果成功：

NEXT_EXPECTED_STEP:

Begin Innovation 2 search on the frozen R-HSPE backbone.

Priority family:

Dual Node–Hyperedge Latent Interaction

目标：

增加与 R-HSPE 正交的：

node–hyperedge semantic compatibility signal，

而不是继续增加：

size/count/motif handcrafted context。

---

## 15. C2C HANDOFF

STATUS: EXECUTED

R_HSPE_METHOD:
FROZEN/NOT_FROZEN

CORA_TEST:
...

PUBMED_TEST:
...

THIRD_DATASET:
...

NOVELTY:
...

CLAIM_SCOPE:
...

SIZE_CAUSAL_CLAIM:
NOT_SUPPORTED

INNOVATION_1:
...

FREEZE_ARTIFACT:
...

NEXT_EXPECTED_STEP:
...

完成后停止。

不要自行开始 Innovation 2。