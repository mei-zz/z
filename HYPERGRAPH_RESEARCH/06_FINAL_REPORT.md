# 06 — final report

## Executive decision

`STATUS: EXECUTED`

The local audit, module implementation, smoke tests and one-seed Cora standard screen were executed. The proposed PCHR innovation is `REJECT`. LPShift remains `PROTOCOL_BLOCKED`; no incompatible DCDLP number was reported as an LPShift result.

## Direct answers

1. **Current DCDLP limitation.** The model is pairwise at the encoder level: target pairs are masked, then GCN/SAGE node states feed degree/CN/residual branches. There is no explicit incidence or set-valued relation. More importantly for LPShift, `GraphDataset.train_graph()` uses only `train_pos` and drops the official message graph's extra context edges; see `src/dcdlp/models/dcdlp.py:68-79`, `src/dcdlp/data/loaders.py:70-74`, and `AUTONOMOUS_FAILURE_DRIVEN_RESEARCH/V7/DCDLP_AA_BASELINE_AUDIT.md:42-52`.
2. **Selected module.** Pairwise-Complementary Hypergraph Residual (PCHR), implemented as `hypergraph_mode=complement`.
3. **Difference from prior methods.** PCHR does not learn attention or reliability weights. It subtracts the per-node component of a standard incidence message parallel to the pairwise encoder state, then uses a matched linear map. Exact literature novelty is `NOVELTY_UNVERIFIED`; standard hypergraph convolution, attention and hyperedge-dependent embeddings are already established.
4. **Modified files.** `src/dcdlp/models/hypergraph.py`, `src/dcdlp/models/dcdlp.py`, `src/dcdlp/train.py`, `src/dcdlp/evaluate.py`, `src/dcdlp/cli.py`, `configs/model/dcdlp.yaml`, and `tests/test_hypergraph_module.py`.
5. **Real experiments.** 20 final tests passed; smoke B0–B4 seed 0; Cora standard B0–B4 seed 0, each with one training epoch and validation-only checkpoint selection. LPShift DCDLP was not run.
6. **Actual results.** Cora validation MRR: B0 0.143932, raw 0.164542, PCHR 0.138576, shuffled 0.127815, pairwise 0.147698. Test MRR: 0.136209, 0.157838, 0.123553, 0.128608, 0.146744 respectively. Full metrics and traceability are in `04_QUICK_EXPERIMENTS.md` and the result JSON files.
7. **Does the hypergraph itself help?** The raw branch improved this one-seed screen, but the ordinary pairwise-equivalent control also improved. Therefore there is a low-cost signal, not proof that hypergraph representation is necessary.
8. **Does PCHR add independent gain?** No. It is below both the raw hypergraph branch and the original baseline on Cora validation MRR.
9. **Leakage/protocol issues.** The implemented branch uses the post-mask message graph and no held-out labels. Standard Cora/smoke evaluation uses generated negatives as configured. LPShift has a separate unresolved protocol mismatch: extra context edges, custom split and official grouped candidates are not representable by the current loader.
10. **Continue formal experiments?** Not for PCHR or a renamed version. The one-seed mechanism screen is a reject, and novelty is unverified. Do not spend GPU budget on multi-seed PCHR under the current evidence.
11. **Single highest-priority next task.** Build and unit-test a protocol-preserving LPShift adapter with separate `message_edge_index`, `train_pos`, official grouped candidates and target masking; then rerun only the frozen B0/raw control before proposing another module.

## Required final fields

```text
STATUS: EXECUTED
CANDIDATE: Pairwise-Complementary Hypergraph Residual (PCHR)
EVIDENCE: 20 tests passed; smoke B0–B4; Cora standard seed-0 B0–B4; raw hypergraph improved one screen, PCHR did not beat baseline/raw/pairwise; LPShift DCDLP not run because protocol adapter is missing.
DECISION: REJECT
NEXT_EXPECTED_STEP: Implement and audit the protocol-preserving LPShift message-graph adapter.
```

