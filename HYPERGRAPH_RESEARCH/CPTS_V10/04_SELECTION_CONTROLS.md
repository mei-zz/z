# Selection controls

- **Global-CPTS:** one BIC split is fit on pooled Cora train-only teacher scores and its shared raw-score boundary is applied to each training positive. Mean validation MRR is 0.443442; CPTS is higher by 0.093604 and wins 3/3 seeds.
- **Matched-Q:** Cora's train-only mean tail fraction is 0.341288; the fixed control removes seven candidates and selects rank 8 for every positive. CPTS is higher in validation by 0.008949 and wins 2/3. On the one-time Cora test, Matched-Q is higher by 0.002046 and CPTS wins 1/3; preserve this caveat.
- **Random-Matched:** removed count exactly matches each positive's CPTS tail count, with deterministic random removal. CPTS is higher by 0.062333 in validation (2/3 wins) and +0.064778 on Cora test (2/3 wins).
- The Cora selection overlap rates are 0% with Graph-hard, 0% with QTHS25, and 4.23–4.68% with SH75 across seeds. CPTS mean selected rank from hardest is 7.826 (median 8); Matched-Q is rank 8; SH75 is about rank 13.
- All selectors use the frozen 20-candidate training pool, `STRICT_TRAIN_ONLY`, K=1, fixed epoch 10. The one-time Cora test used the locked V8/V7.1 candidate set after validation GO.
