# ECPH implementation and screen

The implementation is construction-only: `build_hyperedges` receives the already target-masked message graph and returns the existing raw stars plus deterministic component-group additions. Isolated ego-neighbors remain covered only by the raw star. Additions use sorted node IDs as canonical keys and do not duplicate an existing raw hyperedge.

`construction_stats` in each run's `metrics.json` describes the unmasked Cora train/message graph for auditability; each actual forward pass still rebuilds its hyperedges from that batch's masked graph. Statistics include raw/add-on edge and incidence counts, component count and size distribution, refined-center ratios, node coverage, and within-group internal density.

The remote runner is `run_a_ecph.py`. It runs A0–A3 sequentially for five epochs with test disabled. Ten-epoch confirmation is conditional on the registered five-epoch screen.
