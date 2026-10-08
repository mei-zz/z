import json,re
from pathlib import Path
O=Path(r'E:\我的资料库\Documents\Downloads\DCDLP-main\PAPER_PREP\R_HSPE_DSR_MANUSCRIPT_V2')
p=O/'manuscript.source.md'; src=p.read_text(encoding='utf-8')
src=re.sub(r'title: .*','title: "Dynamic Structural Routing with Hyperedge-Pair Context for Link Prediction"',src,count=1)
src=re.sub(r'subtitle: .*','subtitle: "Working title only; title selection remains open"',src,count=1)
def replace_section(t,a,b,new):
 i=t.index(a);j=t.index(b,i);return t[:i]+new.rstrip()+'\n\n'+t[j:]
abstract=r'''Local structural features are usually combined with fixed rules, even when their usefulness may differ by candidate. We study two related components for pairwise link prediction. R-HSPE encodes a candidate’s incident-hyperedge-pair context with training-derived cardinality ranks and a small residual head. Dynamic Structural Routing (DSR) adds a candidate-conditioned softmax over three structural residual experts: R-HSPE, projected GRAPH statistics, and a path-branch descriptor. Only the residual experts are routed; the NCNC backbone remains unchanged. In the frozen ten-epoch historical protocol, R-HSPE improves NCNC MRR by 0.025853 on Cora and 0.007137 on PubMed, with positive paired differences on all five seeds for each dataset. In the separate validation-only V32 five-epoch protocol, DSR improves PubMed MRR over a fixed equal-weight R/G/P blend by 0.004410 on new seeds 3–7 (4/5 wins). The executed repeated-GRAPH control is a different arm: DSR’s PubMed difference is −0.001378 (2/5), so the fixed-mixture result is not a replicated gain over repeated GRAPH. Cora evidence is weak; Citeseer shows a small transfer signal against NCNC (+0.006629, 2/3). These results support DSR as a provisional integration architecture with dataset-dependent performance, while its mechanism, effective-capacity advantage, and novelty remain unresolved.'''
src=replace_section(src,'# Abstract','# 1 Introduction','# Abstract\n\n'+abstract+'\n\n**Keywords:** pairwise link prediction; hypergraph context; candidate-conditioned decoding; structural mixture; validation controls.')
intro=r'''# 1 Introduction

Link prediction systems often rely on shared-neighbor counts and other fixed local summaries. Such statistics are useful, but compress away how supporting incidence is arranged around a candidate. Separately, predictors commonly combine structural sources with fixed weights even though their usefulness may vary from pair to pair. These two limitations motivate the evaluated method components in this manuscript.

**Problem 1: shared-neighbor counts omit incidence organization.** A support vertex can connect to each endpoint through multiple incident hyperedges. Counting the support once does not encode the multiplicity or size context of those endpoint-side hyperedge pairs. We address this representation gap with R-HSPE, which encodes a candidate-local multiset of incident-hyperedge pairs, calibrates cardinality with a training-only empirical rank, and adds a zero-initialized scalar residual. Raw-star hyperedges are derived from the visible training graph; this is a different structural representation of existing graph information, not an additional observed hypergraph source.

**Problem 2: fixed fusion cannot condition structural contributions on the candidate.** A candidate may have dense projected support, informative path branches, rich R-HSPE tokens, or sparse context. A fixed additive fusion applies the same structural mixture to all pairs. DSR uses a small symmetric state computed from target-masked training-visible structure to produce candidate-specific soft mixture weights over R-HSPE, projected GRAPH, and path-based residuals. The router may assign different weights to different candidates; the results do not establish that any candidate requires a particular source or that the weights are causal explanations.

We separate the frozen ten-epoch historical R-HSPE plug-in evidence from the V32 five-epoch validation-only DSR study. Their checkpoint budgets and purposes differ, so scores are not pooled. Earlier matched evaluations show positive R-HSPE integration with NCN and NCNC on Cora and PubMed. A separate common-protocol factorial did not distinguish the R-HSPE/GRAPH combination from a duplicated-graph control. V32 then tested candidate routing with fixed-mixture, global-mixture, repeated-source, shuffled-context, and zero-context controls. Its corrected arm mapping matters: the independent PubMed +0.00441 result is against fixed equal-weight R/G/P (A4); the actual repeated-GRAPH arm is A7, against which those independent seeds yield −0.00138 MRR (2/5 wins).

We make three contributions:

1. We introduce R-HSPE, a lightweight candidate-specific incident-hyperedge-pair representation using training-relative cardinality ranks, invariant pooling, explicit counts, and residual integration.
2. We introduce DSR, a candidate-adaptive soft-routing architecture over hyperedge-pair, projected-graph, and path-based structural residuals.
3. We report controlled validation, independent-seed, inner-split, transfer, and negative-control evidence that separates measured predictive gains from stronger controls and mechanism claims.

The clearest DSR result is a replicated PubMed MRR improvement over a fixed equal-weight multi-source blend. DSR does not show a replicated PubMed improvement over the executed triple-GRAPH routed control. Its Cora results are small; the Citeseer validation signal is exploratory. We present DSR as a provisional architecture-level integration contribution with dataset-dependent evidence, not as a fully proven routing mechanism, universal method, or state-of-the-art claim.'''
src=replace_section(src,'# 1 Introduction','# 2 Related work',intro)
related=r'''## 2.5 Mixture-of-experts and gated integration

Softmax gating over expert outputs is an established mixture-of-experts design. Early work trained separate expert networks and input-dependent mixture coefficients; later formulations made both gating and experts explicit components of a probabilistic architecture [@jacobs1991; @jordan1994]. DSR does not claim the general gating operation, softmax mixture, or expert abstraction as novel. It applies this established pattern to three specified structural residuals using a compact candidate state and evaluates it with fixed-mixture, global-gate, repeated-GRAPH, shuffled-context, and zero-context controls. Predictive differences do not alone establish that candidate-conditioned routing caused the gain.'''
src=src.replace('# 3 Preliminaries and evaluation setting',related+'\n\n# 3 Preliminaries and evaluation setting',1)
method=r'''## 4.7 Dynamic Structural Routing

DSR augments the NCNC host with three candidate-specific residual experts. The host score is retained unchanged; only the structural residuals are mixed. In V32, each expert has 75 declared parameters and the router has 83, for 308 added parameters in A6.

### 4.7.1 Structural experts

Let $\Delta_R(u,v)$ be the unchanged R-HSPE residual from Sections 4.1–4.5. The GRAPH branch uses two candidate-masked features from the unweighted two-section $P$: $\mathbf g(u,v)=[\log(1+CN_P(u,v)), CN_P(u,v)/\max(\min(d_u^P,d_v^P),1)]$, where $CN_P$ is the shared-neighbor count in the raw-star projection and $d_u^P,d_v^P$ are endpoint degrees in that same target-masked projection. A learned 75-parameter adapter maps this vector to $\Delta_G(u,v)$.

The path expert uses the fixed V30B path-branch dispersion (PBD) descriptor. On the candidate-masked training-visible graph, enumerate every valid simple three-hop path $u\to a\to b\to v$ with all four vertices distinct. Let $c_u[a]$ count paths by first branch and $c_v[b]$ count them by last branch. Define $P_3=\sum_a c_u[a]=\sum_b c_v[b]$, $D_u=P_3^2/\sum_a c_u[a]^2$, and $D_v=P_3^2/\sum_b c_v[b]^2$, with both zero when $P_3=0$. The symmetric feature is $\mathbf p(u,v)=[\log(1+(D_u+D_v)/2),\log(1+|D_u-D_v|)]$. A 75-parameter adapter maps it to $\Delta_P(u,v)$. The effective branch count is an inverse-Simpson/Hill order-2 quantity, an established concentration/diversity statistic [@hill1973]; we do not claim that statistic alone as a new algorithm.

For G and P, the two standardized scalar inputs populate the first two positions of a six-dimensional zero vector. A shared 6-to-8 affine/ReLU encoder supplies the same embedding to mean and max positions; two count positions are zero and an 18-to-1 residual head completes the 75-parameter slot. The R expert uses frozen R-HSPE token encoding and pooling.

### 4.7.2 Candidate structural state

For each pair construct the symmetric six-coordinate state
$$\mathbf c_{uv}=[\log(1+T_{uv}),\log(1+S_{uv}),\log(1+P_3),\log(1+P_4),\log(1+d_u+d_v),\log(1+|d_u-d_v|)]\in\mathbb R^6,\qquad (12)$$
where $T_{uv}$ and $S_{uv}$ are R-HSPE token/support counts, $P_3$ and $P_4$ are exact static three- and four-hop path counts, and $d_u,d_v$ are degrees in the candidate-masked training-visible graph. A training-positive target edge is removed before these candidate features are computed. Validation candidates use only the visible training graph. Each coordinate is standardized using that seed’s actual training-candidate occurrence schedule; validation labels are not router inputs.

### 4.7.3 Candidate-adaptive router

The router $g_\phi$ is a two-layer MLP, $6\to8\to3$, with ReLU then softmax. It has $(6\cdot8+8)+(8\cdot3+3)=83$ parameters. For candidate $(u,v)$,
$$\boldsymbol\alpha_{uv}=\operatorname{softmax}(g_\phi(\mathbf c_{uv})),\quad \alpha_R+\alpha_G+\alpha_P=1,\qquad (13)$$
so the output is a continuous mixture, not a discrete expert choice.

### 4.7.4 Routed residual score

The final logit is
$$s(u,v)=s_{\mathrm{NCNC}}(u,v)+\alpha_R(u,v)\Delta_R(u,v)+\alpha_G(u,v)\Delta_G(u,v)+\alpha_P(u,v)\Delta_P(u,v).\qquad (14)$$
The NCNC backbone is not routed, gated, or replaced. All three expert outputs are combined by their candidate-specific softmax weights.

### 4.7.5 Initialization, symmetry, and masking

The final router layer is zero-initialized, giving initial weights $(1/3,1/3,1/3)$. Each expert residual head is zero-initialized. The V32 audit confirms that the initial complete score equals NCNC exactly. All router features are endpoint-symmetric and target-masked; the router and complete score passed endpoint-swap checks. Normalization uses training occurrences only. The frozen R-HSPE definition and historical results are unchanged.

### 4.7.6 Parameter count and computation

A6 adds 225 expert parameters and 83 router parameters (308 total). Comparison arms A4–A10 also carry 308 *declared* parameters, but A4 has an 83-parameter disconnected pad and A5 has 80 disconnected pad parameters in addition to three global logits. Their nominal parameter counts are not effective-capacity matches. The GRAPH branch computes candidate-local projected common-neighbor features. PBD enumerates valid simple three-hop paths; uncached work scales with the number of enumerated paths. V32 caches candidate features for training. The final evidence bundle does not isolate path-cache construction time or per-candidate inference latency. Job-level runtime and peak GPU memory appear in Table S8.'''
src=src.replace('# 5 Experimental setup',method+'\n\n# 5 Experimental setup',1)
protocol=r'''## 5.5 V32 DSR validation protocol and controls

V32 used a common five-epoch, final-checkpoint validation protocol on Cora and PubMed. Phase A used paired seeds 0–2 for A0–A10. Phase B used new seeds 3–7 on A4, A5, A6, A7, A9, and the strongest selected single expert for each dataset (A1 for Cora, A3 for PubMed). It reused the same validation candidates, so Phase B changes initialization and training randomness rather than the graph or validation population. Citeseer transfer used seeds 0–2 on A0, A1, A2, A4, A6, A7. One PubMed inner validation split derived from original training positives used seeds 0–2 on A4, A6, A7, A9. Every checkpoint is the final epoch; no best-validation checkpoint was selected.

A0 is NCNC; A1–A3 add one R, GRAPH, or PBD expert. A4 is an equal 1/3 R/G/P blend; A5 learns three global mixture logits; A6 is the candidate router; A7 routes among three independently initialized GRAPH experts; A8 routes among three R-HSPE experts; A9 uses a stratified candidate-context correspondence shuffle; A10 receives a zero router state. A4/A5 are nominally parameter-matched with disconnected pads; their pads received no gradients, so the match is not effective-capacity equality.

Validation MRR is primary. CE, Hits@10, Hits@20, and AUC are secondary. Paired differences are recomputed within seeds; “wins” count positive MRR differences. These are descriptive small-sample estimates, not significance tests. All V32 phases are validation-only; no test graph, labels, or candidates were opened. Full per-seed results are retained in `audit_sources/DSR_V32/` and `tables/dsr_per_seed_contrasts.csv`.'''
src=src.replace('## 5.4 Metrics, uncertainty, and reproducibility',protocol+'\n\n## 5.4 Metrics, uncertainty, and reproducibility',1)

