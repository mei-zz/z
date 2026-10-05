# Pairwise-Moment Hyperedge Encoder (PMHE)

## Fixed operator

For each unchanged graph-induced star and its complete incidence-node set `x_1,...,x_k`, compute

`P_bar = ( (sum_i x_i) ⊙ (sum_i x_i) - sum_i (x_i ⊙ x_i) ) / (k(k-1))` for `k >= 2`, else zero.

This equals the mean Hadamard product over unordered distinct node pairs and costs `O(kd)` time and memory without materializing pair rows. Project the statistic with a shared bias-free linear map, broadcast its hyperedge vector to all incident nodes, average by node hyperdegree, and add the residual with learnable `gamma` initialized to zero. The raw global hypergraph branch remains intact.

## Matched arms

- B0: raw global hypergraph only.
- B1: raw plus the same learned projection applied to the hyperedge mean.
- B2: raw plus the same projection applied to the mean elementwise second moment.
- B3: raw plus the same projection applied to the normalized unordered pair moment.

The projection and scalar residual gate are parameter matched across B1–B3. All arms retain every hyperedge and incidence. The star is built from the target-masked message graph. F0/F1 validation scoring does not evaluate test; the runner only evaluates test checkpoints if B3 passes the preregistered F1 GO rule.

## State

Implementation and server tests are complete (8/8 after PMHE; 10/10 after the final ARPM module). F0 and F1 completed on Cora, standard protocol, seed 0, V100 / `mei_env`; B3 was rejected. Validation curves and checkpoints are archived in `remote_evidence/`. Test evaluation was not run.

F1 best validation MRR: B0 0.487678, B1 0.487893, B2 0.487971, B3 0.487705. B3 gained only 0.000027 over B0 (0.0055% relative) and lost to both moment controls. The branch adds 257 trainable parameters (1.04% over the 24,735-parameter raw model); B3 training took 35.3 s vs. 33.4 s raw in this single run.
