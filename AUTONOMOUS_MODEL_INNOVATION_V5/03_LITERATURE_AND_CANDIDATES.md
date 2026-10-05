# DCDLP V5 — Literature Screen and New Candidates

## Search boundary

The search was performed after the T2WL collision decision and covered primary/official sources available by 2026-09-17, with emphasis on temporal/dynamic link prediction, sequential dynamics, topology-aware adaptation, and positive-unlabeled/open-world prediction. The static Cora HeaRT setting remains the default execution environment; a problem shift is not treated as an automatic model change.

The search found no candidate that is both clearly distinct and immediately eligible for a Cora minimal test. Three candidates are recorded because the V5 budget allows at most three; none is presented as proven novel.

## Candidate C1 — Ordered Novelty-Transition Memory (ONTM)

### A. Pain point and evidence

Static Cora HeaRT cannot test the ordering of events or whether a candidate edge is a repeated interaction versus a genuinely new transition. TGB provides realistic temporal link-prediction benchmarks, and TGB-Seq was introduced specifically because common temporal datasets over-emphasize repeated edges and do not sufficiently test sequential dynamics. TGB-Seq reports degradation of existing temporal models on its less-repetitive, sequence-heavy setting and supplies fixed negatives and an MRR evaluator. TGB 2.0 further reports that simple heuristics can remain competitive and that large temporal heterogeneous datasets create substantial scalability failures.

