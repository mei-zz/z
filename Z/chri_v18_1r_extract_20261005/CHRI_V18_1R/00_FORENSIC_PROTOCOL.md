# V18.1R — PUBMED REPRODUCTION FORENSIC AUDIT
# CHRI reproduction bug isolation
#
# MODE:
# FORENSIC_AUDIT_ONLY
#
# NO METHOD DEVELOPMENT
# NO NEW INNOVATION VARIANTS
# NO TEST ACCESS
# NO R-HSPE MODIFICATION

STATUS: READY_TO_EXECUTE

GOAL:

定位并解释 V18 -> V18.1 PubMed reproduction mismatch。

已知事实：

- Cora reproduction passes.
- PubMed reproduction contains multiple validation mismatches.
- Initialization traces match.
- Training sampling traces match.
- Some PubMed validation scores diverge progressively across epochs.
- V18.1 therefore stopped before V1/V2/V3.
- Test sets were not opened.

本轮唯一问题：

    WHY CAN IDENTICAL TRAINING TRACES PRODUCE
    DIFFERENT PUBMED VALIDATION OUTPUTS?

在 root cause 找到并修复前：

    不运行 residualization
    不运行 gating
    不运行 CRIB
    不重新判断 CHRI efficacy
    不开始 Innovation 3

==================================================
0. WORKSPACE GUARD
==================================================

确认 workspace:

    DCDLP-main

如果不是：

    STOP.

读取：

    result/innovation2/CHRI_V18/
    result/innovation2/CHRI_V18_1/

尤其：

    FINAL_REPORT.md
    01_V18_REPRODUCTION.json
    run manifests
    source hashes
    checkpoints
    feature caches
    logs

同时读取：

    HYPERGRAPH_RESEARCH/R_HSPE_FINAL_FROZEN/

只确认 Innovation 1 仍 FINAL_FROZEN。

不要修改 Innovation 1。

创建：

    result/innovation2/CHRI_V18_1R/

==================================================
1. HISTORICAL INTEGRITY
==================================================

禁止修改：

    CHRI_V18/
    CHRI_V18_1/

V18 历史状态保持：

    CHRI_KILL / CHRI_TRANSFER_WEAK

V18.1 历史状态保持：

    V18_1_REPRODUCTION_MISMATCH

本轮只能产生：

    forensic explanation
    minimal deterministic fix
    corrected reproduction evidence

不得 retroactively rewrite old artifacts.

==================================================
2. FIRST: COMPARE V18 vs V18.1 EXECUTION IDENTITY
==================================================

建立：

    01_EXECUTION_IDENTITY_AUDIT.json

逐项比较 V18 与 V18.1：

SOURCE:
    git commit
    git diff
    Python source hashes
    imported module hashes

ENVIRONMENT:
    Python version
    PyTorch version
    CUDA version
    cuDNN version
    GPU model
    deterministic flags
    TF32 settings
    AMP settings
    matmul precision
    environment variables affecting determinism

DATA:
    raw/processed dataset hashes
    split hashes
    candidate hashes
    negative candidate hashes
    candidate order hashes

BACKBONE:
    frozen NCNC checkpoint hash
    all loaded parameter tensor hashes
    buffers
    model config

FEATURES:
    B hash
    P_u hash
    P_v hash
    Z hash
    R_CAT source feature hash
    shuffle-donor mapping hash

CACHE:
    feature cache hashes
    cache file mtimes
    serialization format
    dtype
    device
    tensor shape

TRAINING:
    optimizer config
    optimizer initialization
    batches
    permutations
    RNG states

EVALUATION:
    evaluator source hash
    candidate ordering
    batch size
    tie handling
    dtype/device
    model.eval state
    torch.no_grad/inference_mode usage

任何不一致都记录。

不要先假定“只是 GPU nondeterminism”。

==================================================
3. CHECKPOINT-ONLY EVALUATION REPEATABILITY
==================================================

这是第一优先级。

选择 PubMed：

    seed 0

分别对：

    R0 = Z
    R1 = RAW
    R2 = SHUFFLE

使用完全同一个已保存 checkpoint。

不训练。

连续执行 validation scoring：

    10 times in same process

然后：

    10 times in fresh processes

