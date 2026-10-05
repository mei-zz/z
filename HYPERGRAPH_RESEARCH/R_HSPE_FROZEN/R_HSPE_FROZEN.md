# Innovation 1 freeze

{
  "INNOVATION_1": "R-HSPE",
  "STATUS": "FROZEN",
  "PRIMARY_CLAIM": "candidate-specific hyperedge-pair context encoding",
  "SECONDARY_COMPONENT": "training-only rank-normalized hyperedge cardinality",
  "MECHANISM_STATUS": "CONTEXT_DRIVEN",
  "SIZE_CAUSAL_CLAIM": "NOT_SUPPORTED",
  "CORA_VALIDATION": {
    "delta": {
      "mean": 0.14861508980960064,
      "std": 0.14390577719924127,
      "median": 0.0809394526845586,
      "min": 0.07528992253827149,
      "max": 0.4053371039325848,
      "per_seed": [
        0.0789853068958769,
        0.07528992253827149,
        0.10252366299671145,
        0.0809394526845586,
        0.4053371039325848
      ],
      "wins": 5
    },
    "passed": true
  },
  "PUBMED_VALIDATION": {
    "delta": {
      "mean": 0.013911610800480645,
      "std": 0.016321640627650104,
      "median": 0.01681292552596192,
      "min": -0.013592255367977368,
      "max": 0.02974273694377849,
      "per_seed": [
        0.01681292552596192,
        -0.013592255367977368,
        0.02974273694377849,
        0.020706682691379652,
        0.01588796420926053
      ],
      "wins": 4
    },
    "passed": true
  },
  "CORA_TEST": {
    "mean": 0.14411309043713388,
    "std": 0.1394484616195302,
    "median": 0.08275489536680869,
    "min": 0.06975503324852117,
    "max": 0.392860514949887,
    "per_seed": [
      0.08275489536680869,
      0.07696169524843721,
      0.09823331337201546,
      0.06975503324852117,
      0.392860514949887
    ],
    "wins": 5
  },
  "PUBMED_TEST": {
    "mean": 0.01294802474118606,
    "std": 0.011210075124593996,
    "median": 0.015533443089421395,
    "min": -0.0057782900056340125,
    "max": 0.02380919131187731,
    "per_seed": [
      0.012999340605981291,
      -0.0057782900056340125,
      0.02380919131187731,
      0.018176438704284315,
      0.015533443089421395
    ],
    "wins": 4
  },
  "THIRD_DATASET": {
    "dataset": "citeseer",
    "validation_delta": {
      "mean": 0.09417756010251109,
      "std": 0.07474225770860679,
      "median": 0.05751267253411929,
      "min": 0.04484783127838998,
      "max": 0.18017217649502398,
      "per_seed": [
        0.18017217649502398,
        0.04484783127838998,
        0.05751267253411929
      ],
      "wins": 3
    },
    "validation_seed_results": [
      {
        "state": "COMPLETE",
        "dataset": "citeseer",
        "seed": 0,
        "arms": {
          "B0_BASELINE": {
            "state": "COMPLETE",
            "dataset": "citeseer",
            "seed": 0,
            "epochs": 10,
            "arm": "B0_BASELINE",
            "test_evaluated": false,
            "validation_only": true,
            "validation_metrics": {
              "mrr": 0.3785243976089709,
              "hits10": 0.7444933920704846,
              "hits20": 0.986784140969163,
              "hits50": 1.0,
              "hits100": 1.0,
              "mean_positive_rank": 6.744493392070485
            },
            "checkpoint": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_2/third/citeseer/seed_0/arms/B0_BASELINE/checkpoints/citeseer_uniform_seed0_7edb93280ca0.pt",
            "checkpoint_sha256": "cf5af09ea3b7ecd186756e5e32b715b7551ee6a20be8453dda3f92190e286436",
            "execution_sources": {
              "v171": "b4b477d86ceb55f62cefb02ea1a652085b725ca92793707a29586976016970fc",
              "v17": "da20e41442f8e7b0b12d29515ba2a3df71a2a0a7327a51ea2b1170901e2e28bf",
              "v16_stage1": "f3b19889afa236fd71eeaa6681efc31c845eb32c4a90df87ab8d40092c196982",
              "stage0": "6d1f93ba8ab5ce0c99f584d1c38f1f44701c6c58ab19fbcc436b382eab0f1081",
              "qths_v71": "d8b1533b6398be98fe5741e5c485008c160434712c8d478268ae817b84b19f67",
              "negative_v61": "70b36c2d3b4f56a0b271b30e2bc60b360f99eb264368f22c4d095d1e421a7129",
              "codns_engine": "990c447435a0c1583c7df1bdb69d0a2493607eaf682afb9faf81738f4f9d0d67",
              "dcdlp_train": "1a51d4fecab93b75010def119946a91d4ed8ce44d3df852f167ca5400ac95f7d",
              "baseline_config": "9a5f4c2fb7cc8fab5179dca99e13b45445e1e17a2d23bae8ad3a924d1c47a76a"
            },
            "train_pool_hash": "e2b8d6babecc441e57b34fe2397238c9143e5a92786cf59affd0338c4015054f",
            "selected_negative_hash": "46f0edc0c1b63e02e347bb389b37881c51408cd3ba8079c4da8c4c73c759e1cc",
            "validation_candidate_hash": "d0d7a739d66ba5e5dc922dad3182959cc1a900484ca972984444d607e7cf2b82",
            "trainable_parameters": 61055,
            "added_parameters": 0,
            "train_seconds": 93.49881982523948,
            "validation_scoring_seconds": 3.6302808630280197,
            "wall_seconds": 97.73341315193102,
            "peak_gpu_allocated_mb": 80.15478515625,
            "checkpoint_rule": "fixed final epoch 10; no validation selection",
            "engine_cache_resumed": false
          },
          "H2_R_HSPE": {
            "state": "COMPLETE",
            "dataset": "citeseer",
            "seed": 0,
            "epochs": 10,
            "arm": "H2_R_HSPE",
            "test_evaluated": false,
            "validation_only": true,
            "validation_metrics": {
              "mrr": 0.5586965741039949,
              "hits10": 0.8237885462555066,
              "hits20": 0.9955947136563876,
              "hits50": 1.0,
              "hits100": 1.0,
              "mean_positive_rank": 4.889867841409692
            },
            "checkpoint": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_2/third/citeseer/seed_0/arms/H2_R_HSPE/checkpoints/citeseer_uniform_seed0_e3bb51b7b14b.pt",
            "checkpoint_sha256": "c1a0bf607c21cb1bdc67cecc475af9f29e9f380154a47abf0d08d0ce7fe01bbf",
            "execution_sources": {
              "v171": "b4b477d86ceb55f62cefb02ea1a652085b725ca92793707a29586976016970fc",
              "v17": "da20e41442f8e7b0b12d29515ba2a3df71a2a0a7327a51ea2b1170901e2e28bf",
              "v16_stage1": "f3b19889afa236fd71eeaa6681efc31c845eb32c4a90df87ab8d40092c196982",
              "stage0": "6d1f93ba8ab5ce0c99f584d1c38f1f44701c6c58ab19fbcc436b382eab0f1081",
              "qths_v71": "d8b1533b6398be98fe5741e5c485008c160434712c8d478268ae817b84b19f67",
              "negative_v61": "70b36c2d3b4f56a0b271b30e2bc60b360f99eb264368f22c4d095d1e421a7129",
              "codns_engine": "990c447435a0c1583c7df1bdb69d0a2493607eaf682afb9faf81738f4f9d0d67",
              "dcdlp_train": "1a51d4fecab93b75010def119946a91d4ed8ce44d3df852f167ca5400ac95f7d",
              "baseline_config": "9a5f4c2fb7cc8fab5179dca99e13b45445e1e17a2d23bae8ad3a924d1c47a76a"
            },
            "train_pool_hash": "e2b8d6babecc441e57b34fe2397238c9143e5a92786cf59affd0338c4015054f",
            "selected_negative_hash": "46f0edc0c1b63e02e347bb389b37881c51408cd3ba8079c4da8c4c73c759e1cc",
            "validation_candidate_hash": "d0d7a739d66ba5e5dc922dad3182959cc1a900484ca972984444d607e7cf2b82",
            "trainable_parameters": 61130,
            "added_parameters": 75,
            "train_seconds": 93.85875115124509,
            "validation_scoring_seconds": 3.1411249563097954,
            "wall_seconds": 97.59881294332445,
            "peak_gpu_allocated_mb": 96.21826171875,
            "checkpoint_rule": "fixed final epoch 10; no validation selection",
            "engine_cache_resumed": false
          }
        },
        "test_evaluated": false
      },
      {
        "state": "COMPLETE",
        "dataset": "citeseer",
        "seed": 1,
        "arms": {
          "B0_BASELINE": {
            "state": "COMPLETE",
            "dataset": "citeseer",
            "seed": 1,
            "epochs": 10,
            "arm": "B0_BASELINE",
            "test_evaluated": false,
            "validation_only": true,
            "validation_metrics": {
              "mrr": 0.5322855875509617,
              "hits10": 0.6607929515418502,
              "hits20": 0.9691629955947136,
              "hits50": 1.0,
              "hits100": 1.0,
              "mean_positive_rank": 6.964757709251101
            },
            "checkpoint": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_2/third/citeseer/seed_1/arms/B0_BASELINE/checkpoints/citeseer_uniform_seed1_98d4d1d91125.pt",
            "checkpoint_sha256": "5f80bdfd73dacce9ce462165dd17d5c232d503c5e2559a9f6d053052be433b3e",
            "execution_sources": {
              "v171": "b4b477d86ceb55f62cefb02ea1a652085b725ca92793707a29586976016970fc",
              "v17": "da20e41442f8e7b0b12d29515ba2a3df71a2a0a7327a51ea2b1170901e2e28bf",
              "v16_stage1": "f3b19889afa236fd71eeaa6681efc31c845eb32c4a90df87ab8d40092c196982",
              "stage0": "6d1f93ba8ab5ce0c99f584d1c38f1f44701c6c58ab19fbcc436b382eab0f1081",
              "qths_v71": "d8b1533b6398be98fe5741e5c485008c160434712c8d478268ae817b84b19f67",
              "negative_v61": "70b36c2d3b4f56a0b271b30e2bc60b360f99eb264368f22c4d095d1e421a7129",
              "codns_engine": "990c447435a0c1583c7df1bdb69d0a2493607eaf682afb9faf81738f4f9d0d67",
              "dcdlp_train": "1a51d4fecab93b75010def119946a91d4ed8ce44d3df852f167ca5400ac95f7d",
              "baseline_config": "9a5f4c2fb7cc8fab5179dca99e13b45445e1e17a2d23bae8ad3a924d1c47a76a"
            },
            "train_pool_hash": "e2b8d6babecc441e57b34fe2397238c9143e5a92786cf59affd0338c4015054f",
            "selected_negative_hash": "46f0edc0c1b63e02e347bb389b37881c51408cd3ba8079c4da8c4c73c759e1cc",
            "validation_candidate_hash": "d0d7a739d66ba5e5dc922dad3182959cc1a900484ca972984444d607e7cf2b82",
            "trainable_parameters": 61055,
            "added_parameters": 0,
            "train_seconds": 99.9708753619343,
            "validation_scoring_seconds": 4.152239528018981,
            "wall_seconds": 104.75995192117989,
            "peak_gpu_allocated_mb": 80.14990234375,
            "checkpoint_rule": "fixed final epoch 10; no validation selection",
            "engine_cache_resumed": false
          },
          "H2_R_HSPE": {
            "state": "COMPLETE",
            "dataset": "citeseer",
            "seed": 1,
            "epochs": 10,
            "arm": "H2_R_HSPE",
            "test_evaluated": false,
            "validation_only": true,
            "validation_metrics": {
              "mrr": 0.5771334188293517,
              "hits10": 0.8370044052863436,
              "hits20": 0.9911894273127754,
              "hits50": 1.0,
              "hits100": 1.0,
              "mean_positive_rank": 4.823788546255507
            },
            "checkpoint": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_2/third/citeseer/seed_1/arms/H2_R_HSPE/checkpoints/citeseer_uniform_seed1_331513a4e0a7.pt",
            "checkpoint_sha256": "d0ba4e77800437a35a2147b6cc6de496ddef2dbe42062d4de70927ed8aa5f7ba",
            "execution_sources": {
              "v171": "b4b477d86ceb55f62cefb02ea1a652085b725ca92793707a29586976016970fc",
              "v17": "da20e41442f8e7b0b12d29515ba2a3df71a2a0a7327a51ea2b1170901e2e28bf",
              "v16_stage1": "f3b19889afa236fd71eeaa6681efc31c845eb32c4a90df87ab8d40092c196982",
              "stage0": "6d1f93ba8ab5ce0c99f584d1c38f1f44701c6c58ab19fbcc436b382eab0f1081",
              "qths_v71": "d8b1533b6398be98fe5741e5c485008c160434712c8d478268ae817b84b19f67",
              "negative_v61": "70b36c2d3b4f56a0b271b30e2bc60b360f99eb264368f22c4d095d1e421a7129",
              "codns_engine": "990c447435a0c1583c7df1bdb69d0a2493607eaf682afb9faf81738f4f9d0d67",
              "dcdlp_train": "1a51d4fecab93b75010def119946a91d4ed8ce44d3df852f167ca5400ac95f7d",
              "baseline_config": "9a5f4c2fb7cc8fab5179dca99e13b45445e1e17a2d23bae8ad3a924d1c47a76a"
            },
            "train_pool_hash": "e2b8d6babecc441e57b34fe2397238c9143e5a92786cf59affd0338c4015054f",
            "selected_negative_hash": "46f0edc0c1b63e02e347bb389b37881c51408cd3ba8079c4da8c4c73c759e1cc",
            "validation_candidate_hash": "d0d7a739d66ba5e5dc922dad3182959cc1a900484ca972984444d607e7cf2b82",
            "trainable_parameters": 61130,
            "added_parameters": 75,
            "train_seconds": 95.50543097499758,
            "validation_scoring_seconds": 1.8538149623200297,
            "wall_seconds": 98.09598965896294,
            "peak_gpu_allocated_mb": 96.28857421875,
            "checkpoint_rule": "fixed final epoch 10; no validation selection",
            "engine_cache_resumed": false
          }
        },
        "test_evaluated": false
      },
      {
        "state": "COMPLETE",
        "dataset": "citeseer",
        "seed": 2,
        "arms": {
          "B0_BASELINE": {
            "state": "COMPLETE",
            "dataset": "citeseer",
            "seed": 2,
            "epochs": 10,
            "arm": "B0_BASELINE",
            "test_evaluated": false,
            "validation_only": true,
            "validation_metrics": {
              "mrr": 0.3656083691798221,
              "hits10": 0.8149779735682819,
              "hits20": 1.0,
              "hits50": 1.0,
              "hits100": 1.0,
              "mean_positive_rank": 5.841409691629956
            },
            "checkpoint": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_2/third/citeseer/seed_2/arms/B0_BASELINE/checkpoints/citeseer_uniform_seed2_41b36809a8c4.pt",
            "checkpoint_sha256": "deff728091bc56f2bbdf5c908b4bc88765080c711a73d3a15d3ee9a13be230c3",
            "execution_sources": {
              "v171": "b4b477d86ceb55f62cefb02ea1a652085b725ca92793707a29586976016970fc",
              "v17": "da20e41442f8e7b0b12d29515ba2a3df71a2a0a7327a51ea2b1170901e2e28bf",
              "v16_stage1": "f3b19889afa236fd71eeaa6681efc31c845eb32c4a90df87ab8d40092c196982",
              "stage0": "6d1f93ba8ab5ce0c99f584d1c38f1f44701c6c58ab19fbcc436b382eab0f1081",
              "qths_v71": "d8b1533b6398be98fe5741e5c485008c160434712c8d478268ae817b84b19f67",
              "negative_v61": "70b36c2d3b4f56a0b271b30e2bc60b360f99eb264368f22c4d095d1e421a7129",
              "codns_engine": "990c447435a0c1583c7df1bdb69d0a2493607eaf682afb9faf81738f4f9d0d67",
              "dcdlp_train": "1a51d4fecab93b75010def119946a91d4ed8ce44d3df852f167ca5400ac95f7d",
              "baseline_config": "9a5f4c2fb7cc8fab5179dca99e13b45445e1e17a2d23bae8ad3a924d1c47a76a"
            },
            "train_pool_hash": "e2b8d6babecc441e57b34fe2397238c9143e5a92786cf59affd0338c4015054f",
            "selected_negative_hash": "46f0edc0c1b63e02e347bb389b37881c51408cd3ba8079c4da8c4c73c759e1cc",
            "validation_candidate_hash": "d0d7a739d66ba5e5dc922dad3182959cc1a900484ca972984444d607e7cf2b82",
            "trainable_parameters": 61055,
            "added_parameters": 0,
            "train_seconds": 93.25360247958452,
            "validation_scoring_seconds": 3.452294667251408,
            "wall_seconds": 97.28835052996874,
            "peak_gpu_allocated_mb": 80.15478515625,
            "checkpoint_rule": "fixed final epoch 10; no validation selection",
            "engine_cache_resumed": false
          },
          "H2_R_HSPE": {
            "state": "COMPLETE",
            "dataset": "citeseer",
            "seed": 2,
            "epochs": 10,
            "arm": "H2_R_HSPE",
            "test_evaluated": false,
            "validation_only": true,
            "validation_metrics": {
              "mrr": 0.4231210417139414,
              "hits10": 0.8942731277533039,
              "hits20": 1.0,
              "hits50": 1.0,
              "hits100": 1.0,
              "mean_positive_rank": 4.755506607929515
            },
            "checkpoint": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_2/third/citeseer/seed_2/arms/H2_R_HSPE/checkpoints/citeseer_uniform_seed2_95716699a3d4.pt",
            "checkpoint_sha256": "2dedf8e2f82d806c42214d8ef25d6c878a413b869916a7a6be6a11dd581a7021",
            "execution_sources": {
              "v171": "b4b477d86ceb55f62cefb02ea1a652085b725ca92793707a29586976016970fc",
              "v17": "da20e41442f8e7b0b12d29515ba2a3df71a2a0a7327a51ea2b1170901e2e28bf",
              "v16_stage1": "f3b19889afa236fd71eeaa6681efc31c845eb32c4a90df87ab8d40092c196982",
              "stage0": "6d1f93ba8ab5ce0c99f584d1c38f1f44701c6c58ab19fbcc436b382eab0f1081",
              "qths_v71": "d8b1533b6398be98fe5741e5c485008c160434712c8d478268ae817b84b19f67",
              "negative_v61": "70b36c2d3b4f56a0b271b30e2bc60b360f99eb264368f22c4d095d1e421a7129",
              "codns_engine": "990c447435a0c1583c7df1bdb69d0a2493607eaf682afb9faf81738f4f9d0d67",
              "dcdlp_train": "1a51d4fecab93b75010def119946a91d4ed8ce44d3df852f167ca5400ac95f7d",
              "baseline_config": "9a5f4c2fb7cc8fab5179dca99e13b45445e1e17a2d23bae8ad3a924d1c47a76a"
            },
            "train_pool_hash": "e2b8d6babecc441e57b34fe2397238c9143e5a92786cf59affd0338c4015054f",
            "selected_negative_hash": "46f0edc0c1b63e02e347bb389b37881c51408cd3ba8079c4da8c4c73c759e1cc",
            "validation_candidate_hash": "d0d7a739d66ba5e5dc922dad3182959cc1a900484ca972984444d607e7cf2b82",
            "trainable_parameters": 61130,
            "added_parameters": 75,
            "train_seconds": 92.61077039083466,
            "validation_scoring_seconds": 3.6320600868202746,
            "wall_seconds": 96.845132261049,
            "peak_gpu_allocated_mb": 96.31982421875,
            "checkpoint_rule": "fixed final epoch 10; no validation selection",
            "engine_cache_resumed": false
          }
        },
        "test_evaluated": false
      }
    ],
    "test_evaluated": true,
    "status": "THIRD_DATASET_VALIDATION_SUPPORTED",
    "test_delta": {
      "mean": 0.0887476626284336,
      "std": 0.06971405298714303,
      "median": 0.051092264685382194,
      "min": 0.045958785597985496,
      "max": 0.16919193760193313,
      "per_seed": [
        0.16919193760193313,
        0.045958785597985496,
        0.051092264685382194
      ],
      "wins": 3
    },
    "test_seed_results": [
      {
        "state": "COMPLETE",
        "dataset": "citeseer",
        "seed": 0,
        "arms": {
          "B0_BASELINE": {
            "state": "COMPLETE",
            "arm": "B0_BASELINE",
            "seed": 0,
            "dataset": "citeseer",
            "split": "test",
            "metrics": {
              "mrr": 0.3740331028460005,
              "hits10": 0.6725274725274726,
              "hits20": 0.9956043956043956,
              "hits50": 1.0,
              "hits100": 1.0,
              "mean_positive_rank": 7.3780219780219785
            },
            "checkpoint": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_2/third/citeseer/seed_0/arms/B0_BASELINE/checkpoints/citeseer_uniform_seed0_7edb93280ca0.pt",
            "checkpoint_sha256": "cf5af09ea3b7ecd186756e5e32b715b7551ee6a20be8453dda3f92190e286436",
            "parameters": 61055,
            "scoring_seconds": 6.574888196773827,
            "peak_gpu_allocated_mb": 67.46630859375,
            "evaluator_sources": {
              "v16_stage1": "f3b19889afa236fd71eeaa6681efc31c845eb32c4a90df87ab8d40092c196982",
              "stage0": "6d1f93ba8ab5ce0c99f584d1c38f1f44701c6c58ab19fbcc436b382eab0f1081",
              "qths_v71": "d8b1533b6398be98fe5741e5c485008c160434712c8d478268ae817b84b19f67",
              "negative_v61": "70b36c2d3b4f56a0b271b30e2bc60b360f99eb264368f22c4d095d1e421a7129",
              "codns_engine": "990c447435a0c1583c7df1bdb69d0a2493607eaf682afb9faf81738f4f9d0d67",
              "dcdlp_train": "1a51d4fecab93b75010def119946a91d4ed8ce44d3df852f167ca5400ac95f7d",
              "baseline_config": "9a5f4c2fb7cc8fab5179dca99e13b45445e1e17a2d23bae8ad3a924d1c47a76a"
            },
            "fixed_final_epoch": 10,
            "test_guided_change": false
          },
          "H2_R_HSPE": {
            "state": "COMPLETE",
            "arm": "H2_R_HSPE",
            "seed": 0,
            "dataset": "citeseer",
            "split": "test",
            "metrics": {
              "mrr": 0.5432250404479336,
              "hits10": 0.7736263736263737,
              "hits20": 0.9978021978021978,
              "hits50": 1.0,
              "hits100": 1.0,
              "mean_positive_rank": 5.29010989010989
            },
            "checkpoint": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_2/third/citeseer/seed_0/arms/H2_R_HSPE/checkpoints/citeseer_uniform_seed0_e3bb51b7b14b.pt",
            "checkpoint_sha256": "c1a0bf607c21cb1bdc67cecc475af9f29e9f380154a47abf0d08d0ce7fe01bbf",
            "parameters": 61130,
            "scoring_seconds": 6.169005166739225,
            "peak_gpu_allocated_mb": 67.46826171875,
            "evaluator_sources": {
              "v16_stage1": "f3b19889afa236fd71eeaa6681efc31c845eb32c4a90df87ab8d40092c196982",
              "stage0": "6d1f93ba8ab5ce0c99f584d1c38f1f44701c6c58ab19fbcc436b382eab0f1081",
              "qths_v71": "d8b1533b6398be98fe5741e5c485008c160434712c8d478268ae817b84b19f67",
              "negative_v61": "70b36c2d3b4f56a0b271b30e2bc60b360f99eb264368f22c4d095d1e421a7129",
              "codns_engine": "990c447435a0c1583c7df1bdb69d0a2493607eaf682afb9faf81738f4f9d0d67",
              "dcdlp_train": "1a51d4fecab93b75010def119946a91d4ed8ce44d3df852f167ca5400ac95f7d",
              "baseline_config": "9a5f4c2fb7cc8fab5179dca99e13b45445e1e17a2d23bae8ad3a924d1c47a76a"
            },
            "fixed_final_epoch": 10,
            "test_guided_change": false
          }
        }
      },
      {
        "state": "COMPLETE",
        "dataset": "citeseer",
        "seed": 1,
        "arms": {
          "B0_BASELINE": {
            "state": "COMPLETE",
            "arm": "B0_BASELINE",
            "seed": 1,
            "dataset": "citeseer",
            "split": "test",
            "metrics": {
              "mrr": 0.5438224737154754,
              "hits10": 0.6879120879120879,
              "hits20": 0.9516483516483516,
              "hits50": 1.0,
              "hits100": 1.0,
              "mean_positive_rank": 7.008791208791209
            },
            "checkpoint": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_2/third/citeseer/seed_1/arms/B0_BASELINE/checkpoints/citeseer_uniform_seed1_98d4d1d91125.pt",
            "checkpoint_sha256": "5f80bdfd73dacce9ce462165dd17d5c232d503c5e2559a9f6d053052be433b3e",
            "parameters": 61055,
            "scoring_seconds": 6.508563002105802,
            "peak_gpu_allocated_mb": 67.46630859375,
            "evaluator_sources": {
              "v16_stage1": "f3b19889afa236fd71eeaa6681efc31c845eb32c4a90df87ab8d40092c196982",
              "stage0": "6d1f93ba8ab5ce0c99f584d1c38f1f44701c6c58ab19fbcc436b382eab0f1081",
              "qths_v71": "d8b1533b6398be98fe5741e5c485008c160434712c8d478268ae817b84b19f67",
              "negative_v61": "70b36c2d3b4f56a0b271b30e2bc60b360f99eb264368f22c4d095d1e421a7129",
              "codns_engine": "990c447435a0c1583c7df1bdb69d0a2493607eaf682afb9faf81738f4f9d0d67",
              "dcdlp_train": "1a51d4fecab93b75010def119946a91d4ed8ce44d3df852f167ca5400ac95f7d",
              "baseline_config": "9a5f4c2fb7cc8fab5179dca99e13b45445e1e17a2d23bae8ad3a924d1c47a76a"
            },
            "fixed_final_epoch": 10,
            "test_guided_change": false
          },
          "H2_R_HSPE": {
            "state": "COMPLETE",
            "arm": "H2_R_HSPE",
            "seed": 1,
            "dataset": "citeseer",
            "split": "test",
            "metrics": {
              "mrr": 0.5897812593134609,
              "hits10": 0.832967032967033,
              "hits20": 0.989010989010989,
              "hits50": 1.0,
              "hits100": 1.0,
              "mean_positive_rank": 4.778021978021978
            },
            "checkpoint": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_2/third/citeseer/seed_1/arms/H2_R_HSPE/checkpoints/citeseer_uniform_seed1_331513a4e0a7.pt",
            "checkpoint_sha256": "d0ba4e77800437a35a2147b6cc6de496ddef2dbe42062d4de70927ed8aa5f7ba",
            "parameters": 61130,
            "scoring_seconds": 6.140183099079877,
            "peak_gpu_allocated_mb": 67.46826171875,
            "evaluator_sources": {
              "v16_stage1": "f3b19889afa236fd71eeaa6681efc31c845eb32c4a90df87ab8d40092c196982",
              "stage0": "6d1f93ba8ab5ce0c99f584d1c38f1f44701c6c58ab19fbcc436b382eab0f1081",
              "qths_v71": "d8b1533b6398be98fe5741e5c485008c160434712c8d478268ae817b84b19f67",
              "negative_v61": "70b36c2d3b4f56a0b271b30e2bc60b360f99eb264368f22c4d095d1e421a7129",
              "codns_engine": "990c447435a0c1583c7df1bdb69d0a2493607eaf682afb9faf81738f4f9d0d67",
              "dcdlp_train": "1a51d4fecab93b75010def119946a91d4ed8ce44d3df852f167ca5400ac95f7d",
              "baseline_config": "9a5f4c2fb7cc8fab5179dca99e13b45445e1e17a2d23bae8ad3a924d1c47a76a"
            },
            "fixed_final_epoch": 10,
            "test_guided_change": false
          }
        }
      },
      {
        "state": "COMPLETE",
        "dataset": "citeseer",
        "seed": 2,
        "arms": {
          "B0_BASELINE": {
            "state": "COMPLETE",
            "arm": "B0_BASELINE",
            "seed": 2,
            "dataset": "citeseer",
            "split": "test",
            "metrics": {
              "mrr": 0.39786021521123327,
              "hits10": 0.8285714285714286,
              "hits20": 0.9934065934065934,
              "hits50": 1.0,
              "hits100": 1.0,
              "mean_positive_rank": 5.849450549450549
            },
            "checkpoint": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_2/third/citeseer/seed_2/arms/B0_BASELINE/checkpoints/citeseer_uniform_seed2_41b36809a8c4.pt",
            "checkpoint_sha256": "deff728091bc56f2bbdf5c908b4bc88765080c711a73d3a15d3ee9a13be230c3",
            "parameters": 61055,
            "scoring_seconds": 7.073733669240028,
            "peak_gpu_allocated_mb": 67.46630859375,
            "evaluator_sources": {
              "v16_stage1": "f3b19889afa236fd71eeaa6681efc31c845eb32c4a90df87ab8d40092c196982",
              "stage0": "6d1f93ba8ab5ce0c99f584d1c38f1f44701c6c58ab19fbcc436b382eab0f1081",
              "qths_v71": "d8b1533b6398be98fe5741e5c485008c160434712c8d478268ae817b84b19f67",
              "negative_v61": "70b36c2d3b4f56a0b271b30e2bc60b360f99eb264368f22c4d095d1e421a7129",
              "codns_engine": "990c447435a0c1583c7df1bdb69d0a2493607eaf682afb9faf81738f4f9d0d67",
              "dcdlp_train": "1a51d4fecab93b75010def119946a91d4ed8ce44d3df852f167ca5400ac95f7d",
              "baseline_config": "9a5f4c2fb7cc8fab5179dca99e13b45445e1e17a2d23bae8ad3a924d1c47a76a"
            },
            "fixed_final_epoch": 10,
            "test_guided_change": false
          },
          "H2_R_HSPE": {
            "state": "COMPLETE",
            "arm": "H2_R_HSPE",
            "seed": 2,
            "dataset": "citeseer",
            "split": "test",
            "metrics": {
              "mrr": 0.44895247989661546,
              "hits10": 0.8813186813186813,
              "hits20": 0.9934065934065934,
              "hits50": 1.0,
              "hits100": 1.0,
              "mean_positive_rank": 4.93956043956044
            },
            "checkpoint": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_2/third/citeseer/seed_2/arms/H2_R_HSPE/checkpoints/citeseer_uniform_seed2_95716699a3d4.pt",
            "checkpoint_sha256": "2dedf8e2f82d806c42214d8ef25d6c878a413b869916a7a6be6a11dd581a7021",
            "parameters": 61130,
            "scoring_seconds": 6.290785351768136,
            "peak_gpu_allocated_mb": 67.46826171875,
            "evaluator_sources": {
              "v16_stage1": "f3b19889afa236fd71eeaa6681efc31c845eb32c4a90df87ab8d40092c196982",
              "stage0": "6d1f93ba8ab5ce0c99f584d1c38f1f44701c6c58ab19fbcc436b382eab0f1081",
              "qths_v71": "d8b1533b6398be98fe5741e5c485008c160434712c8d478268ae817b84b19f67",
              "negative_v61": "70b36c2d3b4f56a0b271b30e2bc60b360f99eb264368f22c4d095d1e421a7129",
              "codns_engine": "990c447435a0c1583c7df1bdb69d0a2493607eaf682afb9faf81738f4f9d0d67",
              "dcdlp_train": "1a51d4fecab93b75010def119946a91d4ed8ce44d3df852f167ca5400ac95f7d",
              "baseline_config": "9a5f4c2fb7cc8fab5179dca99e13b45445e1e17a2d23bae8ad3a924d1c47a76a"
            },
            "fixed_final_epoch": 10,
            "test_guided_change": false
          }
        }
      }
    ]
  },
  "PARAMETER_OVERHEAD": 75,
  "NOVELTY_STATUS": "NO_EXACT_COLLISION_IDENTIFIED_IN_FOCUSED_AUDIT",
  "CODE_HASH": {
    "v171": "b4b477d86ceb55f62cefb02ea1a652085b725ca92793707a29586976016970fc",
    "v17": "da20e41442f8e7b0b12d29515ba2a3df71a2a0a7327a51ea2b1170901e2e28bf",
    "v16_stage1": "f3b19889afa236fd71eeaa6681efc31c845eb32c4a90df87ab8d40092c196982",
    "stage0": "6d1f93ba8ab5ce0c99f584d1c38f1f44701c6c58ab19fbcc436b382eab0f1081",
    "qths_v71": "d8b1533b6398be98fe5741e5c485008c160434712c8d478268ae817b84b19f67",
    "negative_v61": "70b36c2d3b4f56a0b271b30e2bc60b360f99eb264368f22c4d095d1e421a7129",
    "codns_engine": "990c447435a0c1583c7df1bdb69d0a2493607eaf682afb9faf81738f4f9d0d67",
    "dcdlp_train": "1a51d4fecab93b75010def119946a91d4ed8ce44d3df852f167ca5400ac95f7d",
    "baseline_config": "9a5f4c2fb7cc8fab5179dca99e13b45445e1e17a2d23bae8ad3a924d1c47a76a"
  },
  "CONFIG_HASH": "22a208039ad9ff41c4c11c8ee84e376e5138662bac8d63bbfd064bf0e2b37d7b",
  "NO_FURTHER_TUNING": true,
  "SECOND_INNOVATION_BASELINE_ARMS": {
    "B0": "frozen original baseline",
    "B1": "frozen R-HSPE",
    "B2": "Innovation2 only",
    "B3": "R-HSPE+Innovation2"
  },
  "INNOVATION2_STARTED": false
}