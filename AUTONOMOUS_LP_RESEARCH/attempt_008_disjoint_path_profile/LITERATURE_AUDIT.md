# Attempt 008 — Literature audit

Working name: Internally Vertex-Disjoint Short-Path Profile (IVDSP)

## Candidate object

For `(u,v)`, enumerate legal length-2 and length-3 paths in the training graph and greedily retain internally vertex-disjoint paths. The object records disjoint capacity, mixed length-2/3 capacity, saturation ratios, and the gap between raw path count and disjoint capacity.

## Novelty-kill result

Searches covered 2022–2026 link prediction, path-based predictors, local-path/MPLP, NCN/NCNC, edge-connectivity, and disjoint-path terminology. Path redundancy is a known neighboring idea (`L1/L2` collision), but no exact complete method using this deterministic mixed short-path capacity profile was found in the current search. It is retained for a cheap probe only.

## Sources checked

- [MPLP (NeurIPS 2024)](https://proceedings.neurips.cc/paper_files/paper/2024/hash/85970f7bbc821852c1d17052b88c2451-Abstract-Conference.html) — local path-family control.
- [NCN/NCNC (ICLR 2024)](https://proceedings.iclr.cc/paper_files/paper/2024/file/9dd67d30e0edd53581363c1b49006e1d-Paper-Conference.pdf) — common-neighborhood control.
- [Structural Information Enhanced Graph Representation (AAAI 2024)](https://ojs.aaai.org/index.php/AAAI/article/view/29417) — structural enclosing-subgraph control.
