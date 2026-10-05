# V8 audit for V9

## Workspace and scope

The connected `workspace_info` tool returned an internal error rather than a workspace identity. The local project at `E:\我的资料库\Documents\Downloads\DCDLP-main` and SSH project `/home/zhoulihui/lchr_v2` were directly inspected and are DCDLP-main. No other project was used.

## Frozen training path

- Protocol: `STRICT_TRAIN_ONLY`; held-out positive identities are not miner inputs. The audited Cora train-only candidate pool has hash `3d1e3ea691fc19fab65d66ad278d169cf099eb831ad0e46a439510ff5d07a7ba`, 4,488 training positives, 20 candidates per positive, and 89,760 candidates total.
- Teacher: frozen graph teacher, seed 0, epoch 10; checkpoint hash `30343bdf61b8fa38a7d9eecbd280a836ee81ef4dfeb63efeb1c74445337ad28b`. Detached score cache hash `a1b01e0e2ad5cd287011862d65ade0681205d11ca99dc50cf1b763faf8a82d5c`.
- Graph-hard: choose the maximum teacher-score candidate from the 20-candidate row.
- Training negative count K: **1 per positive per epoch**. The V8 archive shape is `[10,4488,2]` (10 epochs, 4,488 edges, 2 endpoints). V8 `train_one` checks selected negatives have shape `(N,2)` and asserts one negative per training positive. The 20-item pool is not K.
- QTHS25: select from its frozen top-two prepool. With alpha .25, stable-hash selection uses the runner-up for 50% of positives. It still trains one negative per positive.
- SH75: sort each frozen row by descending teacher score and sample uniformly from indices `[10:15]` (zero-based), the rank window labeled [50%,75%].
- Loss: `binary_cross_entropy_with_logits(logits, labels)` with default mean reduction; the training batch contains shuffled positive and negative examples. For an individual negative logit `s`, BCE is `softplus(s)` and its logit derivative is `sigmoid(s)`. No separate hard-negative logit or auxiliary loss is used in this path.
- Checkpoint: exactly epoch 10; validation does not select a checkpoint. V8 Cora main seeds are 0, 1, 2; test candidates are only evaluated after validation gates.
- Negative filtering: training sampler applies `make_train_forbidden` to exclude training positives, observed train/message-graph edges, self-loops, and invalid node ids. It does not read held-out positive identities.

## Relevant V8 evidence

QTHS25 was a motivating prototype. Its Cora validation mean was 0.474662 versus Graph-hard 0.453804, but SH75 was 0.534363. The paired QTHS25−SH75 mean was −0.059701. Uniform also outperformed Graph-hard on the reported Cora backbones, so the evidence does not support the claim that random negatives are simply too easy.

The protocol requests a single negative-loss weighting change while freezing K. Because K=1, that constraint makes the proposed within-positive RTHNL distribution a singleton. V9 therefore stops at the Cora validation gate; this report does not claim a completed empirical RTHNL benchmark.
