# HL-GNN-PDG V0 source audit

Audit target: the official `LARS-research/HL-GNN` repository, Planetoid files
at the `main` revision used for this screening. The parent files retained in
`Planetoid/` are the audited source snapshot.

Official sources:

- [Planetoid/model.py](https://raw.githubusercontent.com/LARS-research/HL-GNN/main/Planetoid/model.py)
- [Planetoid/planetoid.py](https://raw.githubusercontent.com/LARS-research/HL-GNN/main/Planetoid/planetoid.py)
- [Planetoid/utils.py](https://raw.githubusercontent.com/LARS-research/HL-GNN/main/Planetoid/utils.py)
- [Official repository README](https://github.com/LARS-research/HL-GNN)

## Findings

1. `HLGNN.__init__` creates `lin1 = Linear(data.num_features,
   data.num_features)`, then creates `self.temp` with shape `(K + 1,)`.
2. In `forward`, the input is dropout-regularized and passed through `lin1`.
   The code then propagates one hop at a time. It initializes
   `hidden = X^(0) * temp[0]` and adds `X^(k) * temp[k]` after each subsequent
   propagation. Thus the exact parent is
   `H = sum_k t_k X^(k)`, with a single global vector `t` shared by every node
   and every target pair.
3. The intermediate `X^(k)` values are not stored: the official code keeps
   only the current `x` and accumulated `hidden`. The PDG runner preserves
   this streaming behavior during training; it materializes hops only in the
   no-gradient evaluation path so all edge pools can share one propagation pass.
4. `LinkPredictor.forward(x_i, x_j)` constructs `x_i * x_j`, sends that
   elementwise product through the original MLP, and returns a sigmoid score.
5. `planetoid.py` constructs endpoint pairs by indexing `h[edge[0]]` and
   `h[edge[1]]`, where each edge is transposed from `[num_edges, 2]` to
   `[2, num_edges]`.
6. The official Planetoid commands use Cora
   (`mlp_num_layers=3, hidden_channels=8192, dropout=0.5, epochs=100,
   K=20, alpha=0.2, init=RWR`) and Citeseer
   (`mlp_num_layers=2` with the other values unchanged).
7. `do_edge_split` fixes the official split RNG to Python/torch seed `234`.
   The runner calls this before resetting the requested experiment seed, so
   all variants share the same official split while model initialization,
   DataLoader ordering, and training negative samples are controlled by the
   explicit seed.
8. The official training negative edges are drawn with `torch.randint` in
   each batch. The runner replaces this with a dedicated CPU
   `torch.Generator` seeded per dataset/seed and shared by all variants; its
   batch order is likewise generated independently of model RNG state.
9. `reset_parameters()` in the official `HLGNN` resets `temp` only. It does
   not reset `lin1`. The runner starts one fresh process/model per
   variant×seed, so `lin1` is initialized exactly once from the controlled
   seed; it does not rely on the incomplete official reset for paired runs.
10. `data.edge_index` is replaced with the train positive edges before
    `ToSparseTensor`, so propagation uses the train graph. All topology
    profile features (CN and degree) are computed from that train graph only.

## PDG-specific audit points

- `B2` retains the parent `temp` and adds
  `c * tanh(gate_scale) * tanh(G(profile))`, where
  `c = mean(abs(temp))`, `gate_scale` starts at zero, and the final gate
  layer is zero-initialized. Therefore `w_k(u,v) = t_k` at initialization.
- The four profile inputs are exactly `log1p(CN)`, `log1p(d_u+d_v)`,
  `abs(log1p(d_u)-log1p(d_v))`, and raw-feature cosine similarity.
- `B1` appends the same profile to the original endpoint product in a control
  predictor. `B3` keeps the B2 architecture and independently shuffles profile
  rows inside each positive or negative pool.