# Load paired main table and result JSON for appendix.
main=(O/'tables/table7_dsr_primary.md').read_text(encoding='utf-8')
# Use the source-generated table and keep its definition note intact.
results=r'''## 6.7 Dynamic Structural Routing (V32)

Table 7 separates the fixed equal-weight mixture (A4), global mixture (A5), true repeated-GRAPH routed control (A7), and context-shuffle control (A9). Phase B uses new seeds 3–7 but reuses the Phase A validation populations. This arm mapping changes the headline interpretation: PubMed A6 exceeds A4 by +0.004410 MRR on 4/5 seeds but is below A7 by −0.001378 MRR on 2/5. Thus +0.00441 is a replicated gain over fixed equal-weight fusion, not over repeated GRAPH.

On Cora, Phase B differences are +0.000463 (2/5) against A4 and +0.001905 (3/5) against A7; this is small and mixed evidence. Against the global mixture A5, PubMed Phase B gives +0.004413 (4/5), but A5’s nominal parameter count includes 80 disconnected parameters. A6 exceeds shuffled-context A9 on PubMed by +0.001186 (5/5), while Cora is essentially tied (+0.000005, 3/5). These controls add context but do not prove causality.

'''+main+ r'''

The PubMed inner split yields A6−A4 +0.001324 (2/3), A6−A7 +0.001616 (3/3), and A6−A9 +0.000315 (2/3). This single train-derived split is exploratory. Citeseer validation transfer gives A6−NCNC +0.006629 MRR (SD 0.015091; 2/3), with per-seed differences −0.010675, +0.017063, and +0.013497. In V32, A6 is +0.027821 MRR above R-only A1, while A1 is −0.021192 below NCNC on average. Relative to the earlier V17.4 negative Citeseer result (−0.027379, 0/3 under a different protocol), V32 may partially mitigate the observed pattern; it does not solve Citeseer transfer or establish stable transfer.

A6 router collapse was false on Cora and PubMed. Router weights vary across R-token and P3 subgroups, with a stronger R allocation in positive-context groups on PubMed. These retrospective strata describe routing behavior; they do not identify causal expert specialization. Table S7 reports their means and quantiles. The A9 shuffle changed 77.40% of Cora and 71.70% of PubMed validation context rows; this describes how often features changed, not causal-control power by itself.

The corrected V32 evidence supports a provisional PubMed predictive signal against fixed equal-weight fusion. The positive contrast does not reproduce against the executed triple-GRAPH routed control, leaving the routing mechanism exploratory. Nominal parameter equality also leaves effective-capacity and optimization explanations open.'''
src=src.replace('# 7 Discussion and limitations',results+'\n\n# 7 Discussion and limitations',1)
# Rewrite discussion and conclusion sections.
disc=r'''## 7.1 What the evidence supports

The strongest historical R-HSPE evidence is a matched ten-epoch plug-in improvement over NCN and NCNC on Cora and PubMed, with positive paired differences across five seeds per dataset. This supports a useful structural residual under the stated V17.4 protocol. It does not isolate cardinality ranks as the cause, and standalone count/constant-set controls remain competitive.

DSR adds an adaptive integration architecture over R-HSPE, GRAPH, and path residuals. Its clearest independent-seed result is a PubMed MRR gain over the fixed equal-weight R/G/P control. The executed A7 repeated-GRAPH comparison differs: +0.001726 in Phase A (2/3) but −0.001378 in Phase B (2/5). The +0.004410 result is therefore not described as repeated-GRAPH replication. DSR is performance-supported against fixed fusion; superiority over active duplicated GRAPH and the mechanism remain exploratory.

The router is noncollapsed and assigns context-dependent weights, but those weights are not causal explanations. A4/A5 nominal capacity includes disconnected parameters, and candidate routing changes the function class as well as its inputs. Effective-capacity and optimization explanations remain open.'''
src=replace_section(src,'## 7.1 What the evidence supports','## 7.2 Transfer and structural information',disc)
src=src.replace('The theory example separates a selected incidence context from a particular lossy unweighted projection.','DSR gives a small positive Citeseer validation difference over NCNC on 2/3 seeds, but mixed outcomes and the earlier protocol-specific adverse result preclude a stable transfer claim. This is a preliminary signal, not evidence that routing solves negative transfer.\n\nThe theory example separates a selected incidence context from a particular lossy unweighted projection.',1)
src=src.replace('Repeated use of the same validation population for many candidate designs introduces selection bias.','V32 seeds 3–7 use the same validation candidates as Phase A. They assess new initializations and training paths, not a fresh graph. The inner split is derived from training positives and covers one dataset/split.\n\nRepeated use of the same validation population for many candidate designs introduces selection bias.',1)
src=src.replace('Candidate-conditioned structure, cardinality normalization, invariant pooling, and residual decoding each have substantial prior precedent.','Mixture-of-experts and softmax gating are established methods [@jacobs1991; @jordan1994]; candidate-conditioned structure, cardinality normalization, invariant pooling, and residual decoding also have substantial precedent. PBD’s effective branch count is the inverse-Simpson/Hill order-2 statistic [@hill1973], not a new diversity measure.',1)
status=r'''## 7.5 Manuscript contribution status

**Innovation 1 — R-HSPE: FROZEN.** Implementation, historical results, and claim boundary were not changed by V32 or this manuscript update.

**Innovation 2 — DSR: PROVISIONAL / PERFORMANCE-SUPPORTED.** The PubMed gain over fixed equal-weight fusion reproduces on seeds 3–7; the actual repeated-GRAPH contrast does not.

**Mechanism 2: PARTIALLY RESOLVED / EXPLORATORY.** Router diagnostics show noncollapsed, context-varying behavior, but capacity, duplicated-source, validation reuse, and function-class concerns remain.

**Innovation 3: NOT YET DEFINED.** It is outside the current contribution list.'''
src=src.replace('# 8 Conclusion',status+'\n\n# 8 Conclusion',1)
conclusion=r'''# 8 Conclusion

This manuscript presents two related components for pairwise link prediction. R-HSPE is a frozen candidate-local incident-hyperedge-pair residual whose historical ten-epoch NCN/NCNC plug-in results improve MRR on Cora and PubMed under the matched V17.4 protocol. DSR adds a candidate-conditioned softmax mixture over R-HSPE, projected GRAPH, and PBD residuals while leaving NCNC unchanged. V32 supports an independent PubMed MRR gain over a fixed equal-weight blend, but the gain does not reproduce against the executed repeated-GRAPH routed control. Cora evidence is weak, Citeseer transfer is a small validation signal, and router weights are not causal explanations. We present DSR as a provisional integration contribution with dataset-dependent evidence, not a fully validated mechanism or a novelty claim inferred from performance. R-HSPE remains frozen; Innovation 3 is future work and is not included in the contributions.'''
src=replace_section(src,'# 8 Conclusion','# Appendix A Supplementary evidence',conclusion)

