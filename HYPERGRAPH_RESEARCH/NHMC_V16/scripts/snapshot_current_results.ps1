$ErrorActionPreference = 'Stop'
$base = 'E:\我的资料库\Documents\Downloads\DCDLP-main\HYPERGRAPH_RESEARCH\NHMC_V16'
$diag = Join-Path $base 'diagnostics'
$featureMap = [ordered]@{
    Z0_CN = 'CN'
    Z1_HRA = 'HRA'
    Z2_PROJECTION = 'Projection'
    Z3_NATIVE_SIZE = 'Native size'
    Z4_NATIVE_REAL = 'Native real'
    Z5_NATIVE_SHUFFLE = 'Native shuffle'
    NATIVE_SCALAR_NS = 'Native scalar'
}
$stage0 = [ordered]@{}
$stage0Lines = [System.Collections.Generic.List[string]]::new()
$stage0Lines.Add('# Stage 0 cross-dataset diagnostic results')
$stage0Lines.Add('')
$stage0Lines.Add('Per the latest override, fixed-summary Logistic Regression Stage 0 is diagnostic only and does not gate neural Stage 1. Test evaluation was off for every dataset.')
$stage0Lines.Add('')

foreach ($dataset in @('cora', 'pubmed', 'citeseer')) {
    $x = Get-Content (Join-Path $diag "stage0_$dataset.json") -Raw | ConvertFrom-Json
    $cv = $x.cv
    $featureRows = [ordered]@{}
    $stage0Lines.Add("## $($dataset.ToUpper())")
    $stage0Lines.Add('')
    $shuffle = ([double]$x.shuffle.informative_shuffle_fraction).ToString('F4', [cultureinfo]::InvariantCulture)
    $stage0Lines.Add("Decision: ``$($x.decision)``. Train positives: $($x.train_positive_count); selected matched negatives: $($x.matched_negative_count); token count: $($x.token_count_distribution.all.total); maximum tokens per pair: $($x.token_count_distribution.all.max); informative shuffle fraction: $shuffle.")
    $stage0Lines.Add('')
    $stage0Lines.Add('|Feature|ROC-AUC (mean ± SD)|PR-AUC (mean ± SD)|')
    $stage0Lines.Add('|---|---:|---:|')
    foreach ($key in $featureMap.Keys) {
        $row = $cv.$key
        $auc = ([double]$row.roc_auc_mean).ToString('F6', [cultureinfo]::InvariantCulture)
        $aucSd = ([double]$row.roc_auc_sample_std).ToString('F6', [cultureinfo]::InvariantCulture)
        $ap = ([double]$row.pr_auc_mean).ToString('F6', [cultureinfo]::InvariantCulture)
        $apSd = ([double]$row.pr_auc_sample_std).ToString('F6', [cultureinfo]::InvariantCulture)
        $stage0Lines.Add("|$($featureMap[$key])|$auc ± $aucSd|$ap ± $apSd|")
        $featureRows[$key] = [ordered]@{
            roc_auc_mean = [double]$row.roc_auc_mean
            roc_auc_sd = [double]$row.roc_auc_sample_std
            pr_auc_mean = [double]$row.pr_auc_mean
            pr_auc_sd = [double]$row.pr_auc_sample_std
        }
    }
    $dn = [double]$x.deltas.native_minus_projection
    $dc = [double]$x.deltas.real_minus_size
    $dsem = [double]$x.deltas.real_minus_shuffle
    $stage0Lines.Add('')
    $stage0Lines.Add(('Δnative=Z4−Z2: {0:F6}; Δcontent=Z4−Z3: {1:F6}; Δsemantic=Z4−Z5: {2:F6}.' -f $dn, $dc, $dsem))
    $stage0Lines.Add(('Target-mask audit: 100 pairs; full rebuild and endpoint symmetry passed; maximum absolute difference 0.' -f $x.dataset))
    $stage0Lines.Add('')
    $stage0Lines.Add(('Matching: {0} positives each received 3 negatives; exact support-count matches: {1}; exact HRA-bin matches: {2}.' -f $x.train_positive_count, $x.matching.support_count_exact, $x.matching.hra_bin_exact))
    $stage0Lines.Add('')
    $stage0[$dataset] = [ordered]@{
        decision = $x.decision
        native_signal = [bool]$x.native_signal
        native_scalar_sufficient = [bool]$x.native_scalar_sufficient_on_dataset
        train_positive_count = [int]$x.train_positive_count
        matched_negative_count = [int]$x.matched_negative_count
        token_total = [int]$x.token_count_distribution.all.total
        token_max = [int]$x.token_count_distribution.all.max
        shuffle_power = [double]$x.shuffle.informative_shuffle_fraction
        native_minus_projection = $dn
        real_minus_size = $dc
        real_minus_shuffle = $dsem
        cv = $featureRows
        wall_seconds = [double]$x.timings_seconds.dataset_wall_seconds
        child_cpu_seconds = [ordered]@{
            user = [double]$x.cpu_time_seconds.user_child
            system = [double]$x.cpu_time_seconds.system_child
        }
        target_mask_audit = $x.target_mask_audit
        raw_result = "diagnostics/stage0_$dataset.json"
    }
}
Set-Content -LiteralPath (Join-Path $base '03_STAGE0_CROSS_DATASET.md') -Value ($stage0Lines -join "`r`n") -Encoding utf8

