# Operator audit — DCDLP global hypergraph

## Raw construction and propagation

`src/dcdlp/models/hypergraph.py::_star_members` builds one closed-neighborhood star for each node with at least one message neighbor. The list is formed as `[center, *sorted(neighbors)]`; therefore `anchor_id[e] = hyperedge[0]` is explicit and stable. In `DCDLP.forward`, candidate target edges are removed from `message_edges` before the node encoder and hypergraph operator run. The hyperedges therefore come from the target-masked train/message graph.

The raw operator takes the mean node state within each hyperedge, sends that mean to every incident node, averages received messages by node hyperdegree, then applies a learned linear projection. `DCDLP.forward` adds this raw message to the node-encoder state. It is a full-coverage, permutation-invariant node→hyperedge→node operator.

## Cora standard, seed 0 audit

The train-only structural audit in `AUTONOMOUS_V2/structure_diagnostics.json` reports 2,708 nodes, 4,488 undirected message edges, and 2,620 nonempty stars. Thus there are 11,596 total incidences: 2,620 anchor incidences and 8,976 member incidences. The typed incidence split is complete by construction: `H = H_anchor + H_member`; no edge set or node incidence is removed. Non-isolated nodes anchor exactly one star; isolated nodes have no star under the existing construction.

Anchor and member message channels must be normalized separately. On this split, each non-isolated node has anchor degree 1, while its member degree equals its graph degree. The overall incidence totals differ by 3.43×, so a shared unnormalized return sum would be materially imbalanced.

## Baseline evidence and comparability

The directly comparable Cora-standard seed-0 raw run is validation MRR **0.162793** in both `HYPERGRAPH_RESEARCH/LCHR/results.json` (B1) and `AUTONOMOUS_V2/remote_evidence` (A1/B1/C0). The prior [LCHR Stage 1 table](../LCHR/02_STAGE1_RESULTS.md) also records test MRR 0.158069. The older `HYPERGRAPH_RESEARCH/06_FINAL_REPORT.md` gives a different raw value (0.164542), so V3 will not mix it into matched comparisons: every F0 and F1 budget will rerun its own raw control with the same seed, split, negative sampling, decoder, optimizer, dimensions, and epoch count.

## Registered A operator

- A0: raw global hypergraph.
- A1: parameter-matched symmetric residual branch, which pools the complete hyperedge without using anchor identity.
- A2: separate anchor and member node→hyperedge transforms; no multiplicative interaction; symmetric return.
- A3: A2 plus anchor/member Hadamard and absolute-difference features, followed by separately normalized anchor and member return messages.
- A4, only when A3 is best at F1: randomly reassign the anchor role to a node already in each hyperedge; keep the underlying member set and incidence coverage fixed.

Every ARHC branch uses `h_new = h_raw + gamma * h_role` with `gamma=0` at initialization. A1–A4 have the same added parameter count. The training output records the learned gamma and per-epoch validation MRR; coverage is asserted in unit tests, and parameter overhead is derived from the state-dict dimensions. F1 selection is by best validation checkpoint only; test evaluation remains off unless a candidate passes GO.
