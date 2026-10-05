# LCHR Stage 1 results

Protocol: Cora standard, seed 0, 1 training epoch, 20 uniform negatives per positive. Validation was used for comparison; test MRR is reported once from each completed run. All checkpoints and full metrics are recorded in `results.json` and on the server run directory.

| Arm | Mode | Validation MRR | Test MRR | Params | Train seconds | Peak GPU MB |
|---|---|---:|---:|---:|---:|---:|
| B0 | Graph baseline | 0.143932 | 0.136209 | 24,478 | 4.33 | 45.58 |
| B1 | Global hypergraph | 0.162793 | 0.158069 | 24,734 | 6.97 | 45.58 |
| B2 | Random Top-K | 0.132367 | 0.126946 | 26,000 | 18.34 | 62.04 |
| B3 | Parameter-matched global router | 0.131830 | 0.126971 | 26,000 | 26.48 | 65.18 |
| B4 | LCHR | 0.131696 | 0.126842 | 26,000 | 31.69 | 67.08 |

## Comparisons

- B4 vs B1: −0.031097 validation MRR (−19.10% relative to B1).
- B4 vs B3: −0.000134 validation MRR (−0.10% relative to B3).
- B4 vs B2: −0.000671 validation MRR (−0.51% relative to B2).

B1 improves over B0 in this one-seed screen. Candidate routing adds no independent gain: B4 trails all three relevant controls. Results are a fast falsification screen, not a multi-seed benchmark.