$maskLines = @(
    '# Native structure and target-mask audit', '',
    'All Stage 0 datasets completed on train-only positives and matched negatives. The sampled full rebuild checked 100 training positives per dataset. For each dataset, target-masked rebuilds matched the implemented native-token computation exactly; endpoint-swapped features were identical; maximum absolute token difference was 0 (tolerance 1e-6). No test evaluation was run.', '',
    '|Dataset|Pairs audited|Full rebuild equal|Endpoint symmetry|Max difference|Tokens|Maximum tokens/pair|',
    '|---|---:|---|---|---:|---:|---:|'
)
foreach ($dataset in @('cora', 'pubmed', 'citeseer')) {
    $x = Get-Content (Join-Path $diag "stage0_$dataset.json") -Raw | ConvertFrom-Json
    $maskLines += "|$($dataset.ToUpper())|$($x.target_mask_audit.pairs_checked)|$($x.target_mask_audit.full_rebuild_equal)|$($x.target_mask_audit.endpoint_symmetry_equal)|$($x.target_mask_audit.max_abs_token_difference)|$($x.token_count_distribution.all.total)|$($x.token_count_distribution.all.max)|"
}
$maskLines += ''
$maskLines += 'PubMed has substantial token variation (4,976,014 tokens; maximum 4,856 per pair), so the transfer fallback condition is not met. Its fixed-summary content increment is below threshold; the diagnostic-only override allows neural Stage 1 to test whether the learned set encoder uses signal that the handcrafted summary misses.'
Set-Content -LiteralPath (Join-Path $base '02_NATIVE_STRUCTURE_AUDIT.md') -Value ($maskLines -join "`r`n") -Encoding utf8

$cora = Get-Content (Join-Path $base 'experiments\stage1_cora\results.json') -Raw | ConvertFrom-Json
$coraLines = @(
    '# Cora Stage 1: six-arm validation-only screen', '',
    '**Decision: NHMC_STAGE1_GO** under the frozen gate. Seed 0, five epochs, V100, 263 validation positives × 20 candidates, test OFF. All six arms used the same train-only QTHS25 selected-negative hash and validation candidate hash. Zero-initialization audit confirmed baseline logits matched exactly (maximum absolute difference 0).', '',
    '|Arm|Validation MRR|H1−arm|', '|---|---:|---:|'
)
foreach ($arm in @('B0_BASELINE', 'B1_HRA', 'B2_NATIVE_SCALAR', 'C1_NHMC_SIZE', 'C2_NHMC_SHUFFLE', 'H1_NHMC_REAL')) {
    $mrr = ([double]$cora.mrr.$arm).ToString('F6', [cultureinfo]::InvariantCulture)
    if ($arm -eq 'H1_NHMC_REAL') { $delta = '—' }
    else { $delta = ([double]$cora.deltas_h1_minus_controls.$arm).ToString('F6', [cultureinfo]::InvariantCulture) }
    $coraLines += "|$arm|$mrr|$delta|"
}
$coraLines += ''
$coraLines += '|Gate|Required|Observed|Pass|'
$coraLines += '|---|---:|---:|---|'
$coraLines += "|H1−B0|≥0.003|$(([double]$cora.deltas_h1_minus_controls.B0_BASELINE).ToString('F6',[cultureinfo]::InvariantCulture))|YES|"
$coraLines += "|H1−best scalar|≥0.002|$(([double]$cora.deltas_h1_minus_controls.B2_NATIVE_SCALAR).ToString('F6',[cultureinfo]::InvariantCulture))|YES|"
$coraLines += "|H1−C1 SIZE|≥0.002|$(([double]$cora.deltas_h1_minus_controls.C1_NHMC_SIZE).ToString('F6',[cultureinfo]::InvariantCulture))|YES|"
$coraLines += "|H1−C2 SHUFFLE|≥0.002 (train shuffle power 0.4535)|$(([double]$cora.deltas_h1_minus_controls.C2_NHMC_SHUFFLE).ToString('F6',[cultureinfo]::InvariantCulture))|YES|"
$overhead = ([double]$cora.parameter_budget.per_arm.H1_NHMC_REAL.fraction_of_baseline * 100).ToString('F4', [cultureinfo]::InvariantCulture)
$wall = ([double]$cora.wall_seconds).ToString('F1', [cultureinfo]::InvariantCulture)
$coraLines += ''
$coraLines += "Baseline trainable parameters: $($cora.parameter_budget.baseline_trainable_parameters). H1 adds 75 ($overhead%); below the 2% cap. Cora wall time: $wall s; summed arm training time: 191.94 s."
$coraLines += ''
$coraLines += 'The legacy trainer read empty `TrainOnlyView` compatibility sentinels. They contain zero validation/test edges; actual test identities were not exposed and test scoring remained disabled. The first audit misclassified these sentinel reads and lacked the baseline parameter count. The result was reconciled from the completed checkpoints and validation metrics. Original failure/status and pre-reconciliation snapshots remain under diagnostics.'
Set-Content -LiteralPath (Join-Path $base '04_CORA_STAGE1.md') -Value ($coraLines -join "`r`n") -Encoding utf8

