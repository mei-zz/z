# ==========================================================
# V29 — HDP ZERO-CLOSURE AND CONDITIONAL SIGNAL VALIDATION
# ==========================================================

WORKSPACE: DCDLP-main

OBJECTIVE:

Investigate the small positive conditional HDP signal
observed in V28.

Do not assume the maximum matching mechanism is correct.

Main research questions:

Q1:
Does binary closure existence explain the observed HDP gain?

Q2:
Does the full matching count provide additional value
beyond binary existence?

Q3:
Does candidate-specific true HDP information matter
beyond GRAPH and MULT?

Q4:
Are the observed gains stable on new seeds and
a new train-derived validation split?

Q5:
Can a small but reliable structural gain be isolated
without changing the backbone architecture?

Research policy:

Any positive paired improvement is a research lead.

A research lead is not yet a validated mechanism.

Do not erase small positive findings.

Do not claim novelty before mechanism and literature review.

TEST SEALED.
INNOVATION 1 FROZEN.


# ==========================================================
# 0. WORKSPACE GUARD
# ==========================================================

Call workspace_info.

Require:

    workspace == DCDLP-main

Otherwise STOP.

Read:

    result/innovation2/HDP2_V27/
    result/innovation2/TOPOLOGY_V28/

Especially:

    V28_FINAL_RESEARCH_REVIEW.md
    FINAL_REPORT.md
    06_PHASE_A_METRICS.json
    07_PHASE_A_PAIRED_CONTRASTS.json

If artifact filenames differ, locate actual files
through the workspace; do not fabricate paths.

Read the actual feature, model, split, and cache code.

Confirm:

    V28 = COMPLETE
    test = SEALED
    historical artifacts = IMMUTABLE

Create:

    result/innovation2/HDP_ZERO_V29/


# ==========================================================
# 1. STORAGE AND EXECUTION SAFETY
# ==========================================================

V28 previously encountered disk exhaustion.

Before training:

    check filesystem free space
    check inode availability
    estimate cache/checkpoint growth
    establish a free-space safety margin

Do not delete historical evidence.

Use sequential or collision-safe cache writes.

Use:

    unique temporary paths
    atomic rename
    hash verification
    explicit cache completion marker

Do not log secrets or print .env.

If storage is insufficient:

    STOP safely and return a storage report.


# ==========================================================
# 2. V28 SOURCE REPRODUCTION
# ==========================================================

Verify exact definitions of:

    G = GRAPH features
    M = MULT features
    H = HDP features
    P = PAIR features

Verify actual 6D feature layout and decoder.

Verify:

    canonical target masking
    SHARED initialization
    optimizer
    final checkpoint selection
    loss
    train/validation population

Reproduce the V28 primary model comparisons
using existing validated artifacts when possible.

Require checkpoint / prediction / source hashes
to be consistent with historical evidence.

If reproduction fails:

    STOP.


# ==========================================================
# 3. RETROSPECTIVE DIAGNOSTICS FIRST
# ==========================================================

Before any new training, analyze existing V28
candidate-level validation outputs.

Compare:

    GM
    GMH
    GMS
    GMP
    GMG
    GDUP

For every dataset and seed calculate:

    per-candidate CE difference

Stratify by:

    H = 0
    H = 1
    H >= 2

Also stratify by:

    projected common-neighbor count
    MULT strength
    endpoint degree buckets

For every subgroup report:

    candidate count
    positive count
    negative count
    mean DeltaCE
    DeltaMRR where meaningful
    contribution to total DeltaCE

Important:

    If most overall improvement occurs where H = 0,
    this alone does not establish that H carries predictive
    information.

For H = 0, the HDP feature is constant.
Gains there may arise from changed training dynamics,
shared decoder parameters or global calibration.

Explicitly distinguish:

    observed score improvement

from:

    incremental HDP information.

Save:

    01_RETROSPECTIVE_SUBGROUP_AUDIT.json
    01_RETROSPECTIVE_SUBGROUP_AUDIT.md


# ==========================================================
# 4. PRIMARY HDP REPRESENTATIONS
# ==========================================================

For candidate (u,v):

Let:

    lambda_H(u,v)

be exact V27 maximum bipartite matching size.

Define:

BINARY CLOSURE:

    B_uv = 1 if lambda_H > 0 else 0

FULL HDP:

    H_uv = [
        log1p(lambda_H),
        lambda_H / max(1,min(n_u,n_v))
    ]

BINARY FEATURE:

    H_BIN = [B_uv,0]

