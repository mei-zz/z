# V9 Matched-Protocol Results

## 1. Frozen protocol

V9 reused the two LPShift datasets already frozen in V8. No data-generation seed, split, candidate list, message graph, negative-candidate file, or ranking implementation was changed.

| Setting | Dataset | Message-graph SHA-256 |
|---|---|---|
| A | `ogbl-collab_CN_2_1_0_seed1` | `9f7c3d699b039c5ce37c1c50aa53abfa464df6c897b18c8b79f5d3ad8b101eee` |
| B | `ogbl-collab_CN_4_2_0_seed1` | `e7139c7a780dc610d1032757007b933d32c1b92575cc8fa0fdb996da4445b71d` |

The official average-rank tie rule was retained. Validation MRR was the only selection metric. Test values in the accompanying ablation report are frozen descriptive values; they were not used to select a model, feature, training epoch, or research direction.

## 2. Pairing audit

The V9 control runner used the same training-positive ordering, uniform non-message negative sampler, epoch-dependent random seeds, and training-order seeds as the V8 DCDLP trace. The aggregate checker reports:

| Setting | Seeds checked | Negative-stream hashes | Training-order hashes | Pairing result |
|---|---:|---|---|---|
| A | 1, 2, 3 | all equal to V8 trace | all equal to V8 trace | PASS |
| B | 1, 2, 3 | all equal to V8 trace | all equal to V8 trace | PASS |

Thus differences between a learned control and DCDLP cannot be attributed to a different sampled training-negative stream or a different positive/negative batch permutation in these runs.

## 3. Configuration comparison

| Component | DCDLP Parent (V8) | Learned V9 controls |
|---|---|---|
| Epochs / batch size | 4 / 262,144 | 4 / 262,144 |
| Optimizer | AdamW | AdamW |
| Learning rate / weight decay | `1e-3` / `1e-4` | `1e-3` / `1e-4` |
| Training negatives | uniform non-message edges | identical protocol and hashes |
| Selection | validation MRR | validation MRR |
| Seed pairing | 1, 2, 3 | 1, 2, 3 |
| Parameter count | 28,966 | FeatureMLP 257; TopologyMLP 641; LinearFusion 11; ParamMatchedFusion 29,029 |
| Input | target-masked GNN representations and DCDLP decoder | fixed pair statistics from the official message graph and original node features |

`ParamMatchedFusion` has 63 more parameters than DCDLP (`+0.217%`). It is a capacity control, not a proposed model. FeatureMLP and TopologyMLP test whether a small nonlinear model can use one information family; LinearFusion tests additive combination; ParamMatchedFusion tests whether a large enough ordinary MLP on the same statistics explains the result.

## 4. Important non-equivalences

The controls are protocol-matched, not implementation-identical:

1. DCDLP performs target-edge masking inside its message encoder. The V9 pair-statistic controls have no node encoder; their degree-based statistics decrement the current training positive endpoints, but they cannot reproduce every internal GNN masking effect.
2. DCDLP learns node representations from the message graph. The V9 controls use ten explicitly defined pair statistics: degree, common-neighbor, Adamic–Adar, resource-allocation, feature cosine, and feature absolute-difference terms. This is deliberately a strong simple attribution control, not a replacement claim for the full encoder.
3. Fixed FeatureCosine and TopologyRA have no training budget because they are deterministic algorithms. They are included precisely to test whether learning is necessary.
4. Feature construction is cached once per setting/seed and shared by all controls. The cache cost should therefore not be charged repeatedly to each control. DCDLP's end-to-end GNN cost is not directly comparable to a cached pair-statistics lookup.

These differences are retained rather than hidden. They leave a residual question about representations outside the tested statistics, but they do not provide evidence for an independent feature–topology interaction.

## 5. Resource record

Representative V9 resource measurements from the remote V100 runs:

| Work | Setting A | Setting B |
|---|---:|---:|
| Shared feature-cache construction, seed 1 | 261.93 s | 195.53 s |
| Feature evaluation, seed 1 | 63.64 s | 50.71 s |
| Learned-control model runs | approximately 3.5–5.7 s each | approximately 3.5–5.7 s each |
| FeatureMLP / TopologyMLP peak GPU memory | approximately 237 MB | approximately 237 MB |
| LinearFusion peak GPU memory | approximately 48 MB | approximately 48 MB |
| ParamMatchedFusion peak GPU memory | approximately 932 MB | approximately 932 MB |
| DCDLP Parent V8 peak GPU memory | approximately 3.58–3.63 GB | approximately 3.58–3.63 GB |

The original JSON files and logs are retained under `AUTONOMOUS_FAILURE_DRIVEN_RESEARCH/V9/raw/`. Remote prediction artifacts remain at the recorded paths in those JSON files.

## 6. Protocol conclusion

The comparison is valid for the intended attribution question: under the same frozen LPShift candidate protocol and paired training randomness, simple feature-only and topology-only rules already reproduce or exceed the relevant DCDLP validation behavior. The remaining encoder/masking non-equivalence is a limitation to report, not a basis for claiming a hidden interaction.
