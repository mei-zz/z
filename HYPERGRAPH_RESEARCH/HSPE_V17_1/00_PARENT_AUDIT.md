# V17.1 parent audit

Parent: HSPE_V17. V17 efficacy evidence remains unchanged; the former per-dataset mechanism-control promotion rule is superseded by the V17.1 protocol.

H1 is the exact V16 C1_NHMC_SIZE class used in V17. It represents each incident hyperedge pair by [a+b, |a-b|, a*b, 0, 0, 0], where a=log(1+|e|), b=log(1+|f|). Linear(6,8), ReLU, mean/max pooling, followed by log(1+token_count) and log(1+shared_support_count); zero-initialized Linear(18,1) residual. Added trainable parameters: 75. Baseline/H1 totals: Cora 24735/24810; PubMed 9807/9882.

Frozen training: Raw-HG DCDLP A5, raw-star, GCN hidden16, 2 layers, dropout0, branch8, AdamW/lr0.001/weight_decay0.0001 from the frozen config, batch4096, BCE, QTHS25 fixed selected negative per train positive, target masking, fixed final epoch10, validation only. No five-epoch result is reused as ten-epoch evidence.

Cora pool SHA256: 3d1e3ea691fc19fab65d66ad278d169cf099eb831ad0e46a439510ff5d07a7ba
Cora selected SHA256: 1ada7e01d1b3fa788db9d8312167290d4191344ace2db40bb787ab78e027c758
Cora validation SHA256: 7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902
PubMed pool SHA256: d2434f4508c3fa493a400ddfa2abc71b3eb59999b977a557bc4dcfd4845849db
PubMed selected SHA256: 28f8b8720989c1a445a46480d7ce60ac9e07fa0de24103541b2dec566d97da7d
PubMed validation SHA256: c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683

Frozen V16 implementation SHA256: f3b19889afa236fd71eeaa6681efc31c845eb32c4a90df87ab8d40092c196982. Parent V17 runner SHA256: da20e41442f8e7b0b12d29515ba2a3df71a2a0a7327a51ea2b1170901e2e28bf. Current server sources, cache hashes, split/candidate hashes are checked by build_context and recorded per seed. TEST OFF.