COUNT-ONLY FEATURE:

    H_COUNT = [log1p(lambda_H),0]

SATURATION FEATURE:

    H_SAT = [
        B_uv,
        lambda_H / max(1,min(n_u,n_v))
    ]

All are fixed deterministic features.

Do not introduce attention or learned matching.


# ==========================================================
# 5. MODEL ARCHITECTURE
# ==========================================================

Use exactly the V28 six-dimensional
topological residual branch.

Input:

    [G, M, third_feature]

where each block is two-dimensional.

Same:

    SHARED backbone
    residual MLP
    activation
    zero initialization
    training protocol
    optimizer
    feature normalization
    parameter count

Read exact architecture from V28.

Do not change the backbone.

Do not widen the residual decoder.


# ==========================================================
# 6. PRIMARY MODEL VARIANTS
# ==========================================================

A0 — SHARED

    Historical strong baseline.

A1 — GDUP

    [G,G,0]

    Strong repeated-GRAPH control.

A2 — GM

    [G,M,0]

A3 — GMG

    [G,M,G]

    Duplicate-third-slot control.

A4 — GMP

    [G,M,P]

    Path-count control.

A5 — GM-BINARY

    [G,M,H_BIN]

    Main zero/nonzero hypothesis.

A6 — GM-COUNT

    [G,M,H_COUNT]

A7 — GM-SAT

    [G,M,H_SAT]

A8 — GM-FULL-HDP

    [G,M,H_uv]

    Historical HDP mechanism.

A9 — GM-HDP-SHUFFLE

    [G,M,H_shuffle]

    Reproduce exact V28 shuffle.

A10 — GM-HDP-CONDITIONAL-PERMUTE

    [G,M,H_conditional_permuted]

    Stronger candidate-level correspondence control.

All variants must have identical architecture
and parameter count except standalone SHARED.


# ==========================================================
# 7. CONDITIONAL PERMUTATION CONTROL
# ==========================================================

The historical incidence-rewiring shuffle rarely changed
the final matching statistic.

Do not treat it as a decisive negative control.

Build an additional deterministic conditional
permutation of the 2D HDP feature block.

Within each split independently:

    keep G unchanged
    keep M unchanged
    keep candidate ordering unchanged
    keep labels unused for matching
    keep full candidate population unchanged

Permute H between eligible candidates matched by:

    GRAPH feature values/buckets
    MULT feature values/buckets
    endpoint degree buckets

Prefer exact matching where possible.

Do not silently relax matching.

Report:

    eligible fraction
    exact-match fraction
    changed-H fraction
    zero/nonzero transition fraction
    marginal H distribution
    conditional distribution drift

Check whether permutation sufficiently disrupts
the candidate-to-HDP correspondence.

If too few eligible candidates have different H:

    CONTROL_NOT_IDENTIFIABLE

Do not claim the conditional permutation is strong.

Do not select permutation based on labels or
validation performance.


# ==========================================================
# 8. ZERO-CLOSURE IDENTIFIABILITY AUDIT
# ==========================================================

Report:

    fraction H=0
    fraction H=1
    fraction H>=2

for train and validation.

Also report:

    P(H>0 | GRAPH, MULT degree buckets)

Estimate how predictable closure existence is
from GRAPH and MULT alone.

Train a simple diagnostic predictor using TRAIN only:

    B_hat = f(G,M,degree statistics)

Evaluate on validation:

    AUC
    log loss
    balanced accuracy

Do not use this probe inside primary models.

Purpose:

    Is binary closure merely recoverable from
    already-known topology?

If binary closure can be exactly recovered,
record that structural limitation prominently.


# ==========================================================
# 9. ALGEBRAIC AND STRUCTURAL SANITY
# ==========================================================

Verify:

    B_uv == int(lambda_H > 0)

    H_COUNT[0] == log1p(lambda_H)

    H_uv uses exact matching

    target masking is correct

    candidate swap invariance holds

No test target information.

Use sampled exact matching cross-checks.

Save:

    02_FEATURE_SANITY.json


# ==========================================================
# 10. PARAMETER / INITIALIZATION MATCHING
# ==========================================================

All A1-A10 variants must share the same
trainable parameter count.

For paired seeds preserve:

    initial model state
    candidate order
    negative samples
    training permutations

Compare initialization hashes and
training RNG traces.

Any difference must be documented.

Save:

    03_PARAMETER_RNG_AUDIT.json


# ==========================================================
# 11. DETERMINISM PRECHECK
# ==========================================================

PubMed seed0:

