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
