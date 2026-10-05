# V15 Protocol Audit

Workspace: DCDLP-main at the requested project path. Git metadata is unavailable because this directory is not a Git repository; source files will be identified by SHA-256. V14 was stopped before creating files or launching jobs. Existing V13 remains untouched. Server audit found no V13/V14/HMC process; Tesla V100 was idle at 0%, 14 MiB used.

Frozen V13 strong baseline:
- Raw-HG DCDLP A5; additive decoder; degree/CN/residual branches and interaction enabled.
- GCN, hidden dimension 16, two layers, dropout 0; pair branch dimension 8.
- Hypergraph mode raw, construction raw_star: one closed-neighborhood hyperedge per non-isolated center in the supplied message graph.
- QTHS25 fixed train-negative selection, BCE; AdamW-compatible project optimizer; learning rate 0.001, weight decay 0.0001, batch size 4096.
- Cora seed 0 Stage 1: 5 epochs, 24,735 parameters, validation MRR 0.5256204672, test disabled.
- HMC may change only pair representation/residual input; all arms share split, sampler and training protocol.

Server: ubuntu-ProLiant-DL380-Gen9, Tesla V100-PCIE-16GB; mei_env uses Python 3.11.11, PyTorch 2.8.0+cu128, PyG 2.5.3, CUDA available.

Leakage boundary: Stage 0 builds from TrainOnlyView training positives and the V6.1 STRICT_TRAIN_ONLY legal negative pool. Each training-positive target edge is removed before motif features are computed. No validation/test identity is used for HMC features, matching, folds or normalization. Test remains sealed.