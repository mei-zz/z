# Attempt 009 — Literature audit

Working name: Exclusive-Neighborhood Cohesion Profile (ENCP)

The object measures internal edges, density, mean internal degree, and degree dispersion separately inside `N(u)\\N(v)` and `N(v)\\N(u)`, plus side contrast. It excludes cross-boundary edges, matching, paths, cuts, and common-neighbor variance.

Novelty collision is `L1/L2`: clustering/cohesion-based link predictors are known. Searches covered 2022–2026 local similarity, enclosing-subgraph, motif, and clustering-coefficient link prediction. No exact complete method using this two-sided exclusive-neighborhood cohesion vector was found; it is retained only as a cheap probe.

Source controls: [Structural Information Enhanced Graph Representation (AAAI 2024)](https://ojs.aaai.org/index.php/AAAI/article/view/29417), [NCN/NCNC (ICLR 2024)](https://proceedings.iclr.cc/paper_files/paper/2024/file/9dd67d30e0edd53581363c1b49006e1d-Paper-Conference.pdf), and [link prediction with local similarity and clustering coefficient (2025)](https://doi.org/10.1016/j.physleta.2025.131292).
