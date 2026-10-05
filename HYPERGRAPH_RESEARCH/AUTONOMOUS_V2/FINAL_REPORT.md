# Autonomous Hypergraph Innovation Loop V2 — Final Report

**STATUS: EXECUTED**  
**FINAL_DECISION: `NO_EXECUTABLE_IDEA_AFTER_3_CANDIDATES`**

All three candidates completed their bounded Cora seed-0 falsification runs on the V100 server. No candidate met its registered GO rule. No Stage 2 confirmation or new V2 test evaluation was run. The corrected C run is the one retained; the earlier C batch with mismatched initialization was discarded.

## Baselines and diagnostic

| Arm | Validation MRR | Test MRR |
|---|---:|---:|
| Graph baseline | 0.143932 | Not newly evaluated |
| Raw global hypergraph | 0.162793 | Not newly evaluated in V2 |

The prior LCHR report records raw B1 test MRR 0.158069 under the same Cora standard seed-0 one-epoch setup. This is carried forward as a baseline only; V2 candidate runs all had `evaluate_test=false`.

The train-only structure audit found 2,620 non-empty star hyperedges over 2,708 nodes and 4,488 message edges. Mean off-center cohesion was 0.187 (median 0; P90 0.667); mean shared-node top-3 Jaccard redundancy was 0.392. Cohesion had near-zero Pearson association with size (`r=-0.006`) but moderate rank association (Spearman `rho=0.469`), supporting the registered size control. Full distributions are in [00_STRUCTURE_DIAGNOSTICS.md](00_STRUCTURE_DIAGNOSTICS.md).

## Candidate decisions

### Candidate A — SSHC

Initial A4 MRR was 0.164051, a +0.001258 (+0.77%) gain over raw and only +0.000068 over shuffled cohesion; it was below the registered gain threshold. After the sole allowed initialization adjustment (`a=-5` to `a=-3`), A4 was 0.163446: +0.000653 (+0.40%) over raw, but −0.000537 versus shuffled cohesion at 0.163983. **Decision: REJECT.** Details: [A_SSHC/REPORT.md](A_SSHC/REPORT.md).

### Candidate B — RAHC

True redundancy B4 reached 0.162889, just +0.000096 (+0.06%) over raw, while size control reached 0.163352 and shuffled redundancy reached 0.166308. **Decision: REJECT.** Details: [B_RAHC/REPORT.md](B_RAHC/REPORT.md).

### Candidate C — HSA

The best true arm, C3 with `lambda=0.05`, reached 0.164475, +0.001681 (+1.03%) over raw and +0.001022 over the best shuffled-label control at 0.163453. It exceeded the controls but missed both absolute (+0.003) and relative (+2%) gain thresholds. `lambda=0.10` scored 0.162377. C0 and initialization-matched C1 were identical at 0.16279348007164107. **Decision: REJECT.** Details: [C_HSA/REPORT.md](C_HSA/REPORT.md).

## Final selection and next step

**WINNING_CANDIDATE:** None.  
**BEST_VALIDATION_MRR:** 0.166308, from B3's shuffled-redundancy control; this is not a candidate win.  
**BEST_TRUE_INNOVATION_ARM:** C3 (`lambda=0.05`), 0.164475; rejected by the effect-size rule.  
**NOVELTY_STATUS:** `NOVELTY_CONFLICT` for all three candidates; see the ledger and candidate reports.  
**MECHANISM_EVIDENCE:** SSHC did not beat its shuffled control after correction; RAHC real overlap trailed both controls; HSA's auxiliary branch sampled 4,398 pairs over three batches, and its best true arm beat controls but produced a sub-threshold validation gain.  
**NEXT_EXPECTED_STEP:** Stop this bounded search. No fourth candidate, extra tuning, or Stage 2 confirmation is authorized by the registered protocol.

Per-run configs, validation metrics, runtimes, and completion statuses are retained under [remote_evidence](remote_evidence/). The V2 screen used Cora standard, seed 0, one pretraining epoch, zero disentanglement epochs, 20 uniform evaluation negatives per positive, hidden dimension 16, branch dimension 8, two layers, and no dropout.
