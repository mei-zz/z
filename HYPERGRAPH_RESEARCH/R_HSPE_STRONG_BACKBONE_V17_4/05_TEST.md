# One-shot test

{
  "state": "COMPLETE",
  "datasets": {
    "cora": {
      "seeds": [
        0,
        1,
        2,
        3,
        4
      ],
      "seed_results": [
        {
          "seed": 0,
          "arms": {
            "C0": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 0,
              "arm": "C0",
              "epochs": 10,
              "metrics": {
                "mrr": 0.6673798542887109,
                "hits10": 0.8747628083491461,
                "hits20": 0.9772296015180265,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 3.903225806451613
              },
              "checkpoint_sha256": "846612c9424e2a29c89ae7b8f9ec206fcf2e06f511b293e465df1a3f98823903",
              "inference_seconds": 0.5362577028572559,
              "peak_gpu_mb": 69.56396484375,
              "test_candidate_metadata": {
                "n": 2708,
                "feature_shape": [
                  2708,
                  1433
                ],
                "train_edges": 4488,
                "train_hash": "fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8",
                "valid_positive_hash": "ce0c7a24f7e22fe0ec1c6e22bc185f5f29eb8b1ef2eb2e25da7666a2aabe5482",
                "valid_negative_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
                "test_positive_hash": "9360956ed1e7613ec25bfc677b25dfe9e5cd465b60f6eb7af30d3dc08ad6f4c8",
                "test_negative_hash": "ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92",
                "test_cache_sha256": "c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1",
                "test_queries": 527,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "C1": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 0,
              "arm": "C1",
              "epochs": 10,
              "metrics": {
                "mrr": 0.7015357065892106,
                "hits10": 0.905123339658444,
                "hits20": 0.9867172675521821,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 3.383301707779886
              },
              "checkpoint_sha256": "151f324c79e3b34206897a7ff3b8c46230628baf031b6507867a5119b7847538",
              "inference_seconds": 0.5744872190989554,
              "peak_gpu_mb": 70.45654296875,
              "test_candidate_metadata": {
                "n": 2708,
                "feature_shape": [
                  2708,
                  1433
                ],
                "train_edges": 4488,
                "train_hash": "fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8",
                "valid_positive_hash": "ce0c7a24f7e22fe0ec1c6e22bc185f5f29eb8b1ef2eb2e25da7666a2aabe5482",
                "valid_negative_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
                "test_positive_hash": "9360956ed1e7613ec25bfc677b25dfe9e5cd465b60f6eb7af30d3dc08ad6f4c8",
                "test_negative_hash": "ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92",
                "test_cache_sha256": "c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1",
                "test_queries": 527,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "C2": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 0,
              "arm": "C2",
              "epochs": 10,
              "metrics": {
                "mrr": 0.6672070739342845,
                "hits10": 0.872865275142315,
                "hits20": 0.9791271347248577,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 3.9222011385199242
              },
              "checkpoint_sha256": "95f0f6b5c0cda84e13b3be95564639b0e05a76d6c9773f9b845c13404bf9c0f8",
              "inference_seconds": 0.3828708538785577,
              "peak_gpu_mb": 69.56787109375,
              "test_candidate_metadata": {
                "n": 2708,
                "feature_shape": [
                  2708,
                  1433
                ],
                "train_edges": 4488,
                "train_hash": "fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8",
                "valid_positive_hash": "ce0c7a24f7e22fe0ec1c6e22bc185f5f29eb8b1ef2eb2e25da7666a2aabe5482",
                "valid_negative_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
                "test_positive_hash": "9360956ed1e7613ec25bfc677b25dfe9e5cd465b60f6eb7af30d3dc08ad6f4c8",
                "test_negative_hash": "ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92",
                "test_cache_sha256": "c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1",
                "test_queries": 527,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "N0": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 0,
              "arm": "N0",
              "epochs": 10,
              "metrics": {
                "mrr": 0.6750088571415699,
                "hits10": 0.8956356736242884,
                "hits20": 0.9962049335863378,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 3.5161290322580645
              },
              "checkpoint_sha256": "be6b963fa5ae9519bedb525ac7859780dc527760b37d6339a67e2dcb3b7befe0",
              "inference_seconds": 0.17821618495509028,
              "peak_gpu_mb": 90.69091796875,
              "test_candidate_metadata": {
                "n": 2708,
                "feature_shape": [
                  2708,
                  1433
                ],
                "train_edges": 4488,
                "train_hash": "fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8",
                "valid_positive_hash": "ce0c7a24f7e22fe0ec1c6e22bc185f5f29eb8b1ef2eb2e25da7666a2aabe5482",
                "valid_negative_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
                "test_positive_hash": "9360956ed1e7613ec25bfc677b25dfe9e5cd465b60f6eb7af30d3dc08ad6f4c8",
                "test_negative_hash": "ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92",
                "test_cache_sha256": "c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1",
                "test_queries": 527,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "N1": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 0,
              "arm": "N1",
              "epochs": 10,
              "metrics": {
                "mrr": 0.6960280276933333,
                "hits10": 0.9222011385199241,
                "hits20": 0.9962049335863378,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 3.1252371916508537
              },
              "checkpoint_sha256": "23f18b7d95d86af298e34e12c14ade65eae224a7c07918652340dd3e30687aea",
              "inference_seconds": 0.23958316398784518,
              "peak_gpu_mb": 91.58349609375,
              "test_candidate_metadata": {
                "n": 2708,
                "feature_shape": [
                  2708,
                  1433
                ],
                "train_edges": 4488,
                "train_hash": "fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8",
                "valid_positive_hash": "ce0c7a24f7e22fe0ec1c6e22bc185f5f29eb8b1ef2eb2e25da7666a2aabe5482",
                "valid_negative_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
                "test_positive_hash": "9360956ed1e7613ec25bfc677b25dfe9e5cd465b60f6eb7af30d3dc08ad6f4c8",
                "test_negative_hash": "ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92",
                "test_cache_sha256": "c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1",
                "test_queries": 527,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            }
          }
        },
        {
          "seed": 1,
          "arms": {
            "C0": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 1,
              "arm": "C0",
              "epochs": 10,
              "metrics": {
                "mrr": 0.7666469641159896,
                "hits10": 0.9829222011385199,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 2.0607210626185957
              },
              "checkpoint_sha256": "25003e892cb3890afaa7bb2f915237e5891b16da41aafbb597e0b9ce259c0d18",
              "inference_seconds": 0.42684653494507074,
              "peak_gpu_mb": 69.56396484375,
              "test_candidate_metadata": {
                "n": 2708,
                "feature_shape": [
                  2708,
                  1433
                ],
                "train_edges": 4488,
                "train_hash": "fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8",
                "valid_positive_hash": "ce0c7a24f7e22fe0ec1c6e22bc185f5f29eb8b1ef2eb2e25da7666a2aabe5482",
                "valid_negative_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
                "test_positive_hash": "9360956ed1e7613ec25bfc677b25dfe9e5cd465b60f6eb7af30d3dc08ad6f4c8",
                "test_negative_hash": "ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92",
                "test_cache_sha256": "c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1",
                "test_queries": 527,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "C1": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 1,
              "arm": "C1",
              "epochs": 10,
              "metrics": {
                "mrr": 0.7761257311848896,
                "hits10": 0.9810246679316889,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.984819734345351
              },
              "checkpoint_sha256": "4cb2f05f83d9ea0ec7e9114f188bb93326822d1f145654a575d0c1f397cd50c0",
              "inference_seconds": 0.555869409814477,
              "peak_gpu_mb": 70.45654296875,
              "test_candidate_metadata": {
                "n": 2708,
                "feature_shape": [
                  2708,
                  1433
                ],
                "train_edges": 4488,
                "train_hash": "fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8",
                "valid_positive_hash": "ce0c7a24f7e22fe0ec1c6e22bc185f5f29eb8b1ef2eb2e25da7666a2aabe5482",
                "valid_negative_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
                "test_positive_hash": "9360956ed1e7613ec25bfc677b25dfe9e5cd465b60f6eb7af30d3dc08ad6f4c8",
                "test_negative_hash": "ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92",
                "test_cache_sha256": "c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1",
                "test_queries": 527,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "C2": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 1,
              "arm": "C2",
              "epochs": 10,
              "metrics": {
                "mrr": 0.7653100465160964,
                "hits10": 0.9848197343453511,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 2.066413662239089
              },
              "checkpoint_sha256": "540327fb0f91c481f3ba4ae04592491c25e4006b6231226222ec4d4ce0c63075",
              "inference_seconds": 0.4437133972533047,
              "peak_gpu_mb": 69.56787109375,
              "test_candidate_metadata": {
                "n": 2708,
                "feature_shape": [
                  2708,
                  1433
                ],
                "train_edges": 4488,
                "train_hash": "fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8",
                "valid_positive_hash": "ce0c7a24f7e22fe0ec1c6e22bc185f5f29eb8b1ef2eb2e25da7666a2aabe5482",
                "valid_negative_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
                "test_positive_hash": "9360956ed1e7613ec25bfc677b25dfe9e5cd465b60f6eb7af30d3dc08ad6f4c8",
                "test_negative_hash": "ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92",
                "test_cache_sha256": "c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1",
                "test_queries": 527,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "N0": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 1,
              "arm": "N0",
              "epochs": 10,
              "metrics": {
                "mrr": 0.7875291954513965,
                "hits10": 0.9829222011385199,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.9601518026565465
              },
              "checkpoint_sha256": "01fc8444f9690d4306703b6397c4f7023faa9cc69fbb99c3799c67cd53858dd8",
              "inference_seconds": 0.16600612923502922,
              "peak_gpu_mb": 90.69091796875,
              "test_candidate_metadata": {
                "n": 2708,
                "feature_shape": [
                  2708,
                  1433
                ],
                "train_edges": 4488,
                "train_hash": "fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8",
                "valid_positive_hash": "ce0c7a24f7e22fe0ec1c6e22bc185f5f29eb8b1ef2eb2e25da7666a2aabe5482",
                "valid_negative_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
                "test_positive_hash": "9360956ed1e7613ec25bfc677b25dfe9e5cd465b60f6eb7af30d3dc08ad6f4c8",
                "test_negative_hash": "ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92",
                "test_cache_sha256": "c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1",
                "test_queries": 527,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "N1": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 1,
              "arm": "N1",
              "epochs": 10,
              "metrics": {
                "mrr": 0.7946586688354743,
                "hits10": 0.9848197343453511,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.9259962049335864
              },
              "checkpoint_sha256": "6832ff9c14a7fcdbb4f49ee063fa0edf249fa173c6b363d1f53da118163bbc8d",
              "inference_seconds": 0.2660424327477813,
              "peak_gpu_mb": 91.58349609375,
              "test_candidate_metadata": {
                "n": 2708,
                "feature_shape": [
                  2708,
                  1433
                ],
                "train_edges": 4488,
                "train_hash": "fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8",
                "valid_positive_hash": "ce0c7a24f7e22fe0ec1c6e22bc185f5f29eb8b1ef2eb2e25da7666a2aabe5482",
                "valid_negative_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
                "test_positive_hash": "9360956ed1e7613ec25bfc677b25dfe9e5cd465b60f6eb7af30d3dc08ad6f4c8",
                "test_negative_hash": "ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92",
                "test_cache_sha256": "c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1",
                "test_queries": 527,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            }
          }
        },
        {
          "seed": 2,
          "arms": {
            "C0": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 2,
              "arm": "C0",
              "epochs": 10,
              "metrics": {
                "mrr": 0.6373259848401722,
                "hits10": 0.8918406072106262,
                "hits20": 0.9943074003795066,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 3.7267552182163186
              },
              "checkpoint_sha256": "f8c85f111dc2cab4fa23a279c409c1ef13817a77c84a9eaf9f840c65b8459c49",
              "inference_seconds": 0.42758469795808196,
              "peak_gpu_mb": 69.56396484375,
              "test_candidate_metadata": {
                "n": 2708,
                "feature_shape": [
                  2708,
                  1433
                ],
                "train_edges": 4488,
                "train_hash": "fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8",
                "valid_positive_hash": "ce0c7a24f7e22fe0ec1c6e22bc185f5f29eb8b1ef2eb2e25da7666a2aabe5482",
                "valid_negative_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
                "test_positive_hash": "9360956ed1e7613ec25bfc677b25dfe9e5cd465b60f6eb7af30d3dc08ad6f4c8",
                "test_negative_hash": "ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92",
                "test_cache_sha256": "c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1",
                "test_queries": 527,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "C1": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 2,
              "arm": "C1",
              "epochs": 10,
              "metrics": {
                "mrr": 0.681932107076625,
                "hits10": 0.9032258064516129,
                "hits20": 0.9924098671726755,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 3.407969639468691
              },
              "checkpoint_sha256": "8f022b4ef7774dc024a25688f66dda9a5aec79432ece5f4f52c442f2f1033ab7",
              "inference_seconds": 0.5099591012112796,
              "peak_gpu_mb": 70.45654296875,
              "test_candidate_metadata": {
                "n": 2708,
                "feature_shape": [
                  2708,
                  1433
                ],
                "train_edges": 4488,
                "train_hash": "fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8",
                "valid_positive_hash": "ce0c7a24f7e22fe0ec1c6e22bc185f5f29eb8b1ef2eb2e25da7666a2aabe5482",
                "valid_negative_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
                "test_positive_hash": "9360956ed1e7613ec25bfc677b25dfe9e5cd465b60f6eb7af30d3dc08ad6f4c8",
                "test_negative_hash": "ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92",
                "test_cache_sha256": "c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1",
                "test_queries": 527,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "C2": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 2,
              "arm": "C2",
              "epochs": 10,
              "metrics": {
                "mrr": 0.6297251378621334,
                "hits10": 0.8994307400379506,
                "hits20": 0.9943074003795066,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 3.685009487666034
              },
              "checkpoint_sha256": "93a45d9685bb869dae020a9e38feeef1a6152f8f457986036a4f77ebb0b79ca6",
              "inference_seconds": 0.4401440662331879,
              "peak_gpu_mb": 69.56787109375,
              "test_candidate_metadata": {
                "n": 2708,
                "feature_shape": [
                  2708,
                  1433
                ],
                "train_edges": 4488,
                "train_hash": "fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8",
                "valid_positive_hash": "ce0c7a24f7e22fe0ec1c6e22bc185f5f29eb8b1ef2eb2e25da7666a2aabe5482",
                "valid_negative_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
                "test_positive_hash": "9360956ed1e7613ec25bfc677b25dfe9e5cd465b60f6eb7af30d3dc08ad6f4c8",
                "test_negative_hash": "ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92",
                "test_cache_sha256": "c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1",
                "test_queries": 527,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "N0": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 2,
              "arm": "N0",
              "epochs": 10,
              "metrics": {
                "mrr": 0.6820908893670188,
                "hits10": 0.9146110056925996,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 3.25426944971537
              },
              "checkpoint_sha256": "a972651c3fb8c91be399c133d3dad691a4b0e3f64b2f30cbc3a2d6b549aa83b7",
              "inference_seconds": 0.17281011398881674,
              "peak_gpu_mb": 90.69091796875,
              "test_candidate_metadata": {
                "n": 2708,
                "feature_shape": [
                  2708,
                  1433
                ],
                "train_edges": 4488,
                "train_hash": "fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8",
                "valid_positive_hash": "ce0c7a24f7e22fe0ec1c6e22bc185f5f29eb8b1ef2eb2e25da7666a2aabe5482",
                "valid_negative_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
                "test_positive_hash": "9360956ed1e7613ec25bfc677b25dfe9e5cd465b60f6eb7af30d3dc08ad6f4c8",
                "test_negative_hash": "ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92",
                "test_cache_sha256": "c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1",
                "test_queries": 527,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "N1": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 2,
              "arm": "N1",
              "epochs": 10,
              "metrics": {
                "mrr": 0.6988685618016018,
                "hits10": 0.9259962049335864,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 2.9905123339658446
              },
              "checkpoint_sha256": "1a513dfe30f3f48d85d14c601e7c410c15b56c453fa18940543c1922741e992e",
              "inference_seconds": 0.23943877592682838,
              "peak_gpu_mb": 91.58349609375,
              "test_candidate_metadata": {
                "n": 2708,
                "feature_shape": [
                  2708,
                  1433
                ],
                "train_edges": 4488,
                "train_hash": "fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8",
                "valid_positive_hash": "ce0c7a24f7e22fe0ec1c6e22bc185f5f29eb8b1ef2eb2e25da7666a2aabe5482",
                "valid_negative_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
                "test_positive_hash": "9360956ed1e7613ec25bfc677b25dfe9e5cd465b60f6eb7af30d3dc08ad6f4c8",
                "test_negative_hash": "ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92",
                "test_cache_sha256": "c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1",
                "test_queries": 527,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            }
          }
        },
        {
          "seed": 3,
          "arms": {
            "C0": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 3,
              "arm": "C0",
              "epochs": 10,
              "metrics": {
                "mrr": 0.6825682232967468,
                "hits10": 0.8766603415559773,
                "hits20": 0.9810246679316889,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 3.825426944971537
              },
              "checkpoint_sha256": "dc53fd5d2ad5c9a5c98a5d1b0600a42f7c526469eeb9986388e95920e9e87e2c",
              "inference_seconds": 0.4357146969996393,
              "peak_gpu_mb": 69.56396484375,
              "test_candidate_metadata": {
                "n": 2708,
                "feature_shape": [
                  2708,
                  1433
                ],
                "train_edges": 4488,
                "train_hash": "fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8",
                "valid_positive_hash": "ce0c7a24f7e22fe0ec1c6e22bc185f5f29eb8b1ef2eb2e25da7666a2aabe5482",
                "valid_negative_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
                "test_positive_hash": "9360956ed1e7613ec25bfc677b25dfe9e5cd465b60f6eb7af30d3dc08ad6f4c8",
                "test_negative_hash": "ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92",
                "test_cache_sha256": "c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1",
                "test_queries": 527,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "C1": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 3,
              "arm": "C1",
              "epochs": 10,
              "metrics": {
                "mrr": 0.6868758437808378,
                "hits10": 0.8823529411764706,
                "hits20": 0.9829222011385199,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 3.6963946869070208
              },
              "checkpoint_sha256": "49c217fcc28c26ed57c1133431228bba322167a1bf3fc57931a378245c574b0a",
              "inference_seconds": 0.5749852359294891,
              "peak_gpu_mb": 70.45654296875,
              "test_candidate_metadata": {
                "n": 2708,
                "feature_shape": [
                  2708,
                  1433
                ],
                "train_edges": 4488,
                "train_hash": "fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8",
                "valid_positive_hash": "ce0c7a24f7e22fe0ec1c6e22bc185f5f29eb8b1ef2eb2e25da7666a2aabe5482",
                "valid_negative_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
                "test_positive_hash": "9360956ed1e7613ec25bfc677b25dfe9e5cd465b60f6eb7af30d3dc08ad6f4c8",
                "test_negative_hash": "ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92",
                "test_cache_sha256": "c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1",
                "test_queries": 527,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "C2": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 3,
              "arm": "C2",
              "epochs": 10,
              "metrics": {
                "mrr": 0.680652104943247,
                "hits10": 0.8766603415559773,
                "hits20": 0.9829222011385199,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 3.844402277039848
              },
              "checkpoint_sha256": "dfb30ad7656a908515b4a0f0bf0ecef96097f871aac7b101a5cb1891c6885767",
              "inference_seconds": 0.4644989166408777,
              "peak_gpu_mb": 69.56787109375,
              "test_candidate_metadata": {
                "n": 2708,
                "feature_shape": [
                  2708,
                  1433
                ],
                "train_edges": 4488,
                "train_hash": "fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8",
                "valid_positive_hash": "ce0c7a24f7e22fe0ec1c6e22bc185f5f29eb8b1ef2eb2e25da7666a2aabe5482",
                "valid_negative_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
                "test_positive_hash": "9360956ed1e7613ec25bfc677b25dfe9e5cd465b60f6eb7af30d3dc08ad6f4c8",
                "test_negative_hash": "ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92",
                "test_cache_sha256": "c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1",
                "test_queries": 527,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "N0": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 3,
              "arm": "N0",
              "epochs": 10,
              "metrics": {
                "mrr": 0.7222500380707212,
                "hits10": 0.9658444022770398,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 2.523719165085389
              },
              "checkpoint_sha256": "a095043471b739ca1a164bf214b9b2da60b3641ce3725dd6bdaf9eb5906dc5c4",
              "inference_seconds": 0.16903896490111947,
              "peak_gpu_mb": 90.69091796875,
              "test_candidate_metadata": {
                "n": 2708,
                "feature_shape": [
                  2708,
                  1433
                ],
                "train_edges": 4488,
                "train_hash": "fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8",
                "valid_positive_hash": "ce0c7a24f7e22fe0ec1c6e22bc185f5f29eb8b1ef2eb2e25da7666a2aabe5482",
                "valid_negative_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
                "test_positive_hash": "9360956ed1e7613ec25bfc677b25dfe9e5cd465b60f6eb7af30d3dc08ad6f4c8",
                "test_negative_hash": "ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92",
                "test_cache_sha256": "c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1",
                "test_queries": 527,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "N1": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 3,
              "arm": "N1",
              "epochs": 10,
              "metrics": {
                "mrr": 0.7408108494920639,
                "hits10": 0.967741935483871,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 2.4041745730550286
              },
              "checkpoint_sha256": "ac848e3e88651cb0ae89a9b2ac654cb70ea0d95f50a563c24143b579d8656eeb",
              "inference_seconds": 0.22874143533408642,
              "peak_gpu_mb": 91.58349609375,
              "test_candidate_metadata": {
                "n": 2708,
                "feature_shape": [
                  2708,
                  1433
                ],
                "train_edges": 4488,
                "train_hash": "fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8",
                "valid_positive_hash": "ce0c7a24f7e22fe0ec1c6e22bc185f5f29eb8b1ef2eb2e25da7666a2aabe5482",
                "valid_negative_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
                "test_positive_hash": "9360956ed1e7613ec25bfc677b25dfe9e5cd465b60f6eb7af30d3dc08ad6f4c8",
                "test_negative_hash": "ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92",
                "test_cache_sha256": "c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1",
                "test_queries": 527,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            }
          }
        },
        {
          "seed": 4,
          "arms": {
            "C0": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 4,
              "arm": "C0",
              "epochs": 10,
              "metrics": {
                "mrr": 0.6422661271446087,
                "hits10": 0.8614800759013282,
                "hits20": 0.9829222011385199,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 4.16888045540797
              },
              "checkpoint_sha256": "2c5ac54c3f545ad2ae0cb3dca4edc76f1abf2e74a452191a5924f9017cc6a8b5",
              "inference_seconds": 0.44813481997698545,
              "peak_gpu_mb": 69.56396484375,
              "test_candidate_metadata": {
                "n": 2708,
                "feature_shape": [
                  2708,
                  1433
                ],
                "train_edges": 4488,
                "train_hash": "fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8",
                "valid_positive_hash": "ce0c7a24f7e22fe0ec1c6e22bc185f5f29eb8b1ef2eb2e25da7666a2aabe5482",
                "valid_negative_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
                "test_positive_hash": "9360956ed1e7613ec25bfc677b25dfe9e5cd465b60f6eb7af30d3dc08ad6f4c8",
                "test_negative_hash": "ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92",
                "test_cache_sha256": "c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1",
                "test_queries": 527,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "C1": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 4,
              "arm": "C1",
              "epochs": 10,
              "metrics": {
                "mrr": 0.6789811783593396,
                "hits10": 0.8766603415559773,
                "hits20": 0.9848197343453511,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 3.823529411764706
              },
              "checkpoint_sha256": "bc09eac71b472ee4d1e2687eec4b8ebd6654d55a2992151b0446568a56a26d3c",
              "inference_seconds": 0.5309267537668347,
              "peak_gpu_mb": 70.45654296875,
              "test_candidate_metadata": {
                "n": 2708,
                "feature_shape": [
                  2708,
                  1433
                ],
                "train_edges": 4488,
                "train_hash": "fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8",
                "valid_positive_hash": "ce0c7a24f7e22fe0ec1c6e22bc185f5f29eb8b1ef2eb2e25da7666a2aabe5482",
                "valid_negative_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
                "test_positive_hash": "9360956ed1e7613ec25bfc677b25dfe9e5cd465b60f6eb7af30d3dc08ad6f4c8",
                "test_negative_hash": "ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92",
                "test_cache_sha256": "c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1",
                "test_queries": 527,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "C2": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 4,
              "arm": "C2",
              "epochs": 10,
              "metrics": {
                "mrr": 0.6426151911475403,
                "hits10": 0.8595825426944972,
                "hits20": 0.9810246679316889,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 4.16888045540797
              },
              "checkpoint_sha256": "19ea084e319b3e13d34a404af2b272a5228c9d963f000c9d972bb693fc7c8a3c",
              "inference_seconds": 0.44408890418708324,
              "peak_gpu_mb": 69.56787109375,
              "test_candidate_metadata": {
                "n": 2708,
                "feature_shape": [
                  2708,
                  1433
                ],
                "train_edges": 4488,
                "train_hash": "fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8",
                "valid_positive_hash": "ce0c7a24f7e22fe0ec1c6e22bc185f5f29eb8b1ef2eb2e25da7666a2aabe5482",
                "valid_negative_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
                "test_positive_hash": "9360956ed1e7613ec25bfc677b25dfe9e5cd465b60f6eb7af30d3dc08ad6f4c8",
                "test_negative_hash": "ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92",
                "test_cache_sha256": "c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1",
                "test_queries": 527,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "N0": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 4,
              "arm": "N0",
              "epochs": 10,
              "metrics": {
                "mrr": 0.7042693255811056,
                "hits10": 0.9354838709677419,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 2.905123339658444
              },
              "checkpoint_sha256": "d9f2c521e76923c5dda99c10be54cd9141153ad76677a377f5126f5b383ac1f2",
              "inference_seconds": 0.16993551515042782,
              "peak_gpu_mb": 90.69091796875,
              "test_candidate_metadata": {
                "n": 2708,
                "feature_shape": [
                  2708,
                  1433
                ],
                "train_edges": 4488,
                "train_hash": "fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8",
                "valid_positive_hash": "ce0c7a24f7e22fe0ec1c6e22bc185f5f29eb8b1ef2eb2e25da7666a2aabe5482",
                "valid_negative_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
                "test_positive_hash": "9360956ed1e7613ec25bfc677b25dfe9e5cd465b60f6eb7af30d3dc08ad6f4c8",
                "test_negative_hash": "ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92",
                "test_cache_sha256": "c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1",
                "test_queries": 527,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "N1": {
              "state": "COMPLETE",
              "dataset": "cora",
              "seed": 4,
              "arm": "N1",
              "epochs": 10,
              "metrics": {
                "mrr": 0.7254910716451889,
                "hits10": 0.9468690702087287,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 2.6755218216318783
              },
              "checkpoint_sha256": "7348a30ea916c877c3aa488ae61b2fdf1136d1da85e5a53c72ceb0b38d05e5fa",
              "inference_seconds": 0.23882349114865065,
              "peak_gpu_mb": 91.58349609375,
              "test_candidate_metadata": {
                "n": 2708,
                "feature_shape": [
                  2708,
                  1433
                ],
                "train_edges": 4488,
                "train_hash": "fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8",
                "valid_positive_hash": "ce0c7a24f7e22fe0ec1c6e22bc185f5f29eb8b1ef2eb2e25da7666a2aabe5482",
                "valid_negative_hash": "7a99176386556eddb0c3f7d7b08b52a8da83504b9c980b84f6b99e16bfe9a902",
                "test_positive_hash": "9360956ed1e7613ec25bfc677b25dfe9e5cd465b60f6eb7af30d3dc08ad6f4c8",
                "test_negative_hash": "ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92",
                "test_cache_sha256": "c2a60aee273964509ace1615c01e2fdf0857fedeca76ad749da3eaf019bbc4e1",
                "test_queries": 527,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            }
          }
        }
      ],
      "effects": {
        "delta_ncnc": {
          "mean": 0.025852682660934833,
          "std": 0.017824982388446015,
          "median": 0.03415585230049967,
          "min": 0.004307620484090946,
          "max": 0.04460612223645277,
          "per_seed": [
            0.03415585230049967,
            0.00947876706889994,
            0.04460612223645277,
            0.004307620484090946,
            0.03671505121473084
          ],
          "wins": 5
        },
        "delta_null": {
          "mean": 0.02798820251752021,
          "std": 0.019141083038670837,
          "median": 0.03432863265492614,
          "min": 0.006223738837590753,
          "max": 0.05220696921449164,
          "per_seed": [
            0.03432863265492614,
            0.010815684668793235,
            0.05220696921449164,
            0.006223738837590753,
            0.03636598721179929
          ],
          "wins": 5
        },
        "delta_ncn": {
          "mean": 0.016941774771170048,
          "std": 0.005785170230476603,
          "median": 0.018560811421342693,
          "min": 0.007129473384077767,
          "max": 0.021221746064083336,
          "per_seed": [
            0.02101917055176339,
            0.007129473384077767,
            0.016777672434583057,
            0.018560811421342693,
            0.021221746064083336
          ],
          "wins": 5
        }
      },
      "metrics": {
        "C0": {
          "mrr": {
            "mean": 0.6792374307372457,
            "std": 0.05223880121690982,
            "median": 0.6673798542887109,
            "min": 0.6373259848401722,
            "max": 0.7666469641159896,
            "per_seed": [
              0.6673798542887109,
              0.7666469641159896,
              0.6373259848401722,
              0.6825682232967468,
              0.6422661271446087
            ]
          },
          "hits10": {
            "mean": 0.8975332068311195,
            "std": 0.048932815780750004,
            "median": 0.8766603415559773,
            "min": 0.8614800759013282,
            "max": 0.9829222011385199,
            "per_seed": [
              0.8747628083491461,
              0.9829222011385199,
              0.8918406072106262,
              0.8766603415559773,
              0.8614800759013282
            ]
          },
          "hits20": {
            "mean": 0.9870967741935484,
            "std": 0.009619576361014478,
            "median": 0.9829222011385199,
            "min": 0.9772296015180265,
            "max": 1.0,
            "per_seed": [
              0.9772296015180265,
              1.0,
              0.9943074003795066,
              0.9810246679316889,
              0.9829222011385199
            ]
          },
          "mean_positive_rank": {
            "mean": 3.5370018975332065,
            "std": 0.8414260064916017,
            "median": 3.825426944971537,
            "min": 2.0607210626185957,
            "max": 4.16888045540797,
            "per_seed": [
              3.903225806451613,
              2.0607210626185957,
              3.7267552182163186,
              3.825426944971537,
              4.16888045540797
            ]
          }
        },
        "C1": {
          "mrr": {
            "mean": 0.7050901133981805,
            "std": 0.04064610118279473,
            "median": 0.6868758437808378,
            "min": 0.6789811783593396,
            "max": 0.7761257311848896,
            "per_seed": [
              0.7015357065892106,
              0.7761257311848896,
              0.681932107076625,
              0.6868758437808378,
              0.6789811783593396
            ]
          },
          "hits10": {
            "mean": 0.9096774193548388,
            "std": 0.041801756435935845,
            "median": 0.9032258064516129,
            "min": 0.8766603415559773,
            "max": 0.9810246679316889,
            "per_seed": [
              0.905123339658444,
              0.9810246679316889,
              0.9032258064516129,
              0.8823529411764706,
              0.8766603415559773
            ]
          },
          "hits20": {
            "mean": 0.9893738140417458,
            "std": 0.006920145172224087,
            "median": 0.9867172675521821,
            "min": 0.9829222011385199,
            "max": 1.0,
            "per_seed": [
              0.9867172675521821,
              1.0,
              0.9924098671726755,
              0.9829222011385199,
              0.9848197343453511
            ]
          },
          "mean_positive_rank": {
            "mean": 3.259203036053131,
            "std": 0.736747171726482,
            "median": 3.407969639468691,
            "min": 1.984819734345351,
            "max": 3.823529411764706,
            "per_seed": [
              3.383301707779886,
              1.984819734345351,
              3.407969639468691,
              3.6963946869070208,
              3.823529411764706
            ]
          }
        },
        "C2": {
          "mrr": {
            "mean": 0.6771019108806603,
            "std": 0.05320967799178234,
            "median": 0.6672070739342845,
            "min": 0.6297251378621334,
            "max": 0.7653100465160964,
            "per_seed": [
              0.6672070739342845,
              0.7653100465160964,
              0.6297251378621334,
              0.680652104943247,
              0.6426151911475403
            ]
          },
          "hits10": {
            "mean": 0.8986717267552182,
            "std": 0.050250606082624404,
            "median": 0.8766603415559773,
            "min": 0.8595825426944972,
            "max": 0.9848197343453511,
            "per_seed": [
              0.872865275142315,
              0.9848197343453511,
              0.8994307400379506,
              0.8766603415559773,
              0.8595825426944972
            ]
          },
          "hits20": {
            "mean": 0.9874762808349147,
            "std": 0.009159406744703719,
            "median": 0.9829222011385199,
            "min": 0.9791271347248577,
            "max": 1.0,
            "per_seed": [
              0.9791271347248577,
              1.0,
              0.9943074003795066,
              0.9829222011385199,
              0.9810246679316889
            ]
          },
          "mean_positive_rank": {
            "mean": 3.5373814041745733,
            "std": 0.8406365512032236,
            "median": 3.844402277039848,
            "min": 2.066413662239089,
            "max": 4.16888045540797,
            "per_seed": [
              3.9222011385199242,
              2.066413662239089,
              3.685009487666034,
              3.844402277039848,
              4.16888045540797
            ]
          }
        },
        "N0": {
          "mrr": {
            "mean": 0.7142296611223624,
            "std": 0.04502090786008005,
            "median": 0.7042693255811056,
            "min": 0.6750088571415699,
            "max": 0.7875291954513965,
            "per_seed": [
              0.6750088571415699,
              0.7875291954513965,
              0.6820908893670188,
              0.7222500380707212,
              0.7042693255811056
            ]
          },
          "hits10": {
            "mean": 0.9388994307400379,
            "std": 0.03583776682600713,
            "median": 0.9354838709677419,
            "min": 0.8956356736242884,
            "max": 0.9829222011385199,
            "per_seed": [
              0.8956356736242884,
              0.9829222011385199,
              0.9146110056925996,
              0.9658444022770398,
              0.9354838709677419
            ]
          },
          "hits20": {
            "mean": 0.9992409867172676,
            "std": 0.0016972052960150161,
            "median": 1.0,
            "min": 0.9962049335863378,
            "max": 1.0,
            "per_seed": [
              0.9962049335863378,
              1.0,
              1.0,
              1.0,
              1.0
            ]
          },
          "mean_positive_rank": {
            "mean": 2.831878557874763,
            "std": 0.613768548067961,
            "median": 2.905123339658444,
            "min": 1.9601518026565465,
            "max": 3.5161290322580645,
            "per_seed": [
              3.5161290322580645,
              1.9601518026565465,
              3.25426944971537,
              2.523719165085389,
              2.905123339658444
            ]
          }
        },
        "N1": {
          "mrr": {
            "mean": 0.7311714358935324,
            "std": 0.040107195095352745,
            "median": 0.7254910716451889,
            "min": 0.6960280276933333,
            "max": 0.7946586688354743,
            "per_seed": [
              0.6960280276933333,
              0.7946586688354743,
              0.6988685618016018,
              0.7408108494920639,
              0.7254910716451889
            ]
          },
          "hits10": {
            "mean": 0.9495256166982923,
            "std": 0.02685529079877309,
            "median": 0.9468690702087287,
            "min": 0.9222011385199241,
            "max": 0.9848197343453511,
            "per_seed": [
              0.9222011385199241,
              0.9848197343453511,
              0.9259962049335864,
              0.967741935483871,
              0.9468690702087287
            ]
          },
          "hits20": {
            "mean": 0.9992409867172676,
            "std": 0.0016972052960150161,
            "median": 1.0,
            "min": 0.9962049335863378,
            "max": 1.0,
            "per_seed": [
              0.9962049335863378,
              1.0,
              1.0,
              1.0,
              1.0
            ]
          },
          "mean_positive_rank": {
            "mean": 2.624288425047438,
            "std": 0.48056128944730025,
            "median": 2.6755218216318783,
            "min": 1.9259962049335864,
            "max": 3.1252371916508537,
            "per_seed": [
              3.1252371916508537,
              1.9259962049335864,
              2.9905123339658446,
              2.4041745730550286,
              2.6755218216318783
            ]
          }
        }
      },
      "pass": true
    },
    "pubmed": {
      "seeds": [
        0,
        1,
        2,
        3,
        4
      ],
      "seed_results": [
        {
          "seed": 0,
          "arms": {
            "C0": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 0,
              "arm": "C0",
              "epochs": 10,
              "metrics": {
                "mrr": 0.9048059810977229,
                "hits10": 0.9986462093862816,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.2655685920577617
              },
              "checkpoint_sha256": "80de9b501a7678c090a9991cd2052ac2b09385cdcab9415ff984304a894eeadb",
              "inference_seconds": 2.1210471321828663,
              "peak_gpu_mb": 178.037109375,
              "test_candidate_metadata": {
                "n": 19717,
                "feature_shape": [
                  19717,
                  500
                ],
                "train_edges": 37676,
                "train_hash": "2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1",
                "valid_positive_hash": "eb16f89cdf1fd225e09a8f08d45139dce12ac919d94946bdb7af76e7672f60d8",
                "valid_negative_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
                "test_positive_hash": "d5cb8058bb34feb90727a399dc8c19cccb2dbf85b032e08ca3e0292c905dd1e0",
                "test_negative_hash": "1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b",
                "test_cache_sha256": "b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2",
                "test_queries": 4432,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "C1": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 0,
              "arm": "C1",
              "epochs": 10,
              "metrics": {
                "mrr": 0.9124168012593104,
                "hits10": 0.9988718411552346,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.2495487364620939
              },
              "checkpoint_sha256": "6dfc6ca45d0d1288f045385785b498b16e30d6339395cd26a42b214a50a37d9f",
              "inference_seconds": 3.925699109211564,
              "peak_gpu_mb": 194.52783203125,
              "test_candidate_metadata": {
                "n": 19717,
                "feature_shape": [
                  19717,
                  500
                ],
                "train_edges": 37676,
                "train_hash": "2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1",
                "valid_positive_hash": "eb16f89cdf1fd225e09a8f08d45139dce12ac919d94946bdb7af76e7672f60d8",
                "valid_negative_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
                "test_positive_hash": "d5cb8058bb34feb90727a399dc8c19cccb2dbf85b032e08ca3e0292c905dd1e0",
                "test_negative_hash": "1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b",
                "test_cache_sha256": "b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2",
                "test_queries": 4432,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "C2": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 0,
              "arm": "C2",
              "epochs": 10,
              "metrics": {
                "mrr": 0.9057034722197177,
                "hits10": 0.9986462093862816,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.2637635379061372
              },
              "checkpoint_sha256": "8a66612827ae3a7a4440b971121c89e779ace39a0d4e6f5fc72e8a57cfb14b85",
              "inference_seconds": 3.2011876651085913,
              "peak_gpu_mb": 178.041015625,
              "test_candidate_metadata": {
                "n": 19717,
                "feature_shape": [
                  19717,
                  500
                ],
                "train_edges": 37676,
                "train_hash": "2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1",
                "valid_positive_hash": "eb16f89cdf1fd225e09a8f08d45139dce12ac919d94946bdb7af76e7672f60d8",
                "valid_negative_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
                "test_positive_hash": "d5cb8058bb34feb90727a399dc8c19cccb2dbf85b032e08ca3e0292c905dd1e0",
                "test_negative_hash": "1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b",
                "test_cache_sha256": "b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2",
                "test_queries": 4432,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "N0": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 0,
              "arm": "N0",
              "epochs": 10,
              "metrics": {
                "mrr": 0.9081361741447482,
                "hits10": 0.9995487364620939,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.2642148014440433
              },
              "checkpoint_sha256": "fb2784b14989c1294ebd460f58c7bf502ffd79156b50e65a4620167500a041b2",
              "inference_seconds": 0.21993391402065754,
              "peak_gpu_mb": 149.56689453125,
              "test_candidate_metadata": {
                "n": 19717,
                "feature_shape": [
                  19717,
                  500
                ],
                "train_edges": 37676,
                "train_hash": "2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1",
                "valid_positive_hash": "eb16f89cdf1fd225e09a8f08d45139dce12ac919d94946bdb7af76e7672f60d8",
                "valid_negative_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
                "test_positive_hash": "d5cb8058bb34feb90727a399dc8c19cccb2dbf85b032e08ca3e0292c905dd1e0",
                "test_negative_hash": "1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b",
                "test_cache_sha256": "b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2",
                "test_queries": 4432,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "N1": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 0,
              "arm": "N1",
              "epochs": 10,
              "metrics": {
                "mrr": 0.9099491832625857,
                "hits10": 0.9995487364620939,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.2606046931407942
              },
              "checkpoint_sha256": "7e12d4fdfc355d0974576fcd7e6dba0cb273bbe57ad914ac7e163d6be57fb663",
              "inference_seconds": 0.3085206258110702,
              "peak_gpu_mb": 166.0576171875,
              "test_candidate_metadata": {
                "n": 19717,
                "feature_shape": [
                  19717,
                  500
                ],
                "train_edges": 37676,
                "train_hash": "2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1",
                "valid_positive_hash": "eb16f89cdf1fd225e09a8f08d45139dce12ac919d94946bdb7af76e7672f60d8",
                "valid_negative_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
                "test_positive_hash": "d5cb8058bb34feb90727a399dc8c19cccb2dbf85b032e08ca3e0292c905dd1e0",
                "test_negative_hash": "1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b",
                "test_cache_sha256": "b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2",
                "test_queries": 4432,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            }
          }
        },
        {
          "seed": 1,
          "arms": {
            "C0": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 1,
              "arm": "C0",
              "epochs": 10,
              "metrics": {
                "mrr": 0.9102684701229375,
                "hits10": 0.9990974729241877,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.2518050541516246
              },
              "checkpoint_sha256": "3d54460f96977822c1c8182ec16319bc52d79a620f56b3c2e51e1e0cf05910de",
              "inference_seconds": 3.5608048858121037,
              "peak_gpu_mb": 178.037109375,
              "test_candidate_metadata": {
                "n": 19717,
                "feature_shape": [
                  19717,
                  500
                ],
                "train_edges": 37676,
                "train_hash": "2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1",
                "valid_positive_hash": "eb16f89cdf1fd225e09a8f08d45139dce12ac919d94946bdb7af76e7672f60d8",
                "valid_negative_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
                "test_positive_hash": "d5cb8058bb34feb90727a399dc8c19cccb2dbf85b032e08ca3e0292c905dd1e0",
                "test_negative_hash": "1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b",
                "test_cache_sha256": "b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2",
                "test_queries": 4432,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "C1": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 1,
              "arm": "C1",
              "epochs": 10,
              "metrics": {
                "mrr": 0.9152110618773525,
                "hits10": 0.9986462093862816,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.2450361010830324
              },
              "checkpoint_sha256": "bb2d08950c64959064270fe2850f7d93a2fb24d30c8a6e25ed0b4ede67f20b0b",
              "inference_seconds": 3.697458161972463,
              "peak_gpu_mb": 194.52783203125,
              "test_candidate_metadata": {
                "n": 19717,
                "feature_shape": [
                  19717,
                  500
                ],
                "train_edges": 37676,
                "train_hash": "2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1",
                "valid_positive_hash": "eb16f89cdf1fd225e09a8f08d45139dce12ac919d94946bdb7af76e7672f60d8",
                "valid_negative_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
                "test_positive_hash": "d5cb8058bb34feb90727a399dc8c19cccb2dbf85b032e08ca3e0292c905dd1e0",
                "test_negative_hash": "1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b",
                "test_cache_sha256": "b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2",
                "test_queries": 4432,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "C2": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 1,
              "arm": "C2",
              "epochs": 10,
              "metrics": {
                "mrr": 0.9120406725494722,
                "hits10": 0.9986462093862816,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.2495487364620939
              },
              "checkpoint_sha256": "2ee63fa1d289688aabc06e2ec1d7c4b7881f57b0210172b70927670201b3e722",
              "inference_seconds": 2.4613252892158926,
              "peak_gpu_mb": 178.041015625,
              "test_candidate_metadata": {
                "n": 19717,
                "feature_shape": [
                  19717,
                  500
                ],
                "train_edges": 37676,
                "train_hash": "2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1",
                "valid_positive_hash": "eb16f89cdf1fd225e09a8f08d45139dce12ac919d94946bdb7af76e7672f60d8",
                "valid_negative_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
                "test_positive_hash": "d5cb8058bb34feb90727a399dc8c19cccb2dbf85b032e08ca3e0292c905dd1e0",
                "test_negative_hash": "1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b",
                "test_cache_sha256": "b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2",
                "test_queries": 4432,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "N0": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 1,
              "arm": "N0",
              "epochs": 10,
              "metrics": {
                "mrr": 0.9105377956630213,
                "hits10": 0.9995487364620939,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.25293321299639
              },
              "checkpoint_sha256": "bcd90c09ea1d2f3477f6e14339122d2b1fe7d6652fa6955ea7ad30ae318da031",
              "inference_seconds": 0.222978041972965,
              "peak_gpu_mb": 149.56689453125,
              "test_candidate_metadata": {
                "n": 19717,
                "feature_shape": [
                  19717,
                  500
                ],
                "train_edges": 37676,
                "train_hash": "2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1",
                "valid_positive_hash": "eb16f89cdf1fd225e09a8f08d45139dce12ac919d94946bdb7af76e7672f60d8",
                "valid_negative_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
                "test_positive_hash": "d5cb8058bb34feb90727a399dc8c19cccb2dbf85b032e08ca3e0292c905dd1e0",
                "test_negative_hash": "1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b",
                "test_cache_sha256": "b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2",
                "test_queries": 4432,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "N1": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 1,
              "arm": "N1",
              "epochs": 10,
              "metrics": {
                "mrr": 0.9179565145043485,
                "hits10": 0.9995487364620939,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.2375902527075813
              },
              "checkpoint_sha256": "2b204d1ea28a4c3a97f3f0e2a9455d88e1252ffda7924967b23ed150827fcf67",
              "inference_seconds": 0.33443978196009994,
              "peak_gpu_mb": 166.0576171875,
              "test_candidate_metadata": {
                "n": 19717,
                "feature_shape": [
                  19717,
                  500
                ],
                "train_edges": 37676,
                "train_hash": "2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1",
                "valid_positive_hash": "eb16f89cdf1fd225e09a8f08d45139dce12ac919d94946bdb7af76e7672f60d8",
                "valid_negative_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
                "test_positive_hash": "d5cb8058bb34feb90727a399dc8c19cccb2dbf85b032e08ca3e0292c905dd1e0",
                "test_negative_hash": "1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b",
                "test_cache_sha256": "b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2",
                "test_queries": 4432,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            }
          }
        },
        {
          "seed": 2,
          "arms": {
            "C0": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 2,
              "arm": "C0",
              "epochs": 10,
              "metrics": {
                "mrr": 0.894597627477817,
                "hits10": 0.9993231046931408,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.3037003610108304
              },
              "checkpoint_sha256": "1bb8fee702d3f46723e946b4654eeb8f3050286b2c9ba0868420a62cde6c07b7",
              "inference_seconds": 2.1622748929075897,
              "peak_gpu_mb": 178.037109375,
              "test_candidate_metadata": {
                "n": 19717,
                "feature_shape": [
                  19717,
                  500
                ],
                "train_edges": 37676,
                "train_hash": "2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1",
                "valid_positive_hash": "eb16f89cdf1fd225e09a8f08d45139dce12ac919d94946bdb7af76e7672f60d8",
                "valid_negative_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
                "test_positive_hash": "d5cb8058bb34feb90727a399dc8c19cccb2dbf85b032e08ca3e0292c905dd1e0",
                "test_negative_hash": "1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b",
                "test_cache_sha256": "b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2",
                "test_queries": 4432,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "C1": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 2,
              "arm": "C1",
              "epochs": 10,
              "metrics": {
                "mrr": 0.9037479129875339,
                "hits10": 0.9993231046931408,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.2745938628158844
              },
              "checkpoint_sha256": "8757f21ace66372604dd89cec50b1e5cfe1a90d93371a9898aa96006cc299c86",
              "inference_seconds": 3.820590502116829,
              "peak_gpu_mb": 194.52783203125,
              "test_candidate_metadata": {
                "n": 19717,
                "feature_shape": [
                  19717,
                  500
                ],
                "train_edges": 37676,
                "train_hash": "2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1",
                "valid_positive_hash": "eb16f89cdf1fd225e09a8f08d45139dce12ac919d94946bdb7af76e7672f60d8",
                "valid_negative_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
                "test_positive_hash": "d5cb8058bb34feb90727a399dc8c19cccb2dbf85b032e08ca3e0292c905dd1e0",
                "test_negative_hash": "1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b",
                "test_cache_sha256": "b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2",
                "test_queries": 4432,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "C2": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 2,
              "arm": "C2",
              "epochs": 10,
              "metrics": {
                "mrr": 0.892208253038578,
                "hits10": 0.9990974729241877,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.3088898916967509
              },
              "checkpoint_sha256": "ed857246e8081fb73e2decff877e210bcfed6f03233511b5ff90dca1200e1da2",
              "inference_seconds": 3.7339071123860776,
              "peak_gpu_mb": 178.041015625,
              "test_candidate_metadata": {
                "n": 19717,
                "feature_shape": [
                  19717,
                  500
                ],
                "train_edges": 37676,
                "train_hash": "2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1",
                "valid_positive_hash": "eb16f89cdf1fd225e09a8f08d45139dce12ac919d94946bdb7af76e7672f60d8",
                "valid_negative_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
                "test_positive_hash": "d5cb8058bb34feb90727a399dc8c19cccb2dbf85b032e08ca3e0292c905dd1e0",
                "test_negative_hash": "1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b",
                "test_cache_sha256": "b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2",
                "test_queries": 4432,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "N0": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 2,
              "arm": "N0",
              "epochs": 10,
              "metrics": {
                "mrr": 0.8935618839894561,
                "hits10": 0.9995487364620939,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.3102436823104693
              },
              "checkpoint_sha256": "e93e337c1642abb39db8e45ded296081206b27fce387620438f1c3a530240921",
              "inference_seconds": 0.22558203991502523,
              "peak_gpu_mb": 149.56689453125,
              "test_candidate_metadata": {
                "n": 19717,
                "feature_shape": [
                  19717,
                  500
                ],
                "train_edges": 37676,
                "train_hash": "2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1",
                "valid_positive_hash": "eb16f89cdf1fd225e09a8f08d45139dce12ac919d94946bdb7af76e7672f60d8",
                "valid_negative_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
                "test_positive_hash": "d5cb8058bb34feb90727a399dc8c19cccb2dbf85b032e08ca3e0292c905dd1e0",
                "test_negative_hash": "1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b",
                "test_cache_sha256": "b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2",
                "test_queries": 4432,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "N1": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 2,
              "arm": "N1",
              "epochs": 10,
              "metrics": {
                "mrr": 0.9033362026311033,
                "hits10": 0.9995487364620939,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.279332129963899
              },
              "checkpoint_sha256": "20a6fa9b0045f65b846fc3eed70645017d13ce5b2ecd22e1e41126a3185e58e5",
              "inference_seconds": 0.29142609471455216,
              "peak_gpu_mb": 166.0576171875,
              "test_candidate_metadata": {
                "n": 19717,
                "feature_shape": [
                  19717,
                  500
                ],
                "train_edges": 37676,
                "train_hash": "2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1",
                "valid_positive_hash": "eb16f89cdf1fd225e09a8f08d45139dce12ac919d94946bdb7af76e7672f60d8",
                "valid_negative_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
                "test_positive_hash": "d5cb8058bb34feb90727a399dc8c19cccb2dbf85b032e08ca3e0292c905dd1e0",
                "test_negative_hash": "1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b",
                "test_cache_sha256": "b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2",
                "test_queries": 4432,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            }
          }
        },
        {
          "seed": 3,
          "arms": {
            "C0": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 3,
              "arm": "C0",
              "epochs": 10,
              "metrics": {
                "mrr": 0.9107584525257133,
                "hits10": 0.9988718411552346,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.24706678700361
              },
              "checkpoint_sha256": "0f26f5b08b1fd5bbac268c3de51fdbe8f3fb33b64f472717adf736450036904a",
              "inference_seconds": 3.1557655460201204,
              "peak_gpu_mb": 178.037109375,
              "test_candidate_metadata": {
                "n": 19717,
                "feature_shape": [
                  19717,
                  500
                ],
                "train_edges": 37676,
                "train_hash": "2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1",
                "valid_positive_hash": "eb16f89cdf1fd225e09a8f08d45139dce12ac919d94946bdb7af76e7672f60d8",
                "valid_negative_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
                "test_positive_hash": "d5cb8058bb34feb90727a399dc8c19cccb2dbf85b032e08ca3e0292c905dd1e0",
                "test_negative_hash": "1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b",
                "test_cache_sha256": "b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2",
                "test_queries": 4432,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "C1": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 3,
              "arm": "C1",
              "epochs": 10,
              "metrics": {
                "mrr": 0.9148848024468512,
                "hits10": 0.9993231046931408,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.236913357400722
              },
              "checkpoint_sha256": "02613337b6a34eeb5517d8ed2472bd0faf03e2dcdbd3f28dfc677317d200813b",
              "inference_seconds": 3.5626805890351534,
              "peak_gpu_mb": 194.52783203125,
              "test_candidate_metadata": {
                "n": 19717,
                "feature_shape": [
                  19717,
                  500
                ],
                "train_edges": 37676,
                "train_hash": "2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1",
                "valid_positive_hash": "eb16f89cdf1fd225e09a8f08d45139dce12ac919d94946bdb7af76e7672f60d8",
                "valid_negative_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
                "test_positive_hash": "d5cb8058bb34feb90727a399dc8c19cccb2dbf85b032e08ca3e0292c905dd1e0",
                "test_negative_hash": "1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b",
                "test_cache_sha256": "b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2",
                "test_queries": 4432,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "C2": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 3,
              "arm": "C2",
              "epochs": 10,
              "metrics": {
                "mrr": 0.9126433559420924,
                "hits10": 0.9990974729241877,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.2472924187725631
              },
              "checkpoint_sha256": "6c6d14612c914adbd5e979dbdc938b7d8e53e09d79893271f3b6a7651edec666",
              "inference_seconds": 2.06213508406654,
              "peak_gpu_mb": 178.041015625,
              "test_candidate_metadata": {
                "n": 19717,
                "feature_shape": [
                  19717,
                  500
                ],
                "train_edges": 37676,
                "train_hash": "2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1",
                "valid_positive_hash": "eb16f89cdf1fd225e09a8f08d45139dce12ac919d94946bdb7af76e7672f60d8",
                "valid_negative_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
                "test_positive_hash": "d5cb8058bb34feb90727a399dc8c19cccb2dbf85b032e08ca3e0292c905dd1e0",
                "test_negative_hash": "1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b",
                "test_cache_sha256": "b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2",
                "test_queries": 4432,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "N0": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 3,
              "arm": "N0",
              "epochs": 10,
              "metrics": {
                "mrr": 0.9148170177445899,
                "hits10": 0.9990974729241877,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.2463898916967509
              },
              "checkpoint_sha256": "cee5e17b519661ac71073f0a205d2965274a893f2c5256017f7c4fe72b024fa2",
              "inference_seconds": 0.2249432811513543,
              "peak_gpu_mb": 149.56689453125,
              "test_candidate_metadata": {
                "n": 19717,
                "feature_shape": [
                  19717,
                  500
                ],
                "train_edges": 37676,
                "train_hash": "2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1",
                "valid_positive_hash": "eb16f89cdf1fd225e09a8f08d45139dce12ac919d94946bdb7af76e7672f60d8",
                "valid_negative_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
                "test_positive_hash": "d5cb8058bb34feb90727a399dc8c19cccb2dbf85b032e08ca3e0292c905dd1e0",
                "test_negative_hash": "1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b",
                "test_cache_sha256": "b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2",
                "test_queries": 4432,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "N1": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 3,
              "arm": "N1",
              "epochs": 10,
              "metrics": {
                "mrr": 0.9169128861761985,
                "hits10": 0.9990974729241877,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.2371389891696751
              },
              "checkpoint_sha256": "d532ec6854864f1f59eafb9a70934964bc9701e4ca596ed66fa5f048783e392a",
              "inference_seconds": 0.35201057186350226,
              "peak_gpu_mb": 166.0576171875,
              "test_candidate_metadata": {
                "n": 19717,
                "feature_shape": [
                  19717,
                  500
                ],
                "train_edges": 37676,
                "train_hash": "2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1",
                "valid_positive_hash": "eb16f89cdf1fd225e09a8f08d45139dce12ac919d94946bdb7af76e7672f60d8",
                "valid_negative_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
                "test_positive_hash": "d5cb8058bb34feb90727a399dc8c19cccb2dbf85b032e08ca3e0292c905dd1e0",
                "test_negative_hash": "1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b",
                "test_cache_sha256": "b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2",
                "test_queries": 4432,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            }
          }
        },
        {
          "seed": 4,
          "arms": {
            "C0": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 4,
              "arm": "C0",
              "epochs": 10,
              "metrics": {
                "mrr": 0.8729048732179373,
                "hits10": 0.9986462093862816,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.3713898916967509
              },
              "checkpoint_sha256": "81181b1c1dc07cf2cd5a0747e44ffeb897d6c3077f5d54cc86e20b7e1382b89e",
              "inference_seconds": 2.1492692050524056,
              "peak_gpu_mb": 178.037109375,
              "test_candidate_metadata": {
                "n": 19717,
                "feature_shape": [
                  19717,
                  500
                ],
                "train_edges": 37676,
                "train_hash": "2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1",
                "valid_positive_hash": "eb16f89cdf1fd225e09a8f08d45139dce12ac919d94946bdb7af76e7672f60d8",
                "valid_negative_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
                "test_positive_hash": "d5cb8058bb34feb90727a399dc8c19cccb2dbf85b032e08ca3e0292c905dd1e0",
                "test_negative_hash": "1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b",
                "test_cache_sha256": "b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2",
                "test_queries": 4432,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "C1": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 4,
              "arm": "C1",
              "epochs": 10,
              "metrics": {
                "mrr": 0.882759399270004,
                "hits10": 0.9986462093862816,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.3431859205776173
              },
              "checkpoint_sha256": "589959579ad5f6610a72427147f087f23dd622e2852d321fa9053372476a4307",
              "inference_seconds": 3.6584997391328216,
              "peak_gpu_mb": 194.52783203125,
              "test_candidate_metadata": {
                "n": 19717,
                "feature_shape": [
                  19717,
                  500
                ],
                "train_edges": 37676,
                "train_hash": "2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1",
                "valid_positive_hash": "eb16f89cdf1fd225e09a8f08d45139dce12ac919d94946bdb7af76e7672f60d8",
                "valid_negative_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
                "test_positive_hash": "d5cb8058bb34feb90727a399dc8c19cccb2dbf85b032e08ca3e0292c905dd1e0",
                "test_negative_hash": "1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b",
                "test_cache_sha256": "b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2",
                "test_queries": 4432,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "C2": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 4,
              "arm": "C2",
              "epochs": 10,
              "metrics": {
                "mrr": 0.8704034414492446,
                "hits10": 0.9984205776173285,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.3763537906137184
              },
              "checkpoint_sha256": "bd5d33bba77dc2117484e8ce902d335dac60a4de4cf3bf54f667a5509bdd7493",
              "inference_seconds": 3.269874766934663,
              "peak_gpu_mb": 178.041015625,
              "test_candidate_metadata": {
                "n": 19717,
                "feature_shape": [
                  19717,
                  500
                ],
                "train_edges": 37676,
                "train_hash": "2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1",
                "valid_positive_hash": "eb16f89cdf1fd225e09a8f08d45139dce12ac919d94946bdb7af76e7672f60d8",
                "valid_negative_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
                "test_positive_hash": "d5cb8058bb34feb90727a399dc8c19cccb2dbf85b032e08ca3e0292c905dd1e0",
                "test_negative_hash": "1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b",
                "test_cache_sha256": "b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2",
                "test_queries": 4432,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "N0": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 4,
              "arm": "N0",
              "epochs": 10,
              "metrics": {
                "mrr": 0.8772961166265544,
                "hits10": 0.9995487364620939,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.3788357400722022
              },
              "checkpoint_sha256": "b1c868ba1a27cbf1dd4345cd9025b7cceaaf4d377e0bb6af71eb61931280c406",
              "inference_seconds": 0.23049255134537816,
              "peak_gpu_mb": 149.56689453125,
              "test_candidate_metadata": {
                "n": 19717,
                "feature_shape": [
                  19717,
                  500
                ],
                "train_edges": 37676,
                "train_hash": "2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1",
                "valid_positive_hash": "eb16f89cdf1fd225e09a8f08d45139dce12ac919d94946bdb7af76e7672f60d8",
                "valid_negative_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
                "test_positive_hash": "d5cb8058bb34feb90727a399dc8c19cccb2dbf85b032e08ca3e0292c905dd1e0",
                "test_negative_hash": "1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b",
                "test_cache_sha256": "b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2",
                "test_queries": 4432,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            },
            "N1": {
              "state": "COMPLETE",
              "dataset": "pubmed",
              "seed": 4,
              "arm": "N1",
              "epochs": 10,
              "metrics": {
                "mrr": 0.8880036715484794,
                "hits10": 0.9993231046931408,
                "hits20": 1.0,
                "hits50": 1.0,
                "hits100": 1.0,
                "mean_positive_rank": 1.3375451263537905
              },
              "checkpoint_sha256": "7d4d8712dba0a9d1ac43bf8299f1c79f1cd90bc278b926346cb4de0fbd6fa040",
              "inference_seconds": 0.2886631628498435,
              "peak_gpu_mb": 166.0576171875,
              "test_candidate_metadata": {
                "n": 19717,
                "feature_shape": [
                  19717,
                  500
                ],
                "train_edges": 37676,
                "train_hash": "2e13bb54e6cd8682ea519ce1f4dc859e5b122af51ff549469434bcdad8325ee1",
                "valid_positive_hash": "eb16f89cdf1fd225e09a8f08d45139dce12ac919d94946bdb7af76e7672f60d8",
                "valid_negative_hash": "c630042ee5a0d407773d238b4b313d076e64f43736dd30a4337e9395edc74683",
                "test_positive_hash": "d5cb8058bb34feb90727a399dc8c19cccb2dbf85b032e08ca3e0292c905dd1e0",
                "test_negative_hash": "1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b",
                "test_cache_sha256": "b35e52370d34c048253eaed0ae511561c889ef02e5ad7a2cee1bf448d9a3c1d2",
                "test_queries": 4432,
                "test_negatives": 20,
                "projection": "undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges"
              },
              "configuration_frozen_before_test": true
            }
          }
        }
      ],
      "effects": {
        "delta_ncnc": {
          "mean": 0.007136914679784767,
          "std": 0.0025269652422456415,
          "median": 0.007610820161587428,
          "min": 0.004126349921137917,
          "max": 0.009854526052066714,
          "per_seed": [
            0.007610820161587428,
            0.004942591754414916,
            0.00915028550971686,
            0.004126349921137917,
            0.009854526052066714
          ],
          "wins": 5
        },
        "delta_null": {
          "mean": 0.007204156528389394,
          "std": 0.00464968619091962,
          "median": 0.006713329039592653,
          "min": 0.0022414465047587706,
          "max": 0.012355957820759378,
          "per_seed": [
            0.006713329039592653,
            0.003170389327880274,
            0.011539659948955894,
            0.0022414465047587706,
            0.012355957820759378
          ],
          "wins": 5
        },
        "delta_ncn": {
          "mean": 0.006361893990869061,
          "std": 0.004199333796861386,
          "median": 0.007418718841327165,
          "min": 0.0018130091178374386,
          "max": 0.010707554921924989,
          "per_seed": [
            0.0018130091178374386,
            0.007418718841327165,
            0.009774318641647128,
            0.002095868431608583,
            0.010707554921924989
          ],
          "wins": 5
        }
      },
      "metrics": {
        "C0": {
          "mrr": {
            "mean": 0.8986670808884256,
            "std": 0.015801355884384145,
            "median": 0.9048059810977229,
            "min": 0.8729048732179373,
            "max": 0.9107584525257133,
            "per_seed": [
              0.9048059810977229,
              0.9102684701229375,
              0.894597627477817,
              0.9107584525257133,
              0.8729048732179373
            ]
          },
          "hits10": {
            "mean": 0.9989169675090253,
            "std": 0.0002941878341697988,
            "median": 0.9988718411552346,
            "min": 0.9986462093862816,
            "max": 0.9993231046931408,
            "per_seed": [
              0.9986462093862816,
              0.9990974729241877,
              0.9993231046931408,
              0.9988718411552346,
              0.9986462093862816
            ]
          },
          "hits20": {
            "mean": 1.0,
            "std": 0.0,
            "median": 1.0,
            "min": 1.0,
            "max": 1.0,
            "per_seed": [
              1.0,
              1.0,
              1.0,
              1.0,
              1.0
            ]
          },
          "mean_positive_rank": {
            "mean": 1.2879061371841156,
            "std": 0.05169405530467448,
            "median": 1.2655685920577617,
            "min": 1.24706678700361,
            "max": 1.3713898916967509,
            "per_seed": [
              1.2655685920577617,
              1.2518050541516246,
              1.3037003610108304,
              1.24706678700361,
              1.3713898916967509
            ]
          }
        },
        "C1": {
          "mrr": {
            "mean": 0.9058039955682103,
            "std": 0.01369273569585237,
            "median": 0.9124168012593104,
            "min": 0.882759399270004,
            "max": 0.9152110618773525,
            "per_seed": [
              0.9124168012593104,
              0.9152110618773525,
              0.9037479129875339,
              0.9148848024468512,
              0.882759399270004
            ]
          },
          "hits10": {
            "mean": 0.9989620938628159,
            "std": 0.0003421875200384322,
            "median": 0.9988718411552346,
            "min": 0.9986462093862816,
            "max": 0.9993231046931408,
            "per_seed": [
              0.9988718411552346,
              0.9986462093862816,
              0.9993231046931408,
              0.9993231046931408,
              0.9986462093862816
            ]
          },
          "hits20": {
            "mean": 1.0,
            "std": 0.0,
            "median": 1.0,
            "min": 1.0,
            "max": 1.0,
            "per_seed": [
              1.0,
              1.0,
              1.0,
              1.0,
              1.0
            ]
          },
          "mean_positive_rank": {
            "mean": 1.2698555956678699,
            "std": 0.04333980454280627,
            "median": 1.2495487364620939,
            "min": 1.236913357400722,
            "max": 1.3431859205776173,
            "per_seed": [
              1.2495487364620939,
              1.2450361010830324,
              1.2745938628158844,
              1.236913357400722,
              1.3431859205776173
            ]
          }
        },
        "C2": {
          "mrr": {
            "mean": 0.8985998390398209,
            "std": 0.017777986285503634,
            "median": 0.9057034722197177,
            "min": 0.8704034414492446,
            "max": 0.9126433559420924,
            "per_seed": [
              0.9057034722197177,
              0.9120406725494722,
              0.892208253038578,
              0.9126433559420924,
              0.8704034414492446
            ]
          },
          "hits10": {
            "mean": 0.9987815884476534,
            "std": 0.00030271678395755704,
            "median": 0.9986462093862816,
            "min": 0.9984205776173285,
            "max": 0.9990974729241877,
            "per_seed": [
              0.9986462093862816,
              0.9986462093862816,
              0.9990974729241877,
              0.9990974729241877,
              0.9984205776173285
            ]
          },
          "hits20": {
            "mean": 1.0,
            "std": 0.0,
            "median": 1.0,
            "min": 1.0,
            "max": 1.0,
            "per_seed": [
              1.0,
              1.0,
              1.0,
              1.0,
              1.0
            ]
          },
          "mean_positive_rank": {
            "mean": 1.2891696750902528,
            "std": 0.05467849697026273,
            "median": 1.2637635379061372,
            "min": 1.2472924187725631,
            "max": 1.3763537906137184,
            "per_seed": [
              1.2637635379061372,
              1.2495487364620939,
              1.3088898916967509,
              1.2472924187725631,
              1.3763537906137184
            ]
          }
        },
        "N0": {
          "mrr": {
            "mean": 0.9008697976336739,
            "std": 0.015410381244272232,
            "median": 0.9081361741447482,
            "min": 0.8772961166265544,
            "max": 0.9148170177445899,
            "per_seed": [
              0.9081361741447482,
              0.9105377956630213,
              0.8935618839894561,
              0.9148170177445899,
              0.8772961166265544
            ]
          },
          "hits10": {
            "mean": 0.9994584837545126,
            "std": 0.00020181118930503804,
            "median": 0.9995487364620939,
            "min": 0.9990974729241877,
            "max": 0.9995487364620939,
            "per_seed": [
              0.9995487364620939,
              0.9995487364620939,
              0.9995487364620939,
              0.9990974729241877,
              0.9995487364620939
            ]
          },
          "hits20": {
            "mean": 1.0,
            "std": 0.0,
            "median": 1.0,
            "min": 1.0,
            "max": 1.0,
            "per_seed": [
              1.0,
              1.0,
              1.0,
              1.0,
              1.0
            ]
          },
          "mean_positive_rank": {
            "mean": 1.2905234657039713,
            "std": 0.055319277868364165,
            "median": 1.2642148014440433,
            "min": 1.2463898916967509,
            "max": 1.3788357400722022,
            "per_seed": [
              1.2642148014440433,
              1.25293321299639,
              1.3102436823104693,
              1.2463898916967509,
              1.3788357400722022
            ]
          }
        },
        "N1": {
          "mrr": {
            "mean": 0.9072316916245431,
            "std": 0.012257892407511888,
            "median": 0.9099491832625857,
            "min": 0.8880036715484794,
            "max": 0.9179565145043485,
            "per_seed": [
              0.9099491832625857,
              0.9179565145043485,
              0.9033362026311033,
              0.9169128861761985,
              0.8880036715484794
            ]
          },
          "hits10": {
            "mean": 0.999413357400722,
            "std": 0.00020181118930503804,
            "median": 0.9995487364620939,
            "min": 0.9990974729241877,
            "max": 0.9995487364620939,
            "per_seed": [
              0.9995487364620939,
              0.9995487364620939,
              0.9995487364620939,
              0.9990974729241877,
              0.9993231046931408
            ]
          },
          "hits20": {
            "mean": 1.0,
            "std": 0.0,
            "median": 1.0,
            "min": 1.0,
            "max": 1.0,
            "per_seed": [
              1.0,
              1.0,
              1.0,
              1.0,
              1.0
            ]
          },
          "mean_positive_rank": {
            "mean": 1.270442238267148,
            "std": 0.041433574591494604,
            "median": 1.2606046931407942,
            "min": 1.2371389891696751,
            "max": 1.3375451263537905,
            "per_seed": [
              1.2606046931407942,
              1.2375902527075813,
              1.279332129963899,
              1.2371389891696751,
              1.3375451263537905
            ]
          }
        }
      },
      "pass": true
    }
  },
  "passes": {
    "cora": true,
    "pubmed": true
  },
  "cora_pubmed_pass": true
}
