# Stage 0 cross-dataset diagnostic results

Per the latest override, fixed-summary Logistic Regression Stage 0 is diagnostic only and does not gate neural Stage 1. Test evaluation was off for every dataset.

## CORA

Decision: `NO_NATIVE_STRUCTURE_SIGNAL`. Train positives: 4488; selected matched negatives: 13464; token count: 135189; maximum tokens per pair: 372; informative shuffle fraction: 0.2802.

|Feature|ROC-AUC (mean ± SD)|PR-AUC (mean ± SD)|
|---|---:|---:|
|CN|0.810846 ± 0.005794|0.637859 ± 0.013213|
|HRA|0.825468 ± 0.006334|0.732724 ± 0.010822|
|Projection|0.826591 ± 0.005947|0.740013 ± 0.009435|
|Native size|0.836022 ± 0.005870|0.749874 ± 0.007015|
|Native real|0.835925 ± 0.006490|0.751966 ± 0.007576|
|Native shuffle|0.835783 ± 0.007573|0.749599 ± 0.007732|
|Native scalar|0.796201 ± 0.006102|0.679236 ± 0.008340|

Δnative=Z4−Z2: 0.009334; Δcontent=Z4−Z3: -0.000097; Δsemantic=Z4−Z5: 0.000142.
Target-mask audit: 100 pairs; full rebuild and endpoint symmetry passed; maximum absolute difference 0.

Matching: 4488 positives each received 3 negatives; exact support-count matches: 3670; exact HRA-bin matches: 13464.

## PUBMED

Decision: `NO_NATIVE_STRUCTURE_SIGNAL`. Train positives: 37676; selected matched negatives: 113028; token count: 4976014; maximum tokens per pair: 4856; informative shuffle fraction: 0.2810.

|Feature|ROC-AUC (mean ± SD)|PR-AUC (mean ± SD)|
|---|---:|---:|
|CN|0.787592 ± 0.002306|0.671012 ± 0.003447|
|HRA|0.793083 ± 0.002643|0.692194 ± 0.003773|
|Projection|0.793598 ± 0.002508|0.701818 ± 0.002866|
|Native size|0.808829 ± 0.002210|0.713337 ± 0.001838|
|Native real|0.809133 ± 0.002115|0.714967 ± 0.002108|
|Native shuffle|0.808682 ± 0.002136|0.713368 ± 0.001800|
|Native scalar|0.792060 ± 0.002183|0.686063 ± 0.003340|

Δnative=Z4−Z2: 0.015535; Δcontent=Z4−Z3: 0.000304; Δsemantic=Z4−Z5: 0.000451.
Target-mask audit: 100 pairs; full rebuild and endpoint symmetry passed; maximum absolute difference 0.

Matching: 37676 positives each received 3 negatives; exact support-count matches: 36568; exact HRA-bin matches: 113028.

## CITESEER

Decision: `NO_NATIVE_STRUCTURE_SIGNAL`. Train positives: 3870; selected matched negatives: 11610; token count: 161491; maximum tokens per pair: 1101; informative shuffle fraction: 0.1621.

|Feature|ROC-AUC (mean ± SD)|PR-AUC (mean ± SD)|
|---|---:|---:|
|CN|0.758611 ± 0.012041|0.600422 ± 0.022330|
|HRA|0.762868 ± 0.011958|0.641755 ± 0.016614|
|Projection|0.763744 ± 0.012108|0.648879 ± 0.017133|
|Native size|0.763924 ± 0.013332|0.649517 ± 0.017939|
|Native real|0.764339 ± 0.012329|0.650220 ± 0.017517|
|Native shuffle|0.764959 ± 0.013088|0.649760 ± 0.017570|
|Native scalar|0.736897 ± 0.014951|0.597540 ± 0.023282|

Δnative=Z4−Z2: 0.000595; Δcontent=Z4−Z3: 0.000415; Δsemantic=Z4−Z5: -0.000620.
Target-mask audit: 100 pairs; full rebuild and endpoint symmetry passed; maximum absolute difference 0.

Matching: 3870 positives each received 3 negatives; exact support-count matches: 5142; exact HRA-bin matches: 11610.

