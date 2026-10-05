# LCHR Stage 1 implementation

## Scope and identity

- Project: `DCDLP-main`.
- Candidate: Link-Conditioned Hyperedge Routing (LCHR).
- Server: `ubuntu-ProLiant-DL380-Gen9`, Tesla V100 16 GB, existing `mei_env` (Python 3.11, PyTorch 2.8.0+cu128).
- Source tree had no Git metadata, so `git_commit` is recorded as `untracked`.
- Only the Cora standard seed-0 screen was run: 1 pretraining epoch, 0 disentanglement epochs, hidden dim 16, branch dim 8, two GCN layers, dropout 0, uniform training negatives and 20 uniform evaluation negatives per positive.

## Implementation

The candidate pool is the union of star hyperedges incident to the pair endpoints, prefiltered to 32 by neighborhood overlap and routed with Top-K=8. The candidate query uses endpoint states, product and absolute difference; the structural features are endpoint containment, neighborhood overlap and normalized hyperedge size. A learned scalar initialized to 0.1 scales the projected routed context added to the existing residual pair representation.

Modes used for the screen:

- B0 `disabled`
- B1 `raw`
- B2 `random_topk`
- B3 `global_router` (same router parameterization with candidate query and structural features zeroed)
- B4 `lchr`

The B2–B4 modes use the same routed-context projection. Pair-target edges are masked before graph and hypergraph construction. Empty candidate pools contribute a zero context and preserve the existing graph predictor.

## Checks and run status

Local forward/backward smoke and targeted unit tests passed. The remote LCHR smoke run passed, then the five Cora runs completed on the V100. Per-run stdout, stderr, config, metrics and checkpoints are under `/home/ubuntu/lchr_stage1/runs/lchr_stage1/`; a local copy of these artifacts is in `E:\Z\lchr_remote\lchr_stage1\`.

The router diagnostic instrumentation was added after training to evaluate the frozen B4 checkpoint on validation candidates; it did not change model parameters or retrain any baseline.
