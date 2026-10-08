# V18.1R forensic report

**FINAL_STATUS: HISTORICAL_ROOT_CAUSE_IDENTIFIED**

## 1. Historical reproduction

V18 remains `CHRI_KILL / CHRI_TRANSFER_WEAK`. V18.1 remains `V18_1_REPRODUCTION_MISMATCH`. Neither historical artifact was edited. V18 did not save epoch-level model/optimizer/RNG hashes or the full software environment, so its exact internal trajectory cannot be reconstructed.

## 2. Root cause and first divergence

The primary class is `NUMERICAL_KERNEL_NONDETERMINISM`. Two fresh unpatched PubMed seed0 RAW runs diverged at epoch 1, optimizer batch 1, in endpoint `torch_scatter.scatter_mean`. Inputs, first-batch logits and loss were equal; pooled outputs differed. The first different gradient and updated parameter was `decoder.4.weight`. PyTorch strict deterministic mode alone did not control this third-party CUDA operation.

Repeated evaluation of fixed checkpoints is stable to within the tiny float32 score/CE drift in `02_CHECKPOINT_EVAL_REPEATABILITY.json` (max observed score drift is below 2e-6 and CE drift is below 3e-10). This is far smaller than the across-training score divergence, which exceeded 0.1 for PubMed RAW by epoch 5.

## 3. Inputs, cache, execution identity, and evaluation

The frozen NCNC checkpoint, V18 source hashes, raw-data/split hashes, cached candidates, negative order, feature arrays, normalization, and donor mappings match. Audited cache files remained unchanged after all runs. The evaluation calls `net.eval()` under `torch.no_grad()`; the predictor contains no Dropout or BatchNorm, and validation left its state hash unchanged. Historical V18 environment/RNG/state hashes were not recorded. The server checkout has no `.git` directory, so a server commit/diff cannot be reported.

The original supervisor launches each arm as an independent child process. The same R1-only first-step divergence occurs in fresh standalone processes, so shared Python arm state is not the cause. Full explicit forward/reverse sequence replay was not run after localizing the first isolated atomic reduction.

## 4. Minimal fix and corrected reproducibility

V18.1R adds `scripts/deterministic_aggregation.py`: replace grouped CUDA atomic mean/sum/max operations with `torch.segment_reduce` on the existing sorted group lengths. The architecture, features, masks, data, loss, optimizer, batches and epoch selection stay fixed. V18 and V18.1 files were not changed.

After the fix, two independent PubMed seed0 RAW five-epoch runs matched on all 90 optimizer steps: input, logits, loss, gradient, full model parameter/buffer and optimizer-state hashes all matched. Each epoch's model hash, optimizer hash, CE and MRR also matched exactly. The limited corrected reproduction then completed for PubMed seeds 0–2 (Z/RAW/SHUFFLE) and Cora seed0 (same three arms); test remains sealed.

Corrected PubMed versus historical tolerance: **FAIL**. Cora seed0 historical tolerance: **FAIL**. The corrected Cora seed0 A1/A2/A3 runs reproduce their second executions exactly (metrics, score vectors and checkpoint hashes). The deterministic reduction order produces stable new canonical runs but cannot recreate the exact old atomic accumulation order; therefore these are new reproducible V18R candidates, not a rewrite of V18 evidence. These metric comparisons are reproduction checks only and are not a CHRI efficacy verdict.

## 5. Handoff

- `FIRST_DIVERGENCE`: PubMed seed0 RAW/A2, epoch1 optimizer batch1, CUDA endpoint `scatter_mean`; then `decoder.4.weight` gradient/update.
- `ROOT_CAUSE_CLASS`: `NUMERICAL_KERNEL_NONDETERMINISM`.
- `MINIMAL_FIX`: deterministic segment reductions isolated in V18.1R.
- `PUBMED_REPRODUCTION`: FAIL against exact historical V18 tolerance; new corrected two-run repeatability PASS.
- `CORA_SPOT_CHECK`: FAIL against historical V18 tolerance; corrected second execution matches all three arms exactly.
- `HISTORICAL_V18_MODIFIED`: NO.
- `V18_1_MODIFIED`: NO.
- `TEST_OPENED`: NO.
- `INNOVATION_1_MODIFIED`: NO.
- `NEW_METHOD_VARIANTS_RUN`: NO.

**NEXT_EXPECTED_STEP:** reconcile whether the deterministic V18R run becomes canonical, then resume V18.1. Do not interpret CHRI efficacy from this forensic round.

Per-run validation metrics are recorded in `12_CORRECTED_REPRODUCTION.json`; artifacts distinguish historical mismatch from deterministic repeatability.
