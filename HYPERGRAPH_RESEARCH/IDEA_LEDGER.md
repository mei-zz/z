# Hypergraph research idea ledger

This ledger is specific to the current round. Historical ledgers under `AUTONOMOUS_LP_RESEARCH/` were not overwritten.

| ID | Candidate | Status | Reason |
|---|---|---|---|
| HG-01 | Adaptive Hyperedge Reliability | REJECT | Standard hypergraph attention/adaptive weighting collision; current reliability/variance blacklist. |
| HG-02 | Structural-role Hypergraph | INCONCLUSIVE backup | Motif/CN/role information has repeated collision and failure risk; no implementation authorized. |
| HG-03 | Shift-aware Hypergraph Fusion | REJECT | Gate/fusion family collides with HL-GNN-PDG and prior V9 attribution result. |
| HG-04 | Pairwise-Complementary Hypergraph Residual (PCHR) | REJECT | Implemented; Cora seed-0 PCHR validation MRR 0.138576 < B0 0.143932 and raw 0.164542; novelty remains unverified. |

## Reuse prohibition

Do not rescue HG-04 by adding attention, reliability weights, gates, extra depth, a new loss, wider hidden states or test-driven tuning. Any future attempt must be a genuinely different structural object and start with a new novelty audit.

