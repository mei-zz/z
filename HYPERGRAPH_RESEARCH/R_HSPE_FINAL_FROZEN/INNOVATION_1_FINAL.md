# Innovation 1 — R-HSPE

INNOVATION_1: R-HSPE  
STATUS: FINAL_FROZEN  
ROLE: HYPERGRAPH_CONTEXT_PLUGIN  
CANONICAL_PROTOCOL: R-HSPE-PAPER-V17.5 (V17.4 fixed-final-10 primary for plugin claim)

## Canonical paired results

- CORA_NCNC: 0.679237 ± 0.052239; CORA_NCNC_PLUS_R_HSPE: 0.705090 ± 0.040646; delta +0.025853, 5/5 wins.
- PUBMED_NCNC: 0.898667 ± 0.015801; PUBMED_NCNC_PLUS_R_HSPE: 0.905804 ± 0.013693; delta +0.007137, 5/5 wins.
- C1−NULL75 mean paired delta: Cora +0.027988; PubMed +0.007204; 5/5 wins each.
- CITESEER: TRANSFER_NOT_SUPPORTED; validation delta −0.027379, 0/3; test not run.

PARAMETER_OVERHEAD: 75  
MECHANISM: CONTEXT_DRIVEN  
SIZE_CAUSAL_CLAIM: NOT_SUPPORTED  
NOVELTY: NO_EXACT_COLLISION_IDENTIFIED_IN_FOCUSED_AUDIT; closest overlap CCLPH and NCN/NCNC.  
NO_MORE_INNOVATION_1_TUNING: TRUE

Position R-HSPE as a lightweight candidate-specific hypergraph-context plug-in providing complementary information to strong pairwise graph link predictors on Cora/PubMed. Do not position it as standalone SOTA. V17.3 remains separate benchmark evidence; scores are not cross-ranked with V17.4.
