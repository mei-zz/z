# DCDLP V5 — Stage-0 Decision

## Locked gates

The gates were applied before any new training: A literature/code deduplication, B historical deduplication, C nontrivial mechanism, D falsifiability, and E resource/data feasibility.

| Candidate | Gate A: literature/code | Gate B: history | Gate C: nontrivial object | Gate D: falsifier | Gate E: current resources | Final Stage-0 status |
|---|---|---|---|---|---|---|
| T2WL-INC | **Fail**: exact 2-FWL/Local 2-FWL association and sparse implementation | Pass as a new name only; structurally closed | Fail as a novelty claim | Not applicable after direct collision | Would be implementable, but that cannot repair collision | **NOVELTY_COLLISION_STOP** |
| C1 ONTM | Hold: temporal memory/motif/code collision audit remains open | Pass relative to static blacklists | Provisional: ordered temporal transition is non-scalar, but may reduce to temporal motif/memory | Pass: order shuffle, recurrence proxy, matched temporal baseline | **Fail for current Cora**; needs temporal benchmark and loader | **HOLD** |
| C2 PTALP | **Fail**: TMetaNet directly uses persistent topology to adapt dynamic GNN updates | Pass relative to static blacklist | Fail as an independent mechanism | Not applicable after direct collision | Not feasible under current static budget | **NOVELTY_COLLISION_STOP** |
| C3 EAPU-LP | Fail/near-fail: temporal PU and graph PU already establish the formulation | Pass relative to structural blacklists | Fail on current data: latent exposure is not observed or identifiable | Pass only on exposure-aware data | **Fail for Cora HeaRT** | **MECHANISM_STOP** |

## Decision

No candidate passed all five gates. In particular, C1 is not a permission to train: it is a HOLD caused by a problem/data shift and an unresolved temporal literature collision. C2 and T2WL-INC are hard collision stops; C3 lacks the required observable mechanism.

Therefore:

```text
STAGE0_RESULT = NO_ELIGIBLE_CANDIDATE
NEW_TRAINING = NOT_AUTHORIZED
CDPT = TERMINATED
T2WL-INC = NOVELTY_COLLISION_STOP
STATIC_CORA_SEARCH = HOLD / CLOSED FOR THIS ROUND
```

The V5 hard-stop rule is applied after the three-candidate budget. No attention, gate, extra depth, larger width, auxiliary loss, new optimizer, renamed 2-WL module, or test-driven rescue is allowed.

## If C1 is revisited in a later stage

It must begin as a new temporal research problem, not as “DCDLP plus a temporal module”. Before implementation it needs:

1. a formula/code collision audit against TGN, DyGFormer, temporal motifs, TGB, and TGB-Seq;
2. a chronological leakage audit and fixed temporal negative candidates;
3. an explicit definition of recurrence/novelty labels and an observable exposure assumption;
4. one repeat-heavy and one low-repeat benchmark;
5. a matched order-shuffled control and a recurrence-only proxy.

No current Cora result can be transferred to that claim.

