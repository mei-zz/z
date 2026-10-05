# Construction research ledger — V4

| Candidate | Construction-only hypothesis | Novelty screen | Empirical status | Decision |
|---|---|---|---|---|
| PCHR, LCHR, SSHC, RAHC, HSA, ARHC, PMHE, ARPM | Prior operator, weighting, or routing variants from earlier sprints | Historical | Rejected before V4; not activated or changed here | Closed |
| A — ECPH | Retain each raw ego star and add one `{center} ∪ component` hyperedge for each non-singleton connected component in the center's ego-minus-center graph | `NOVELTY_CONFLICT` for the general center-plus-neighbor-cluster hyperedge template; exact link-prediction augmentation is narrower but unverified | 5-epoch A3 MRR 0.488174681 vs Raw 0.487677542 (+0.000497139); below +0.001 screen gate | REJECT |
| B — ECNH | Retain Raw and add edge-centered common-neighbor groups | `CONCEPTUAL_OVERLAP; EXACT_CONSTRUCTION_UNVERIFIED`; see `01_NOVELTY_SEARCH.md` | 5-epoch B3 MRR 0.487562378 vs Raw 0.487677542 (−0.000115164); no confirmation or test | REJECT |
| C — OWH | Retain Raw and add target-masked, capped open-wedge triples | `NOVELTY_CONFLICT` for generic open/closed motif-hypergraph LP and open-wedge hypergraphs; exact Raw augmentation unverified | 5-epoch C3 MRR 0.485423038 vs Raw 0.487677542 (−0.002254503); also below C1 and C2. No confirmation or test | REJECT |

## ECPH registered comparison and result

- A0 `raw_star`: existing construction.
- A1 `ecph_random`: same per-center group count and size multiset, random neighbor assignment.
- A2 `ecph_degree`: same per-center group count and size multiset, neighbors ordered by message-graph degree ascending and node ID.
- A3 `ecph_true`: actual ego-neighborhood connected components, ignoring singletons.

All arms preserved Raw. Canonical duplicate additions were removed against the raw edges and each other. Random assignment was deterministic per center (`seed = 12345 + center`). The model operator, branch parameters, decoder, loss, optimizer, candidate routing, and top-k behavior remained untouched.

The completed 5-epoch screen had validation MRR A0=0.487677542, A1=0.486871138, A2=0.485220358, A3=0.488174681. Although A3 beat Raw and both controls, the +0.000497139 gain was below the registered +0.001 entry gate. A was rejected; no 10-epoch or test evaluation was run.

## Decision gates

5 epochs, same seed 0, four arms. A3 at or below Raw, gain below 0.001 MRR, or failure to exceed both controls rejects A. Only if A3 exceeds Raw by more than 0.001 and exceeds both controls do matched Raw / best control / A3 10-epoch confirmation. A3 then needs to beat Raw and the matched control and clear either +0.003 absolute MRR or +1% relative gain. GO stops the A→B→C search. Test stays disabled in all screening runs.

Candidate B was rejected at its five-epoch gate: B3 did not exceed Raw. No confirmation or test evaluation was run. Candidate C was the last registered construction; no candidate followed it.

Candidate C was rejected at its five-epoch gate: C3 was below Raw, the random-triple control, and the closed-triangle control. No 10-epoch, multi-seed, or test evaluation was run. All three registered construction candidates are closed; final outcome is `NO_CONSTRUCTION_SIGNAL`.
