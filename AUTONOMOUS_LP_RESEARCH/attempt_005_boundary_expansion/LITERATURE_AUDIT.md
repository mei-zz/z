# Attempt 005 — Literature audit

Working name: Boundary Expansion Deficit (BED)

## Candidate object

For a pair `(u,v)`, split the exclusive one-hop neighborhoods into `A=N(u)\\N(v)` and `B=N(v)\\N(u)`. Expand each side one more hop outside the pair boundary and retain the two-sided frontier sizes, frontier overlap, exclusive frontier masses, normalized growth, and side imbalance. The object tests whether candidate endpoints sit in locally convergent or divergent boundary regions.

## Novelty-kill result

Searches covered 2022–2026 local-neighborhood link prediction, enclosing-subgraph methods, neighborhood expansion, boundary growth, graph diffusion, and pairwise distance/role profiles. Enclosing-subgraph and local-similarity methods are strong neighboring families, so collision is `L1/L2`; BED is retained only as a cheap feature-only probe and is not claimed as a new GNN architecture.

The candidate excludes raw CECG cross-edge counts and the blacklisted matching/cover object. A Stage1 failure will permanently blacklist the exact two-sided expansion profile.

## Sources checked

- [Weighted enclosing subgraph-based link prediction (2022)](https://link.springer.com/article/10.1186/s13638-022-02143-1) — enclosing-subgraph neighbor topology is a nearby control family.
- [Structural Information Enhanced Graph Representation (AAAI 2024)](https://ojs.aaai.org/index.php/AAAI/article/view/29417) — structural/local representation control.
- [NCN/NCNC (ICLR 2024)](https://proceedings.iclr.cc/paper_files/paper/2024/file/9dd67d30e0edd53581363c1b49006e1d-Paper-Conference.pdf) — neighborhood-composition control.
- [PULL (AAAI 2025)](https://ojs.aaai.org/index.php/AAAI/article/view/33966) — recent link-prediction protocol and negative-label setting, but not this static expansion object.