# Full DSR metrics and router diagnostics in supplementary material.
A=json.loads((O/'DSR_NUMERICAL_AUDIT.json').read_text(encoding='utf-8')); phases=A['phases']; MET=['ce','mrr','hits10','hits20','auc']
supp='## A.7 DSR full validation metrics\n\nTable S6 lists CE, MRR, Hits@10, Hits@20, and AUC means and sample SDs for all completed V32 arms/phases. Exact per-seed scores and paired contrasts are retained in the accompanying CSV files.\n\n'
for phase,label in [('phase_a','Phase A: Cora/PubMed, seeds 0–2'),('phase_b','Phase B: Cora/PubMed, seeds 3–7'),('citeseer_transfer','Citeseer transfer, seeds 0–2'),('inner_validation','PubMed inner validation, seeds 0–2')]:
 supp+=f'**Table S6 ({label}). Mean ± sample SD.**\n\n| Dataset | Arm | CE | MRR | Hits@10 | Hits@20 | AUC |\n|---|---|---:|---:|---:|---:|---:|\n'
 for ds,d in phases[phase].items():
  for arm,m in d['metrics_mean_sd'].items(): supp+=f"| {ds.capitalize()} | {arm} | "+' | '.join(f"{m[k]['mean']:.6f} ± {m[k]['std']:.6f}" for k in MET)+' |\n'
 supp+='\n'