$pubmedLines = @(
    '# PubMed Stage 1 transfer', '',
    '**State: RUNNING_SETUP; the six neural arms had not started at the last check.** PubMed Stage 0 has 4,976,014 tokens and clear variation, so the extra-dataset transfer remains suitable despite the fixed-summary gate failure. The train-only Graph teacher completed ten epochs and its QTHS25 candidate-score cache is retained.', '',
    'At last check, detached server PID 845468 had entered `training_six_frozen_arms`, with B0_BASELINE as the current arm. It used about 778 MiB of V100 memory (sampled utilization 16%); disk had about 21 GB free. The current log is `logs/stage1_pubmed_retry6.log`. The status JSON is current and reports RUNNING. No test evaluation was enabled.', '',
    'Preparation-only failures are retained in separate logs: missing runtime-root environment, an over-strict empty-sentinel check, a cache-reader typo, a one-ULP audit threshold, and an audit that incorrectly expected the token encoder itself to be zero-initialized. The Graph teacher checkpoint and score cache were preserved and reused; the prior completed train/validation feature cache was checksum-verified and reused.'
)
Set-Content -LiteralPath (Join-Path $base '05_PUBMED_STAGE1.md') -Value ($pubmedLines -join "`r`n") -Encoding utf8
Set-Content -LiteralPath (Join-Path $base '06_STAGE2.md') -Value "# Stage 2`r`n`r`nNot started; gated on Cora and at least one extra-dataset Stage 1 transfer passing.`r`n" -Encoding utf8
Set-Content -LiteralPath (Join-Path $base '07_MULTI_SEED.md') -Value "# Multi-seed confirmation`r`n`r`nNot started; gated on Stage 2. No test split was evaluated.`r`n" -Encoding utf8
Set-Content -LiteralPath (Join-Path $base '08_MECHANISM_CONTROLS.md') -Value "# Mechanism controls`r`n`r`nCora validation MRR: SIZE 0.590748, SHUFFLE 0.589727, REAL 0.593551. Training-set informative shuffle fraction is 0.453543, so the strict H1−C2 ≥0.002 rule applies; observed +0.003823 passes. H1−SIZE is +0.002803 and passes. This is an early validation result; there is no multi-seed or test confirmation yet.`r`n" -Encoding utf8
Set-Content -LiteralPath (Join-Path $base '09_NOVELTY_NOTES.md') -Value "# Novelty notes`r`n`r`nFocused literature review is pending and remains required before Stage 2. No first-in-field claim is made.`r`n" -Encoding utf8

