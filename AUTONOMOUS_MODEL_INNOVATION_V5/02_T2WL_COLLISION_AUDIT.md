# DCDLP V5 — T2WL-INC Collision Audit

## Verdict

**T2WL-INC = NOVELTY_COLLISION_STOP.** No GPU experiment was run and no new implementation was created.

The V4 candidate proposes to maintain a state on ordered node pairs and update a target pair through the incidence composition

```text
(i,k) and (k,j) -> (i,j).
```

That is the defining shared-middle-pair operation of 2-FWL. Restricting the state to observed/local pair support is the Local 2-FWL construction. A different encoder, hidden width, MLP, target batch, or enclosing-region truncation would change the implementation budget or application scope, not the core structural object.

## Sources inspected

- Paper: [Two-Dimensional Weisfeiler-Lehman Graph Neural Networks for Link Prediction](https://arxiv.org/abs/2206.09567), especially the introduction, the 2-WL definitions, and the 2-FWL/Local 2-FWL implementation discussion.
- Official repository: [GraphPKU/2WL_link_pred](https://github.com/GraphPKU/2WL_link_pred), official `README.md`, `model.py`, and `utils.py`.
- Raw source inspected: [`model.py`](https://raw.githubusercontent.com/GraphPKU/2WL_link_pred/main/model.py), [`utils.py`](https://raw.githubusercontent.com/GraphPKU/2WL_link_pred/main/utils.py), and [`2WLtest.py`](https://raw.githubusercontent.com/GraphPKU/2WL_link_pred/main/2WLtest.py).

The repository README states that links/2-node tuples are the message-passing units and lists the four variants 2-WL, Local 2-WL, 2-FWL, and Local 2-FWL. Its formulas are the decisive comparison:

```text
2-WL:       N(p,q) = ({(r,q)}, {(p,s)})
Local 2-WL: N(p,q) = ({(u,q) in E}, {(p,v) in E})
2-FWL:      N(p,q) = {((r,q),(p,r))}
Local 2-FWL:N(p,q) = {((r,q),(p,r)): (r,q) in E and (p,r) in E}
```

These definitions are in the official README at the `N(p,q)` formulas immediately after the four-model description. The paper also says that 2-WL-GNNs use node pairs as elemental message-passing units and directly obtain link representations rather than aggregating two independent node representations.

## Structural comparison

| Question | T2WL-INC | Existing 2-WL family | Assessment |
|---|---|---|---|
| State object | ordered/symmetric state for a node pair `(i,j)` | node-pair/2-tuple state for `(p,q)` | same object |
| Association | compatible pairs sharing a middle node: `(i,k),(k,j)` | 2-FWL pairs `((r,q),(p,r))`; set `r=k`, `p=i`, `q=j` | exact shared-middle correspondence |
| Local restriction | intended sparse target/enclosing support | Local 2-FWL keeps only `(r,q)` and `(p,r)` that are graph edges and propagates sparse support | same restriction class |
| Aggregation | learned map of each compatible pair followed by aggregation | 2-FWL sums/aggregates transformed pair states; official implementation uses two MLP branches and matrix multiplication | same mechanism, up to parameterization |
| Update | pair state updated and rescored | pair tensor is updated by MLP after the contraction; local code uses sparse composition then MLP | same computational role |
| Target scoring | only queried target pairs may be materialized | official code materializes the support needed for queried links and scores queried positions | scope difference, not mechanism difference |
| Encoder | may reuse DCDLP masked GCN | official code first obtains node features with a 1-WL-GNN and forms initial pair features | encoder difference only |
| Name/incidence view | “incidence lifting” | 2-FWL’s middle-index join | relabeling, not a new information object |

## Formula-level equivalence

The intended T2WL update can be written as

```text
Z_ij^(t+1) = Phi_t( Z_ij^t,
                    AGG_k Psi_t(Z_ik^t, Z_kj^t) ).
```

For 2-FWL, put `p=i`, `q=j`, and `r=k`. The official neighborhood contains `((k,j),(i,k))`, which is the same two pair states, with order reversed only if the implementation writes the arguments as `(i,k),(k,j)`. An MLP that combines the two states before summation is exactly a learned parameterization of `Psi`; `Phi` is the subsequent state MLP.

For Local 2-FWL, the sum is restricted to the middle nodes for which both incident pair entries are present. T2WL’s proposed local/sparse target support is therefore a support restriction of the same operation. It does not create a new structural relation.

## Source-code evidence

The official `model.py` makes the collision executable rather than merely conceptual:

1. `FWLNet.forward`, lines 286–291, applies two MLPs to the pair tensor, permutes the middle index into matrix dimensions, computes `x1 @ x2`, concatenates the result with the current pair state, and applies another MLP. This is the dense 2-FWL contraction over the shared middle index.
2. `LocalFWLNet.forward`, lines 423–429, calls `sparse_bmm(current_edges, x, edge_index, mul, n, ...)`, then `sparse_cat` and an MLP. `sparse_bmm` in `utils.py`, lines 45–69, performs sparse matrix multiplication channel by channel. This is the local sparse pair-incidence composition.
3. `LocalFWLNet.forward`, lines 439–448, restores queried pairs that are absent from the sparse support with `add_zero`, concatenates the pair result with the endpoint product, and scores the requested pair. T2WL’s target-only scoring path is therefore also present as a standard sparse-support/evaluation optimization.
4. `Net_cora.forward` repeats the same sparse pair composition in `model.py` around lines 556–578, so the Cora-specific implementation does not introduce a different operator.
5. `utils.py`, lines 114–130, maps sparse composed pairs back to queried edge positions and inserts zero values for missing queried support. `utils.py`, lines 160–166, constructs reversed pair-edge views used by local propagation.

The official `2WLtest.py` also exposes all four patterns (`2wl`, `2wl_l`, `2fwl`, `2fwl_l`) rather than leaving Local 2-FWL as a theoretical-only variant.

## Complexity and sparsification

The paper’s implementation section describes dense 2-FWL as slice-wise matrix multiplication over pair tensors, with the shared middle index summed out. A dense pair state has `O(n^2 d)` memory and the contraction is cubic in the node dimension before implementation-specific sparsity/channel constants. The local implementation begins with nonzero entries only on observed edge support and uses sparse matrix multiplication; its work is proportional to the reachable edge-pair composition support (often described by an edge-degree or `sum_v deg(v)^2` term) rather than all `n^2` pairs.

This is not evidence for T2WL novelty: sparsifying a published 2-FWL operator, restricting it to the candidate’s local region, and changing its MLP only changes resource/coverage trade-offs. The paper explicitly notes that Local 2-FWL tracks sparse reachable entries, can learn common-neighbor/path-counting information, and reduces space complexity.

## Possible differences checked and rejected as novelty

- **Different DCDLP backbone:** an encoder choice, even with target-edge masking, is not a new pair-state propagation mechanism.
- **Target-only materialization:** the official local implementation already restores/scores queried pairs after sparse propagation.
- **Enclosing-subgraph or k-hop truncation:** locality/sparsification is already part of Local 2-FWL and is also an application restriction.
- **Learned versus fixed MLP:** parameterization does not change the shared-middle pair association.
- **Symmetric versus ordered notation:** 2-FWL is defined on ordered 2-tuples; converting to an undirected/symmetric score does not remove the collision.
- **One refinement step versus multiple steps:** depth changes iteration count, not the defining operator.

## Cheapest falsifier was not run

No experiment was appropriate after the formula/code collision. A GPU comparison could only show that one implementation or budget is faster/better; it could not repair the lack of a distinct structural object. The correct action is the pre-registered hard stop, not a renamed Local 2-FWL baseline.

