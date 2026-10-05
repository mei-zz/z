# Complementarity research ledger — V5

| Item | Definition | Status |
|---|---|---|
| Architecture audit | Trace Graph-only, Raw-HG residual, and final A5 decoder in current code and prior V4/V3/LCHR records | Complete; see `00_ARCHITECTURE_AUDIT.md` |
| Matched baseline | Same A5 DCDLP, initialization, split, negatives, optimizer, dimensions, decoder, and candidate set; Graph-only vs Raw-HG | Complete, validation-only, 10 epochs, seed 0 |
| Oracle audit | Per-positive `max(rr_g, rr_h)` on a fixed shared validation candidate set | `STRONG_COMPLEMENTARITY`, gain +0.0286877 |
| Novelty search | Focused local-web search of dual-view LP and difficulty/hard-negative methods | `CONCEPTUAL_OVERLAP; EXACT_RULE_UNVERIFIED` |
| A — GHHR | Graph-hard-weighted BCE on the existing Raw-HG residual; uniform and shuffled controls | Rejected: A4 0.493500 < A1 0.503012, A2 0.502818, A3 0.493882 |
| B — CVHNM | Balanced cross-view hard-negative selection | Rejected: B4 0.532693 failed strict comparison with B1 Graph-hard 0.533445 |
| C — DAF | Residual fusion gated by graph/hypergraph disagreement and train-negative margins | Rejected: C5 0.496903 < C1 0.503012 and did not exceed C2/C3/C4 |
| Final | No candidate passed its registered GO conditions | `NO_TASK_LEVEL_SIGNAL`; no confirmation/test run |

The oracle identifies per-link complementarity, but this sprint did not produce a task-level candidate that beat all required controls. No V5 test labels were scored.
