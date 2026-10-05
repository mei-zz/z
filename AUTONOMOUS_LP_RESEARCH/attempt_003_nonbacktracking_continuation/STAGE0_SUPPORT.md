# Attempt 003 — Stage0 support

Status: PASS for a cheap probe; not sufficient for acceptance.

The training-graph-only extractor was run on Cora HeaRT seeds 0–4. Per seed, the positive test set contained 527 pairs, of which 349 had at least one legal non-backtracking continuation, 281 had multiple continuation states, and 133 had high continuation support. The mean total continuation count was 16.8672. Across five seeds this gave 1,745 informative positive pairs and 355,950 informative negative pairs.

Extraction was cheap enough for a probe. The object was not constant, so Stage1 was allowed. This support is not evidence that the continuation profile is predictive.
