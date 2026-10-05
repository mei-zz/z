# Integration and paired-comparison validity

Train message graphs contain undirected train-positive edges only; held-out edges are absent and no clique expansion is used. Target-pair masking is enabled. Training negative sampling sees train-visible positives only; held-out positives are filtered in frozen evaluation candidate construction. There are 20 grouped negatives per query.

V17.4 audits 54 paired comparisons. Initial model state, official negatives, epoch permutations/training order and CUDA RNG traces match exactly within each dataset/seed/backbone. Thus V17.4 C1−C0 and C1−C2 deltas are strict paired. V17.3 did not retain complete initialization/sample/order/CUDA traces, so V17.3 versus V17.4 values are not called paired.

The invalid preliminary PubMed load was caught before optimization and excluded. The corrected load-before-reseed path was used for all final comparisons. R-HSPE was frozen before test; Citeseer test remained unopened after its validation gate failed. No leakage or unresolved integration bug remains.
