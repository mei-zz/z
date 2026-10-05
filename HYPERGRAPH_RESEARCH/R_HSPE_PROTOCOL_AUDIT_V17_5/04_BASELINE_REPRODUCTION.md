# Baseline reproduction and score audit

Both archived runs are complete. V17.3 reports 45/45 jobs and zero failures. V17.4 has complete Phase A/B and fixed-final test artifacts. Hash audit confirms selected/final checkpoints exist and match. No new training is required.

V17.3 NCN/NCNC validation-selected epochs:

- Cora: range 79–99; NCN 98,96,99,90,99; NCNC 79,96,95,91,88.
- Pubmed: range 62–100; NCN 90,72,95,62,71; NCNC 89,97,100,95,98.
- Citeseer: range 45–99; NCN 69,56,68,45,99; NCNC 96,76,61,57,90.

V17.4 paired test results use the identical frozen 20-negative candidates and evaluator. See PAPER_TABLE_B.md for all arms and metrics. Cora NCNC+R-HSPE paired ΔMRR is +0.025853 (5/5); PubMed +0.007137 (5/5). C1−NULL75 mean deltas are +0.027988 and +0.007204. Both datasets meet the stated gates.

Citeseer validation only: mean NCNC+R-HSPE minus NCNC ΔMRR −0.027379, median −0.031435, 0/3 wins. The failed gate prevented test access; CITESEER_TRANSFER is NOT_SUPPORTED.

A preliminary PubMed loader consumed Python RNG before initialization; it was stopped before optimizer steps and excluded. Corrected final runs load the auxiliary view before reseeding. The 54 valid pair comparisons show zero initialization, negative-sample, permutation or CUDA trace mismatches.
