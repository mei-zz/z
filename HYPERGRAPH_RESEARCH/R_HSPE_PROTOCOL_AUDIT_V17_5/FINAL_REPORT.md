# V17.5 final report

STATUS: EXECUTED  
DIRECTION: R_HSPE_PROTOCOL_RECONCILIATION  
V17_3_PROTOCOL: 100 epochs; best validation-MRR checkpoint.  
V17_4_PROTOCOL: fixed final epoch 10, matched arms and seed traces.  
DIFFERENCE_CLASS: INTENTIONAL_PROTOCOL_DIFFERENCE  
ROOT_CAUSE: declared training-budget/checkpoint rule; source, data, candidates and evaluator match.  
RERUN_REQUIRED: NO  
CANONICAL_PROTOCOL: R-HSPE-PAPER-V17.5; plugin claim uses V17.4 Phase B; V17.3 remains separate standalone benchmark.  
CORA_CANONICAL_RESULT: NCNC 0.679237; NCNC+R-HSPE 0.705090; paired Δ +0.025853, 5/5; versus NULL75 +0.027988.  
PUBMED_CANONICAL_RESULT: NCNC 0.898667; NCNC+R-HSPE 0.905804; paired Δ +0.007137, 5/5; versus NULL75 +0.007204.  
CITESEER_STATUS: NOT_SUPPORTED; validation Δ −0.027379, 0/3; test NOT RUN.  
COMPLEMENTARY_SIGNAL: SUPPORTED on Cora/PubMed.  
INNOVATION_1: FINAL_FROZEN; Innovation 2 not started.

Audit artifacts and freeze package are complete. No unresolved implementation mismatch remains; no rerun was needed.
