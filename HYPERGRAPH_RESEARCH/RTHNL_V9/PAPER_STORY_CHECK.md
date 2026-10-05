# Paper story check

- Supported: V8 QTHS25 motivated a continuous, ratio-free tail-weighting hypothesis; its Cora SH75 control and trim sensitivity exposed weaknesses in treating QTHS25 as a final method.
- Supported: under the actually frozen V8 training count K=1, the V9 median-centered weighting has no within-positive tail to suppress. Its raw weights are 1 and it is algebraically identical to the shuffled control.
- Supported: Cora's cached V8 Graph-hard fixed-epoch-10 validation MRRs imply a zero RTHNL-vs-Graph-hard difference for the registered K=1 rule; the validation gain and mechanism gates fail. V8 SH75 mean is higher.
- Not supported: empirical RTHNL improvement, cross-dataset stability, backbone generalization, or any causal explanation of Graph-hard/QTHS performance.
- Not supported: that random negatives are universally too easy. V8 Uniform exceeded Graph-hard on reported Cora backbones.
- Claim limit: report this as a protocol-level falsification/degeneracy finding. Do not present RTHNL as a validated method or claim novelty.
