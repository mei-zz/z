# CDPT Deepening V3 — Novelty and Collision Audit

## Scope

This is an attribution and collision audit, not a claim that the experiments prove publication-level novelty. V2 already recorded that CDPT is adjacent to bilinear/low-rank link decoders, multi-scale pair representations, layer aggregation, and conditional message passing. V3 tests whether the claimed mechanism survives controls.

## Collision matrix

| Nearby family or explanation | Overlap with CDPT | V3 evidence |
|---|---|---|
| Ordinary bilinear link decoder | Learned matrix contraction of two pair representations | B2 late-only keeps the same parameter budget and matrix path; it matches or exceeds CDPT on Cora test MRR |
| Multi-scale/layer aggregation | Pair states are extracted at more than one encoder depth | B3 concat MLP tests whether explicit cross-depth tensor contraction is needed; it reproduces part of the Parent gain |
| Conditional / target-aware message passing | Pair-conditioned features can change endpoint scoring | The implementation preserves target-edge masking and adds a pair decoder, so attribution must remain separate from the encoder |
| Fixed random operator | Same path and dimensions without learned operator | B4 improves over Parent on Cora validation and is not below CDPT by a decisive margin |
| Pair-alignment shuffle | Breaks alignment between early and late pair states | Cora and CiteSeer move in opposite directions; it is a diagnostic, not a clean proof |
| V2 PCDT | Earlier candidate using pair-conditioned local transport | V2 PCDT was already stopped after the shuffled control; it is not revived here |

## Literature adjacency

The collision audit checked primary sources on multi-level pairwise link prediction and related conditional graph message passing, including [MPLP at NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/hash/85970f7bbc821852c1d17052b88c2451-Abstract-Conference.html), [SLRGNN at PMLR](https://proceedings.mlr.press/v251/lachi24a.html), and the conditional message-passing theory paper [at OpenReview](https://openreview.net/pdf?id=7hLlZNrkt5). These sources make the broad ingredients—pairwise scoring, multiple representation levels, and target-conditioned propagation—non-isolated design space. The audit did not find evidence here for an exact isomorphism to CDPT's particular symmetric early/late pair-state contraction, but “no exact match found” is not a novelty proof.

## Updated novelty judgment

The strongest defensible description is:

> A symmetric pair decoder that encodes endpoint-pair states at two message-passing depths and adds a learned bilinear cross-depth score to the DCDLP score.

That description is technically specific but collision-prone. The experiments do not show that the bilinear cross-depth interaction, rather than late-only capacity or a fixed operator, is the causal source of the gain. Therefore the current collision status is **HIGH RISK / UNCONFIRMED NOVELTY**.

No new CDPT V3 structure is proposed. Adding attention, gates, losses, or hidden width without a surviving mechanism finding would increase collision and tuning risk rather than resolve it.