supp+='## A.8 Router behavior diagnostics\n\n'+(O/'tables/tableS7_router_weights.md').read_text(encoding='utf-8')+'\n'
src=src.replace('# References',supp+'\n# References',1)
p.write_text(src,encoding='utf-8')

bib=O/'references.bib'; b=bib.read_text(encoding='utf-8')
if 'jacobs1991' not in b: b+='''\n@article{jacobs1991,\n author={Robert A. Jacobs and Michael I. Jordan and Steven J. Nowlan and Geoffrey E. Hinton},\n title={Adaptive Mixtures of Local Experts},\n journal={Neural Computation}, year={1991}, volume={3}, number={1}, pages={79--87},\n doi={10.1162/neco.1991.3.1.79}, url={https://doi.org/10.1162/neco.1991.3.1.79}\n}\n@article{jordan1994,\n author={Michael I. Jordan and Robert A. Jacobs},\n title={Hierarchical Mixtures of Experts and the {EM} Algorithm},\n journal={Neural Computation}, year={1994}, volume={6}, number={2}, pages={181--214},\n doi={10.1162/neco.1994.6.2.181}, url={https://doi.org/10.1162/neco.1994.6.2.181}\n}\n@article{hill1973,\n author={M. O. Hill}, title={Diversity and Evenness: A Unifying Notation and Its Consequences},\n journal={Ecology}, year={1973}, volume={54}, number={2}, pages={427--432},\n doi={10.2307/1934352}, url={https://doi.org/10.2307/1934352}\n}\n'''
bib.write_text(b,encoding='utf-8')
print('Manuscript source updated:',p)


