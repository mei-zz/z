# Anchor-Conditioned Relational Pair Moment (ARPM)

## Fixed operator

For each target-masked star, let `c` be its anchor and let `M_c` be the remaining members. Compute the mean unordered Hadamard pair moment `P_bar` over pairs in `M_c` using the O(kd) sum-square identity; for fewer than two members, set it to zero. Define

`q_e = [P_bar, h_c ⊙ P_bar, |h_c - W_p P_bar|]`

and encode it with a fixed `Linear(3d,d) + GELU + LayerNorm` relation MLP. Broadcast each edge vector back to its incident nodes and average by incidence degree. Add this as `h_raw + gamma * z_rel`, with `gamma=0` initially.

## Matched arms

- C0: raw global hypergraph only.
- C1: raw plus the PMHE pair-moment branch from Candidate B.
- C2: same anchor-conditioned encoder applied to member mean instead of pair moment.
- C3: the specified anchor-conditioned pair moment.
- C4: if compute permits, randomly reassign the anchor to a member in each unchanged star and rerun C3 as a diagnostic control.

C3 must exceed C0/C1/C2 and meet the registered effect threshold. C4 diagnoses whether the actual anchor helps; it is a preferred mechanism check. Only after GO would the runner evaluate test once for raw, the best validation-matched control, and C3.

## State

Implementation and final server tests are complete (10/10). C ran F0 and F1 on the V100; C3 was rejected because it did not exceed C0/C1/C2. The supplemental C4 diagnostic was also run: C3 exceeded shuffled-anchor C4 by 0.000164 MRR, but that did not change the rejection. All test scoring remains disabled. Full metrics and checkpoints are archived in `remote_evidence/`.
