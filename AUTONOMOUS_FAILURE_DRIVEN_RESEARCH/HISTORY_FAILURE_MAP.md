# Historical Failure Map

## Scope and status

This document closes V1--V5 routes before any new architecture is proposed. It is a failure map, not a claim that every possible variant of a family has been disproved.

| Historical route | What was actually tested | Evidence | Failure / boundary | Do not repeat |
|---|---|---|---|---|
| V1 static local statistics | Disjoint paths, role transitions, block-cut routes, non-backtracking, boundary matching/expansion, role alignment, spectral/community features | Cora HeaRT screening and proxy/shuffle controls | Feature/AUC signals did not reliably transfer to validation/test MRR, Hits or AP; simple controls often matched or won | Do not rename CN/path/boundary/degree statistics as a new propagation rule |
| V2 PCDT | Pair-correspondence decoding with aligned versus shuffled controls | Aligned seed-0 MRR 0.11374, shuffled-evaluation MRR 0.12120; shuffled control won key metrics | The target-correspondence mechanism was not supported; evaluation-time shuffle changed the answer | Do not revisit target-pair correspondence, alignment or edge-boundary matching |
| V2/V3 CDPT | Learned Early/Late cross-depth tensor decoder | V3 3-seed deltas: +0.00800, -0.00565, +0.02385; V4 5-seed Cora mechanism audit had CDPT minus Early×Early = -0.00562 and 0/5 wins | Positive screening was unstable; V4 showed no independent cross-depth mechanism advantage; random/frozen controls were not worse in a decisive way | Do not add attention, gates, losses or width to rescue CDPT |
| V4 reproducibility audit | Strict deterministic repeat and independent reruns | Strict seed-0 repeat was bitwise identical; historical non-strict execution variation reached about 0.01395 test-MRR | Execution noise existed, but deterministic rerun still did not rescue CDPT; the issue is not explained only by CUDA randomness | Do not call a single noisy run an innovation |
| V5 T2WL-INC | Pair-state update `(i,k),(k,j)->(i,j)` | Formula and implementation collided with 2-FWL/Local 2-FWL | Novelty gate failed before training | Do not rename 2-WL, 2-FWL or local 2-FWL |
| V5 other candidates | Temporal shift, topology-aware pair learning, positive/unlabeled link prediction | ONTM remained HOLD; PTALP collided with TMetaNet; EAPU-LP was stopped | No candidate had both a verified independent structure and a minimum experiment | Do not use a different task definition to disguise a static-graph collision |
| Prior V6 search | Complementary propagation, edge/cochain propagation, topology-residual propagation | Collision audit against ECGN/补图 GNN, SLRGNN/Hodge, non-backtracking families and LEAP/CORE | No valid candidate reached GPU training | A new direction must originate from a measured baseline failure, not from a module name |

## What was actually falsified

The following specific hypotheses have negative evidence:

1. Pair-target correspondence alone is a reliable source of link-prediction gain.
2. A learned Early/Late tensor interaction is independently useful on the tested Cora/CiteSeer protocols.
3. Static local/path/boundary statistics, when appended or probed, automatically create a robust MRR improvement.
4. A 2-WL-like pair-state propagation can be presented as an independent contribution in this project.

The following are **not** falsified by V1--V5:

- All incomplete-graph or noisy-graph methods on an explicit edge-missing benchmark.
- All inductive/new-node protocols.
- Every possible hard-negative distribution-shift protocol.
- Every message-passing rule that has a genuinely different state object and is not a disguised pair decoder, 2-FWL, topology editing, or common-neighbor/path statistic.

## Root-cause synthesis

The repeated failure is methodological as much as architectural. The project repeatedly searched for a new calculation inside one narrow static Cora HeaRT protocol before establishing a stable, unmet baseline failure. Once a positive fluctuation appeared, the next experiment was often a new module or a new control rather than a pre-registered test of the same causal claim. This creates three recurrent outcomes:

- the proposed signal is already present in CN/degree/features or an existing strong link predictor;
- the decoder is asked to recover information that the masked encoder never retained;
- the apparent gain is a seed, validation/test-selection, or protocol effect rather than a mechanism effect.

The failure-driven correction is therefore: benchmark failure first, information boundary second, collision audit third, model last.
