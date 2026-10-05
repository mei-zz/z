{
  "datasets": {
    "cora": {
      "seed_results": [
        {
          "state": "COMPLETE",
          "dataset": "cora",
          "seed": 0,
          "epochs": 10,
          "arms": {
            "H2_R_HSPE": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 0,
              "epochs": 10,
              "arm": "H2_R_HSPE",
              "test_evaluated": false,
              "validation_only": true,
              "validation_metrics": {
                "mrr": 0.6158931787023348,
                "hits10": 0.8859315589353612,
                "hits20": 0.9581749049429658,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 3.958174904942966
              },
              "checkpoint": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_1/experiments/phase_rank/cora/seed_0/arms/H2_R_HSPE/checkpoints/cora_uniform_seed0_bbcad8664812.pt",
              "checkpoint_sha256": "64df1e4dbc698499dc026f9f71aebf5ca3a78374637bcd5c76482d8ebb8a82c5",
              "execution_sources": {
                "v171": "94eae10a845b3f4930edc776d0e9b18c104c9f40e0ae7dc7d93b6fe875cab4c3",
                "v17": "da20e41442f8e7b0b12d29515ba2a3df71a2a0a7327a51ea2b1170901e2e28bf",
                "v16_stage1": "f3b19889afa236fd71eeaa6681efc31c845eb32c4a90df87ab8d40092c196982",
                "stage0": "6d1f93ba8ab5ce0c99f584d1c38f1f44701c6c58ab19fbcc436b382eab0f1081",
                "qths_v71": "d8b1533b6398be98fe5741e5c485008c160434712c8d478268ae817b84b19f67",
                "negative_v61": "70b36c2d3b4f56a0b271b30e2bc60b360f99eb264368f22c4d095d1e421a7129",
                "codns_engine": "990c447435a0c1583c7df1bdb69d0a2493607eaf682afb9faf81738f4f9d0d67",
                "dcdlp_train": "1a51d4fecab93b75010def119946a91d4ed8ce44d3df852f167ca5400ac95f7d",
                "baseline_config": "9a5f4c2fb7cc8fab5179dca99e13b45445e1e17a2d23bae8ad3a924d1c47a76a"
              },
              "train_pool_hash": "3d1e3ea691fc19fab65d66ad278d169cf099eb831ad0e46a439510ff5d07a7ba",
              "selected_negative_hash": "1ada7e01d1b3fa788db9d8312167290d4191344ace2db40bb787ab78e027c758",
              "validation_candidate_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
              "trainable_parameters": 24810,
              "added_parameters": 75,
              "train_seconds": 151.4461280098185,
              "validation_scoring_seconds": 4.174337842036039,
              "wall_seconds": 156.07249056361616,
              "peak_gpu_allocated_mb": 70.65576171875,
              "checkpoint_rule": "fixed final epoch 10; no validation selection",
              "engine_cache_resumed": false
            }
          },
          "mrr": {
            "H2_R_HSPE": 0.6158931787023348
          },
          "feature_metadata_path": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_1/features/cora/metadata.json",
          "test_evaluated": false
        },
        {
          "state": "COMPLETE",
          "dataset": "cora",
          "seed": 1,
          "epochs": 10,
          "arms": {
            "H2_R_HSPE": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 1,
              "epochs": 10,
              "arm": "H2_R_HSPE",
              "test_evaluated": false,
              "validation_only": true,
              "validation_metrics": {
                "mrr": 0.45382466680716216,
                "hits10": 0.8479087452471483,
                "hits20": 0.9961977186311787,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 5.1254752851711025
              },
              "checkpoint": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_1/experiments/phase_rank/cora/seed_1/arms/H2_R_HSPE/checkpoints/cora_uniform_seed1_58b81712312a.pt",
              "checkpoint_sha256": "be608751f6d3e65fbf291e59c6168388a6e1cd0bd2be27bee45e5de1f5b86423",
              "execution_sources": {
                "v171": "94eae10a845b3f4930edc776d0e9b18c104c9f40e0ae7dc7d93b6fe875cab4c3",
                "v17": "da20e41442f8e7b0b12d29515ba2a3df71a2a0a7327a51ea2b1170901e2e28bf",
                "v16_stage1": "f3b19889afa236fd71eeaa6681efc31c845eb32c4a90df87ab8d40092c196982",
                "stage0": "6d1f93ba8ab5ce0c99f584d1c38f1f44701c6c58ab19fbcc436b382eab0f1081",
                "qths_v71": "d8b1533b6398be98fe5741e5c485008c160434712c8d478268ae817b84b19f67",
                "negative_v61": "70b36c2d3b4f56a0b271b30e2bc60b360f99eb264368f22c4d095d1e421a7129",
                "codns_engine": "990c447435a0c1583c7df1bdb69d0a2493607eaf682afb9faf81738f4f9d0d67",
                "dcdlp_train": "1a51d4fecab93b75010def119946a91d4ed8ce44d3df852f167ca5400ac95f7d",
                "baseline_config": "9a5f4c2fb7cc8fab5179dca99e13b45445e1e17a2d23bae8ad3a924d1c47a76a"
              },
              "train_pool_hash": "3d1e3ea691fc19fab65d66ad278d169cf099eb831ad0e46a439510ff5d07a7ba",
              "selected_negative_hash": "1ada7e01d1b3fa788db9d8312167290d4191344ace2db40bb787ab78e027c758",
              "validation_candidate_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
              "trainable_parameters": 24810,
              "added_parameters": 75,
              "train_seconds": 141.31588681973517,
              "validation_scoring_seconds": 5.023791825864464,
              "wall_seconds": 146.79871247708797,
              "peak_gpu_allocated_mb": 70.4775390625,
              "checkpoint_rule": "fixed final epoch 10; no validation selection",
              "engine_cache_resumed": false
            }
          },
          "mrr": {
            "H2_R_HSPE": 0.45382466680716216
          },
          "feature_metadata_path": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_1/features/cora/metadata.json",
          "test_evaluated": false
        },
        {
          "state": "COMPLETE",
          "dataset": "cora",
          "seed": 2,
          "epochs": 10,
          "arms": {
            "H2_R_HSPE": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 2,
              "epochs": 10,
              "arm": "H2_R_HSPE",
              "test_evaluated": false,
              "validation_only": true,
              "validation_metrics": {
                "mrr": 0.6260422298445112,
                "hits10": 0.9429657794676806,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 3.349809885931559
              },
              "checkpoint": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_1/experiments/phase_rank/cora/seed_2/arms/H2_R_HSPE/checkpoints/cora_uniform_seed2_04b0d3b0879e.pt",
              "checkpoint_sha256": "a94f6c15715a6a2850ce9e1974065b9102e357745abd65f6494f828bbdde3e3c",
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
              "train_pool_hash": "3d1e3ea691fc19fab65d66ad278d169cf099eb831ad0e46a439510ff5d07a7ba",
              "selected_negative_hash": "1ada7e01d1b3fa788db9d8312167290d4191344ace2db40bb787ab78e027c758",
              "validation_candidate_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
              "trainable_parameters": 24810,
              "added_parameters": 75,
              "train_seconds": 144.927665382158,
              "validation_scoring_seconds": 5.028036735020578,
              "wall_seconds": 150.3961950019002,
              "peak_gpu_allocated_mb": 71.06689453125,
              "checkpoint_rule": "fixed final epoch 10; no validation selection",
              "engine_cache_resumed": false
            }
          },
          "mrr": {
            "H2_R_HSPE": 0.6260422298445112
          },
          "feature_metadata_path": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_1/features/cora/metadata.json",
          "test_evaluated": false
        },
        {
          "state": "COMPLETE",
          "dataset": "cora",
          "seed": 3,
          "epochs": 10,
          "arms": {
            "H2_R_HSPE": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 3,
              "epochs": 10,
              "arm": "H2_R_HSPE",
              "test_evaluated": false,
              "validation_only": true,
              "validation_metrics": {
                "mrr": 0.6192053283787736,
                "hits10": 0.8935361216730038,
                "hits20": 0.9961977186311787,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 4.083650190114068
              },
              "checkpoint": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_1/experiments/phase_rank/cora/seed_3/arms/H2_R_HSPE/checkpoints/cora_uniform_seed3_aabc24216535.pt",
              "checkpoint_sha256": "7ffd8769ff580d1be7cdb486e0dc305c16e763ff8afff2189f1f2db03c6e574a",
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
              "train_pool_hash": "3d1e3ea691fc19fab65d66ad278d169cf099eb831ad0e46a439510ff5d07a7ba",
              "selected_negative_hash": "1ada7e01d1b3fa788db9d8312167290d4191344ace2db40bb787ab78e027c758",
              "validation_candidate_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
              "trainable_parameters": 24810,
              "added_parameters": 75,
              "train_seconds": 143.6870167478919,
              "validation_scoring_seconds": 5.214493834879249,
              "wall_seconds": 149.31723004532978,
              "peak_gpu_allocated_mb": 70.7734375,
              "checkpoint_rule": "fixed final epoch 10; no validation selection",
              "engine_cache_resumed": false
            }
          },
          "mrr": {
            "H2_R_HSPE": 0.6192053283787736
          },
          "feature_metadata_path": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_1/features/cora/metadata.json",
          "test_evaluated": false
        },
        {
          "state": "COMPLETE",
          "dataset": "cora",
          "seed": 4,
          "epochs": 10,
          "arms": {
            "H2_R_HSPE": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 4,
              "epochs": 10,
              "arm": "H2_R_HSPE",
              "test_evaluated": false,
              "validation_only": true,
              "validation_metrics": {
                "mrr": 0.655290483745498,
                "hits10": 0.8935361216730038,
                "hits20": 0.9885931558935361,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 3.6045627376425857
              },
              "checkpoint": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_1/experiments/phase_rank/cora/seed_4/arms/H2_R_HSPE/checkpoints/cora_uniform_seed4_accccd6f22b2.pt",
              "checkpoint_sha256": "dde63d3bed3a3673729ca323192c8c2024f8d2050bd7c35feb6985c5ba01287a",
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
              "train_pool_hash": "3d1e3ea691fc19fab65d66ad278d169cf099eb831ad0e46a439510ff5d07a7ba",
              "selected_negative_hash": "1ada7e01d1b3fa788db9d8312167290d4191344ace2db40bb787ab78e027c758",
              "validation_candidate_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
              "trainable_parameters": 24810,
              "added_parameters": 75,
              "train_seconds": 152.11586563196033,
              "validation_scoring_seconds": 3.0303462580777705,
              "wall_seconds": 155.5813394971192,
              "peak_gpu_allocated_mb": 70.78564453125,
              "checkpoint_rule": "fixed final epoch 10; no validation selection",
              "engine_cache_resumed": false
            }
          },
          "mrr": {
            "H2_R_HSPE": 0.655290483745498
          },
          "feature_metadata_path": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_1/features/cora/metadata.json",
          "test_evaluated": false
        }
      ],
      "H2_minus_H1": {
        "mean": 0.019563554672473015,
        "std": 0.06620361056949271,
        "median": 0.004088424746554908,
        "min": -0.04841992957685903,
        "max": 0.1295951777415657,
        "per_seed": [
          0.016534193024351995,
          -0.04841992957685903,
          -0.003980092573248495,
          0.004088424746554908,
          0.1295951777415657
        ]
      },
      "H2_minus_B0": {
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
      "metrics": {
        "mrr": {
          "mean": 0.5940511774956561,
          "std": 0.07991707996977651,
          "median": 0.6192053283787736,
          "min": 0.45382466680716216,
          "max": 0.655290483745498,
          "per_seed": [
            0.6158931787023348,
            0.45382466680716216,
            0.6260422298445112,
            0.6192053283787736,
            0.655290483745498
          ]
        },
        "hits10": {
          "mean": 0.8927756653992397,
          "std": 0.03383816800195737,
          "median": 0.8935361216730038,
          "min": 0.8479087452471483,
          "max": 0.9429657794676806,
          "per_seed": [
            0.8859315589353612,
            0.8479087452471483,
            0.9429657794676806,
            0.8935361216730038,
            0.8935361216730038
          ]
        },
        "hits20": {
          "mean": 0.9878326996197717,
          "std": 0.01708912931881691,
          "median": 0.9961977186311787,
          "min": 0.9581749049429658,
          "max": 1.0,
          "per_seed": [
            0.9581749049429658,
            0.9961977186311787,
            1.0,
            0.9961977186311787,
            0.9885931558935361
          ]
        },
        "mean_positive_rank": {
          "mean": 4.024334600760456,
          "std": 0.6803672279247122,
          "median": 3.958174904942966,
          "min": 3.349809885931559,
          "max": 5.1254752851711025,
          "per_seed": [
            3.958174904942966,
            5.1254752851711025,
            3.349809885931559,
            4.083650190114068,
            3.6045627376425857
          ]
        }
      },
      "parameters": 24810,
      "costs": {
        "train_seconds": {
          "mean": 146.69851251831278,
          "std": 4.823516180625146,
          "median": 144.927665382158,
          "min": 141.31588681973517,
          "max": 152.11586563196033,
          "per_seed": [
            151.4461280098185,
            141.31588681973517,
            144.927665382158,
            143.6870167478919,
            152.11586563196033
          ]
        },
        "validation_scoring_seconds": {
          "mean": 4.49420129917562,
          "std": 0.9123392938037881,
          "median": 5.023791825864464,
          "min": 3.0303462580777705,
          "max": 5.214493834879249,
          "per_seed": [
            4.174337842036039,
            5.023791825864464,
            5.028036735020578,
            5.214493834879249,
            3.0303462580777705
          ]
        },
        "peak_gpu_allocated_mb": {
          "mean": 70.75185546875,
          "std": 0.21525600760801156,
          "median": 70.7734375,
          "min": 70.4775390625,
          "max": 71.06689453125,
          "per_seed": [
            70.65576171875,
            70.4775390625,
            71.06689453125,
            70.7734375,
            70.78564453125
          ]
        }
      }
    },
    "pubmed": {
      "seed_results": [
        {
          "state": "COMPLETE",
          "dataset": "pubmed",
          "seed": 0,
          "epochs": 10,
          "arms": {
            "H2_R_HSPE": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 0,
              "epochs": 10,
              "arm": "H2_R_HSPE",
              "test_evaluated": false,
              "validation_only": true,
              "validation_metrics": {
                "mrr": 0.8688368217059952,
                "hits10": 0.9905234657039711,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.5667870036101084
              },
              "checkpoint": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_1/experiments/phase_rank/pubmed/seed_0/arms/H2_R_HSPE/checkpoints/pubmed_uniform_seed0_2444a1e1593f.pt",
              "checkpoint_sha256": "b552fa866b6cc27192246d09551a30cd53a41ec9d2719a3a6a817c71bd665ddd",
              "execution_sources": {
                "v171": "94eae10a845b3f4930edc776d0e9b18c104c9f40e0ae7dc7d93b6fe875cab4c3",
                "v17": "da20e41442f8e7b0b12d29515ba2a3df71a2a0a7327a51ea2b1170901e2e28bf",
                "v16_stage1": "f3b19889afa236fd71eeaa6681efc31c845eb32c4a90df87ab8d40092c196982",
                "stage0": "6d1f93ba8ab5ce0c99f584d1c38f1f44701c6c58ab19fbcc436b382eab0f1081",
                "qths_v71": "d8b1533b6398be98fe5741e5c485008c160434712c8d478268ae817b84b19f67",
                "negative_v61": "70b36c2d3b4f56a0b271b30e2bc60b360f99eb264368f22c4d095d1e421a7129",
                "codns_engine": "990c447435a0c1583c7df1bdb69d0a2493607eaf682afb9faf81738f4f9d0d67",
                "dcdlp_train": "1a51d4fecab93b75010def119946a91d4ed8ce44d3df852f167ca5400ac95f7d",
                "baseline_config": "9a5f4c2fb7cc8fab5179dca99e13b45445e1e17a2d23bae8ad3a924d1c47a76a"
              },
              "train_pool_hash": "d2434f4508c3fa493a400ddfa2abc71b3eb59999b977a557bc4dcfd4845849db",
              "selected_negative_hash": "28f8b8720989c1a445a46480d7ce60ac9e07fa0de24103541b2dec566d97da7d",
              "validation_candidate_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
              "trainable_parameters": 9882,
              "added_parameters": 75,
              "train_seconds": 3120.1923824101686,
              "validation_scoring_seconds": 47.49725368479267,
              "wall_seconds": 3172.199634666089,
              "peak_gpu_allocated_mb": 762.2177734375,
              "checkpoint_rule": "fixed final epoch 10; no validation selection",
              "engine_cache_resumed": false
            }
          },
          "mrr": {
            "H2_R_HSPE": 0.8688368217059952
          },
          "feature_metadata_path": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_1/features/pubmed/metadata.json",
          "test_evaluated": false
        },
        {
          "state": "COMPLETE",
          "dataset": "pubmed",
          "seed": 1,
          "epochs": 10,
          "arms": {
            "H2_R_HSPE": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 1,
              "epochs": 10,
              "arm": "H2_R_HSPE",
              "test_evaluated": false,
              "validation_only": true,
              "validation_metrics": {
                "mrr": 0.8266323529897935,
                "hits10": 0.9887184115523465,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.7775270758122743
              },
              "checkpoint": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_1/experiments/phase_rank/pubmed/seed_1/arms/H2_R_HSPE/checkpoints/pubmed_uniform_seed1_b97f51e42a03.pt",
              "checkpoint_sha256": "cb82b7c4ab661462b10752b949999a6563aa21fa855545025b825aaeb5b61d27",
              "execution_sources": {
                "v171": "94eae10a845b3f4930edc776d0e9b18c104c9f40e0ae7dc7d93b6fe875cab4c3",
                "v17": "da20e41442f8e7b0b12d29515ba2a3df71a2a0a7327a51ea2b1170901e2e28bf",
                "v16_stage1": "f3b19889afa236fd71eeaa6681efc31c845eb32c4a90df87ab8d40092c196982",
                "stage0": "6d1f93ba8ab5ce0c99f584d1c38f1f44701c6c58ab19fbcc436b382eab0f1081",
                "qths_v71": "d8b1533b6398be98fe5741e5c485008c160434712c8d478268ae817b84b19f67",
                "negative_v61": "70b36c2d3b4f56a0b271b30e2bc60b360f99eb264368f22c4d095d1e421a7129",
                "codns_engine": "990c447435a0c1583c7df1bdb69d0a2493607eaf682afb9faf81738f4f9d0d67",
                "dcdlp_train": "1a51d4fecab93b75010def119946a91d4ed8ce44d3df852f167ca5400ac95f7d",
                "baseline_config": "9a5f4c2fb7cc8fab5179dca99e13b45445e1e17a2d23bae8ad3a924d1c47a76a"
              },
              "train_pool_hash": "d2434f4508c3fa493a400ddfa2abc71b3eb59999b977a557bc4dcfd4845849db",
              "selected_negative_hash": "28f8b8720989c1a445a46480d7ce60ac9e07fa0de24103541b2dec566d97da7d",
              "validation_candidate_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
              "trainable_parameters": 9882,
              "added_parameters": 75,
              "train_seconds": 3078.8762713978067,
              "validation_scoring_seconds": 59.85003844182938,
              "wall_seconds": 3143.2754403478466,
              "peak_gpu_allocated_mb": 762.0478515625,
              "checkpoint_rule": "fixed final epoch 10; no validation selection",
              "engine_cache_resumed": false
            }
          },
          "mrr": {
            "H2_R_HSPE": 0.8266323529897935
          },
          "feature_metadata_path": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_1/features/pubmed/metadata.json",
          "test_evaluated": false
        },
        {
          "state": "COMPLETE",
          "dataset": "pubmed",
          "seed": 2,
          "epochs": 10,
          "arms": {
            "H2_R_HSPE": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 2,
              "epochs": 10,
              "arm": "H2_R_HSPE",
              "test_evaluated": false,
              "validation_only": true,
              "validation_metrics": {
                "mrr": 0.872205446537842,
                "hits10": 0.990072202166065,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.5848375451263539
              },
              "checkpoint": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_1/experiments/phase_rank/pubmed/seed_2/arms/H2_R_HSPE/checkpoints/pubmed_uniform_seed2_1590af779beb.pt",
              "checkpoint_sha256": "fc683ca3547fa7d6e7011c292f7ee0af8bc82fca2cf50ba0ed743ca8ae0ccd30",
              "execution_sources": {
                "v171": "94eae10a845b3f4930edc776d0e9b18c104c9f40e0ae7dc7d93b6fe875cab4c3",
                "v17": "da20e41442f8e7b0b12d29515ba2a3df71a2a0a7327a51ea2b1170901e2e28bf",
                "v16_stage1": "f3b19889afa236fd71eeaa6681efc31c845eb32c4a90df87ab8d40092c196982",
                "stage0": "6d1f93ba8ab5ce0c99f584d1c38f1f44701c6c58ab19fbcc436b382eab0f1081",
                "qths_v71": "d8b1533b6398be98fe5741e5c485008c160434712c8d478268ae817b84b19f67",
                "negative_v61": "70b36c2d3b4f56a0b271b30e2bc60b360f99eb264368f22c4d095d1e421a7129",
                "codns_engine": "990c447435a0c1583c7df1bdb69d0a2493607eaf682afb9faf81738f4f9d0d67",
                "dcdlp_train": "1a51d4fecab93b75010def119946a91d4ed8ce44d3df852f167ca5400ac95f7d",
                "baseline_config": "9a5f4c2fb7cc8fab5179dca99e13b45445e1e17a2d23bae8ad3a924d1c47a76a"
              },
              "train_pool_hash": "d2434f4508c3fa493a400ddfa2abc71b3eb59999b977a557bc4dcfd4845849db",
              "selected_negative_hash": "28f8b8720989c1a445a46480d7ce60ac9e07fa0de24103541b2dec566d97da7d",
              "validation_candidate_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
              "trainable_parameters": 9882,
              "added_parameters": 75,
              "train_seconds": 3194.178983310703,
              "validation_scoring_seconds": 21.63155455607921,
              "wall_seconds": 3220.086226612795,
              "peak_gpu_allocated_mb": 762.33447265625,
              "checkpoint_rule": "fixed final epoch 10; no validation selection",
              "engine_cache_resumed": false
            }
          },
          "mrr": {
            "H2_R_HSPE": 0.872205446537842
          },
          "feature_metadata_path": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_1/features/pubmed/metadata.json",
          "test_evaluated": false
        },
        {
          "state": "COMPLETE",
          "dataset": "pubmed",
          "seed": 3,
          "epochs": 10,
          "arms": {
            "H2_R_HSPE": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 3,
              "epochs": 10,
              "arm": "H2_R_HSPE",
              "test_evaluated": false,
              "validation_only": true,
              "validation_metrics": {
                "mrr": 0.8692951398369216,
                "hits10": 0.9950361010830325,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.5446750902527075
              },
              "checkpoint": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_1/experiments/phase_rank/pubmed/seed_3/arms/H2_R_HSPE/checkpoints/pubmed_uniform_seed3_f0c301fe0a33.pt",
              "checkpoint_sha256": "73847903993851172afbe6943684eb9ee313bc02eaf736f88a6dd9bd4e98a51f",
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
              "train_pool_hash": "d2434f4508c3fa493a400ddfa2abc71b3eb59999b977a557bc4dcfd4845849db",
              "selected_negative_hash": "28f8b8720989c1a445a46480d7ce60ac9e07fa0de24103541b2dec566d97da7d",
              "validation_candidate_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
              "trainable_parameters": 9882,
              "added_parameters": 75,
              "train_seconds": 2316.09582330985,
              "validation_scoring_seconds": 41.77562359813601,
              "wall_seconds": 2362.209279133007,
              "peak_gpu_allocated_mb": 762.68994140625,
              "checkpoint_rule": "fixed final epoch 10; no validation selection",
              "engine_cache_resumed": false
            }
          },
          "mrr": {
            "H2_R_HSPE": 0.8692951398369216
          },
          "feature_metadata_path": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_1/features/pubmed/metadata.json",
          "test_evaluated": false
        },
        {
          "state": "COMPLETE",
          "dataset": "pubmed",
          "seed": 4,
          "epochs": 10,
          "arms": {
            "H2_R_HSPE": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 4,
              "epochs": 10,
              "arm": "H2_R_HSPE",
              "test_evaluated": false,
              "validation_only": true,
              "validation_metrics": {
                "mrr": 0.8833791635935103,
                "hits10": 0.9896209386281588,
                "hits20": 0.9995487364620939,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.513537906137184
              },
              "checkpoint": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_1/experiments/phase_rank/pubmed/seed_4/arms/H2_R_HSPE/checkpoints/pubmed_uniform_seed4_da8ec6bf7a2a.pt",
              "checkpoint_sha256": "4756478d69d7fcc1411685b90c4246cc183cad8c2d06500a2dce0cede7ae769a",
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
              "train_pool_hash": "d2434f4508c3fa493a400ddfa2abc71b3eb59999b977a557bc4dcfd4845849db",
              "selected_negative_hash": "28f8b8720989c1a445a46480d7ce60ac9e07fa0de24103541b2dec566d97da7d",
              "validation_candidate_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
              "trainable_parameters": 9882,
              "added_parameters": 75,
              "train_seconds": 2245.7106432951987,
              "validation_scoring_seconds": 21.404795341193676,
              "wall_seconds": 2271.265330610331,
              "peak_gpu_allocated_mb": 762.1826171875,
              "checkpoint_rule": "fixed final epoch 10; no validation selection",
              "engine_cache_resumed": false
            }
          },
          "mrr": {
            "H2_R_HSPE": 0.8833791635935103
          },
          "feature_metadata_path": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HSPE_V17_1/features/pubmed/metadata.json",
          "test_evaluated": false
        }
      ],
      "H2_minus_H1": {
        "mean": 0.0007863224664304668,
        "std": 0.003837667635784238,
        "median": 0.0025731468102461186,
        "min": -0.0049470838136125295,
        "max": 0.004611494531133409,
        "per_seed": [
          0.0025731468102461186,
          -0.0049470838136125295,
          0.004611494531133409,
          0.002872708919640421,
          -0.0011786541152550845
        ]
      },
      "H2_minus_B0": {
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
      "metrics": {
        "mrr": {
          "mean": 0.8640697849328125,
          "std": 0.021740695584391463,
          "median": 0.8692951398369216,
          "min": 0.8266323529897935,
          "max": 0.8833791635935103,
          "per_seed": [
            0.8688368217059952,
            0.8266323529897935,
            0.872205446537842,
            0.8692951398369216,
            0.8833791635935103
          ]
        },
        "hits10": {
          "mean": 0.9907942238267149,
          "std": 0.002463419506129309,
          "median": 0.990072202166065,
          "min": 0.9887184115523465,
          "max": 0.9950361010830325,
          "per_seed": [
            0.9905234657039711,
            0.9887184115523465,
            0.990072202166065,
            0.9950361010830325,
            0.9896209386281588
          ]
        },
        "hits20": {
          "mean": 0.9999097472924188,
          "std": 0.00020181118930503804,
          "median": 1.0,
          "min": 0.9995487364620939,
          "max": 1.0,
          "per_seed": [
            1.0,
            1.0,
            1.0,
            1.0,
            0.9995487364620939
          ]
        },
        "mean_positive_rank": {
          "mean": 1.5974729241877257,
          "std": 0.10410748600164499,
          "median": 1.5667870036101084,
          "min": 1.513537906137184,
          "max": 1.7775270758122743,
          "per_seed": [
            1.5667870036101084,
            1.7775270758122743,
            1.5848375451263539,
            1.5446750902527075,
            1.513537906137184
          ]
        }
      },
      "parameters": 9882,
      "costs": {
        "train_seconds": {
          "mean": 2791.0108207447456,
          "std": 468.15278591558155,
          "median": 3078.8762713978067,
          "min": 2245.7106432951987,
          "max": 3194.178983310703,
          "per_seed": [
            3120.1923824101686,
            3078.8762713978067,
            3194.178983310703,
            2316.09582330985,
            2245.7106432951987
          ]
        },
        "validation_scoring_seconds": {
          "mean": 38.43185312440619,
          "std": 16.76508037059853,
          "median": 41.77562359813601,
          "min": 21.404795341193676,
          "max": 59.85003844182938,
          "per_seed": [
            47.49725368479267,
            59.85003844182938,
            21.63155455607921,
            41.77562359813601,
            21.404795341193676
          ]
        },
        "peak_gpu_allocated_mb": {
          "mean": 762.29453125,
          "std": 0.24352201901933512,
          "median": 762.2177734375,
          "min": 762.0478515625,
          "max": 762.68994140625,
          "per_seed": [
            762.2177734375,
            762.0478515625,
            762.33447265625,
            762.68994140625,
            762.1826171875
          ]
        }
      }
    }
  },
  "promoted": true,
  "final_variant": "R_HSPE"
}