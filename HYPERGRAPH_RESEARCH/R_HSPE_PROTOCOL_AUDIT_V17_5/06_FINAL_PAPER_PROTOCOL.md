# Final paper protocol

Canonical identifier: R-HSPE-PAPER-V17.5. It is a reconciled evidence package with two separately labeled table protocols.

- Table A is V17.3 standalone/fair benchmark: NCN/NCNC 100 epochs with first best validation-MRR checkpoint; NSLR-HMANN 5000 epochs/final checkpoint; previous frozen R-HSPE/control results reused.
- Table B is V17.4 plugin comparison: five seeds, all arms at 10 epochs, fixed final checkpoint, shared locked splits/candidates/evaluator and exact within-run seed pairing. This is the primary protocol for complementarity claims.

The absolute scores cannot be combined into one rank order. Cora/PubMed paired effects are canonical for plugin claims. Citeseer is validation-only failure; test is not run.

Evaluation contract: train-only undirected graph; no held-out message edges; target masking on; 20 negatives per query; frozen V17.2/QTHS V7.1 test candidates (seed 999, group seed 1000); frozen ranking_metrics implementation and tie/group rules. Protocol hashes are in CANONICAL_PROTOCOL.json and SOURCE_HASHES.json.

## Backbone training configuration audited

Official NCN/NCNC implementation uses hidden width 256, one message-passing layer, three predictor layers, Adam with separate GNN/predictor learning rates, PyG official negative sampling, official summed positive/negative log-sigmoid loss, input masking, and default weight decay 0. The per-dataset dropout, learning rates, probability parameters, and train batch sizes are preserved in CANONICAL_PROTOCOL.json. V17.4 changes the epoch budget and final checkpoint policy only.

Dataset-specific NCN/NCNC optimizer settings (GNN LR / predictor LR / train batch): Cora 0.0043 / 0.0024 / 1152; Citeseer 0.0085 / 0.0078 / 384; PubMed 0.0097 / 0.0020 / 2048. Official hidden width 256, one message-passing layer and three predictor layers apply across these citation datasets.
