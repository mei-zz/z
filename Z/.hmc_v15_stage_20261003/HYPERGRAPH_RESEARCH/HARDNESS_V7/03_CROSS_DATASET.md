# Cross-dataset confirmation

- Dataset: citeseer; transfer rule: A4_QTHS25; no dataset-specific parameter tuning.
- Train-only pool hash: e2b8d6babecc441e57b34fe2397238c9143e5a92786cf59affd0338c4015054f; split hash: 5a1a177685a1c3a4852f7e3034ea05ffd35b59aaf05fa58578cd40b0f1c46d36; validation candidate hash: 419f7e31c9320e435b210d3b05614f7d202d95ea9968765df8ceb9f9bdd875c5.
- Held-out identities were not used to exclude the training pool. The full-positive set is used only for validation-negative filtering; no test-split metrics are evaluated.
- Seed-0 screen: {"seed0_mrr": {"Graph-hard": 0.3576036800926328, "Random-veto": 0.35521023310282185, "Winner": 0.37587450402554534}, "proceed_to_three_seeds": true}.
- Three-seed mean validation MRR: {"Graph-hard": 0.41736740809721257, "Random-veto": 0.41183917794148833, "Winner": 0.4270301373473715}; Winner wins vs Graph-hard in 2/3. Supported=True.
- Runtime: Python 3.11, PyTorch 2.8.0+cu128, PyG 2.5.3 on Tesla V100. The project environment declares PyTorch 2.3.1/CUDA 12.1; all comparison arms share this active runtime, but exact lockfile parity is not established.