Run independently twice:

    GM-BINARY
    GM-FULL-HDP
    GM-HDP-CONDITIONAL-PERMUTE
    GMG

Require exact:

    feature hashes
    checkpoint hashes
    prediction hashes
    training trajectory hashes

If failed:

    STOP.


# ==========================================================
# 12. PHASE A — PROSPECTIVE NEW-SEED TEST
# ==========================================================

Use seeds NOT previously used for selecting
these hypotheses.

Suggested:

    8,9,10,11,12

Datasets:

    Cora
    PubMed

Epochs:

    5

Checkpoint:

    final epoch

Validation:

    original canonical validation only

Run primary variants.

Report:

    CE
    MRR
    Hits@10
    Hits@20
    AUC

Use paired comparisons.

Do not include old seeds when calculating the
new-seed-only mean.

Report old and new results separately.


# ==========================================================
# 13. PRIMARY QUESTIONS
# ==========================================================

QUESTION A:

Does binary closure improve GM?

Compare:

    GM-BINARY vs GM

Also:

    GM-BINARY vs GMG
    GM-BINARY vs GMP
    GM-BINARY vs GDUP

QUESTION B:

Does continuous HDP improve over binary closure?

Compare:

    GM-FULL-HDP vs GM-BINARY

and:

    GM-FULL-HDP vs GM-COUNT
    GM-FULL-HDP vs GM-SAT

QUESTION C:

Does true candidate-specific HDP matter?

Compare:

    GM-FULL-HDP vs GM-HDP-CONDITIONAL-PERMUTE
    GM-FULL-HDP vs GM-HDP-SHUFFLE

QUESTION D:

Does any surviving method improve ranking?

Compare:

    CE
    MRR
    Hits@10

on both datasets.


# ==========================================================
# 14. SMALL POSITIVE SIGNAL POLICY
# ==========================================================

Do not reject a whole direction merely because one
dataset or one mechanism control is inconclusive.

Classify separately:

    PERFORMANCE_SIGNAL
    BINARY_CLOSURE_SIGNAL
    MATCHING_COUNT_INCREMENT
    TRUE_HYPEREDGE_IDENTITY_SIGNAL

Levels:

    NO_GAIN
    EXPLORATORY_POSITIVE
    REPLICATION_CANDIDATE
    REPLICATED_SIGNAL
    MECHANISM_SUPPORTED

For EXPLORATORY_POSITIVE:

    preserve per-seed evidence
    record limitations
    recommend the next narrow falsification

Do not call it innovation yet.

For MECHANISM_SUPPORTED:

    still require targeted novelty audit.


# ==========================================================
# 15. PHASE B — INDEPENDENT INNER VALIDATION
# ==========================================================

Only for the best one or two surviving
Phase A hypotheses.

Use a new train-derived validation split.

Do not reuse the V28 inner split as the
only independent confirmation.

Rebuild:

    training-visible hypergraph
    candidate masks
    feature caches
    negative sampling

using inner-train only.

Use fixed predeclared split seeds.

Compare:

    surviving candidate
    its strongest matched control
    GM
    GDUP

Keep all training settings fixed.

Report new split results separately.

Do not open test.


# ==========================================================
# 16. RESULT INTERPRETATION
# ==========================================================

Case 1:

    GM-BINARY ~= GM-FULL-HDP
    and both outperform matched controls

Interpretation:

    closure existence may explain the HDP gain.

Do not claim matching capacity is necessary.

Case 2:

    GM-FULL-HDP > GM-BINARY
    and > GM-COUNT controls where relevant

Interpretation:

    continuous matching information may help.

Check conditional permutation before mechanism claims.

Case 3:

    TRUE HDP ~= conditional permutation

Interpretation:

    candidate-specific HDP evidence unsupported.

Performance may reflect feature distribution
or optimization effects.

Case 4:

    GMG / GMP >= all HDP variants

Interpretation:

    duplicate topology or ordinary path counts
    remain sufficient explanations.

Case 5:

    any HDP model improves only where H=0

Interpretation:

    do not immediately claim structural matching value.

Investigate calibration and shared-parameter effects.


# ==========================================================
# 17. NO UNCONTROLLED TUNING
# ==========================================================

Do not:

    modify matching algorithm
    add K=3 paths
    add attention
    increase model width
    add ranking loss
    tune learning rate
    select validation-best epochs
    alter negative sampling
    change test split

The purpose is to isolate V28's small gain,
not to rescue an architecture.


