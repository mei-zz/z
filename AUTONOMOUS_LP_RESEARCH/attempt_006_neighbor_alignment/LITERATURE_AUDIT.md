# Attempt 006 — Literature audit

Working name: Neighbor Signature Alignment Profile (NSAP)

## Candidate object

For each endpoint, assign its one-hop neighbors a coarse internal role using degree shell and the neighbor's number of links back into that endpoint's own neighborhood. The pair object is the elementwise alignment histogram of the two endpoint neighborhoods, plus aligned mass and neighborhood-size imbalance. It uses no cross-boundary edge count, matching, cut, path continuation, or gate.

## Novelty-kill result

Searches covered 2022–2026 neighborhood-composition link prediction, enclosing-subgraph labeling, role/graphlet methods, similarity learning, and neighborhood alignment. Existing NCN/NCNC and enclosing-subgraph methods make this an L1/L2 collision-risk candidate. No exact complete method using this endpoint-internal role-alignment histogram was found in the current search scope, so it is retained only for a cheap probe.

## Sources checked

- [NCN/NCNC (ICLR 2024)](https://proceedings.iclr.cc/paper_files/paper/2024/file/9dd67d30e0edd53581363c1b49006e1d-Paper-Conference.pdf) — neighborhood-composition control.
- [Structural Information Enhanced Graph Representation (AAAI 2024)](https://ojs.aaai.org/index.php/AAAI/article/view/29417) — structural-role control.
- [Weighted enclosing subgraph-based link prediction (2022)](https://link.springer.com/article/10.1186/s13638-022-02143-1) — enclosing local subgraph control.
