# CDPT Deepening V3 — Phase 0 Audit

## Historical protocol issue

V2 used Cora HeaRT test MRR/Hits to select and promote CDPT. This creates test-set selection bias. V2's internal checkpoint selection used validation MRR, but the subsequent architecture decision read test results. V3 therefore treats V2 test gains as exploratory historical evidence only.

V2 also initialized Parent and CDPT from matched common weights, but trained them sequentially without resetting the complete random state before each training run. Their dropout streams were not fully paired. V3 resets Python/NumPy/PyTorch randomness before every model construction and every training run, while keeping the common Parent state identical.

## V3 repair

- B0--B4 are fixed before any V3 test result is inspected.
- Checkpoint selection uses validation MRR only.
- Test metrics are written only as frozen-protocol reports; `test_used_for_selection=false` is stored in every result.
- Cora test is reported with the historical-selection caveat. A second official dataset is required for an independent final decision.
- Parent, CDPT, and every mechanism control use the same train positives, uniform training negatives, HeaRT grouped validation/test candidates, target-edge masking, optimizer, epochs, dimensions, and seeds.
- Candidate edges are removed before node encoding by the repository's vectorized `mask_pair_edges`; no validation/test positive is inserted into the message graph.
- The legacy shuffled control rolls early pair-state rows relative to late pair-state rows. It is retained for V2 comparability, but is labeled pair-alignment shuffle rather than pure depth-order shuffle.
- CUDA graph execution is not bitwise deterministic in this path. Resource-complete reruns therefore provide resource fields only; the first complete five-seed metric batch remains the single performance aggregate.

## Model matching

- B0: original DCDLP Parent.
- B1: CDPT cross-depth tensor contraction.
- B2: same CDPT extra parameter budget and pair-state encoder, but late state contracted with itself; the early state is not used.
- B3: early+late concatenation MLP; its extra parameter count differs from CDPT by 33 at the locked 64/32 dimensions.
- B4: same CDPT path with a fixed random operator sampled once at construction, frozen thereafter; it is never resampled at evaluation.

The V3 runner records total/trainable parameter counts, data/code/config hashes, validation selection metadata, checkpoints, score-path contribution, peak memory, and runtime. The initial metric batch predated peak-memory instrumentation for Cora seeds 0–2; a separate resource-complete rerun supplies those fields without replacing the original metrics.

## Gate

The audit was repaired before the new V3 performance comparison. The actual result is therefore an auditable mechanism comparison, not a continuation of test-driven V2 selection.
