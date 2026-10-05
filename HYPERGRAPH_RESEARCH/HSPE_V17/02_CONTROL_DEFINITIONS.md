# Frozen controls

B0 — Strong baseline: V16 Raw-HG DCDLP A5 with raw-star hypergraph context and QTHS25 training negatives; no HSPE residual.

C1 — Histogram scalar: cardinality bins 2, 3–4, 5–8, 9–16, and at least 17. The unordered pair gives 15 bins. Features are the normalized 15-bin histogram, log(1+token_count), and log(1+shared_support_count). A single zero-initialized Linear(17,1) emits the scalar residual; no hidden layer.

C2 — Size-shuffle: exact complete size-token multisets are assigned to different candidate pairs within the same train or validation split, exact token-count group, shared-support-count bin, and sorted endpoint-degree-bin pair. This preserves token counts and the size-token multiset while breaking the candidate-to-size-configuration assignment. The 30% power rule is recorded separately for train and validation; the gate calls it adequate only when both splits reach 30% for every seed.

C3 — Parameter-matched: exact V16 C1 token encoder, pooling, residual head, and parameter count; each size descriptor is replaced with the dataset-independent constant [1,1,1]. Real token count and shared-support count remain available.

H1 — HSPE-REAL: exact frozen V16 C1_NHMC_SIZE implementation, with real candidate-specific size-pair tokens and all overlap inputs zeroed.

All residuals start at zero, so each arm’s initial baseline logits must match within 2e-7. Test evaluation is disabled.