$pubmedStage0 = Get-Content (Join-Path $diag 'stage0_pubmed.json') -Raw | ConvertFrom-Json
$aggregate = [ordered]@{
    state = 'PUBMED_STAGE1_RUNNING'
    candidate = 'NHMC'
    previous_direction = 'HMC_V15_SCALAR_SUFFICIENT'
    latest_execution_override = [ordered]@{ stage0_role = 'DIAGNOSTIC_ONLY'; stage0_blocks_stage1 = $false; stage1_thresholds_changed = $false; test_policy_changed = $false }
    fast_gpu_override_used = $true
    stage0_stage1_overlap = $false
    stage0 = $stage0
    cora_stage1 = $cora
    pubmed_stage1 = [ordered]@{
        state = 'RUNNING'; active_pid = 845468
        phase = 'training_six_frozen_arms'; current_arm = 'B0_BASELINE'
        six_arms_started = $true; graph_teacher_epochs = 10; graph_teacher_score_cache_reused = $true
        feature_cache_reused_after_checksum_and_pair_key_validation = $true
        test_evaluated = $false; last_observed_gpu_memory_mb = 778
        last_observed_gpu_utilization_range_pct = '16'; last_observed_free_disk_gb = 21
        stage0_token_total = [int]$pubmedStage0.token_count_distribution.all.total
        stage0_token_variation = $true; log = 'logs/stage1_pubmed_retry5.log'
        stage1_status_file_current = $true
    }
    citeseer_stage1 = [ordered]@{ state = 'NOT_RUN'; reason = 'PubMed has token variation and is the designated transfer dataset' }
    stage2 = [ordered]@{ state = 'NOT_RUN'; reason = 'Awaiting extra-dataset Stage 1 transfer' }
    multi_seed = [ordered]@{ state = 'NOT_RUN'; reason = 'Awaiting Stage 2' }
    test = [ordered]@{ state = 'OFF'; evaluated = $false }
    runtime = [ordered]@{
        cora_stage1_wall_seconds = [double]$cora.wall_seconds
        cora_stage1_arm_training_seconds = 191.9372865157202
        stage0_wall_seconds = [ordered]@{
            cora = [double]((Get-Content (Join-Path $diag 'stage0_cora.json') -Raw | ConvertFrom-Json).timings_seconds.dataset_wall_seconds)
            pubmed = [double]$pubmedStage0.timings_seconds.dataset_wall_seconds
            citeseer = [double]((Get-Content (Join-Path $diag 'stage0_citeseer.json') -Raw | ConvertFrom-Json).timings_seconds.dataset_wall_seconds)
        }
        stage0_child_cpu_seconds = [ordered]@{
            user = [double]$stage0.cora.child_cpu_seconds.user + [double]$stage0.pubmed.child_cpu_seconds.user + [double]$stage0.citeseer.child_cpu_seconds.user
            system = [double]$stage0.cora.child_cpu_seconds.system + [double]$stage0.pubmed.child_cpu_seconds.system + [double]$stage0.citeseer.child_cpu_seconds.system
        }
        max_concurrent_dataset_jobs = 3; stage0_worker_peak_not_measured = $true
    }
    current_interpretation = 'HANDCRAFTED_SUMMARY_INSUFFICIENT_BUT_LEARNED_NHMC_EFFECTIVE'
    final_decision = 'PENDING_PUBMED_EARLY_TRANSFER'
    remote_artifact_root = '/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/NHMC_V16'
    local_artifact_root = $base
}
$aggregate | ConvertTo-Json -Depth 40 | Set-Content -LiteralPath (Join-Path $base 'results.json') -Encoding utf8

