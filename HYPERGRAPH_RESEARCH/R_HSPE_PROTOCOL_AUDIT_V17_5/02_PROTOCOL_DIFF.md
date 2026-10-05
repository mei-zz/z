# Protocol difference and root cause

**Classification: INTENTIONAL_PROTOCOL_DIFFERENCE.** V17.3 NCN/NCNC ran 100 epochs and tested the first checkpoint attaining maximum validation MRR. V17.4 used a 5-epoch validation screen, then retrained all Phase B arms for 10 epochs and froze the final epoch-10 checkpoint. V17.3 selected epochs are mostly late (45–100); exact per-seed epochs are in results.json.

Data archive, train/validation/test positives, candidates, train-only graph projection, official NCN/NCNC source, scorer and R-HSPE config reconcile. These are not same-compute/same-checkpoint experiments. The lower V17.4 absolute scores are explained by the predeclared horizon/checkpoint rule. Do not combine the scores in one ranking or call cross-version score differences paired deltas.

V17.3 remains the standalone fair-baseline table under official 100-epoch NCN/NCNC settings. V17.4 is the matched 10-epoch plug-in table and canonical evidence for paired complementarity.