每次记录：

    full score vector hash
    score max abs difference
    CE
    MRR
    AUC

要求判断：

A.
同 checkpoint + 同输入是否每次输出完全/近完全一致？

如果不一致：

    problem is evaluation/state/nondeterministic execution.

如果一致：

    mismatch originates before evaluation.

输出：

    02_CHECKPOINT_EVAL_REPEATABILITY.json

==================================================
4. HASH THE FULL STATE, NOT ONLY RNG TRACE
==================================================

目前“training trace matched”还不够。

对 PubMed seed0 R0/R1/R2：

在：

    initialization
    end of every epoch

保存 hash：

MODEL:
    every parameter tensor
    every registered buffer

OPTIMIZER:
    optimizer state tensors
    step counters

FEATURE MODULES:
    hyperedge encoder parameters
    relation encoder parameters
    decoder parameters

CACHED/DERIVED STATE:
    normalization tensors
    PCA state if present
    shuffle structures
    mutable feature tensors

生成：

    STATE_HASH_EPOCH_0
    STATE_HASH_EPOCH_1
    ...
    STATE_HASH_EPOCH_5

和 historical V18 对比。

如果历史 V18 没有这些 hashes：

不要伪造 comparison。

改为：

    reproduce twice from identical start

并比较两次 run 的 full state hashes。

输出：

    03_FULL_STATE_HASH_AUDIT.json

==================================================
5. FIND THE FIRST DIVERGENCE
==================================================

目标不是只知道 epoch5 不一样。

必须定位：

    FIRST_DIVERGENCE_POINT

优先针对：

    PubMed seed0 R1

因为该 arm 已知较早产生偏差。

逐级比较：

1.
input batch ids

2.
input tensor hashes

3.
forward logits before optimizer step

4.
loss

5.
grad tensor hashes / norms

6.
optimizer-updated parameter hashes

先按 epoch。

如果 divergence 已在某个 epoch 内出现：

只对该 epoch做 batch-level binary search。

不要从头给所有任务增加超重 instrumentation。

最终输出：

    first divergent epoch
    first divergent batch if resolvable
    first divergent tensor/module

写入：

    04_FIRST_DIVERGENCE.md

==================================================
6. VALIDATION INPUT IMMUTABILITY AUDIT
==================================================

重点检查 PubMed validation pipeline。

对每次 validation 前后 hash：

    candidate ids
    positive ids
    negative ids
    B
    P_u
    P_v
    Z
    R_CAT tensors
    shuffle mappings

检查：

    validation input changed during training?
    cache mutated in place?
    tensor view points to writable shared storage?
    normalization updated?
    features lazily recomputed differently?
    candidate ordering changed?
    DataLoader order changed?

特别搜索：

    in-place operations
    `.copy_`
    `.add_`
    `.mul_`
    `.scatter_`
    `.index_put_`
    reuse of tensor views
    cached list mutation
    dict mutation
    global singleton state

输出：

    05_CACHE_MUTABILITY_AUDIT.md
    05_CACHE_MUTABILITY_AUDIT.json

==================================================
7. ARM-ORDER / PROCESS-ISOLATION TEST
==================================================

检查是否存在 shared mutable state。

PubMed seed0：

运行三种顺序：

    R0 -> R1 -> R2
    R2 -> R1 -> R0
    R1 alone

每个 arm：

    fresh model
    fresh optimizer
    fresh process where practical

比较：

    final checkpoint hashes
    validation score hashes

如果同一 arm 因执行顺序而改变：

分类：

    ORDER_DEPENDENT_SHARED_STATE

然后定位：

    global cache
    shared sampler
    mutable feature object
    RNG consumption outside declared scope
    library state

==================================================
8. TRAIN/EVAL MODE AUDIT
==================================================

明确检查：

    model.train()
    model.eval()

以及所有子模块：

    backbone
    hyperedge encoder
    R encoder
    decoder

检查是否存在：

    Dropout
    BatchNorm
    stochastic attention
    sampled neighborhood
    stochastic feature generation

在 validation 时记录每个相关模块：

    module.training

检查 buffer：

    running_mean
    running_var
    num_batches_tracked

如任何 validation 会更新 buffer：

标记 root cause candidate。

==================================================
9. GPU DETERMINISM ISOLATION
==================================================

