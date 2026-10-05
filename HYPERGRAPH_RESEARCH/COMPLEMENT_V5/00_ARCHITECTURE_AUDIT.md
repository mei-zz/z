# V5 Complementarity Architecture Audit

**Scope:** code and registered experiment records were inspected before any V5 model changes. V5 freezes Raw construction, the incidence operator, and the Raw hypergraph branch.

## Historical evidence reviewed

- V4 construction sprint: [final report](../CONSTRUCTION_V4/FINAL_REPORT.md), [results](../CONSTRUCTION_V4/results.json), and candidate run evidence. A, B, and C were rejected; no construction became a winner.
- V3 structural sprint: [final report](../STRUCTURAL_V3/FINAL_REPORT.md) and [results](../STRUCTURAL_V3/results.json). Operator candidates were rejected; the Raw A5 Cora seed-0 5-epoch validation MRR was 0.4876775417205556.
- LCHR: [implementation](../LCHR/01_IMPLEMENTATION.md), [results](../LCHR/results.json), and [final decision](../LCHR/04_FINAL_DECISION.md). Its router added candidate-local hyperedge context to the residual representation and was rejected on its registered screen.

## Actual code path

### Message graph and target masking

`src/dcdlp/models/dcdlp.py` `DCDLP.forward` (around lines 128–138) first calls `mask_pair_edges` for the candidate pairs. The resulting `message_edges` go to the graph `NodeEncoder`; the Raw hypergraph module receives that same masked graph. The train graph itself comes from `GraphDataset.train_graph()` and `train_pos` only. At validation, each positive target is removed before its graph and hypergraph representation is computed.

### Raw hypergraph path

`src/dcdlp/models/hypergraph.py` `_star_members` and `build_hyperedges` construct closed-neighborhood stars from the supplied message graph. `IncidenceResidualComplement.forward` (around line 620) aggregates node states over those stars with the existing unweighted incidence mean, then applies its existing linear projection. In `DCDLP.forward`, the representation is fused additively:

```text
node_state = GraphNodeEncoder(x, message_edges)
h = node_state + RawIncidenceProjection(node_state, message_edges)
```

Thus the current Raw model is **Graph + Hypergraph residual at the node-representation level**. It is neither a hypergraph-only replacement nor a separate graph-score-plus-hypergraph-score decoder. Raw hypergraph information changes the `h` consumed by the pair branches.

### Final decoder

For V4 A5, `ablation_profile("A5")` activates degree, common-neighbor, and residual branches, enables their degree/CN interaction, uses the additive decoder, and adds no auxiliary loss or interventions. The degree branch uses message-graph degrees; the CN branch and residual branch consume the pair representations derived from `h`. The final logit is:

```text
score_degree + score_cn + score_residual + score_interaction + bias
```

The model does not expose an independent `s_g` and `s_h`. For the complementarity audit, `s_g` is therefore defined as the **total logit from the same A5 DCDLP with `hypergraph_mode=disabled`**, while `s_h` is the **total logit from A5 with `hypergraph_mode=raw`**. This holds the pair decoder and branch capacity fixed and compares the actual graph-only and Raw-HG paths.

### Historical variants

- GAE (`src/dcdlp/baselines/gae.py`) is a graph encoder with a Hadamard-product link decoder. It is not the V5 matched Graph-only baseline because it has a different decoder and branch capacity.
- LCHR (`LinkHyperedgeRouter` in `src/dcdlp/models/hypergraph.py`) selects endpoint-local star context and adds it to the residual pair representation; it does not replace the node encoder or final DCDLP decoder.
- V3/V4 operator, routing, weighting, and construction experiments retained or compared against the Raw branch; those experiment decisions and their exact metrics remain in the historical reports linked above.

## Matched baseline contract

The first V5 experiment uses Cora / standard / seed 0 / A5 for 10 epochs, uniform training negatives, the existing 20 uniform validation negatives per positive, AdamW defaults, hidden dimension 16, branch dimension 8, two GCN layers, dropout 0, and batch size 4096. The only arm difference is `hypergraph_mode`: `disabled` for Graph-only vs `raw` for Raw-HG. Both use identical shared model parameter initialization (Graph-only loads shared weights captured immediately before Raw-HG training), the same seed-driven epoch negative samples, and deterministic training-pair permutations. The runner verifies per-epoch negative hashes and shared-initialization hashes. `evaluate_test=false` is set for both. Validation curves, checkpoints, configs, and validation candidate scores are archived under `A_GHHR/remote_evidence/`.
