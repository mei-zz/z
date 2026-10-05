# DCDLP V5 — History and Blacklist Audit

Date: 2026-09-17  
Scope: `AUTONOMOUS_LP_RESEARCH`, `AUTONOMOUS_MODEL_INNOVATION_V2`, `V3`, `V4`, and the current DCDLP source tree.  
Protection: no V1–V4 file, checkpoint, result, or source file was modified.

## Audit status and version boundary

The current directory is not a Git working tree:

```text
git status --short: fatal: not a git repository
git rev-parse --short HEAD: fatal: not a git repository
```

Therefore V5 records a filesystem/source-hash boundary rather than inventing a commit ID.  V4 JSON manifests contain the source hash used by the formal runs; the most relevant values are retained below.

| Artifact | SHA-256 / recorded hash | Role |
|---|---|---|
| `src/dcdlp/models/dcdlp.py` | `C1BBF8A86A798FE088D13E61D38053E8DC23D8ADFB4443DEA5C56EF3F5FEBBA3` | Parent/CDPT source used by V3/V4 manifests |
| `src/dcdlp/models/node_encoder.py` | `EADA0A085994145AED9DAFA78AEB98215C027E329A931DDCCDEB8178C2272FA1` | target-edge mask implementation |
| `src/dcdlp/train.py` | `DF889AB13B374AE5AED517346F3F2DF8A97B5DB633854AD2F32C4CDCF0CDB1F4` | training/evaluation protocol |
| `AUTONOMOUS_MODEL_INNOVATION_V4/scripts/v4_runner.py` | `DF08127D16747325B506CACC092BF4F5F4BC82477CB4F4C7BDB1793B5A35FCA7` | V4 formal runner |
| `AUTONOMOUS_MODEL_INNOVATION_V4/scripts/v4_models.py` | `A203C41DBE31C727D0183544F7B27C09D0EF50A049743F0AC4D998CB46D81588` | V4 A–E model definitions |
| `AUTONOMOUS_MODEL_INNOVATION_V4/scripts/aggregate_v4.py` | `3590E671083E8A41FA67C53B05DA3EC30A79828231D527F130282D9001530CA9` | V4 aggregation |
| Cora HeaRT | `98e4aaaf07d4` in V4 manifests | formal Cora data/candidate boundary |
| historical CiteSeer HeaRT | `93b2480b3b56` in V4 manifests | extension only; already used in V3 |

## Deduplicated history

“Executed” means that raw JSON/checkpoints/logs or a reproducible result artifact exists. “Literature-only” means no model run is treated as evidence. “Incomplete” means a report exists but the paired/raw evidence is missing or the protocol is invalid.

| Candidate / family | Core object | Literature / collision state | Actual stage and result | Failure or exclusion boundary | Evidence |
|---|---|---|---|---|---|
| PRIOR-001 DCDLP Degree/CN disentanglement | degree, CN, residual branches and interventions | audited prior route | Executed; STOP | no causal/mechanistic gain | `AUTONOMOUS_LP_RESEARCH/IDEA_LEDGER.md`, `BLACKLIST.md` |
| PRIOR-002 MPLP-VC | pair-level estimator variance/confidence | adjacent to MPLP; not a new mechanism | Executed; STOP | variance not better than shuffled; degree-correlated and unstable | same V1 ledger |
| PRIOR-003 NCN-CNDP | CN variance/second moment | NCN/NCNC family | Executed, 24 runs; STOP | only 3/6 seed wins; no stable gain | same V1 ledger |
| PRIOR-004 HL-GNN-PDG | pair-dependent hop gate | adjacent to HL-GNN | Executed; STOP | gate collapsed; peak memory increased about 37.6% | same V1 ledger |
| PRIOR-005 CECG / L3 | exclusive-neighborhood witness interaction | graphlet/CH2-L3/CH3-L3 collision family | Executed; STOP | controlled P4 < P3 on five Cora seeds | same V1 ledger |
| R1-03 disjoint paths | internally vertex-disjoint short-path capacity | path/separator collision family | Stage0/1/2 executed; STOP | locked ranking below Parent/Proxy; AP below shuffled | `EXHAUSTIVE_SEARCH_ROUND.md` |
| R1-07 role transition | degree-shell role transitions on short paths | path/graphlet collision risk | Stage0/1/2 executed; STOP | integration below Parent and shuffled | same |
| R2-01 block-cut route | biconnected block/articulation route | block-cut/bridge family | Stage0/1/2 executed; STOP | small AUC signal did not transfer to ranking; Proxy won | same |
| R3-01 non-backtracking | legal non-backtracking continuation profile | Hashimoto/line-graph collision risk | Stage0/1/2 executed; STOP | below Parent and shuffled on locked ranking | same |
| R4-01 boundary matching | maximum matching/Hall deficit | matching/cover family | Stage0/1 executed; STOP | AUC increment contradicted by AP | same |
| R4-03 boundary expansion | two-sided frontier growth/overlap | neighborhood-expansion family | Stage0/1/2 executed; STOP | mixed aggregate ranking; lost key Parent/Proxy metrics | same |
| R4-07 neighbor alignment | endpoint-neighbor role alignment | role/homophily family | Stage0/1 executed; STOP | below dangerous controls, shuffled, and Proxy | same |
| R4-08 spectral band | fixed Laplacian spectral bands | spectral/diffusion family | Stage0/1 executed; STOP | True AUC below scalar Proxy | same |
| R4-12 cohesion | exclusive-neighborhood density/contrast | clustering/cohesion family | Stage0/1/2 executed; STOP | lost Proxy on every aggregate ranking metric | same |
| R4-13 community boundary | community mass/boundary profile | community-aware LP family | Stage0/1/2 executed; STOP | below Parent on all aggregate metrics | same |
| V2-001 PCDT | pair token generates local neighborhood transport | high risk: conditional message passing, NBFNet, target matching | Stage1 executed; Stage2 control executed; STOP | shuffled evaluation beat aligned PCDT, so intended alignment was not causal | `AUTONOMOUS_MODEL_INNOVATION_V2/FAILURE_ANALYSIS.md`, `CANDIDATE_LEDGER.md` |
| V2-002 / V3 / V4 CDPT | early/late pair states with learned tensor contraction | V2 bounded audit only; no global novelty certificate | V2 3-seed screen positive; V3/V4 mechanism audit completed; final STOP | V4 Cora: CDPT lost Early×Early 0/5, was tied with Late×Late, and lost to fixed random on average | `AUTONOMOUS_MODEL_INNOVATION_V4/CDPT_FINAL_DECISION.md`, `MECHANISM_COMPARISON.md` |
| T2WL-INC | `(i,k),(k,j) -> (i,j)` sparse pair incidence propagation | V4 Stage-0 HOLD; V5 source/formula/code audit finds direct 2-FWL/Local 2-FWL collision | No experiment authorized | `NOVELTY_COLLISION_STOP`; see V5 collision audit | `AUTONOMOUS_MODEL_INNOVATION_V4/NEXT_INNOVATION_SEARCH.md`, V5 document 02 |

