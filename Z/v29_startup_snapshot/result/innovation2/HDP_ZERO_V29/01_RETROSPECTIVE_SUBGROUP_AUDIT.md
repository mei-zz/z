# V29 retrospective diagnostic

Observed H0 score improvement is not incremental HDP information. Per-candidate vectors and positive-anchored full-population MRR retained.

{
  "state": "COMPLETE",
  "records": [
    {
      "dataset": "cora",
      "seed": 0,
      "subgroups": {
        "H0": {
          "candidate_count": 4865,
          "positive_count": 77,
          "negative_count": 4788,
          "positive_anchored_query_count": 77,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.0004971401195445866,
              "contribution_to_total_DeltaCE": 0.0004379117656317968,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.0005235450335139473,
              "contribution_to_total_DeltaCE": 0.00046117084701165196,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.00030711528177892393,
              "contribution_to_total_DeltaCE": 0.0002705261354072904,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.00039431053055318503,
              "contribution_to_total_DeltaCE": 0.00034733310359247603,
              "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 2.425099144109596e-05,
              "contribution_to_total_DeltaCE": 2.1361773195895677e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
            }
          }
        },
        "H1": {
          "candidate_count": 387,
          "positive_count": 70,
          "negative_count": 317,
          "positive_anchored_query_count": 70,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.0001092071841214853,
              "contribution_to_total_DeltaCE": -7.652214422418036e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 9.157509157509145e-05
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -8.296288359632203e-05,
              "contribution_to_total_DeltaCE": -5.813260175950865e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 9.157509157509145e-05
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.00030358586613118895,
              "contribution_to_total_DeltaCE": 2.1272447979860607e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 9.157509157509145e-05
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.0009209959393952807,
              "contribution_to_total_DeltaCE": 6.453475077783336e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 9.157509157509145e-05
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -0.0018446291199236463,
              "contribution_to_total_DeltaCE": -0.00012925429466059226,
              "DeltaMRR_positive_anchor_full_negative_population": 0.007142857142857143
            }
          }
        },
        "H2plus": {
          "candidate_count": 271,
          "positive_count": 116,
          "negative_count": 155,
          "positive_anchored_query_count": 116,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.0008246523260286009,
              "contribution_to_total_DeltaCE": -4.046365749660525e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.0010061721301331847,
              "contribution_to_total_DeltaCE": -4.9370386975573605e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0002977763189589537,
              "contribution_to_total_DeltaCE": 1.4611150178865914e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.002246058609133095,
              "contribution_to_total_DeltaCE": 0.00011020856112168545,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.01071200134343682,
              "contribution_to_total_DeltaCE": 0.0005256115089754441,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            }
          }
        },
        "G0": {
          "candidate_count": 4865,
          "positive_count": 77,
          "negative_count": 4788,
          "positive_anchored_query_count": 77,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.0004971401195445866,
              "contribution_to_total_DeltaCE": 0.0004379117656317968,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.0005235450335139473,
              "contribution_to_total_DeltaCE": 0.00046117084701165196,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.00030711528177892393,
              "contribution_to_total_DeltaCE": 0.0002705261354072904,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.00039431053055318503,
              "contribution_to_total_DeltaCE": 0.00034733310359247603,
              "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 2.425099144109596e-05,
              "contribution_to_total_DeltaCE": 2.1361773195895677e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
            }
          }
        },
        "G1": {
          "candidate_count": 234,
          "positive_count": 18,
          "negative_count": 216,
          "positive_anchored_query_count": 18,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.0002183596156576514,
              "contribution_to_total_DeltaCE": -9.251520924115594e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 0.00035612535612535566
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.00012852076069173345,
              "contribution_to_total_DeltaCE": 5.4452033318605155e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 0.00035612535612535566
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0005587093140580968,
              "contribution_to_total_DeltaCE": 2.3671551600506e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.00035612535612535566
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.000169955919332858,
              "contribution_to_total_DeltaCE": 7.200739656688172e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 0.00035612535612535566
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.0017376253031137115,
              "contribution_to_total_DeltaCE": 7.362019209281342e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            }
          }
        },
        "G2to3": {
          "candidate_count": 170,
          "positive_count": 35,
          "negative_count": 135,
          "positive_anchored_query_count": 35,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.001113559328746259,
              "contribution_to_total_DeltaCE": -3.4275771480511324e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.0013002788260639583,
              "contribution_to_total_DeltaCE": -4.0023067251651804e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0008850814149462818,
              "contribution_to_total_DeltaCE": 2.724313607475428e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.0026584375482766173,
              "contribution_to_total_DeltaCE": 8.182769929513398e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.010502668996544224,
              "contribution_to_total_DeltaCE": 0.0003232760690589386,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            }
          }
        },
        "G4plus": {
          "candidate_count": 254,
          "positive_count": 133,
          "negative_count": 121,
          "positive_anchored_query_count": 133,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -9.977450652760309e-05,
              "contribution_to_total_DeltaCE": -4.588579514396376e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.00044805409759394636,
              "contribution_to_total_DeltaCE": -2.0605783231733187e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -0.0003268374307079369,
              "contribution_to_total_DeltaCE": -1.5031089516533762e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.0018637922964178295,
              "contribution_to_total_DeltaCE": 8.571487294769666e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -1.1721085355115334e-05,
              "contribution_to_total_DeltaCE": -5.390468369001077e-07,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0037593984962406013
            }
          }
        },
        "MULT0": {
          "candidate_count": 4865,
          "positive_count": 77,
          "negative_count": 4788,
          "positive_anchored_query_count": 77,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.0004971401195445866,
              "contribution_to_total_DeltaCE": 0.0004379117656317968,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.0005235450335139473,
              "contribution_to_total_DeltaCE": 0.00046117084701165196,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.00030711528177892393,
              "contribution_to_total_DeltaCE": 0.0002705261354072904,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.00039431053055318503,
              "contribution_to_total_DeltaCE": 0.00034733310359247603,
              "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 2.425099144109596e-05,
              "contribution_to_total_DeltaCE": 2.1361773195895677e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
            }
          }
        },
        "MULT1to3": {
          "candidate_count": 372,
          "positive_count": 59,
          "negative_count": 313,
          "positive_anchored_query_count": 59,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -9.316611122400708e-05,
              "contribution_to_total_DeltaCE": -6.2751753350227476e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 0.00010864841373315934
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.000101610840962482,
              "contribution_to_total_DeltaCE": 6.843967560753812e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 0.00010864841373315934
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0005748502467016509,
              "contribution_to_total_DeltaCE": 3.871886506844363e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.00010864841373315934
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.001027421542815817,
              "contribution_to_total_DeltaCE": 6.920166828308599e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.00010864841373315934
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -0.0016291174328190504,
              "contribution_to_total_DeltaCE": -0.00010972871356304305,
              "DeltaMRR_positive_anchor_full_negative_population": 0.00847457627118644
            }
          }
        },
        "MULT4to15": {
          "candidate_count": 226,
          "positive_count": 91,
          "negative_count": 135,
          "positive_anchored_query_count": 91,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.0014056859444843588,
              "contribution_to_total_DeltaCE": -5.752037361098409e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.0017866533035969044,
              "contribution_to_total_DeltaCE": -7.310947793099772e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -0.0004834269945574228,
              "contribution_to_total_DeltaCE": -1.9781731082740823e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.0022789264267169163,
              "contribution_to_total_DeltaCE": 9.32531907365604e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.00840985457022502,
              "contribution_to_total_DeltaCE": 0.0003441294826852896,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            }
          }
        },
        "MULT16plus": {
          "candidate_count": 60,
          "positive_count": 36,
          "negative_count": 24,
          "positive_anchored_query_count": 36,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.001443314270333836,
              "contribution_to_total_DeltaCE": 1.567967702698355e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.0010200855092831233,
              "contribution_to_total_DeltaCE": 1.1081863218719427e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.001559922027126833,
              "contribution_to_total_DeltaCE": 1.6946464173023714e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.0011311520875922575,
              "contribution_to_total_DeltaCE": 1.2288452879872435e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.014908090779979314,
              "contribution_to_total_DeltaCE": 0.00016195644519260527,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            }
          }
        },
        "degree0to3": {
          "candidate_count": 138,
          "positive_count": 8,
          "negative_count": 130,
          "positive_anchored_query_count": 8,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.0007504543159857029,
              "contribution_to_total_DeltaCE": 1.875116704798606e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.0006779788202992005,
              "contribution_to_total_DeltaCE": 1.6940263842348303e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0005032112603972137,
              "contribution_to_total_DeltaCE": 1.2573448114216096e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.0005483438076640189,
              "contribution_to_total_DeltaCE": 1.3701148915016223e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 1.003167903087744e-05,
              "contribution_to_total_DeltaCE": 2.506557498209463e-07,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            }
          }
        },
        "degree4to15": {
          "candidate_count": 1607,
          "positive_count": 78,
          "negative_count": 1529,
          "positive_anchored_query_count": 78,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.0006080746108779511,
              "contribution_to_total_DeltaCE": 0.00017692846273417845,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.0005399545824310223,
              "contribution_to_total_DeltaCE": 0.00015710791489528388,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0004351095043262352,
              "contribution_to_total_DeltaCE": 0.00012660166095460076,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.0004770703295946172,
              "contribution_to_total_DeltaCE": 0.00013881079479604377,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -1.0672020259484778e-05,
              "contribution_to_total_DeltaCE": -3.105184964148477e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 0.00641025641025641
            }
          }
        },
        "degree16plus": {
          "candidate_count": 3778,
          "positive_count": 177,
          "negative_count": 3601,
          "positive_anchored_query_count": 177,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.0002837755758837357,
              "contribution_to_total_DeltaCE": 0.000194116263930609,
              "DeltaMRR_positive_anchor_full_negative_population": 3.6216137911053115e-05
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.00033906808196388076,
              "contribution_to_total_DeltaCE": 0.00023193902112249532,
              "DeltaMRR_positive_anchor_full_negative_population": 3.6216137911053115e-05
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.00024447772130705033,
              "contribution_to_total_DeltaCE": 0.0001672346244972001,
              "DeltaMRR_positive_anchor_full_negative_population": 3.6216137911053115e-05
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.0005402606081646647,
              "contribution_to_total_DeltaCE": 0.00036956447178093486,
              "DeltaMRR_positive_anchor_full_negative_population": 5.975662755323767e-05
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.0006148299451753811,
              "contribution_to_total_DeltaCE": 0.0004205735167250751,
              "DeltaMRR_positive_anchor_full_negative_population": 2.3540489642184554e-05
            }
          }
        }
      },
      "ranking_rule": "subgroup positive anchors, original full negative population; no filtered-negative ranking",
      "calibration_warning": "H0 uses a constant HDP raw block; improvements there do not prove incremental structural information",
      "all_pairwise_subgroups": {
        "GM_vs_GMH": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0004971401195445866,
            "contribution_to_total": -0.0004379117656317968,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.0001092071841214853,
            "contribution_to_total": 7.652214422418036e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -9.157509157509145e-05
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.0008246523260286009,
            "contribution_to_total": 4.046365749660525e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0004971401195445866,
            "contribution_to_total": -0.0004379117656317968,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.0002183596156576514,
            "contribution_to_total": 9.251520924115594e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00035612535612535566
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.001113559328746259,
            "contribution_to_total": 3.4275771480511324e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 9.977450652760309e-05,
            "contribution_to_total": 4.588579514396376e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0004971401195445866,
            "contribution_to_total": -0.0004379117656317968,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 9.316611122400708e-05,
            "contribution_to_total": 6.2751753350227476e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00010864841373315934
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.0014056859444843588,
            "contribution_to_total": 5.752037361098409e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.001443314270333836,
            "contribution_to_total": -1.567967702698355e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.0007504543159857029,
            "contribution_to_total": -1.875116704798606e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.0006080746108779511,
            "contribution_to_total": -0.00017692846273417845,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.0002837755758837357,
            "contribution_to_total": -0.000194116263930609,
            "DeltaMRR_positive_anchor_full_negative_population": -3.6216137911053115e-05
          }
        },
        "GM_vs_GMS": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0005235450335139473,
            "contribution_to_total": -0.00046117084701165196,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 8.296288359632203e-05,
            "contribution_to_total": 5.813260175950865e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -9.157509157509145e-05
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.0010061721301331847,
            "contribution_to_total": 4.9370386975573605e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0005235450335139473,
            "contribution_to_total": -0.00046117084701165196,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.00012852076069173345,
            "contribution_to_total": -5.4452033318605155e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00035612535612535566
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.0013002788260639583,
            "contribution_to_total": 4.0023067251651804e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.00044805409759394636,
            "contribution_to_total": 2.0605783231733187e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0005235450335139473,
            "contribution_to_total": -0.00046117084701165196,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.000101610840962482,
            "contribution_to_total": -6.843967560753812e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00010864841373315934
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.0017866533035969044,
            "contribution_to_total": 7.310947793099772e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.0010200855092831233,
            "contribution_to_total": -1.1081863218719427e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.0006779788202992005,
            "contribution_to_total": -1.6940263842348303e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.0005399545824310223,
            "contribution_to_total": -0.00015710791489528388,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.00033906808196388076,
            "contribution_to_total": -0.00023193902112249532,
            "DeltaMRR_positive_anchor_full_negative_population": -3.6216137911053115e-05
          }
        },
        "GM_vs_GMP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00030711528177892393,
            "contribution_to_total": -0.0002705261354072904,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.00030358586613118895,
            "contribution_to_total": -2.1272447979860607e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -9.157509157509145e-05
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.0002977763189589537,
            "contribution_to_total": -1.4611150178865914e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00030711528177892393,
            "contribution_to_total": -0.0002705261354072904,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.0005587093140580968,
            "contribution_to_total": -2.3671551600506e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00035612535612535566
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.0008850814149462818,
            "contribution_to_total": -2.724313607475428e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0003268374307079369,
            "contribution_to_total": 1.5031089516533762e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00030711528177892393,
            "contribution_to_total": -0.0002705261354072904,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.0005748502467016509,
            "contribution_to_total": -3.871886506844363e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00010864841373315934
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.0004834269945574228,
            "contribution_to_total": 1.9781731082740823e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.001559922027126833,
            "contribution_to_total": -1.6946464173023714e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.0005032112603972137,
            "contribution_to_total": -1.2573448114216096e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.0004351095043262352,
            "contribution_to_total": -0.00012660166095460076,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.00024447772130705033,
            "contribution_to_total": -0.0001672346244972001,
            "DeltaMRR_positive_anchor_full_negative_population": -3.6216137911053115e-05
          }
        },
        "GM_vs_GMG": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00039431053055318503,
            "contribution_to_total": -0.00034733310359247603,
            "DeltaMRR_positive_anchor_full_negative_population": -5.41125541125541e-05
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.0009209959393952807,
            "contribution_to_total": -6.453475077783336e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -9.157509157509145e-05
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.002246058609133095,
            "contribution_to_total": -0.00011020856112168545,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00039431053055318503,
            "contribution_to_total": -0.00034733310359247603,
            "DeltaMRR_positive_anchor_full_negative_population": -5.41125541125541e-05
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.000169955919332858,
            "contribution_to_total": -7.200739656688172e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00035612535612535566
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.0026584375482766173,
            "contribution_to_total": -8.182769929513398e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0018637922964178295,
            "contribution_to_total": -8.571487294769666e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00039431053055318503,
            "contribution_to_total": -0.00034733310359247603,
            "DeltaMRR_positive_anchor_full_negative_population": -5.41125541125541e-05
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.001027421542815817,
            "contribution_to_total": -6.920166828308599e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00010864841373315934
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.0022789264267169163,
            "contribution_to_total": -9.32531907365604e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.0011311520875922575,
            "contribution_to_total": -1.2288452879872435e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.0005483438076640189,
            "contribution_to_total": -1.3701148915016223e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.0004770703295946172,
            "contribution_to_total": -0.00013881079479604377,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.0005402606081646647,
            "contribution_to_total": -0.00036956447178093486,
            "DeltaMRR_positive_anchor_full_negative_population": -5.975662755323767e-05
          }
        },
        "GM_vs_GDUP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -2.425099144109596e-05,
            "contribution_to_total": -2.1361773195895677e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -5.41125541125541e-05
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.0018446291199236463,
            "contribution_to_total": 0.00012925429466059226,
            "DeltaMRR_positive_anchor_full_negative_population": -0.007142857142857143
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.01071200134343682,
            "contribution_to_total": -0.0005256115089754441,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -2.425099144109596e-05,
            "contribution_to_total": -2.1361773195895677e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -5.41125541125541e-05
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.0017376253031137115,
            "contribution_to_total": -7.362019209281342e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.010502668996544224,
            "contribution_to_total": -0.0003232760690589386,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 1.1721085355115334e-05,
            "contribution_to_total": 5.390468369001077e-07,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0037593984962406013
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -2.425099144109596e-05,
            "contribution_to_total": -2.1361773195895677e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -5.41125541125541e-05
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.0016291174328190504,
            "contribution_to_total": 0.00010972871356304305,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00847457627118644
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.00840985457022502,
            "contribution_to_total": -0.0003441294826852896,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.014908090779979314,
            "contribution_to_total": -0.00016195644519260527,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -1.003167903087744e-05,
            "contribution_to_total": -2.506557498209463e-07,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 1.0672020259484778e-05,
            "contribution_to_total": 3.105184964148477e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00641025641025641
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.0006148299451753811,
            "contribution_to_total": -0.0004205735167250751,
            "DeltaMRR_positive_anchor_full_negative_population": -2.3540489642184554e-05
          }
        },
        "GMH_vs_GM": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0004971401195445866,
            "contribution_to_total": 0.0004379117656317968,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.0001092071841214853,
            "contribution_to_total": -7.652214422418036e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 9.157509157509145e-05
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.0008246523260286009,
            "contribution_to_total": -4.046365749660525e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0004971401195445866,
            "contribution_to_total": 0.0004379117656317968,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.0002183596156576514,
            "contribution_to_total": -9.251520924115594e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00035612535612535566
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.001113559328746259,
            "contribution_to_total": -3.4275771480511324e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -9.977450652760309e-05,
            "contribution_to_total": -4.588579514396376e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0004971401195445866,
            "contribution_to_total": 0.0004379117656317968,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -9.316611122400708e-05,
            "contribution_to_total": -6.2751753350227476e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00010864841373315934
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.0014056859444843588,
            "contribution_to_total": -5.752037361098409e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.001443314270333836,
            "contribution_to_total": 1.567967702698355e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.0007504543159857029,
            "contribution_to_total": 1.875116704798606e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.0006080746108779511,
            "contribution_to_total": 0.00017692846273417845,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.0002837755758837357,
            "contribution_to_total": 0.000194116263930609,
            "DeltaMRR_positive_anchor_full_negative_population": 3.6216137911053115e-05
          }
        },
        "GMH_vs_GMS": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -2.6404913969360823e-05,
            "contribution_to_total": -2.3259081379855226e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -2.6244300525163275e-05,
            "contribution_to_total": -1.8389542464671714e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.00018151980410458383,
            "contribution_to_total": 8.906729478968353e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -2.6404913969360823e-05,
            "contribution_to_total": -2.3259081379855226e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.00034688037634938486,
            "contribution_to_total": -1.469672425597611e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.00018671949731769935,
            "contribution_to_total": 5.747295771140483e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0003482795910663433,
            "contribution_to_total": 1.601720371733681e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -2.6404913969360823e-05,
            "contribution_to_total": -2.3259081379855226e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.00019477695218648907,
            "contribution_to_total": -1.3119142895776559e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.0003809673591125451,
            "contribution_to_total": 1.5589104320013615e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.00042322876105071273,
            "contribution_to_total": 4.597813808264126e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 7.24754956865024e-05,
            "contribution_to_total": 1.8109032056377567e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 6.81200284469288e-05,
            "contribution_to_total": 1.982054783889455e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -5.5292506080145135e-05,
            "contribution_to_total": -3.782275719188635e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMH_vs_GMP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0001900248377656626,
            "contribution_to_total": 0.00016738563022450635,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.00041279305025267426,
            "contribution_to_total": -2.8924662402278644e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.0011224286449875544,
            "contribution_to_total": -5.507480767547116e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0001900248377656626,
            "contribution_to_total": 0.00016738563022450635,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.0007770689297157482,
            "contribution_to_total": -3.29230725246216e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.0019986407436925406,
            "contribution_to_total": -6.15189075552656e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.00022706292418033379,
            "contribution_to_total": 1.0442510002137385e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0001900248377656626,
            "contribution_to_total": 0.00016738563022450635,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.000668016357925658,
            "contribution_to_total": -4.499404040346637e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.0009222589499269364,
            "contribution_to_total": -3.773864252824328e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.00011660775679299684,
            "contribution_to_total": -1.2667871460401613e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.00024724305558848923,
            "contribution_to_total": 6.177718933769964e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.00017296510655171599,
            "contribution_to_total": 5.0326801779577686e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 3.929785457668536e-05,
            "contribution_to_total": 2.688163943340889e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMH_vs_GMG": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00010282958899140154,
            "contribution_to_total": 9.057866203932074e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -5.41125541125541e-05
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.0010302031235167662,
            "contribution_to_total": -7.21869652002514e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.0030707109351616954,
            "contribution_to_total": -0.0001506722186182907,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00010282958899140154,
            "contribution_to_total": 9.057866203932074e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -5.41125541125541e-05
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.0003883155349905094,
            "contribution_to_total": -1.6452260580803765e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.0037719968770228767,
            "contribution_to_total": -0.00011610347077564531,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0019635668029454327,
            "contribution_to_total": -9.030345246209304e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00010282958899140154,
            "contribution_to_total": 9.057866203932074e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -5.41125541125541e-05
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.001120587654039824,
            "contribution_to_total": -7.547684361810874e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.003684612371201275,
            "contribution_to_total": -0.00015077356434754446,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.00031216218274157843,
            "contribution_to_total": 3.3912241471111183e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.00020211050832168406,
            "contribution_to_total": 5.050018132969836e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.00013100428128333394,
            "contribution_to_total": 3.8117667938134647e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.00025648503228092894,
            "contribution_to_total": -0.00017544820785032585,
            "DeltaMRR_positive_anchor_full_negative_population": -2.3540489642184554e-05
          }
        },
        "GMH_vs_GDUP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00047288912810349053,
            "contribution_to_total": 0.00041654999243590104,
            "DeltaMRR_positive_anchor_full_negative_population": -5.41125541125541e-05
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.0017354219358021608,
            "contribution_to_total": 0.00012160208023817422,
            "DeltaMRR_positive_anchor_full_negative_population": -0.007051282051282051
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.011536653669465421,
            "contribution_to_total": -0.0005660751664720494,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00047288912810349053,
            "contribution_to_total": 0.00041654999243590104,
            "DeltaMRR_positive_anchor_full_negative_population": -5.41125541125541e-05
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.001955984918771363,
            "contribution_to_total": -8.2871713016929e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00035612535612535566
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.011616228325290483,
            "contribution_to_total": -0.00035755184053944995,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -8.80534211724882e-05,
            "contribution_to_total": -4.049532677496288e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0037593984962406013
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00047288912810349053,
            "contribution_to_total": 0.00041654999243590104,
            "DeltaMRR_positive_anchor_full_negative_population": -5.41125541125541e-05
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.0015359513215950432,
            "contribution_to_total": 0.00010345353822802029,
            "DeltaMRR_positive_anchor_full_negative_population": -0.008365927857453282
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.009815540514709382,
            "contribution_to_total": -0.0004016498562962738,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.013464776509645478,
            "contribution_to_total": -0.0001462767681656217,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.0007404226369548256,
            "contribution_to_total": 1.8500511298165115e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.0006187466311374359,
            "contribution_to_total": 0.0001800336476983269,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00641025641025641
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.0003310543692916454,
            "contribution_to_total": -0.00022645725279446608,
            "DeltaMRR_positive_anchor_full_negative_population": 1.2675648268868563e-05
          }
        },
        "GMS_vs_GM": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0005235450335139473,
            "contribution_to_total": 0.00046117084701165196,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -8.296288359632203e-05,
            "contribution_to_total": -5.813260175950865e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 9.157509157509145e-05
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.0010061721301331847,
            "contribution_to_total": -4.9370386975573605e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0005235450335139473,
            "contribution_to_total": 0.00046117084701165196,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.00012852076069173345,
            "contribution_to_total": 5.4452033318605155e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00035612535612535566
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.0013002788260639583,
            "contribution_to_total": -4.0023067251651804e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.00044805409759394636,
            "contribution_to_total": -2.0605783231733187e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0005235450335139473,
            "contribution_to_total": 0.00046117084701165196,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.000101610840962482,
            "contribution_to_total": 6.843967560753812e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00010864841373315934
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.0017866533035969044,
            "contribution_to_total": -7.310947793099772e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.0010200855092831233,
            "contribution_to_total": 1.1081863218719427e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.0006779788202992005,
            "contribution_to_total": 1.6940263842348303e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.0005399545824310223,
            "contribution_to_total": 0.00015710791489528388,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.00033906808196388076,
            "contribution_to_total": 0.00023193902112249532,
            "DeltaMRR_positive_anchor_full_negative_population": 3.6216137911053115e-05
          }
        },
        "GMS_vs_GMH": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 2.6404913969360823e-05,
            "contribution_to_total": 2.3259081379855226e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 2.6244300525163275e-05,
            "contribution_to_total": 1.8389542464671714e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.00018151980410458383,
            "contribution_to_total": -8.906729478968353e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 2.6404913969360823e-05,
            "contribution_to_total": 2.3259081379855226e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.00034688037634938486,
            "contribution_to_total": 1.469672425597611e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.00018671949731769935,
            "contribution_to_total": -5.747295771140483e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0003482795910663433,
            "contribution_to_total": -1.601720371733681e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 2.6404913969360823e-05,
            "contribution_to_total": 2.3259081379855226e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.00019477695218648907,
            "contribution_to_total": 1.3119142895776559e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.0003809673591125451,
            "contribution_to_total": -1.5589104320013615e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.00042322876105071273,
            "contribution_to_total": -4.597813808264126e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -7.24754956865024e-05,
            "contribution_to_total": -1.8109032056377567e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -6.81200284469288e-05,
            "contribution_to_total": -1.982054783889455e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 5.5292506080145135e-05,
            "contribution_to_total": 3.782275719188635e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMS_vs_GMP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00021642975173502346,
            "contribution_to_total": 0.0001906447116043616,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.00038654874972751094,
            "contribution_to_total": -2.708570815581147e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.0013039484490921383,
            "contribution_to_total": -6.398153715443952e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00021642975173502346,
            "contribution_to_total": 0.0001906447116043616,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.0004301885533663634,
            "contribution_to_total": -1.8226348268645488e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.0021853602410102403,
            "contribution_to_total": -6.726620332640609e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.00012121666688600951,
            "contribution_to_total": -5.574693715199423e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00021642975173502346,
            "contribution_to_total": 0.0001906447116043616,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.00047323940573916896,
            "contribution_to_total": -3.187489750768982e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.0013032263090394815,
            "contribution_to_total": -5.3327746848256897e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.0005398365178437096,
            "contribution_to_total": -5.864600954304287e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.00017476755990198682,
            "contribution_to_total": 4.366815728132207e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.00010484507810478717,
            "contribution_to_total": 3.050625394068314e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 9.45903606568305e-05,
            "contribution_to_total": 6.470439662529525e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMS_vs_GMG": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00012923450296076238,
            "contribution_to_total": 0.00011383774341917599,
            "DeltaMRR_positive_anchor_full_negative_population": -5.41125541125541e-05
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.001003958822991603,
            "contribution_to_total": -7.034801095378422e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.003252230739266279,
            "contribution_to_total": -0.00015957894809725902,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00012923450296076238,
            "contribution_to_total": 0.00011383774341917599,
            "DeltaMRR_positive_anchor_full_negative_population": -5.41125541125541e-05
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -4.1435158641124555e-05,
            "contribution_to_total": -1.7555363248276562e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.003958716374340575,
            "contribution_to_total": -0.00012185076654678577,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.002311846394011776,
            "contribution_to_total": -0.00010632065617942987,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00012923450296076238,
            "contribution_to_total": 0.00011383774341917599,
            "DeltaMRR_positive_anchor_full_negative_population": -5.41125541125541e-05
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.0009258107018533352,
            "contribution_to_total": -6.23577007223322e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.00406557973031382,
            "contribution_to_total": -0.0001663626686675581,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.00011106657830913431,
            "contribution_to_total": -1.2065896611530073e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.00012963501263518168,
            "contribution_to_total": 3.239114927332079e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 6.288425283640515e-05,
            "contribution_to_total": 1.8297120099240097e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.00020119252620078384,
            "contribution_to_total": -0.0001376254506584395,
            "DeltaMRR_positive_anchor_full_negative_population": -2.3540489642184554e-05
          }
        },
        "GMS_vs_GDUP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0004992940420728514,
            "contribution_to_total": 0.00043980907381575634,
            "DeltaMRR_positive_anchor_full_negative_population": -5.41125541125541e-05
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.001761666236327324,
            "contribution_to_total": 0.0001234410344846414,
            "DeltaMRR_positive_anchor_full_negative_population": -0.007051282051282051
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.011718173473570005,
            "contribution_to_total": -0.0005749818959510177,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0004992940420728514,
            "contribution_to_total": 0.00043980907381575634,
            "DeltaMRR_positive_anchor_full_negative_population": -5.41125541125541e-05
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.001609104542421978,
            "contribution_to_total": -6.81749887609529e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00035612535612535566
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.01180294782260818,
            "contribution_to_total": -0.0003632991363105904,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.00043633301223883095,
            "contribution_to_total": -2.0066736394833072e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0037593984962406013
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0004992940420728514,
            "contribution_to_total": 0.00043980907381575634,
            "DeltaMRR_positive_anchor_full_negative_population": -5.41125541125541e-05
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.0017307282737815321,
            "contribution_to_total": 0.00011657268112379684,
            "DeltaMRR_positive_anchor_full_negative_population": -0.008365927857453282
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.010196507873821925,
            "contribution_to_total": -0.00041723896061628737,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.013888005270696191,
            "contribution_to_total": -0.00015087458197388584,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.0006679471412683232,
            "contribution_to_total": 1.6689608092527357e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.0005506266026905071,
            "contribution_to_total": 0.00016021309985943236,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00641025641025641
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.0002757618632115003,
            "contribution_to_total": -0.0001886344956025798,
            "DeltaMRR_positive_anchor_full_negative_population": 1.2675648268868563e-05
          }
        },
        "GMP_vs_GM": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00030711528177892393,
            "contribution_to_total": 0.0002705261354072904,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.00030358586613118895,
            "contribution_to_total": 2.1272447979860607e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 9.157509157509145e-05
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.0002977763189589537,
            "contribution_to_total": 1.4611150178865914e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00030711528177892393,
            "contribution_to_total": 0.0002705261354072904,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.0005587093140580968,
            "contribution_to_total": 2.3671551600506e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00035612535612535566
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.0008850814149462818,
            "contribution_to_total": 2.724313607475428e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0003268374307079369,
            "contribution_to_total": -1.5031089516533762e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00030711528177892393,
            "contribution_to_total": 0.0002705261354072904,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.0005748502467016509,
            "contribution_to_total": 3.871886506844363e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00010864841373315934
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.0004834269945574228,
            "contribution_to_total": -1.9781731082740823e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.001559922027126833,
            "contribution_to_total": 1.6946464173023714e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.0005032112603972137,
            "contribution_to_total": 1.2573448114216096e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.0004351095043262352,
            "contribution_to_total": 0.00012660166095460076,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.00024447772130705033,
            "contribution_to_total": 0.0001672346244972001,
            "DeltaMRR_positive_anchor_full_negative_population": 3.6216137911053115e-05
          }
        },
        "GMP_vs_GMH": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0001900248377656626,
            "contribution_to_total": -0.00016738563022450635,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.00041279305025267426,
            "contribution_to_total": 2.8924662402278644e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.0011224286449875544,
            "contribution_to_total": 5.507480767547116e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0001900248377656626,
            "contribution_to_total": -0.00016738563022450635,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.0007770689297157482,
            "contribution_to_total": 3.29230725246216e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.0019986407436925406,
            "contribution_to_total": 6.15189075552656e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.00022706292418033379,
            "contribution_to_total": -1.0442510002137385e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0001900248377656626,
            "contribution_to_total": -0.00016738563022450635,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.000668016357925658,
            "contribution_to_total": 4.499404040346637e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.0009222589499269364,
            "contribution_to_total": 3.773864252824328e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.00011660775679299684,
            "contribution_to_total": 1.2667871460401613e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.00024724305558848923,
            "contribution_to_total": -6.177718933769964e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.00017296510655171599,
            "contribution_to_total": -5.0326801779577686e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -3.929785457668536e-05,
            "contribution_to_total": -2.688163943340889e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMP_vs_GMS": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00021642975173502346,
            "contribution_to_total": -0.0001906447116043616,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.00038654874972751094,
            "contribution_to_total": 2.708570815581147e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.0013039484490921383,
            "contribution_to_total": 6.398153715443952e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00021642975173502346,
            "contribution_to_total": -0.0001906447116043616,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.0004301885533663634,
            "contribution_to_total": 1.8226348268645488e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.0021853602410102403,
            "contribution_to_total": 6.726620332640609e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.00012121666688600951,
            "contribution_to_total": 5.574693715199423e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00021642975173502346,
            "contribution_to_total": -0.0001906447116043616,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.00047323940573916896,
            "contribution_to_total": 3.187489750768982e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.0013032263090394815,
            "contribution_to_total": 5.3327746848256897e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.0005398365178437096,
            "contribution_to_total": 5.864600954304287e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.00017476755990198682,
            "contribution_to_total": -4.366815728132207e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.00010484507810478717,
            "contribution_to_total": -3.050625394068314e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -9.45903606568305e-05,
            "contribution_to_total": -6.470439662529525e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMP_vs_GMG": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -8.719524877426107e-05,
            "contribution_to_total": -7.680696818518561e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -5.41125541125541e-05
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.0006174100732640918,
            "contribution_to_total": -4.326230279797276e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.0019482822901741416,
            "contribution_to_total": -9.559741094281955e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -8.719524877426107e-05,
            "contribution_to_total": -7.680696818518561e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -5.41125541125541e-05
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.00038875339472523886,
            "contribution_to_total": 1.6470811943817834e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.0017733561333303357,
            "contribution_to_total": -5.45845632203797e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0021906297271257666,
            "contribution_to_total": -0.00010074596246423045,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -8.719524877426107e-05,
            "contribution_to_total": -7.680696818518561e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -5.41125541125541e-05
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.0004525712961141662,
            "contribution_to_total": -3.0482803214642374e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.0027623534212743387,
            "contribution_to_total": -0.00011303492181930119,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.00042876993953457526,
            "contribution_to_total": 4.6580112931512796e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -4.513254726680516e-05,
            "contribution_to_total": -1.1277008008001289e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -4.196082526838201e-05,
            "contribution_to_total": -1.2209133841443038e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.00029578288685761433,
            "contribution_to_total": -0.00020232984728373472,
            "DeltaMRR_positive_anchor_full_negative_population": -2.3540489642184554e-05
          }
        },
        "GMP_vs_GDUP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00028286429033782797,
            "contribution_to_total": 0.00024916436221139474,
            "DeltaMRR_positive_anchor_full_negative_population": -5.41125541125541e-05
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.0021482149860548353,
            "contribution_to_total": 0.00015052674264045288,
            "DeltaMRR_positive_anchor_full_negative_population": -0.007051282051282051
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.010414225024477865,
            "contribution_to_total": -0.0005110003587965782,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00028286429033782797,
            "contribution_to_total": 0.00024916436221139474,
            "DeltaMRR_positive_anchor_full_negative_population": -5.41125541125541e-05
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.0011789159890556147,
            "contribution_to_total": -4.9948640492307415e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00035612535612535566
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.009617587581597939,
            "contribution_to_total": -0.00029603293298418427,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0003151163453528216,
            "contribution_to_total": -1.4492042679633658e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0037593984962406013
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00028286429033782797,
            "contribution_to_total": 0.00024916436221139474,
            "DeltaMRR_positive_anchor_full_negative_population": -5.41125541125541e-05
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.0022039676795207012,
            "contribution_to_total": 0.00014844757863148668,
            "DeltaMRR_positive_anchor_full_negative_population": -0.008365927857453282
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.008893281564782444,
            "contribution_to_total": -0.0003639112137680305,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.01334816875285248,
            "contribution_to_total": -0.00014500998101958155,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.0004931795813663363,
            "contribution_to_total": 1.232279236439515e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.00044578152458571994,
            "contribution_to_total": 0.00012970684591874921,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00641025641025641
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.00037035222386833073,
            "contribution_to_total": -0.000253338892227875,
            "DeltaMRR_positive_anchor_full_negative_population": 1.2675648268868563e-05
          }
        },
        "GMG_vs_GM": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00039431053055318503,
            "contribution_to_total": 0.00034733310359247603,
            "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.0009209959393952807,
            "contribution_to_total": 6.453475077783336e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 9.157509157509145e-05
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.002246058609133095,
            "contribution_to_total": 0.00011020856112168545,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00039431053055318503,
            "contribution_to_total": 0.00034733310359247603,
            "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.000169955919332858,
            "contribution_to_total": 7.200739656688172e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00035612535612535566
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.0026584375482766173,
            "contribution_to_total": 8.182769929513398e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0018637922964178295,
            "contribution_to_total": 8.571487294769666e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00039431053055318503,
            "contribution_to_total": 0.00034733310359247603,
            "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.001027421542815817,
            "contribution_to_total": 6.920166828308599e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00010864841373315934
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.0022789264267169163,
            "contribution_to_total": 9.32531907365604e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.0011311520875922575,
            "contribution_to_total": 1.2288452879872435e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.0005483438076640189,
            "contribution_to_total": 1.3701148915016223e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.0004770703295946172,
            "contribution_to_total": 0.00013881079479604377,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.0005402606081646647,
            "contribution_to_total": 0.00036956447178093486,
            "DeltaMRR_positive_anchor_full_negative_population": 5.975662755323767e-05
          }
        },
        "GMG_vs_GMH": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00010282958899140154,
            "contribution_to_total": -9.057866203932074e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.0010302031235167662,
            "contribution_to_total": 7.21869652002514e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.0030707109351616954,
            "contribution_to_total": 0.0001506722186182907,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00010282958899140154,
            "contribution_to_total": -9.057866203932074e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.0003883155349905094,
            "contribution_to_total": 1.6452260580803765e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.0037719968770228767,
            "contribution_to_total": 0.00011610347077564531,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0019635668029454327,
            "contribution_to_total": 9.030345246209304e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00010282958899140154,
            "contribution_to_total": -9.057866203932074e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.001120587654039824,
            "contribution_to_total": 7.547684361810874e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.003684612371201275,
            "contribution_to_total": 0.00015077356434754446,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.00031216218274157843,
            "contribution_to_total": -3.3912241471111183e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.00020211050832168406,
            "contribution_to_total": -5.050018132969836e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.00013100428128333394,
            "contribution_to_total": -3.8117667938134647e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.00025648503228092894,
            "contribution_to_total": 0.00017544820785032585,
            "DeltaMRR_positive_anchor_full_negative_population": 2.3540489642184554e-05
          }
        },
        "GMG_vs_GMS": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00012923450296076238,
            "contribution_to_total": -0.00011383774341917599,
            "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.001003958822991603,
            "contribution_to_total": 7.034801095378422e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.003252230739266279,
            "contribution_to_total": 0.00015957894809725902,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00012923450296076238,
            "contribution_to_total": -0.00011383774341917599,
            "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 4.1435158641124555e-05,
            "contribution_to_total": 1.7555363248276562e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.003958716374340575,
            "contribution_to_total": 0.00012185076654678577,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.002311846394011776,
            "contribution_to_total": 0.00010632065617942987,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00012923450296076238,
            "contribution_to_total": -0.00011383774341917599,
            "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.0009258107018533352,
            "contribution_to_total": 6.23577007223322e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.00406557973031382,
            "contribution_to_total": 0.0001663626686675581,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.00011106657830913431,
            "contribution_to_total": 1.2065896611530073e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.00012963501263518168,
            "contribution_to_total": -3.239114927332079e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -6.288425283640515e-05,
            "contribution_to_total": -1.8297120099240097e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.00020119252620078384,
            "contribution_to_total": 0.0001376254506584395,
            "DeltaMRR_positive_anchor_full_negative_population": 2.3540489642184554e-05
          }
        },
        "GMG_vs_GMP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 8.719524877426107e-05,
            "contribution_to_total": 7.680696818518561e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.0006174100732640918,
            "contribution_to_total": 4.326230279797276e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.0019482822901741416,
            "contribution_to_total": 9.559741094281955e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 8.719524877426107e-05,
            "contribution_to_total": 7.680696818518561e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.00038875339472523886,
            "contribution_to_total": -1.6470811943817834e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.0017733561333303357,
            "contribution_to_total": 5.45845632203797e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0021906297271257666,
            "contribution_to_total": 0.00010074596246423045,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 8.719524877426107e-05,
            "contribution_to_total": 7.680696818518561e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.0004525712961141662,
            "contribution_to_total": 3.0482803214642374e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.0027623534212743387,
            "contribution_to_total": 0.00011303492181930119,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.00042876993953457526,
            "contribution_to_total": -4.6580112931512796e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 4.513254726680516e-05,
            "contribution_to_total": 1.1277008008001289e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 4.196082526838201e-05,
            "contribution_to_total": 1.2209133841443038e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.00029578288685761433,
            "contribution_to_total": 0.00020232984728373472,
            "DeltaMRR_positive_anchor_full_negative_population": 2.3540489642184554e-05
          }
        },
        "GMG_vs_GDUP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0003700595391120891,
            "contribution_to_total": 0.00032597133039658036,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.0027656250593189272,
            "contribution_to_total": 0.00019378904543842566,
            "DeltaMRR_positive_anchor_full_negative_population": -0.007051282051282051
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.008465942734303724,
            "contribution_to_total": -0.00041540294785375874,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0003700595391120891,
            "contribution_to_total": 0.00032597133039658036,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.0015676693837808537,
            "contribution_to_total": -6.641945243612526e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00035612535612535566
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.007844231448267604,
            "contribution_to_total": -0.00024144836976380457,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0018755133817729445,
            "contribution_to_total": 8.625391978459676e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0037593984962406013
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0003700595391120891,
            "contribution_to_total": 0.00032597133039658036,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.0026565389756348676,
            "contribution_to_total": 0.00017893038184612904,
            "DeltaMRR_positive_anchor_full_negative_population": -0.008365927857453282
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.0061309281435081055,
            "contribution_to_total": -0.00025087629194872927,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.013776938692387056,
            "contribution_to_total": -0.00014966799231273283,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.0005383121286331415,
            "contribution_to_total": 1.3450493165195279e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.00048774234985410195,
            "contribution_to_total": 0.00014191597976019225,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00641025641025641
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -7.456933701071638e-05,
            "contribution_to_total": -5.100904494414023e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 3.6216137911053115e-05
          }
        },
        "GDUP_vs_GM": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 2.425099144109596e-05,
            "contribution_to_total": 2.1361773195895677e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.0018446291199236463,
            "contribution_to_total": -0.00012925429466059226,
            "DeltaMRR_positive_anchor_full_negative_population": 0.007142857142857143
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.01071200134343682,
            "contribution_to_total": 0.0005256115089754441,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 2.425099144109596e-05,
            "contribution_to_total": 2.1361773195895677e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.0017376253031137115,
            "contribution_to_total": 7.362019209281342e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.010502668996544224,
            "contribution_to_total": 0.0003232760690589386,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -1.1721085355115334e-05,
            "contribution_to_total": -5.390468369001077e-07,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0037593984962406013
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 2.425099144109596e-05,
            "contribution_to_total": 2.1361773195895677e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.0016291174328190504,
            "contribution_to_total": -0.00010972871356304305,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00847457627118644
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.00840985457022502,
            "contribution_to_total": 0.0003441294826852896,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.014908090779979314,
            "contribution_to_total": 0.00016195644519260527,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 1.003167903087744e-05,
            "contribution_to_total": 2.506557498209463e-07,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -1.0672020259484778e-05,
            "contribution_to_total": -3.105184964148477e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00641025641025641
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.0006148299451753811,
            "contribution_to_total": 0.0004205735167250751,
            "DeltaMRR_positive_anchor_full_negative_population": 2.3540489642184554e-05
          }
        },
        "GDUP_vs_GMH": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00047288912810349053,
            "contribution_to_total": -0.00041654999243590104,
            "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.0017354219358021608,
            "contribution_to_total": -0.00012160208023817422,
            "DeltaMRR_positive_anchor_full_negative_population": 0.007051282051282051
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.011536653669465421,
            "contribution_to_total": 0.0005660751664720494,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00047288912810349053,
            "contribution_to_total": -0.00041654999243590104,
            "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.001955984918771363,
            "contribution_to_total": 8.2871713016929e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00035612535612535566
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.011616228325290483,
            "contribution_to_total": 0.00035755184053944995,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 8.80534211724882e-05,
            "contribution_to_total": 4.049532677496288e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0037593984962406013
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00047288912810349053,
            "contribution_to_total": -0.00041654999243590104,
            "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.0015359513215950432,
            "contribution_to_total": -0.00010345353822802029,
            "DeltaMRR_positive_anchor_full_negative_population": 0.008365927857453282
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.009815540514709382,
            "contribution_to_total": 0.0004016498562962738,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.013464776509645478,
            "contribution_to_total": 0.0001462767681656217,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.0007404226369548256,
            "contribution_to_total": -1.8500511298165115e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.0006187466311374359,
            "contribution_to_total": -0.0001800336476983269,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00641025641025641
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.0003310543692916454,
            "contribution_to_total": 0.00022645725279446608,
            "DeltaMRR_positive_anchor_full_negative_population": -1.2675648268868563e-05
          }
        },
        "GDUP_vs_GMS": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0004992940420728514,
            "contribution_to_total": -0.00043980907381575634,
            "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.001761666236327324,
            "contribution_to_total": -0.0001234410344846414,
            "DeltaMRR_positive_anchor_full_negative_population": 0.007051282051282051
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.011718173473570005,
            "contribution_to_total": 0.0005749818959510177,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0004992940420728514,
            "contribution_to_total": -0.00043980907381575634,
            "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.001609104542421978,
            "contribution_to_total": 6.81749887609529e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00035612535612535566
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.01180294782260818,
            "contribution_to_total": 0.0003632991363105904,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.00043633301223883095,
            "contribution_to_total": 2.0066736394833072e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0037593984962406013
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0004992940420728514,
            "contribution_to_total": -0.00043980907381575634,
            "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.0017307282737815321,
            "contribution_to_total": -0.00011657268112379684,
            "DeltaMRR_positive_anchor_full_negative_population": 0.008365927857453282
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.010196507873821925,
            "contribution_to_total": 0.00041723896061628737,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.013888005270696191,
            "contribution_to_total": 0.00015087458197388584,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.0006679471412683232,
            "contribution_to_total": -1.6689608092527357e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.0005506266026905071,
            "contribution_to_total": -0.00016021309985943236,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00641025641025641
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.0002757618632115003,
            "contribution_to_total": 0.0001886344956025798,
            "DeltaMRR_positive_anchor_full_negative_population": -1.2675648268868563e-05
          }
        },
        "GDUP_vs_GMP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00028286429033782797,
            "contribution_to_total": -0.00024916436221139474,
            "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.0021482149860548353,
            "contribution_to_total": -0.00015052674264045288,
            "DeltaMRR_positive_anchor_full_negative_population": 0.007051282051282051
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.010414225024477865,
            "contribution_to_total": 0.0005110003587965782,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00028286429033782797,
            "contribution_to_total": -0.00024916436221139474,
            "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.0011789159890556147,
            "contribution_to_total": 4.9948640492307415e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00035612535612535566
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.009617587581597939,
            "contribution_to_total": 0.00029603293298418427,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0003151163453528216,
            "contribution_to_total": 1.4492042679633658e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0037593984962406013
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00028286429033782797,
            "contribution_to_total": -0.00024916436221139474,
            "DeltaMRR_positive_anchor_full_negative_population": 5.41125541125541e-05
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.0022039676795207012,
            "contribution_to_total": -0.00014844757863148668,
            "DeltaMRR_positive_anchor_full_negative_population": 0.008365927857453282
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.008893281564782444,
            "contribution_to_total": 0.0003639112137680305,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.01334816875285248,
            "contribution_to_total": 0.00014500998101958155,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.0004931795813663363,
            "contribution_to_total": -1.232279236439515e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.00044578152458571994,
            "contribution_to_total": -0.00012970684591874921,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00641025641025641
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.00037035222386833073,
            "contribution_to_total": 0.000253338892227875,
            "DeltaMRR_positive_anchor_full_negative_population": -1.2675648268868563e-05
          }
        },
        "GDUP_vs_GMG": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0003700595391120891,
            "contribution_to_total": -0.00032597133039658036,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.0027656250593189272,
            "contribution_to_total": -0.00019378904543842566,
            "DeltaMRR_positive_anchor_full_negative_population": 0.007051282051282051
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.008465942734303724,
            "contribution_to_total": 0.00041540294785375874,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0003700595391120891,
            "contribution_to_total": -0.00032597133039658036,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.0015676693837808537,
            "contribution_to_total": 6.641945243612526e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00035612535612535566
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.007844231448267604,
            "contribution_to_total": 0.00024144836976380457,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0018755133817729445,
            "contribution_to_total": -8.625391978459676e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0037593984962406013
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0003700595391120891,
            "contribution_to_total": -0.00032597133039658036,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.0026565389756348676,
            "contribution_to_total": -0.00017893038184612904,
            "DeltaMRR_positive_anchor_full_negative_population": 0.008365927857453282
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.0061309281435081055,
            "contribution_to_total": 0.00025087629194872927,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.013776938692387056,
            "contribution_to_total": 0.00014966799231273283,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.0005383121286331415,
            "contribution_to_total": -1.3450493165195279e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.00048774234985410195,
            "contribution_to_total": -0.00014191597976019225,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00641025641025641
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 7.456933701071638e-05,
            "contribution_to_total": 5.100904494414023e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -3.6216137911053115e-05
          }
        }
      },
      "per_candidate_directory": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HDP_ZERO_V29/retrospective/cora/seed_0"
    },
    {
      "dataset": "cora",
      "seed": 1,
      "subgroups": {
        "H0": {
          "candidate_count": 4865,
          "positive_count": 77,
          "negative_count": 4788,
          "positive_anchored_query_count": 77,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.00016644789741666853,
              "contribution_to_total_DeltaCE": 0.00014661760292089304,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.00030522520906828705,
              "contribution_to_total_DeltaCE": 0.0002688612424619259,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0001792090099030551,
              "contribution_to_total_DeltaCE": 0.00015785838007937046,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.00019493812098695138,
              "contribution_to_total_DeltaCE": 0.0001717135539745643,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -0.0003531019220826279,
              "contribution_to_total_DeltaCE": -0.0003110340124808953,
              "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
            }
          }
        },
        "H1": {
          "candidate_count": 387,
          "positive_count": 70,
          "negative_count": 317,
          "positive_anchored_query_count": 70,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.0009774926436525604,
              "contribution_to_total_DeltaCE": -6.849350952264003e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.0004825634490754362,
              "contribution_to_total_DeltaCE": -3.381351707264056e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -0.0013844422134650005,
              "contribution_to_total_DeltaCE": -9.700871566376159e-05,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0011904761904761901
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": -0.0009242664750859512,
              "contribution_to_total_DeltaCE": -6.476391922112315e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.0016734478486143598,
              "contribution_to_total_DeltaCE": 0.00011725951790942553,
              "DeltaMRR_positive_anchor_full_negative_population": 0.017857142857142856
            }
          }
        },
        "H2plus": {
          "candidate_count": 271,
          "positive_count": 116,
          "negative_count": 155,
          "positive_anchored_query_count": 116,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.0007081342153298772,
              "contribution_to_total_DeltaCE": -3.4746400933260315e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.0005657178185805711,
              "contribution_to_total_DeltaCE": -2.775837929301734e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -0.0006955014372531616,
              "contribution_to_total_DeltaCE": -3.41265416432386e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": -0.0005368986456004316,
              "contribution_to_total_DeltaCE": -2.6344293492253657e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.010577319768886479,
              "contribution_to_total_DeltaCE": 0.0005190030160000427,
              "DeltaMRR_positive_anchor_full_negative_population": -0.004310344827586207
            }
          }
        },
        "G0": {
          "candidate_count": 4865,
          "positive_count": 77,
          "negative_count": 4788,
          "positive_anchored_query_count": 77,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.00016644789741666853,
              "contribution_to_total_DeltaCE": 0.00014661760292089304,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.00030522520906828705,
              "contribution_to_total_DeltaCE": 0.0002688612424619259,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0001792090099030551,
              "contribution_to_total_DeltaCE": 0.00015785838007937046,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.00019493812098695138,
              "contribution_to_total_DeltaCE": 0.0001717135539745643,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -0.0003531019220826279,
              "contribution_to_total_DeltaCE": -0.0003110340124808953,
              "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
            }
          }
        },
        "G1": {
          "candidate_count": 234,
          "positive_count": 18,
          "negative_count": 216,
          "positive_anchored_query_count": 18,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.0012930171120776328,
              "contribution_to_total_DeltaCE": -5.478290860513599e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.0007190615238316454,
              "contribution_to_total_DeltaCE": -3.046539861970035e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -0.001991035744439717,
              "contribution_to_total_DeltaCE": -8.435675614682124e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": -0.0013296061284868278,
              "contribution_to_total_DeltaCE": -5.633312222812198e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.005984775722242096,
              "contribution_to_total_DeltaCE": 0.00025356464222427134,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0046296296296296285
            }
          }
        },
        "G2to3": {
          "candidate_count": 170,
          "positive_count": 35,
          "negative_count": 135,
          "positive_anchored_query_count": 35,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 3.486231034810998e-05,
              "contribution_to_total_DeltaCE": 1.0730749156579209e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.00045314345265747144,
              "contribution_to_total_DeltaCE": 1.394792448882313e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -0.00030038038936382053,
              "contribution_to_total_DeltaCE": -9.24582042220704e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": -9.511078148993424e-05,
              "contribution_to_total_DeltaCE": -2.9275453292212238e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.011757202476142257,
              "contribution_to_total_DeltaCE": 0.00036189107748400937,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            }
          }
        },
        "G4plus": {
          "candidate_count": 254,
          "positive_count": 133,
          "negative_count": 121,
          "positive_anchored_query_count": 133,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.0010769866692163402,
              "contribution_to_total_DeltaCE": -4.95300767664223e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.0009796676141838336,
              "contribution_to_total_DeltaCE": -4.505442223478069e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -0.0008161141563614916,
              "contribution_to_total_DeltaCE": -3.753268073797191e-05,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0006265664160401001
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": -0.0006924960310896597,
              "contribution_to_total_DeltaCE": -3.18475451560336e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.0004524253339888147,
              "contribution_to_total_DeltaCE": 2.0806814201187568e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.005012531328320803
            }
          }
        },
        "MULT0": {
          "candidate_count": 4865,
          "positive_count": 77,
          "negative_count": 4788,
          "positive_anchored_query_count": 77,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.00016644789741666853,
              "contribution_to_total_DeltaCE": 0.00014661760292089304,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.00030522520906828705,
              "contribution_to_total_DeltaCE": 0.0002688612424619259,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0001792090099030551,
              "contribution_to_total_DeltaCE": 0.00015785838007937046,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.00019493812098695138,
              "contribution_to_total_DeltaCE": 0.0001717135539745643,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -0.0003531019220826279,
              "contribution_to_total_DeltaCE": -0.0003110340124808953,
              "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
            }
          }
        },
        "MULT1to3": {
          "candidate_count": 372,
          "positive_count": 59,
          "negative_count": 313,
          "positive_anchored_query_count": 59,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.0009550155403848804,
              "contribution_to_total_DeltaCE": -6.432478381734121e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.00047310056559958963,
              "contribution_to_total_DeltaCE": -3.1865545971944115e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -0.0014491514538884419,
              "contribution_to_total_DeltaCE": -9.760715930590266e-05,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0014124293785310732
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": -0.0010066657438497846,
              "contribution_to_total_DeltaCE": -6.78036677009089e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.0022887109945683576,
              "contribution_to_total_DeltaCE": 0.000154155439069243,
              "DeltaMRR_positive_anchor_full_negative_population": 0.018361581920903952
            }
          }
        },
        "MULT4to15": {
          "candidate_count": 226,
          "positive_count": 91,
          "negative_count": 135,
          "positive_anchored_query_count": 91,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.0005126814692796829,
              "contribution_to_total_DeltaCE": -2.0978818044035548e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.00029029534641757836,
              "contribution_to_total_DeltaCE": -1.1878824604449158e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -0.00040634151593481327,
              "contribution_to_total_DeltaCE": -1.6627409487826868e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": -0.0001963804151402557,
              "contribution_to_total_DeltaCE": -8.035845341607422e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.008473756332081197,
              "contribution_to_total_DeltaCE": 0.00034674432935910744,
              "DeltaMRR_positive_anchor_full_negative_population": -0.003663003663003663
            }
          }
        },
        "MULT16plus": {
          "candidate_count": 60,
          "positive_count": 36,
          "negative_count": 24,
          "positive_anchored_query_count": 36,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.0016510372061258978,
              "contribution_to_total_DeltaCE": -1.7936308594523605e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.0016410237489018092,
              "contribution_to_total_DeltaCE": -1.782752578926463e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -0.0015557083776465638,
              "contribution_to_total_DeltaCE": -1.6900688513270656e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": -0.0014054838047027067,
              "contribution_to_total_DeltaCE": -1.5268699670860474e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.012460142562536894,
              "contribution_to_total_DeltaCE": 0.00013536276548111782,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            }
          }
        },
        "degree0to3": {
          "candidate_count": 138,
          "positive_count": 8,
          "negative_count": 130,
          "positive_anchored_query_count": 8,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 9.604224676854698e-05,
              "contribution_to_total_DeltaCE": 2.3997519561940037e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.00014939590911798044,
              "contribution_to_total_DeltaCE": 3.732868994800163e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 7.512865374206153e-05,
              "contribution_to_total_DeltaCE": 1.8771961282644381e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 9.494078221647914e-05,
              "contribution_to_total_DeltaCE": 2.3722302998142534e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -4.292395041083058e-05,
              "contribution_to_total_DeltaCE": -1.072515871210324e-06,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0625
            }
          }
        },
        "degree4to15": {
          "candidate_count": 1607,
          "positive_count": 78,
          "negative_count": 1529,
          "positive_anchored_query_count": 78,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.0001430378788425613,
              "contribution_to_total_DeltaCE": 4.161902431649394e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.00025168539598765675,
              "contribution_to_total_DeltaCE": 7.323165514252479e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.00011222701201623217,
              "contribution_to_total_DeltaCE": 3.265413874888378e-05,
              "DeltaMRR_positive_anchor_full_negative_population": -0.001068376068376068
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.0001849051227535954,
              "contribution_to_total_DeltaCE": 5.380092925312834e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -0.00017615797904198518,
              "contribution_to_total_DeltaCE": -5.125581610003081e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.00641025641025641
            }
          }
        },
        "degree16plus": {
          "candidate_count": 3778,
          "positive_count": 177,
          "negative_count": 3601,
          "positive_anchored_query_count": 177,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -9.371905425888965e-07,
              "contribution_to_total_DeltaCE": -6.410838076952473e-07,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.00019051984957100108,
              "contribution_to_total_DeltaCE": 0.000130324821958943,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -1.141470499065336e-05,
              "contribution_to_total_DeltaCE": -7.80821210477791e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 3.5717030062106007e-05,
              "contribution_to_total_DeltaCE": 2.4432181708244882e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.0005519445477308559,
              "contribution_to_total_DeltaCE": 0.0003775568533998141,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0014124293785310737
            }
          }
        }
      },
      "ranking_rule": "subgroup positive anchors, original full negative population; no filtered-negative ranking",
      "calibration_warning": "H0 uses a constant HDP raw block; improvements there do not prove incremental structural information",
      "all_pairwise_subgroups": {
        "GM_vs_GMH": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00016644789741666853,
            "contribution_to_total": -0.00014661760292089304,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.0009774926436525604,
            "contribution_to_total": 6.849350952264003e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.0007081342153298772,
            "contribution_to_total": 3.4746400933260315e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00016644789741666853,
            "contribution_to_total": -0.00014661760292089304,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.0012930171120776328,
            "contribution_to_total": 5.478290860513599e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -3.486231034810998e-05,
            "contribution_to_total": -1.0730749156579209e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0010769866692163402,
            "contribution_to_total": 4.95300767664223e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00016644789741666853,
            "contribution_to_total": -0.00014661760292089304,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.0009550155403848804,
            "contribution_to_total": 6.432478381734121e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.0005126814692796829,
            "contribution_to_total": 2.0978818044035548e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.0016510372061258978,
            "contribution_to_total": 1.7936308594523605e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -9.604224676854698e-05,
            "contribution_to_total": -2.3997519561940037e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.0001430378788425613,
            "contribution_to_total": -4.161902431649394e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 9.371905425888965e-07,
            "contribution_to_total": 6.410838076952473e-07,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GM_vs_GMS": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00030522520906828705,
            "contribution_to_total": -0.0002688612424619259,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.0004825634490754362,
            "contribution_to_total": 3.381351707264056e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.0005657178185805711,
            "contribution_to_total": 2.775837929301734e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00030522520906828705,
            "contribution_to_total": -0.0002688612424619259,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.0007190615238316454,
            "contribution_to_total": 3.046539861970035e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.00045314345265747144,
            "contribution_to_total": -1.394792448882313e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0009796676141838336,
            "contribution_to_total": 4.505442223478069e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00030522520906828705,
            "contribution_to_total": -0.0002688612424619259,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.00047310056559958963,
            "contribution_to_total": 3.1865545971944115e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.00029029534641757836,
            "contribution_to_total": 1.1878824604449158e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.0016410237489018092,
            "contribution_to_total": 1.782752578926463e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.00014939590911798044,
            "contribution_to_total": -3.732868994800163e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.00025168539598765675,
            "contribution_to_total": -7.323165514252479e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.00019051984957100108,
            "contribution_to_total": -0.000130324821958943,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GM_vs_GMP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0001792090099030551,
            "contribution_to_total": -0.00015785838007937046,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.0013844422134650005,
            "contribution_to_total": 9.700871566376159e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0011904761904761901
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.0006955014372531616,
            "contribution_to_total": 3.41265416432386e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0001792090099030551,
            "contribution_to_total": -0.00015785838007937046,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.001991035744439717,
            "contribution_to_total": 8.435675614682124e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.00030038038936382053,
            "contribution_to_total": 9.24582042220704e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0008161141563614916,
            "contribution_to_total": 3.753268073797191e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0006265664160401001
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0001792090099030551,
            "contribution_to_total": -0.00015785838007937046,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.0014491514538884419,
            "contribution_to_total": 9.760715930590266e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0014124293785310732
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.00040634151593481327,
            "contribution_to_total": 1.6627409487826868e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.0015557083776465638,
            "contribution_to_total": 1.6900688513270656e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -7.512865374206153e-05,
            "contribution_to_total": -1.8771961282644381e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.00011222701201623217,
            "contribution_to_total": -3.265413874888378e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001068376068376068
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 1.141470499065336e-05,
            "contribution_to_total": 7.80821210477791e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GM_vs_GMG": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00019493812098695138,
            "contribution_to_total": -0.0001717135539745643,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.0009242664750859512,
            "contribution_to_total": 6.476391922112315e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.0005368986456004316,
            "contribution_to_total": 2.6344293492253657e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00019493812098695138,
            "contribution_to_total": -0.0001717135539745643,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.0013296061284868278,
            "contribution_to_total": 5.633312222812198e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 9.511078148993424e-05,
            "contribution_to_total": 2.9275453292212238e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0006924960310896597,
            "contribution_to_total": 3.18475451560336e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00019493812098695138,
            "contribution_to_total": -0.0001717135539745643,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.0010066657438497846,
            "contribution_to_total": 6.78036677009089e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.0001963804151402557,
            "contribution_to_total": 8.035845341607422e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.0014054838047027067,
            "contribution_to_total": 1.5268699670860474e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -9.494078221647914e-05,
            "contribution_to_total": -2.3722302998142534e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.0001849051227535954,
            "contribution_to_total": -5.380092925312834e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -3.5717030062106007e-05,
            "contribution_to_total": -2.4432181708244882e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GM_vs_GDUP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0003531019220826279,
            "contribution_to_total": 0.0003110340124808953,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006493506493506494
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.0016734478486143598,
            "contribution_to_total": -0.00011725951790942553,
            "DeltaMRR_positive_anchor_full_negative_population": -0.017857142857142856
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.010577319768886479,
            "contribution_to_total": -0.0005190030160000427,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0003531019220826279,
            "contribution_to_total": 0.0003110340124808953,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006493506493506494
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.005984775722242096,
            "contribution_to_total": -0.00025356464222427134,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0046296296296296285
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.011757202476142257,
            "contribution_to_total": -0.00036189107748400937,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0004524253339888147,
            "contribution_to_total": -2.0806814201187568e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005012531328320803
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0003531019220826279,
            "contribution_to_total": 0.0003110340124808953,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006493506493506494
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.0022887109945683576,
            "contribution_to_total": -0.000154155439069243,
            "DeltaMRR_positive_anchor_full_negative_population": -0.018361581920903952
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.008473756332081197,
            "contribution_to_total": -0.00034674432935910744,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003663003663003663
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.012460142562536894,
            "contribution_to_total": -0.00013536276548111782,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 4.292395041083058e-05,
            "contribution_to_total": 1.072515871210324e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0625
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.00017615797904198518,
            "contribution_to_total": 5.125581610003081e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00641025641025641
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.0005519445477308559,
            "contribution_to_total": -0.0003775568533998141,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0014124293785310737
          }
        },
        "GMH_vs_GM": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00016644789741666853,
            "contribution_to_total": 0.00014661760292089304,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.0009774926436525604,
            "contribution_to_total": -6.849350952264003e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.0007081342153298772,
            "contribution_to_total": -3.4746400933260315e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00016644789741666853,
            "contribution_to_total": 0.00014661760292089304,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.0012930171120776328,
            "contribution_to_total": -5.478290860513599e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 3.486231034810998e-05,
            "contribution_to_total": 1.0730749156579209e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0010769866692163402,
            "contribution_to_total": -4.95300767664223e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00016644789741666853,
            "contribution_to_total": 0.00014661760292089304,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.0009550155403848804,
            "contribution_to_total": -6.432478381734121e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.0005126814692796829,
            "contribution_to_total": -2.0978818044035548e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.0016510372061258978,
            "contribution_to_total": -1.7936308594523605e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 9.604224676854698e-05,
            "contribution_to_total": 2.3997519561940037e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.0001430378788425613,
            "contribution_to_total": 4.161902431649394e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -9.371905425888965e-07,
            "contribution_to_total": -6.410838076952473e-07,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMH_vs_GMS": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00013877731165161852,
            "contribution_to_total": -0.00012224363954103278,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.0004949291945771245,
            "contribution_to_total": -3.4679992449999485e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.00014241639674930615,
            "contribution_to_total": -6.988021640242978e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00013877731165161852,
            "contribution_to_total": -0.00012224363954103278,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.0005739555882459873,
            "contribution_to_total": -2.431750998543564e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.00041828114230936145,
            "contribution_to_total": -1.2874849573165208e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -9.731905503250643e-05,
            "contribution_to_total": -4.475654531641614e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00013877731165161852,
            "contribution_to_total": -0.00012224363954103278,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.0004819149747852908,
            "contribution_to_total": -3.24592378453971e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.00022238612286210453,
            "contribution_to_total": -9.099993439586388e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -1.0013457224088603e-05,
            "contribution_to_total": -1.087828052589745e-07,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -5.335366234943347e-05,
            "contribution_to_total": -1.3331170386061594e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.00010864751714509548,
            "contribution_to_total": -3.161263082603086e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.00019145704011359,
            "contribution_to_total": -0.00013096590576663824,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMH_vs_GMP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -1.27611124863866e-05,
            "contribution_to_total": -1.1240777158477423e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.00040694956981244005,
            "contribution_to_total": 2.8515206141121544e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0011904761904761901
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -1.263277807671575e-05,
            "contribution_to_total": -6.198592900217215e-07,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -1.27611124863866e-05,
            "contribution_to_total": -1.1240777158477423e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.0006980186323620838,
            "contribution_to_total": 2.9573847541685244e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.0003352426997119305,
            "contribution_to_total": 1.0318895337864963e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0002608725128548483,
            "contribution_to_total": -1.1997396028450384e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0006265664160401001
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -1.27611124863866e-05,
            "contribution_to_total": -1.1240777158477423e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.0004941359135035615,
            "contribution_to_total": 3.3282375488561445e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0014124293785310732
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.00010633995334486956,
            "contribution_to_total": -4.351408556208676e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -9.532882847933382e-05,
            "contribution_to_total": -1.0356200812529475e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 2.0913593026485446e-05,
            "contribution_to_total": 5.225558279295658e-07,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 3.081086682632916e-05,
            "contribution_to_total": 8.964885567610168e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001068376068376068
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 1.0477514448064468e-05,
            "contribution_to_total": 7.167128297082665e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMH_vs_GMG": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -2.849022357028286e-05,
            "contribution_to_total": -2.5095951053671214e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -5.3226168566609417e-05,
            "contribution_to_total": -3.729590301516901e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.00017123556972944566,
            "contribution_to_total": -8.402107441006658e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -2.849022357028286e-05,
            "contribution_to_total": -2.5095951053671214e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 3.658901640919503e-05,
            "contribution_to_total": 1.5502136229859928e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.00012997309183804422,
            "contribution_to_total": 4.000620244879144e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0003844906381266802,
            "contribution_to_total": -1.7682531610388696e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -2.849022357028286e-05,
            "contribution_to_total": -2.5095951053671214e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 5.165020346490419e-05,
            "contribution_to_total": 3.478883883567691e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.0003163010541394271,
            "contribution_to_total": -1.2942972702428124e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.00024555340142319094,
            "contribution_to_total": -2.6676089236631285e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 1.1014645520678168e-06,
            "contribution_to_total": 2.7521656379749903e-08,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -4.18672439110341e-05,
            "contribution_to_total": -1.2181904936634402e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -3.6654220604694904e-05,
            "contribution_to_total": -2.507326551594013e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMH_vs_GDUP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0005195498194992964,
            "contribution_to_total": 0.0004576516154017884,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006493506493506494
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.002650940492266921,
            "contribution_to_total": -0.0001857530274320656,
            "DeltaMRR_positive_anchor_full_negative_population": -0.017857142857142856
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.011285453984216357,
            "contribution_to_total": -0.0005537494169333031,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0005195498194992964,
            "contribution_to_total": 0.0004576516154017884,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006493506493506494
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.0072777928343197296,
            "contribution_to_total": -0.00030834755082940736,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0046296296296296285
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.011722340165794149,
            "contribution_to_total": -0.00036081800256835146,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.001529412003205155,
            "contribution_to_total": -7.033689096760988e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005012531328320803
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0005195498194992964,
            "contribution_to_total": 0.0004576516154017884,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006493506493506494
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.0032437265349532377,
            "contribution_to_total": -0.00021848022288658417,
            "DeltaMRR_positive_anchor_full_negative_population": -0.018361581920903952
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.008986437801360879,
            "contribution_to_total": -0.00036772314740314294,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003663003663003663
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.014111179768662793,
            "contribution_to_total": -0.00015329907407564142,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.00013896619717937759,
            "contribution_to_total": 3.4722678274043283e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0625
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.0003191958578845464,
            "contribution_to_total": 9.287484041652474e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00641025641025641
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.0005528817382734447,
            "contribution_to_total": -0.00037819793720750934,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0014124293785310737
          }
        },
        "GMS_vs_GM": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00030522520906828705,
            "contribution_to_total": 0.0002688612424619259,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.0004825634490754362,
            "contribution_to_total": -3.381351707264056e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.0005657178185805711,
            "contribution_to_total": -2.775837929301734e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00030522520906828705,
            "contribution_to_total": 0.0002688612424619259,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.0007190615238316454,
            "contribution_to_total": -3.046539861970035e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.00045314345265747144,
            "contribution_to_total": 1.394792448882313e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0009796676141838336,
            "contribution_to_total": -4.505442223478069e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00030522520906828705,
            "contribution_to_total": 0.0002688612424619259,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.00047310056559958963,
            "contribution_to_total": -3.1865545971944115e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.00029029534641757836,
            "contribution_to_total": -1.1878824604449158e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.0016410237489018092,
            "contribution_to_total": -1.782752578926463e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.00014939590911798044,
            "contribution_to_total": 3.732868994800163e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.00025168539598765675,
            "contribution_to_total": 7.323165514252479e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.00019051984957100108,
            "contribution_to_total": 0.000130324821958943,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMS_vs_GMH": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00013877731165161852,
            "contribution_to_total": 0.00012224363954103278,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.0004949291945771245,
            "contribution_to_total": 3.4679992449999485e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.00014241639674930615,
            "contribution_to_total": 6.988021640242978e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00013877731165161852,
            "contribution_to_total": 0.00012224363954103278,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.0005739555882459873,
            "contribution_to_total": 2.431750998543564e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.00041828114230936145,
            "contribution_to_total": 1.2874849573165208e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 9.731905503250643e-05,
            "contribution_to_total": 4.475654531641614e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00013877731165161852,
            "contribution_to_total": 0.00012224363954103278,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.0004819149747852908,
            "contribution_to_total": 3.24592378453971e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.00022238612286210453,
            "contribution_to_total": 9.099993439586388e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 1.0013457224088603e-05,
            "contribution_to_total": 1.087828052589745e-07,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 5.335366234943347e-05,
            "contribution_to_total": 1.3331170386061594e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.00010864751714509548,
            "contribution_to_total": 3.161263082603086e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.00019145704011359,
            "contribution_to_total": 0.00013096590576663824,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMS_vs_GMP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00012601619916523192,
            "contribution_to_total": 0.00011100286238255537,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.0009018787643895645,
            "contribution_to_total": 6.319519859112103e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0011904761904761901
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.00012978361867259039,
            "contribution_to_total": 6.3681623502212555e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00012601619916523192,
            "contribution_to_total": 0.00011100286238255537,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.001271974220608071,
            "contribution_to_total": 5.389135752712088e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.0007535238420212922,
            "contribution_to_total": 2.3193744911030178e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.00016355345782234184,
            "contribution_to_total": -7.521741496808768e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0006265664160401001
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00012601619916523192,
            "contribution_to_total": 0.00011100286238255537,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.0009760508882888524,
            "contribution_to_total": 6.574161333395855e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0014124293785310732
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.00011604616951723495,
            "contribution_to_total": 4.748584883377711e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -8.531537125524522e-05,
            "contribution_to_total": -9.268372759939731e-07,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 7.426725537591891e-05,
            "contribution_to_total": 1.8556728665357252e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.00013945838397142463,
            "contribution_to_total": 4.0577516393641025e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001068376068376068
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.00020193455456165443,
            "contribution_to_total": 0.0001381330340637209,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMS_vs_GMG": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00011028708808133566,
            "contribution_to_total": 9.714768848736157e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.000441703026010515,
            "contribution_to_total": 3.0950402148482585e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -2.8819172980139513e-05,
            "contribution_to_total": -1.4140858007636808e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00011028708808133566,
            "contribution_to_total": 9.714768848736157e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.0006105446046551823,
            "contribution_to_total": 2.586772360842163e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.0005482542341474056,
            "contribution_to_total": 1.6875469818044356e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.00028717158309417377,
            "contribution_to_total": -1.3206877078747084e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00011028708808133566,
            "contribution_to_total": 9.714768848736157e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.000533565178250195,
            "contribution_to_total": 3.593812172896479e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -9.391493127732261e-05,
            "contribution_to_total": -3.842979262841736e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.00023553994419910236,
            "contribution_to_total": -2.5588261184041538e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 5.445512690150128e-05,
            "contribution_to_total": 1.3606386949859094e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 6.678027323406137e-05,
            "contribution_to_total": 1.943072588939646e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.00015480281950889507,
            "contribution_to_total": 0.00010589264025069809,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMS_vs_GDUP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.000658327131150915,
            "contribution_to_total": 0.0005798952549428212,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006493506493506494
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.0021560112976897958,
            "contribution_to_total": -0.00015107303498206607,
            "DeltaMRR_positive_anchor_full_negative_population": -0.017857142857142856
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.011143037587467049,
            "contribution_to_total": -0.00054676139529306,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.000658327131150915,
            "contribution_to_total": 0.0005798952549428212,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006493506493506494
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.006703837246073741,
            "contribution_to_total": -0.00028403004084397165,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0046296296296296285
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.011304059023484787,
            "contribution_to_total": -0.00034794315299518626,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.001432092948172648,
            "contribution_to_total": -6.586123643596824e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005012531328320803
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.000658327131150915,
            "contribution_to_total": 0.0005798952549428212,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006493506493506494
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.0027618115601679466,
            "contribution_to_total": -0.00018602098504118706,
            "DeltaMRR_positive_anchor_full_negative_population": -0.018361581920903952
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.008764051678498775,
            "contribution_to_total": -0.00035862315396355656,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003663003663003663
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.014101166311438703,
            "contribution_to_total": -0.00015319029127038242,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.000192319859528811,
            "contribution_to_total": 4.805384866010488e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0625
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.000427843375029642,
            "contribution_to_total": 0.00012448747124255564,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00641025641025641
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.0003614246981598547,
            "contribution_to_total": -0.00024723203144087107,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0014124293785310737
          }
        },
        "GMP_vs_GM": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0001792090099030551,
            "contribution_to_total": 0.00015785838007937046,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.0013844422134650005,
            "contribution_to_total": -9.700871566376159e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0011904761904761901
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.0006955014372531616,
            "contribution_to_total": -3.41265416432386e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0001792090099030551,
            "contribution_to_total": 0.00015785838007937046,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.001991035744439717,
            "contribution_to_total": -8.435675614682124e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.00030038038936382053,
            "contribution_to_total": -9.24582042220704e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0008161141563614916,
            "contribution_to_total": -3.753268073797191e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0006265664160401001
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0001792090099030551,
            "contribution_to_total": 0.00015785838007937046,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.0014491514538884419,
            "contribution_to_total": -9.760715930590266e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0014124293785310732
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.00040634151593481327,
            "contribution_to_total": -1.6627409487826868e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.0015557083776465638,
            "contribution_to_total": -1.6900688513270656e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 7.512865374206153e-05,
            "contribution_to_total": 1.8771961282644381e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.00011222701201623217,
            "contribution_to_total": 3.265413874888378e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001068376068376068
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -1.141470499065336e-05,
            "contribution_to_total": -7.80821210477791e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMP_vs_GMH": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 1.27611124863866e-05,
            "contribution_to_total": 1.1240777158477423e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.00040694956981244005,
            "contribution_to_total": -2.8515206141121544e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0011904761904761901
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 1.263277807671575e-05,
            "contribution_to_total": 6.198592900217215e-07,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 1.27611124863866e-05,
            "contribution_to_total": 1.1240777158477423e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.0006980186323620838,
            "contribution_to_total": -2.9573847541685244e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.0003352426997119305,
            "contribution_to_total": -1.0318895337864963e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0002608725128548483,
            "contribution_to_total": 1.1997396028450384e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0006265664160401001
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 1.27611124863866e-05,
            "contribution_to_total": 1.1240777158477423e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.0004941359135035615,
            "contribution_to_total": -3.3282375488561445e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0014124293785310732
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.00010633995334486956,
            "contribution_to_total": 4.351408556208676e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 9.532882847933382e-05,
            "contribution_to_total": 1.0356200812529475e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -2.0913593026485446e-05,
            "contribution_to_total": -5.225558279295658e-07,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -3.081086682632916e-05,
            "contribution_to_total": -8.964885567610168e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001068376068376068
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -1.0477514448064468e-05,
            "contribution_to_total": -7.167128297082665e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMP_vs_GMS": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00012601619916523192,
            "contribution_to_total": -0.00011100286238255537,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.0009018787643895645,
            "contribution_to_total": -6.319519859112103e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0011904761904761901
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.00012978361867259039,
            "contribution_to_total": -6.3681623502212555e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00012601619916523192,
            "contribution_to_total": -0.00011100286238255537,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.001271974220608071,
            "contribution_to_total": -5.389135752712088e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.0007535238420212922,
            "contribution_to_total": -2.3193744911030178e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.00016355345782234184,
            "contribution_to_total": 7.521741496808768e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0006265664160401001
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00012601619916523192,
            "contribution_to_total": -0.00011100286238255537,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.0009760508882888524,
            "contribution_to_total": -6.574161333395855e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0014124293785310732
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.00011604616951723495,
            "contribution_to_total": -4.748584883377711e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 8.531537125524522e-05,
            "contribution_to_total": 9.268372759939731e-07,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -7.426725537591891e-05,
            "contribution_to_total": -1.8556728665357252e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.00013945838397142463,
            "contribution_to_total": -4.0577516393641025e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001068376068376068
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.00020193455456165443,
            "contribution_to_total": -0.0001381330340637209,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMP_vs_GMG": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -1.572911108389626e-05,
            "contribution_to_total": -1.3855173895193792e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.0004601757383790495,
            "contribution_to_total": -3.224479644263845e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0011904761904761901
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.00015860279165272993,
            "contribution_to_total": -7.782248150984937e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -1.572911108389626e-05,
            "contribution_to_total": -1.3855173895193792e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.0006614296159528887,
            "contribution_to_total": -2.802363391869925e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.00020526960787388632,
            "contribution_to_total": -6.3182750929858184e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0001236181252718319,
            "contribution_to_total": -5.685135581938312e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0006265664160401001
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -1.572911108389626e-05,
            "contribution_to_total": -1.3855173895193792e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.0004424857100386574,
            "contribution_to_total": -2.980349160499376e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0014124293785310732
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.00020996110079455753,
            "contribution_to_total": -8.591564146219446e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.00015022457294385714,
            "contribution_to_total": -1.6319888424101808e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -1.9812128474417627e-05,
            "contribution_to_total": -4.950341715498158e-07,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -7.267811073736326e-05,
            "contribution_to_total": -2.114679050424457e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001068376068376068
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -4.7131735052759355e-05,
            "contribution_to_total": -3.2240393813022783e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMP_vs_GDUP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0005323109319856831,
            "contribution_to_total": 0.00046889239256026587,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006493506493506494
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.0030578900620793605,
            "contribution_to_total": -0.00021426823357318712,
            "DeltaMRR_positive_anchor_full_negative_population": -0.019047619047619046
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.01127282120613964,
            "contribution_to_total": -0.0005531295576432812,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0005323109319856831,
            "contribution_to_total": 0.00046889239256026587,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006493506493506494
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.007975811466681812,
            "contribution_to_total": -0.00033792139837109255,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0046296296296296285
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.012057582865506077,
            "contribution_to_total": -0.0003711368979062164,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.001268539490350306,
            "contribution_to_total": -5.833949493915947e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005639097744360902
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0005323109319856831,
            "contribution_to_total": 0.00046889239256026587,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006493506493506494
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.003737862448456799,
            "contribution_to_total": -0.0002517625983751456,
            "DeltaMRR_positive_anchor_full_negative_population": -0.019774011299435026
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.00888009784801601,
            "contribution_to_total": -0.0003633717388469343,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003663003663003663
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.014015850940183457,
            "contribution_to_total": -0.00015226345399438844,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.0001180526041528921,
            "contribution_to_total": 2.949711999474762e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0625
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.00028838499105821735,
            "contribution_to_total": 8.390995484891459e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.007478632478632478
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.000563359252721509,
            "contribution_to_total": -0.0003853650655045919,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0014124293785310737
          }
        },
        "GMG_vs_GM": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00019493812098695138,
            "contribution_to_total": 0.0001717135539745643,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.0009242664750859512,
            "contribution_to_total": -6.476391922112315e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.0005368986456004316,
            "contribution_to_total": -2.6344293492253657e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00019493812098695138,
            "contribution_to_total": 0.0001717135539745643,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.0013296061284868278,
            "contribution_to_total": -5.633312222812198e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -9.511078148993424e-05,
            "contribution_to_total": -2.9275453292212238e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0006924960310896597,
            "contribution_to_total": -3.18475451560336e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00019493812098695138,
            "contribution_to_total": 0.0001717135539745643,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.0010066657438497846,
            "contribution_to_total": -6.78036677009089e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.0001963804151402557,
            "contribution_to_total": -8.035845341607422e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.0014054838047027067,
            "contribution_to_total": -1.5268699670860474e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 9.494078221647914e-05,
            "contribution_to_total": 2.3722302998142534e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.0001849051227535954,
            "contribution_to_total": 5.380092925312834e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 3.5717030062106007e-05,
            "contribution_to_total": 2.4432181708244882e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMG_vs_GMH": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 2.849022357028286e-05,
            "contribution_to_total": 2.5095951053671214e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 5.3226168566609417e-05,
            "contribution_to_total": 3.729590301516901e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.00017123556972944566,
            "contribution_to_total": 8.402107441006658e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 2.849022357028286e-05,
            "contribution_to_total": 2.5095951053671214e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -3.658901640919503e-05,
            "contribution_to_total": -1.5502136229859928e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.00012997309183804422,
            "contribution_to_total": -4.000620244879144e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0003844906381266802,
            "contribution_to_total": 1.7682531610388696e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 2.849022357028286e-05,
            "contribution_to_total": 2.5095951053671214e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -5.165020346490419e-05,
            "contribution_to_total": -3.478883883567691e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.0003163010541394271,
            "contribution_to_total": 1.2942972702428124e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.00024555340142319094,
            "contribution_to_total": 2.6676089236631285e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -1.1014645520678168e-06,
            "contribution_to_total": -2.7521656379749903e-08,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 4.18672439110341e-05,
            "contribution_to_total": 1.2181904936634402e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 3.6654220604694904e-05,
            "contribution_to_total": 2.507326551594013e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMG_vs_GMS": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00011028708808133566,
            "contribution_to_total": -9.714768848736157e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.000441703026010515,
            "contribution_to_total": -3.0950402148482585e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 2.8819172980139513e-05,
            "contribution_to_total": 1.4140858007636808e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00011028708808133566,
            "contribution_to_total": -9.714768848736157e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.0006105446046551823,
            "contribution_to_total": -2.586772360842163e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.0005482542341474056,
            "contribution_to_total": -1.6875469818044356e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.00028717158309417377,
            "contribution_to_total": 1.3206877078747084e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00011028708808133566,
            "contribution_to_total": -9.714768848736157e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.000533565178250195,
            "contribution_to_total": -3.593812172896479e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 9.391493127732261e-05,
            "contribution_to_total": 3.842979262841736e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.00023553994419910236,
            "contribution_to_total": 2.5588261184041538e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -5.445512690150128e-05,
            "contribution_to_total": -1.3606386949859094e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -6.678027323406137e-05,
            "contribution_to_total": -1.943072588939646e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.00015480281950889507,
            "contribution_to_total": -0.00010589264025069809,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMG_vs_GMP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 1.572911108389626e-05,
            "contribution_to_total": 1.3855173895193792e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.0004601757383790495,
            "contribution_to_total": 3.224479644263845e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0011904761904761901
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.00015860279165272993,
            "contribution_to_total": 7.782248150984937e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 1.572911108389626e-05,
            "contribution_to_total": 1.3855173895193792e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.0006614296159528887,
            "contribution_to_total": 2.802363391869925e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.00020526960787388632,
            "contribution_to_total": 6.3182750929858184e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0001236181252718319,
            "contribution_to_total": 5.685135581938312e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0006265664160401001
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 1.572911108389626e-05,
            "contribution_to_total": 1.3855173895193792e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.0004424857100386574,
            "contribution_to_total": 2.980349160499376e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0014124293785310732
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.00020996110079455753,
            "contribution_to_total": 8.591564146219446e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.00015022457294385714,
            "contribution_to_total": 1.6319888424101808e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 1.9812128474417627e-05,
            "contribution_to_total": 4.950341715498158e-07,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 7.267811073736326e-05,
            "contribution_to_total": 2.114679050424457e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001068376068376068
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 4.7131735052759355e-05,
            "contribution_to_total": 3.2240393813022783e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMG_vs_GDUP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0005480400430695792,
            "contribution_to_total": 0.00048274756645545953,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006493506493506494
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.002597714323700311,
            "contribution_to_total": -0.00018202343713054868,
            "DeltaMRR_positive_anchor_full_negative_population": -0.017857142857142856
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.01111421841448691,
            "contribution_to_total": -0.0005453473094922963,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0005480400430695792,
            "contribution_to_total": 0.00048274756645545953,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006493506493506494
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.007314381850728924,
            "contribution_to_total": -0.00030989776445239326,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0046296296296296285
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.011852313257632191,
            "contribution_to_total": -0.0003648186228132306,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0011449213650784739,
            "contribution_to_total": -5.2654359357221146e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005012531328320803
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0005480400430695792,
            "contribution_to_total": 0.00048274756645545953,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006493506493506494
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.0032953767384181418,
            "contribution_to_total": -0.00022195910677015186,
            "DeltaMRR_positive_anchor_full_negative_population": -0.018361581920903952
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.008670136747221452,
            "contribution_to_total": -0.00035478017470071485,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003663003663003663
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.0138656263672396,
            "contribution_to_total": -0.0001506314651519783,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.00013786473262730975,
            "contribution_to_total": 3.4447461710245785e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0625
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.00036106310179558055,
            "contribution_to_total": 0.00010505674535315915,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00641025641025641
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.0005162275176687498,
            "contribution_to_total": -0.0003531246716915692,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0014124293785310737
          }
        },
        "GDUP_vs_GM": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0003531019220826279,
            "contribution_to_total": -0.0003110340124808953,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.0016734478486143598,
            "contribution_to_total": 0.00011725951790942553,
            "DeltaMRR_positive_anchor_full_negative_population": 0.017857142857142856
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.010577319768886479,
            "contribution_to_total": 0.0005190030160000427,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0003531019220826279,
            "contribution_to_total": -0.0003110340124808953,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.005984775722242096,
            "contribution_to_total": 0.00025356464222427134,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0046296296296296285
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.011757202476142257,
            "contribution_to_total": 0.00036189107748400937,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0004524253339888147,
            "contribution_to_total": 2.0806814201187568e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005012531328320803
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0003531019220826279,
            "contribution_to_total": -0.0003110340124808953,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.0022887109945683576,
            "contribution_to_total": 0.000154155439069243,
            "DeltaMRR_positive_anchor_full_negative_population": 0.018361581920903952
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.008473756332081197,
            "contribution_to_total": 0.00034674432935910744,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003663003663003663
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.012460142562536894,
            "contribution_to_total": 0.00013536276548111782,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -4.292395041083058e-05,
            "contribution_to_total": -1.072515871210324e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0625
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.00017615797904198518,
            "contribution_to_total": -5.125581610003081e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00641025641025641
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.0005519445477308559,
            "contribution_to_total": 0.0003775568533998141,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0014124293785310737
          }
        },
        "GDUP_vs_GMH": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0005195498194992964,
            "contribution_to_total": -0.0004576516154017884,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.002650940492266921,
            "contribution_to_total": 0.0001857530274320656,
            "DeltaMRR_positive_anchor_full_negative_population": 0.017857142857142856
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.011285453984216357,
            "contribution_to_total": 0.0005537494169333031,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0005195498194992964,
            "contribution_to_total": -0.0004576516154017884,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.0072777928343197296,
            "contribution_to_total": 0.00030834755082940736,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0046296296296296285
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.011722340165794149,
            "contribution_to_total": 0.00036081800256835146,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.001529412003205155,
            "contribution_to_total": 7.033689096760988e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005012531328320803
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0005195498194992964,
            "contribution_to_total": -0.0004576516154017884,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.0032437265349532377,
            "contribution_to_total": 0.00021848022288658417,
            "DeltaMRR_positive_anchor_full_negative_population": 0.018361581920903952
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.008986437801360879,
            "contribution_to_total": 0.00036772314740314294,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003663003663003663
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.014111179768662793,
            "contribution_to_total": 0.00015329907407564142,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.00013896619717937759,
            "contribution_to_total": -3.4722678274043283e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0625
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.0003191958578845464,
            "contribution_to_total": -9.287484041652474e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00641025641025641
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.0005528817382734447,
            "contribution_to_total": 0.00037819793720750934,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0014124293785310737
          }
        },
        "GDUP_vs_GMS": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.000658327131150915,
            "contribution_to_total": -0.0005798952549428212,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.0021560112976897958,
            "contribution_to_total": 0.00015107303498206607,
            "DeltaMRR_positive_anchor_full_negative_population": 0.017857142857142856
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.011143037587467049,
            "contribution_to_total": 0.00054676139529306,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.000658327131150915,
            "contribution_to_total": -0.0005798952549428212,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.006703837246073741,
            "contribution_to_total": 0.00028403004084397165,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0046296296296296285
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.011304059023484787,
            "contribution_to_total": 0.00034794315299518626,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.001432092948172648,
            "contribution_to_total": 6.586123643596824e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005012531328320803
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.000658327131150915,
            "contribution_to_total": -0.0005798952549428212,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.0027618115601679466,
            "contribution_to_total": 0.00018602098504118706,
            "DeltaMRR_positive_anchor_full_negative_population": 0.018361581920903952
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.008764051678498775,
            "contribution_to_total": 0.00035862315396355656,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003663003663003663
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.014101166311438703,
            "contribution_to_total": 0.00015319029127038242,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.000192319859528811,
            "contribution_to_total": -4.805384866010488e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0625
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.000427843375029642,
            "contribution_to_total": -0.00012448747124255564,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00641025641025641
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.0003614246981598547,
            "contribution_to_total": 0.00024723203144087107,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0014124293785310737
          }
        },
        "GDUP_vs_GMP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0005323109319856831,
            "contribution_to_total": -0.00046889239256026587,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.0030578900620793605,
            "contribution_to_total": 0.00021426823357318712,
            "DeltaMRR_positive_anchor_full_negative_population": 0.019047619047619046
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.01127282120613964,
            "contribution_to_total": 0.0005531295576432812,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0005323109319856831,
            "contribution_to_total": -0.00046889239256026587,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.007975811466681812,
            "contribution_to_total": 0.00033792139837109255,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0046296296296296285
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.012057582865506077,
            "contribution_to_total": 0.0003711368979062164,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.001268539490350306,
            "contribution_to_total": 5.833949493915947e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005639097744360902
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0005323109319856831,
            "contribution_to_total": -0.00046889239256026587,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.003737862448456799,
            "contribution_to_total": 0.0002517625983751456,
            "DeltaMRR_positive_anchor_full_negative_population": 0.019774011299435026
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.00888009784801601,
            "contribution_to_total": 0.0003633717388469343,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003663003663003663
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.014015850940183457,
            "contribution_to_total": 0.00015226345399438844,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.0001180526041528921,
            "contribution_to_total": -2.949711999474762e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0625
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.00028838499105821735,
            "contribution_to_total": -8.390995484891459e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.007478632478632478
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.000563359252721509,
            "contribution_to_total": 0.0003853650655045919,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0014124293785310737
          }
        },
        "GDUP_vs_GMG": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0005480400430695792,
            "contribution_to_total": -0.00048274756645545953,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.002597714323700311,
            "contribution_to_total": 0.00018202343713054868,
            "DeltaMRR_positive_anchor_full_negative_population": 0.017857142857142856
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.01111421841448691,
            "contribution_to_total": 0.0005453473094922963,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0005480400430695792,
            "contribution_to_total": -0.00048274756645545953,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.007314381850728924,
            "contribution_to_total": 0.00030989776445239326,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0046296296296296285
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.011852313257632191,
            "contribution_to_total": 0.0003648186228132306,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0011449213650784739,
            "contribution_to_total": 5.2654359357221146e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005012531328320803
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0005480400430695792,
            "contribution_to_total": -0.00048274756645545953,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.0032953767384181418,
            "contribution_to_total": 0.00022195910677015186,
            "DeltaMRR_positive_anchor_full_negative_population": 0.018361581920903952
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.008670136747221452,
            "contribution_to_total": 0.00035478017470071485,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003663003663003663
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.0138656263672396,
            "contribution_to_total": 0.0001506314651519783,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.00013786473262730975,
            "contribution_to_total": -3.4447461710245785e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0625
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.00036106310179558055,
            "contribution_to_total": -0.00010505674535315915,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00641025641025641
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.0005162275176687498,
            "contribution_to_total": 0.0003531246716915692,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0014124293785310737
          }
        }
      },
      "per_candidate_directory": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HDP_ZERO_V29/retrospective/cora/seed_1"
    },
    {
      "dataset": "cora",
      "seed": 2,
      "subgroups": {
        "H0": {
          "candidate_count": 4865,
          "positive_count": 77,
          "negative_count": 4788,
          "positive_anchored_query_count": 77,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.006646895460419812,
              "contribution_to_total_DeltaCE": 0.005854996634970557,
              "DeltaMRR_positive_anchor_full_negative_population": -0.006085905436554787
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.006849626818412332,
              "contribution_to_total_DeltaCE": 0.006033574954114791,
              "DeltaMRR_positive_anchor_full_negative_population": -0.006085905436554787
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0058253739994127566,
              "contribution_to_total_DeltaCE": 0.005131349720648753,
              "DeltaMRR_positive_anchor_full_negative_population": -0.006085905436554787
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.006154497070979143,
              "contribution_to_total_DeltaCE": 0.0054212616784924,
              "DeltaMRR_positive_anchor_full_negative_population": -0.006085905436554787
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.0005573741247653269,
              "contribution_to_total_DeltaCE": 0.0004909696029301676,
              "DeltaMRR_positive_anchor_full_negative_population": 0.002164502164502165
            }
          }
        },
        "H1": {
          "candidate_count": 387,
          "positive_count": 70,
          "negative_count": 317,
          "positive_anchored_query_count": 70,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.00026449129707889154,
              "contribution_to_total_DeltaCE": 1.8533067530242808e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0008163265306122451
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.00043890251652420705,
              "contribution_to_total_DeltaCE": 3.075416872983308e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0008163265306122451
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.006039715975644501,
              "contribution_to_total_DeltaCE": 0.00042320660557204815,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0008163265306122451
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.004558245674256931,
              "contribution_to_total_DeltaCE": 0.00031939907223201746,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0020068027210884353
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.0009096795131719735,
              "contribution_to_total_DeltaCE": 6.374180184637945e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0003401360544217687
            }
          }
        },
        "H2plus": {
          "candidate_count": 271,
          "positive_count": 116,
          "negative_count": 155,
          "positive_anchored_query_count": 116,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.00047293516595208466,
              "contribution_to_total_DeltaCE": -2.3205763167303088e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.008620689655172414
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.00043463106278280597,
              "contribution_to_total_DeltaCE": -2.1326275215306974e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.008620689655172414
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0016425115270381839,
              "contribution_to_total_DeltaCE": 8.059399308842076e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.004310344827586207
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.009067530259991817,
              "contribution_to_total_DeltaCE": 0.00044492136528295897,
              "DeltaMRR_positive_anchor_full_negative_population": 0.004310344827586207
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.013931289305999996,
              "contribution_to_total_DeltaCE": 0.0006835740361988047,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            }
          }
        },
        "G0": {
          "candidate_count": 4865,
          "positive_count": 77,
          "negative_count": 4788,
          "positive_anchored_query_count": 77,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.006646895460419812,
              "contribution_to_total_DeltaCE": 0.005854996634970557,
              "DeltaMRR_positive_anchor_full_negative_population": -0.006085905436554787
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.006849626818412332,
              "contribution_to_total_DeltaCE": 0.006033574954114791,
              "DeltaMRR_positive_anchor_full_negative_population": -0.006085905436554787
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0058253739994127566,
              "contribution_to_total_DeltaCE": 0.005131349720648753,
              "DeltaMRR_positive_anchor_full_negative_population": -0.006085905436554787
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.006154497070979143,
              "contribution_to_total_DeltaCE": 0.0054212616784924,
              "DeltaMRR_positive_anchor_full_negative_population": -0.006085905436554787
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.0005573741247653269,
              "contribution_to_total_DeltaCE": 0.0004909696029301676,
              "DeltaMRR_positive_anchor_full_negative_population": 0.002164502164502165
            }
          }
        },
        "G1": {
          "candidate_count": 234,
          "positive_count": 18,
          "negative_count": 216,
          "positive_anchored_query_count": 18,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.0012519148393936765,
              "contribution_to_total_DeltaCE": -5.3041476085120467e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0031746031746031755
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.0005463429074622209,
              "contribution_to_total_DeltaCE": -2.3147608246634023e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0031746031746031755
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.007065106360670727,
              "contribution_to_total_DeltaCE": 0.0002993363911636701,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0031746031746031755
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.010190153208929674,
              "contribution_to_total_DeltaCE": 0.0004317392451366185,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0031746031746031755
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.0064524920959832185,
              "contribution_to_total_DeltaCE": 0.0002733809796234063,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0013227513227513227
            }
          }
        },
        "G2to3": {
          "candidate_count": 170,
          "positive_count": 35,
          "negative_count": 135,
          "positive_anchored_query_count": 35,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 4.2484199317718365e-05,
              "contribution_to_total_DeltaCE": 1.3076795009980303e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 0.02857142857142857
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.0002402098332071868,
              "contribution_to_total_DeltaCE": 7.393748260949078e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 0.02857142857142857
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.004781945154246577,
              "contribution_to_total_DeltaCE": 0.00014719005544485206,
              "DeltaMRR_positive_anchor_full_negative_population": 0.014285714285714285
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.011940742716964535,
              "contribution_to_total_DeltaCE": 0.0003675405145544036,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.013930457436118841,
              "contribution_to_total_DeltaCE": 0.0004287846757451028,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            }
          }
        },
        "G4plus": {
          "candidate_count": 254,
          "positive_count": 133,
          "negative_count": 121,
          "positive_anchored_query_count": 133,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.0010233010257111191,
              "contribution_to_total_DeltaCE": 4.706110094706215e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.0005475544274868726,
              "contribution_to_total_DeltaCE": 2.5181753500211053e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0012453745739484311,
              "contribution_to_total_DeltaCE": 5.727415205194668e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": -0.0007601588046389772,
              "contribution_to_total_DeltaCE": -3.4959322176045664e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0043859649122807015
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.0009817498382806162,
              "contribution_to_total_DeltaCE": 4.515018267667509e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            }
          }
        },
        "MULT0": {
          "candidate_count": 4865,
          "positive_count": 77,
          "negative_count": 4788,
          "positive_anchored_query_count": 77,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.006646895460419812,
              "contribution_to_total_DeltaCE": 0.005854996634970557,
              "DeltaMRR_positive_anchor_full_negative_population": -0.006085905436554787
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.006849626818412332,
              "contribution_to_total_DeltaCE": 0.006033574954114791,
              "DeltaMRR_positive_anchor_full_negative_population": -0.006085905436554787
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0058253739994127566,
              "contribution_to_total_DeltaCE": 0.005131349720648753,
              "DeltaMRR_positive_anchor_full_negative_population": -0.006085905436554787
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.006154497070979143,
              "contribution_to_total_DeltaCE": 0.0054212616784924,
              "DeltaMRR_positive_anchor_full_negative_population": -0.006085905436554787
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.0005573741247653269,
              "contribution_to_total_DeltaCE": 0.0004909696029301676,
              "DeltaMRR_positive_anchor_full_negative_population": 0.002164502164502165
            }
          }
        },
        "MULT1to3": {
          "candidate_count": 372,
          "positive_count": 59,
          "negative_count": 313,
          "positive_anchored_query_count": 59,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.00040287527729979534,
              "contribution_to_total_DeltaCE": 2.7135542849089963e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0009685230024213078
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.0011103481695996522,
              "contribution_to_total_DeltaCE": 7.478716623050346e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0009685230024213078
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0067943740473292895,
              "contribution_to_total_DeltaCE": 0.0004576330156810602,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0009685230024213078
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.005803663612578557,
              "contribution_to_total_DeltaCE": 0.0003909040130145253,
              "DeltaMRR_positive_anchor_full_negative_population": -0.007506053268765133
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.0012734133538293345,
              "contribution_to_total_DeltaCE": 8.577037255558798e-05,
              "DeltaMRR_positive_anchor_full_negative_population": -0.008071025020177562
            }
          }
        },
        "MULT4to15": {
          "candidate_count": 226,
          "positive_count": 91,
          "negative_count": 135,
          "positive_anchored_query_count": 91,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.0005571762470292578,
              "contribution_to_total_DeltaCE": -2.2799535004275256e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.01098901098901099
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.0012209602354556505,
              "contribution_to_total_DeltaCE": -4.996143639561416e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.01098901098901099
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0022815113604281903,
              "contribution_to_total_DeltaCE": 9.335896568111009e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.005494505494505495
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.007932568477492092,
              "contribution_to_total_DeltaCE": 0.0003245990360154287,
              "DeltaMRR_positive_anchor_full_negative_population": 0.011904761904761904
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.011953750526513835,
              "contribution_to_total_DeltaCE": 0.0004891449608893946,
              "DeltaMRR_positive_anchor_full_negative_population": 0.01098901098901099
            }
          }
        },
        "MULT16plus": {
          "candidate_count": 60,
          "positive_count": 36,
          "negative_count": 24,
          "positive_anchored_query_count": 36,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.0008292511555065921,
              "contribution_to_total_DeltaCE": -9.008703481874983e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.0014173708332894312,
              "contribution_to_total_DeltaCE": -1.5397836320363184e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -0.004343966777691614,
              "contribution_to_total_DeltaCE": -4.71913827017014e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.004493640610046317,
              "contribution_to_total_DeltaCE": 4.881738848502246e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.015869466448448562,
              "contribution_to_total_DeltaCE": 0.00017240050460020165,
              "DeltaMRR_positive_anchor_full_negative_population": -0.013888888888888888
            }
          }
        },
        "degree0to3": {
          "candidate_count": 138,
          "positive_count": 8,
          "negative_count": 130,
          "positive_anchored_query_count": 8,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.0016054875515132724,
              "contribution_to_total_DeltaCE": 4.011538694709969e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.0017863737521881745,
              "contribution_to_total_DeltaCE": 4.463508560600545e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0013059026496420646,
              "contribution_to_total_DeltaCE": 3.262983263635794e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.0012102312158077594,
              "contribution_to_total_DeltaCE": 3.023934596803744e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -0.0005276347023429668,
              "contribution_to_total_DeltaCE": -1.3183702502866089e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            }
          }
        },
        "degree4to15": {
          "candidate_count": 1607,
          "positive_count": 78,
          "negative_count": 1529,
          "positive_anchored_query_count": 78,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.0033193001887898,
              "contribution_to_total_DeltaCE": 0.0009658003627349644,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0011349761349761353
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.0034338696181376795,
              "contribution_to_total_DeltaCE": 0.0009991360630721077,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0011349761349761353
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0028974343225803066,
              "contribution_to_total_DeltaCE": 0.0008430521376763629,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0011349761349761353
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.0029333273339356737,
              "contribution_to_total_DeltaCE": 0.0008534957497075191,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0011349761349761353
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.00014700048106428072,
              "contribution_to_total_DeltaCE": 4.2772003090765724e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0024420024420024424
            }
          }
        },
        "degree16plus": {
          "candidate_count": 3778,
          "positive_count": 177,
          "negative_count": 3601,
          "positive_anchored_query_count": 177,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.007081965704458673,
              "contribution_to_total_DeltaCE": 0.004844408189651433,
              "DeltaMRR_positive_anchor_full_negative_population": 0.002824858757062147
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.007308299807651536,
              "contribution_to_total_DeltaCE": 0.004999231698951205,
              "DeltaMRR_positive_anchor_full_negative_population": 0.002824858757062147
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.006957793459901449,
              "contribution_to_total_DeltaCE": 0.004759468348996501,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.007750688484196041,
              "contribution_to_total_DeltaCE": 0.005301847020331821,
              "DeltaMRR_positive_anchor_full_negative_population": 0.00047080979284369075
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.0017669757295817622,
              "contribution_to_total_DeltaCE": 0.0012086971403874522,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            }
          }
        }
      },
      "ranking_rule": "subgroup positive anchors, original full negative population; no filtered-negative ranking",
      "calibration_warning": "H0 uses a constant HDP raw block; improvements there do not prove incremental structural information",
      "all_pairwise_subgroups": {
        "GM_vs_GMH": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.006646895460419812,
            "contribution_to_total": -0.005854996634970557,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006085905436554787
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.00026449129707889154,
            "contribution_to_total": -1.8533067530242808e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0008163265306122451
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.00047293516595208466,
            "contribution_to_total": 2.3205763167303088e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.008620689655172414
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.006646895460419812,
            "contribution_to_total": -0.005854996634970557,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006085905436554787
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.0012519148393936765,
            "contribution_to_total": 5.3041476085120467e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0031746031746031755
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -4.2484199317718365e-05,
            "contribution_to_total": -1.3076795009980303e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.02857142857142857
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0010233010257111191,
            "contribution_to_total": -4.706110094706215e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.006646895460419812,
            "contribution_to_total": -0.005854996634970557,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006085905436554787
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.00040287527729979534,
            "contribution_to_total": -2.7135542849089963e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0009685230024213078
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.0005571762470292578,
            "contribution_to_total": 2.2799535004275256e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.01098901098901099
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.0008292511555065921,
            "contribution_to_total": 9.008703481874983e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.0016054875515132724,
            "contribution_to_total": -4.011538694709969e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.0033193001887898,
            "contribution_to_total": -0.0009658003627349644,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0011349761349761353
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.007081965704458673,
            "contribution_to_total": -0.004844408189651433,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002824858757062147
          }
        },
        "GM_vs_GMS": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.006849626818412332,
            "contribution_to_total": -0.006033574954114791,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006085905436554787
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.00043890251652420705,
            "contribution_to_total": -3.075416872983308e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0008163265306122451
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.00043463106278280597,
            "contribution_to_total": 2.1326275215306974e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.008620689655172414
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.006849626818412332,
            "contribution_to_total": -0.006033574954114791,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006085905436554787
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.0005463429074622209,
            "contribution_to_total": 2.3147608246634023e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0031746031746031755
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.0002402098332071868,
            "contribution_to_total": -7.393748260949078e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.02857142857142857
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0005475544274868726,
            "contribution_to_total": -2.5181753500211053e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.006849626818412332,
            "contribution_to_total": -0.006033574954114791,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006085905436554787
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.0011103481695996522,
            "contribution_to_total": -7.478716623050346e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0009685230024213078
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.0012209602354556505,
            "contribution_to_total": 4.996143639561416e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.01098901098901099
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.0014173708332894312,
            "contribution_to_total": 1.5397836320363184e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.0017863737521881745,
            "contribution_to_total": -4.463508560600545e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.0034338696181376795,
            "contribution_to_total": -0.0009991360630721077,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0011349761349761353
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.007308299807651536,
            "contribution_to_total": -0.004999231698951205,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002824858757062147
          }
        },
        "GM_vs_GMP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0058253739994127566,
            "contribution_to_total": -0.005131349720648753,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006085905436554787
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.006039715975644501,
            "contribution_to_total": -0.00042320660557204815,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0008163265306122451
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.0016425115270381839,
            "contribution_to_total": -8.059399308842076e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0058253739994127566,
            "contribution_to_total": -0.005131349720648753,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006085905436554787
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.007065106360670727,
            "contribution_to_total": -0.0002993363911636701,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0031746031746031755
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.004781945154246577,
            "contribution_to_total": -0.00014719005544485206,
            "DeltaMRR_positive_anchor_full_negative_population": -0.014285714285714285
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0012453745739484311,
            "contribution_to_total": -5.727415205194668e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0058253739994127566,
            "contribution_to_total": -0.005131349720648753,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006085905436554787
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.0067943740473292895,
            "contribution_to_total": -0.0004576330156810602,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0009685230024213078
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.0022815113604281903,
            "contribution_to_total": -9.335896568111009e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005494505494505495
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.004343966777691614,
            "contribution_to_total": 4.71913827017014e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.0013059026496420646,
            "contribution_to_total": -3.262983263635794e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.0028974343225803066,
            "contribution_to_total": -0.0008430521376763629,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0011349761349761353
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.006957793459901449,
            "contribution_to_total": -0.004759468348996501,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GM_vs_GMG": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.006154497070979143,
            "contribution_to_total": -0.0054212616784924,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006085905436554787
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.004558245674256931,
            "contribution_to_total": -0.00031939907223201746,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0020068027210884353
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.009067530259991817,
            "contribution_to_total": -0.00044492136528295897,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.006154497070979143,
            "contribution_to_total": -0.0054212616784924,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006085905436554787
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.010190153208929674,
            "contribution_to_total": -0.0004317392451366185,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0031746031746031755
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.011940742716964535,
            "contribution_to_total": -0.0003675405145544036,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0007601588046389772,
            "contribution_to_total": 3.4959322176045664e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0043859649122807015
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.006154497070979143,
            "contribution_to_total": -0.0054212616784924,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006085905436554787
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.005803663612578557,
            "contribution_to_total": -0.0003909040130145253,
            "DeltaMRR_positive_anchor_full_negative_population": 0.007506053268765133
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.007932568477492092,
            "contribution_to_total": -0.0003245990360154287,
            "DeltaMRR_positive_anchor_full_negative_population": -0.011904761904761904
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.004493640610046317,
            "contribution_to_total": -4.881738848502246e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.0012102312158077594,
            "contribution_to_total": -3.023934596803744e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.0029333273339356737,
            "contribution_to_total": -0.0008534957497075191,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0011349761349761353
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.007750688484196041,
            "contribution_to_total": -0.005301847020331821,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00047080979284369075
          }
        },
        "GM_vs_GDUP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0005573741247653269,
            "contribution_to_total": -0.0004909696029301676,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002164502164502165
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.0009096795131719735,
            "contribution_to_total": -6.374180184637945e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0003401360544217687
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.013931289305999996,
            "contribution_to_total": -0.0006835740361988047,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0005573741247653269,
            "contribution_to_total": -0.0004909696029301676,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002164502164502165
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.0064524920959832185,
            "contribution_to_total": -0.0002733809796234063,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0013227513227513227
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.013930457436118841,
            "contribution_to_total": -0.0004287846757451028,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0009817498382806162,
            "contribution_to_total": -4.515018267667509e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0005573741247653269,
            "contribution_to_total": -0.0004909696029301676,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002164502164502165
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.0012734133538293345,
            "contribution_to_total": -8.577037255558798e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.008071025020177562
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.011953750526513835,
            "contribution_to_total": -0.0004891449608893946,
            "DeltaMRR_positive_anchor_full_negative_population": -0.01098901098901099
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.015869466448448562,
            "contribution_to_total": -0.00017240050460020165,
            "DeltaMRR_positive_anchor_full_negative_population": 0.013888888888888888
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.0005276347023429668,
            "contribution_to_total": 1.3183702502866089e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.00014700048106428072,
            "contribution_to_total": -4.2772003090765724e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0024420024420024424
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.0017669757295817622,
            "contribution_to_total": -0.0012086971403874522,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMH_vs_GM": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.006646895460419812,
            "contribution_to_total": 0.005854996634970557,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006085905436554787
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.00026449129707889154,
            "contribution_to_total": 1.8533067530242808e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0008163265306122451
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.00047293516595208466,
            "contribution_to_total": -2.3205763167303088e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.008620689655172414
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.006646895460419812,
            "contribution_to_total": 0.005854996634970557,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006085905436554787
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.0012519148393936765,
            "contribution_to_total": -5.3041476085120467e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0031746031746031755
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 4.2484199317718365e-05,
            "contribution_to_total": 1.3076795009980303e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.02857142857142857
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0010233010257111191,
            "contribution_to_total": 4.706110094706215e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.006646895460419812,
            "contribution_to_total": 0.005854996634970557,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006085905436554787
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.00040287527729979534,
            "contribution_to_total": 2.7135542849089963e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0009685230024213078
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.0005571762470292578,
            "contribution_to_total": -2.2799535004275256e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.01098901098901099
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.0008292511555065921,
            "contribution_to_total": -9.008703481874983e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.0016054875515132724,
            "contribution_to_total": 4.011538694709969e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.0033193001887898,
            "contribution_to_total": 0.0009658003627349644,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0011349761349761353
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.007081965704458673,
            "contribution_to_total": 0.004844408189651433,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002824858757062147
          }
        },
        "GMH_vs_GMS": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00020273135799251966,
            "contribution_to_total": -0.00017857831914423468,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.0001744112194453156,
            "contribution_to_total": -1.2221101199590283e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -3.83041031692787e-05,
            "contribution_to_total": -1.8794879519961122e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00020273135799251966,
            "contribution_to_total": -0.00017857831914423468,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.0007055719319314556,
            "contribution_to_total": -2.989386783848644e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.0001977256338894686,
            "contribution_to_total": -6.086068759951052e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0004757465982242466,
            "contribution_to_total": 2.18793474468511e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00020273135799251966,
            "contribution_to_total": -0.00017857831914423468,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.0007074728922998568,
            "contribution_to_total": -4.7651623381413494e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.0006637839884263927,
            "contribution_to_total": 2.7161901391338903e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.000588119677782839,
            "contribution_to_total": 6.389132838488202e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.0001808862006749021,
            "contribution_to_total": -4.519698658905755e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.00011456942934787994,
            "contribution_to_total": -3.333570033714341e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.00022633410319286402,
            "contribution_to_total": -0.0001548235092997719,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMH_vs_GMP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0008215214610070562,
            "contribution_to_total": 0.0007236469143218049,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.00577522467856561,
            "contribution_to_total": -0.0004046735380418053,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.0021154466929902685,
            "contribution_to_total": -0.00010379975625572384,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0008215214610070562,
            "contribution_to_total": 0.0007236469143218049,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.008317021200064403,
            "contribution_to_total": -0.0003523778672487906,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.004739460954928859,
            "contribution_to_total": -0.00014588237594385407,
            "DeltaMRR_positive_anchor_full_negative_population": 0.014285714285714285
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0002220735482373123,
            "contribution_to_total": -1.0213051104884542e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0008215214610070562,
            "contribution_to_total": 0.0007236469143218049,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.006391498770029494,
            "contribution_to_total": -0.00043049747283197025,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.0028386876074574475,
            "contribution_to_total": -0.00011615850068538533,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005494505494505495
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.0035147156221850217,
            "contribution_to_total": 3.818267921982642e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.0002995849018712078,
            "contribution_to_total": 7.485554310741748e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.00042186586620949335,
            "contribution_to_total": 0.00012274822505860145,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.00012417224455722392,
            "contribution_to_total": 8.493984065493246e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002824858757062147
          }
        },
        "GMH_vs_GMG": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0004923983894406698,
            "contribution_to_total": 0.0004337349564781565,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.00429375437717804,
            "contribution_to_total": -0.00030086600470177467,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0011904761904761901
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.009540465425943901,
            "contribution_to_total": -0.000468127128450262,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0004923983894406698,
            "contribution_to_total": 0.0004337349564781565,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.011442068048323352,
            "contribution_to_total": -0.000484780721221739,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.011898258517646818,
            "contribution_to_total": -0.0003662328350534056,
            "DeltaMRR_positive_anchor_full_negative_population": 0.02857142857142857
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.001783459830350096,
            "contribution_to_total": 8.202042312310779e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0043859649122807015
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0004923983894406698,
            "contribution_to_total": 0.0004337349564781565,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.005400788335278761,
            "contribution_to_total": -0.0003637684701654353,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00847457627118644
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.00848974472452135,
            "contribution_to_total": -0.00034739857101970397,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0009157509157509155
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.00532289176555291,
            "contribution_to_total": -5.782609196689745e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.0003952563357055134,
            "contribution_to_total": 9.876040979062257e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.0003859728548541262,
            "contribution_to_total": 0.00011230461302744538,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.0006687227797373696,
            "contribution_to_total": -0.0004574388306803879,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002354048964218456
          }
        },
        "GMH_vs_GDUP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0060895213356544865,
            "contribution_to_total": 0.00536402703204039,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00825040760105695
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.0006451882160930821,
            "contribution_to_total": -4.520873431613666e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00047619047619047646
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.014404224471952082,
            "contribution_to_total": -0.000706779799366108,
            "DeltaMRR_positive_anchor_full_negative_population": 0.008620689655172414
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0060895213356544865,
            "contribution_to_total": 0.00536402703204039,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00825040760105695
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.007704406935376895,
            "contribution_to_total": -0.0003264224557085268,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001851851851851853
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.013887973236801122,
            "contribution_to_total": -0.0004274769962441048,
            "DeltaMRR_positive_anchor_full_negative_population": 0.02857142857142857
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 4.155118743050344e-05,
            "contribution_to_total": 1.9109182703870858e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0060895213356544865,
            "contribution_to_total": 0.00536402703204039,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00825040760105695
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.0008705380765295395,
            "contribution_to_total": -5.863482970649804e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00903954802259887
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.012510926773543088,
            "contribution_to_total": -0.0005119444958936697,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.01669871760395515,
            "contribution_to_total": -0.0001814092080820766,
            "DeltaMRR_positive_anchor_full_negative_population": 0.013888888888888888
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.0021331222538562393,
            "contribution_to_total": 5.3299089449965785e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.0031722997077255188,
            "contribution_to_total": 0.0009230283596441985,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0013070263070263071
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.00531498997487691,
            "contribution_to_total": 0.0036357110492639807,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002824858757062147
          }
        },
        "GMS_vs_GM": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.006849626818412332,
            "contribution_to_total": 0.006033574954114791,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006085905436554787
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.00043890251652420705,
            "contribution_to_total": 3.075416872983308e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0008163265306122451
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.00043463106278280597,
            "contribution_to_total": -2.1326275215306974e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.008620689655172414
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.006849626818412332,
            "contribution_to_total": 0.006033574954114791,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006085905436554787
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.0005463429074622209,
            "contribution_to_total": -2.3147608246634023e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0031746031746031755
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.0002402098332071868,
            "contribution_to_total": 7.393748260949078e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.02857142857142857
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0005475544274868726,
            "contribution_to_total": 2.5181753500211053e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.006849626818412332,
            "contribution_to_total": 0.006033574954114791,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006085905436554787
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.0011103481695996522,
            "contribution_to_total": 7.478716623050346e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0009685230024213078
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.0012209602354556505,
            "contribution_to_total": -4.996143639561416e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.01098901098901099
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.0014173708332894312,
            "contribution_to_total": -1.5397836320363184e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.0017863737521881745,
            "contribution_to_total": 4.463508560600545e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.0034338696181376795,
            "contribution_to_total": 0.0009991360630721077,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0011349761349761353
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.007308299807651536,
            "contribution_to_total": 0.004999231698951205,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002824858757062147
          }
        },
        "GMS_vs_GMH": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00020273135799251966,
            "contribution_to_total": 0.00017857831914423468,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.0001744112194453156,
            "contribution_to_total": 1.2221101199590283e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 3.83041031692787e-05,
            "contribution_to_total": 1.8794879519961122e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00020273135799251966,
            "contribution_to_total": 0.00017857831914423468,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.0007055719319314556,
            "contribution_to_total": 2.989386783848644e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.0001977256338894686,
            "contribution_to_total": 6.086068759951052e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0004757465982242466,
            "contribution_to_total": -2.18793474468511e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00020273135799251966,
            "contribution_to_total": 0.00017857831914423468,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.0007074728922998568,
            "contribution_to_total": 4.7651623381413494e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.0006637839884263927,
            "contribution_to_total": -2.7161901391338903e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.000588119677782839,
            "contribution_to_total": -6.389132838488202e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.0001808862006749021,
            "contribution_to_total": 4.519698658905755e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.00011456942934787994,
            "contribution_to_total": 3.333570033714341e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.00022633410319286402,
            "contribution_to_total": 0.0001548235092997719,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMS_vs_GMP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0010242528189995759,
            "contribution_to_total": 0.0009022252334660397,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.0056008134591202935,
            "contribution_to_total": -0.0003924524368422151,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.0020771425898209904,
            "contribution_to_total": -0.00010192026830372776,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0010242528189995759,
            "contribution_to_total": 0.0009022252334660397,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.007611449268132949,
            "contribution_to_total": -0.00032248399941030417,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.004541735321039389,
            "contribution_to_total": -0.000139796307183903,
            "DeltaMRR_positive_anchor_full_negative_population": 0.014285714285714285
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0006978201464615587,
            "contribution_to_total": -3.209239855173564e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0010242528189995759,
            "contribution_to_total": 0.0009022252334660397,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.005684025877729638,
            "contribution_to_total": -0.0003828458494505568,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.003502471595883841,
            "contribution_to_total": -0.00014332040207672424,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005494505494505495
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.002926595944402183,
            "contribution_to_total": 3.1793546381338216e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.0004804711025461099,
            "contribution_to_total": 1.2005252969647504e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.0005364352955573733,
            "contribution_to_total": 0.00015608392539574487,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.00035050634775008794,
            "contribution_to_total": 0.00023976334995470436,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002824858757062147
          }
        },
        "GMS_vs_GMG": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0006951297474331894,
            "contribution_to_total": 0.0006123132756223911,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.004119343157732725,
            "contribution_to_total": -0.00028864490350218443,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0011904761904761901
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.009502161322774622,
            "contribution_to_total": -0.0004662476404982659,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0006951297474331894,
            "contribution_to_total": 0.0006123132756223911,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.010736496116391898,
            "contribution_to_total": -0.00045488685338325257,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.011700532883757348,
            "contribution_to_total": -0.0003601467662934545,
            "DeltaMRR_positive_anchor_full_negative_population": 0.02857142857142857
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0013077132321258496,
            "contribution_to_total": 6.01410756762567e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0043859649122807015
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0006951297474331894,
            "contribution_to_total": 0.0006123132756223911,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.004693315442978905,
            "contribution_to_total": -0.0003161168467840219,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00847457627118644
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.009153528712947742,
            "contribution_to_total": -0.0003745604724110428,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0009157509157509155
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.005911011443335749,
            "contribution_to_total": -6.421522480538565e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.0005761425363804154,
            "contribution_to_total": 1.4395739637968011e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.0005005422842020061,
            "contribution_to_total": 0.00014564031336458878,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.00044238867654450563,
            "contribution_to_total": -0.000302615321380616,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002354048964218456
          }
        },
        "GMS_vs_GDUP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.006292252693647005,
            "contribution_to_total": 0.005542605351184624,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00825040760105695
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.00047077699664776633,
            "contribution_to_total": -3.2987633116546366e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00047619047619047646
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.014365920368782805,
            "contribution_to_total": -0.0007049003114141119,
            "DeltaMRR_positive_anchor_full_negative_population": 0.008620689655172414
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.006292252693647005,
            "contribution_to_total": 0.005542605351184624,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00825040760105695
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.00699883500344544,
            "contribution_to_total": -0.0002965285878700404,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001851851851851853
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.013690247602911654,
            "contribution_to_total": -0.00042139092748415377,
            "DeltaMRR_positive_anchor_full_negative_population": 0.02857142857142857
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.00043419541079374316,
            "contribution_to_total": -1.9968429176464017e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.006292252693647005,
            "contribution_to_total": 0.005542605351184624,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00825040760105695
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.00016306518422968237,
            "contribution_to_total": -1.0983206325084528e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00903954802259887
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.013174710761969483,
            "contribution_to_total": -0.0005391063972850087,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.017286837281737997,
            "contribution_to_total": -0.00018779834092056487,
            "DeltaMRR_positive_anchor_full_negative_population": 0.013888888888888888
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.0023140084545311412,
            "contribution_to_total": 5.781878810887153e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.003286869137073399,
            "contribution_to_total": 0.0009563640599813421,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0013070263070263071
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.005541324078069774,
            "contribution_to_total": 0.003790534558563753,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002824858757062147
          }
        },
        "GMP_vs_GM": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0058253739994127566,
            "contribution_to_total": 0.005131349720648753,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006085905436554787
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.006039715975644501,
            "contribution_to_total": 0.00042320660557204815,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0008163265306122451
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.0016425115270381839,
            "contribution_to_total": 8.059399308842076e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0058253739994127566,
            "contribution_to_total": 0.005131349720648753,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006085905436554787
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.007065106360670727,
            "contribution_to_total": 0.0002993363911636701,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0031746031746031755
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.004781945154246577,
            "contribution_to_total": 0.00014719005544485206,
            "DeltaMRR_positive_anchor_full_negative_population": 0.014285714285714285
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0012453745739484311,
            "contribution_to_total": 5.727415205194668e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0058253739994127566,
            "contribution_to_total": 0.005131349720648753,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006085905436554787
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.0067943740473292895,
            "contribution_to_total": 0.0004576330156810602,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0009685230024213078
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.0022815113604281903,
            "contribution_to_total": 9.335896568111009e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005494505494505495
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.004343966777691614,
            "contribution_to_total": -4.71913827017014e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.0013059026496420646,
            "contribution_to_total": 3.262983263635794e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.0028974343225803066,
            "contribution_to_total": 0.0008430521376763629,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0011349761349761353
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.006957793459901449,
            "contribution_to_total": 0.004759468348996501,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMP_vs_GMH": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0008215214610070562,
            "contribution_to_total": -0.0007236469143218049,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.00577522467856561,
            "contribution_to_total": 0.0004046735380418053,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.0021154466929902685,
            "contribution_to_total": 0.00010379975625572384,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0008215214610070562,
            "contribution_to_total": -0.0007236469143218049,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.008317021200064403,
            "contribution_to_total": 0.0003523778672487906,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.004739460954928859,
            "contribution_to_total": 0.00014588237594385407,
            "DeltaMRR_positive_anchor_full_negative_population": -0.014285714285714285
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0002220735482373123,
            "contribution_to_total": 1.0213051104884542e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0008215214610070562,
            "contribution_to_total": -0.0007236469143218049,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.006391498770029494,
            "contribution_to_total": 0.00043049747283197025,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.0028386876074574475,
            "contribution_to_total": 0.00011615850068538533,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005494505494505495
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.0035147156221850217,
            "contribution_to_total": -3.818267921982642e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.0002995849018712078,
            "contribution_to_total": -7.485554310741748e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.00042186586620949335,
            "contribution_to_total": -0.00012274822505860145,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.00012417224455722392,
            "contribution_to_total": -8.493984065493246e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002824858757062147
          }
        },
        "GMP_vs_GMS": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0010242528189995759,
            "contribution_to_total": -0.0009022252334660397,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.0056008134591202935,
            "contribution_to_total": 0.0003924524368422151,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.0020771425898209904,
            "contribution_to_total": 0.00010192026830372776,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0010242528189995759,
            "contribution_to_total": -0.0009022252334660397,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.007611449268132949,
            "contribution_to_total": 0.00032248399941030417,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.004541735321039389,
            "contribution_to_total": 0.000139796307183903,
            "DeltaMRR_positive_anchor_full_negative_population": -0.014285714285714285
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0006978201464615587,
            "contribution_to_total": 3.209239855173564e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0010242528189995759,
            "contribution_to_total": -0.0009022252334660397,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.005684025877729638,
            "contribution_to_total": 0.0003828458494505568,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.003502471595883841,
            "contribution_to_total": 0.00014332040207672424,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005494505494505495
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.002926595944402183,
            "contribution_to_total": -3.1793546381338216e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.0004804711025461099,
            "contribution_to_total": -1.2005252969647504e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.0005364352955573733,
            "contribution_to_total": -0.00015608392539574487,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.00035050634775008794,
            "contribution_to_total": -0.00023976334995470436,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002824858757062147
          }
        },
        "GMP_vs_GMG": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0003291230715663865,
            "contribution_to_total": -0.00028991195784364843,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.0014814703013875696,
            "contribution_to_total": 0.00010380753334003067,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0011904761904761901
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.007425018732953632,
            "contribution_to_total": -0.00036432737219453817,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0003291230715663865,
            "contribution_to_total": -0.00028991195784364843,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.003125046848258948,
            "contribution_to_total": -0.00013240285397294837,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.007158797562717958,
            "contribution_to_total": -0.0002203504591095515,
            "DeltaMRR_positive_anchor_full_negative_population": 0.014285714285714285
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0020055333785874083,
            "contribution_to_total": 9.223347422799235e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0043859649122807015
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0003291230715663865,
            "contribution_to_total": -0.00028991195784364843,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.0009907104347507323,
            "contribution_to_total": 6.672900266653494e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00847457627118644
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.005651057117063901,
            "contribution_to_total": -0.00023124007033431863,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006410256410256409
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.008837607387737931,
            "contribution_to_total": -9.600877118672386e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 9.567143383430558e-05,
            "contribution_to_total": 2.390486668320509e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -3.589301135536716e-05,
            "contribution_to_total": -1.0443612031156078e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.0007928950242945936,
            "contribution_to_total": -0.0005423786713353205,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00047080979284369075
          }
        },
        "GMP_vs_GDUP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00526799987464743,
            "contribution_to_total": 0.004640380117718585,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00825040760105695
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.005130036462472527,
            "contribution_to_total": 0.00035946480372566863,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00047619047619047646
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.012288777778961814,
            "contribution_to_total": -0.0006029800431103841,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00526799987464743,
            "contribution_to_total": 0.004640380117718585,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00825040760105695
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.0006126142646875087,
            "contribution_to_total": 2.595541154026381e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001851851851851853
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.009148512281872264,
            "contribution_to_total": -0.00028159462030025075,
            "DeltaMRR_positive_anchor_full_negative_population": 0.014285714285714285
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0002636247356678153,
            "contribution_to_total": 1.2123969375271608e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.00526799987464743,
            "contribution_to_total": 0.004640380117718585,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00825040760105695
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.005520960693499954,
            "contribution_to_total": 0.0003718626431254722,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00903954802259887
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.009672239166085644,
            "contribution_to_total": -0.0003957859952082846,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005494505494505495
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.020213433226140175,
            "contribution_to_total": -0.00021959188730190306,
            "DeltaMRR_positive_anchor_full_negative_population": 0.013888888888888888
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.0018335373519850315,
            "contribution_to_total": 4.5813535139224034e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.0027504338415160257,
            "contribution_to_total": 0.0008002801345855972,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0013070263070263071
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.005190817730319685,
            "contribution_to_total": 0.003550771208609048,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GMG_vs_GM": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.006154497070979143,
            "contribution_to_total": 0.0054212616784924,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006085905436554787
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.004558245674256931,
            "contribution_to_total": 0.00031939907223201746,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0020068027210884353
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.009067530259991817,
            "contribution_to_total": 0.00044492136528295897,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.006154497070979143,
            "contribution_to_total": 0.0054212616784924,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006085905436554787
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.010190153208929674,
            "contribution_to_total": 0.0004317392451366185,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0031746031746031755
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.011940742716964535,
            "contribution_to_total": 0.0003675405145544036,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0007601588046389772,
            "contribution_to_total": -3.4959322176045664e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0043859649122807015
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.006154497070979143,
            "contribution_to_total": 0.0054212616784924,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006085905436554787
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.005803663612578557,
            "contribution_to_total": 0.0003909040130145253,
            "DeltaMRR_positive_anchor_full_negative_population": -0.007506053268765133
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.007932568477492092,
            "contribution_to_total": 0.0003245990360154287,
            "DeltaMRR_positive_anchor_full_negative_population": 0.011904761904761904
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.004493640610046317,
            "contribution_to_total": 4.881738848502246e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.0012102312158077594,
            "contribution_to_total": 3.023934596803744e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.0029333273339356737,
            "contribution_to_total": 0.0008534957497075191,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0011349761349761353
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.007750688484196041,
            "contribution_to_total": 0.005301847020331821,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00047080979284369075
          }
        },
        "GMG_vs_GMH": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0004923983894406698,
            "contribution_to_total": -0.0004337349564781565,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.00429375437717804,
            "contribution_to_total": 0.00030086600470177467,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0011904761904761901
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.009540465425943901,
            "contribution_to_total": 0.000468127128450262,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0004923983894406698,
            "contribution_to_total": -0.0004337349564781565,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.011442068048323352,
            "contribution_to_total": 0.000484780721221739,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.011898258517646818,
            "contribution_to_total": 0.0003662328350534056,
            "DeltaMRR_positive_anchor_full_negative_population": -0.02857142857142857
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.001783459830350096,
            "contribution_to_total": -8.202042312310779e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0043859649122807015
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0004923983894406698,
            "contribution_to_total": -0.0004337349564781565,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.005400788335278761,
            "contribution_to_total": 0.0003637684701654353,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00847457627118644
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.00848974472452135,
            "contribution_to_total": 0.00034739857101970397,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0009157509157509155
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.00532289176555291,
            "contribution_to_total": 5.782609196689745e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.0003952563357055134,
            "contribution_to_total": -9.876040979062257e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.0003859728548541262,
            "contribution_to_total": -0.00011230461302744538,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.0006687227797373696,
            "contribution_to_total": 0.0004574388306803879,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002354048964218456
          }
        },
        "GMG_vs_GMS": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0006951297474331894,
            "contribution_to_total": -0.0006123132756223911,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.004119343157732725,
            "contribution_to_total": 0.00028864490350218443,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0011904761904761901
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.009502161322774622,
            "contribution_to_total": 0.0004662476404982659,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0006951297474331894,
            "contribution_to_total": -0.0006123132756223911,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.010736496116391898,
            "contribution_to_total": 0.00045488685338325257,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.011700532883757348,
            "contribution_to_total": 0.0003601467662934545,
            "DeltaMRR_positive_anchor_full_negative_population": -0.02857142857142857
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0013077132321258496,
            "contribution_to_total": -6.01410756762567e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0043859649122807015
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0006951297474331894,
            "contribution_to_total": -0.0006123132756223911,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.004693315442978905,
            "contribution_to_total": 0.0003161168467840219,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00847457627118644
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.009153528712947742,
            "contribution_to_total": 0.0003745604724110428,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0009157509157509155
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.005911011443335749,
            "contribution_to_total": 6.421522480538565e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.0005761425363804154,
            "contribution_to_total": -1.4395739637968011e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.0005005422842020061,
            "contribution_to_total": -0.00014564031336458878,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.00044238867654450563,
            "contribution_to_total": 0.000302615321380616,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002354048964218456
          }
        },
        "GMG_vs_GMP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0003291230715663865,
            "contribution_to_total": 0.00028991195784364843,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.0014814703013875696,
            "contribution_to_total": -0.00010380753334003067,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0011904761904761901
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.007425018732953632,
            "contribution_to_total": 0.00036432737219453817,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0003291230715663865,
            "contribution_to_total": 0.00028991195784364843,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.003125046848258948,
            "contribution_to_total": 0.00013240285397294837,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.007158797562717958,
            "contribution_to_total": 0.0002203504591095515,
            "DeltaMRR_positive_anchor_full_negative_population": -0.014285714285714285
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0020055333785874083,
            "contribution_to_total": -9.223347422799235e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0043859649122807015
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0003291230715663865,
            "contribution_to_total": 0.00028991195784364843,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.0009907104347507323,
            "contribution_to_total": -6.672900266653494e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00847457627118644
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.005651057117063901,
            "contribution_to_total": 0.00023124007033431863,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006410256410256409
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.008837607387737931,
            "contribution_to_total": 9.600877118672386e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -9.567143383430558e-05,
            "contribution_to_total": -2.390486668320509e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 3.589301135536716e-05,
            "contribution_to_total": 1.0443612031156078e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.0007928950242945936,
            "contribution_to_total": 0.0005423786713353205,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00047080979284369075
          }
        },
        "GMG_vs_GDUP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.005597122946213816,
            "contribution_to_total": 0.004930292075562233,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00825040760105695
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.003648566161084958,
            "contribution_to_total": 0.00025565727038563804,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0016666666666666668
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": -0.0048637590460081795,
            "contribution_to_total": -0.00023865267091584586,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.005597122946213816,
            "contribution_to_total": 0.004930292075562233,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00825040760105695
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.0037376611129464575,
            "contribution_to_total": 0.0001583582655132122,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001851851851851853
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": -0.0019897147191543065,
            "contribution_to_total": -6.124416119069927e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0017419086429195931,
            "contribution_to_total": -8.010950485272075e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0043859649122807015
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.005597122946213816,
            "contribution_to_total": 0.004930292075562233,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00825040760105695
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.004530250258749222,
            "contribution_to_total": 0.0003051336404589373,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0005649717514124297
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": -0.004021182049021743,
            "contribution_to_total": -0.00016454592487396595,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0009157509157509155
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": -0.011375825838402244,
            "contribution_to_total": -0.00012358311611517918,
            "DeltaMRR_positive_anchor_full_negative_population": 0.013888888888888888
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": 0.001737865918150726,
            "contribution_to_total": 4.342304847090353e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.002786326852871393,
            "contribution_to_total": 0.0008107237466167533,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0013070263070263071
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.0059837127546142795,
            "contribution_to_total": 0.004093149879944369,
            "DeltaMRR_positive_anchor_full_negative_population": 0.000470809792843691
          }
        },
        "GDUP_vs_GM": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0005573741247653269,
            "contribution_to_total": 0.0004909696029301676,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002164502164502165
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.0009096795131719735,
            "contribution_to_total": 6.374180184637945e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0003401360544217687
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.013931289305999996,
            "contribution_to_total": 0.0006835740361988047,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0005573741247653269,
            "contribution_to_total": 0.0004909696029301676,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002164502164502165
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.0064524920959832185,
            "contribution_to_total": 0.0002733809796234063,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0013227513227513227
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.013930457436118841,
            "contribution_to_total": 0.0004287846757451028,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0009817498382806162,
            "contribution_to_total": 4.515018267667509e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": 0.0005573741247653269,
            "contribution_to_total": 0.0004909696029301676,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002164502164502165
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.0012734133538293345,
            "contribution_to_total": 8.577037255558798e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.008071025020177562
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.011953750526513835,
            "contribution_to_total": 0.0004891449608893946,
            "DeltaMRR_positive_anchor_full_negative_population": 0.01098901098901099
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.015869466448448562,
            "contribution_to_total": 0.00017240050460020165,
            "DeltaMRR_positive_anchor_full_negative_population": -0.013888888888888888
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.0005276347023429668,
            "contribution_to_total": -1.3183702502866089e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": 0.00014700048106428072,
            "contribution_to_total": 4.2772003090765724e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0024420024420024424
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": 0.0017669757295817622,
            "contribution_to_total": 0.0012086971403874522,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GDUP_vs_GMH": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0060895213356544865,
            "contribution_to_total": -0.00536402703204039,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00825040760105695
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.0006451882160930821,
            "contribution_to_total": 4.520873431613666e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00047619047619047646
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.014404224471952082,
            "contribution_to_total": 0.000706779799366108,
            "DeltaMRR_positive_anchor_full_negative_population": -0.008620689655172414
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0060895213356544865,
            "contribution_to_total": -0.00536402703204039,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00825040760105695
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.007704406935376895,
            "contribution_to_total": 0.0003264224557085268,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001851851851851853
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.013887973236801122,
            "contribution_to_total": 0.0004274769962441048,
            "DeltaMRR_positive_anchor_full_negative_population": -0.02857142857142857
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -4.155118743050344e-05,
            "contribution_to_total": -1.9109182703870858e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.0060895213356544865,
            "contribution_to_total": -0.00536402703204039,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00825040760105695
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.0008705380765295395,
            "contribution_to_total": 5.863482970649804e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00903954802259887
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.012510926773543088,
            "contribution_to_total": 0.0005119444958936697,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.01669871760395515,
            "contribution_to_total": 0.0001814092080820766,
            "DeltaMRR_positive_anchor_full_negative_population": -0.013888888888888888
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.0021331222538562393,
            "contribution_to_total": -5.3299089449965785e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.0031722997077255188,
            "contribution_to_total": -0.0009230283596441985,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0013070263070263071
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.00531498997487691,
            "contribution_to_total": -0.0036357110492639807,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002824858757062147
          }
        },
        "GDUP_vs_GMS": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.006292252693647005,
            "contribution_to_total": -0.005542605351184624,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00825040760105695
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": 0.00047077699664776633,
            "contribution_to_total": 3.2987633116546366e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00047619047619047646
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.014365920368782805,
            "contribution_to_total": 0.0007049003114141119,
            "DeltaMRR_positive_anchor_full_negative_population": -0.008620689655172414
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.006292252693647005,
            "contribution_to_total": -0.005542605351184624,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00825040760105695
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": 0.00699883500344544,
            "contribution_to_total": 0.0002965285878700404,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001851851851851853
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.013690247602911654,
            "contribution_to_total": 0.00042139092748415377,
            "DeltaMRR_positive_anchor_full_negative_population": -0.02857142857142857
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.00043419541079374316,
            "contribution_to_total": 1.9968429176464017e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.006292252693647005,
            "contribution_to_total": -0.005542605351184624,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00825040760105695
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": 0.00016306518422968237,
            "contribution_to_total": 1.0983206325084528e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00903954802259887
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.013174710761969483,
            "contribution_to_total": 0.0005391063972850087,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.017286837281737997,
            "contribution_to_total": 0.00018779834092056487,
            "DeltaMRR_positive_anchor_full_negative_population": -0.013888888888888888
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.0023140084545311412,
            "contribution_to_total": -5.781878810887153e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.003286869137073399,
            "contribution_to_total": -0.0009563640599813421,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0013070263070263071
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.005541324078069774,
            "contribution_to_total": -0.003790534558563753,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002824858757062147
          }
        },
        "GDUP_vs_GMP": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00526799987464743,
            "contribution_to_total": -0.004640380117718585,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00825040760105695
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.005130036462472527,
            "contribution_to_total": -0.00035946480372566863,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00047619047619047646
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.012288777778961814,
            "contribution_to_total": 0.0006029800431103841,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00526799987464743,
            "contribution_to_total": -0.004640380117718585,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00825040760105695
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.0006126142646875087,
            "contribution_to_total": -2.595541154026381e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001851851851851853
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.009148512281872264,
            "contribution_to_total": 0.00028159462030025075,
            "DeltaMRR_positive_anchor_full_negative_population": -0.014285714285714285
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": -0.0002636247356678153,
            "contribution_to_total": -1.2123969375271608e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.00526799987464743,
            "contribution_to_total": -0.004640380117718585,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00825040760105695
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.005520960693499954,
            "contribution_to_total": -0.0003718626431254722,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00903954802259887
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.009672239166085644,
            "contribution_to_total": 0.0003957859952082846,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005494505494505495
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.020213433226140175,
            "contribution_to_total": 0.00021959188730190306,
            "DeltaMRR_positive_anchor_full_negative_population": -0.013888888888888888
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.0018335373519850315,
            "contribution_to_total": -4.5813535139224034e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.0027504338415160257,
            "contribution_to_total": -0.0008002801345855972,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0013070263070263071
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.005190817730319685,
            "contribution_to_total": -0.003550771208609048,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          }
        },
        "GDUP_vs_GMG": {
          "H0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.005597122946213816,
            "contribution_to_total": -0.004930292075562233,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00825040760105695
          },
          "H1": {
            "candidate_count": 387,
            "positive_count": 70,
            "negative_count": 317,
            "mean_DeltaCE": -0.003648566161084958,
            "contribution_to_total": -0.00025565727038563804,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0016666666666666668
          },
          "H2plus": {
            "candidate_count": 271,
            "positive_count": 116,
            "negative_count": 155,
            "mean_DeltaCE": 0.0048637590460081795,
            "contribution_to_total": 0.00023865267091584586,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004310344827586207
          },
          "G0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.005597122946213816,
            "contribution_to_total": -0.004930292075562233,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00825040760105695
          },
          "G1": {
            "candidate_count": 234,
            "positive_count": 18,
            "negative_count": 216,
            "mean_DeltaCE": -0.0037376611129464575,
            "contribution_to_total": -0.0001583582655132122,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001851851851851853
          },
          "G2to3": {
            "candidate_count": 170,
            "positive_count": 35,
            "negative_count": 135,
            "mean_DeltaCE": 0.0019897147191543065,
            "contribution_to_total": 6.124416119069927e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 254,
            "positive_count": 133,
            "negative_count": 121,
            "mean_DeltaCE": 0.0017419086429195931,
            "contribution_to_total": 8.010950485272075e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0043859649122807015
          },
          "MULT0": {
            "candidate_count": 4865,
            "positive_count": 77,
            "negative_count": 4788,
            "mean_DeltaCE": -0.005597122946213816,
            "contribution_to_total": -0.004930292075562233,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00825040760105695
          },
          "MULT1to3": {
            "candidate_count": 372,
            "positive_count": 59,
            "negative_count": 313,
            "mean_DeltaCE": -0.004530250258749222,
            "contribution_to_total": -0.0003051336404589373,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0005649717514124297
          },
          "MULT4to15": {
            "candidate_count": 226,
            "positive_count": 91,
            "negative_count": 135,
            "mean_DeltaCE": 0.004021182049021743,
            "contribution_to_total": 0.00016454592487396595,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0009157509157509155
          },
          "MULT16plus": {
            "candidate_count": 60,
            "positive_count": 36,
            "negative_count": 24,
            "mean_DeltaCE": 0.011375825838402244,
            "contribution_to_total": 0.00012358311611517918,
            "DeltaMRR_positive_anchor_full_negative_population": -0.013888888888888888
          },
          "degree0to3": {
            "candidate_count": 138,
            "positive_count": 8,
            "negative_count": 130,
            "mean_DeltaCE": -0.001737865918150726,
            "contribution_to_total": -4.342304847090353e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 1607,
            "positive_count": 78,
            "negative_count": 1529,
            "mean_DeltaCE": -0.002786326852871393,
            "contribution_to_total": -0.0008107237466167533,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0013070263070263071
          },
          "degree16plus": {
            "candidate_count": 3778,
            "positive_count": 177,
            "negative_count": 3601,
            "mean_DeltaCE": -0.0059837127546142795,
            "contribution_to_total": -0.004093149879944369,
            "DeltaMRR_positive_anchor_full_negative_population": -0.000470809792843691
          }
        }
      },
      "per_candidate_directory": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HDP_ZERO_V29/retrospective/cora/seed_2"
    },
    {
      "dataset": "pubmed",
      "seed": 0,
      "subgroups": {
        "H0": {
          "candidate_count": 41871,
          "positive_count": 712,
          "negative_count": 41159,
          "positive_anchored_query_count": 712,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.0038342381398866524,
              "contribution_to_total_DeltaCE": 0.003449875046312404,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0012350126465295003
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.003880924893175679,
              "contribution_to_total_DeltaCE": 0.003491881687342248,
              "DeltaMRR_positive_anchor_full_negative_population": -0.002003532516172965
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0033806106177322924,
              "contribution_to_total_DeltaCE": 0.0030417214022492012,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0022567671092951994
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.0026632699065572006,
              "contribution_to_total_DeltaCE": 0.002396290490318389,
              "DeltaMRR_positive_anchor_full_negative_population": 0.00227622330852668
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -0.0007410048511265311,
              "contribution_to_total_DeltaCE": -0.0006667228408440559,
              "DeltaMRR_positive_anchor_full_negative_population": -0.000314339218833601
            }
          }
        },
        "H1": {
          "candidate_count": 2409,
          "positive_count": 185,
          "negative_count": 2224,
          "positive_anchored_query_count": 185,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.007614369317766805,
              "contribution_to_total_DeltaCE": 0.00039416829307418414,
              "DeltaMRR_positive_anchor_full_negative_population": 0.002702702702702703
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.006019102306722478,
              "contribution_to_total_DeltaCE": 0.0003115871036809019,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0001801801801801803
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.01325981304099131,
              "contribution_to_total_DeltaCE": 0.0006864124466165563,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.008824826844286265,
              "contribution_to_total_DeltaCE": 0.0004568292906112604,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0001801801801801803
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -0.006010043479299763,
              "contribution_to_total_DeltaCE": -0.0003111181610287332,
              "DeltaMRR_positive_anchor_full_negative_population": 0.01099099099099099
            }
          }
        },
        "H2plus": {
          "candidate_count": 2256,
          "positive_count": 1319,
          "negative_count": 937,
          "positive_anchored_query_count": 1319,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.002244802409359412,
              "contribution_to_total_DeltaCE": -0.00010882487183072963,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0005686125852918878
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.00308771367879765,
              "contribution_to_total_DeltaCE": -0.0001496880277498603,
              "DeltaMRR_positive_anchor_full_negative_population": 0.001326762699014405
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.007824789048942501,
              "contribution_to_total_DeltaCE": 0.0003793347965964905,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0009476876421531463
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.0044276741728533795,
              "contribution_to_total_DeltaCE": 0.0002146474328252799,
              "DeltaMRR_positive_anchor_full_negative_population": 0.001579479403588577
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.012466462097078338,
              "contribution_to_total_DeltaCE": 0.0006043565947010643,
              "DeltaMRR_positive_anchor_full_negative_population": -0.002021733636593379
            }
          }
        },
        "G0": {
          "candidate_count": 41871,
          "positive_count": 712,
          "negative_count": 41159,
          "positive_anchored_query_count": 712,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.0038342381398866524,
              "contribution_to_total_DeltaCE": 0.003449875046312404,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0012350126465295003
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.003880924893175679,
              "contribution_to_total_DeltaCE": 0.003491881687342248,
              "DeltaMRR_positive_anchor_full_negative_population": -0.002003532516172965
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0033806106177322924,
              "contribution_to_total_DeltaCE": 0.0030417214022492012,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0022567671092951994
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.0026632699065572006,
              "contribution_to_total_DeltaCE": 0.002396290490318389,
              "DeltaMRR_positive_anchor_full_negative_population": 0.00227622330852668
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -0.0007410048511265311,
              "contribution_to_total_DeltaCE": -0.0006667228408440559,
              "DeltaMRR_positive_anchor_full_negative_population": -0.000314339218833601
            }
          }
        },
        "G1": {
          "candidate_count": 1584,
          "positive_count": 50,
          "negative_count": 1534,
          "positive_anchored_query_count": 50,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.00590268757188943,
              "contribution_to_total_DeltaCE": 0.000200916647624911,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.0067265203186435175,
              "contribution_to_total_DeltaCE": 0.00022895840176919658,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0006666666666666671
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.012154450773172046,
              "contribution_to_total_DeltaCE": 0.0004137151887722306,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.010515239520850195,
              "contribution_to_total_DeltaCE": 0.00035791944733167246,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0006666666666666671
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -0.003097207553590432,
              "contribution_to_total_DeltaCE": -0.00010542325865753919,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0006666666666666671
            }
          }
        },
        "G2to3": {
          "candidate_count": 1031,
          "positive_count": 181,
          "negative_count": 850,
          "positive_anchored_query_count": 181,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.0004520349327777549,
              "contribution_to_total_DeltaCE": -1.0014784590292791e-05,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0023020257826887663
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.0024852724681055176,
              "contribution_to_total_DeltaCE": -5.506094023157961e-05,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0023020257826887663
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.017334178027032944,
              "contribution_to_total_DeltaCE": 0.0003840368219415284,
              "DeltaMRR_positive_anchor_full_negative_population": 0.00046040515653775313
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.014643248548358032,
              "contribution_to_total_DeltaCE": 0.0003244195730908787,
              "DeltaMRR_positive_anchor_full_negative_population": -0.00046040515653775405
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.004167339923961398,
              "contribution_to_total_DeltaCE": 9.232696109687557e-05,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0009208103130755068
            }
          }
        },
        "G4plus": {
          "candidate_count": 2050,
          "positive_count": 1273,
          "negative_count": 777,
          "positive_anchored_query_count": 1273,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.0021438694403933694,
              "contribution_to_total_DeltaCE": 9.444155820883632e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0013092432573972245
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.00027236920614028914,
              "contribution_to_total_DeltaCE": -1.1998385606575397e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.001702016234616392
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.006083622507115539,
              "contribution_to_total_DeltaCE": 0.00026799523249928776,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0009164702801780571
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": -0.0002465794402639033,
              "contribution_to_total_DeltaCE": -1.086229698601087e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.001702016234616392
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.0069539478305651915,
              "contribution_to_total_DeltaCE": 0.00030633473123299474,
              "DeltaMRR_positive_anchor_full_negative_population": -0.00039277297721916735
            }
          }
        },
        "MULT0": {
          "candidate_count": 41871,
          "positive_count": 712,
          "negative_count": 41159,
          "positive_anchored_query_count": 712,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.0038342381398866524,
              "contribution_to_total_DeltaCE": 0.003449875046312404,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0012350126465295003
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.003880924893175679,
              "contribution_to_total_DeltaCE": 0.003491881687342248,
              "DeltaMRR_positive_anchor_full_negative_population": -0.002003532516172965
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0033806106177322924,
              "contribution_to_total_DeltaCE": 0.0030417214022492012,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0022567671092951994
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.0026632699065572006,
              "contribution_to_total_DeltaCE": 0.002396290490318389,
              "DeltaMRR_positive_anchor_full_negative_population": 0.00227622330852668
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -0.0007410048511265311,
              "contribution_to_total_DeltaCE": -0.0006667228408440559,
              "DeltaMRR_positive_anchor_full_negative_population": -0.000314339218833601
            }
          }
        },
        "MULT1to3": {
          "candidate_count": 2199,
          "positive_count": 154,
          "negative_count": 2045,
          "positive_anchored_query_count": 154,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.005367092160627224,
              "contribution_to_total_DeltaCE": 0.00025361517236589446,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.00531005764964352,
              "contribution_to_total_DeltaCE": 0.00025092007846755414,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0030303030303030303
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.013245743221360684,
              "contribution_to_total_DeltaCE": 0.0006259108935828637,
              "DeltaMRR_positive_anchor_full_negative_population": -0.003246753246753247
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.009143317498639062,
              "contribution_to_total_DeltaCE": 0.0004320559390473461,
              "DeltaMRR_positive_anchor_full_negative_population": 0.00021645021645021659
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -0.007539374276950865,
              "contribution_to_total_DeltaCE": -0.00035626362461352394,
              "DeltaMRR_positive_anchor_full_negative_population": 0.006709956709956709
            }
          }
        },
        "MULT4to15": {
          "candidate_count": 1198,
          "positive_count": 397,
          "negative_count": 801,
          "positive_anchored_query_count": 397,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.0008954596614643195,
              "contribution_to_total_DeltaCE": 2.3052275108179793e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0006297229219143577
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.0007082770609194969,
              "contribution_to_total_DeltaCE": -1.8233537884252133e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0006297229219143577
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0166332319533137,
              "contribution_to_total_DeltaCE": 0.0004281977797848937,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0006297229219143577
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.011711655196373636,
              "contribution_to_total_DeltaCE": 0.00030149911735550145,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0010495382031905963
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.00641438783978729,
              "contribution_to_total_DeltaCE": 0.00016512886006672626,
              "DeltaMRR_positive_anchor_full_negative_population": -0.00041981528127623866
            }
          }
        },
        "MULT16plus": {
          "candidate_count": 1268,
          "positive_count": 953,
          "negative_count": 315,
          "positive_anchored_query_count": 953,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.00031841097423649815,
              "contribution_to_total_DeltaCE": 8.675973769380257e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 0.001049317943336831
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.0025979222831684487,
              "contribution_to_total_DeltaCE": -7.078746465226046e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.002098635886673662
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.00042713918479525466,
              "contribution_to_total_DeltaCE": 1.1638569845289302e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0015739769150052466
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": -0.002278294402933814,
              "contribution_to_total_DeltaCE": -6.20783329663073e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0026232948583420775
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.017776649173758183,
              "contribution_to_total_DeltaCE": 0.00048437319821912874,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0015739769150052466
            }
          }
        },
        "degree0to3": {
          "candidate_count": 419,
          "positive_count": 9,
          "negative_count": 410,
          "positive_anchored_query_count": 9,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.00028979671064714035,
              "contribution_to_total_DeltaCE": -2.609266412264737e-06,
              "DeltaMRR_positive_anchor_full_negative_population": -0.001984126984126983
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.00014508543465209563,
              "contribution_to_total_DeltaCE": 1.3063176276265272e-06,
              "DeltaMRR_positive_anchor_full_negative_population": -0.001984126984126983
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -0.0015285172062097124,
              "contribution_to_total_DeltaCE": -1.3762435735814627e-05,
              "DeltaMRR_positive_anchor_full_negative_population": -0.001984126984126983
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.0004208447798276003,
              "contribution_to_total_DeltaCE": 3.7891946610745343e-06,
              "DeltaMRR_positive_anchor_full_negative_population": -0.001984126984126983
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.0012888519106629658,
              "contribution_to_total_DeltaCE": 1.1604541657378861e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            }
          }
        },
        "degree4to15": {
          "candidate_count": 6322,
          "positive_count": 111,
          "negative_count": 6211,
          "positive_anchored_query_count": 111,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.0010607819662801989,
              "contribution_to_total_DeltaCE": 0.0001441091540060043,
              "DeltaMRR_positive_anchor_full_negative_population": 0.004290004290004291
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.0012110050464982456,
              "contribution_to_total_DeltaCE": 0.00016451723190566246,
              "DeltaMRR_positive_anchor_full_negative_population": 0.008794508794508795
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0010835734179702474,
              "contribution_to_total_DeltaCE": 0.00014720541405380575,
              "DeltaMRR_positive_anchor_full_negative_population": 0.008794508794508795
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.00046171909274140356,
              "contribution_to_total_DeltaCE": 6.272537614558951e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.008794508794508793
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.00031687952995580786,
              "contribution_to_total_DeltaCE": 4.304865885294433e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.005040755040755041
            }
          }
        },
        "degree16plus": {
          "candidate_count": 39795,
          "positive_count": 2096,
          "negative_count": 37699,
          "positive_anchored_query_count": 2096,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.0042024698539293165,
              "contribution_to_total_DeltaCE": 0.0035937185799621188,
              "DeltaMRR_positive_anchor_full_negative_population": -4.182363438088624e-05
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.004078793237808887,
              "contribution_to_total_DeltaCE": 0.0034879572137400004,
              "DeltaMRR_positive_anchor_full_negative_population": -0.00028698241961600733
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.004647198352713284,
              "contribution_to_total_DeltaCE": 0.0039740256671442565,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0009057656719870463
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.003509644251595438,
              "contribution_to_total_DeltaCE": 0.003001252642948265,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0013258608439906156
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -0.0005006611813316191,
              "contribution_to_total_DeltaCE": -0.00042813760768204795,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0006758905852417304
            }
          }
        }
      },
      "ranking_rule": "subgroup positive anchors, original full negative population; no filtered-negative ranking",
      "calibration_warning": "H0 uses a constant HDP raw block; improvements there do not prove incremental structural information",
      "all_pairwise_subgroups": {
        "GM_vs_GMH": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0038342381398866524,
            "contribution_to_total": -0.003449875046312404,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0012350126465295003
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.007614369317766805,
            "contribution_to_total": -0.00039416829307418414,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002702702702702703
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.002244802409359412,
            "contribution_to_total": 0.00010882487183072963,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0005686125852918878
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0038342381398866524,
            "contribution_to_total": -0.003449875046312404,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0012350126465295003
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.00590268757188943,
            "contribution_to_total": -0.000200916647624911,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.0004520349327777549,
            "contribution_to_total": 1.0014784590292791e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0023020257826887663
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.0021438694403933694,
            "contribution_to_total": -9.444155820883632e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0013092432573972245
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0038342381398866524,
            "contribution_to_total": -0.003449875046312404,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0012350126465295003
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.005367092160627224,
            "contribution_to_total": -0.00025361517236589446,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.0008954596614643195,
            "contribution_to_total": -2.3052275108179793e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0006297229219143577
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.00031841097423649815,
            "contribution_to_total": -8.675973769380257e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001049317943336831
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.00028979671064714035,
            "contribution_to_total": 2.609266412264737e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001984126984126983
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0010607819662801989,
            "contribution_to_total": -0.0001441091540060043,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004290004290004291
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0042024698539293165,
            "contribution_to_total": -0.0035937185799621188,
            "DeltaMRR_positive_anchor_full_negative_population": 4.182363438088624e-05
          }
        },
        "GM_vs_GMS": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.003880924893175679,
            "contribution_to_total": -0.003491881687342248,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002003532516172965
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.006019102306722478,
            "contribution_to_total": -0.0003115871036809019,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0001801801801801803
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.00308771367879765,
            "contribution_to_total": 0.0001496880277498603,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001326762699014405
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.003880924893175679,
            "contribution_to_total": -0.003491881687342248,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002003532516172965
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.0067265203186435175,
            "contribution_to_total": -0.00022895840176919658,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0006666666666666671
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.0024852724681055176,
            "contribution_to_total": 5.506094023157961e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0023020257826887663
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.00027236920614028914,
            "contribution_to_total": 1.1998385606575397e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001702016234616392
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.003880924893175679,
            "contribution_to_total": -0.003491881687342248,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002003532516172965
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.00531005764964352,
            "contribution_to_total": -0.00025092007846755414,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0030303030303030303
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.0007082770609194969,
            "contribution_to_total": 1.8233537884252133e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0006297229219143577
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.0025979222831684487,
            "contribution_to_total": 7.078746465226046e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002098635886673662
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.00014508543465209563,
            "contribution_to_total": -1.3063176276265272e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001984126984126983
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0012110050464982456,
            "contribution_to_total": -0.00016451723190566246,
            "DeltaMRR_positive_anchor_full_negative_population": -0.008794508794508795
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.004078793237808887,
            "contribution_to_total": -0.0034879572137400004,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00028698241961600733
          }
        },
        "GM_vs_GMP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0033806106177322924,
            "contribution_to_total": -0.0030417214022492012,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0022567671092951994
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.01325981304099131,
            "contribution_to_total": -0.0006864124466165563,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.007824789048942501,
            "contribution_to_total": -0.0003793347965964905,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0009476876421531463
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0033806106177322924,
            "contribution_to_total": -0.0030417214022492012,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0022567671092951994
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.012154450773172046,
            "contribution_to_total": -0.0004137151887722306,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.017334178027032944,
            "contribution_to_total": -0.0003840368219415284,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00046040515653775313
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.006083622507115539,
            "contribution_to_total": -0.00026799523249928776,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0009164702801780571
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0033806106177322924,
            "contribution_to_total": -0.0030417214022492012,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0022567671092951994
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.013245743221360684,
            "contribution_to_total": -0.0006259108935828637,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003246753246753247
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.0166332319533137,
            "contribution_to_total": -0.0004281977797848937,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0006297229219143577
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.00042713918479525466,
            "contribution_to_total": -1.1638569845289302e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0015739769150052466
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.0015285172062097124,
            "contribution_to_total": 1.3762435735814627e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001984126984126983
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0010835734179702474,
            "contribution_to_total": -0.00014720541405380575,
            "DeltaMRR_positive_anchor_full_negative_population": -0.008794508794508795
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.004647198352713284,
            "contribution_to_total": -0.0039740256671442565,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0009057656719870463
          }
        },
        "GM_vs_GMG": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0026632699065572006,
            "contribution_to_total": -0.002396290490318389,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00227622330852668
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.008824826844286265,
            "contribution_to_total": -0.0004568292906112604,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0001801801801801803
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.0044276741728533795,
            "contribution_to_total": -0.0002146474328252799,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001579479403588577
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0026632699065572006,
            "contribution_to_total": -0.002396290490318389,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00227622330852668
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.010515239520850195,
            "contribution_to_total": -0.00035791944733167246,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0006666666666666671
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.014643248548358032,
            "contribution_to_total": -0.0003244195730908787,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00046040515653775405
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.0002465794402639033,
            "contribution_to_total": 1.086229698601087e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001702016234616392
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0026632699065572006,
            "contribution_to_total": -0.002396290490318389,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00227622330852668
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.009143317498639062,
            "contribution_to_total": -0.0004320559390473461,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00021645021645021659
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.011711655196373636,
            "contribution_to_total": -0.00030149911735550145,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0010495382031905963
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.002278294402933814,
            "contribution_to_total": 6.20783329663073e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0026232948583420775
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.0004208447798276003,
            "contribution_to_total": -3.7891946610745343e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001984126984126983
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.00046171909274140356,
            "contribution_to_total": -6.272537614558951e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.008794508794508793
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.003509644251595438,
            "contribution_to_total": -0.003001252642948265,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0013258608439906156
          }
        },
        "GM_vs_GDUP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0007410048511265311,
            "contribution_to_total": 0.0006667228408440559,
            "DeltaMRR_positive_anchor_full_negative_population": 0.000314339218833601
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.006010043479299763,
            "contribution_to_total": 0.0003111181610287332,
            "DeltaMRR_positive_anchor_full_negative_population": -0.01099099099099099
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.012466462097078338,
            "contribution_to_total": -0.0006043565947010643,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002021733636593379
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0007410048511265311,
            "contribution_to_total": 0.0006667228408440559,
            "DeltaMRR_positive_anchor_full_negative_population": 0.000314339218833601
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.003097207553590432,
            "contribution_to_total": 0.00010542325865753919,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0006666666666666671
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.004167339923961398,
            "contribution_to_total": -9.232696109687557e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0009208103130755068
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.0069539478305651915,
            "contribution_to_total": -0.00030633473123299474,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00039277297721916735
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0007410048511265311,
            "contribution_to_total": 0.0006667228408440559,
            "DeltaMRR_positive_anchor_full_negative_population": 0.000314339218833601
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.007539374276950865,
            "contribution_to_total": 0.00035626362461352394,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006709956709956709
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.00641438783978729,
            "contribution_to_total": -0.00016512886006672626,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00041981528127623866
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.017776649173758183,
            "contribution_to_total": -0.00048437319821912874,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0015739769150052466
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.0012888519106629658,
            "contribution_to_total": -1.1604541657378861e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.00031687952995580786,
            "contribution_to_total": -4.304865885294433e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005040755040755041
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0005006611813316191,
            "contribution_to_total": 0.00042813760768204795,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0006758905852417304
          }
        },
        "GMH_vs_GM": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0038342381398866524,
            "contribution_to_total": 0.003449875046312404,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0012350126465295003
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.007614369317766805,
            "contribution_to_total": 0.00039416829307418414,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002702702702702703
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.002244802409359412,
            "contribution_to_total": -0.00010882487183072963,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0005686125852918878
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0038342381398866524,
            "contribution_to_total": 0.003449875046312404,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0012350126465295003
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.00590268757188943,
            "contribution_to_total": 0.000200916647624911,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.0004520349327777549,
            "contribution_to_total": -1.0014784590292791e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0023020257826887663
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.0021438694403933694,
            "contribution_to_total": 9.444155820883632e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0013092432573972245
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0038342381398866524,
            "contribution_to_total": 0.003449875046312404,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0012350126465295003
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.005367092160627224,
            "contribution_to_total": 0.00025361517236589446,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.0008954596614643195,
            "contribution_to_total": 2.3052275108179793e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0006297229219143577
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.00031841097423649815,
            "contribution_to_total": 8.675973769380257e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001049317943336831
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.00028979671064714035,
            "contribution_to_total": -2.609266412264737e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001984126984126983
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0010607819662801989,
            "contribution_to_total": 0.0001441091540060043,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004290004290004291
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0042024698539293165,
            "contribution_to_total": 0.0035937185799621188,
            "DeltaMRR_positive_anchor_full_negative_population": -4.182363438088624e-05
          }
        },
        "GMH_vs_GMS": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -4.668675328902598e-05,
            "contribution_to_total": -4.2006641029843706e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0007685198696434652
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.0015952670110443278,
            "contribution_to_total": 8.258118939328231e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0025225225225225228
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.000842911269438238,
            "contribution_to_total": 4.086315591913067e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.000758150113722517
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -4.668675328902598e-05,
            "contribution_to_total": -4.2006641029843706e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0007685198696434652
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.0008238327467540863,
            "contribution_to_total": -2.804175414428556e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0006666666666666671
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.0020332375353277633,
            "contribution_to_total": 4.504615564128683e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.0024162386465336584,
            "contribution_to_total": 0.00010643994381541173,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00039277297721916735
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -4.668675328902598e-05,
            "contribution_to_total": -4.2006641029843706e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0007685198696434652
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 5.703451098370421e-05,
            "contribution_to_total": 2.6950938983403293e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0030303030303030303
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.001603736722383817,
            "contribution_to_total": 4.1285812992431936e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.002916333257404946,
            "contribution_to_total": 7.94634384216407e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001049317943336831
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.00043488214529923596,
            "contribution_to_total": -3.915584039891265e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0001502230802180469,
            "contribution_to_total": -2.0408077899658165e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0045045045045045045
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.00012367661612043012,
            "contribution_to_total": 0.00010576136622211872,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0002451587852351211
          }
        },
        "GMH_vs_GMP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0004536275221543599,
            "contribution_to_total": 0.00040815364406320275,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0034917797558247
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.005645443723224503,
            "contribution_to_total": -0.0002922441535423721,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002702702702702703
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.010069591458301913,
            "contribution_to_total": -0.0004881596684272201,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0003790750568612585
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0004536275221543599,
            "contribution_to_total": 0.00040815364406320275,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0034917797558247
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.006251763201282614,
            "contribution_to_total": -0.00021279854114731952,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.0177862129598107,
            "contribution_to_total": -0.00039405160653182116,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0027624309392265192
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.00393975306672217,
            "contribution_to_total": -0.00017355367429045145,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00039277297721916735
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0004536275221543599,
            "contribution_to_total": 0.00040815364406320275,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0034917797558247
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.00787865106073346,
            "contribution_to_total": -0.00037229572121696926,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003246753246753247
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.01573777229184938,
            "contribution_to_total": -0.00040514550467671387,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.00010872821055875639,
            "contribution_to_total": -2.9625960759090405e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0005246589716684155
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.001238720495562572,
            "contribution_to_total": 1.1153169323549888e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -2.279145169004873e-05,
            "contribution_to_total": -3.0962600478014456e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0045045045045045045
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.00044472849878396696,
            "contribution_to_total": -0.00038030708718213784,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0009475893063679323
          }
        },
        "GMH_vs_GMG": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0011709682333294524,
            "contribution_to_total": 0.0010535845559940156,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0035112359550561797
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.0012104575265194607,
            "contribution_to_total": -6.266099753707626e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0025225225225225228
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.006672476582212792,
            "contribution_to_total": -0.0003234723046560095,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0010108668182966893
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0011709682333294524,
            "contribution_to_total": 0.0010535845559940156,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0035112359550561797
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.0046125519489607645,
            "contribution_to_total": -0.00015700279970676145,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0006666666666666671
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.015095283481135788,
            "contribution_to_total": -0.0003344343576811715,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0018416206261510127
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.0023904488806572727,
            "contribution_to_total": 0.0001053038551948472,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00039277297721916735
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0011709682333294524,
            "contribution_to_total": 0.0010535845559940156,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0035112359550561797
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.003776225338011839,
            "contribution_to_total": -0.00017844076668145165,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00021645021645021659
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.010816195534909315,
            "contribution_to_total": -0.00027844684224732165,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001679261125104954
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.002596705377170312,
            "contribution_to_total": 7.075430673568754e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0015739769150052466
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.0007106414904747407,
            "contribution_to_total": -6.398461073339272e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0005990628735387953,
            "contribution_to_total": 8.138377786041481e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0045045045045045045
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0006928256023338791,
            "contribution_to_total": 0.0005924659370138541,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0013676844783715014
          }
        },
        "GMH_vs_GDUP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.004575242991013184,
            "contribution_to_total": 0.00411659788715646,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0009206734276958994
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.013624412797066564,
            "contribution_to_total": 0.0007052864541029172,
            "DeltaMRR_positive_anchor_full_negative_population": -0.008288288288288289
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.014711264506437751,
            "contribution_to_total": -0.000713181466531794,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002590346221885267
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.004575242991013184,
            "contribution_to_total": 0.00411659788715646,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0009206734276958994
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.008999895125479863,
            "contribution_to_total": 0.0003063399062824502,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0006666666666666671
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.0046193748567391535,
            "contribution_to_total": -0.00010234174568716836,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0013812154696132596
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.0048100783901718226,
            "contribution_to_total": -0.00021189317302415842,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001702016234616392
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.004575242991013184,
            "contribution_to_total": 0.00411659788715646,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0009206734276958994
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.012906466437578088,
            "contribution_to_total": 0.0006098787969794184,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006709956709956709
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.005518928178322972,
            "contribution_to_total": -0.0001420765849585465,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0010495382031905961
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.01745823819952168,
            "contribution_to_total": -0.0004756972244497484,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0026232948583420775
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.0015786486213101058,
            "contribution_to_total": -1.4213808069643594e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001984126984126983
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0007439024363243909,
            "contribution_to_total": 0.00010106049515305998,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0007507507507507506
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.004703131035260937,
            "contribution_to_total": 0.0040218561876441674,
            "DeltaMRR_positive_anchor_full_negative_population": 0.000634066950860844
          }
        },
        "GMS_vs_GM": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.003880924893175679,
            "contribution_to_total": 0.003491881687342248,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002003532516172965
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.006019102306722478,
            "contribution_to_total": 0.0003115871036809019,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0001801801801801803
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.00308771367879765,
            "contribution_to_total": -0.0001496880277498603,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001326762699014405
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.003880924893175679,
            "contribution_to_total": 0.003491881687342248,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002003532516172965
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.0067265203186435175,
            "contribution_to_total": 0.00022895840176919658,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0006666666666666671
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.0024852724681055176,
            "contribution_to_total": -5.506094023157961e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0023020257826887663
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.00027236920614028914,
            "contribution_to_total": -1.1998385606575397e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001702016234616392
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.003880924893175679,
            "contribution_to_total": 0.003491881687342248,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002003532516172965
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.00531005764964352,
            "contribution_to_total": 0.00025092007846755414,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0030303030303030303
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.0007082770609194969,
            "contribution_to_total": -1.8233537884252133e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0006297229219143577
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.0025979222831684487,
            "contribution_to_total": -7.078746465226046e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002098635886673662
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.00014508543465209563,
            "contribution_to_total": 1.3063176276265272e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001984126984126983
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0012110050464982456,
            "contribution_to_total": 0.00016451723190566246,
            "DeltaMRR_positive_anchor_full_negative_population": 0.008794508794508795
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.004078793237808887,
            "contribution_to_total": 0.0034879572137400004,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00028698241961600733
          }
        },
        "GMS_vs_GMH": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 4.668675328902598e-05,
            "contribution_to_total": 4.2006641029843706e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0007685198696434652
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.0015952670110443278,
            "contribution_to_total": -8.258118939328231e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0025225225225225228
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.000842911269438238,
            "contribution_to_total": -4.086315591913067e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.000758150113722517
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 4.668675328902598e-05,
            "contribution_to_total": 4.2006641029843706e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0007685198696434652
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.0008238327467540863,
            "contribution_to_total": 2.804175414428556e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0006666666666666671
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.0020332375353277633,
            "contribution_to_total": -4.504615564128683e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.0024162386465336584,
            "contribution_to_total": -0.00010643994381541173,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00039277297721916735
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 4.668675328902598e-05,
            "contribution_to_total": 4.2006641029843706e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0007685198696434652
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -5.703451098370421e-05,
            "contribution_to_total": -2.6950938983403293e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0030303030303030303
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.001603736722383817,
            "contribution_to_total": -4.1285812992431936e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.002916333257404946,
            "contribution_to_total": -7.94634384216407e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001049317943336831
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.00043488214529923596,
            "contribution_to_total": 3.915584039891265e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0001502230802180469,
            "contribution_to_total": 2.0408077899658165e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0045045045045045045
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.00012367661612043012,
            "contribution_to_total": -0.00010576136622211872,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0002451587852351211
          }
        },
        "GMS_vs_GMP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0005003142754433858,
            "contribution_to_total": 0.00045016028509304646,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004260299625468165
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.00724071073426883,
            "contribution_to_total": -0.00037482534293565434,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0001801801801801803
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.010912502727740149,
            "contribution_to_total": -0.0005290228243463507,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0003790750568612585
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0005003142754433858,
            "contribution_to_total": 0.00045016028509304646,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004260299625468165
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.005427930454528528,
            "contribution_to_total": -0.00018475678700303395,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0006666666666666671
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.01981945049513846,
            "contribution_to_total": -0.000439097762173108,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0027624309392265192
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.006355991713255828,
            "contribution_to_total": -0.0002799936181058631,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0007855459544383347
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0005003142754433858,
            "contribution_to_total": 0.00045016028509304646,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004260299625468165
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.007935685571717163,
            "contribution_to_total": -0.00037499081511530946,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00021645021645021659
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.017341509014233196,
            "contribution_to_total": -0.00044643131766914577,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.003025061467963703,
            "contribution_to_total": -8.242603449754975e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0005246589716684155
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.001673602640861808,
            "contribution_to_total": 1.5068753363441155e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.00012743162852799818,
            "contribution_to_total": 1.7311817851856724e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0005684051149043972,
            "contribution_to_total": -0.00048606845340425667,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0011927480916030535
          }
        },
        "GMS_vs_GMG": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0012176549866184782,
            "contribution_to_total": 0.001095591197023859,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004279755824699645
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.002805724537563788,
            "contribution_to_total": -0.00014524218693035855,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.007515387851651032,
            "contribution_to_total": -0.0003643354605751403,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0002527167045741723
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0012176549866184782,
            "contribution_to_total": 0.001095591197023859,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004279755824699645
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.003788719202206678,
            "contribution_to_total": -0.00012896104556247588,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.01712852101646355,
            "contribution_to_total": -0.0003794805133224583,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0018416206261510127
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -2.5789765876385582e-05,
            "contribution_to_total": -1.1360886205645187e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0012176549866184782,
            "contribution_to_total": 0.001095591197023859,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004279755824699645
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.0038332598489955426,
            "contribution_to_total": -0.00018113586057979196,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003246753246753247
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.012419932257293135,
            "contribution_to_total": -0.0003197326552397536,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001679261125104954
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.0003196278802346343,
            "contribution_to_total": -8.709131685953162e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0005246589716684155
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.00027575934517550476,
            "contribution_to_total": -2.4828770334480076e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.000749285953756842,
            "contribution_to_total": 0.00010179185576007295,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0005691489862134488,
            "contribution_to_total": 0.00048670457079173535,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0016128432636066225
          }
        },
        "GMS_vs_GDUP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.00462192974430221,
            "contribution_to_total": 0.0041586045281863035,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0016891932973393646
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.012029145786022242,
            "contribution_to_total": 0.0006227052647096352,
            "DeltaMRR_positive_anchor_full_negative_population": -0.010810810810810811
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.015554175775875985,
            "contribution_to_total": -0.0007540446224509245,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003348496335607784
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.00462192974430221,
            "contribution_to_total": 0.0041586045281863035,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0016891932973393646
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.009823727872233949,
            "contribution_to_total": 0.0003343816604267358,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.006652612392066916,
            "contribution_to_total": -0.0001473879013284552,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0013812154696132596
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.007226317036705482,
            "contribution_to_total": -0.00031833311683957015,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002094789211835559
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.00462192974430221,
            "contribution_to_total": 0.0041586045281863035,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0016891932973393646
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.012849431926594384,
            "contribution_to_total": 0.0006071837030810781,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00974025974025974
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.007122664900706786,
            "contribution_to_total": -0.0001833623979509784,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0010495382031905961
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.020374571456926633,
            "contribution_to_total": -0.0005551606628713893,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0036726128016789086
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.00114376647601087,
            "contribution_to_total": -1.0298224029752334e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001984126984126983
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0008941255165424378,
            "contribution_to_total": 0.00012146857305271815,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0037537537537537537
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.004579454419140507,
            "contribution_to_total": 0.0039160948214220495,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00038890816562572297
          }
        },
        "GMP_vs_GM": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0033806106177322924,
            "contribution_to_total": 0.0030417214022492012,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0022567671092951994
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.01325981304099131,
            "contribution_to_total": 0.0006864124466165563,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.007824789048942501,
            "contribution_to_total": 0.0003793347965964905,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0009476876421531463
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0033806106177322924,
            "contribution_to_total": 0.0030417214022492012,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0022567671092951994
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.012154450773172046,
            "contribution_to_total": 0.0004137151887722306,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.017334178027032944,
            "contribution_to_total": 0.0003840368219415284,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00046040515653775313
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.006083622507115539,
            "contribution_to_total": 0.00026799523249928776,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0009164702801780571
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0033806106177322924,
            "contribution_to_total": 0.0030417214022492012,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0022567671092951994
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.013245743221360684,
            "contribution_to_total": 0.0006259108935828637,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003246753246753247
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.0166332319533137,
            "contribution_to_total": 0.0004281977797848937,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0006297229219143577
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.00042713918479525466,
            "contribution_to_total": 1.1638569845289302e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0015739769150052466
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.0015285172062097124,
            "contribution_to_total": -1.3762435735814627e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001984126984126983
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0010835734179702474,
            "contribution_to_total": 0.00014720541405380575,
            "DeltaMRR_positive_anchor_full_negative_population": 0.008794508794508795
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.004647198352713284,
            "contribution_to_total": 0.0039740256671442565,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0009057656719870463
          }
        },
        "GMP_vs_GMH": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0004536275221543599,
            "contribution_to_total": -0.00040815364406320275,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0034917797558247
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.005645443723224503,
            "contribution_to_total": 0.0002922441535423721,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002702702702702703
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.010069591458301913,
            "contribution_to_total": 0.0004881596684272201,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0003790750568612585
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0004536275221543599,
            "contribution_to_total": -0.00040815364406320275,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0034917797558247
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.006251763201282614,
            "contribution_to_total": 0.00021279854114731952,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.0177862129598107,
            "contribution_to_total": 0.00039405160653182116,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0027624309392265192
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.00393975306672217,
            "contribution_to_total": 0.00017355367429045145,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00039277297721916735
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0004536275221543599,
            "contribution_to_total": -0.00040815364406320275,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0034917797558247
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.00787865106073346,
            "contribution_to_total": 0.00037229572121696926,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003246753246753247
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.01573777229184938,
            "contribution_to_total": 0.00040514550467671387,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.00010872821055875639,
            "contribution_to_total": 2.9625960759090405e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0005246589716684155
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.001238720495562572,
            "contribution_to_total": -1.1153169323549888e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 2.279145169004873e-05,
            "contribution_to_total": 3.0962600478014456e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0045045045045045045
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.00044472849878396696,
            "contribution_to_total": 0.00038030708718213784,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0009475893063679323
          }
        },
        "GMP_vs_GMS": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0005003142754433858,
            "contribution_to_total": -0.00045016028509304646,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004260299625468165
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.00724071073426883,
            "contribution_to_total": 0.00037482534293565434,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0001801801801801803
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.010912502727740149,
            "contribution_to_total": 0.0005290228243463507,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0003790750568612585
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0005003142754433858,
            "contribution_to_total": -0.00045016028509304646,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004260299625468165
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.005427930454528528,
            "contribution_to_total": 0.00018475678700303395,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0006666666666666671
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.01981945049513846,
            "contribution_to_total": 0.000439097762173108,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0027624309392265192
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.006355991713255828,
            "contribution_to_total": 0.0002799936181058631,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0007855459544383347
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0005003142754433858,
            "contribution_to_total": -0.00045016028509304646,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004260299625468165
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.007935685571717163,
            "contribution_to_total": 0.00037499081511530946,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00021645021645021659
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.017341509014233196,
            "contribution_to_total": 0.00044643131766914577,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.003025061467963703,
            "contribution_to_total": 8.242603449754975e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0005246589716684155
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.001673602640861808,
            "contribution_to_total": -1.5068753363441155e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.00012743162852799818,
            "contribution_to_total": -1.7311817851856724e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0005684051149043972,
            "contribution_to_total": 0.00048606845340425667,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0011927480916030535
          }
        },
        "GMP_vs_GMG": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0007173407111750925,
            "contribution_to_total": 0.0006454309119308127,
            "DeltaMRR_positive_anchor_full_negative_population": -1.9456199231480033e-05
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.004434986196705042,
            "contribution_to_total": 0.00022958315600529584,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0001801801801801803
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.0033971148760891198,
            "contribution_to_total": 0.00016468736377121056,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0006317917614354308
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0007173407111750925,
            "contribution_to_total": 0.0006454309119308127,
            "DeltaMRR_positive_anchor_full_negative_population": -1.9456199231480033e-05
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.00163921125232185,
            "contribution_to_total": 5.5795741440558076e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0006666666666666671
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.0026909294786749117,
            "contribution_to_total": 5.961724885064969e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0009208103130755068
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.006330201947379442,
            "contribution_to_total": 0.0002788575294852986,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0007855459544383347
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0007173407111750925,
            "contribution_to_total": 0.0006454309119308127,
            "DeltaMRR_positive_anchor_full_negative_population": -1.9456199231480033e-05
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.004102425722721622,
            "contribution_to_total": 0.0001938549545355176,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003463203463203463
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.004921576756940064,
            "contribution_to_total": 0.00012669866242939222,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001679261125104954
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.0027054335877290687,
            "contribution_to_total": 7.371690281159658e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001049317943336831
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.0019493619860373127,
            "contribution_to_total": -1.755163039688916e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0006218543252288441,
            "contribution_to_total": 8.448003790821627e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0011375541011178463,
            "contribution_to_total": 0.0009727730241959921,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00042009517200356894
          }
        },
        "GMP_vs_GDUP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0041216154688588245,
            "contribution_to_total": 0.0037084442430932573,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0025711063281288003
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.019269856520291073,
            "contribution_to_total": 0.0009975306076452895,
            "DeltaMRR_positive_anchor_full_negative_population": -0.01099099099099099
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.004641673048135837,
            "contribution_to_total": -0.00022502179810457386,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0029694212787465253
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0041216154688588245,
            "contribution_to_total": 0.0037084442430932573,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0025711063281288003
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.015251658326762478,
            "contribution_to_total": 0.0005191384474297697,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0006666666666666671
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.013166838103071546,
            "contribution_to_total": 0.00029170986084465285,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00138121546961326
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.0008703253234496537,
            "contribution_to_total": -3.833949873370702e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0013092432573972245
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0041216154688588245,
            "contribution_to_total": 0.0037084442430932573,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0025711063281288003
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.020785117498311547,
            "contribution_to_total": 0.0009821745181963876,
            "DeltaMRR_positive_anchor_full_negative_population": -0.009956709956709955
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.01021884411352641,
            "contribution_to_total": 0.0002630689197181674,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0010495382031905963
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.017349509988962925,
            "contribution_to_total": -0.0004727346283738394,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0031479538300104933
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.002817369116872678,
            "contribution_to_total": -2.5366977393193487e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001984126984126983
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0007666938880144397,
            "contribution_to_total": 0.00010415675520086144,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0037537537537537537
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.005147859534044905,
            "contribution_to_total": 0.004402163274826306,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0015816562572287766
          }
        },
        "GMG_vs_GM": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0026632699065572006,
            "contribution_to_total": 0.002396290490318389,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00227622330852668
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.008824826844286265,
            "contribution_to_total": 0.0004568292906112604,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0001801801801801803
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.0044276741728533795,
            "contribution_to_total": 0.0002146474328252799,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001579479403588577
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0026632699065572006,
            "contribution_to_total": 0.002396290490318389,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00227622330852668
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.010515239520850195,
            "contribution_to_total": 0.00035791944733167246,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0006666666666666671
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.014643248548358032,
            "contribution_to_total": 0.0003244195730908787,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00046040515653775405
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.0002465794402639033,
            "contribution_to_total": -1.086229698601087e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001702016234616392
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0026632699065572006,
            "contribution_to_total": 0.002396290490318389,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00227622330852668
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.009143317498639062,
            "contribution_to_total": 0.0004320559390473461,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00021645021645021659
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.011711655196373636,
            "contribution_to_total": 0.00030149911735550145,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0010495382031905963
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.002278294402933814,
            "contribution_to_total": -6.20783329663073e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0026232948583420775
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.0004208447798276003,
            "contribution_to_total": 3.7891946610745343e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001984126984126983
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.00046171909274140356,
            "contribution_to_total": 6.272537614558951e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.008794508794508793
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.003509644251595438,
            "contribution_to_total": 0.003001252642948265,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0013258608439906156
          }
        },
        "GMG_vs_GMH": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0011709682333294524,
            "contribution_to_total": -0.0010535845559940156,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0035112359550561797
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.0012104575265194607,
            "contribution_to_total": 6.266099753707626e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0025225225225225228
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.006672476582212792,
            "contribution_to_total": 0.0003234723046560095,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0010108668182966893
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0011709682333294524,
            "contribution_to_total": -0.0010535845559940156,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0035112359550561797
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.0046125519489607645,
            "contribution_to_total": 0.00015700279970676145,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0006666666666666671
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.015095283481135788,
            "contribution_to_total": 0.0003344343576811715,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0018416206261510127
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.0023904488806572727,
            "contribution_to_total": -0.0001053038551948472,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00039277297721916735
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0011709682333294524,
            "contribution_to_total": -0.0010535845559940156,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0035112359550561797
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.003776225338011839,
            "contribution_to_total": 0.00017844076668145165,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00021645021645021659
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.010816195534909315,
            "contribution_to_total": 0.00027844684224732165,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001679261125104954
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.002596705377170312,
            "contribution_to_total": -7.075430673568754e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0015739769150052466
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.0007106414904747407,
            "contribution_to_total": 6.398461073339272e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0005990628735387953,
            "contribution_to_total": -8.138377786041481e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0045045045045045045
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0006928256023338791,
            "contribution_to_total": -0.0005924659370138541,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0013676844783715014
          }
        },
        "GMG_vs_GMS": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0012176549866184782,
            "contribution_to_total": -0.001095591197023859,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004279755824699645
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.002805724537563788,
            "contribution_to_total": 0.00014524218693035855,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.007515387851651032,
            "contribution_to_total": 0.0003643354605751403,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0002527167045741723
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0012176549866184782,
            "contribution_to_total": -0.001095591197023859,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004279755824699645
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.003788719202206678,
            "contribution_to_total": 0.00012896104556247588,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.01712852101646355,
            "contribution_to_total": 0.0003794805133224583,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0018416206261510127
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 2.5789765876385582e-05,
            "contribution_to_total": 1.1360886205645187e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0012176549866184782,
            "contribution_to_total": -0.001095591197023859,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004279755824699645
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.0038332598489955426,
            "contribution_to_total": 0.00018113586057979196,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003246753246753247
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.012419932257293135,
            "contribution_to_total": 0.0003197326552397536,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001679261125104954
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.0003196278802346343,
            "contribution_to_total": 8.709131685953162e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0005246589716684155
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.00027575934517550476,
            "contribution_to_total": 2.4828770334480076e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.000749285953756842,
            "contribution_to_total": -0.00010179185576007295,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0005691489862134488,
            "contribution_to_total": -0.00048670457079173535,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0016128432636066225
          }
        },
        "GMG_vs_GMP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0007173407111750925,
            "contribution_to_total": -0.0006454309119308127,
            "DeltaMRR_positive_anchor_full_negative_population": 1.9456199231480033e-05
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.004434986196705042,
            "contribution_to_total": -0.00022958315600529584,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0001801801801801803
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.0033971148760891198,
            "contribution_to_total": -0.00016468736377121056,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0006317917614354308
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0007173407111750925,
            "contribution_to_total": -0.0006454309119308127,
            "DeltaMRR_positive_anchor_full_negative_population": 1.9456199231480033e-05
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.00163921125232185,
            "contribution_to_total": -5.5795741440558076e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0006666666666666671
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.0026909294786749117,
            "contribution_to_total": -5.961724885064969e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0009208103130755068
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.006330201947379442,
            "contribution_to_total": -0.0002788575294852986,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0007855459544383347
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0007173407111750925,
            "contribution_to_total": -0.0006454309119308127,
            "DeltaMRR_positive_anchor_full_negative_population": 1.9456199231480033e-05
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.004102425722721622,
            "contribution_to_total": -0.0001938549545355176,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003463203463203463
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.004921576756940064,
            "contribution_to_total": -0.00012669866242939222,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001679261125104954
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.0027054335877290687,
            "contribution_to_total": -7.371690281159658e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001049317943336831
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.0019493619860373127,
            "contribution_to_total": 1.755163039688916e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0006218543252288441,
            "contribution_to_total": -8.448003790821627e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0011375541011178463,
            "contribution_to_total": -0.0009727730241959921,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00042009517200356894
          }
        },
        "GMG_vs_GDUP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.003404274757683732,
            "contribution_to_total": 0.003063013331162445,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0025905625273602803
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.01483487032358603,
            "contribution_to_total": 0.0007679474516399937,
            "DeltaMRR_positive_anchor_full_negative_population": -0.010810810810810811
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.008038787924224957,
            "contribution_to_total": -0.00038970916187578444,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003601213040181956
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.003404274757683732,
            "contribution_to_total": 0.003063013331162445,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0025905625273602803
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.013612447074440629,
            "contribution_to_total": 0.0004633427059892117,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.010475908624396636,
            "contribution_to_total": 0.00023209261199400318,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00046040515653775313
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.007200527270829095,
            "contribution_to_total": -0.0003171970282190056,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002094789211835559
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.003404274757683732,
            "contribution_to_total": 0.003063013331162445,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0025905625273602803
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.016682691775589925,
            "contribution_to_total": 0.00078831956366087,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.005297267356586345,
            "contribution_to_total": 0.0001363702572887752,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0006297229219143577
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.020054943576692,
            "contribution_to_total": -0.0005464515311854361,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004197271773347324
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.0008680071308353655,
            "contribution_to_total": -7.815346996304327e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001984126984126983
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0001448395627855956,
            "contribution_to_total": 1.9676717292645164e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0037537537537537537
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0040103054329270575,
            "contribution_to_total": 0.0034293902506303134,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0020017514292323454
          }
        },
        "GDUP_vs_GM": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0007410048511265311,
            "contribution_to_total": -0.0006667228408440559,
            "DeltaMRR_positive_anchor_full_negative_population": -0.000314339218833601
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.006010043479299763,
            "contribution_to_total": -0.0003111181610287332,
            "DeltaMRR_positive_anchor_full_negative_population": 0.01099099099099099
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.012466462097078338,
            "contribution_to_total": 0.0006043565947010643,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002021733636593379
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0007410048511265311,
            "contribution_to_total": -0.0006667228408440559,
            "DeltaMRR_positive_anchor_full_negative_population": -0.000314339218833601
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.003097207553590432,
            "contribution_to_total": -0.00010542325865753919,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0006666666666666671
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.004167339923961398,
            "contribution_to_total": 9.232696109687557e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0009208103130755068
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.0069539478305651915,
            "contribution_to_total": 0.00030633473123299474,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00039277297721916735
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0007410048511265311,
            "contribution_to_total": -0.0006667228408440559,
            "DeltaMRR_positive_anchor_full_negative_population": -0.000314339218833601
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.007539374276950865,
            "contribution_to_total": -0.00035626362461352394,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006709956709956709
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.00641438783978729,
            "contribution_to_total": 0.00016512886006672626,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00041981528127623866
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.017776649173758183,
            "contribution_to_total": 0.00048437319821912874,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0015739769150052466
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.0012888519106629658,
            "contribution_to_total": 1.1604541657378861e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.00031687952995580786,
            "contribution_to_total": 4.304865885294433e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005040755040755041
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0005006611813316191,
            "contribution_to_total": -0.00042813760768204795,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0006758905852417304
          }
        },
        "GDUP_vs_GMH": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.004575242991013184,
            "contribution_to_total": -0.00411659788715646,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0009206734276958994
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.013624412797066564,
            "contribution_to_total": -0.0007052864541029172,
            "DeltaMRR_positive_anchor_full_negative_population": 0.008288288288288289
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.014711264506437751,
            "contribution_to_total": 0.000713181466531794,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002590346221885267
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.004575242991013184,
            "contribution_to_total": -0.00411659788715646,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0009206734276958994
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.008999895125479863,
            "contribution_to_total": -0.0003063399062824502,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0006666666666666671
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.0046193748567391535,
            "contribution_to_total": 0.00010234174568716836,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0013812154696132596
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.0048100783901718226,
            "contribution_to_total": 0.00021189317302415842,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001702016234616392
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.004575242991013184,
            "contribution_to_total": -0.00411659788715646,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0009206734276958994
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.012906466437578088,
            "contribution_to_total": -0.0006098787969794184,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006709956709956709
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.005518928178322972,
            "contribution_to_total": 0.0001420765849585465,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0010495382031905961
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.01745823819952168,
            "contribution_to_total": 0.0004756972244497484,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0026232948583420775
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.0015786486213101058,
            "contribution_to_total": 1.4213808069643594e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001984126984126983
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0007439024363243909,
            "contribution_to_total": -0.00010106049515305998,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0007507507507507506
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.004703131035260937,
            "contribution_to_total": -0.0040218561876441674,
            "DeltaMRR_positive_anchor_full_negative_population": -0.000634066950860844
          }
        },
        "GDUP_vs_GMS": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.00462192974430221,
            "contribution_to_total": -0.0041586045281863035,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0016891932973393646
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.012029145786022242,
            "contribution_to_total": -0.0006227052647096352,
            "DeltaMRR_positive_anchor_full_negative_population": 0.010810810810810811
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.015554175775875985,
            "contribution_to_total": 0.0007540446224509245,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003348496335607784
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.00462192974430221,
            "contribution_to_total": -0.0041586045281863035,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0016891932973393646
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.009823727872233949,
            "contribution_to_total": -0.0003343816604267358,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.006652612392066916,
            "contribution_to_total": 0.0001473879013284552,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0013812154696132596
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.007226317036705482,
            "contribution_to_total": 0.00031833311683957015,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002094789211835559
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.00462192974430221,
            "contribution_to_total": -0.0041586045281863035,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0016891932973393646
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.012849431926594384,
            "contribution_to_total": -0.0006071837030810781,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00974025974025974
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.007122664900706786,
            "contribution_to_total": 0.0001833623979509784,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0010495382031905961
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.020374571456926633,
            "contribution_to_total": 0.0005551606628713893,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0036726128016789086
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.00114376647601087,
            "contribution_to_total": 1.0298224029752334e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001984126984126983
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0008941255165424378,
            "contribution_to_total": -0.00012146857305271815,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0037537537537537537
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.004579454419140507,
            "contribution_to_total": -0.0039160948214220495,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00038890816562572297
          }
        },
        "GDUP_vs_GMP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0041216154688588245,
            "contribution_to_total": -0.0037084442430932573,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0025711063281288003
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.019269856520291073,
            "contribution_to_total": -0.0009975306076452895,
            "DeltaMRR_positive_anchor_full_negative_population": 0.01099099099099099
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.004641673048135837,
            "contribution_to_total": 0.00022502179810457386,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0029694212787465253
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0041216154688588245,
            "contribution_to_total": -0.0037084442430932573,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0025711063281288003
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.015251658326762478,
            "contribution_to_total": -0.0005191384474297697,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0006666666666666671
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.013166838103071546,
            "contribution_to_total": -0.00029170986084465285,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00138121546961326
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.0008703253234496537,
            "contribution_to_total": 3.833949873370702e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0013092432573972245
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0041216154688588245,
            "contribution_to_total": -0.0037084442430932573,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0025711063281288003
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.020785117498311547,
            "contribution_to_total": -0.0009821745181963876,
            "DeltaMRR_positive_anchor_full_negative_population": 0.009956709956709955
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.01021884411352641,
            "contribution_to_total": -0.0002630689197181674,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0010495382031905963
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.017349509988962925,
            "contribution_to_total": 0.0004727346283738394,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0031479538300104933
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.002817369116872678,
            "contribution_to_total": 2.5366977393193487e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001984126984126983
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0007666938880144397,
            "contribution_to_total": -0.00010415675520086144,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0037537537537537537
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.005147859534044905,
            "contribution_to_total": -0.004402163274826306,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0015816562572287766
          }
        },
        "GDUP_vs_GMG": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.003404274757683732,
            "contribution_to_total": -0.003063013331162445,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0025905625273602803
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.01483487032358603,
            "contribution_to_total": -0.0007679474516399937,
            "DeltaMRR_positive_anchor_full_negative_population": 0.010810810810810811
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.008038787924224957,
            "contribution_to_total": 0.00038970916187578444,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003601213040181956
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.003404274757683732,
            "contribution_to_total": -0.003063013331162445,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0025905625273602803
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.013612447074440629,
            "contribution_to_total": -0.0004633427059892117,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.010475908624396636,
            "contribution_to_total": -0.00023209261199400318,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00046040515653775313
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.007200527270829095,
            "contribution_to_total": 0.0003171970282190056,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002094789211835559
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.003404274757683732,
            "contribution_to_total": -0.003063013331162445,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0025905625273602803
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.016682691775589925,
            "contribution_to_total": -0.00078831956366087,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006493506493506494
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.005297267356586345,
            "contribution_to_total": -0.0001363702572887752,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0006297229219143577
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.020054943576692,
            "contribution_to_total": 0.0005464515311854361,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004197271773347324
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.0008680071308353655,
            "contribution_to_total": 7.815346996304327e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001984126984126983
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0001448395627855956,
            "contribution_to_total": -1.9676717292645164e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0037537537537537537
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0040103054329270575,
            "contribution_to_total": -0.0034293902506303134,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0020017514292323454
          }
        }
      },
      "per_candidate_directory": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HDP_ZERO_V29/retrospective/pubmed/seed_0"
    },
    {
      "dataset": "pubmed",
      "seed": 1,
      "subgroups": {
        "H0": {
          "candidate_count": 41871,
          "positive_count": 712,
          "negative_count": 41159,
          "positive_anchored_query_count": 712,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.001861767748427176,
              "contribution_to_total_DeltaCE": 0.0016751348932953903,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0007490636704119848
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.001562305348785716,
              "contribution_to_total_DeltaCE": 0.0014056920934116966,
              "DeltaMRR_positive_anchor_full_negative_population": -6.632334581772791e-05
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0014135879651620221,
              "contribution_to_total_DeltaCE": 0.0012718828796909711,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0005149812734082397
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.00190320839691425,
              "contribution_to_total_DeltaCE": 0.0017124213251503472,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0005344881398252184
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -0.0012586811766939008,
              "contribution_to_total_DeltaCE": -0.0011325047178388844,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0049519067075246845
            }
          }
        },
        "H1": {
          "candidate_count": 2409,
          "positive_count": 185,
          "negative_count": 2224,
          "positive_anchored_query_count": 185,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.003477660838656143,
              "contribution_to_total_DeltaCE": -0.00018002589307896356,
              "DeltaMRR_positive_anchor_full_negative_population": 0.000900900900900901
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.007187850370854699,
              "contribution_to_total_DeltaCE": -0.0003720889535711916,
              "DeltaMRR_positive_anchor_full_negative_population": 0.002702702702702703
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -0.0003016312552724092,
              "contribution_to_total_DeltaCE": -1.5614356497147022e-05,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0045045045045045045
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": -0.0008964989712390396,
              "contribution_to_total_DeltaCE": -4.6408501412129245e-05,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0018018018018018016
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.0020354677731740938,
              "contribution_to_total_DeltaCE": 0.00010536878686557487,
              "DeltaMRR_positive_anchor_full_negative_population": 0.011711711711711714
            }
          }
        },
        "H2plus": {
          "candidate_count": 2256,
          "positive_count": 1319,
          "negative_count": 937,
          "positive_anchored_query_count": 1319,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.012462109799904926,
              "contribution_to_total_DeltaCE": -0.0006041456014394342,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0024008086934546374
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.016468701708262635,
              "contribution_to_total_DeltaCE": -0.0007983795567698234,
              "DeltaMRR_positive_anchor_full_negative_population": 0.00265352539802881
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -0.01216082906008514,
              "contribution_to_total_DeltaCE": -0.0005895399338050558,
              "DeltaMRR_positive_anchor_full_negative_population": 0.002274450341167551
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": -0.008080635140622915,
              "contribution_to_total_DeltaCE": -0.00039173785622411246,
              "DeltaMRR_positive_anchor_full_negative_population": 0.001516300227445034
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.02341634733466678,
              "contribution_to_total_DeltaCE": 0.0011351916706852385,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0018953752843062926
            }
          }
        },
        "G0": {
          "candidate_count": 41871,
          "positive_count": 712,
          "negative_count": 41159,
          "positive_anchored_query_count": 712,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.001861767748427176,
              "contribution_to_total_DeltaCE": 0.0016751348932953903,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0007490636704119848
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.001562305348785716,
              "contribution_to_total_DeltaCE": 0.0014056920934116966,
              "DeltaMRR_positive_anchor_full_negative_population": -6.632334581772791e-05
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0014135879651620221,
              "contribution_to_total_DeltaCE": 0.0012718828796909711,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0005149812734082397
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.00190320839691425,
              "contribution_to_total_DeltaCE": 0.0017124213251503472,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0005344881398252184
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -0.0012586811766939008,
              "contribution_to_total_DeltaCE": -0.0011325047178388844,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0049519067075246845
            }
          }
        },
        "G1": {
          "candidate_count": 1584,
          "positive_count": 50,
          "negative_count": 1534,
          "positive_anchored_query_count": 50,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.005601460252030679,
              "contribution_to_total_DeltaCE": -0.00019066342270965695,
              "DeltaMRR_positive_anchor_full_negative_population": 0.01
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.007214291491456348,
              "contribution_to_total_DeltaCE": -0.00024556123694487826,
              "DeltaMRR_positive_anchor_full_negative_population": 0.01
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.00012319679025356577,
              "contribution_to_total_DeltaCE": 4.193392551178618e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.0024909496500636766,
              "contribution_to_total_DeltaCE": 8.478735270974867e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.0014016281431492525,
              "contribution_to_total_DeltaCE": 4.7708848606421174e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            }
          }
        },
        "G2to3": {
          "candidate_count": 1031,
          "positive_count": 181,
          "negative_count": 850,
          "positive_anchored_query_count": 181,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.012000542268973903,
              "contribution_to_total_DeltaCE": -0.0002658707039563369,
              "DeltaMRR_positive_anchor_full_negative_population": 0.017495395948434623
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.015964049893930483,
              "contribution_to_total_DeltaCE": -0.00035368178271966497,
              "DeltaMRR_positive_anchor_full_negative_population": 0.019337016574585635
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -0.006199923804005173,
              "contribution_to_total_DeltaCE": -0.00013735863507670048,
              "DeltaMRR_positive_anchor_full_negative_population": 0.009208103130755065
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": -0.0016230714238296936,
              "contribution_to_total_DeltaCE": -3.595897021592776e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0009208103130755068
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.022220075465329062,
              "contribution_to_total_DeltaCE": 0.0004922833463287405,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0055248618784530384
            }
          }
        },
        "G4plus": {
          "candidate_count": 2050,
          "positive_count": 1273,
          "negative_count": 777,
          "positive_anchored_query_count": 1273,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.00743752807335584,
              "contribution_to_total_DeltaCE": -0.000327637367852404,
              "DeltaMRR_positive_anchor_full_negative_population": -0.00026184865147944484
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.012967097284936726,
              "contribution_to_total_DeltaCE": -0.0005712254906764718,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -0.010714381623090546,
              "contribution_to_total_DeltaCE": -0.00047198904777668086,
              "DeltaMRR_positive_anchor_full_negative_population": 0.00039277297721916735
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": -0.011054564149606145,
              "contribution_to_total_DeltaCE": -0.0004869747401300627,
              "DeltaMRR_positive_anchor_full_negative_population": 0.001178318931657502
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.01590324130199121,
              "contribution_to_total_DeltaCE": 0.0007005682626156519,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0010473946059177794
            }
          }
        },
        "MULT0": {
          "candidate_count": 41871,
          "positive_count": 712,
          "negative_count": 41159,
          "positive_anchored_query_count": 712,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.001861767748427176,
              "contribution_to_total_DeltaCE": 0.0016751348932953903,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0007490636704119848
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.001562305348785716,
              "contribution_to_total_DeltaCE": 0.0014056920934116966,
              "DeltaMRR_positive_anchor_full_negative_population": -6.632334581772791e-05
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0014135879651620221,
              "contribution_to_total_DeltaCE": 0.0012718828796909711,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0005149812734082397
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.00190320839691425,
              "contribution_to_total_DeltaCE": 0.0017124213251503472,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0005344881398252184
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -0.0012586811766939008,
              "contribution_to_total_DeltaCE": -0.0011325047178388844,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0049519067075246845
            }
          }
        },
        "MULT1to3": {
          "candidate_count": 2199,
          "positive_count": 154,
          "negative_count": 2045,
          "positive_anchored_query_count": 154,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.005494154246829036,
              "contribution_to_total_DeltaCE": -0.00025961933102924725,
              "DeltaMRR_positive_anchor_full_negative_population": 0.00432900432900433
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.007540324513190959,
              "contribution_to_total_DeltaCE": -0.00035630852682884043,
              "DeltaMRR_positive_anchor_full_negative_population": 0.006493506493506494
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0006431278479642978,
              "contribution_to_total_DeltaCE": 3.0390195497539346e-05,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0021645021645021645
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": -5.071980909828237e-05,
              "contribution_to_total_DeltaCE": -2.3967006233265203e-06,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0021645021645021645
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -3.3350607738264696e-07,
              "contribution_to_total_DeltaCE": -1.5759409149141323e-08,
              "DeltaMRR_positive_anchor_full_negative_population": 0.007575757575757576
            }
          }
        },
        "MULT4to15": {
          "candidate_count": 1198,
          "positive_count": 397,
          "negative_count": 801,
          "positive_anchored_query_count": 397,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.01140310528442273,
              "contribution_to_total_DeltaCE": -0.0002935559594881045,
              "DeltaMRR_positive_anchor_full_negative_population": 0.006717044500419816
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.01699126709529506,
              "contribution_to_total_DeltaCE": -0.0004374148611862533,
              "DeltaMRR_positive_anchor_full_negative_population": 0.007556675062972292
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -0.00998628488771454,
              "contribution_to_total_DeltaCE": -0.00025708202886973565,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0025188916876574307
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": -0.006058392523950788,
              "contribution_to_total_DeltaCE": -0.00015596429095094216,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.024357348851507792,
              "contribution_to_total_DeltaCE": 0.0006270436634886181,
              "DeltaMRR_positive_anchor_full_negative_population": -0.00041981528127623866
            }
          }
        },
        "MULT16plus": {
          "candidate_count": 1268,
          "positive_count": 953,
          "negative_count": 315,
          "positive_anchored_query_count": 953,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.008477633556303375,
              "contribution_to_total_DeltaCE": -0.00023099620400104609,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.013826664836403052,
              "contribution_to_total_DeltaCE": -0.00037674512232592126,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -0.013889691558118906,
              "contribution_to_total_DeltaCE": -0.0003784624569300063,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0015739769150052466
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": -0.010268211194842253,
              "contribution_to_total_DeltaCE": -0.000279785366061973,
              "DeltaMRR_positive_anchor_full_negative_population": 0.002098635886673662
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.022516838255790605,
              "contribution_to_total_DeltaCE": 0.0006135325534713446,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0013990905911157746
            }
          }
        },
        "degree0to3": {
          "candidate_count": 419,
          "positive_count": 9,
          "negative_count": 410,
          "positive_anchored_query_count": 9,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.0039533394743489275,
              "contribution_to_total_DeltaCE": -3.559500687107187e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.0029864087796058606,
              "contribution_to_total_DeltaCE": -2.6888973668876903e-05,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0015432098765432107
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -0.002509600997330811,
              "contribution_to_total_DeltaCE": -2.2595900332680286e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": -0.0011245723285712836,
              "contribution_to_total_DeltaCE": -1.0125404110180674e-05,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0015432098765432107
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -0.0003530409307934915,
              "contribution_to_total_DeltaCE": -3.1787035843749557e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            }
          }
        },
        "degree4to15": {
          "candidate_count": 6322,
          "positive_count": 111,
          "negative_count": 6211,
          "positive_anchored_query_count": 111,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.0001821658454610963,
              "contribution_to_total_DeltaCE": 2.4747560490911352e-05,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0015015015015015017
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 2.0744880979335882e-05,
              "contribution_to_total_DeltaCE": 2.8182297049888573e-06,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0007507507507507511
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -7.417117325492015e-05,
              "contribution_to_total_DeltaCE": -1.0076288407203138e-05,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0007507507507507511
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.0006885583185815018,
              "contribution_to_total_DeltaCE": 9.354189638284885e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0007507507507507506
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.0004794501555125796,
              "contribution_to_total_DeltaCE": 6.513417318098952e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.004804804804804805
            }
          }
        },
        "degree16plus": {
          "candidate_count": 39795,
          "positive_count": 2096,
          "negative_count": 37699,
          "positive_anchored_query_count": 2096,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.00105457141576161,
              "contribution_to_total_DeltaCE": 0.000901810845157153,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0014153944020356235
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.00030321700723409336,
              "contribution_to_total_DeltaCE": 0.0002592943270345699,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0019322519083969465
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0008178744719435845,
              "contribution_to_total_DeltaCE": 0.0006994007781286519,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0008985368956743002
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.0013925817314696701,
              "contribution_to_total_DeltaCE": 0.0011908584752414373,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0005804707379134861
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 5.3909339617697566e-05,
              "contribution_to_total_DeltaCE": 4.610027011531448e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.001268650242886884
            }
          }
        }
      },
      "ranking_rule": "subgroup positive anchors, original full negative population; no filtered-negative ranking",
      "calibration_warning": "H0 uses a constant HDP raw block; improvements there do not prove incremental structural information",
      "all_pairwise_subgroups": {
        "GM_vs_GMH": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.001861767748427176,
            "contribution_to_total": -0.0016751348932953903,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0007490636704119848
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.003477660838656143,
            "contribution_to_total": 0.00018002589307896356,
            "DeltaMRR_positive_anchor_full_negative_population": -0.000900900900900901
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.012462109799904926,
            "contribution_to_total": 0.0006041456014394342,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0024008086934546374
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.001861767748427176,
            "contribution_to_total": -0.0016751348932953903,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0007490636704119848
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.005601460252030679,
            "contribution_to_total": 0.00019066342270965695,
            "DeltaMRR_positive_anchor_full_negative_population": -0.01
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.012000542268973903,
            "contribution_to_total": 0.0002658707039563369,
            "DeltaMRR_positive_anchor_full_negative_population": -0.017495395948434623
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.00743752807335584,
            "contribution_to_total": 0.000327637367852404,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00026184865147944484
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.001861767748427176,
            "contribution_to_total": -0.0016751348932953903,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0007490636704119848
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.005494154246829036,
            "contribution_to_total": 0.00025961933102924725,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00432900432900433
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.01140310528442273,
            "contribution_to_total": 0.0002935559594881045,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006717044500419816
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.008477633556303375,
            "contribution_to_total": 0.00023099620400104609,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.0039533394743489275,
            "contribution_to_total": 3.559500687107187e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0001821658454610963,
            "contribution_to_total": -2.4747560490911352e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0015015015015015017
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.00105457141576161,
            "contribution_to_total": -0.000901810845157153,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0014153944020356235
          }
        },
        "GM_vs_GMS": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.001562305348785716,
            "contribution_to_total": -0.0014056920934116966,
            "DeltaMRR_positive_anchor_full_negative_population": 6.632334581772791e-05
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.007187850370854699,
            "contribution_to_total": 0.0003720889535711916,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002702702702702703
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.016468701708262635,
            "contribution_to_total": 0.0007983795567698234,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00265352539802881
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.001562305348785716,
            "contribution_to_total": -0.0014056920934116966,
            "DeltaMRR_positive_anchor_full_negative_population": 6.632334581772791e-05
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.007214291491456348,
            "contribution_to_total": 0.00024556123694487826,
            "DeltaMRR_positive_anchor_full_negative_population": -0.01
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.015964049893930483,
            "contribution_to_total": 0.00035368178271966497,
            "DeltaMRR_positive_anchor_full_negative_population": -0.019337016574585635
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.012967097284936726,
            "contribution_to_total": 0.0005712254906764718,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.001562305348785716,
            "contribution_to_total": -0.0014056920934116966,
            "DeltaMRR_positive_anchor_full_negative_population": 6.632334581772791e-05
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.007540324513190959,
            "contribution_to_total": 0.00035630852682884043,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.01699126709529506,
            "contribution_to_total": 0.0004374148611862533,
            "DeltaMRR_positive_anchor_full_negative_population": -0.007556675062972292
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.013826664836403052,
            "contribution_to_total": 0.00037674512232592126,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.0029864087796058606,
            "contribution_to_total": 2.6888973668876903e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0015432098765432107
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -2.0744880979335882e-05,
            "contribution_to_total": -2.8182297049888573e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0007507507507507511
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.00030321700723409336,
            "contribution_to_total": -0.0002592943270345699,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0019322519083969465
          }
        },
        "GM_vs_GMP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0014135879651620221,
            "contribution_to_total": -0.0012718828796909711,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0005149812734082397
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.0003016312552724092,
            "contribution_to_total": 1.5614356497147022e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0045045045045045045
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.01216082906008514,
            "contribution_to_total": 0.0005895399338050558,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002274450341167551
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0014135879651620221,
            "contribution_to_total": -0.0012718828796909711,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0005149812734082397
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.00012319679025356577,
            "contribution_to_total": -4.193392551178618e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.006199923804005173,
            "contribution_to_total": 0.00013735863507670048,
            "DeltaMRR_positive_anchor_full_negative_population": -0.009208103130755065
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.010714381623090546,
            "contribution_to_total": 0.00047198904777668086,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00039277297721916735
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0014135879651620221,
            "contribution_to_total": -0.0012718828796909711,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0005149812734082397
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.0006431278479642978,
            "contribution_to_total": -3.0390195497539346e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0021645021645021645
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.00998628488771454,
            "contribution_to_total": 0.00025708202886973565,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0025188916876574307
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.013889691558118906,
            "contribution_to_total": 0.0003784624569300063,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0015739769150052466
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.002509600997330811,
            "contribution_to_total": 2.2595900332680286e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 7.417117325492015e-05,
            "contribution_to_total": 1.0076288407203138e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0007507507507507511
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0008178744719435845,
            "contribution_to_total": -0.0006994007781286519,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0008985368956743002
          }
        },
        "GM_vs_GMG": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.00190320839691425,
            "contribution_to_total": -0.0017124213251503472,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0005344881398252184
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.0008964989712390396,
            "contribution_to_total": 4.6408501412129245e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0018018018018018016
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.008080635140622915,
            "contribution_to_total": 0.00039173785622411246,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001516300227445034
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.00190320839691425,
            "contribution_to_total": -0.0017124213251503472,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0005344881398252184
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.0024909496500636766,
            "contribution_to_total": -8.478735270974867e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.0016230714238296936,
            "contribution_to_total": 3.595897021592776e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0009208103130755068
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.011054564149606145,
            "contribution_to_total": 0.0004869747401300627,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001178318931657502
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.00190320839691425,
            "contribution_to_total": -0.0017124213251503472,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0005344881398252184
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 5.071980909828237e-05,
            "contribution_to_total": 2.3967006233265203e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0021645021645021645
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.006058392523950788,
            "contribution_to_total": 0.00015596429095094216,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.010268211194842253,
            "contribution_to_total": 0.000279785366061973,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002098635886673662
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.0011245723285712836,
            "contribution_to_total": 1.0125404110180674e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0015432098765432107
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0006885583185815018,
            "contribution_to_total": -9.354189638284885e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0007507507507507506
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0013925817314696701,
            "contribution_to_total": -0.0011908584752414373,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0005804707379134861
          }
        },
        "GM_vs_GDUP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0012586811766939008,
            "contribution_to_total": 0.0011325047178388844,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0049519067075246845
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.0020354677731740938,
            "contribution_to_total": -0.00010536878686557487,
            "DeltaMRR_positive_anchor_full_negative_population": -0.011711711711711714
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.02341634733466678,
            "contribution_to_total": -0.0011351916706852385,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0018953752843062926
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0012586811766939008,
            "contribution_to_total": 0.0011325047178388844,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0049519067075246845
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.0014016281431492525,
            "contribution_to_total": -4.7708848606421174e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.022220075465329062,
            "contribution_to_total": -0.0004922833463287405,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0055248618784530384
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.01590324130199121,
            "contribution_to_total": -0.0007005682626156519,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0010473946059177794
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0012586811766939008,
            "contribution_to_total": 0.0011325047178388844,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0049519067075246845
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 3.3350607738264696e-07,
            "contribution_to_total": 1.5759409149141323e-08,
            "DeltaMRR_positive_anchor_full_negative_population": -0.007575757575757576
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.024357348851507792,
            "contribution_to_total": -0.0006270436634886181,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00041981528127623866
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.022516838255790605,
            "contribution_to_total": -0.0006135325534713446,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0013990905911157746
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.0003530409307934915,
            "contribution_to_total": 3.1787035843749557e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0004794501555125796,
            "contribution_to_total": -6.513417318098952e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004804804804804805
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -5.3909339617697566e-05,
            "contribution_to_total": -4.610027011531448e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001268650242886884
          }
        },
        "GMH_vs_GM": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.001861767748427176,
            "contribution_to_total": 0.0016751348932953903,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0007490636704119848
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.003477660838656143,
            "contribution_to_total": -0.00018002589307896356,
            "DeltaMRR_positive_anchor_full_negative_population": 0.000900900900900901
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.012462109799904926,
            "contribution_to_total": -0.0006041456014394342,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0024008086934546374
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.001861767748427176,
            "contribution_to_total": 0.0016751348932953903,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0007490636704119848
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.005601460252030679,
            "contribution_to_total": -0.00019066342270965695,
            "DeltaMRR_positive_anchor_full_negative_population": 0.01
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.012000542268973903,
            "contribution_to_total": -0.0002658707039563369,
            "DeltaMRR_positive_anchor_full_negative_population": 0.017495395948434623
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.00743752807335584,
            "contribution_to_total": -0.000327637367852404,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00026184865147944484
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.001861767748427176,
            "contribution_to_total": 0.0016751348932953903,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0007490636704119848
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.005494154246829036,
            "contribution_to_total": -0.00025961933102924725,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00432900432900433
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.01140310528442273,
            "contribution_to_total": -0.0002935559594881045,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006717044500419816
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.008477633556303375,
            "contribution_to_total": -0.00023099620400104609,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.0039533394743489275,
            "contribution_to_total": -3.559500687107187e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0001821658454610963,
            "contribution_to_total": 2.4747560490911352e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0015015015015015017
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.00105457141576161,
            "contribution_to_total": 0.000901810845157153,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0014153944020356235
          }
        },
        "GMH_vs_GMS": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0002994623996414597,
            "contribution_to_total": 0.00026944279988369346,
            "DeltaMRR_positive_anchor_full_negative_population": -0.000682740324594257
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.0037101895321985565,
            "contribution_to_total": 0.000192063060492228,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0018018018018018016
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.004006591908357708,
            "contribution_to_total": 0.00019423395533038916,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0002527167045741723
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0002994623996414597,
            "contribution_to_total": 0.00026944279988369346,
            "DeltaMRR_positive_anchor_full_negative_population": -0.000682740324594257
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.0016128312394256686,
            "contribution_to_total": 5.489781423522132e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.003963507624956581,
            "contribution_to_total": 8.781107876332808e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0018416206261510127
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.005529569211580887,
            "contribution_to_total": 0.0002435881228240678,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00026184865147944484
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0002994623996414597,
            "contribution_to_total": 0.00026944279988369346,
            "DeltaMRR_positive_anchor_full_negative_population": -0.000682740324594257
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.002046170266361923,
            "contribution_to_total": 9.668919579959318e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0021645021645021645
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.005588161810872332,
            "contribution_to_total": 0.00014385890169814884,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0008396305625524769
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.005349031280099678,
            "contribution_to_total": 0.00014574891832487517,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.0009669306947430672,
            "contribution_to_total": -8.70603320219497e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0015432098765432107
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.00016142096448176042,
            "contribution_to_total": 2.1929330785922497e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0007507507507507506
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0007513544085275167,
            "contribution_to_total": 0.0006425165181225831,
            "DeltaMRR_positive_anchor_full_negative_population": -0.000516857506361323
          }
        },
        "GMH_vs_GMP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.00044817978326515374,
            "contribution_to_total": 0.00040325201360441923,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00023408239700374494
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.003176029583383734,
            "contribution_to_total": -0.00016441153658181654,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005405405405405406
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.0003012807398197893,
            "contribution_to_total": -1.4605667634378646e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0001263583522870862
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.00044817978326515374,
            "contribution_to_total": 0.00040325201360441923,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00023408239700374494
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.005724657042284245,
            "contribution_to_total": -0.00019485681526083557,
            "DeltaMRR_positive_anchor_full_negative_population": 0.01
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.0058006184649687315,
            "contribution_to_total": -0.00012851206887963646,
            "DeltaMRR_positive_anchor_full_negative_population": 0.008287292817679558
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.003276853549734706,
            "contribution_to_total": 0.00014435167992427682,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0006546216286986121
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.00044817978326515374,
            "contribution_to_total": 0.00040325201360441923,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00023408239700374494
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.006137282094793335,
            "contribution_to_total": -0.0002900095265267866,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006493506493506494
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.00141682039670819,
            "contribution_to_total": -3.6473930618368826e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0041981528127623844
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.005412058001815531,
            "contribution_to_total": 0.00014746625292896023,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0015739769150052466
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.0014437384770181166,
            "contribution_to_total": -1.2999106538391587e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0002563370187160164,
            "contribution_to_total": 3.482384889811449e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0007507507507507506
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.00023669694381802563,
            "contribution_to_total": 0.00020241006702850117,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0005168575063613232
          }
        },
        "GMH_vs_GMG": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -4.144064848707388e-05,
            "contribution_to_total": -3.728643185495682e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00021457553058676642
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.002581161867417103,
            "contribution_to_total": -0.00013361739166683432,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002702702702702703
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.00438147465928201,
            "contribution_to_total": -0.00021240774521532178,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0008845084660096033
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -4.144064848707388e-05,
            "contribution_to_total": -3.728643185495682e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00021457553058676642
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.008092409902094356,
            "contribution_to_total": -0.0002754507754194056,
            "DeltaMRR_positive_anchor_full_negative_population": 0.01
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.01037747084514421,
            "contribution_to_total": -0.00022991173374040916,
            "DeltaMRR_positive_anchor_full_negative_population": 0.016574585635359115
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.0036170360762503044,
            "contribution_to_total": 0.00015933737227765866,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0014401675831369467
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -4.144064848707388e-05,
            "contribution_to_total": -3.728643185495682e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00021457553058676642
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.005443434437730753,
            "contribution_to_total": -0.00025722263040592075,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006493506493506494
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.005344712760471944,
            "contribution_to_total": -0.00013759166853716237,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006717044500419816
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.001790577638538879,
            "contribution_to_total": 4.8789162060926985e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002098635886673662
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.002828767145777644,
            "contribution_to_total": -2.54696027608912e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0015432098765432107
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0005063924731204055,
            "contribution_to_total": -6.87943358919375e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0022522522522522522
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0003380103157080601,
            "contribution_to_total": -0.00028904763008428424,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0008349236641221376
          }
        },
        "GMH_vs_GDUP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0031204489251210775,
            "contribution_to_total": 0.002807639611134275,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0057009703779366695
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.005513128611830237,
            "contribution_to_total": -0.0002853946799445384,
            "DeltaMRR_positive_anchor_full_negative_population": -0.010810810810810811
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.03587845713457171,
            "contribution_to_total": -0.001739337272124673,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00429618397776093
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0031204489251210775,
            "contribution_to_total": 0.002807639611134275,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0057009703779366695
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.007003088395179931,
            "contribution_to_total": -0.0002383722713160781,
            "DeltaMRR_positive_anchor_full_negative_population": 0.01
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.03422061773430297,
            "contribution_to_total": -0.0007581540502850774,
            "DeltaMRR_positive_anchor_full_negative_population": 0.011970534069981586
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.02334076937534705,
            "contribution_to_total": -0.001028205630468056,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0007855459544383347
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0031204489251210775,
            "contribution_to_total": 0.002807639611134275,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0057009703779366695
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.005493820740751654,
            "contribution_to_total": -0.00025960357162009817,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003246753246753247
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.03576045413593052,
            "contribution_to_total": -0.0009205996229767226,
            "DeltaMRR_positive_anchor_full_negative_population": 0.007136859781696054
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.030994471812093978,
            "contribution_to_total": -0.0008445287574723906,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0013990905911157746
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.0036002985435554364,
            "contribution_to_total": -3.241630328669692e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0002972843100514834,
            "contribution_to_total": -4.038661269007817e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006306306306306306
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0010006620761439126,
            "contribution_to_total": 0.0008557105750418386,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0001467441591487394
          }
        },
        "GMS_vs_GM": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.001562305348785716,
            "contribution_to_total": 0.0014056920934116966,
            "DeltaMRR_positive_anchor_full_negative_population": -6.632334581772791e-05
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.007187850370854699,
            "contribution_to_total": -0.0003720889535711916,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002702702702702703
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.016468701708262635,
            "contribution_to_total": -0.0007983795567698234,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00265352539802881
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.001562305348785716,
            "contribution_to_total": 0.0014056920934116966,
            "DeltaMRR_positive_anchor_full_negative_population": -6.632334581772791e-05
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.007214291491456348,
            "contribution_to_total": -0.00024556123694487826,
            "DeltaMRR_positive_anchor_full_negative_population": 0.01
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.015964049893930483,
            "contribution_to_total": -0.00035368178271966497,
            "DeltaMRR_positive_anchor_full_negative_population": 0.019337016574585635
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.012967097284936726,
            "contribution_to_total": -0.0005712254906764718,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.001562305348785716,
            "contribution_to_total": 0.0014056920934116966,
            "DeltaMRR_positive_anchor_full_negative_population": -6.632334581772791e-05
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.007540324513190959,
            "contribution_to_total": -0.00035630852682884043,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006493506493506494
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.01699126709529506,
            "contribution_to_total": -0.0004374148611862533,
            "DeltaMRR_positive_anchor_full_negative_population": 0.007556675062972292
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.013826664836403052,
            "contribution_to_total": -0.00037674512232592126,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.0029864087796058606,
            "contribution_to_total": -2.6888973668876903e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0015432098765432107
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 2.0744880979335882e-05,
            "contribution_to_total": 2.8182297049888573e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0007507507507507511
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.00030321700723409336,
            "contribution_to_total": 0.0002592943270345699,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0019322519083969465
          }
        },
        "GMS_vs_GMH": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0002994623996414597,
            "contribution_to_total": -0.00026944279988369346,
            "DeltaMRR_positive_anchor_full_negative_population": 0.000682740324594257
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.0037101895321985565,
            "contribution_to_total": -0.000192063060492228,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0018018018018018016
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.004006591908357708,
            "contribution_to_total": -0.00019423395533038916,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0002527167045741723
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0002994623996414597,
            "contribution_to_total": -0.00026944279988369346,
            "DeltaMRR_positive_anchor_full_negative_population": 0.000682740324594257
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.0016128312394256686,
            "contribution_to_total": -5.489781423522132e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.003963507624956581,
            "contribution_to_total": -8.781107876332808e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0018416206261510127
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.005529569211580887,
            "contribution_to_total": -0.0002435881228240678,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00026184865147944484
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0002994623996414597,
            "contribution_to_total": -0.00026944279988369346,
            "DeltaMRR_positive_anchor_full_negative_population": 0.000682740324594257
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.002046170266361923,
            "contribution_to_total": -9.668919579959318e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0021645021645021645
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.005588161810872332,
            "contribution_to_total": -0.00014385890169814884,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0008396305625524769
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.005349031280099678,
            "contribution_to_total": -0.00014574891832487517,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.0009669306947430672,
            "contribution_to_total": 8.70603320219497e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0015432098765432107
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.00016142096448176042,
            "contribution_to_total": -2.1929330785922497e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0007507507507507506
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0007513544085275167,
            "contribution_to_total": -0.0006425165181225831,
            "DeltaMRR_positive_anchor_full_negative_population": 0.000516857506361323
          }
        },
        "GMS_vs_GMP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.00014871738362369412,
            "contribution_to_total": 0.00013380921372072583,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00044865792759051203
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.006886219115582291,
            "contribution_to_total": -0.00035647459707404463,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0072072072072072065
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.004307872648177498,
            "contribution_to_total": -0.00020883962296476782,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0003790750568612585
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.00014871738362369412,
            "contribution_to_total": 0.00013380921372072583,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00044865792759051203
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.007337488281709915,
            "contribution_to_total": -0.00024975462949605693,
            "DeltaMRR_positive_anchor_full_negative_population": 0.01
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.009764126089925312,
            "contribution_to_total": -0.00021632314764296451,
            "DeltaMRR_positive_anchor_full_negative_population": 0.010128913443830571
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.0022527156618461818,
            "contribution_to_total": -9.923644289979098e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00039277297721916735
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.00014871738362369412,
            "contribution_to_total": 0.00013380921372072583,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00044865792759051203
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.008183452361155258,
            "contribution_to_total": -0.00038669872232637985,
            "DeltaMRR_positive_anchor_full_negative_population": 0.008658008658008658
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.00700498220758052,
            "contribution_to_total": -0.0001803328323165176,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005037783375314861
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 6.302672171585342e-05,
            "contribution_to_total": 1.7173346040850555e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0015739769150052466
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.00047680778227504963,
            "contribution_to_total": -4.293073336196618e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0015432098765432107
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 9.491605423425601e-05,
            "contribution_to_total": 1.289451811219199e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.000514657464709491,
            "contribution_to_total": -0.0004401064510940819,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0010337150127226464
          }
        },
        "GMS_vs_GMG": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.00034090304812853364,
            "contribution_to_total": -0.00030672923173865035,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0004681647940074907
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.006291351399615661,
            "contribution_to_total": -0.0003256804521590624,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0045045045045045045
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.008388066567639718,
            "contribution_to_total": -0.0004066417005457109,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0011372251705837756
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.00034090304812853364,
            "contribution_to_total": -0.00030672923173865035,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0004681647940074907
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.009705241141520023,
            "contribution_to_total": -0.0003303485896546269,
            "DeltaMRR_positive_anchor_full_negative_population": 0.01
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.01434097847010079,
            "contribution_to_total": -0.00031772281250373724,
            "DeltaMRR_positive_anchor_full_negative_population": 0.018416206261510127
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.0019125331353305824,
            "contribution_to_total": -8.425075054640911e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001178318931657502
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.00034090304812853364,
            "contribution_to_total": -0.00030672923173865035,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0004681647940074907
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.007489604704092676,
            "contribution_to_total": -0.0003539118262055139,
            "DeltaMRR_positive_anchor_full_negative_population": 0.008658008658008658
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.010932874571344276,
            "contribution_to_total": -0.0002814505702353112,
            "DeltaMRR_positive_anchor_full_negative_population": 0.007556675062972292
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.0035584536415607993,
            "contribution_to_total": -9.69597562639482e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002098635886673662
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.001861836451034577,
            "contribution_to_total": -1.676356955869623e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0006678134376021659,
            "contribution_to_total": -9.072366667786e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0015015015015015017
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0010893647242355767,
            "contribution_to_total": -0.0009315641482068673,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0013517811704834607
          }
        },
        "GMS_vs_GDUP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0028209865254796174,
            "contribution_to_total": 0.0025381968112505814,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005018230053342413
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.009223318144028794,
            "contribution_to_total": -0.00047745774043676646,
            "DeltaMRR_positive_anchor_full_negative_population": -0.009009009009009009
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.03988504904292942,
            "contribution_to_total": -0.0019335712274550622,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004548900682335102
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0028209865254796174,
            "contribution_to_total": 0.0025381968112505814,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005018230053342413
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.0086159196346056,
            "contribution_to_total": -0.00029327008555129943,
            "DeltaMRR_positive_anchor_full_negative_population": 0.01
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.03818412535925955,
            "contribution_to_total": -0.0008459651290484055,
            "DeltaMRR_positive_anchor_full_negative_population": 0.013812154696132596
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.028870338586927936,
            "contribution_to_total": -0.0012717937532921236,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0010473946059177794
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0028209865254796174,
            "contribution_to_total": 0.0025381968112505814,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005018230053342413
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.007539991007113576,
            "contribution_to_total": -0.0003562927674196913,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0010822510822510827
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.04134861594680285,
            "contribution_to_total": -0.0010644585246748714,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00797649034424853
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.03634350309219366,
            "contribution_to_total": -0.000990277675797266,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0013990905911157746
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.002633367848812369,
            "contribution_to_total": -2.371027008450195e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0015432098765432107
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0004587052745332438,
            "contribution_to_total": -6.231594347600067e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005555555555555556
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.00024930766761639575,
            "contribution_to_total": 0.0002131940569192554,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0006636016655100625
          }
        },
        "GMP_vs_GM": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0014135879651620221,
            "contribution_to_total": 0.0012718828796909711,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0005149812734082397
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.0003016312552724092,
            "contribution_to_total": -1.5614356497147022e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0045045045045045045
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.01216082906008514,
            "contribution_to_total": -0.0005895399338050558,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002274450341167551
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0014135879651620221,
            "contribution_to_total": 0.0012718828796909711,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0005149812734082397
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.00012319679025356577,
            "contribution_to_total": 4.193392551178618e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.006199923804005173,
            "contribution_to_total": -0.00013735863507670048,
            "DeltaMRR_positive_anchor_full_negative_population": 0.009208103130755065
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.010714381623090546,
            "contribution_to_total": -0.00047198904777668086,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00039277297721916735
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0014135879651620221,
            "contribution_to_total": 0.0012718828796909711,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0005149812734082397
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.0006431278479642978,
            "contribution_to_total": 3.0390195497539346e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0021645021645021645
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.00998628488771454,
            "contribution_to_total": -0.00025708202886973565,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0025188916876574307
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.013889691558118906,
            "contribution_to_total": -0.0003784624569300063,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0015739769150052466
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.002509600997330811,
            "contribution_to_total": -2.2595900332680286e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -7.417117325492015e-05,
            "contribution_to_total": -1.0076288407203138e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0007507507507507511
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0008178744719435845,
            "contribution_to_total": 0.0006994007781286519,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0008985368956743002
          }
        },
        "GMP_vs_GMH": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.00044817978326515374,
            "contribution_to_total": -0.00040325201360441923,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00023408239700374494
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.003176029583383734,
            "contribution_to_total": 0.00016441153658181654,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005405405405405406
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.0003012807398197893,
            "contribution_to_total": 1.4605667634378646e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0001263583522870862
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.00044817978326515374,
            "contribution_to_total": -0.00040325201360441923,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00023408239700374494
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.005724657042284245,
            "contribution_to_total": 0.00019485681526083557,
            "DeltaMRR_positive_anchor_full_negative_population": -0.01
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.0058006184649687315,
            "contribution_to_total": 0.00012851206887963646,
            "DeltaMRR_positive_anchor_full_negative_population": -0.008287292817679558
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.003276853549734706,
            "contribution_to_total": -0.00014435167992427682,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0006546216286986121
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.00044817978326515374,
            "contribution_to_total": -0.00040325201360441923,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00023408239700374494
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.006137282094793335,
            "contribution_to_total": 0.0002900095265267866,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.00141682039670819,
            "contribution_to_total": 3.6473930618368826e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0041981528127623844
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.005412058001815531,
            "contribution_to_total": -0.00014746625292896023,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0015739769150052466
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.0014437384770181166,
            "contribution_to_total": 1.2999106538391587e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0002563370187160164,
            "contribution_to_total": -3.482384889811449e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0007507507507507506
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.00023669694381802563,
            "contribution_to_total": -0.00020241006702850117,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0005168575063613232
          }
        },
        "GMP_vs_GMS": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.00014871738362369412,
            "contribution_to_total": -0.00013380921372072583,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00044865792759051203
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.006886219115582291,
            "contribution_to_total": 0.00035647459707404463,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0072072072072072065
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.004307872648177498,
            "contribution_to_total": 0.00020883962296476782,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0003790750568612585
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.00014871738362369412,
            "contribution_to_total": -0.00013380921372072583,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00044865792759051203
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.007337488281709915,
            "contribution_to_total": 0.00024975462949605693,
            "DeltaMRR_positive_anchor_full_negative_population": -0.01
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.009764126089925312,
            "contribution_to_total": 0.00021632314764296451,
            "DeltaMRR_positive_anchor_full_negative_population": -0.010128913443830571
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.0022527156618461818,
            "contribution_to_total": 9.923644289979098e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00039277297721916735
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.00014871738362369412,
            "contribution_to_total": -0.00013380921372072583,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00044865792759051203
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.008183452361155258,
            "contribution_to_total": 0.00038669872232637985,
            "DeltaMRR_positive_anchor_full_negative_population": -0.008658008658008658
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.00700498220758052,
            "contribution_to_total": 0.0001803328323165176,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005037783375314861
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -6.302672171585342e-05,
            "contribution_to_total": -1.7173346040850555e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0015739769150052466
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.00047680778227504963,
            "contribution_to_total": 4.293073336196618e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0015432098765432107
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -9.491605423425601e-05,
            "contribution_to_total": -1.289451811219199e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.000514657464709491,
            "contribution_to_total": 0.0004401064510940819,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0010337150127226464
          }
        },
        "GMP_vs_GMG": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0004896204317522278,
            "contribution_to_total": -0.0004405384454593761,
            "DeltaMRR_positive_anchor_full_negative_population": 1.9506866416978394e-05
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.0005948677159666304,
            "contribution_to_total": 3.079414491498222e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002702702702702703
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.004080193919462221,
            "contribution_to_total": -0.00019780207758094315,
            "DeltaMRR_positive_anchor_full_negative_population": 0.000758150113722517
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0004896204317522278,
            "contribution_to_total": -0.0004405384454593761,
            "DeltaMRR_positive_anchor_full_negative_population": 1.9506866416978394e-05
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.0023677528598101114,
            "contribution_to_total": -8.059396015857006e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.004576852380175479,
            "contribution_to_total": -0.0001013996648607727,
            "DeltaMRR_positive_anchor_full_negative_population": 0.008287292817679558
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.0003401825265155991,
            "contribution_to_total": 1.4985692353381857e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0007855459544383347
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0004896204317522278,
            "contribution_to_total": -0.0004405384454593761,
            "DeltaMRR_positive_anchor_full_negative_population": 1.9506866416978394e-05
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.0006938476570625804,
            "contribution_to_total": 3.2786896120865874e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.003927892363763752,
            "contribution_to_total": -0.00010111773791879353,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0025188916876574307
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.0036214803632766517,
            "contribution_to_total": -9.867709086803322e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0005246589716684155
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.0013850286687595273,
            "contribution_to_total": -1.2470496222499612e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0015432098765432107
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0007627294918364219,
            "contribution_to_total": -0.000103618184790052,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0015015015015015017
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0005747072595260858,
            "contribution_to_total": -0.0004914576971127854,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0003180661577608142
          }
        },
        "GMP_vs_GDUP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.002672269141855924,
            "contribution_to_total": 0.0024043875975298563,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005466887980932925
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.0023370990284465026,
            "contribution_to_total": -0.00012098314336272187,
            "DeltaMRR_positive_anchor_full_negative_population": -0.016216216216216217
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.03557717639475193,
            "contribution_to_total": -0.0017247316044902944,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004169825625473844
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.002672269141855924,
            "contribution_to_total": 0.0024043875975298563,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005466887980932925
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.0012784313528956869,
            "contribution_to_total": -4.351545605524256e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.028419999269334237,
            "contribution_to_total": -0.0006296419814054409,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0036832412523020264
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.02661762292508176,
            "contribution_to_total": -0.001172557310392333,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0014401675831369467
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.002672269141855924,
            "contribution_to_total": 0.0024043875975298563,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005466887980932925
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.0006434613540416805,
            "contribution_to_total": 3.040595490668849e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00974025974025974
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.03434363373922233,
            "contribution_to_total": -0.0008841256923583537,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0029387069689336695
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.03640652981390951,
            "contribution_to_total": -0.0009919950104013509,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002973067506121021
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.002156560066537319,
            "contribution_to_total": -1.9417196748305328e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0005536213287674998,
            "contribution_to_total": -7.521046158819267e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005555555555555556
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0007639651323258868,
            "contribution_to_total": 0.0006533005080133373,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0003701133472125839
          }
        },
        "GMG_vs_GM": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.00190320839691425,
            "contribution_to_total": 0.0017124213251503472,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0005344881398252184
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.0008964989712390396,
            "contribution_to_total": -4.6408501412129245e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0018018018018018016
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.008080635140622915,
            "contribution_to_total": -0.00039173785622411246,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001516300227445034
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.00190320839691425,
            "contribution_to_total": 0.0017124213251503472,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0005344881398252184
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.0024909496500636766,
            "contribution_to_total": 8.478735270974867e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.0016230714238296936,
            "contribution_to_total": -3.595897021592776e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0009208103130755068
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.011054564149606145,
            "contribution_to_total": -0.0004869747401300627,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001178318931657502
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.00190320839691425,
            "contribution_to_total": 0.0017124213251503472,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0005344881398252184
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -5.071980909828237e-05,
            "contribution_to_total": -2.3967006233265203e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0021645021645021645
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.006058392523950788,
            "contribution_to_total": -0.00015596429095094216,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.010268211194842253,
            "contribution_to_total": -0.000279785366061973,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002098635886673662
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.0011245723285712836,
            "contribution_to_total": -1.0125404110180674e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0015432098765432107
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0006885583185815018,
            "contribution_to_total": 9.354189638284885e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0007507507507507506
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0013925817314696701,
            "contribution_to_total": 0.0011908584752414373,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0005804707379134861
          }
        },
        "GMG_vs_GMH": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 4.144064848707388e-05,
            "contribution_to_total": 3.728643185495682e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00021457553058676642
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.002581161867417103,
            "contribution_to_total": 0.00013361739166683432,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002702702702702703
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.00438147465928201,
            "contribution_to_total": 0.00021240774521532178,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0008845084660096033
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 4.144064848707388e-05,
            "contribution_to_total": 3.728643185495682e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00021457553058676642
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.008092409902094356,
            "contribution_to_total": 0.0002754507754194056,
            "DeltaMRR_positive_anchor_full_negative_population": -0.01
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.01037747084514421,
            "contribution_to_total": 0.00022991173374040916,
            "DeltaMRR_positive_anchor_full_negative_population": -0.016574585635359115
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.0036170360762503044,
            "contribution_to_total": -0.00015933737227765866,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0014401675831369467
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 4.144064848707388e-05,
            "contribution_to_total": 3.728643185495682e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00021457553058676642
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.005443434437730753,
            "contribution_to_total": 0.00025722263040592075,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.005344712760471944,
            "contribution_to_total": 0.00013759166853716237,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006717044500419816
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.001790577638538879,
            "contribution_to_total": -4.8789162060926985e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002098635886673662
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.002828767145777644,
            "contribution_to_total": 2.54696027608912e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0015432098765432107
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0005063924731204055,
            "contribution_to_total": 6.87943358919375e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0022522522522522522
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0003380103157080601,
            "contribution_to_total": 0.00028904763008428424,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0008349236641221376
          }
        },
        "GMG_vs_GMS": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.00034090304812853364,
            "contribution_to_total": 0.00030672923173865035,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0004681647940074907
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.006291351399615661,
            "contribution_to_total": 0.0003256804521590624,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0045045045045045045
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.008388066567639718,
            "contribution_to_total": 0.0004066417005457109,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0011372251705837756
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.00034090304812853364,
            "contribution_to_total": 0.00030672923173865035,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0004681647940074907
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.009705241141520023,
            "contribution_to_total": 0.0003303485896546269,
            "DeltaMRR_positive_anchor_full_negative_population": -0.01
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.01434097847010079,
            "contribution_to_total": 0.00031772281250373724,
            "DeltaMRR_positive_anchor_full_negative_population": -0.018416206261510127
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.0019125331353305824,
            "contribution_to_total": 8.425075054640911e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001178318931657502
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.00034090304812853364,
            "contribution_to_total": 0.00030672923173865035,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0004681647940074907
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.007489604704092676,
            "contribution_to_total": 0.0003539118262055139,
            "DeltaMRR_positive_anchor_full_negative_population": -0.008658008658008658
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.010932874571344276,
            "contribution_to_total": 0.0002814505702353112,
            "DeltaMRR_positive_anchor_full_negative_population": -0.007556675062972292
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.0035584536415607993,
            "contribution_to_total": 9.69597562639482e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002098635886673662
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.001861836451034577,
            "contribution_to_total": 1.676356955869623e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0006678134376021659,
            "contribution_to_total": 9.072366667786e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0015015015015015017
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0010893647242355767,
            "contribution_to_total": 0.0009315641482068673,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0013517811704834607
          }
        },
        "GMG_vs_GMP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0004896204317522278,
            "contribution_to_total": 0.0004405384454593761,
            "DeltaMRR_positive_anchor_full_negative_population": -1.9506866416978394e-05
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.0005948677159666304,
            "contribution_to_total": -3.079414491498222e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002702702702702703
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.004080193919462221,
            "contribution_to_total": 0.00019780207758094315,
            "DeltaMRR_positive_anchor_full_negative_population": -0.000758150113722517
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0004896204317522278,
            "contribution_to_total": 0.0004405384454593761,
            "DeltaMRR_positive_anchor_full_negative_population": -1.9506866416978394e-05
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.0023677528598101114,
            "contribution_to_total": 8.059396015857006e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.004576852380175479,
            "contribution_to_total": 0.0001013996648607727,
            "DeltaMRR_positive_anchor_full_negative_population": -0.008287292817679558
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.0003401825265155991,
            "contribution_to_total": -1.4985692353381857e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0007855459544383347
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0004896204317522278,
            "contribution_to_total": 0.0004405384454593761,
            "DeltaMRR_positive_anchor_full_negative_population": -1.9506866416978394e-05
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.0006938476570625804,
            "contribution_to_total": -3.2786896120865874e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.003927892363763752,
            "contribution_to_total": 0.00010111773791879353,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0025188916876574307
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.0036214803632766517,
            "contribution_to_total": 9.867709086803322e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0005246589716684155
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.0013850286687595273,
            "contribution_to_total": 1.2470496222499612e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0015432098765432107
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0007627294918364219,
            "contribution_to_total": 0.000103618184790052,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0015015015015015017
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0005747072595260858,
            "contribution_to_total": 0.0004914576971127854,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0003180661577608142
          }
        },
        "GMG_vs_GDUP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.003161889573608151,
            "contribution_to_total": 0.0028449260429892318,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005486394847349903
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.0029319667444131334,
            "contribution_to_total": -0.0001517772882777041,
            "DeltaMRR_positive_anchor_full_negative_population": -0.013513513513513514
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.031496982475289696,
            "contribution_to_total": -0.001526929526909351,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003411675511751327
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.003161889573608151,
            "contribution_to_total": 0.0028449260429892318,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005486394847349903
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.0010893215069144248,
            "contribution_to_total": 3.707850410332751e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.02384314688915876,
            "contribution_to_total": -0.0005282423165446682,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004604051565377532
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.026957805451597355,
            "contribution_to_total": -0.0011875430027457148,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0022257135375752814
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.003161889573608151,
            "contribution_to_total": 0.0028449260429892318,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005486394847349903
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -5.038630302089973e-05,
            "contribution_to_total": -2.380941214177379e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00974025974025974
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.030415741375458577,
            "contribution_to_total": -0.0007830079544395602,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00041981528127623866
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.03278504945063286,
            "contribution_to_total": -0.0008933179195333176,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0034977264777894365
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.0007715313977777918,
            "contribution_to_total": -6.9467005258057155e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0015432098765432107
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.00020910816306892217,
            "contribution_to_total": 2.8407723201859334e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004054054054054054
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0013386723918519727,
            "contribution_to_total": 0.001144758205126123,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0006881795049733981
          }
        },
        "GDUP_vs_GM": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0012586811766939008,
            "contribution_to_total": -0.0011325047178388844,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0049519067075246845
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.0020354677731740938,
            "contribution_to_total": 0.00010536878686557487,
            "DeltaMRR_positive_anchor_full_negative_population": 0.011711711711711714
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.02341634733466678,
            "contribution_to_total": 0.0011351916706852385,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0018953752843062926
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0012586811766939008,
            "contribution_to_total": -0.0011325047178388844,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0049519067075246845
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.0014016281431492525,
            "contribution_to_total": 4.7708848606421174e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.022220075465329062,
            "contribution_to_total": 0.0004922833463287405,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0055248618784530384
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.01590324130199121,
            "contribution_to_total": 0.0007005682626156519,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0010473946059177794
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0012586811766939008,
            "contribution_to_total": -0.0011325047178388844,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0049519067075246845
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -3.3350607738264696e-07,
            "contribution_to_total": -1.5759409149141323e-08,
            "DeltaMRR_positive_anchor_full_negative_population": 0.007575757575757576
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.024357348851507792,
            "contribution_to_total": 0.0006270436634886181,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00041981528127623866
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.022516838255790605,
            "contribution_to_total": 0.0006135325534713446,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0013990905911157746
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.0003530409307934915,
            "contribution_to_total": -3.1787035843749557e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0004794501555125796,
            "contribution_to_total": 6.513417318098952e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004804804804804805
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 5.3909339617697566e-05,
            "contribution_to_total": 4.610027011531448e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001268650242886884
          }
        },
        "GDUP_vs_GMH": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0031204489251210775,
            "contribution_to_total": -0.002807639611134275,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0057009703779366695
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.005513128611830237,
            "contribution_to_total": 0.0002853946799445384,
            "DeltaMRR_positive_anchor_full_negative_population": 0.010810810810810811
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.03587845713457171,
            "contribution_to_total": 0.001739337272124673,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00429618397776093
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0031204489251210775,
            "contribution_to_total": -0.002807639611134275,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0057009703779366695
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.007003088395179931,
            "contribution_to_total": 0.0002383722713160781,
            "DeltaMRR_positive_anchor_full_negative_population": -0.01
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.03422061773430297,
            "contribution_to_total": 0.0007581540502850774,
            "DeltaMRR_positive_anchor_full_negative_population": -0.011970534069981586
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.02334076937534705,
            "contribution_to_total": 0.001028205630468056,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0007855459544383347
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0031204489251210775,
            "contribution_to_total": -0.002807639611134275,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0057009703779366695
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.005493820740751654,
            "contribution_to_total": 0.00025960357162009817,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003246753246753247
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.03576045413593052,
            "contribution_to_total": 0.0009205996229767226,
            "DeltaMRR_positive_anchor_full_negative_population": -0.007136859781696054
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.030994471812093978,
            "contribution_to_total": 0.0008445287574723906,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0013990905911157746
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.0036002985435554364,
            "contribution_to_total": 3.241630328669692e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0002972843100514834,
            "contribution_to_total": 4.038661269007817e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006306306306306306
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0010006620761439126,
            "contribution_to_total": -0.0008557105750418386,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0001467441591487394
          }
        },
        "GDUP_vs_GMS": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0028209865254796174,
            "contribution_to_total": -0.0025381968112505814,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005018230053342413
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.009223318144028794,
            "contribution_to_total": 0.00047745774043676646,
            "DeltaMRR_positive_anchor_full_negative_population": 0.009009009009009009
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.03988504904292942,
            "contribution_to_total": 0.0019335712274550622,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004548900682335102
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0028209865254796174,
            "contribution_to_total": -0.0025381968112505814,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005018230053342413
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.0086159196346056,
            "contribution_to_total": 0.00029327008555129943,
            "DeltaMRR_positive_anchor_full_negative_population": -0.01
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.03818412535925955,
            "contribution_to_total": 0.0008459651290484055,
            "DeltaMRR_positive_anchor_full_negative_population": -0.013812154696132596
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.028870338586927936,
            "contribution_to_total": 0.0012717937532921236,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0010473946059177794
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0028209865254796174,
            "contribution_to_total": -0.0025381968112505814,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005018230053342413
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.007539991007113576,
            "contribution_to_total": 0.0003562927674196913,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0010822510822510827
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.04134861594680285,
            "contribution_to_total": 0.0010644585246748714,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00797649034424853
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.03634350309219366,
            "contribution_to_total": 0.000990277675797266,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0013990905911157746
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.002633367848812369,
            "contribution_to_total": 2.371027008450195e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0015432098765432107
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0004587052745332438,
            "contribution_to_total": 6.231594347600067e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005555555555555556
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.00024930766761639575,
            "contribution_to_total": -0.0002131940569192554,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0006636016655100625
          }
        },
        "GDUP_vs_GMP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.002672269141855924,
            "contribution_to_total": -0.0024043875975298563,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005466887980932925
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.0023370990284465026,
            "contribution_to_total": 0.00012098314336272187,
            "DeltaMRR_positive_anchor_full_negative_population": 0.016216216216216217
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.03557717639475193,
            "contribution_to_total": 0.0017247316044902944,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004169825625473844
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.002672269141855924,
            "contribution_to_total": -0.0024043875975298563,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005466887980932925
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.0012784313528956869,
            "contribution_to_total": 4.351545605524256e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.028419999269334237,
            "contribution_to_total": 0.0006296419814054409,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0036832412523020264
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.02661762292508176,
            "contribution_to_total": 0.001172557310392333,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0014401675831369467
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.002672269141855924,
            "contribution_to_total": -0.0024043875975298563,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005466887980932925
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.0006434613540416805,
            "contribution_to_total": -3.040595490668849e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00974025974025974
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.03434363373922233,
            "contribution_to_total": 0.0008841256923583537,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0029387069689336695
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.03640652981390951,
            "contribution_to_total": 0.0009919950104013509,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002973067506121021
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.002156560066537319,
            "contribution_to_total": 1.9417196748305328e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0005536213287674998,
            "contribution_to_total": 7.521046158819267e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005555555555555556
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0007639651323258868,
            "contribution_to_total": -0.0006533005080133373,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0003701133472125839
          }
        },
        "GDUP_vs_GMG": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.003161889573608151,
            "contribution_to_total": -0.0028449260429892318,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005486394847349903
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.0029319667444131334,
            "contribution_to_total": 0.0001517772882777041,
            "DeltaMRR_positive_anchor_full_negative_population": 0.013513513513513514
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.031496982475289696,
            "contribution_to_total": 0.001526929526909351,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003411675511751327
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.003161889573608151,
            "contribution_to_total": -0.0028449260429892318,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005486394847349903
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.0010893215069144248,
            "contribution_to_total": -3.707850410332751e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.02384314688915876,
            "contribution_to_total": 0.0005282423165446682,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004604051565377532
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.026957805451597355,
            "contribution_to_total": 0.0011875430027457148,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0022257135375752814
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.003161889573608151,
            "contribution_to_total": -0.0028449260429892318,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005486394847349903
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 5.038630302089973e-05,
            "contribution_to_total": 2.380941214177379e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00974025974025974
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.030415741375458577,
            "contribution_to_total": 0.0007830079544395602,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00041981528127623866
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.03278504945063286,
            "contribution_to_total": 0.0008933179195333176,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0034977264777894365
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.0007715313977777918,
            "contribution_to_total": 6.9467005258057155e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0015432098765432107
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.00020910816306892217,
            "contribution_to_total": -2.8407723201859334e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004054054054054054
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0013386723918519727,
            "contribution_to_total": -0.001144758205126123,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0006881795049733981
          }
        }
      },
      "per_candidate_directory": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HDP_ZERO_V29/retrospective/pubmed/seed_1"
    },
    {
      "dataset": "pubmed",
      "seed": 2,
      "subgroups": {
        "H0": {
          "candidate_count": 41871,
          "positive_count": 712,
          "negative_count": 41159,
          "positive_anchored_query_count": 712,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.003545575926306704,
              "contribution_to_total_DeltaCE": 0.0031901497681448344,
              "DeltaMRR_positive_anchor_full_negative_population": -0.003971683746964646
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.002456981950870399,
              "contribution_to_total_DeltaCE": 0.0022106818648980247,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0037453183520599247
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0015849397243758178,
              "contribution_to_total_DeltaCE": 0.0014260574866627959,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0030443573280651936
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.0019823621061765104,
              "contribution_to_total_DeltaCE": 0.0017836402730728182,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0012887393505371034
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -0.00040994089090189785,
              "contribution_to_total_DeltaCE": -0.00036884637792146646,
              "DeltaMRR_positive_anchor_full_negative_population": 0.00020158524372007516
            }
          }
        },
        "H1": {
          "candidate_count": 2409,
          "positive_count": 185,
          "negative_count": 2224,
          "positive_anchored_query_count": 185,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.00850717699304317,
              "contribution_to_total_DeltaCE": -0.00044038570947741525,
              "DeltaMRR_positive_anchor_full_negative_population": 0.008108108108108109
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.016809567424457026,
              "contribution_to_total_DeltaCE": -0.0008701703611293831,
              "DeltaMRR_positive_anchor_full_negative_population": 0.008108108108108109
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0057139376066013756,
              "contribution_to_total_DeltaCE": 0.00029578983355472565,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 6.557397859955945e-07,
              "contribution_to_total_DeltaCE": 3.394527128381011e-08,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0072072072072072065
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -0.0011092798636315193,
              "contribution_to_total_DeltaCE": -5.7423396757098376e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.013513513513513514
            }
          }
        },
        "H2plus": {
          "candidate_count": 2256,
          "positive_count": 1319,
          "negative_count": 937,
          "positive_anchored_query_count": 1319,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.0326310304149454,
              "contribution_to_total_DeltaCE": -0.0015819065801984877,
              "DeltaMRR_positive_anchor_full_negative_population": 0.004738438210765732
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.03769524499713733,
              "contribution_to_total_DeltaCE": -0.0018274125991392,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0069497093757897406
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -0.026078871410187655,
              "contribution_to_total_DeltaCE": -0.001264267102917813,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0047384382107657315
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": -0.015105299965847472,
              "contribution_to_total_DeltaCE": -0.0007322837528569687,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0034748546878948703
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.018505678017473604,
              "contribution_to_total_DeltaCE": 0.0008971293108006801,
              "DeltaMRR_positive_anchor_full_negative_population": -0.001389941875157948
            }
          }
        },
        "G0": {
          "candidate_count": 41871,
          "positive_count": 712,
          "negative_count": 41159,
          "positive_anchored_query_count": 712,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.003545575926306704,
              "contribution_to_total_DeltaCE": 0.0031901497681448344,
              "DeltaMRR_positive_anchor_full_negative_population": -0.003971683746964646
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.002456981950870399,
              "contribution_to_total_DeltaCE": 0.0022106818648980247,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0037453183520599247
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0015849397243758178,
              "contribution_to_total_DeltaCE": 0.0014260574866627959,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0030443573280651936
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.0019823621061765104,
              "contribution_to_total_DeltaCE": 0.0017836402730728182,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0012887393505371034
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -0.00040994089090189785,
              "contribution_to_total_DeltaCE": -0.00036884637792146646,
              "DeltaMRR_positive_anchor_full_negative_population": 0.00020158524372007516
            }
          }
        },
        "G1": {
          "candidate_count": 1584,
          "positive_count": 50,
          "negative_count": 1534,
          "positive_anchored_query_count": 50,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.015336292428579047,
              "contribution_to_total_DeltaCE": -0.0005220192368675694,
              "DeltaMRR_positive_anchor_full_negative_population": 0.02
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.016898740564069065,
              "contribution_to_total_DeltaCE": -0.0005752021027480961,
              "DeltaMRR_positive_anchor_full_negative_population": 0.02
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0065900475891103455,
              "contribution_to_total_DeltaCE": 0.00022431312061953727,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.009514239858448747,
              "contribution_to_total_DeltaCE": 0.00032384725665684236,
              "DeltaMRR_positive_anchor_full_negative_population": -0.003333333333333335
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.0015589166060159467,
              "contribution_to_total_DeltaCE": 5.3062659101110096e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.006666666666666666
            }
          }
        },
        "G2to3": {
          "candidate_count": 1031,
          "positive_count": 181,
          "negative_count": 850,
          "positive_anchored_query_count": 181,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.03146122181906148,
              "contribution_to_total_DeltaCE": -0.0006970199350062831,
              "DeltaMRR_positive_anchor_full_negative_population": 0.01289134438305709
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.04025860842879123,
              "contribution_to_total_DeltaCE": -0.0008919250749975021,
              "DeltaMRR_positive_anchor_full_negative_population": 0.017955801104972375
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -0.0105932186195789,
              "contribution_to_total_DeltaCE": -0.00023469160213137884,
              "DeltaMRR_positive_anchor_full_negative_population": 0.006445672191528545
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": -0.0021932825312560617,
              "contribution_to_total_DeltaCE": -4.8591935055118616e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0055248618784530384
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.018711222609621454,
              "contribution_to_total_DeltaCE": 0.0004145450943467363,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0055248618784530384
            }
          }
        },
        "G4plus": {
          "candidate_count": 2050,
          "positive_count": 1273,
          "negative_count": 777,
          "positive_anchored_query_count": 1273,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.01823423760489571,
              "contribution_to_total_DeltaCE": -0.0008032531178020502,
              "DeltaMRR_positive_anchor_full_negative_population": 0.003469494632102645
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.027931946485604698,
              "contribution_to_total_DeltaCE": -0.001230455782522985,
              "DeltaMRR_positive_anchor_full_negative_population": 0.005040586540979314
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -0.021749309849485643,
              "contribution_to_total_DeltaCE": -0.0009580987878512457,
              "DeltaMRR_positive_anchor_full_negative_population": 0.003993191935061534
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": -0.02287085789847085,
              "contribution_to_total_DeltaCE": -0.0010075051291874085,
              "DeltaMRR_positive_anchor_full_negative_population": 0.003993191935061534
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.008446809756821045,
              "contribution_to_total_DeltaCE": 0.00037209816059573535,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0005236973029588898
            }
          }
        },
        "MULT0": {
          "candidate_count": 41871,
          "positive_count": 712,
          "negative_count": 41159,
          "positive_anchored_query_count": 712,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.003545575926306704,
              "contribution_to_total_DeltaCE": 0.0031901497681448344,
              "DeltaMRR_positive_anchor_full_negative_population": -0.003971683746964646
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": 0.002456981950870399,
              "contribution_to_total_DeltaCE": 0.0022106818648980247,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0037453183520599247
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0015849397243758178,
              "contribution_to_total_DeltaCE": 0.0014260574866627959,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0030443573280651936
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.0019823621061765104,
              "contribution_to_total_DeltaCE": 0.0017836402730728182,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0012887393505371034
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -0.00040994089090189785,
              "contribution_to_total_DeltaCE": -0.00036884637792146646,
              "DeltaMRR_positive_anchor_full_negative_population": 0.00020158524372007516
            }
          }
        },
        "MULT1to3": {
          "candidate_count": 2199,
          "positive_count": 154,
          "negative_count": 2045,
          "positive_anchored_query_count": 154,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.014347407978741358,
              "contribution_to_total_DeltaCE": -0.0006779686725385131,
              "DeltaMRR_positive_anchor_full_negative_population": 0.003246753246753247
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.018007573370130123,
              "contribution_to_total_DeltaCE": -0.0008509251727891556,
              "DeltaMRR_positive_anchor_full_negative_population": 0.003246753246753247
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.00805339328218546,
              "contribution_to_total_DeltaCE": 0.0003805529445488617,
              "DeltaMRR_positive_anchor_full_negative_population": -0.003246753246753247
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.0024889412977290395,
              "contribution_to_total_DeltaCE": 0.0001176117825706154,
              "DeltaMRR_positive_anchor_full_negative_population": -0.0010822510822510825
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -0.0033393907126277778,
              "contribution_to_total_DeltaCE": -0.00015779869728959267,
              "DeltaMRR_positive_anchor_full_negative_population": 0.00974025974025974
            }
          }
        },
        "MULT4to15": {
          "candidate_count": 1198,
          "positive_count": 397,
          "negative_count": 801,
          "positive_anchored_query_count": 397,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.03257563324173293,
              "contribution_to_total_DeltaCE": -0.0008386111531630576,
              "DeltaMRR_positive_anchor_full_negative_population": 0.010705289672544081
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.04176568061223748,
              "contribution_to_total_DeltaCE": -0.0010751952332271899,
              "DeltaMRR_positive_anchor_full_negative_population": 0.009235936188077245
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -0.019478235197657536,
              "contribution_to_total_DeltaCE": -0.000501438150395258,
              "DeltaMRR_positive_anchor_full_negative_population": 0.005667506297229219
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": -0.013862284087984707,
              "contribution_to_total_DeltaCE": -0.0003568638545944146,
              "DeltaMRR_positive_anchor_full_negative_population": 0.009026028547439127
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.018702473952137248,
              "contribution_to_total_DeltaCE": 0.0004814673327028628,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0029387069689336687
            }
          }
        },
        "MULT16plus": {
          "candidate_count": 1268,
          "positive_count": 953,
          "negative_count": 315,
          "positive_anchored_query_count": 953,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.01855980695860372,
              "contribution_to_total_DeltaCE": -0.000505712463974332,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0031479538300104933
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.02831291910463892,
              "contribution_to_total_DeltaCE": -0.0007714625542522381,
              "DeltaMRR_positive_anchor_full_negative_population": 0.006820566631689402
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -0.03110689611026241,
              "contribution_to_total_DeltaCE": -0.000847592063516691,
              "DeltaMRR_positive_anchor_full_negative_population": 0.00472193074501574
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": -0.018093172414911606,
              "contribution_to_total_DeltaCE": -0.0004929977355618857,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0026232948583420775
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.01893873091351749,
              "contribution_to_total_DeltaCE": 0.0005160372786303115,
              "DeltaMRR_positive_anchor_full_negative_population": -0.002098635886673662
            }
          }
        },
        "degree0to3": {
          "candidate_count": 419,
          "positive_count": 9,
          "negative_count": 410,
          "positive_anchored_query_count": 9,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": -0.00041348344583614575,
              "contribution_to_total_DeltaCE": -3.722914814452146e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.003682521687297141,
              "contribution_to_total_DeltaCE": -3.3156622549800196e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -0.0008266598613712166,
              "contribution_to_total_DeltaCE": -7.443065195000425e-06,
              "DeltaMRR_positive_anchor_full_negative_population": -0.01851851851851852
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.00014092988430495238,
              "contribution_to_total_DeltaCE": 1.2689019581351006e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": -0.0013853386866073516,
              "contribution_to_total_DeltaCE": -1.247328755562318e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0
            }
          }
        },
        "degree4to15": {
          "candidate_count": 6322,
          "positive_count": 111,
          "negative_count": 6211,
          "positive_anchored_query_count": 111,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.00021758171438660944,
              "contribution_to_total_DeltaCE": 2.955887051642051e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.004804804804804805
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.0005342653658718698,
              "contribution_to_total_DeltaCE": -7.258091892388605e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0078078078078078084
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": -3.235088453631898e-05,
              "contribution_to_total_DeltaCE": -4.394926337429272e-06,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0037537537537537533
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.000186711014823332,
              "contribution_to_total_DeltaCE": 2.536502999211589e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0045045045045045045
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.0006371539270953968,
              "contribution_to_total_DeltaCE": 8.655851656990498e-05,
              "DeltaMRR_positive_anchor_full_negative_population": 0.008258258258258258
            }
          }
        },
        "degree16plus": {
          "candidate_count": 39795,
          "positive_count": 2096,
          "negative_count": 37699,
          "positive_anchored_query_count": 2096,
          "effects": {
            "GMH": {
              "mean_DeltaCE_vs_GM": 0.0013354721342752457,
              "contribution_to_total_DeltaCE": 0.0011420215227669632,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0020939064116545034
            },
            "GMS": {
              "mean_DeltaCE_vs_GM": -0.0004457300450846805,
              "contribution_to_total_DeltaCE": -0.0003811635538968725,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0034033078880407125
            },
            "GMP": {
              "mean_DeltaCE_vs_GM": 0.0005489344331250756,
              "contribution_to_total_DeltaCE": 0.0004694182088321382,
              "DeltaMRR_positive_anchor_full_negative_population": 0.0018284435030618237
            },
            "GMG": {
              "mean_DeltaCE_vs_GM": 0.0011983432603259795,
              "contribution_to_total_DeltaCE": 0.0010247565335368821,
              "DeltaMRR_positive_anchor_full_negative_population": 0.002146509660822638
            },
            "GDUP": {
              "mean_DeltaCE_vs_GM": 0.00046398515279733976,
              "contribution_to_total_DeltaCE": 0.00039677430710783343,
              "DeltaMRR_positive_anchor_full_negative_population": -5.0797379041653935e-05
            }
          }
        }
      },
      "ranking_rule": "subgroup positive anchors, original full negative population; no filtered-negative ranking",
      "calibration_warning": "H0 uses a constant HDP raw block; improvements there do not prove incremental structural information",
      "all_pairwise_subgroups": {
        "GM_vs_GMH": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.003545575926306704,
            "contribution_to_total": -0.0031901497681448344,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003971683746964646
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.00850717699304317,
            "contribution_to_total": 0.00044038570947741525,
            "DeltaMRR_positive_anchor_full_negative_population": -0.008108108108108109
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.0326310304149454,
            "contribution_to_total": 0.0015819065801984877,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004738438210765732
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.003545575926306704,
            "contribution_to_total": -0.0031901497681448344,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003971683746964646
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.015336292428579047,
            "contribution_to_total": 0.0005220192368675694,
            "DeltaMRR_positive_anchor_full_negative_population": -0.02
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.03146122181906148,
            "contribution_to_total": 0.0006970199350062831,
            "DeltaMRR_positive_anchor_full_negative_population": -0.01289134438305709
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.01823423760489571,
            "contribution_to_total": 0.0008032531178020502,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003469494632102645
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.003545575926306704,
            "contribution_to_total": -0.0031901497681448344,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003971683746964646
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.014347407978741358,
            "contribution_to_total": 0.0006779686725385131,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003246753246753247
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.03257563324173293,
            "contribution_to_total": 0.0008386111531630576,
            "DeltaMRR_positive_anchor_full_negative_population": -0.010705289672544081
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.01855980695860372,
            "contribution_to_total": 0.000505712463974332,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0031479538300104933
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.00041348344583614575,
            "contribution_to_total": 3.722914814452146e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.00021758171438660944,
            "contribution_to_total": -2.955887051642051e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004804804804804805
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0013354721342752457,
            "contribution_to_total": -0.0011420215227669632,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0020939064116545034
          }
        },
        "GM_vs_GMS": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.002456981950870399,
            "contribution_to_total": -0.0022106818648980247,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0037453183520599247
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.016809567424457026,
            "contribution_to_total": 0.0008701703611293831,
            "DeltaMRR_positive_anchor_full_negative_population": -0.008108108108108109
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.03769524499713733,
            "contribution_to_total": 0.0018274125991392,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0069497093757897406
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.002456981950870399,
            "contribution_to_total": -0.0022106818648980247,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0037453183520599247
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.016898740564069065,
            "contribution_to_total": 0.0005752021027480961,
            "DeltaMRR_positive_anchor_full_negative_population": -0.02
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.04025860842879123,
            "contribution_to_total": 0.0008919250749975021,
            "DeltaMRR_positive_anchor_full_negative_population": -0.017955801104972375
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.027931946485604698,
            "contribution_to_total": 0.001230455782522985,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005040586540979314
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.002456981950870399,
            "contribution_to_total": -0.0022106818648980247,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0037453183520599247
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.018007573370130123,
            "contribution_to_total": 0.0008509251727891556,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003246753246753247
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.04176568061223748,
            "contribution_to_total": 0.0010751952332271899,
            "DeltaMRR_positive_anchor_full_negative_population": -0.009235936188077245
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.02831291910463892,
            "contribution_to_total": 0.0007714625542522381,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006820566631689402
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.003682521687297141,
            "contribution_to_total": 3.3156622549800196e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0005342653658718698,
            "contribution_to_total": 7.258091892388605e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0078078078078078084
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0004457300450846805,
            "contribution_to_total": 0.0003811635538968725,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0034033078880407125
          }
        },
        "GM_vs_GMP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0015849397243758178,
            "contribution_to_total": -0.0014260574866627959,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0030443573280651936
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.0057139376066013756,
            "contribution_to_total": -0.00029578983355472565,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.026078871410187655,
            "contribution_to_total": 0.001264267102917813,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0047384382107657315
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0015849397243758178,
            "contribution_to_total": -0.0014260574866627959,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0030443573280651936
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.0065900475891103455,
            "contribution_to_total": -0.00022431312061953727,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.0105932186195789,
            "contribution_to_total": 0.00023469160213137884,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006445672191528545
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.021749309849485643,
            "contribution_to_total": 0.0009580987878512457,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003993191935061534
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0015849397243758178,
            "contribution_to_total": -0.0014260574866627959,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0030443573280651936
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.00805339328218546,
            "contribution_to_total": -0.0003805529445488617,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003246753246753247
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.019478235197657536,
            "contribution_to_total": 0.000501438150395258,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005667506297229219
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.03110689611026241,
            "contribution_to_total": 0.000847592063516691,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00472193074501574
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.0008266598613712166,
            "contribution_to_total": 7.443065195000425e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.01851851851851852
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 3.235088453631898e-05,
            "contribution_to_total": 4.394926337429272e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0037537537537537533
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0005489344331250756,
            "contribution_to_total": -0.0004694182088321382,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0018284435030618237
          }
        },
        "GM_vs_GMG": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0019823621061765104,
            "contribution_to_total": -0.0017836402730728182,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0012887393505371034
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -6.557397859955945e-07,
            "contribution_to_total": -3.394527128381011e-08,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0072072072072072065
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.015105299965847472,
            "contribution_to_total": 0.0007322837528569687,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0034748546878948703
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0019823621061765104,
            "contribution_to_total": -0.0017836402730728182,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0012887393505371034
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.009514239858448747,
            "contribution_to_total": -0.00032384725665684236,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003333333333333335
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.0021932825312560617,
            "contribution_to_total": 4.8591935055118616e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0055248618784530384
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.02287085789847085,
            "contribution_to_total": 0.0010075051291874085,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003993191935061534
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0019823621061765104,
            "contribution_to_total": -0.0017836402730728182,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0012887393505371034
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.0024889412977290395,
            "contribution_to_total": -0.0001176117825706154,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0010822510822510825
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.013862284087984707,
            "contribution_to_total": 0.0003568638545944146,
            "DeltaMRR_positive_anchor_full_negative_population": -0.009026028547439127
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.018093172414911606,
            "contribution_to_total": 0.0004929977355618857,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0026232948583420775
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.00014092988430495238,
            "contribution_to_total": -1.2689019581351006e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.000186711014823332,
            "contribution_to_total": -2.536502999211589e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0045045045045045045
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0011983432603259795,
            "contribution_to_total": -0.0010247565335368821,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002146509660822638
          }
        },
        "GM_vs_GDUP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.00040994089090189785,
            "contribution_to_total": 0.00036884637792146646,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00020158524372007516
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.0011092798636315193,
            "contribution_to_total": 5.7423396757098376e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.013513513513513514
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.018505678017473604,
            "contribution_to_total": -0.0008971293108006801,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001389941875157948
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.00040994089090189785,
            "contribution_to_total": 0.00036884637792146646,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00020158524372007516
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.0015589166060159467,
            "contribution_to_total": -5.3062659101110096e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006666666666666666
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.018711222609621454,
            "contribution_to_total": -0.0004145450943467363,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0055248618784530384
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.008446809756821045,
            "contribution_to_total": -0.00037209816059573535,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0005236973029588898
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.00040994089090189785,
            "contribution_to_total": 0.00036884637792146646,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00020158524372007516
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.0033393907126277778,
            "contribution_to_total": 0.00015779869728959267,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00974025974025974
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.018702473952137248,
            "contribution_to_total": -0.0004814673327028628,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0029387069689336687
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.01893873091351749,
            "contribution_to_total": -0.0005160372786303115,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002098635886673662
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.0013853386866073516,
            "contribution_to_total": 1.247328755562318e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0006371539270953968,
            "contribution_to_total": -8.655851656990498e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.008258258258258258
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.00046398515279733976,
            "contribution_to_total": -0.00039677430710783343,
            "DeltaMRR_positive_anchor_full_negative_population": 5.0797379041653935e-05
          }
        },
        "GMH_vs_GM": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.003545575926306704,
            "contribution_to_total": 0.0031901497681448344,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003971683746964646
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.00850717699304317,
            "contribution_to_total": -0.00044038570947741525,
            "DeltaMRR_positive_anchor_full_negative_population": 0.008108108108108109
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.0326310304149454,
            "contribution_to_total": -0.0015819065801984877,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004738438210765732
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.003545575926306704,
            "contribution_to_total": 0.0031901497681448344,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003971683746964646
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.015336292428579047,
            "contribution_to_total": -0.0005220192368675694,
            "DeltaMRR_positive_anchor_full_negative_population": 0.02
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.03146122181906148,
            "contribution_to_total": -0.0006970199350062831,
            "DeltaMRR_positive_anchor_full_negative_population": 0.01289134438305709
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.01823423760489571,
            "contribution_to_total": -0.0008032531178020502,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003469494632102645
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.003545575926306704,
            "contribution_to_total": 0.0031901497681448344,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003971683746964646
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.014347407978741358,
            "contribution_to_total": -0.0006779686725385131,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003246753246753247
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.03257563324173293,
            "contribution_to_total": -0.0008386111531630576,
            "DeltaMRR_positive_anchor_full_negative_population": 0.010705289672544081
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.01855980695860372,
            "contribution_to_total": -0.000505712463974332,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0031479538300104933
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.00041348344583614575,
            "contribution_to_total": -3.722914814452146e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.00021758171438660944,
            "contribution_to_total": 2.955887051642051e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004804804804804805
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0013354721342752457,
            "contribution_to_total": 0.0011420215227669632,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0020939064116545034
          }
        },
        "GMH_vs_GMS": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0010885939754363056,
            "contribution_to_total": 0.00097946790324681,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00022636539490472087
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.008302390431413854,
            "contribution_to_total": 0.00042978465165196785,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.005064214582191933,
            "contribution_to_total": 0.00024550601894071254,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002211271165024008
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0010885939754363056,
            "contribution_to_total": 0.00097946790324681,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00022636539490472087
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.0015624481354900173,
            "contribution_to_total": 5.3182865880526635e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.008797386609729747,
            "contribution_to_total": 0.00019490513999121902,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005064456721915285
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.009697708880708984,
            "contribution_to_total": 0.00042720266472093477,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0015710919088766694
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0010885939754363056,
            "contribution_to_total": 0.00097946790324681,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00022636539490472087
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.0036601653913887625,
            "contribution_to_total": 0.00017295650025064228,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.009190047370504557,
            "contribution_to_total": 0.00023658408006413227,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0014693534844668348
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.009753112146035197,
            "contribution_to_total": 0.00026575009027790595,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0036726128016789086
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.0032690382414609963,
            "contribution_to_total": 2.9433707735348063e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0007518470802584793,
            "contribution_to_total": 0.00010213978944030655,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003003003003003003
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.001781202179359926,
            "contribution_to_total": 0.0015231850766638355,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0013094014763862093
          }
        },
        "GMH_vs_GMP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0019606362019308865,
            "contribution_to_total": 0.0017640922814820387,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0009273264188994528
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.014221114599644548,
            "contribution_to_total": -0.000736175543032141,
            "DeltaMRR_positive_anchor_full_negative_population": 0.008108108108108109
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.006552159004757747,
            "contribution_to_total": -0.0003176394772806747,
            "DeltaMRR_positive_anchor_full_negative_population": 1.6834314247538386e-19
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0019606362019308865,
            "contribution_to_total": 0.0017640922814820387,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0009273264188994528
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.02192634001768939,
            "contribution_to_total": -0.0007463323574871066,
            "DeltaMRR_positive_anchor_full_negative_population": 0.02
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.02086800319948259,
            "contribution_to_total": -0.00046232833287490437,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006445672191528545
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.0035150722445899335,
            "contribution_to_total": 0.00015484567004919554,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0005236973029588897
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0019606362019308865,
            "contribution_to_total": 0.0017640922814820387,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0009273264188994528
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.02240080126092682,
            "contribution_to_total": -0.0010585216170873749,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006493506493506494
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.01309739804407539,
            "contribution_to_total": -0.0003371730027677995,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005037783375314861
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.01254708915165868,
            "contribution_to_total": 0.00034187959954235875,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0015739769150052466
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.00041317641553507105,
            "contribution_to_total": 3.7201503805482806e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.01851851851851852
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.00024993259892292847,
            "contribution_to_total": 3.395379685384978e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0010510510510510513
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0007865377011501701,
            "contribution_to_total": 0.000672603313934825,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0002654629085926797
          }
        },
        "GMH_vs_GMG": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.001563213820130194,
            "contribution_to_total": 0.0014065094950720162,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0026829443964275423
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.008507832732829165,
            "contribution_to_total": -0.00044041965474869905,
            "DeltaMRR_positive_anchor_full_negative_population": 0.000900900900900901
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.017525730449097925,
            "contribution_to_total": -0.0008496228273415188,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0012635835228708618
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.001563213820130194,
            "contribution_to_total": 0.0014065094950720162,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0026829443964275423
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.024850532287027792,
            "contribution_to_total": -0.0008458664935244117,
            "DeltaMRR_positive_anchor_full_negative_population": 0.023333333333333334
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.02926793928780543,
            "contribution_to_total": -0.0006484279999511645,
            "DeltaMRR_positive_anchor_full_negative_population": 0.007366482504604053
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.004636620293575143,
            "contribution_to_total": 0.00020425201138535849,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0005236973029588897
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.001563213820130194,
            "contribution_to_total": 0.0014065094950720162,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0026829443964275423
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.0168363492764704,
            "contribution_to_total": -0.0007955804551091286,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00432900432900433
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.01871334915374822,
            "contribution_to_total": -0.00048174729856864293,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0016792611251049546
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.0004666345436921172,
            "contribution_to_total": -1.2714728412446377e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0005246589716684155
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.0005544133301410981,
            "contribution_to_total": -4.991816772587246e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 3.0870699563277425e-05,
            "contribution_to_total": 4.193840524304622e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00030030030030030023
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.00013712887394926615,
            "contribution_to_total": 0.00011726498923008094,
            "DeltaMRR_positive_anchor_full_negative_population": -5.260324916813448e-05
          }
        },
        "GMH_vs_GDUP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.003955516817208603,
            "contribution_to_total": 0.0035589961460663014,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004173268990684721
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.007397897129411649,
            "contribution_to_total": -0.00038296231272031686,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005405405405405406
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.051136708432419,
            "contribution_to_total": -0.0024790358909991678,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00612838008592368
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.003955516817208603,
            "contribution_to_total": 0.0035589961460663014,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004173268990684721
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.01689520903459499,
            "contribution_to_total": -0.0005750818959686795,
            "DeltaMRR_positive_anchor_full_negative_population": 0.013333333333333334
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.05017244442868294,
            "contribution_to_total": -0.0011115650293530195,
            "DeltaMRR_positive_anchor_full_negative_population": 0.007366482504604053
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.026681047361716757,
            "contribution_to_total": -0.0011753512783977856,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003993191935061535
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.003955516817208603,
            "contribution_to_total": 0.0035589961460663014,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004173268990684721
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.01100801726611358,
            "contribution_to_total": -0.0005201699752489205,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.05127810719387018,
            "contribution_to_total": -0.0013200784858659203,
            "DeltaMRR_positive_anchor_full_negative_population": 0.007766582703610411
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.037498537872121214,
            "contribution_to_total": -0.0010217497426046438,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005246589716684155
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.000971855240771206,
            "contribution_to_total": 8.750372741171036e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0004195722127087874,
            "contribution_to_total": -5.699964605348448e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003453453453453453
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0008714869814779058,
            "contribution_to_total": 0.0007452472156591296,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0021447037906961574
          }
        },
        "GMS_vs_GM": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.002456981950870399,
            "contribution_to_total": 0.0022106818648980247,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0037453183520599247
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.016809567424457026,
            "contribution_to_total": -0.0008701703611293831,
            "DeltaMRR_positive_anchor_full_negative_population": 0.008108108108108109
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.03769524499713733,
            "contribution_to_total": -0.0018274125991392,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0069497093757897406
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.002456981950870399,
            "contribution_to_total": 0.0022106818648980247,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0037453183520599247
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.016898740564069065,
            "contribution_to_total": -0.0005752021027480961,
            "DeltaMRR_positive_anchor_full_negative_population": 0.02
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.04025860842879123,
            "contribution_to_total": -0.0008919250749975021,
            "DeltaMRR_positive_anchor_full_negative_population": 0.017955801104972375
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.027931946485604698,
            "contribution_to_total": -0.001230455782522985,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005040586540979314
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.002456981950870399,
            "contribution_to_total": 0.0022106818648980247,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0037453183520599247
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.018007573370130123,
            "contribution_to_total": -0.0008509251727891556,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003246753246753247
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.04176568061223748,
            "contribution_to_total": -0.0010751952332271899,
            "DeltaMRR_positive_anchor_full_negative_population": 0.009235936188077245
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.02831291910463892,
            "contribution_to_total": -0.0007714625542522381,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006820566631689402
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.003682521687297141,
            "contribution_to_total": -3.3156622549800196e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0005342653658718698,
            "contribution_to_total": -7.258091892388605e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0078078078078078084
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0004457300450846805,
            "contribution_to_total": -0.0003811635538968725,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0034033078880407125
          }
        },
        "GMS_vs_GMH": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0010885939754363056,
            "contribution_to_total": -0.00097946790324681,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00022636539490472087
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.008302390431413854,
            "contribution_to_total": -0.00042978465165196785,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.005064214582191933,
            "contribution_to_total": -0.00024550601894071254,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002211271165024008
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0010885939754363056,
            "contribution_to_total": -0.00097946790324681,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00022636539490472087
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.0015624481354900173,
            "contribution_to_total": -5.3182865880526635e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.008797386609729747,
            "contribution_to_total": -0.00019490513999121902,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005064456721915285
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.009697708880708984,
            "contribution_to_total": -0.00042720266472093477,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0015710919088766694
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0010885939754363056,
            "contribution_to_total": -0.00097946790324681,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00022636539490472087
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.0036601653913887625,
            "contribution_to_total": -0.00017295650025064228,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.009190047370504557,
            "contribution_to_total": -0.00023658408006413227,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0014693534844668348
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.009753112146035197,
            "contribution_to_total": -0.00026575009027790595,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0036726128016789086
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.0032690382414609963,
            "contribution_to_total": -2.9433707735348063e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0007518470802584793,
            "contribution_to_total": -0.00010213978944030655,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003003003003003003
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.001781202179359926,
            "contribution_to_total": -0.0015231850766638355,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0013094014763862093
          }
        },
        "GMS_vs_GMP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0008720422264945809,
            "contribution_to_total": 0.0007846243782352286,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0007009610239947313
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.022523505031058398,
            "contribution_to_total": -0.0011659601946841086,
            "DeltaMRR_positive_anchor_full_negative_population": 0.008108108108108109
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.011616373586949679,
            "contribution_to_total": -0.0005631454962213873,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002211271165024008
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0008720422264945809,
            "contribution_to_total": 0.0007846243782352286,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0007009610239947313
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.02348878815317941,
            "contribution_to_total": -0.0007995152233676334,
            "DeltaMRR_positive_anchor_full_negative_population": 0.02
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.029665389809212336,
            "contribution_to_total": -0.0006572334728661234,
            "DeltaMRR_positive_anchor_full_negative_population": 0.011510128913443829
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.006182636636119053,
            "contribution_to_total": -0.00027235699467173925,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0010473946059177796
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0008720422264945809,
            "contribution_to_total": 0.0007846243782352286,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0007009610239947313
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.026060966652315578,
            "contribution_to_total": -0.001231478117338017,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006493506493506494
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.022287445414579946,
            "contribution_to_total": -0.0005737570828319318,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003568429890848027
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.002793977005623485,
            "contribution_to_total": 7.612950926445288e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002098635886673662
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.002855861825925925,
            "contribution_to_total": -2.571355735479978e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.01851851851851852
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.000501914481335551,
            "contribution_to_total": -6.818599258645678e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004054054054054054
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0009946644782097562,
            "contribution_to_total": -0.0008505817627290108,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0015748643849788889
          }
        },
        "GMS_vs_GMG": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0004746198446938885,
            "contribution_to_total": 0.0004270415918252064,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0024565790015228218
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.016810223164243018,
            "contribution_to_total": -0.0008702043064006667,
            "DeltaMRR_positive_anchor_full_negative_population": 0.000900900900900901
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.02258994503128986,
            "contribution_to_total": -0.0010951288462822315,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0034748546878948703
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0004746198446938885,
            "contribution_to_total": 0.0004270415918252064,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0024565790015228218
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.02641298042251781,
            "contribution_to_total": -0.0008990493594049384,
            "DeltaMRR_positive_anchor_full_negative_population": 0.023333333333333334
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.038065325897535175,
            "contribution_to_total": -0.0008433331399423837,
            "DeltaMRR_positive_anchor_full_negative_population": 0.012430939226519336
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.005061088587133844,
            "contribution_to_total": -0.00022295065333557634,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0010473946059177798
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0004746198446938885,
            "contribution_to_total": 0.0004270415918252064,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0024565790015228218
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.02049651466785916,
            "contribution_to_total": -0.0009685369553597708,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00432900432900433
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.027903396524252777,
            "contribution_to_total": -0.0007183313786327752,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0002099076406381196
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.010219746689727313,
            "contribution_to_total": -0.0002784648186903523,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004197271773347324
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.0038234515716020936,
            "contribution_to_total": -3.4425524507935304e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0007209763806952018,
            "contribution_to_total": -9.794594891600194e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0033033033033033035
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0016440733054106597,
            "contribution_to_total": -0.0014059200874337546,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0012567982272180748
          }
        },
        "GMS_vs_GDUP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.002866922841772297,
            "contribution_to_total": 0.0025795282428194913,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00394690359578
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.015700287560825504,
            "contribution_to_total": -0.0008127469643722847,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005405405405405406
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.05620092301461094,
            "contribution_to_total": -0.0027245419099398804,
            "DeltaMRR_positive_anchor_full_negative_population": 0.008339651250947688
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.002866922841772297,
            "contribution_to_total": 0.0025795282428194913,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00394690359578
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.01845765717008501,
            "contribution_to_total": -0.0006282647618492061,
            "DeltaMRR_positive_anchor_full_negative_population": 0.013333333333333334
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.05896983103841269,
            "contribution_to_total": -0.0013064701693442386,
            "DeltaMRR_positive_anchor_full_negative_population": 0.012430939226519336
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.036378756242425744,
            "contribution_to_total": -0.0016025539431187205,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005564283843938204
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.002866922841772297,
            "contribution_to_total": 0.0025795282428194913,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00394690359578
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.014668182657502343,
            "contribution_to_total": -0.0006931264754995628,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.06046815456437474,
            "contribution_to_total": -0.0015566625659300527,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006297229219143577
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.04725165001815641,
            "contribution_to_total": -0.0012874998328825497,
            "DeltaMRR_positive_anchor_full_negative_population": 0.008919202518363064
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.0022971830006897898,
            "contribution_to_total": -2.0683334994177023e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0011714192929672667,
            "contribution_to_total": -0.00015913943549379105,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0004504504504504496
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0009097151978820204,
            "contribution_to_total": -0.000777937861004706,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003454105267082367
          }
        },
        "GMP_vs_GM": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0015849397243758178,
            "contribution_to_total": 0.0014260574866627959,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0030443573280651936
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.0057139376066013756,
            "contribution_to_total": 0.00029578983355472565,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.026078871410187655,
            "contribution_to_total": -0.001264267102917813,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0047384382107657315
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0015849397243758178,
            "contribution_to_total": 0.0014260574866627959,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0030443573280651936
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.0065900475891103455,
            "contribution_to_total": 0.00022431312061953727,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.0105932186195789,
            "contribution_to_total": -0.00023469160213137884,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006445672191528545
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.021749309849485643,
            "contribution_to_total": -0.0009580987878512457,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003993191935061534
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0015849397243758178,
            "contribution_to_total": 0.0014260574866627959,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0030443573280651936
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.00805339328218546,
            "contribution_to_total": 0.0003805529445488617,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003246753246753247
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.019478235197657536,
            "contribution_to_total": -0.000501438150395258,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005667506297229219
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.03110689611026241,
            "contribution_to_total": -0.000847592063516691,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00472193074501574
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.0008266598613712166,
            "contribution_to_total": -7.443065195000425e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.01851851851851852
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -3.235088453631898e-05,
            "contribution_to_total": -4.394926337429272e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0037537537537537533
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0005489344331250756,
            "contribution_to_total": 0.0004694182088321382,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0018284435030618237
          }
        },
        "GMP_vs_GMH": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0019606362019308865,
            "contribution_to_total": -0.0017640922814820387,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0009273264188994528
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.014221114599644548,
            "contribution_to_total": 0.000736175543032141,
            "DeltaMRR_positive_anchor_full_negative_population": -0.008108108108108109
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.006552159004757747,
            "contribution_to_total": 0.0003176394772806747,
            "DeltaMRR_positive_anchor_full_negative_population": -1.6834314247538386e-19
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0019606362019308865,
            "contribution_to_total": -0.0017640922814820387,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0009273264188994528
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.02192634001768939,
            "contribution_to_total": 0.0007463323574871066,
            "DeltaMRR_positive_anchor_full_negative_population": -0.02
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.02086800319948259,
            "contribution_to_total": 0.00046232833287490437,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006445672191528545
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.0035150722445899335,
            "contribution_to_total": -0.00015484567004919554,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0005236973029588897
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0019606362019308865,
            "contribution_to_total": -0.0017640922814820387,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0009273264188994528
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.02240080126092682,
            "contribution_to_total": 0.0010585216170873749,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.01309739804407539,
            "contribution_to_total": 0.0003371730027677995,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005037783375314861
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.01254708915165868,
            "contribution_to_total": -0.00034187959954235875,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0015739769150052466
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.00041317641553507105,
            "contribution_to_total": -3.7201503805482806e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.01851851851851852
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.00024993259892292847,
            "contribution_to_total": -3.395379685384978e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0010510510510510513
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0007865377011501701,
            "contribution_to_total": -0.000672603313934825,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0002654629085926797
          }
        },
        "GMP_vs_GMS": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0008720422264945809,
            "contribution_to_total": -0.0007846243782352286,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0007009610239947313
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.022523505031058398,
            "contribution_to_total": 0.0011659601946841086,
            "DeltaMRR_positive_anchor_full_negative_population": -0.008108108108108109
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.011616373586949679,
            "contribution_to_total": 0.0005631454962213873,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002211271165024008
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0008720422264945809,
            "contribution_to_total": -0.0007846243782352286,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0007009610239947313
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.02348878815317941,
            "contribution_to_total": 0.0007995152233676334,
            "DeltaMRR_positive_anchor_full_negative_population": -0.02
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.029665389809212336,
            "contribution_to_total": 0.0006572334728661234,
            "DeltaMRR_positive_anchor_full_negative_population": -0.011510128913443829
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.006182636636119053,
            "contribution_to_total": 0.00027235699467173925,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0010473946059177796
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0008720422264945809,
            "contribution_to_total": -0.0007846243782352286,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0007009610239947313
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.026060966652315578,
            "contribution_to_total": 0.001231478117338017,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006493506493506494
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.022287445414579946,
            "contribution_to_total": 0.0005737570828319318,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003568429890848027
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.002793977005623485,
            "contribution_to_total": -7.612950926445288e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002098635886673662
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.002855861825925925,
            "contribution_to_total": 2.571355735479978e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.01851851851851852
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.000501914481335551,
            "contribution_to_total": 6.818599258645678e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004054054054054054
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0009946644782097562,
            "contribution_to_total": 0.0008505817627290108,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0015748643849788889
          }
        },
        "GMP_vs_GMG": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0003974223818006926,
            "contribution_to_total": -0.00035758278641002234,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0017556179775280898
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.00571328186681538,
            "contribution_to_total": 0.00029575588828344184,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0072072072072072065
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.010973571444340179,
            "contribution_to_total": -0.0005319833500608441,
            "DeltaMRR_positive_anchor_full_negative_population": 0.001263583522870862
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0003974223818006926,
            "contribution_to_total": -0.00035758278641002234,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0017556179775280898
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.0029241922693384018,
            "contribution_to_total": -9.953413603730506e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0033333333333333335
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.008399936088322839,
            "contribution_to_total": -0.00018609966707626023,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0009208103130755066
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.0011215480489852087,
            "contribution_to_total": 4.940634133616292e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0003974223818006926,
            "contribution_to_total": -0.00035758278641002234,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0017556179775280898
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.00556445198445642,
            "contribution_to_total": 0.00026294116197824623,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0021645021645021645
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.005615951109672831,
            "contribution_to_total": -0.00014457429580084344,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0033585222502099076
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.013013723695350797,
            "contribution_to_total": -0.0003545943279548051,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002098635886673662
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.0009675897456761691,
            "contribution_to_total": -8.711967153135527e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.01851851851851852
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.00021906189935965096,
            "contribution_to_total": -2.9759956329545154e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0007507507507507511
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0006494088272009038,
            "contribution_to_total": -0.0005553383247047439,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00031806615776081416
          }
        },
        "GMP_vs_GDUP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.001994880615277715,
            "contribution_to_total": 0.001794903864584262,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003245942571785268
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.0068232174702328955,
            "contribution_to_total": 0.0003532132303118241,
            "DeltaMRR_positive_anchor_full_negative_population": -0.013513513513513514
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.04458454942766126,
            "contribution_to_total": -0.0021613964137184934,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00612838008592368
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.001994880615277715,
            "contribution_to_total": 0.001794903864584262,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003245942571785268
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.005031130983094398,
            "contribution_to_total": 0.00017125046151842717,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006666666666666666
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.029304441229200354,
            "contribution_to_total": -0.0006492366964781152,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0009208103130755063
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.030196119606306686,
            "contribution_to_total": -0.001330196948446981,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004516889238020424
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.001994880615277715,
            "contribution_to_total": 0.001794903864584262,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003245942571785268
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.011392783994813237,
            "contribution_to_total": 0.0005383516418384543,
            "DeltaMRR_positive_anchor_full_negative_population": -0.012987012987012988
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.03818070914979479,
            "contribution_to_total": -0.0009829054830981208,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0027287993282955505
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.05004562702377989,
            "contribution_to_total": -0.0013636293421470025,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006820566631689402
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.0005586788252361347,
            "contribution_to_total": 5.030222360622753e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.01851851851851852
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.0006695048116317158,
            "contribution_to_total": -9.095344290733427e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004504504504504504
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 8.494928032773568e-05,
            "contribution_to_total": 7.264390172430464e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0018792408821034776
          }
        },
        "GMG_vs_GM": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0019823621061765104,
            "contribution_to_total": 0.0017836402730728182,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0012887393505371034
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 6.557397859955945e-07,
            "contribution_to_total": 3.394527128381011e-08,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0072072072072072065
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.015105299965847472,
            "contribution_to_total": -0.0007322837528569687,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0034748546878948703
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0019823621061765104,
            "contribution_to_total": 0.0017836402730728182,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0012887393505371034
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.009514239858448747,
            "contribution_to_total": 0.00032384725665684236,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003333333333333335
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.0021932825312560617,
            "contribution_to_total": -4.8591935055118616e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0055248618784530384
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.02287085789847085,
            "contribution_to_total": -0.0010075051291874085,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003993191935061534
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0019823621061765104,
            "contribution_to_total": 0.0017836402730728182,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0012887393505371034
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.0024889412977290395,
            "contribution_to_total": 0.0001176117825706154,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0010822510822510825
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.013862284087984707,
            "contribution_to_total": -0.0003568638545944146,
            "DeltaMRR_positive_anchor_full_negative_population": 0.009026028547439127
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.018093172414911606,
            "contribution_to_total": -0.0004929977355618857,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0026232948583420775
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.00014092988430495238,
            "contribution_to_total": 1.2689019581351006e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.000186711014823332,
            "contribution_to_total": 2.536502999211589e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0045045045045045045
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0011983432603259795,
            "contribution_to_total": 0.0010247565335368821,
            "DeltaMRR_positive_anchor_full_negative_population": 0.002146509660822638
          }
        },
        "GMG_vs_GMH": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.001563213820130194,
            "contribution_to_total": -0.0014065094950720162,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0026829443964275423
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.008507832732829165,
            "contribution_to_total": 0.00044041965474869905,
            "DeltaMRR_positive_anchor_full_negative_population": -0.000900900900900901
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.017525730449097925,
            "contribution_to_total": 0.0008496228273415188,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0012635835228708618
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.001563213820130194,
            "contribution_to_total": -0.0014065094950720162,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0026829443964275423
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.024850532287027792,
            "contribution_to_total": 0.0008458664935244117,
            "DeltaMRR_positive_anchor_full_negative_population": -0.023333333333333334
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.02926793928780543,
            "contribution_to_total": 0.0006484279999511645,
            "DeltaMRR_positive_anchor_full_negative_population": -0.007366482504604053
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.004636620293575143,
            "contribution_to_total": -0.00020425201138535849,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0005236973029588897
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.001563213820130194,
            "contribution_to_total": -0.0014065094950720162,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0026829443964275423
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.0168363492764704,
            "contribution_to_total": 0.0007955804551091286,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00432900432900433
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.01871334915374822,
            "contribution_to_total": 0.00048174729856864293,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0016792611251049546
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.0004666345436921172,
            "contribution_to_total": 1.2714728412446377e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0005246589716684155
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.0005544133301410981,
            "contribution_to_total": 4.991816772587246e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -3.0870699563277425e-05,
            "contribution_to_total": -4.193840524304622e-06,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00030030030030030023
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.00013712887394926615,
            "contribution_to_total": -0.00011726498923008094,
            "DeltaMRR_positive_anchor_full_negative_population": 5.260324916813448e-05
          }
        },
        "GMG_vs_GMS": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0004746198446938885,
            "contribution_to_total": -0.0004270415918252064,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0024565790015228218
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.016810223164243018,
            "contribution_to_total": 0.0008702043064006667,
            "DeltaMRR_positive_anchor_full_negative_population": -0.000900900900900901
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.02258994503128986,
            "contribution_to_total": 0.0010951288462822315,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0034748546878948703
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0004746198446938885,
            "contribution_to_total": -0.0004270415918252064,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0024565790015228218
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.02641298042251781,
            "contribution_to_total": 0.0008990493594049384,
            "DeltaMRR_positive_anchor_full_negative_population": -0.023333333333333334
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.038065325897535175,
            "contribution_to_total": 0.0008433331399423837,
            "DeltaMRR_positive_anchor_full_negative_population": -0.012430939226519336
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.005061088587133844,
            "contribution_to_total": 0.00022295065333557634,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0010473946059177798
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.0004746198446938885,
            "contribution_to_total": -0.0004270415918252064,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0024565790015228218
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.02049651466785916,
            "contribution_to_total": 0.0009685369553597708,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00432900432900433
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.027903396524252777,
            "contribution_to_total": 0.0007183313786327752,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0002099076406381196
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.010219746689727313,
            "contribution_to_total": 0.0002784648186903523,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004197271773347324
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.0038234515716020936,
            "contribution_to_total": 3.4425524507935304e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0007209763806952018,
            "contribution_to_total": 9.794594891600194e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0033033033033033035
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0016440733054106597,
            "contribution_to_total": 0.0014059200874337546,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0012567982272180748
          }
        },
        "GMG_vs_GMP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0003974223818006926,
            "contribution_to_total": 0.00035758278641002234,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0017556179775280898
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.00571328186681538,
            "contribution_to_total": -0.00029575588828344184,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0072072072072072065
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.010973571444340179,
            "contribution_to_total": 0.0005319833500608441,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001263583522870862
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0003974223818006926,
            "contribution_to_total": 0.00035758278641002234,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0017556179775280898
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.0029241922693384018,
            "contribution_to_total": 9.953413603730506e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0033333333333333335
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.008399936088322839,
            "contribution_to_total": 0.00018609966707626023,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0009208103130755066
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.0011215480489852087,
            "contribution_to_total": -4.940634133616292e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.0003974223818006926,
            "contribution_to_total": 0.00035758278641002234,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0017556179775280898
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.00556445198445642,
            "contribution_to_total": -0.00026294116197824623,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0021645021645021645
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.005615951109672831,
            "contribution_to_total": 0.00014457429580084344,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0033585222502099076
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.013013723695350797,
            "contribution_to_total": 0.0003545943279548051,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002098635886673662
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.0009675897456761691,
            "contribution_to_total": 8.711967153135527e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.01851851851851852
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.00021906189935965096,
            "contribution_to_total": 2.9759956329545154e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0007507507507507511
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0006494088272009038,
            "contribution_to_total": 0.0005553383247047439,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00031806615776081416
          }
        },
        "GMG_vs_GDUP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.002392302997078408,
            "contribution_to_total": 0.0021524866509942844,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0014903245942571783
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.0011099356034175152,
            "contribution_to_total": 5.745734202838221e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006306306306306307
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": -0.03361097798332107,
            "contribution_to_total": -0.0016294130636576487,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004864796563052818
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.002392302997078408,
            "contribution_to_total": 0.0021524866509942844,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0014903245942571783
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.0079553232524328,
            "contribution_to_total": 0.00027078459755573226,
            "DeltaMRR_positive_anchor_full_negative_population": -0.01
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": -0.020904505140877515,
            "contribution_to_total": -0.00046313702940185483,
            "DeltaMRR_positive_anchor_full_negative_population": -3.066914432666178e-19
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": -0.0313176676552919,
            "contribution_to_total": -0.0013796032897831442,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004516889238020424
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": 0.002392302997078408,
            "contribution_to_total": 0.0021524866509942844,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0014903245942571783
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.005828332010356818,
            "contribution_to_total": 0.00027541047986020807,
            "DeltaMRR_positive_anchor_full_negative_population": -0.010822510822510824
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": -0.032564758040121954,
            "contribution_to_total": -0.0008383311872972773,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0060873215785054585
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": -0.037031903328429094,
            "contribution_to_total": -0.0010090350141921973,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00472193074501574
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.0015262685709123039,
            "contribution_to_total": 1.374218951375828e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": -0.00045044291227206476,
            "contribution_to_total": -6.11934865777891e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0037537537537537533
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0007343581075286395,
            "contribution_to_total": 0.0006279822264290487,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0021973070398642915
          }
        },
        "GDUP_vs_GM": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.00040994089090189785,
            "contribution_to_total": -0.00036884637792146646,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00020158524372007516
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.0011092798636315193,
            "contribution_to_total": -5.7423396757098376e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.013513513513513514
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.018505678017473604,
            "contribution_to_total": 0.0008971293108006801,
            "DeltaMRR_positive_anchor_full_negative_population": -0.001389941875157948
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.00040994089090189785,
            "contribution_to_total": -0.00036884637792146646,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00020158524372007516
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.0015589166060159467,
            "contribution_to_total": 5.3062659101110096e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006666666666666666
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.018711222609621454,
            "contribution_to_total": 0.0004145450943467363,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0055248618784530384
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.008446809756821045,
            "contribution_to_total": 0.00037209816059573535,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0005236973029588898
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.00040994089090189785,
            "contribution_to_total": -0.00036884637792146646,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00020158524372007516
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.0033393907126277778,
            "contribution_to_total": -0.00015779869728959267,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00974025974025974
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.018702473952137248,
            "contribution_to_total": 0.0004814673327028628,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0029387069689336687
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.01893873091351749,
            "contribution_to_total": 0.0005160372786303115,
            "DeltaMRR_positive_anchor_full_negative_population": -0.002098635886673662
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.0013853386866073516,
            "contribution_to_total": -1.247328755562318e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0006371539270953968,
            "contribution_to_total": 8.655851656990498e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.008258258258258258
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.00046398515279733976,
            "contribution_to_total": 0.00039677430710783343,
            "DeltaMRR_positive_anchor_full_negative_population": -5.0797379041653935e-05
          }
        },
        "GDUP_vs_GMH": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.003955516817208603,
            "contribution_to_total": -0.0035589961460663014,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004173268990684721
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.007397897129411649,
            "contribution_to_total": 0.00038296231272031686,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005405405405405406
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.051136708432419,
            "contribution_to_total": 0.0024790358909991678,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00612838008592368
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.003955516817208603,
            "contribution_to_total": -0.0035589961460663014,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004173268990684721
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.01689520903459499,
            "contribution_to_total": 0.0005750818959686795,
            "DeltaMRR_positive_anchor_full_negative_population": -0.013333333333333334
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.05017244442868294,
            "contribution_to_total": 0.0011115650293530195,
            "DeltaMRR_positive_anchor_full_negative_population": -0.007366482504604053
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.026681047361716757,
            "contribution_to_total": 0.0011753512783977856,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003993191935061535
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.003955516817208603,
            "contribution_to_total": -0.0035589961460663014,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004173268990684721
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.01100801726611358,
            "contribution_to_total": 0.0005201699752489205,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006493506493506494
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.05127810719387018,
            "contribution_to_total": 0.0013200784858659203,
            "DeltaMRR_positive_anchor_full_negative_population": -0.007766582703610411
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.037498537872121214,
            "contribution_to_total": 0.0010217497426046438,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005246589716684155
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.000971855240771206,
            "contribution_to_total": -8.750372741171036e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0004195722127087874,
            "contribution_to_total": 5.699964605348448e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003453453453453453
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0008714869814779058,
            "contribution_to_total": -0.0007452472156591296,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0021447037906961574
          }
        },
        "GDUP_vs_GMS": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.002866922841772297,
            "contribution_to_total": -0.0025795282428194913,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00394690359578
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": 0.015700287560825504,
            "contribution_to_total": 0.0008127469643722847,
            "DeltaMRR_positive_anchor_full_negative_population": 0.005405405405405406
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.05620092301461094,
            "contribution_to_total": 0.0027245419099398804,
            "DeltaMRR_positive_anchor_full_negative_population": -0.008339651250947688
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.002866922841772297,
            "contribution_to_total": -0.0025795282428194913,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00394690359578
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": 0.01845765717008501,
            "contribution_to_total": 0.0006282647618492061,
            "DeltaMRR_positive_anchor_full_negative_population": -0.013333333333333334
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.05896983103841269,
            "contribution_to_total": 0.0013064701693442386,
            "DeltaMRR_positive_anchor_full_negative_population": -0.012430939226519336
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.036378756242425744,
            "contribution_to_total": 0.0016025539431187205,
            "DeltaMRR_positive_anchor_full_negative_population": -0.005564283843938204
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.002866922841772297,
            "contribution_to_total": -0.0025795282428194913,
            "DeltaMRR_positive_anchor_full_negative_population": 0.00394690359578
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": 0.014668182657502343,
            "contribution_to_total": 0.0006931264754995628,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006493506493506494
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.06046815456437474,
            "contribution_to_total": 0.0015566625659300527,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006297229219143577
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.04725165001815641,
            "contribution_to_total": 0.0012874998328825497,
            "DeltaMRR_positive_anchor_full_negative_population": -0.008919202518363064
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": 0.0022971830006897898,
            "contribution_to_total": 2.0683334994177023e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0011714192929672667,
            "contribution_to_total": 0.00015913943549379105,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0004504504504504496
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": 0.0009097151978820204,
            "contribution_to_total": 0.000777937861004706,
            "DeltaMRR_positive_anchor_full_negative_population": -0.003454105267082367
          }
        },
        "GDUP_vs_GMP": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.001994880615277715,
            "contribution_to_total": -0.001794903864584262,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003245942571785268
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.0068232174702328955,
            "contribution_to_total": -0.0003532132303118241,
            "DeltaMRR_positive_anchor_full_negative_population": 0.013513513513513514
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.04458454942766126,
            "contribution_to_total": 0.0021613964137184934,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00612838008592368
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.001994880615277715,
            "contribution_to_total": -0.001794903864584262,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003245942571785268
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.005031130983094398,
            "contribution_to_total": -0.00017125046151842717,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006666666666666666
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.029304441229200354,
            "contribution_to_total": 0.0006492366964781152,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0009208103130755063
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.030196119606306686,
            "contribution_to_total": 0.001330196948446981,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004516889238020424
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.001994880615277715,
            "contribution_to_total": -0.001794903864584262,
            "DeltaMRR_positive_anchor_full_negative_population": 0.003245942571785268
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.011392783994813237,
            "contribution_to_total": -0.0005383516418384543,
            "DeltaMRR_positive_anchor_full_negative_population": 0.012987012987012988
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.03818070914979479,
            "contribution_to_total": 0.0009829054830981208,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0027287993282955505
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.05004562702377989,
            "contribution_to_total": 0.0013636293421470025,
            "DeltaMRR_positive_anchor_full_negative_population": -0.006820566631689402
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.0005586788252361347,
            "contribution_to_total": -5.030222360622753e-06,
            "DeltaMRR_positive_anchor_full_negative_population": 0.01851851851851852
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.0006695048116317158,
            "contribution_to_total": 9.095344290733427e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.004504504504504504
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -8.494928032773568e-05,
            "contribution_to_total": -7.264390172430464e-05,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0018792408821034776
          }
        },
        "GDUP_vs_GMG": {
          "H0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.002392302997078408,
            "contribution_to_total": -0.0021524866509942844,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0014903245942571783
          },
          "H1": {
            "candidate_count": 2409,
            "positive_count": 185,
            "negative_count": 2224,
            "mean_DeltaCE": -0.0011099356034175152,
            "contribution_to_total": -5.745734202838221e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.006306306306306307
          },
          "H2plus": {
            "candidate_count": 2256,
            "positive_count": 1319,
            "negative_count": 937,
            "mean_DeltaCE": 0.03361097798332107,
            "contribution_to_total": 0.0016294130636576487,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004864796563052818
          },
          "G0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.002392302997078408,
            "contribution_to_total": -0.0021524866509942844,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0014903245942571783
          },
          "G1": {
            "candidate_count": 1584,
            "positive_count": 50,
            "negative_count": 1534,
            "mean_DeltaCE": -0.0079553232524328,
            "contribution_to_total": -0.00027078459755573226,
            "DeltaMRR_positive_anchor_full_negative_population": 0.01
          },
          "G2to3": {
            "candidate_count": 1031,
            "positive_count": 181,
            "negative_count": 850,
            "mean_DeltaCE": 0.020904505140877515,
            "contribution_to_total": 0.00046313702940185483,
            "DeltaMRR_positive_anchor_full_negative_population": 3.066914432666178e-19
          },
          "G4plus": {
            "candidate_count": 2050,
            "positive_count": 1273,
            "negative_count": 777,
            "mean_DeltaCE": 0.0313176676552919,
            "contribution_to_total": 0.0013796032897831442,
            "DeltaMRR_positive_anchor_full_negative_population": -0.004516889238020424
          },
          "MULT0": {
            "candidate_count": 41871,
            "positive_count": 712,
            "negative_count": 41159,
            "mean_DeltaCE": -0.002392302997078408,
            "contribution_to_total": -0.0021524866509942844,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0014903245942571783
          },
          "MULT1to3": {
            "candidate_count": 2199,
            "positive_count": 154,
            "negative_count": 2045,
            "mean_DeltaCE": -0.005828332010356818,
            "contribution_to_total": -0.00027541047986020807,
            "DeltaMRR_positive_anchor_full_negative_population": 0.010822510822510824
          },
          "MULT4to15": {
            "candidate_count": 1198,
            "positive_count": 397,
            "negative_count": 801,
            "mean_DeltaCE": 0.032564758040121954,
            "contribution_to_total": 0.0008383311872972773,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0060873215785054585
          },
          "MULT16plus": {
            "candidate_count": 1268,
            "positive_count": 953,
            "negative_count": 315,
            "mean_DeltaCE": 0.037031903328429094,
            "contribution_to_total": 0.0010090350141921973,
            "DeltaMRR_positive_anchor_full_negative_population": -0.00472193074501574
          },
          "degree0to3": {
            "candidate_count": 419,
            "positive_count": 9,
            "negative_count": 410,
            "mean_DeltaCE": -0.0015262685709123039,
            "contribution_to_total": -1.374218951375828e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0
          },
          "degree4to15": {
            "candidate_count": 6322,
            "positive_count": 111,
            "negative_count": 6211,
            "mean_DeltaCE": 0.00045044291227206476,
            "contribution_to_total": 6.11934865777891e-05,
            "DeltaMRR_positive_anchor_full_negative_population": 0.0037537537537537533
          },
          "degree16plus": {
            "candidate_count": 39795,
            "positive_count": 2096,
            "negative_count": 37699,
            "mean_DeltaCE": -0.0007343581075286395,
            "contribution_to_total": -0.0006279822264290487,
            "DeltaMRR_positive_anchor_full_negative_population": -0.0021973070398642915
          }
        }
      },
      "per_candidate_directory": "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HDP_ZERO_V29/retrospective/pubmed/seed_2"
    }
  ],
  "test_opened": false
}
