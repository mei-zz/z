# Candidate C — OWH

**Status:** rejected after A and B rejected; the sprint is complete with `NO_CONSTRUCTION_SIGNAL`. Focused novelty search is recorded in `../01_NOVELTY_SEARCH.md`; it found a direct generic open/closed motif-hypergraph link-prediction precedent, so OWH is a mechanism experiment and not a paper-core novelty claim.

## Registered construction

Use the already target-masked message graph. For each center `w`, enumerate endpoint pairs `u < v` from its neighbors and retain only pairs with no observed `(u,v)` edge. Rank by `(degree(u) * degree(v), u, v)` and take at most 32 per center. Add `{u,w,v}` to the unchanged Raw-star set and canonicalize duplicates.

## Controls and gate

- C0: Raw stars.
- C1: Raw plus deterministic random triples, matched to the unique C3 additions after Raw collisions and deduplication.
- C2: Raw plus observed closed-triangle triples.
- C3: Raw plus OWH open wedges.

Run the four arms for five epochs on Cora, seed 0. Enter 10-epoch Raw / best-control / C3 confirmation only if C3 beats Raw by more than 0.001 validation MRR, beats C1, and is at least tied with C2 (a lower C3 score rejects). In confirmation, require C3 > Raw and best control plus either +0.003 absolute MRR or +1% relative MRR. A GO triggers the registered 3-seed check and one post-GO test evaluation each for Raw, best control, and C3. No test is used during screening.

## Result

The screen yielded C0=0.487677542, C1=0.486985646, C2=0.487551641, C3=0.485423038 validation MRR. C3 was −0.002254503 versus Raw and was also below both controls. It was rejected at the first gate; no 10-epoch, 3-seed, or test evaluation was run. See `remote_evidence/status.json` and `remote_evidence/results.json`.
