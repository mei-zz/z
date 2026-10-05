# 05 — ablation and mechanism audit

## Executed low-cost ablation

The Cora seed-0 screen was the prescribed first mechanism check:

- B0: original DCDLP, `hypergraph_mode=disabled`.
- B1: original DCDLP + standard raw star-hypergraph incidence message.
- B2: original DCDLP + PCHR orthogonal complement.
- B3: same enabled branch with shuffled node assignment.
- B4: same incidence source converted to ordinary pairwise co-membership averaging.

All modes used the same split, seed, training negatives, one-epoch budget, evaluation candidates and decoder/loss. The candidate hash was identical across modes: `ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92`.

## Attribution result

| Question | Evidence | Conclusion |
|---|---|---|
| Does adding a hypergraph branch change behavior? | B1 validation MRR 0.164542 vs B0 0.143932; test MRR 0.157838 vs 0.136209. | Yes in this one-seed, low-budget Cora screen. |
| Is the PCHR mechanism independently beneficial? | B2 validation MRR 0.138576, below B0 and B1; test MRR 0.123553. | No evidence; the proposed mechanism is rejected. |
| Is hypergraph incidence necessary rather than an ordinary projection? | B4 validation MRR 0.147698 and AUC 0.392640; B1 remains higher, but B4 also beats B0 on this run. | Hypergraph-specific necessity is not established. |
| Does shuffled structure reproduce the gain? | B3 validation MRR 0.127815, below B0; test MRR 0.128608. | The assignment carries some signal, but this is not enough to prove a novel mechanism. |
| Is the comparison parameter-matched? | Every enabled mode has 24,734 parameters; B0 has 24,478. | Yes within the screen; the 256-parameter branch is exposed. |

## Not run

- No multi-seed stability stage: the selected mechanism failed the first Cora screen.
- No LPShift DCDLP run: current loader/message-graph mismatch is a protocol blocker.
- No full B0/B1/B2 formal benchmark matrix, no GPU memory measurement and no claim about SOTA.

## Decision rule

PCHR would have required B2 to beat B1/B4 under paired seeds while retaining a shuffled-null gap. It did not pass the first falsifier. The raw hypergraph branch is retained as an ordinary hypergraph control only; it is not promoted as a paper innovation.

