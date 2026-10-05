# Fair benchmark main table

Only frozen-protocol reruns and hash-compatible frozen results. Sample SD (ddof=1). **Best**, *second best*, by mean MRR within this table only. Citeseer frozen R-HSPE/B0 use 3 seeds; third-party methods target 5.

| Method | Cora MRR | PubMed MRR | Citeseer MRR | Params | Fair protocol |
|---|---:|---:|---:|---|---|
| B0_BASELINE | 0.465940 ± 0.129872 (n=5) | 0.843116 ± 0.012572 (n=5) | 0.438572 ± 0.091925 (n=3) | cora:24735; pubmed:9807; citeseer:61055 | YES (available cells) |
| C1_COUNT_PARAM_MATCHED | 0.624237 ± 0.085967 (n=5) | PENDING / NOT RUN | PENDING / NOT RUN | cora:24810 | YES (available cells) |
| C2_CONSTANT_SET | PENDING / NOT RUN | 0.857205 ± 0.025185 (n=5) | PENDING / NOT RUN | pubmed:9882 | YES (available cells) |
| NCN | **0.848105 ± 0.006706 (n=5)** | *0.930320 ± 0.001863 (n=5)* | *0.869390 ± 0.007841 (n=5)* | cora:764163; pubmed:525315; citeseer:1411587 | YES (available cells) |
| NCNC | *0.843495 ± 0.006660 (n=5)* | **0.937093 ± 0.001874 (n=5)** | **0.885873 ± 0.004042 (n=5)** | cora:830212; pubmed:591364; citeseer:1477636 | YES (available cells) |
| NSLR-HMANN | 0.390938 ± 0.034778 (n=5) | 0.522645 ± 0.021630 (n=5) | 0.363857 ± 0.014862 (n=5) | cora:79393; pubmed:79393; citeseer:79393 | YES (available cells) |
| R-HSPE | 0.610054 ± 0.083963 (n=5) | 0.856064 ± 0.021902 (n=5) | 0.527320 ± 0.071749 (n=3) | cora:24810; pubmed:9882; citeseer:61130 | YES (available cells) |
