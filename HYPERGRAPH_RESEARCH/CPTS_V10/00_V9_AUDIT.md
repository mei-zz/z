# V9 audit and protocol lock

V9 established why selected-negative loss reweighting cannot work with the existing training protocol: there is one selected negative per positive (K=1), even though the frozen train-only graph-teacher pool contains M=20 candidates per positive. Within-positive median and weight redistribution therefore degenerate. V10 permanently leaves K=1 and changes only the candidate selection rule.

V8/V7.1 evidence and implementation were reviewed. Graph-hard is the top graph-teacher score from the frozen 20-item row; QTHS25 selects from its fixed top-two rule; SH75 samples the registered rank interval. All training remains `STRICT_TRAIN_ONLY`, uses the same DCDLP GCN encoder/decoder/optimizer, fixed 10 epochs and epoch-10 checkpoint, and applies the existing train-forbidden edge filter. V10 test remains disabled until Cora validation passes.

The candidate score caches are reused without teacher retraining. Cora teacher score hash: `a1b01e0e2ad5cd287011862d65ade0681205d11ca99dc50cf1b763faf8a82d5c`; candidate pool hash: `3d1e3ea691fc19fab65d66ad278d169cf099eb831ad0e46a439510ff5d07a7ba`. PubMed and Citeseer teacher score arrays and metadata are also available and passed hash verification in the tail audit.
