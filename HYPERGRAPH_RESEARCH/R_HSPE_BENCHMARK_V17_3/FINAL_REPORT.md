# V17.3 benchmark report

STATUS: COMPLETE
R_HSPE_FROZEN: TRUE
FAIR_BASELINE_BENCHMARK: COMPLETE
COMPLETED_JOBS: 45/45
COMPETITIVENESS: WEAK
PAPER_READY_INNOVATION_1: NO
INNOVATION_1_METHOD_VALIDATED: YES
TEST_GENERALIZATION: YES
THIRD_DATASET: YES
NO_EXACT_COLLISION_IN_FOCUSED_AUDIT: YES (limited audit, no priority proof)

## Dataset rankings

CORA_R_HSPE: {'mean': 0.6100535476808527, 'std': 0.0839628360024447, 'median': 0.6404792356904612, 'min': 0.46163354057620926, 'max': 0.6692092916799328, 'per_seed': [0.6367877550859528, 0.46163354057620926, 0.6404792356904612, 0.6421579153717081, 0.6692092916799328]}
BEST_ON_CORA: NCN
R_HSPE_RANK_CORA: 4
PUBMED_R_HSPE: {'mean': 0.8560636614766113, 'std': 0.02190243205516568, 'median': 0.8606890660474189, 'min': 0.8182941583596195, 'max': 0.8743531958164178, 'per_seed': [0.8606890660474189, 0.8182941583596195, 0.8671034414226255, 0.8598784457369747, 0.8743531958164178]}
BEST_ON_PUBMED: NCNC
R_HSPE_RANK_PUBMED: 4
CITESEER_R_HSPE: {'mean': 0.5273195932193366, 'std': 0.07174903286223369, 'median': 0.5432250404479336, 'min': 0.44895247989661546, 'max': 0.5897812593134609, 'per_seed': [0.5432250404479336, 0.5897812593134609, 0.44895247989661546]}
BEST_ON_CITESEER: NCNC
R_HSPE_RANK_CITESEER: 3

## Coverage

NSLR-HMANN: cora 5/5 seeds; pubmed 5/5 seeds; citeseer 5/5 seeds
NCN: cora 5/5 seeds; pubmed 5/5 seeds; citeseer 5/5 seeds
NCNC: cora 5/5 seeds; pubmed 5/5 seeds; citeseer 5/5 seeds
HMNE: REFERENCE_ONLY / NO_VERIFIED_IMPLEMENTATION
HMRLH: REFERENCE_ONLY / NO_VERIFIED_IMPLEMENTATION
CCLPH: REFERENCE_ONLY / NO_VERIFIED_COMPLETE_IMPLEMENTATION; pairwise scoring is supported in paper, not categorically TASK_MISMATCH
DIRECTLY_COMPARABLE_METHODS: B0_BASELINE, C1_COUNT_PARAM_MATCHED, C2_CONSTANT_SET, NCN, NCNC, NSLR-HMANN, R-HSPE
REFERENCE_ONLY_METHODS: HMNE, HMRLH, CCLPH, Tier C
PARAMETER_EFFICIENCY: R-HSPE adds 75 parameters; absolute totals and measured baseline costs in CSV; frozen training timing unavailable is NA, not zero.
NOVELTY_STATUS: context-driven candidate-specific hyperedge-pair residual; no size-causality or first-ever claim.
NEXT_EXPECTED_STEP: retrieve completed benchmark and decide paper positioning; keep Innovation1 frozen; do not start Innovation2.

## Failures
[]

## Effect sizes
{
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
}

## Decision limits
Competition thresholds fixed before third-party test access: third-dataset lag/strong-range threshold 0.02 absolute MRR, descriptive only. Different model RNGs do not justify a paired significance test. Rankings cover only rerun methods. Frozen Citeseer has 3 seeds. Missing reference-only original numeric scores remain NOT_VERIFIED, never fabricated.
