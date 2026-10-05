# C — Open-Wedge Hypergraph (OWH)

The construction is derived only from each run's target-masked message graph. For each center `w`, inspect pairs `u < v` in `N(w)` and add `{u,w,v}` only when `(u,v)` is absent from that message graph. Each center contributes at most 32 wedges, chosen by ascending `degree(u) * degree(v)`, then node IDs. Raw stars remain in the hypergraph; canonical duplicate hyperedges are removed.

On the registered Cora seed-0 training graph, the audit finds 35,135 open-wedge candidates before the cap, 11,504 selected proposals, and 11,036 unique additions after Raw collisions/deduplication. OWH adds 33,108 incidences to the 11,596 Raw incidences. The count-matched C1 control also adds 11,036 size-3 hyperedges. C2 has 3,003 closed-triangle proposals, which deduplicate/collide to 841 additions.

The fixed screen uses C0 Raw, C1 random triples, C2 closed triangles, and C3 open wedges; each receives five epochs, seed 0, and validation-only selection. The exact gates and any eligible confirmation/test policy are documented in `README.md` and the root task record. The novelty assessment in `../01_NOVELTY_SEARCH.md` records overlap with prior motif-hypergraph link prediction and open-wedge hypergraph work; this is not a broad novelty claim.
