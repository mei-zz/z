# V6 idea ledger

| ID | Idea | Status | Decision rule | Evidence pointer |
|---|---|---|---|---|
| V6-A / HVGH | Graph proposes top-2K; frozen Raw-HG score vetoes the highest-plausibility quarter; retain K Graph-hard negatives. | Single-seed GO and 3/3-seed validation STRONG_SIGNAL; independent test did not beat A3 shuffled veto. | Passed the registered validation gate. Test transfer remains unresolved because A3 had higher test MRR. | A_HG_VETO/, 02_QUADRANT_ANALYSIS.md, and results.json |
| V6-B | Select by per-positive percentile disagreement Rg - 0.5 Rh. | Not run; stopped after Candidate A GO. | No B results. | B_DISAGREEMENT/README.md |
| V6-C | Delay purified Graph-hard negatives using the fixed 50/50, 75/25, 100% schedule. | Not run; stopped after Candidate A GO. | No C results. | C_CURRICULUM/README.md |

No model component changes are authorized in this sprint. The term cross-view ambiguous negative is descriptive; no claim that a sampled non-edge is a false negative is made without direct evidence. Do not claim priority from the focused search.