仅当：

    parameters same
    inputs same

但 outputs differ 时执行。

对一个最小 PubMed checkpoint evaluation：

A.
current GPU mode

B.
torch deterministic mode:
    torch.use_deterministic_algorithms(True)
    cudnn deterministic where relevant
    cudnn benchmark False
    disable TF32 if needed

C.
CPU evaluation
    only if operator support allows

比较 score vector。

如果：

GPU current differs
but deterministic GPU / CPU matches

分类：

    NONDETERMINISTIC_KERNEL

记录具体 operator if PyTorch reports one。

不要因为一点 floating drift 就接受 root cause；
必须解释当前 observed magnitude。

==================================================
10. DTYPE / NUMERICAL PATH AUDIT
==================================================

检查 V18 与 V18.1：

    float32 / float64
    AMP
    autocast
    TF32
    matmul precision
    sparse operations
    reduction order
    sorting/top-k
    scatter reductions

尤其检查 PubMed 比 Cora 更大是否触发：

    different batching
    different sparse kernel
    different reduction path

如果只有 PubMed 触发不同 kernel/path：

明确记录。

==================================================
11. CHECKPOINT LOAD / SAVE AUDIT
==================================================

检查：

    checkpoint exact hash
    save timing
    load timing
    strict=True/False
    missing keys
    unexpected keys

确认：

    no accidental best-checkpoint load
    no epoch-final mismatch
    no stale cache/checkpoint mix
    no partial module reload

保存 load report：

    missing_keys
    unexpected_keys
    tensor hash before save
    tensor hash after reload

==================================================
12. MINIMAL FIX POLICY
==================================================

如果 root cause 找到：

只允许最小修复。

例如：

    clone immutable cached tensors
    isolate process-local cache
    call eval correctly
    reset mutable iterator
    freeze normalization
    deterministic operator replacement
    correct stale checkpoint/cache loading

禁止：

    change model
    change hyperparameters
    change features
    change CHRI definition
    change loss
    change split

修复必须写：

    exact file
    exact function
    exact bug
    why it affected PubMed
    why Cora appeared unaffected

==================================================
13. AFTER FIX: REPRODUCTION ONLY
==================================================

只有 root cause 已定位且 minimal fix 已实施：

重新运行：

PubMed:
    seeds 0,1,2
    R0
    R1
    R2

5 epochs

不要运行：

    V1
    V2
    V3
    Phase B

先验证 reproduction。

要求：

    initialization match
    training inputs match
    parameter/state hashes deterministic
    validation score tolerance pass

同时做一个 Cora spot-check：

    seed0
    R0/R1/R2

确认修复没有破坏 Cora。

==================================================
14. REPRODUCTION ACCEPTANCE
==================================================

如果修复后：

PubMed historical V18
可以在预设 tolerance 内复现：

    REPRODUCTION_RESTORED

如果历史 V18 本身无法被 exact reconstruct，
但：

    two fresh executions from identical state

现在达到 deterministic agreement，

且能明确证明历史差异来自某个旧 bug：

    HISTORICAL_ROOT_CAUSE_IDENTIFIED
    NEW_CANONICAL_REPRODUCIBLE_RUN_AVAILABLE

这种情况下：

不要偷偷替换 V18。

必须保留：

    old historical V18
    corrected reproducible V18R

后续再由下一轮决定采用哪个 canonical evidence。

如果 root cause 找不到：

    REPRODUCTION_UNRESOLVED

停止。

==================================================
15. ROOT CAUSE CLASSIFICATION
==================================================

最终只能选择一个主分类：

    CHECKPOINT_STATE_MISMATCH
    CACHE_MUTATION
    ORDER_DEPENDENT_SHARED_STATE
    EVAL_MODE_STATE
    FEATURE_RECOMPUTATION_MISMATCH
    DATA_OR_CANDIDATE_MISMATCH
    NUMERICAL_KERNEL_NONDETERMINISM
    ENVIRONMENT_MISMATCH
    HISTORICAL_ARTIFACT_MISMATCH
    OTHER_IDENTIFIED
    UNRESOLVED

可附 secondary contributors。

==================================================
16. DO NOT INTERPRET CHRI PERFORMANCE
==================================================

