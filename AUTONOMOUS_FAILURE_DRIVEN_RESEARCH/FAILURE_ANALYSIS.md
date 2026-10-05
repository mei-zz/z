# Failure Analysis

## Immediate finding

The current failure-driven audit did not discover a supported new architecture. It discovered a stable Parent weakness on Cora HeaRT, but that weakness is substantially explained by existing non-neural proxies and by known pair-aware link-prediction families. The correct conclusion is not “the next module should be AA/RA”; those are already known statistics and are not an independent contribution.

## Why the four prior sessions failed

### 1. The search started from modules, not unmet failures

V1–V5 mostly asked whether a new statistic, decoder, branch or pair state could improve one existing benchmark. That reverses the causal order. Without first identifying a subgroup in which Parent and strong baselines fail for the same reason, every new module is free to explain a random fluctuation.

### 2. The proposed information was already available elsewhere

V1’s path, boundary, spectral and community features were ordinary functions of the observed train graph. The V6 Cora audit shows the same danger directly: fixed AA/RA and feature cosine are competitive or better than Parent under the exact official candidate set. A decoder cannot claim independent information when a cheap proxy can compute the relevant ordering.

### 3. The decoder did not repair encoder information loss

PCDT and CDPT changed the pair-side calculation. But target-pair masking and node-only message passing determine what information reaches the decoder. If the missing signal is not retained by the encoder, a more elaborate decoder only reparameterizes the same representation. V4’s Early×Early control defeating CDPT is consistent with this explanation.

### 4. Controls were sometimes weaker than the claim

Historical shuffled, frozen, parameter-matched and cross-depth controls were not always introduced before the positive result. V4 corrected much of this and rejected CDPT. The lesson is that a candidate must be designed together with the control that would kill it, not after a positive run.

### 5. Narrow benchmark and metric incentives encouraged overfitting

Cora HeaRT is useful but narrow. Repeatedly selecting structures or settings from one test distribution creates a hidden research-set effect. AUC-only or probe-only gains were repeatedly mistaken for link-ranking progress. Current reports separate validation decisions from descriptive test values.

### 6. Randomness was real but not the whole explanation

V4 found execution variability in non-strict reruns, but strict deterministic repeats were bitwise identical and CDPT still failed the mechanism comparison. Therefore “run more seeds” is necessary for evidence, not a repair for a false mechanism.

### 7. Novelty was checked too late or too shallowly

T2WL-INC was mathematically a 2-FWL/Local 2-FWL collision. Topology editing and edge-space variants likewise collided with existing methods. Comparing names is insufficient; the state object and update equation must be compared before code is written.

## Error-type classification

| Failure type | Historical examples | Evidence level | Correct response |
|---|---|---|---|
| Hypothesis wrong | PCDT correspondence, CDPT cross-depth independence | Strong | Terminate family |
| Structure redundant | V1 statistics, current AA/RA explanation | Strong for tested protocols | Do not rename or wrap the proxy |
| Novelty collision | T2WL-INC, PTALP, topology editing | Strong | Stop before training |
| Optimization / budget | Some seed variation and short runs | Partial | Only test after mechanism remains viable |
| Data/protocol mismatch | Cross-comparing NCN native Cora to HeaRT | Certain risk | Do not compare |
| Unavailable benchmark | A/B in this cycle | Confirmed logistical block | Mark NOT_EXECUTED, do not infer failure |

## Preparation for the next legitimate innovation

The next project should not begin with a tensor or branch. It should begin with one of these falsifiable questions:

1. Under an explicit incomplete/noisy graph protocol, does the observed graph itself become an uncertain object, and can a method beat PULL/CORE controls?
2. Under a node-disjoint inductive split, what information is available for a new endpoint, and can a method beat GraphSAGE/NCN/LEAP controls?
3. Under LPShift or another predeclared structural shift, which hard-negative subgroup remains unsolved after AA/RA, feature, NCN and SEAL controls?

Until one question has a public dataset, a repeatable Parent error subgroup, and a baseline-independent information bottleneck, there is no scientific basis for another architecture.
