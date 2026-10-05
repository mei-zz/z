# V5 scope guard

## Frozen components

- Hypergraph construction and Raw-star membership.
- Raw incidence aggregation/operator and Raw branch.
- Hyperedge weighting, routing, attention, and top-k selection.
- Existing split, loss, decoder, and optimizer during the matched baseline audit.

## Stop and candidate order

Run the matched validation-only Graph vs Raw-HG complementarity audit first. If the oracle gain is below 0.003, stop with `NO_COMPLEMENTARITY_SIGNAL` and do not implement A/B/C. Otherwise test at most A GHHR, then B CVHNM only if A rejects, then C DAF only if A/B reject and the audit oracle gain is at least 0.005. Any candidate GO stops the search. Test is permitted only after a 3-seed `STRONG_SIGNAL`.
