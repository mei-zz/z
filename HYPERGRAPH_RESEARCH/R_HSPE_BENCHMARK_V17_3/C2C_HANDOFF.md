STATUS: EXECUTED
DIRECTION: R_HSPE_PUBLICATION_BENCHMARK
R_HSPE: FROZEN
{
  "ranks": {
    "cora": {
      "NCN": 1,
      "NCNC": 2,
      "C1_COUNT_PARAM_MATCHED": 3,
      "R-HSPE": 4,
      "B0_BASELINE": 5,
      "NSLR-HMANN": 6
    },
    "pubmed": {
      "NCNC": 1,
      "NCN": 2,
      "C2_CONSTANT_SET": 3,
      "R-HSPE": 4,
      "B0_BASELINE": 5,
      "NSLR-HMANN": 6
    },
    "citeseer": {
      "NCNC": 1,
      "NCN": 2,
      "R-HSPE": 3,
      "B0_BASELINE": 4,
      "NSLR-HMANN": 5
    }
  },
  "effects": {
    "cora": {
      "strongest": "NCN",
      "shared_seed_labels": [
        0,
        1,
        2,
        3,
        4
      ],
      "deltas": [
        -0.2056700638187352,
        -0.39795196668481975,
        -0.20677369586038297,
        -0.20221640627965332,
        -0.17764536905043948
      ],
      "mean": -0.23805150033880612,
      "median": -0.2056700638187352,
      "wins": 0,
      "strict_paired_rng_test": false,
      "mean_gap_all_seeds": -0.2380515003388063
    },
    "pubmed": {
      "strongest": "NCNC",
      "shared_seed_labels": [
        0,
        1,
        2,
        3,
        4
      ],
      "deltas": [
        -0.07527942169227819,
        -0.11938589937346178,
        -0.0727590974499539,
        -0.0771672408518077,
        -0.060555530760855625
      ],
      "mean": -0.08102943802567145,
      "median": -0.07527942169227819,
      "wins": 0,
      "strict_paired_rng_test": false,
      "mean_gap_all_seeds": -0.08102943802567131
    },
    "citeseer": {
      "strongest": "NCNC",
      "shared_seed_labels": [
        0,
        1,
        2
      ],
      "deltas": [
        -0.339515393721072,
        -0.29082270021907,
        -0.43847992896436483
      ],
      "mean": -0.3562726743015023,
      "median": -0.339515393721072,
      "wins": 0,
      "strict_paired_rng_test": false,
      "mean_gap_all_seeds": -0.3585538904398613
    }
  },
  "COMPETITIVENESS": "WEAK",
  "PAPER_READY_INNOVATION_1": "NO"
}
NEXT_EXPECTED_STEP: retrieve results; no Innovation2 launch
