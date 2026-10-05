# Validation-negative quadrant analysis

Negative matrix hash: aca455fc094f2b037a812d62a4fcb79fd8d48102d021d72418aea1ab0b65b455  
Positive-plus-negative candidate tensor hash: 197912d7397d8d8e118e2c985ff2a7948810c8b96ab5bed91e49c598aa481d48

Quadrants are split within each validation query: 20 candidates, top 10 by frozen Graph score and top 10 by frozen Raw-HG score are high. Counts and interference use each final arm model. This is a rank diagnostic, not false-negative ground truth.

## A0

| Quadrant | Count | Mean Graph score | Mean HG score | Mean final score | Negatives outranking positive | Queries with any outranker | Mean outrankers/query | Mean positive-negative margin |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Q1_Graph_high_HG_high | 2012 | -0.105676 | -0.001657 | -0.001657 | 0.4702 | 0.5779 | 3.5970 | 0.256245 |
| Q2_Graph_high_HG_low | 618 | -0.131552 | -0.098684 | -0.098684 | 0.2039 | 0.2738 | 0.4791 | 0.377556 |
| Q3_Graph_low_HG_high | 618 | -0.167197 | -0.052439 | -0.052439 | 0.3673 | 0.4259 | 0.8631 | 0.331311 |
| Q4_Graph_low_HG_low | 2012 | -0.188490 | -0.117746 | -0.117746 | 0.1754 | 0.3118 | 1.3422 | 0.372334 |

Fixed-candidate MRR: 0.503012005; hard Graph-tertile MRR: 0.107957613; validation mean pair margin: 0.323723; selected-train mean margin: -0.029279.

## A1

| Quadrant | Count | Mean Graph score | Mean HG score | Mean final score | Negatives outranking positive | Queries with any outranker | Mean outrankers/query | Mean positive-negative margin |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Q1_Graph_high_HG_high | 2012 | -0.105676 | -0.001657 | -0.127963 | 0.3867 | 0.4943 | 2.9582 | 0.096846 |
| Q2_Graph_high_HG_low | 618 | -0.131552 | -0.098684 | -0.129185 | 0.3738 | 0.4335 | 0.8783 | 0.105920 |
| Q3_Graph_low_HG_high | 618 | -0.167197 | -0.052439 | -0.168179 | 0.2524 | 0.2928 | 0.5932 | 0.144915 |
| Q4_Graph_low_HG_low | 2012 | -0.188490 | -0.117746 | -0.170382 | 0.2440 | 0.4601 | 1.8669 | 0.139265 |

Fixed-candidate MRR: 0.533444582; hard Graph-tertile MRR: 0.157264241; validation mean pair margin: 0.119786; selected-train mean margin: 0.061340.

## A2

| Quadrant | Count | Mean Graph score | Mean HG score | Mean final score | Negatives outranking positive | Queries with any outranker | Mean outrankers/query | Mean positive-negative margin |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Q1_Graph_high_HG_high | 2012 | -0.105676 | -0.001657 | -0.132279 | 0.3882 | 0.4981 | 2.9696 | 0.099423 |
| Q2_Graph_high_HG_low | 618 | -0.131552 | -0.098684 | -0.136252 | 0.3722 | 0.4259 | 0.8745 | 0.111925 |
| Q3_Graph_low_HG_high | 618 | -0.167197 | -0.052439 | -0.172569 | 0.2443 | 0.2928 | 0.5741 | 0.148241 |
| Q4_Graph_low_HG_low | 2012 | -0.188490 | -0.117746 | -0.176918 | 0.2425 | 0.4563 | 1.8555 | 0.144062 |

Fixed-candidate MRR: 0.535584316; hard Graph-tertile MRR: 0.158224179; validation mean pair margin: 0.123702; selected-train mean margin: 0.075838.

## A3

| Quadrant | Count | Mean Graph score | Mean HG score | Mean final score | Negatives outranking positive | Queries with any outranker | Mean outrankers/query | Mean positive-negative margin |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Q1_Graph_high_HG_high | 2012 | -0.105676 | -0.001657 | -0.104401 | 0.3698 | 0.4905 | 2.8289 | 0.193287 |
| Q2_Graph_high_HG_low | 618 | -0.131552 | -0.098684 | -0.108551 | 0.3608 | 0.4068 | 0.8479 | 0.211329 |
| Q3_Graph_low_HG_high | 618 | -0.167197 | -0.052439 | -0.140805 | 0.2411 | 0.2966 | 0.5665 | 0.243582 |
| Q4_Graph_low_HG_low | 2012 | -0.188490 | -0.117746 | -0.141630 | 0.2416 | 0.4563 | 1.8479 | 0.230516 |

Fixed-candidate MRR: 0.536448230; hard Graph-tertile MRR: 0.181907980; validation mean pair margin: 0.215556; selected-train mean margin: 0.069067.

## A4

| Quadrant | Count | Mean Graph score | Mean HG score | Mean final score | Negatives outranking positive | Queries with any outranker | Mean outrankers/query | Mean positive-negative margin |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Q1_Graph_high_HG_high | 2012 | -0.105676 | -0.001657 | -0.030695 | 0.3280 | 0.5323 | 2.5095 | 0.276808 |
| Q2_Graph_high_HG_low | 618 | -0.131552 | -0.098684 | -0.071072 | 0.1909 | 0.2624 | 0.4487 | 0.339039 |
| Q3_Graph_low_HG_high | 618 | -0.167197 | -0.052439 | -0.048262 | 0.2686 | 0.3726 | 0.6312 | 0.316229 |
| Q4_Graph_low_HG_low | 2012 | -0.188490 | -0.117746 | -0.078298 | 0.2048 | 0.3992 | 1.5665 | 0.324411 |

Fixed-candidate MRR: 0.540428304; hard Graph-tertile MRR: 0.200325615; validation mean pair margin: 0.306960; selected-train mean margin: 0.059698.

## A5

| Quadrant | Count | Mean Graph score | Mean HG score | Mean final score | Negatives outranking positive | Queries with any outranker | Mean outrankers/query | Mean positive-negative margin |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Q1_Graph_high_HG_high | 2012 | -0.105676 | -0.001657 | -0.145697 | 0.3593 | 0.4753 | 2.7490 | 0.144862 |
| Q2_Graph_high_HG_low | 618 | -0.131552 | -0.098684 | -0.123270 | 0.3819 | 0.4221 | 0.8973 | 0.130822 |
| Q3_Graph_low_HG_high | 618 | -0.167197 | -0.052439 | -0.186815 | 0.2330 | 0.2814 | 0.5475 | 0.194368 |
| Q4_Graph_low_HG_low | 2012 | -0.188490 | -0.117746 | -0.172153 | 0.2624 | 0.4677 | 2.0076 | 0.171319 |

Fixed-candidate MRR: 0.536054530; hard Graph-tertile MRR: 0.198935365; validation mean pair margin: 0.159149; selected-train mean margin: 0.156232.
