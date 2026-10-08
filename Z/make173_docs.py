import os,json,shutil,hashlib,zipfile
from pathlib import Path
root=Path(r'E:\我的资料库\Documents\Downloads\DCDLP-main\HYPERGRAPH_RESEARCH\R_HSPE_BENCHMARK_V17_3')
root.mkdir(parents=True,exist_ok=True)
docs={
'00_PROTOCOL.md':'''# V17.3 frozen benchmark protocol

R-HSPE is frozen; no model, sampler, optimizer, epochs, splits, candidate set, or evaluator changes. Frozen reports and exact checkpoints are reused without checkpoint selection or test rescoring. Source/config/data/candidate SHA256 hashes are asserted by FROZEN_AUDIT.json before jobs run and again during aggregation.

Datasets: exact V17.2 Cora, PubMed, Citeseer. Fixed train/valid/test split (not each baseline's original randomly re-split dataset). Train edges alone form all message graphs, NSLR incidence and negative exclusions. NCN/NCNC use the original undirected train relation, identical to B0 graph side, without clique expansion. Raw-HG in this project is raw-star construction from that same train relation; NSLR retains its own official NSLR hypergraph construction from the train relation rather than substituting R-HSPE incidence.

Test: existing V17.2 positive and grouped negative NPZ files, exactly 20 negatives per query, original frozen ranking_metrics. Historical evaluation candidate generation excluded all known positives, including heldout, strictly as evaluation construction. These labels are never used by baseline training filters. Frozen validation candidates are reused and their hashes checked.

Primary MRR, secondary Hits@10, Hits@20, mean positive rank. Scores are unrounded decoder logits. Official downstream scorer retained. Mean and sample standard deviation (ddof=1), individual seeds, ranks within tested methods. Official baseline training negatives may differ from QTHS25, but use train-visible information only and are disclosed.

5 seeds (0..4) for NCN, NCNC, NSLR-HMANN on each dataset. Frozen R-HSPE and B0 Cora/PubMed have 5 seeds; Citeseer has only 3, explicitly marked. No R-HSPE rerun to fill this seed-count difference. Validation-only smoke uses seed99 and never tests; smoke checkpoints are excluded from main results.

NCN/NCNC: author's dataset-specific README configs, 100 epochs, validation MRR selects first maximum, test scores only after selection. NSLR-HMANN: official dimensions/loss/Adam(.01)/5000 epochs/final checkpoint; validation logged every25 epochs diagnostically, never test selection. No hyperparameter search. Configs fixed before third-party test access. Official source hashes and compatibility changes in implementation audit. Training budgets differ because each official recommended config is retained; this is accuracy comparison under common information/evaluation, not equal-compute training comparison.

Resources: two GPU processes for smaller jobs; PubMed dense NSLR alone on GPU; one CPU dense-preparation process at a time with16 BLAS threads, GPU workers4 CPU threads each. PubMed NCN/NCNC completion scoring batch512 is a memory-only evaluation adapter; full neighborhoods, same model computation. NSLR matrices/cache are prepared once per dataset and reused across seeds. No automatic architecture changes following OOM or poor metrics. Failures remain recorded, benchmark marked PARTIAL.

Before baseline tests, fix descriptive competitiveness criterion: STRONG iff R-HSPE best/second in >=2 datasets and <=.02 absolute MRR below strongest on remaining dataset. ACCEPTABLE iff within.02 of strongest in >=2 datasets and total parameters below both NCN and NCNC wherever measured. Otherwise WEAK after all planned jobs terminate. .02 is a transparent operational interpretation of 'material lag/strong baseline range', not a significance threshold or universal publication rule. PENDING until jobs terminate. Failed jobs make coverage PARTIAL and paper readiness NO. Labels can be reconsidered by researcher using full evidence, without changing frozen method. No automatic SOTA claim.

Effect sizes vs highest comparable mean MRR: shared seed-label differences, mean/median/wins. Same seed numbers do not create matched RNG semantics between architectures; no strict paired significance tests or significance fishing. Optional query bootstrap omitted.

Server operates offline: sources/wheel fetched locally, pinned/uploaded, pip --no-index --no-deps --target local isolated .deps. Existing server environment is unchanged. User explicitly authorized authentication-only reading of configuration, with credentials never displayed; this overrides document prohibition solely for SSH login.
''',
'01_BASELINE_SELECTION.md':'''# Baseline selection

| Tier | Method | Decision | Evidence / condition |
|---|---|---|---|
| A | NSLR-HMANN | RUN 5 seeds x 3 datasets | Author [repository](https://github.com/pinglanchu/NSLR-HMANN), DOI [10.1016/j.patcog.2024.110292](https://doi.org/10.1016/j.patcog.2024.110292); canonical MLP pair decoder |
| A | HMNE | REFERENCE_ONLY / NO_VERIFIED_IMPLEMENTATION | [Publisher](https://link.springer.com/article/10.1007/s10115-024-02255-8); preview lacks released runnable pipeline; focused exact-title/acronym GitHub search did not verify author implementation. This is not proof none exists. Do not confuse the unrelated 2021 multiplex HMNE acronym. |
| A | HMRLH | REFERENCE_ONLY / NO_VERIFIED_IMPLEMENTATION | [Publisher](https://www.mdpi.com/2079-9292/12/23/4842); focused paper/title+GitHub search did not verify runnable author pipeline and scorer. No invented neural decoder. |
| A | CCLPH | REFERENCE_ONLY / IMPLEMENTATION_NOT_VERIFIED | [Publisher full text](https://www.nature.com/articles/s41598-026-45116-w) downloaded locally and inspected. Paper supports size2 pairwise candidates, so not categorically TASK_MISMATCH. Complete community construction, six scoring variants, candidate admission and aggregation require faithful implementation. No linked GitHub/code-availability release verified in fetched HTML; replacing community detection with graph Louvain or dropping community filtering would change core method. No fake substitute run. |
| B | NCN | RUN 5 seeds x 3 datasets | [Official repository](https://github.com/GraphPKU/NeuralCommonNeighbor), predictor cn1, exact dataset README config |
| B | NCNC | RUN 5 seeds x 3 datasets | Same official repository, predictor incn1cn1, depth1, exact dataset README config |
| Existing | Frozen B0 | REUSE only after hash audit | Exact V17.2 candidates, evaluator, checkpoints |
| Existing | C1_COUNT_PARAM_MATCHED / C2_CONSTANT_SET | REUSE where already tested | Cora C1 / PubMed C2; selected previously by validation, not this benchmark's test; separate arm rows with missing cells, not one method invented across datasets |
| C | OFSH/OHAA, HP2PH, Hyperedge Copy Model, HNHN, HGNN, HYPER, Hypergraph Motif Representation Learning | RELATED_WORK_ONLY | Frozen novelty matrix governs task distinctions; no unverified canonical ordinary-pair scorer or forced adapter inserted into main quantitative table |

The fair benchmark is complete for the three verified runnable third-party baselines only when every planned seed completes. Literature coverage includes additional reference-only methods, whose quantitative absence is explicit; it is not an exhaustive SOTA benchmark.
''',
'02_IMPLEMENTATION_AUDIT.md':'''# Implementation fidelity audit

Pinned official sources: NSLR-HMANN commit7847dee275ca01e383dc33403da95ff455896813; NCN/NCNC commit11d597013750da17ce7468e344bec756a7af39a4. Repository files remain unedited. File SHA256 in SOURCE_MANIFEST.json. URLs in *_source.json. Changes occur only in benchmark loader/evaluation/device wrappers.

NCN/NCNC model.py/utils.py imported directly. Official train()/set_seed() AST nodes executed unchanged from NeighborOverlap.py, including target batch masking, official negative_sampling, sum of positive and negative log-sigmoid losses. Original split loader replaced by frozen train/valid/test wrapper. Sparse graph excludes validation/test edges at every stage. Full official README Cora/Citeseer/Pubmed hyperparameters preserved (hidden256, MPNN1, predictor3,100epochs; separate encoder/predictor rates and dataset-specific dropout). Dataset features exactly frozen view, no external resplit or preprocessing. Python random seeded as reproducibility wrapper for PyG sampler. NCNC splitsize131072 and evaluation batch512 bound operation memory without changing neighborhood set/architecture. Smaller evaluation batch vs README has no training effect.

NSLR-HMANN official construct_hypergraph() and attention classes imported unchanged. Official MLPPredictor and compute_loss AST extracted without running author's top-level eight-dataset training or importing missing, unused SAGE/GAT/HGNN files. NetworkX deprecated from_numpy_matrix name aliased to equivalent from_numpy_array API. Self-loop train adjacency, alpha1, threshold.25, nonbinary incidence and weighted hypergraph projection preserved. Random64-dimensional fixed feature embedding remains outside optimizer, matching official release. Model64->32, heads8/2, output32, dropout.5; official concatenation MLP scorer32; Adam lr.01; BCE loss executed exactly including CPU logits copy;5000epochs/final checkpoint. CUDA device replaces official CPU device to accelerate identical algorithm. Dense construction is float64 NumPy as original; H cast float32 as original. Train-only fixed uniform off-diagonal complement sampler matches author's with-replacement sampling without allocating full complement; 1:1 directed training edges; selfloops added to positive and negative label graphs as official code. No test loop per epoch; validation diagnostics only. No architecture/loss fixes for observed quirks (ignored F.dropout result retained).

DGL1.1.3+cu121 cp311 manylinux wheel downloaded from official data.dgl.ai; SHA25607e2a27f7d30c6c0f5a04384390298977207f6df0ff832ce09fa644f893af0fa. Installed offline in benchmark .deps only; PyTorch2.8.0+cu128 and existing torch_sparse/torch_scatter/PyG/OGB retained. Dataset/model/decoder/evaluator adapters are independently separated in script. Raw per-query scores saved for post-run audit.

Costs: measured train optimizer-step time, total wall, test inference, peak allocated GPU and parameter totals. NSLR CPU construction measured separately in nslr_cache metadata. Frozen baseline train timings reused where recorded; feature-construction costs remain parent artifact references and are not mislabeled zero. Total parameter counts (not just R-HSPE's75 increment) compared. Existing reports' peak training/inference measurements are both retained.
''',
'06_PAPER_REPORTED_RESULTS.md':'''# Paper-reported scores — REFERENCE_ONLY / NOT_DIRECTLY_COMPARABLE

These entries never enter MRR rankings or the main fair quantitative table. Unknown original fields are explicitly NOT_VERIFIED. No comparison of original AUROC/AUPR against frozen MRR.

| Paper / variant | Original dataset | Task | Metric | Original reported score | Split | Negative / candidate protocol | Current comparison |
|---|---|---|---|---:|---|---|---|
| CCLPH / CCAAH | NDC-classes | size2 hyperlink | AUPR | 0.407 | Original hypergraph train/test; fraction NOT_VERIFIED | Community candidate filtering/threshold; per-query20 negatives not established | NOT_DIRECTLY_COMPARABLE |
| CCLPH / CCCNH | Contact-High-School | size2 hyperlink | AUPR | 0.744 | Same caveat | Same caveat | NOT_DIRECTLY_COMPARABLE |
| CCLPH / CCPRH | Cat-Edge-Geometry-Questions | size2 hyperlink | AUPR | 0.612 | Same caveat | Same caveat | NOT_DIRECTLY_COMPARABLE |
| CCLPH / CCPRH | Email-Enron | size2 hyperlink | AUPR | 0.598 | Same caveat | Same caveat | NOT_DIRECTLY_COMPARABLE |
| HMNE (2024 online/2025 issue) | Real-world networks; exact score table NOT_VERIFIED | pairwise link prediction | NOT_VERIFIED | NOT_VERIFIED (subscription preview) | NOT_VERIFIED | NOT_VERIFIED | REFERENCE_ONLY |
| HMRLH | Original networks; exact score table NOT_VERIFIED | pairwise link prediction | NOT_VERIFIED | NOT_VERIFIED (publisher full-text access limited during audit) | NOT_VERIFIED | NOT_VERIFIED | REFERENCE_ONLY |

CCLPH scores from publisher Results/discussion/Table4 narrative, [Scientific Reports2026](https://www.nature.com/articles/s41598-026-45116-w). These are different CCLPH variants/datasets, not a single selected Cora result. Source HTML retained locally with hash manifest. HMNE [publisher preview](https://link.springer.com/article/10.1007/s10115-024-02255-8). HMRLH [publisher](https://www.mdpi.com/2079-9292/12/23/4842). Fields not verified cannot support numeric publication claims. The unresolved original score fields are a literature limitation separate from the scheduled official baseline reruns.
''',
'07_FAIRNESS_AUDIT.md':'''# Fairness audit

Preflight must PASS before official jobs: frozen R-HSPE source equality, all frozen artifact hashes recorded, dataset train hashes, heldout disjointness, candidate arrays and archived NPZ hashes. Validation candidates checked against previously recorded parent validation hash. Frozen exact evaluator source hashed. No heldout edge enters sparse NCN message graph or NSLR dense train adjacency/hypergraph. Rejection samplers check only train edge complement; official NCN sampler sees only train edge_index. Labels used for disjointness audit are not made available to training sampler.

All test scores have the same query/grouping/ties in original ranking_metrics; no custom metric implementation. Only data/evaluation/output/device/API compatibility wrappers. R-HSPE/B0 frozen previous checkpoints and test scores reused; no test-driven checkpoint reselection. Third-party NCN/NCNC checkpoint selection uses validation MRR, NSLR fixed final epoch. No tuning search. Same seed labels only descriptive differences, no strict paired RNG interpretation.

Compare official recommended architecture/training settings; feature/input/training budget differences explicit. NSLR official random features and fixed negatives differ from attributed GNN and QTHS25, while permitted information and evaluation match. Candidate20 metrics saturate Hits@20; they do not imply performance with all-node or1000-negative ranking. Citeseer R-HSPE/B0 n3 vs third-party n5 disclosed. Rankings are not universal SOTA.

Failures remain error.json/logs, never replaced with synthetic metrics or silently simplified models. Failure leads PARTIAL and paper readiness NO. Frozen-file immutability reasserted during final aggregation. Final reports automatically expose every primary and secondary metric, including PubMed Hits declines. Full implementation and environment inventories saved with hashes.
''',
'08_NOVELTY_POSITIONING.md':'''# Frozen novelty positioning

The V17.2 NOVELTY_MATRIX.md is copied verbatim into FROZEN_NOVELTY_MATRIX.md with its SHA256 recorded. Benchmark scores cannot enlarge the frozen claim.

Contribution wording: candidate-specific hyperedge-pair context encoder with training-only rank-normalized cardinality descriptors and a permutation-invariant decoder residual.

Mechanism remains CONTEXT_DRIVEN. Added75parameters is an efficiency observation, not evidence that cardinality causes gains. Broad claims 'first hyperedge size', 'first candidate hyperedge context', 'size causes performance' prohibited. CCLPH is known close prior work with community-dependent hyperedge-pair intersections/cardinality factors; it supports pairwise predictions, so blanket task-mismatch dismissal is incorrect. NCN/NCNC are strong candidate-specific graph baselines. No exact complete collision identified in limited V17.2 focused audit does not prove global novelty/priority.

Results determine positioning/competitiveness, not rescue or redesign. Innovation1 stays frozen even if competitors are stronger. User decides subsequent experiments; no Innovation2 auto-launch.
'''
}
for name,text in docs.items():(root/name).write_text(text,encoding='utf8')
frozen=root.parent/'R_HSPE_FROZEN'
shutil.copyfile(str(frozen/'NOVELTY_MATRIX.md'),str(root/'FROZEN_NOVELTY_MATRIX.md'))
shutil.copyfile(r'E:\Z\benchmark173.py',str(root/'scripts/benchmark173.py'))
shutil.copyfile(r'E:\CodexStorage\Home\attachments\f63e7713-793a-499e-a507-0c25eab2af45\已粘贴的文本.txt',str(root/'TASK_V17_3.md'))
manifest={}
for dirname in ['vendor','scripts','wheelhouse']:
 for p in (root/dirname).rglob('*'):
  if p.is_file():manifest[str(p.relative_to(root))]=hashlib.sha256(p.read_bytes()).hexdigest()
for name in list(docs)+['FROZEN_NOVELTY_MATRIX.md','TASK_V17_3.md']:
 manifest[name]=hashlib.sha256((root/name).read_bytes()).hexdigest()
(root/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2))
with zipfile.ZipFile(r'E:\Z\benchmark173_docs.zip','w',zipfile.ZIP_DEFLATED) as z:
 for name in list(docs)+['FROZEN_NOVELTY_MATRIX.md','TASK_V17_3.md','SOURCE_MANIFEST.json']:z.write(str(root/name),name)
 for p in (root/'literature').glob('*'):z.write(str(p),str(p.relative_to(root)))
print('Wrote',len(docs),'protocol/audit documents')
