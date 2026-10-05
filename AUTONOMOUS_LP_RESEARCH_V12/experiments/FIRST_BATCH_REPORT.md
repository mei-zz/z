# V12 First Batch Report

State: STAGE1_BATCH_COMPLETE

Cora standard, seed 0, five fixed epochs, SH75-matched training negatives, fixed-final-epoch validation MRR. Test was not loaded or evaluated.

Matched SH75+BCE baseline MRR: 0.4840758807304911

| Candidate | Decision | Candidate MRR | Delta vs baseline | Matched control MRR |
|---|---|---:|---:|---:|
| V12-F1 | STAGE1_GO | 0.4935642310996936 | 0.00948835036920248 | 0.4856499948724401 |
| V12-G1 | REJECT | 0.4857079488171378 | 0.0016320680866466764 | 0.48296687239391095 |
| V12-C1 | REJECT | 0.4321131245409342 | -0.051962756189556925 | 0.4377790891690408 |
| V12-D1 | STAGE1_GO | 0.4975181162480306 | 0.01344223551753948 | 0.48682597569223657 |

Stage1_GO is not a PAPER_CANDIDATE. Novelty review and Stage 2/3 are still required.
This report is only the first falsification batch. If all ideas fail, derive another batch from the observed failure modes under the registered budget.
