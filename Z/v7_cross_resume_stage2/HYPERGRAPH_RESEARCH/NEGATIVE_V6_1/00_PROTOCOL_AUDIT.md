# V6.1 Protocol Audit

## Strict boundary

- Candidate-pool forbidden set was formed only from canonicalized training positives and the training/message graph edges; self-loops and out-of-range pairs were rejected by the same eligibility predicate.
- The miner and teachers received a train-only view. Accessing `all_positive` raises; actual validation/test identities were not exposed to candidate sampling, teacher fitting/scoring, or strict training.
- The compatibility training loop saw empty validation/test placeholders only. Validation selection was replaced by the precommitted fixed-final-epoch-10 rule; no validation or test score selected a checkpoint.
- The held-out-positive eligibility unit test passed: a synthetic future-positive identity and an ordinary unknown pair both pass the exact same train-only candidate predicate.
- Validation used the previously audited V6 fixed candidate tensor; test scoring ran once only after all strict validation results and gates were frozen.
- Test labels were first consumed in the post-hoc stage after training and validation decisions were frozen.

## Frozen settings

Cora standard; 20 candidate pairs per training positive; A1/A3/A4; nominal veto=0.25; graph prepool multiplier=2 (2 candidates, 1 removed); 10 epochs; seeds 0/1/2.

Train positives: 4488; candidate pool hash: `3d1e3ea691fc19fab65d66ad278d169cf099eb831ad0e46a439510ff5d07a7ba`; train-only split hash: `c5cec7e3bf6eaad41e12ae786246bf454a1bbcd4476286c71eb7e75b0eeba71a`.

## Filtered sensitivity control

Reused the exact V6 FILTERED_ALL_POSITIVE runs. Their validation-best checkpoint rule differs from strict V6.1's fixed epoch-10 rule, so this is protocol sensitivity context rather than a fully matched retraining comparison.

## Novelty status

`EXACT_RULE_UNVERIFIED`.
