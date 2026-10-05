# Autonomous innovation ledger

| Candidate | Hypothesis | Novelty status before experiment | Status |
|---|---|---|---|
| A — SSHC | Calibrate every raw star-hyperedge message with off-center leaf cohesion, initialized near identity. | `NOVELTY_CONFLICT`: structural hyperedge weighting and within-hyperedge pairwise density/clustering are established; exact near-identity calibration for star-hypergraph link prediction is narrower and unverified. | REJECT after the one allowed initialization correction: corrected A4 is below shuffled-cohesion A3 and below the required gain threshold. |
| B — RAHC | Reduce repeated contribution from overlapping star hyperedges with all edges retained. | `NOVELTY_CONFLICT`: Jaccard-weighted hyperedge line graphs and redundancy pruning are known; RAHC retains every edge and applies a top-3 overlap penalty directly to messages, but the exact link-prediction use remains unverified. | REJECT: real-redundancy B4 falls below size and shuffled controls. |
| C — HSA | Train raw hyperedge summaries with non-center leaf-pair support. | `NOVELTY_CONFLICT`: substructure-aware self-supervised hyperedge prediction and incidence reconstruction are established; HSA narrows the target to graph-edge support among leaves of fixed stars, but novelty is unverified. | REJECT: the best true arm beats every control but misses both predefined effect-size thresholds. Final candidate; no fourth candidate or Stage 2 follows. |

## Literature checked for A

- Huang, Elgammal & Yang, “On The Effect of Hyperedge Weights On Hypergraph Learning,” proposes hyperedge weighting schemes based on geometry, multivariate statistics and regression. [arXiv:1410.6736](https://arxiv.org/abs/1410.6736).
- Miyashita, Hironaka & Shudo, “Clustering coefficient reflecting pairwise relationships within hyperedges,” defines a hypergraph clustering coefficient that explicitly uses within-hyperedge pairwise link density. [Scientific Reports (2025)](https://www.nature.com/articles/s41598-025-07869-8).

These works make a broad claim of novel “structural hyperedge weighting” unsafe. SSHC is retained only as a tightly controlled falsification of the specific off-center cohesion signal on star hyperedges; it must not be presented as a new general weighting principle without a deeper literature audit.

## Literature checked for B

- DDEC uses Jaccard overlap to weight edges in the hyperedge line graph for structural dependency modeling. [Entropy (2026)](https://www.mdpi.com/1099-4300/28/7/729).
- Hypergraph Structure Learning for Hypergraph Neural Networks explicitly samples/prunes redundant hyperedges. [IJCAI 2022](https://www.ijcai.org/proceedings/2022/0267).
- TF-MP uses inverse hyperedge degree in propagation normalization. [ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/ad9804eed175610302917a0c21ab9b52-Abstract-Conference.html).

These methods establish overlap modeling, redundancy handling and degree-based message calibration as known ideas. RAHC's limited distinction is to keep the complete incidence set and apply a top-3 shared-node Jaccard penalty to each message in pairwise link prediction. The overlap is material, so this remains a mechanism falsification rather than a novelty claim.

## Literature checked for C

- S3Hyper uses sub-hyperedge information to model internal compositional structure for self-supervised hyperedge prediction. [AAAI 2026](https://ojs.aaai.org/index.php/AAAI/article/view/39471).
- DualCL includes explicit node-hyperedge incidence reconstruction as a self-supervised objective. [Springer (2026)](https://link.springer.com/article/10.1007/s44443-026-01156-w).
- Neural Hypergraph Link Prediction directly targets prediction of missing hyperlinks. [NHP paper](https://prateek-yadav.github.io/assets/pdf/nhp.pdf).

These establish close precedents for hyperedge/substructure supervision. HSA differs in using observed train-graph leaf-leaf edges inside fixed star hyperedges as a small auxiliary signal for ordinary pairwise link prediction, while excluding center-leaf pairs. The distinction is narrow and carries novelty risk, but merits the final one-epoch mechanism check because its label source and prediction target differ from full missing-hyperedge prediction.
