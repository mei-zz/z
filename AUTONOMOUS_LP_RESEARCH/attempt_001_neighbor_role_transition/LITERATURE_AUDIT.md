# Attempt 001 — Literature audit

Working name: Neighbor-Role Transition Matrix (NRTM)

Candidate ID: `R1-07`

## Parent sees

The parent LP pipeline sees endpoint node representations and the usual pairwise controls: CN, AA, RA, endpoint degree product, L3/path counts, and (depending on parent) explicit common-neighbor aggregation.

## Parent misses

For a candidate pair `(u, v)`, the parent does not receive the joint role relation of the two internal nodes `(a, b)` on each length-3 path `u-a-b-v`. The candidate represents that relation as a symmetric 4×4 upper-triangular histogram of degree-shell transitions. The total number of paths is separately controlled by L3.

## Novelty-kill result

- Exact working-name search: no complete method found in this round.
- Synonym search: “role transition”, “path role profile”, “degree-shell transition”, “joint internal-node role relation”, and “structural role transition matrix” were searched with link prediction, KGE, recommender, graph classification, and graph matching terms.
- Strong neighboring work: SEAL/enclosing-subgraph methods, NBFNet/path reasoning, MPLP, BST, graphlet/motif LP, and CECG/CH2-L3/CH3-L3 controls.
- Collision: `L1/L2`. The distinction is the fixed candidate-conditioned joint role-transition object on length-3 paths, tested incrementally beyond L3 and the existing scalar controls; it is not an enclosing-subgraph GNN, a generic attention/gate, a CN statistic, or a line-graph model.
- Search conclusion: keep only because it is cheap to kill and has a sharply defined incremental hypothesis. Any failure ends this candidate immediately.

## Most dangerous prior checks

- `MPLP`: controls length-based structural estimates; candidate must beat L3 and MPLP-like scalar controls.
- `CECG/CH2-L3/CH3-L3`: controls degree/context functions on length-3 witnesses; candidate must beat these controls.
- `SEAL/BST/SLRGNN`: broad collision with pair-conditioned structure; candidate is not claimed globally unique.
- `CN graph / CNNC / HGNN-CNA`: common-neighbor relation is nearby; candidate uses length-3 internal role transitions and must not be described as common-neighbor graph structure.

## Why it cannot be killed more cheaply

The only cheaper tests are support and a label-free permutation check. The actual question is incremental predictive signal beyond L3 and dangerous scalar controls, so a train/validation logistic probe is the minimum experiment. No GPU training is justified before it passes this probe.
