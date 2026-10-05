# Teacher boundary stability

Perturbation is analysis only and is never used in training.

```json
{
  "mode": "DETERMINISTIC_SCORE_PERTURBATION",
  "eligible_frozen_graph_only_teachers": [
    "/home/zhoulihui/lchr_v2/HYPERGRAPH_RESEARCH/NEGATIVE_V6_1/TEACHERS/Graph/checkpoints/cora_uniform_seed0_88990ac8de0c.pt"
  ],
  "row_std_multiplier": 0.01,
  "replicates": [
    {
      "seed": 0,
      "tail_size_spearman": 0.9923631611814665,
      "boundary_exact_match": 0.9621212121212122,
      "selected_negative_match": 0.9311497326203209
    },
    {
      "seed": 1,
      "tail_size_spearman": 0.9939565725358488,
      "boundary_exact_match": 0.9679144385026738,
      "selected_negative_match": 0.9351604278074866
    },
    {
      "seed": 2,
      "tail_size_spearman": 0.9935481824254481,
      "boundary_exact_match": 0.9692513368983957,
      "selected_negative_match": 0.9389483065953654
    }
  ],
  "cross_teacher_stability": "NOT_MEASURED_NO_MULTIPLE_FROZEN_GRAPH_ONLY_TEACHERS",
  "TAIL_BOUNDARY_UNSTABLE": "UNCONFIRMED: report continuous stability; task supplied no numerical flag threshold"
}
```