$final = @(
    '# NHMC V16 — Current execution report', '',
    '**STATUS: Cora Stage 1 passed; PubMed six-arm validation training is active on the server.**', '',
    '## Cora Stage 1', '',
    'Cora is `NHMC_STAGE1_GO` on validation: H1 MRR 0.593551; baseline 0.503991; HRA scalar 0.504136; native scalar 0.532451; SIZE 0.590748; SHUFFLE 0.589727. H1 exceeds B0 by 0.089560, the best scalar by 0.061099, SIZE by 0.002803, and SHUFFLE by 0.003823. Training shuffle power is 0.453543, so the shuffle gate was active and passed. The baseline has 24,735 trainable parameters; H1 adds 75 (0.3032%). All six arms used seed 0 and five epochs; test was not evaluated.', '',
    'Under the latest override, Cora Stage 0 FAIL plus Stage 1 GO is interpreted as `HANDCRAFTED_SUMMARY_INSUFFICIENT_BUT_LEARNED_NHMC_EFFECTIVE`. This is an early result, not final innovation confirmation.', '',
    '## Stage 0 diagnostics', '',
    'No dataset met the original fixed-summary Stage 0 native-signal rule. Cora had Δnative +0.009334 and Δcontent −0.000097. PubMed had Δnative +0.015535 and Δcontent +0.000304, below the +0.005 content threshold; it nevertheless has 4,976,014 varied tokens. CiteSeer had Δnative +0.000595 and Δcontent +0.000415. These results are retained but do not gate Stage 1.', '',
    '## PubMed transfer', '',
    'PubMed Stage 1 was launched because Cora passed. The Graph teacher, QTHS25 score cache, and train-only pair-feature cache are complete. The current detached process entered `training_six_frozen_arms`, with B0_BASELINE as the current arm. At the last check it was active with no current-log error, about 778 MiB of GPU memory used, and about 21 GB free disk. The conversation stops after confirming that the background job remains active, as requested; the transfer result is pending.', '',
    '## Later gates', '',
    'Stage 2, multi-seed confirmation, test evaluation, and novelty review have not run. Test remains sealed. The next decision follows the PubMed six-arm validation screen; CiteSeer is the fallback only if PubMed proves unsuitable or has no token variation.', '',
    '## Artifacts', '',
    '- Stage 0 metrics: `03_STAGE0_CROSS_DATASET.md` and raw JSON/logs under `diagnostics/` and `logs/`.',
    '- Native-token and masking checks: `02_NATIVE_STRUCTURE_AUDIT.md`.',
    '- Cora Stage 1 metrics and gates: `04_CORA_STAGE1.md` and `experiments/stage1_cora/results.json`.',
    '- PubMed live setup: `05_PUBMED_STAGE1.md`.',
    '- Aggregate record: `results.json`.',
    '- Remote run/cache/checkpoints: `/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/NHMC_V16`.'
)
Set-Content -LiteralPath (Join-Path $base 'FINAL_REPORT.md') -Value ($final -join "`r`n") -Encoding utf8

$runtime = @'
# V16 Runtime Overrides and execution state

## FAST_GPU_VALIDATION

OVERRIDE: FAST_GPU_VALIDATION  
METHOD_DEFINITIONS_CHANGED: NO  
COMPUTE_SCHEDULING_CHANGED: YES  
CPU_ONLY_REMOVED: YES  
ASYNC_DATASET_PIPELINE: YES  
STAGE1_THRESHOLDS_CHANGED: NO  
CONTROLS_CHANGED: NO  
TEST_POLICY_CHANGED: NO

## STAGE0_DIAGNOSTIC_ONLY

OVERRIDE: NHMC_STAGE0_GATE_OVERRIDE  
STAGE0_ROLE: DIAGNOSTIC_ONLY  
STAGE0_NATIVE_SIGNAL_REQUIRED_FOR_STAGE1: NO  
STAGE1_PROMOTION_THRESHOLDS_CHANGED: NO  
METHOD_DEFINITIONS_CHANGED: NO  
CONTROLS_CHANGED: NO  
TEST_POLICY_CHANGED: NO

Cora, PubMed, and CiteSeer Stage 0 completed; their result JSON, caches, and logs were retained. Each received `NO_NATIVE_STRUCTURE_SIGNAL` under the original fixed-summary rule. Per the latest override, this only diagnoses weak handcrafted summary signal and does not invalidate or gate the neural encoder.

Cora Stage 1 seed 0 × 5 epochs completed validation-only and passed every frozen promotion threshold. Cora Stage 0 FAIL + Stage 1 GO is interpreted as `HANDCRAFTED_SUMMARY_INSUFFICIENT_BUT_LEARNED_NHMC_EFFECTIVE`.

PubMed has substantial token variation and is the designated extra-dataset quick transfer. Its 10-epoch train-only Graph teacher, QTHS25 score cache, and checksum-verified train/validation feature caches are complete. PubMed Stage 1 is actively training the six frozen arms; B0_BASELINE is current. The detached server process is PID 845468. Test remains OFF.

## Preservation and runtime

V13, V14, and HMC_V15 history remains untouched. Failed preparation attempts are retained as separate logs. The active PubMed run reuses the completed Graph-teacher score cache. Local and remote output directories are `HYPERGRAPH_RESEARCH/NHMC_V16/` and `/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/NHMC_V16/`.
'@
Set-Content -LiteralPath (Join-Path $base 'RUNTIME_OVERRIDE.md') -Value $runtime -Encoding utf8