Sources: [TGB](https://proceedings.neurips.cc/paper_files/paper/2023/file/066b98e63313162f6562b35962671288-Paper-Datasets_and_Benchmarks.pdf), [TGB-Seq](https://arxiv.org/abs/2502.02975), [TGB-Seq data/evaluator](https://tgb-seq.github.io/get_started/), [TGB 2.0](https://proceedings.neurips.cc/paper_files/paper/2024/file/fda026cf2423a01fcbcf1e1e43ee9a50-Paper-Datasets_and_Benchmarks_Track.pdf).

### B. Closest methods and code

The closest families are TGN/JODIE/DyRep-style temporal memory, GraphMixer/DyGFormer sequence encoders, EdgeBank recurrence baselines, and TGB/TGB-Seq evaluation. Official benchmark code is available through [TGB](https://github.com/shenyangHuang/TGB) and [TGB-Seq](https://github.com/TGB-Seq/TGB-Seq). This is a collision risk with temporal memory and temporal motif methods, not a novelty certificate.

### C. Proposed mathematical definition

For an event stream `e=(u,v,t,a)`, let `b_uv(t)` record recurrence/exposure history and define a directed ordered two-event transition state

```text
r_uv(t) = sum_a sum_{t1 < t2 < t}
          K(t-t1, t-t2) Psi(e_{u,a,t1}, e_{a,v,t2})
          1[t_uv has not occurred before t].
z_uv(t+) = U(z_u(t), z_v(t), b_uv(t), r_uv(t)),
s(u,v,t) = f(z_u(t), z_v(t), z_uv(t+), r_uv(t)).
```

The proposed object is the ordered, time-decayed transition state `r_uv`, not a static common-neighbor count.

### D. New information/computation

It adds event order, inter-event time, recurrence status, and a directed two-event transition state. The middle entity `a` is not collapsed into a static count; the two incident interactions are retained as an ordered temporal relation.

### E. Difference from existing work

The intended distinction is a pre-registered *new-edge/novelty* subtask and an explicit ordered transition state, rather than another static pair decoder. However, temporal message passing and temporal motif models may already encode the same information implicitly. A formula/code audit against TGN-family and temporal motif implementations is required before any novelty claim.

### F. Difference from historical failures

It is not a static CN, degree, path, community, spectral, boundary, PCDT, CDPT, or 2-WL replacement. Its essential object is timestamped order and recurrence. It nevertheless must not be described as a safe extension of Cora: temporal data and evaluation are required.

### G. Cheapest falsifier

On one small TGB-Seq dataset, compare: Parent-compatible temporal encoder, ONTM, an order-shuffled ONTM control, an EdgeBank/TGN baseline, and a recurrence-only proxy. Use fixed benchmark negatives and validation MRR. If timestamp-order shuffling matches ONTM, or if the recurrence-only proxy matches it, stop the candidate. If it cannot improve on a matched temporal baseline on both a repeat-heavy and a low-repeat dataset, stop it.

### H. Feasibility and cost

Medium/high. The current static DCDLP loader and Cora artifacts are insufficient. A temporal event loader, chronological masking, fixed temporal negatives, event-memory cache, and leakage tests are required. Sparse ordered-wedge updates can be approximately `O(number of observed temporal two-events × d)` per window, but the memory/cache size depends on event history. No V5 implementation was authorized.

### I. Risks and uncertainty

High collision risk with temporal memory, temporal motif, and sequence-aware link prediction. The “novelty state” may collapse to recurrence counting or a standard temporal embedding. Exposure is not observed in Cora, and negative sampling assumptions can dominate any model effect. **Stage-0 status: HOLD**, pending a separately approved temporal-problem audit; not eligible for the current Cora experiment.

## Candidate C2 — Persistent-Topology Adaptive Link Predictor (PTALP)

### A. Pain point and evidence

Dynamic graphs change between snapshots, and fixed parameter updates may fail to reflect structural change. The ICML 2025 paper [TMetaNet](https://openreview.net/forum?id=A6RjIi2ONN) explicitly uses Dowker zigzag persistence to represent high-order changes and to adapt dynamic GNN parameters.

### B. Closest method and code

TMetaNet is a direct method-level and code-level precedent; the paper links its implementation at [github.com/Lihaogx/TMetaNet](https://github.com/Lihaogx/TMetaNet). It is not merely a general mention of topology: it specifies a dynamic persistent-homology representation and uses it to control parameter updates.

### C. Proposed mathematical definition

The candidate would compute a snapshot-change descriptor `P_t = PH(Dowker(G_t), Dowker(G_{t+1}))`, map its distance to an update controller `alpha_t = rho(P_t)`, and update link-predictor parameters as `theta_{t+1} = theta_t - alpha_t grad_theta L_t` before predicting future edges.

### D. New information/computation

Persistent topological features across time snapshots and topology-conditioned parameter updates.

### E. Difference from existing work

There is no defensible difference left at Stage 0: the proposed object and update role are already the central TMetaNet contribution.

### F. Difference from historical failures

It is temporally persistent rather than a static spectral/community feature, but that difference does not overcome the direct literature collision.

### G. Cheapest falsifier

None is needed for novelty: a direct structural/code collision stops it before performance testing.

### H. Feasibility and cost

Not feasible within the static Cora V5 budget; would require temporal snapshots and a persistent-homology dependency/pipeline.

### I. Risks and uncertainty

The only uncertainty is implementation variant, not the core contribution. **Stage-0 status: NOVELTY_COLLISION_STOP.**

## Candidate C3 — Exposure-Aware Positive-Unlabeled Link Prediction (EAPU-LP)

### A. Pain point and evidence

An unobserved edge is not necessarily a negative edge when the graph records only observed interactions. The NeurIPS 2020 temporal PU paper formulates future connectivity as positive-unlabeled learning and estimates a positive prior; PULL (2024) likewise treats observed edges as positives and unconnected pairs as unlabeled. These sources establish that the problem is real and already studied.

Sources: [Temporal PU risk estimation](https://proceedings.neurips.cc/paper/2020/hash/310614fca8fb8e5491295336298c340f-Abstract.html), [PULL](https://arxiv.org/abs/2405.11911), and the [PULL supplementary/code reference](https://openreview.net/attachment?id=bP1cZIsAh1&name=supplementary_material).

### B. Closest methods and code

Closest methods include temporal PU risk estimation, graph PU learning, reliable-negative sampling, and open-world knowledge-graph completion. The current project’s HeaRT benchmark, however, supplies fixed positive/negative candidate sets rather than exposure logs, so the existing Cora protocol does not identify an exposure mechanism.

### C. Proposed mathematical definition

Introduce a latent exposure variable `o_uv` and a latent true relation `z_uv`, with observed positive `y_uv = o_uv z_uv`. Estimate an exposure propensity `pi_uv = P(o_uv=1 | x_uv, history)` and use a corrected risk such as `R = E[y l_+ / pi + (1-y) l_-/ (1-pi)]`, subject to an explicit identifiability assumption and validation on held-out exposure/edge events.

### D. New information/computation

The proposed new object is an exposure propensity, not a graph structural feature. It requires logging who could have formed an edge or a sampling process that identifies exposure.

### E. Difference from existing work

The latent exposure decomposition is an established PU/open-world direction. Without a measured exposure variable, it is a modeling assumption rather than a verifiable new mechanism.

### F. Difference from historical failures

It is not a degree/CN/path/spectral/CDPT variant, but it is not a valid static-Cora architecture candidate and must not be smuggled into the old benchmark by relabeling unobserved pairs.

### G. Cheapest falsifier

On a data source with exposure logs, compare corrected risk, standard PN training, and PU baselines under synthetic-but-known censoring only as a unit test. If the corrected estimator fails when the exposure model is correct, or its gain disappears under exposure shuffling, stop. On Cora there is no valid falsifier because exposure is unobserved.

### H. Feasibility and cost

Low compute but high data/identifiability cost. Requires a new exposure-aware benchmark and protocol; no Cora HeaRT experiment is meaningful.

### I. Risks and uncertainty

High risk of confounding exposure with degree, popularity, or negative-sampling artifacts; direct collision with PU methods; no observable exposure in the current repository. **Stage-0 status: MECHANISM_STOP** for this project.

## Candidate search conclusion

The three candidates do not produce an eligible static-Cora experiment:

- C1 is a HOLD problem shift with a plausible but collision-prone temporal object.
- C2 is a direct published structural collision.
- C3 is an established PU formulation without the data required to identify its new variable.

No additional candidate is generated under the V5 maximum-three rule.

