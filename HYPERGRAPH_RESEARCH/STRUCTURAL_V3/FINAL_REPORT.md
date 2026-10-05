# Hypergraph Structural Innovation Sprint V3 — Final Report

## Final status

**STATUS: EXECUTED**  
**FINAL_DECISION: NO_STRUCTURAL_SIGNAL**  
**WINNING_CANDIDATE: none**  
**BEST_VALIDATION_MRR: 0.487971 (B2 second-moment control).** The best structural candidate was B3 at 0.487705; the matched F1 Raw score was 0.487678.

No candidate met the preregistered GO rule. Consequently, no test-set scores were computed. The best observed candidate-over-Raw change was PMHE B3 at only **+0.000027 MRR (+0.0055%)**; it lost to both of its moment controls.

## Raw hypergraph audit

`_star_members` forms one target-masked closed-neighborhood star per non-isolated center:

`e_c = {c} ∪ N(c)`, with `anchor_id[e] = hyperedge[e][0]`.

The target pair is removed before the message graph, node encoder, and hypergraph branch are built. On Cora standard seed 0, the existing audit records 2,708 nodes, 4,488 undirected message edges, 2,620 nonempty stars, 2,620 anchor incidences, and 8,976 member incidences. All tested modules retained full coverage. See [00_OPERATOR_AUDIT.md](00_OPERATOR_AUDIT.md).

## Experiment contract and integrity

All arms used Cora, standard split, seed 0, uniform training negatives, 20 evaluation negatives per positive, A5, hidden dimension 16, branch dimension 8, two layers, dropout 0, batch size 4096, on the offline V100 in `mei_env`. F0 was one epoch; F1 was five epochs. Each stage reran Raw using the same epoch budget. Validation-best checkpoints were selected from per-epoch validation MRR.

All **24 primary screening runs plus the supplemental C4 diagnostic** share split hash `4ad9a114f501`; all 25 validation-only runs have `test_evaluated=false`. No test metrics exist for this sprint. The validation learning curves and full remote run evidence are archived under each candidate's `remote_evidence/` folder.

## Candidate A — ARHC

| Arm | Definition | F0 best MRR | F1 best MRR |
|---|---|---:|---:|
| A0 | Raw global hypergraph | 0.162793 | **0.487678** |
| A1 | Symmetric parameter-matched branch | 0.164558 | 0.487579 |
| A2 | Anchor/member split, symmetric return | 0.162603 | 0.487406 |
| A3 | Full anchor/member interaction and typed return | 0.164557 | 0.487407 |

F0 passed the early screen. In F1, A3 was **−0.000271 MRR** versus Raw, while A2 was −0.000272; neither qualified for the role-only fallback. A1, the symmetric control, also finished below Raw. A3 did not lead the primary controls, so A4 was skipped. **Decision: REJECT.**

Added parameters: **2,097** (8.48% over the 24,735-parameter Raw model). F1 training runtime: Raw 36.3 s; A3 39.6 s (**+9.1%**, one run each). A3 learned `gamma = −0.00589`.

## Candidate B — PMHE

| Arm | Definition | F0 best MRR | F1 best MRR |
|---|---|---:|---:|
| B0 | Raw global hypergraph | 0.162793 | 0.487678 |
| B1 | Mean control | 0.162642 | 0.487893 |
| B2 | Second-moment control | 0.164497 | **0.487971** |
| B3 | Exact normalized pair moment | 0.164560 | 0.487705 |

F0 passed the early screen. In F1, B3 gained only **+0.000027 MRR (+0.0055%)** over Raw, below both B1 (−0.000188 relative to B1) and B2 (−0.000266 relative to B2), and below the +0.003 / +2% threshold. **Decision: REJECT.** Test remained disabled.

Added parameters: **257** (1.04%). F1 runtime: Raw 33.4 s; B3 35.3 s (**+5.7%**). B3 learned `gamma = 0.00617`.

## Candidate C — ARPM

| Arm | Definition | F0 best MRR | F1 best MRR |
|---|---|---:|---:|
| C0 | Raw global hypergraph | 0.162793 | **0.487678** |
| C1 | PMHE pair-moment control | 0.164560 | 0.487705 |
| C2 | Anchor-conditioned member mean | 0.162636 | 0.487655 |
| C3 | Anchor-conditioned member pair moment | 0.164546 | 0.487629 |
| C4 | Shuffled-anchor ARPM diagnostic | — | 0.487465 |

F0 passed the early screen. In F1, C3 was **−0.000048 MRR** versus Raw and did not exceed C0, C1, or C2. C4 was run as an additional diagnostic because compute was available; C3 exceeded shuffled-anchor C4 by 0.000164, but this does not compensate for losing to the primary controls. **Decision: REJECT.** Test remained disabled.

Added parameters: **1,073** (4.34%). F1 runtime: Raw 36.7 s; C3 39.3 s (**+7.1%**). C3 learned `gamma = −0.00993`.

## Novelty status

**NOVELTY_STATUS: broad operator families conflict with prior work; the exact graph-induced-star variants remain unverified.** Role-aware/typed-incidence hypergraph methods and position-aware knowledge-hypergraph link prediction already exist. Pairwise-aware set/hyperedge encoders are also established. The focused search found no exact match for these specific operators on fixed graph-induced stars, but this is not a novelty guarantee. See [01_NOVELTY_SEARCH.md](01_NOVELTY_SEARCH.md) for the source-by-source comparison.

## Final fields

- **RAW_HYPERGRAPH:** `e_c = {c} ∪ N(c)`; `anchor_id[e] = hyperedge[e][0]`; raw F1 validation MRR 0.487678.
- **A_ARHC:** F0 passed; F1 A3 0.487407 vs Raw 0.487678; A2 fallback failed; REJECT; A4 not run.
- **B_PMHE:** F0 passed; F1 B3 0.487705 vs Raw 0.487678, but B1/B2 were higher and gain threshold failed; REJECT.
- **C_ARPM:** F0 passed; F1 C3 0.487629 vs Raw 0.487678 and all primary controls; C4 shuffled-anchor diagnostic 0.487465; REJECT.
- **WINNING_CANDIDATE:** none.
- **BEST_VALIDATION_MRR:** 0.487971 (B2 control, F1 epoch 5); best Raw was 0.487678 and best structural candidate was B3 at 0.487705.
- **BEST_ATTEMPTED_ABSOLUTE_GAIN:** +0.000027 MRR (B3 vs Raw); **relative gain:** +0.0055%; not a GO.
- **FINAL_DECISION:** NO_STRUCTURAL_SIGNAL.
- **NEXT_EXPECTED_STEP:** move the next research cycle to hypergraph-construction innovation rather than continuing these rejected operator variants. Keep the current Raw operator as the matched structural baseline.
