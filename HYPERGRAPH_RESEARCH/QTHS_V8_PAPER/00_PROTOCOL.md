# V8 protocol — QTHS paperization and backbone generalization

## Frozen method and training protocol

- The only proposed method is QTHS25, with the V7.1 implementation and alpha fixed at 0.25.
- Training uses STRICT_TRAIN_ONLY candidate pools. Validation is used for the registered comparisons; checkpoints are always the fixed final epoch 10.
- All training arms use one negative per training positive per epoch, the same dataset split, 20-item graph-teacher candidate pool, decoder, optimizer configuration and 10-epoch budget.
- The frozen QTHS rule first defines a two-candidate prepool per positive. Alpha is applied to the 2N candidate-occurrence slots and a deterministic hash of the training positive selects which hardest candidates are replaced by their runner-up. Thus alpha=0.25 replaces the hardest candidate for 50% of positive rows. The main rule remains QTHS25 regardless of sensitivity results.
- For the sensitivity sweep, alpha values 0, 0.10, 0.25, 0.40 and 0.60 are evaluated on Cora, seed 0, validation only. Since there are only N positive rows to trim, nominal alpha above 0.50 saturates at replacing all rows. This curve is descriptive and is not used to select a new main rule.

## Registered experiments

1. PubMed: Graph-hard, Random-veto and QTHS25; seeds 0–2; validation first, then one shared test candidate set after all validation checkpoints are frozen. The registered support rule requires QTHS25 test mean MRR above Graph-hard and wins on at least two of three paired seeds.
2. Citeseer: reuse the existing three paired test results. Compute the paired mean and a deterministic 100,000-resample percentile bootstrap confidence interval over seed-level deltas. A confidence interval crossing zero is classified CITESEER_NEUTRAL.
3. Cora backbone study: GCN, GraphSAGE and single-head GAT; Uniform, Graph-hard and QTHS25; seeds 0–2; validation only; fixed epoch 10. GCN reuses V7.1 checkpoints. The experiment-local GAT uses PyG GATConv with one head and concat=False; main project model files are unchanged.
4. Backbone gate: at least two of the three encoders must have higher QTHS25 mean validation MRR than Graph-hard and QTHS25 must win at least two of three paired seeds for each qualifying encoder.
5. Cora controls: RANDOM_HARD50 samples uniformly from the top half of the 20-item graph-teacher pool; SH75 samples uniformly from rank window [50%,75%]. Both use seeds 0–2 and the same fixed epoch-10 budget.
6. Hardness-tail characterization: compute Rg as the within-positive percentile of the frozen graph-teacher score over 20 candidates, where 1 is hardest. Summarize the four observed V7.1 Cora training arms: Uniform, Graph-hard, Random-veto and QTHS25; use all saved epochs and seeds. Also report endpoint diversity, degree, common neighbors, Adamic–Adar, Resource Allocation and shortest-path buckets on the train graph.
7. Efficiency: measure Cora GCN seed 0 training wall time, selection preprocessing, a per-epoch sampling microbenchmark, peak allocated GPU memory and trainable parameter counts. Measure frozen graph-teacher scoring time on the Cora candidate pool. QTHS changes only selected negative pairs and adds zero trainable parameters.
8. Optional transfer: Citeseer Graph-hard vs QTHS25, GraphSAGE, seed 0, validation only.
9. Five-seed stability extension: after the primary gates, add Cora Graph-hard/QTHS25 seeds 3–4 and, only if PubMed is supported, PubMed Graph-hard/QTHS25 seeds 3–4. Reuse the existing first three Cora test rows and V8's frozen PubMed test rows; do not use them to tune QTHS.

## Scope and interpretation

- Do not develop another sampler, alter alpha, change the candidate count, or add model modules.
- The code audit found no ready-to-run DNS, self-adversarial or DMNS implementation in the project. These methods are not reimplemented from scratch; the registered Random-hard and SH75 controls are the matched controls for this sprint.
- Three-seed summaries report mean and sample standard deviation. Paired seed differences and wins are reported directly; bootstrap intervals over three seeds are descriptive, not strong population-level evidence.
- Hardness–performance Spearman correlations describe association only. They do not establish causality.
- If QTHS remains graph-only, frame the paper as graph link prediction and negative sampling rather than forcing a hypergraph title.
