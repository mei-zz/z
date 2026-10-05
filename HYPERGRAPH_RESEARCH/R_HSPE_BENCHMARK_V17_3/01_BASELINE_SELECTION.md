# Baseline selection

| Tier | Method | Decision | Evidence / condition |
|---|---|---|---|
| A | NSLR-HMANN | RUN 5 seeds x 3 datasets | Author [repository](https://github.com/pinglanchu/NSLR-HMANN), DOI [10.1016/j.patcog.2024.110292](https://doi.org/10.1016/j.patcog.2024.110292); canonical MLP pair decoder |
| A | HMNE | REFERENCE_ONLY / NO_VERIFIED_IMPLEMENTATION | [Publisher](https://link.springer.com/article/10.1007/s10115-024-02255-8); preview lacks released runnable pipeline; focused exact-title/acronym GitHub search did not verify author implementation. This is not proof none exists. Do not confuse the unrelated 2021 multiplex HMNE acronym. |
| A | HMRLH | REFERENCE_ONLY / NO_VERIFIED_IMPLEMENTATION | [Publisher](https://www.mdpi.com/2079-9292/12/23/4842); focused paper/title+GitHub search did not verify runnable author pipeline and scorer. No invented neural decoder. |
| A | CCLPH | REFERENCE_ONLY / IMPLEMENTATION_NOT_VERIFIED | [Publisher full text](https://www.nature.com/articles/s41598-026-45116-w) downloaded locally and inspected. Paper supports size2 pairwise candidates, so not categorically TASK_MISMATCH. Complete community construction, six scoring variants, candidate admission and aggregation require faithful implementation. No linked GitHub/code-availability release verified in fetched HTML; replacing community detection with graph Louvain or dropping community filtering would change core method. No fake substitute run. |
| B | NCN | RUN 5 seeds x 3 datasets | [Official repository](https://github.com/GraphPKU/NeuralCommonNeighbor), predictor cn1, exact dataset README config |
| B | NCNC | RUN 5 seeds x 3 datasets | Same official repository, predictor incn1cn1, depth1, exact dataset README config |
| Existing | Frozen B0 | REUSE only after hash audit | Exact V17.2 candidates, evaluator, checkpoints |
| Existing | C1_COUNT_PARAM_MATCHED / C2_CONSTANT_SET | REUSE where already tested | Cora C1 / PubMed C2; selected previously by validation, not this benchmark's test; separate arm rows with missing cells, not one method invented across datasets |
| C | OFSH/OHAA, HP2PH, Hyperedge Copy Model, HNHN, HGNN, HYPER, Hypergraph Motif Representation Learning | RELATED_WORK_ONLY | Frozen novelty matrix governs task distinctions; no unverified canonical ordinary-pair scorer or forced adapter inserted into main quantitative table |

The fair benchmark is complete for the three verified runnable third-party baselines only when every planned seed completes. Literature coverage includes additional reference-only methods, whose quantitative absence is explicit; it is not an exhaustive SOTA benchmark.
