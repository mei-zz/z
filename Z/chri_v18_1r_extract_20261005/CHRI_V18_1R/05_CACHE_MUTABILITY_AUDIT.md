# Cache mutability audit

**Result: PASS.** The V18.1 cache clone and V18 cache have identical byte hashes, sizes and preserved mtimes for all audited PubMed seed0 files, and remain unchanged after training. The training and validation loaders use `mmap_mode="r"` for NumPy features and create CUDA tensors from those arrays. The only in-place assignment found, `maximum[counts == 0] = 0`, modifies the temporary result of `scatter_max`, not a cache or shared source tensor.

Candidate IDs, validation features, kNN donor mapping, normalization values, and V18 structure arrays stayed unchanged. `evaluate` loads the fixed candidate order, calls `net.eval()` under `torch.no_grad()`, and does not update buffers. The failure mechanism is floating-point CUDA atomics in grouped reductions, not cache mutation. No test data was accessed.
