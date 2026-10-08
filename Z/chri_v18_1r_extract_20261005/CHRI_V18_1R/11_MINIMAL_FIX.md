# Minimal fix

**File:** `HYPERGRAPH_RESEARCH/CHRI_V18_1R/scripts/deterministic_aggregation.py`

**Affected functions:** `endpoint`, `representation`, `install`.

**Bug:** the original endpoint mean uses `torch_scatter.scatter_mean` and the relation sum uses CUDA `index_add` grouped by candidate. Their floating-point atomics can add same-group values in different orders. PyTorch strict deterministic mode does not cover the installed `torch_scatter` extension.

**Fix:** replace only grouped sum/mean/max reductions with `torch.segment_reduce` over the existing sorted contiguous group lengths. Keep the same model, inputs, widths, candidate masks, loss, optimizer, batch construction, and final-epoch selection. Empty groups are explicitly mapped to the original zero representation. The corrected aggregate values differ from the old atomic path by at most the float32 reduction-order drift measured in the parity probe; the new path is bitwise stable across runs.

**Why PubMed was more exposed:** more training candidates and more endpoint-pair interactions create more atomic updates. Cora has the same kernel issue but fewer interactions; its historical comparison happened to remain inside the old gate.

The patch is isolated to V18.1R. `CHRI_V18`, `CHRI_V18_1`, R-HSPE, and test data were not modified.