本轮禁止根据重新得到的：

    Delta CE
    Delta MRR
    seed wins

宣布：

    CHRI supported
    CHRI failed
    CHRI stabilized

本轮只回答：

    CAN WE TRUST THE EXPERIMENTAL PIPELINE?

方法判断留到 reproduction 修复以后。

==================================================
17. TEST SEAL
==================================================

严格禁止访问：

    Cora test
    PubMed test
    Citeseer test

如果任何 test 被意外读取：

    STATUS = TEST_SEAL_VIOLATION

立即停止并记录。

==================================================
18. REQUIRED ARTIFACTS
==================================================

创建：

result/innovation2/CHRI_V18_1R/

至少：

00_FORENSIC_PROTOCOL.md
01_EXECUTION_IDENTITY_AUDIT.json
02_CHECKPOINT_EVAL_REPEATABILITY.json
03_FULL_STATE_HASH_AUDIT.json
04_FIRST_DIVERGENCE.md
05_CACHE_MUTABILITY_AUDIT.md
05_CACHE_MUTABILITY_AUDIT.json
06_ARM_ORDER_AUDIT.json
07_EVAL_MODE_AUDIT.json
08_DETERMINISM_AUDIT.json
09_CHECKPOINT_AUDIT.json
10_ROOT_CAUSE.md
11_MINIMAL_FIX.md
12_CORRECTED_REPRODUCTION.json
SOURCE_HASHES.json
RUN_MANIFEST.json
FINAL_REPORT.md

未执行项：

写 NOT_RUN + reason。

==================================================
19. FINAL REPORT MUST ANSWER
==================================================

1.
V18 -> V18.1 PubMed mismatch 的 first divergence 在哪里？

2.
参数是否分叉？

3.
optimizer state 是否分叉？

4.
validation inputs 是否分叉？

5.
cache 是否发生 mutation？

6.
arm execution order 是否影响结果？

7.
eval mode / buffers 是否正确？

8.
GPU nondeterminism 是否足以解释误差？

9.
root cause 是什么？

10.
修改了哪个文件 / 函数？

11.
为什么该问题主要出现在 PubMed？

12.
修复后能否复现？

13.
Cora spot-check 是否保持一致？

14.
test 是否保持 sealed？

==================================================
20. FINAL STATUS
==================================================

只能返回：

A.
REPRODUCTION_RESTORED

B.
HISTORICAL_ROOT_CAUSE_IDENTIFIED

C.
REPRODUCTION_UNRESOLVED

D.
TEST_SEAL_VIOLATION

不要返回 CHRI efficacy verdict。

==================================================
21. FINAL C2C HANDOFF
==================================================

STATUS: EXECUTED

TASK:
CHRI_V18_1R_REPRODUCTION_FORENSICS

WORKSPACE:
DCDLP-main

FIRST_DIVERGENCE:
...

ROOT_CAUSE_CLASS:
...

ROOT_CAUSE:
...

AFFECTED_FILE_FUNCTION:
...

MINIMAL_FIX:
...

PUBMED_REPRODUCTION:
PASS / FAIL

CORA_SPOT_CHECK:
PASS / FAIL / NOT_RUN

HISTORICAL_V18_MODIFIED:
NO

V18_1_MODIFIED:
NO

TEST_OPENED:
NO

INNOVATION_1_MODIFIED:
NO

NEW_METHOD_VARIANTS_RUN:
NO

FINAL_STATUS:
REPRODUCTION_RESTORED
/
HISTORICAL_ROOT_CAUSE_IDENTIFIED
/
REPRODUCTION_UNRESOLVED
/
TEST_SEAL_VIOLATION

PRIMARY_ARTIFACT:
result/innovation2/CHRI_V18_1R/FINAL_REPORT.md

NEXT_EXPECTED_STEP:

If REPRODUCTION_RESTORED:
    resume V18.1 residualization/stability study from the
    trusted canonical reproduction.

If HISTORICAL_ROOT_CAUSE_IDENTIFIED:
    first reconcile which corrected run becomes canonical,
    then resume V18.1.

If REPRODUCTION_UNRESOLVED:
    do not run CHRI optimization;
    investigate infrastructure/reproducibility further.

Stop after handoff.
Do not start Innovation 3.