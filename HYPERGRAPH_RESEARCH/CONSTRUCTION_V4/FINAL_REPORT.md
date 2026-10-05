# Hypergraph Construction Innovation Sprint V4 — Final Report

**STATUS:** EXECUTED  
**RAW_CONSTRUCTION:** Per non-isolated center, one target-masked closed-neighborhood star `{c} ∪ N(c)`.  
**RAW_5EPOCH_MRR:** 0.4876775417205556 (seed 0, Cora standard split); reproduced the registered V3 value.  
**TEST_POLICY:** No candidate passed its registered GO gates. Test scoring remained disabled throughout; no test metrics were produced.

## A_ECPH — REJECT

- Construction: retained 2,620 Raw stars; 1,342 non-singleton ego-component proposals across 1,144 centers; 628 unique additions and 2,730 added incidences. Component size mean 2.988, median 2, p90 4, max 52. Refined-center ratio 42.245% of all nodes (43.664% of non-isolated centers); added-group node coverage 42.245%. Mean internal density was 0.830739 for true components vs 0.374346 for the random partition control.
- Five-epoch validation MRR: A0 Raw 0.487677542; A1 random 0.486871138; A2 degree-sorted 0.485220359; A3 true components 0.488174682.
- A3 gain over Raw: +0.000497139 (+0.10194%), below the +0.001 screen gate. Rejected; no 10-epoch or test evaluation.
- A3 training runtime 47.33 s vs Raw 33.94 s (+39.43%); peak GPU allocator use 43.42 MiB vs 43.30 MiB.

## B_ECNH — REJECT

- Construction: 2,005 observed train edges had at least one common neighbor. B3 canonicalized to 924 unique additions and 3,391 incidences, with common-neighbor cap 16. B1 random-endpoint and B2 union-neighborhood controls each matched 924 additions and the exact B3 added-hyperedge size multiset.
- Five-epoch validation MRR: B0 Raw 0.487677542; B1 random 0.487055545; B2 union-neighborhood 0.485338383; B3 true common-neighborhood groups 0.487562378.
- B3 gain over Raw: −0.000115164 (−0.02361%). Rejected because it did not exceed Raw; no 10-epoch or test evaluation.

## C_OWH — REJECT

- Construction audit on the target-masked Cora train graph: 35,135 open-wedge candidates before cap; 11,504 selected proposals over 1,804 centers; after 468 Raw collisions/duplicate proposals, 11,036 unique additions and 33,108 added incidences. Each center was capped at 32 using endpoint-degree product ascending, then node IDs.
- C1 random control exactly matched 11,036 size-3 additions. C2 had 3,003 closed-triangle proposals and 841 unique additions after canonicalization and Raw collisions.
- Five-epoch validation MRR: C0 Raw 0.487677542; C1 random triples 0.486985646; C2 closed triangles 0.487551641; C3 open wedges 0.485423038.
- C3 gain over Raw: −0.002254503 (−0.46229%). C3 was also below C1 and C2, so it was rejected at the first gate. No 10-epoch, 3-seed, or test evaluation.
- C3 construction overhead: 11,036 additions over 2,620 Raw stars (+421.22% hyperedges; 13,656 total, 5.212× Raw). Incidences increased from 11,596 to 44,704 total (3.855× Raw). Training runtime was 86.95 s vs Raw 36.32 s (+139.35%); peak GPU allocator use 49.42 MiB vs 43.30 MiB (+14.12%).

## Final decision

**WINNING_CONSTRUCTION:** None.  
**BEST_VALIDATION_MRR:** 0.488174682, observed for A3 at the 5-epoch screen; this did not satisfy A's +0.001 entry threshold and is not a winning result.  
**ABSOLUTE_GAIN:** Best observed A3 vs Raw +0.000497139; final candidate C3 vs Raw −0.002254503.  
**RELATIVE_GAIN:** Best observed A3 vs Raw +0.10194%; C3 vs Raw −0.46229%.  
**NOVELTY_STATUS:** A has a direct center-plus-neighbor-cluster structural precedent; B has conceptual overlap with edge-centric hypergraphs and common-neighbor link prediction; C conflicts with generic motif-hypergraph link prediction and open-wedge hypergraphs. Exact narrow formulations remain unverified, and none is advanced as a paper-core novelty. Sources and scope are recorded in `01_NOVELTY_SEARCH.md`.  
**HYPEREDGE_COUNT_OVERHEAD:** C3 adds 11,036 unique size-3 hyperedges (+421.22% relative to the 2,620 Raw stars).  
**RUNTIME_OVERHEAD:** C3 +139.35% vs C0 Raw for the registered 5-epoch run; memory stayed below 50 MiB on the V100.  
**FINAL_DECISION:** `NO_CONSTRUCTION_SIGNAL`.  
**NEXT_EXPECTED_STEP:** Stop this sprint. Do not create Candidate D or run any unregistered follow-up.

Detailed per-run configurations, metrics, validation curves, logs, and checkpoints are stored in each candidate's `remote_evidence/` directory. The registered environment was the offline V100 server using `mei_env`. The complete repository test suite passed before the C screen (19 passed).
