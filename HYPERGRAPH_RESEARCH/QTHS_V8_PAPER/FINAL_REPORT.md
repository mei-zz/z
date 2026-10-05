# V8 final report

- STATUS: **COMPLETE**
- QTHS: **QTHS25 frozen; alpha=0.25**
- CORA: V7.1 locked reproduction **PASS**; test QTHS25 mean 0.493377 vs Graph-hard 0.472552.
- CITESEER: **CITESEER_NEUTRAL**, paired mean delta -0.000763, 95% bootstrap CI [-0.022228, +0.019841].
- PUBMED: **SUPPORTED**, test paired mean delta +0.040828, wins 3/3.
- BACKBONE_GENERALIZATION: **YES** (3/3 pass).
- SEMI_HARD_CONTROL: **QTHS25_NOT_ABOVE_SH75**, delta -0.059701, wins 1/3.
- TRIM_SENSITIVITY: Spearman(alpha, MRR)=-0.8000; Spearman(mean Rg, MRR)=0.8000.
- EFFICIENCY: QTHS additional trainable parameters **0**; sampling, scoring, wall time and GPU memory recorded.
- NOVELTY_STATUS: **EXACT_RULE_UNVERIFIED**.
- PAPER_EVIDENCE_READY: **YES**.
- FINAL_DECISION: **PAPERIZE_QTHS**.
- NEXT_EXPECTED_STEP: paper outline, tables, figures, related work, and writing

## Additional stability and transfer checks

- Cora 5-seed test: Graph-hard 0.448347 ± 0.122044; QTHS25 0.465782 ± 0.129742; paired delta +0.017435; QTHS wins 4/5; per-seed deltas [-0.0015961419048433623, 0.01377608488996035, 0.050296626042788506, 0.02324222015424926, 0.0014567117460561607].
- Pubmed 5-seed test: Graph-hard 0.791729 ± 0.025822; QTHS25 0.837641 ± 0.012689; paired delta +0.045911; QTHS wins 5/5; per-seed deltas [0.024300746526899064, 0.06709231933224735, 0.03109074160316494, 0.04814764933221616, 0.05892412939473757].
- Citeseer GraphSAGE seed 0 validation transfer: Graph-hard 0.417571, QTHS25 0.472313, delta +0.054743.
