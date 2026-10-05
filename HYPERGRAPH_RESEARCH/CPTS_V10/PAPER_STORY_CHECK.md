# Paper story check

## Supported

- The train-only BIC audit detects heterogeneous tail sizes on Cora, PubMed and Citeseer. Tail presence is 100% in all three datasets, but tail size is dispersed; no dataset collapses to one fixed removal count.
- Cora validation passes the preregistered main, SH75, QTHS25, Global-CPTS, Matched-Q and Random-Matched gates.
- Cora test supports CPTS against Graph-hard, QTHS25 and SH75 under the registered test gate.
- PubMed and Citeseer CPTS validation means exceed Graph-hard; CPTS also beats Graph-hard on all three tested Cora backbones by mean.

## Limits to state plainly

- Cora test Matched-Q mean is 0.002046 MRR above CPTS, with CPTS winning only 1/3 seeds. Therefore held-out evidence for per-positive adaptivity is mixed even though the Cora validation Matched-Q gate passed.
- PubMed QTHS25 is 0.007313 above CPTS and wins all three seeds. Citeseer SH75 is 0.013495 above CPTS and wins all three seeds.
- PubMed, Citeseer and backbone results are validation-only. Only Cora has a test evaluation in this staged experiment.
- Novelty remains EXACT_RULE_UNVERIFIED. Do not claim “first”; distinguish the rule from DMNS, ProGCL and adaptive hardness work in adjacent settings using `09_NOVELTY.md`.

## Overall interpretation

The registered decision is **GO**, not STRONG_GO. CPTS is a viable adaptive selector with consistent mean gains over Graph-hard and positive Cora backbone results. The results do not support universal superiority over fixed hardness controls or a strong priority claim.
