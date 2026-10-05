# Family L: L1 Setwise Rank Calibration — Stage 1 result

**Decision: STAGE1_REJECT.** Five of five Cora seed-0 jobs completed all five epochs. Test evaluation was disabled. The independent result audit passed; see the status-record note below.

## Registered comparison

All arms used the same Raw-HG DCDLP model, frozen Cora split, fixed train-only pool of 20 candidates per positive, QTHS25-selected negatives, and validation candidates. Each arm had 24,735 trainable parameters.

The candidate minimizes one minus the expected reciprocal rank over one positive and its 20 fixed negatives. For each negative it computes an outrank probability sigmoid((s_j − s+)/0.5) and derives the rank distribution via a Poisson-binomial calculation. The loss adds no model parameters.

## Validation MRR

| Arm | MRR | Difference from QTHS25 |
|---|---:|---:|
| QTHS25 + BCE baseline | 0.5256204672 | — |
| L1 expected MRR | 0.3457115803 | −0.1799088869 |
| 20-candidate independent BCE | 0.4870842144 | −0.0385362527 |
| Random-set listwise | 0.5032648386 | −0.0223556285 |
| 20 repeated K=1 BCE | 0.4844376842 | −0.0411827830 |

L1's relative change against QTHS25 was −34.23%. It also trailed independent BCE by 0.1413726342, random-set listwise by 0.1575532583, and repeated BCE by 0.1387261039. The registered baseline-gain threshold and all three control comparisons failed.

## Integrity and status-record correction

- All five archived per-arm records show COMPLETE, five epochs, 24,735 parameters, and test_evaluated false.
- The independent audit reports AUDIT_PASS, no audit errors, 5/5 jobs complete, and the corrected scientific decision STAGE1_REJECT.
- The raw orchestrator status says INFRASTRUCTURE_FAILURE because its summarizer keyed results by human-readable definition strings while looking up symbolic arm names. This is an aggregation-key bug, not a training failure; the individual runs completed and their metrics are available.
- The archived raw result file SHA-256 is recorded in l1_phaseb_stage1_audit.json. The downloaded run archive is remote_results/phaseb_l1_completed/v13_l1_phaseb_completed.tgz.

## Research consequence

L1 is rejected and is not an Innovation 2 result. ECR did not pass its PubMed matched-control gate, so no Innovation 1 is confirmed. No P1 training result is recorded.

## Artifacts

- Audit: remote_results/phaseb_l1_completed/l1_phaseb_stage1_audit.json
- Original status, raw results, per-arm JSON, logs, and checkpoints: remote_results/phaseb_l1_completed/AUTONOMOUS_LP_RESEARCH_V13/
- Full cross-family summary: INNOVATION_RESULTS_SUMMARY.md
