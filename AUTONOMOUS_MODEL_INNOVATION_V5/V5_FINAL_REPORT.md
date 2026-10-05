# DCDLP V5 — Final Report

Date: 2026-09-17  
Overall state: **HOLD for a separately reviewed temporal problem shift; STOP for CDPT/T2WL-INC and the current static-Cora innovation search.**

## Executive conclusion

T2WL-INC is not a new link-prediction mechanism. Its `(i,k),(k,j) -> (i,j)` pair-incidence update is the shared-middle association already defined by 2-FWL; restricting it to observed/local support is Local 2-FWL. The official paper and implementation contain both the dense matrix-contraction and sparse pair-composition versions. V5 therefore stopped the candidate before GPU execution.

CDPT is also closed. V4’s matched Cora evidence does not isolate learned cross-depth interaction: CDPT lost Early×Early on all five validation seeds, was effectively tied with Late×Late, and lost to the frozen random operator on average. This is a mechanism rejection, not a claim that every depth combination is useless.

## Answers to the required questions

1. **Does T2WL-INC overlap substantially with existing work?** Yes. It is a direct structural overlap with 2-FWL/Local 2-FWL, including the state object, shared-middle association, aggregation role, sparse support, and queried-pair scoring path. See [`02_T2WL_COLLISION_AUDIT.md`](02_T2WL_COLLISION_AUDIT.md).
2. **Are historical failures excluded?** Yes. V1 feature families, V2 PCDT/CDPT, V3 controls, V4 A–E mechanisms, and early A5/A14/A14-w010 records were audited and their no-retry boundaries are recorded. The early A14 summary is explicitly marked incomplete/invalid for confirmatory use where the local paired artifacts are missing and test-selected weights were used.
3. **What does a new candidate add?** The only non-collision candidate is ONTM, which would add ordered timestamped two-event transitions and recurrence state for future *new-edge* prediction. It is a problem/data shift, not a validated static-Cora structure.
4. **How does it differ from closest papers?** The intended ONTM distinction is explicit ordered novelty-state computation, but TGB/TGB-Seq and temporal-memory/motif methods make the collision risk high; no novelty claim is made. PTALP is directly covered by TMetaNet, and EAPU-LP is covered by PU/open-world link prediction.
5. **Was the minimal experiment completed?** No. `05_MINIMAL_EXPERIMENT_REPORT.md` records `NOT_EXECUTED` because no candidate passed all Stage-0 gates. No GPU run or new raw result was fabricated.
6. **What are the original performance and controls?** The relevant original numbers are preserved in V4: Cora validation MRR A/Early×Early `0.109457`, B/Late×Late `0.103374`, C/CDPT `0.103837`, D/Concat `0.098977`, E/Fixed Random `0.105747`; paired C−A `−0.005620`, C−B `+0.000463`, and C−E `−0.001909`. The full seed-wise metrics and all checkpoints remain under V4 raw paths.
7. **Current status?** `T2WL-INC = NOVELTY_COLLISION_STOP`; `CDPT = TERMINATED`; V5 candidate batch has no eligible experiment; overall research direction is **HOLD** only because ONTM would require a new temporal-data review.
8. **Next step?** Do not continue static undirected Cora structural search or modify CDPT. If research continues, review ONTM as a new temporal benchmark problem with TGB/TGB-Seq, chronological leakage controls, recurrence proxies, and order-shuffled falsification. If that review does not establish a distinct mechanism, stop the current search space.

## Literature evidence

The 2-WL paper explicitly distinguishes 2-WL, Local 2-WL, 2-FWL, and Local 2-FWL and treats node pairs as message-passing units; the official repository provides the corresponding formulas and code. [Paper](https://arxiv.org/abs/2206.09567), [official code](https://github.com/GraphPKU/2WL_link_pred). TGB-Seq provides fixed negatives and MRR evaluation for sequence-heavy temporal link prediction, while TMetaNet explicitly uses Dowker zigzag persistence for dynamic link prediction. [TGB-Seq](https://tgb-seq.github.io/get_started/), [TMetaNet](https://openreview.net/forum?id=A6RjIi2ONN).

## Artifact index

- [`01_HISTORY_AND_BLACKLIST.md`](01_HISTORY_AND_BLACKLIST.md)
- [`02_T2WL_COLLISION_AUDIT.md`](02_T2WL_COLLISION_AUDIT.md)
- [`03_LITERATURE_AND_CANDIDATES.md`](03_LITERATURE_AND_CANDIDATES.md)
- [`04_STAGE0_DECISION.md`](04_STAGE0_DECISION.md)
- [`05_MINIMAL_EXPERIMENT_REPORT.md`](05_MINIMAL_EXPERIMENT_REPORT.md)
- Historical V4 formal raw artifacts: `AUTONOMOUS_MODEL_INNOVATION_V4/raw/mechanism_cora_v4run3/`
- Historical V4 CiteSeer extension: `AUTONOMOUS_MODEL_INNOVATION_V4/raw/mechanism_citeseer_v4/`