# ==========================================================
# 18. REQUIRED ARTIFACTS
# ==========================================================

Create:

result/innovation2/HDP_ZERO_V29/

    00_PROTOCOL.md
    01_RETROSPECTIVE_SUBGROUP_AUDIT.md
    01_RETROSPECTIVE_SUBGROUP_AUDIT.json
    02_FEATURE_SANITY.json
    03_PARAMETER_RNG_AUDIT.json
    04_SHUFFLE_IDENTIFIABILITY.json
    05_CLOSURE_PREDICTABILITY.json
    06_DETERMINISM_PRECHECK.json
    07_PHASE_A_NEW_SEEDS.json
    08_PHASE_A_PAIRED_CONTRASTS.json
    09_ACTIVE_SUBGROUP_ANALYSIS.json
    10_INNER_VALIDATION.json
    11_RANKING_CALIBRATION.md
    12_DECISION.md

    SOURCE_HASHES.json
    RUN_MANIFEST.json
    RUN_STATUS.json
    FINAL_REPORT.md


# ==========================================================
# 19. FINAL C2C HANDOFF
# ==========================================================

STATUS: EXECUTED

TASK:
V29_HDP_ZERO_CLOSURE_CONDITIONAL_VALIDATION

WORKSPACE:
DCDLP-main

V28_BASELINE_REPRODUCTION:
PASS/FAIL

DETERMINISM:
PASS/FAIL

LEAKAGE:
PASS/FAIL

STORAGE:
PASS/FAIL

HDP_ZERO_FRACTION:
Cora ...
PubMed ...

CLOSURE_FROM_GRAPH_MULT_PREDICTABILITY:
Cora ...
PubMed ...

CORA_BINARY_VS_GM:
DeltaCE ...
wins ...
DeltaMRR ...

PUBMED_BINARY_VS_GM:
...

CORA_FULL_VS_BINARY:
...

PUBMED_FULL_VS_BINARY:
...

CORA_FULL_VS_GMG:
...

PUBMED_FULL_VS_GMG:
...

CORA_FULL_VS_GMP:
...

PUBMED_FULL_VS_GMP:
...

CORA_TRUE_VS_CONDITIONAL_PERMUTE:
...

PUBMED_TRUE_VS_CONDITIONAL_PERMUTE:
...

CONDITIONAL_SHUFFLE_IDENTIFIABILITY:
VALID/WEAK/NOT_IDENTIFIABLE

NEW_SEED_REPLICATION:
...

INNER_VALIDATION:
...

BINARY_CLOSURE_SIGNAL:
...

MATCHING_COUNT_INCREMENT:
...

TRUE_HYPEREDGE_IDENTITY_SIGNAL:
...

BEST_PERFORMING_VARIANT:
...

PERFORMANCE_STATUS:
...

MECHANISM_STATUS:
...

NOVELTY_STATUS:
NOT_AUDITED

TEST_OPENED:
NO

INNOVATION_1_MODIFIED:
NO

HISTORICAL_RESULTS_MODIFIED:
NO

NEXT_EXPECTED_STEP:

Return results for research review.

If binary closure is supported:
    investigate closure-existence topology,
    not maximum matching complexity.

If continuous count survives binary controls:
    investigate the incremental matching profile.

If neither survives strong controls:
    preserve the stable GRAPH baseline and
    abandon HDP-specific mechanism claims.

Do not automatically start V30.

Stop after handoff.
## Execution preregistration
New seeds: 8,9,10,11,12. Inner split seed: 290016 (10% train-pool holdout, distinct from V28). Inner training seeds: 13,14,15; final 5 epochs;20 frozen negatives/query. Strongest matched control selected per dataset from GDUP/GMG/GMP by Phase A mean CE. Maximum two candidate representations with positive dataset mean CE versus GM; order positive datasets, mean paired CE, simplicity BINARY/COUNT/SAT/FULL. Individual positive seeds retained. Conditional permutation uses fixed floorlog2 buckets of G/M/projected degree plus exact occurrence multiplicity; no fallback; report exact-match fraction and drift. Binary features normalize with their train5 moments; shuffle/permutation use true H scaler. Runtime disk stop: 3GiB free; initial conservative growth estimate: 8GiB. Single writer for each seed; unique temporary directory; atomic rename and hashed READY publication. Training workers6, backbone workers2, feature workers3, CPU6 numba threads per feature worker. Workspace_info unavailable; existing workspace audit and frozen hashes verify logical DCDLP-main. Stop session after detached experiment is confirmed stable, as specified in server instructions.
