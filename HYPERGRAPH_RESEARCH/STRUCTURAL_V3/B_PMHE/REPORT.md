# Candidate B — PMHE falsification

## Decision

**REJECT.** F0 passed the early screen, but in F1 the pair-moment arm B3 failed to outperform both the mean and second-moment controls and missed the gain threshold. Test scoring was not run. Candidate C was then started.

## Protocol and operator

Cora, standard split, seed 0, same A5 configuration and training/evaluation negatives as Candidate A. B0–B3 used 1 epoch in F0 and 5 epochs in F1, with a matched Raw arm at each budget. All runs set `evaluate_test=false`; the best checkpoint was selected by validation MRR.

For each full star incidence set, B3 computes the mean unordered Hadamard product using `(S1 ⊙ S1 − S2)/(k(k−1))`, with zero for `k<2`; this is O(kd) and does not enumerate pairs. B1 and B2 pass the incidence mean or mean second moment through the same learned projection, keeping the residual branch parameter-matched.

## Results

| Arm | Statistic | F0 best val MRR | F1 epoch curve (val MRR) | F1 best val MRR |
|---|---|---:|---|---:|
| B0 | Raw global hypergraph | 0.162793 | 0.162793, 0.287014, 0.399852, 0.463626, 0.487678 | 0.487678 |
| B1 | Mean control | 0.162642 | 0.162642, 0.285556, 0.399630, 0.463422, 0.487893 | 0.487893 |
| B2 | Second-moment control | 0.164497 | 0.164451, 0.286401, 0.403609, 0.463048, 0.487971 | **0.487971** |
| B3 | Pair-moment | 0.164560 | 0.164560, 0.286256, 0.401431, 0.463123, 0.487705 | 0.487705 |

B3's F1 gain over Raw is +0.000027 MRR (+0.0055% relative), below +0.003/+2%; it is also 0.000188 below B1 and 0.000266 below B2. The F0 B3–Raw difference was +0.001767 and did not meet the GO threshold, so F1 was required.

## Cost and novelty

The PMHE residual adds 257 trainable parameters (1.04% over the raw model). F1 training time was 33.4 s for B0 and 35.3 s for B3 (+5.7% in this single run). B3's learned gamma was 0.00617. No test metrics were computed.

Broad pairwise-aware hyperedge encoding has prior art (`NOVELTY_CONFLICT`); this exact normalized closed-form moment on graph-induced stars remains `NOVELTY_UNVERIFIED`. See `../01_NOVELTY_SEARCH.md`.