The V1 exhaustive search explicitly reached `NO_EXECUTABLE_IDEA_AFTER_EXHAUSTIVE_SEARCH` for the static undirected Cora HeaRT environment. V5 does not reinterpret any feature-only positive probe as a surviving structure.

## Early A5, A14, and A14-w010 audit

The early records are not silently promoted to a new candidate:

1. `IMPLEMENTATION_AUDIT.md` identifies the project as untracked and describes A5/A14 as an old mechanism-audit framework, not a new validated architecture.
2. `results/phase2/PHASE2_IMPLEMENTATION_REPORT.md` contains a historical summary claiming six A5/A14-w010 paired runs and the exploratory decision `A14_MECHANISM_NOT_SUPPORTED`. It reports a small mean MRR difference, no stable routing-selectivity gain, lower target response, much higher runtime, and 402 explicit missing intervention cases. It also states that A14-w010 weights were chosen after inspecting test MRR and that the old evaluation path used uniform candidates despite a `heart` label.
3. The currently present `results/mechanism_audit/summary.json`, `paired_runs.csv`, and `MECHANISM_AUDIT_REPORT.md` explicitly report `INCOMPLETE_MISSING`, `available_pair_count=0`, and six missing pairs. Consequently the historical summary is retained as an implementation/diagnostic record, but its claimed six-pair metrics are not used as confirmatory evidence in V5.
4. The phase-2 YAML files show A5 `raw`, `raw_plus_residual`, and `disabled interaction` configurations, but no new architecture was trained by V5. These are configuration variants, not a surviving innovation.

This distinction prevents an early exploratory A14 selection, a missing raw-pair audit, or an invalid candidate protocol from being rewritten as stable model evidence.

## Permanent no-retry boundaries

The following families are closed for this search:

- degree/CN/residual disentanglement, conditional-CN residuals, MPLP-VC, NCN-CNDP, and extra CN moments;
- soft gates, hop mixtures, attention, auxiliary losses, width/depth/optimizer rescue, and simple concatenation of existing branches;
- CECG/L3, common-neighbor witness interaction, cycle closure, local path counts, non-backtracking/line-graph rewrites, disjoint-path capacity, block-cut/separator/bridge objects;
- boundary matching, boundary expansion, endpoint-role alignment, homophily/cohesion, community-boundary profiles, and fixed spectral/diffusion bands;
- PCDT and the generic pair-conditioned transport family;
- CDPT and any renamed cross-depth tensor/late decoder that does not add a demonstrably different information object;
- T2WL-INC’s local pair incidence update, because it is structurally covered by published 2-FWL/Local 2-FWL rather than being a new route.

## V4 mechanism evidence carried forward

The formal V4 Cora batch used the same masked encoder, candidates, four-epoch budget, optimizer, and validation-only checkpoint selection for A–E. Validation MRR means were A `0.109457`, B `0.103374`, C/CDPT `0.103837`, D `0.098977`, E/fixed random `0.105747`. Paired C−A was `−0.005620` with 0/5 wins; C−B was `+0.000463` with a confidence interval crossing zero; C−E was `−0.001909` with 2/5 wins. CiteSeer was already used in V3 and is not an independent test. These are direct reasons not to spend V5 compute on CDPT rescue.

