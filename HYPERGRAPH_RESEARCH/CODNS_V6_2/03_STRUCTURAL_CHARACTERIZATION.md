# Structural Characterization

Descriptive statistics use only the Cora training graph and selected train negatives. No future-positive enrichment analysis is performed.

```json
{
  "M1_HG_low": {
    "common_neighbors": {
      "mean": 0.18114973262032086,
      "median": 0.0
    },
    "adamic_adar": {
      "mean": 0.0670808294694322,
      "median": 0.0
    },
    "resource_allocation": {
      "mean": 0.013951307019304918,
      "median": 0.0
    },
    "jaccard": {
      "mean": 0.029829675695060766,
      "median": 0.0
    },
    "degree_u": {
      "mean": 5.561497326203209,
      "median": 5.0
    },
    "degree_v": {
      "mean": 5.557486631016043,
      "median": 5.0
    },
    "degree_product": {
      "mean": 35.40151515151515,
      "median": 24.0
    },
    "raw_star_shared_hyperedge_count": {
      "mean": 0.18114973262032086,
      "median": 0.0
    },
    "raw_star_overlap_strength": {
      "mean": 0.021049517460733566,
      "median": 0.0
    },
    "shortest_path_counts": {
      "1-hop": 0,
      "2-hop": 756,
      "3-hop": 231,
      ">3": 3349,
      "disconnected": 152
    },
    "unique_pair_ratio": 1.0,
    "unique_endpoint_ratio": 0.18081550802139038,
    "mean_Rg": 0.9521024227502127,
    "median_Rg": 0.9662819327309796,
    "mean_Rh": 0.9376677831640238
  },
  "M3_HG_high": {
    "common_neighbors": {
      "mean": 0.18315508021390375,
      "median": 0.0
    },
    "adamic_adar": {
      "mean": 0.067628203318364,
      "median": 0.0
    },
    "resource_allocation": {
      "mean": 0.014011588473675016,
      "median": 0.0
    },
    "jaccard": {
      "mean": 0.030270810727738157,
      "median": 0.0
    },
    "degree_u": {
      "mean": 5.579099821746881,
      "median": 5.0
    },
    "degree_v": {
      "mean": 5.571301247771836,
      "median": 5.0
    },
    "degree_product": {
      "mean": 35.6695632798574,
      "median": 24.0
    },
    "raw_star_shared_hyperedge_count": {
      "mean": 0.18315508021390375,
      "median": 0.0
    },
    "raw_star_overlap_strength": {
      "mean": 0.021347711954560863,
      "median": 0.0
    },
    "shortest_path_counts": {
      "1-hop": 0,
      "2-hop": 764,
      "3-hop": 237,
      ">3": 3340,
      "disconnected": 147
    },
    "unique_pair_ratio": 1.0,
    "unique_endpoint_ratio": 0.17736185383244207,
    "mean_Rg": 0.9523123903245051,
    "median_Rg": 0.9662596508428125,
    "mean_Rh": 0.9429329441867099
  },
  "interpretation_limit": "Descriptive train-graph structure only; no future-positive or false-negative enrichment analysis was run."
}
```
