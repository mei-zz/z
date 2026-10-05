# Raw construction audit — V4

## Historical matched baseline

The verified V3 `results.json` records Raw 5-epoch validation MRR **0.4876775417205556** for Cora standard, seed 0, A5, uniform training negatives, 20 evaluation negatives per positive, hidden dimension 16, branch dimension 8, two layers, dropout 0, and batch size 4096. The 25 V3 screening/diagnostic runs shared split hash `4ad9a114f501`; none evaluated the test set. These values were read directly from `STRUCTURAL_V3/results.json` and its `FINAL_REPORT.md`.

The V3 construction audit independently records 2,708 nodes, 4,488 undirected train/message edges, 2,620 nonempty raw stars, 11,596 total raw incidences (2,620 center incidences and 8,976 member incidences). `_star_members` forms one `{c} ∪ N(c)` hyperedge for each non-isolated center.

## Leakage boundary

`DCDLP.forward` calls `mask_pair_edges(edge_index, pairs)` before the node encoder and hypergraph branch. The construction builder receives only this target-masked `message_edges` tensor. The runner uses `train_graph()` as its training graph, which is built from `train_pos` only. Validation/test positives are not used to construct any training hypergraph. Per-batch target masking remains active at evaluation.

## V4 construction census

The offline `mei_env` audit reconfirmed Cora standard seed 0: **2,708 nodes**, **4,488** train/message edges, **2,620 raw stars**, and **11,596 raw incidences**.

For true ego components of size ≥2, the audit found **1,342 per-center group proposals** across **1,144 centers**. The mean component count is **0.496 per node** or **0.512 per non-isolated center**. Component sizes have mean **2.988**, median **2**, p90 **4**, and max **52**. Refined centers are **42.25% of all nodes** (**43.66% of non-isolated centers**); their component hyperedges cover **42.25% of nodes**.

Canonical set-union deduplication collapses proposals that already equal a raw hyperedge or another addition: ECPH adds **628 unique hyperedges** and **2,730 incidences**, giving **3,248 total hyperedges** and **14,326 total incidences** on this graph. A1 random partition proposes the same 1,342 per-center groups and size multiset, then adds 925 unique edges; A2 adds 923. Thus the per-center partition controls match the registered count/size rule, while global duplicate removal differs by arm and is reported explicitly.

Mean internal density among group members is **0.830739** for true components versus **0.374346** for random partitions (excluding the ego-center from the density calculation). This confirms the true groups are substantially more cohesive on the audited train graph. Machine-readable values are in `construction_audit.json` and each run's `metrics.json`. The audit is computed from the full Cora train/message graph; model forward passes rebuild hyperedges from each batch's target-masked graph.

## Fixed experiment contract

All arms use the same `hypergraph_mode=raw`, unchanged incidence mean aggregation and projection, A5, split, negatives, seed, optimizer, dimensions, dropout, and batch size. The only arm-level difference is `hypergraph_construction`: `raw_star`, `ecph_random`, `ecph_degree`, or `ecph_true`. No test evaluation occurs during the screen or confirmation stages.
