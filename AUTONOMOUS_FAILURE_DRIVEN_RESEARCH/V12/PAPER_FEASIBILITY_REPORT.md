# V12 Paper Feasibility Report

## 结论

本轮不能形成“Task-Aligned Model Selection for Inductive Link Prediction”作为独立方法论文的充分证据。最终状态为 `NOVELTY_KILL`，而不是 `PAPER_CANDIDATE`。

## 可以成立的结果

可以保留以下谨慎结论：

1. 在 NodeDup 的 Cora/CiteSeer repaired protocol 中，old-only validation 与 new-node deployment composition 不一致；
2. 改变 checkpoint 指标或加入 new-node validation 会改变选择 epoch；
3. 这种影响在 V11 的四个模型/数据组合中可观察，但 B→D 方向并不一致；
4. 这属于 benchmark/protocol audit finding，不是网络结构收益。

## 不能成立的结果

- 不能声称 M2 优于 D，因为 M2 没有独立 test；
- 不能声称 0.5/0.5 是最优权重；
- 不能声称方法在未见数据划分上稳定；
- 不能声称全球首次或论文级创新；
- 不能把 V11 已查看 test 作为 V12 confirmatory evidence。

## 若以后只做协议论文

需要另建真正未参与决策的 final evaluation，至少多次独立 node partition，并将 M2 与普通 mixed-MRR、worst-group、sample-weighted MRR 等已有选择规则比较。那将是评测方法的增量研究，当前证据不足以承诺 SCI 二/三区论文价值。
