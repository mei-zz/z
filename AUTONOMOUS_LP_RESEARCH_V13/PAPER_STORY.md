# Paper story (working)

## Current evidence

A low-capacity residual combining pair-specific Raw-HG features with target-masked structural evidence improves fixed-final-epoch Cora validation MRR. With 28 additional parameters, ECR_FULL reached 0.607815 (5 epochs) against 0.525620 for the matched QTHS25+BCE baseline and 0.486030 for a pair-shuffled evidence control. A separate 10-epoch seed-0 confirmation reached 0.588266 against 0.530263 baseline and 0.552266 shuffled control.

Across fresh Cora seeds 0/1/2 at 10 epochs, the candidate beat baseline and shuffled control in all three seeds; mean gains were +0.068162 and +0.057092. Following the registered LOCAL_GO gate, one Cora test evaluation (527 positive pairs, 20 negatives each) gave 0.623888 vs 0.554033 baseline and 0.577498 shuffled control.

## Status and limits

Cora evidence is strong but single-dataset. PubMed three-seed validation is in progress. Related work already learns structural heuristics and injects them into neural link prediction, so novelty is not established. Cora test has been used once and will not guide any further method changes.

## Provisional question

Can a parameter-efficient, target-masked residual that calibrates a hypergraph link score from complementary pair-level structural evidence generalize across seeds and datasets, and can a separate mechanism add value on top of it?
