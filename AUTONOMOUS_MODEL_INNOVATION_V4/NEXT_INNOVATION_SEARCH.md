# V4 — Next Innovation Search After CDPT Termination

Date: 2026-09-16  
Status: **search restarted; no new structure has passed a validation gate**

## Failure review carried forward

The V1–V4 records were read before restarting the search. The recurring failure pattern is more informative than any isolated positive seed:

| Family | Recorded outcome | What must not be repeated |
|---|---|---|
| DCDLP degree/CN disentanglement | STOP: no causal mechanism gain | scalar reliability and degree/CN separation as the main novelty |
| MPLP-VC, NCN-CNDP | STOP: variance/second-moment summaries unstable | extra summary statistics of common-neighbor estimators |
| HL-GNN-PDG | STOP: soft gate collapse and memory growth | gates, soft routing, or mixtures of existing depths |
| CECG / L3 and path candidates | STOP: controls or ranking below Parent | renamed common-neighbor, path, or cycle-closure features |
| block/cut, matching, expansion, alignment, spectral, cohesion, community | STOP or proxy failure | boundary, separator, matching, expansion, alignment, and scalar spectral rewrites |
| V2 PCDT | STOP: shuffled evaluation control defeated it | pair-conditioned transport as a rescue route |
| V2/V3 CDPT | V4 MECHANISM_UNSUPPORTED | learned cross-depth tensor interaction as a standalone claim |

The V1 hard-stop record explicitly says that the static undirected Cora HeaRT environment had no remaining executable idea after those collisions. Therefore this restart does not silently revive a blacklisted feature under a new name.

## Literature and collision screen

The broad space is already occupied by closely related structural paradigms:

- [SEAL](https://proceedings.neurips.cc/paper/2018/hash/53f0d7c537d99b3824f0f99d62ea2428-Abstract.html) learns from target-link enclosing subgraphs.
- [GraIL](https://proceedings.mlr.press/v119/teru20a.html) performs inductive relation prediction by local subgraph reasoning.
- [SLRGNN](https://proceedings.mlr.press/v251/lachi24a.html) lifts links to a line graph and learns structural link representations.
- [NBFNet](https://proceedings.neurips.cc/paper_files/paper/2021/hash/f6a673f09493afcd8b129a0bcf1cd5bc-Abstract.html) provides a path-oriented neural Bellman–Ford framework.
- The V3 collision audit also checked multi-level pairwise decoders and conditional message passing; see `AUTONOMOUS_MODEL_INNOVATION_V3/NOVELTY_AND_COLLISION_AUDIT.md`.

These references do not prove that every future construction is already published. They do establish that “local subgraph”, “line graph”, “path”, “multi-level pair decoder”, and “target-conditioned message passing” are not safe novelty claims by themselves.

## One fresh search seed, explicitly not a result

The only candidate allowed into the next Stage-0 ledger is **T2WL-INC: target-pair 2-WL incidence lifting**. It is deliberately not a CDPT modification.

**Structural hypothesis.** Instead of encoding a node pair independently and combining two depths at the decoder, maintain a sparse state for ordered node pairs in the target’s small enclosing region. One refinement step aggregates compatible pair states along `(i,k)` and `(k,j)` incidences, then scores the target pair. The object being changed is the pair-state propagation graph, not the hidden width, loss, gate, or depth-concatenation head.

**Why it is not accepted yet.** This candidate has high collision risk with 2-WL/graph-isomorphism GNNs, SEAL-style enclosing-subgraph learning, line-graph link representations, and common-neighbor/path methods. The literature screen therefore yields **Stage-0 HOLD**, not GO. No implementation or performance number is presented as evidence.

**Cheapest falsifier if Stage 0 survives.** Implement one sparse pair-incidence refinement with a fixed 16-dimensional pair state on the same Cora candidates. Use three validation seeds only for the screen. Compare against a parameter-matched pair MLP, a shuffled incidence map, and a frozen random incidence operator, with the same masked encoder and validation-only checkpoint selection. Stop immediately if the pair update does not beat all controls or if its gain is reproduced by the shuffled/frozen operator.

**Critic before implementation.** The likely explanations are common-neighbor counting in disguise, an enclosing-subgraph capacity increase, indexing leakage, and poor optimization. The experiment must log pair-index hashes, target-edge masking, parameter/compute counts, and a permutation control. A positive screen would still require a new literature audit and five-seed confirmation; it would not establish novelty.

## Search gate

The next candidate can move from HOLD to minimal implementation only if a full title/abstract/code collision audit finds a distinct structural object and the falsifier is pre-registered. The required sequence remains:

`literature dedup → structural hypothesis → critic → minimal implementation → validation screen → matched controls → GO/STOP`

Until that gate is met, the correct research action is to preserve the CDPT negative result and avoid adding attention, gates, auxiliary losses, wider layers, or another depth-mixing decoder.

## Source paths

- V1/V2/V3 failure ledger and blacklist: `AUTONOMOUS_LP_RESEARCH/IDEA_LEDGER.md`, `BLACKLIST.md`, `EXHAUSTIVE_SEARCH_ROUND.md`.
- V2 failure analysis: `AUTONOMOUS_MODEL_INNOVATION_V2/FAILURE_ANALYSIS.md`.
- V3 collision audit: `AUTONOMOUS_MODEL_INNOVATION_V3/NOVELTY_AND_COLLISION_AUDIT.md`.
- V4 formal mechanism data: `AUTONOMOUS_MODEL_INNOVATION_V4/raw/mechanism_cora_v4run3/`.
