# Tail size shuffle and reverse controls

Seeds0/1/2 primary validation, fixed epoch10. TS-SHUFFLE permutation seed=101000+training seed. TS-REVERSE stable tail-sort, reverse assignment. Both preserve exact tail multiset; sorted tie assignment deterministic. LOCAL_PAIRING_SIGNAL requires >=2/3 wins and mean>.002.

```json
{
  "mrr_by_seed": {
    "CPTS": [
      0.4949009749656315,
      0.5304590361478907,
      0.5857761687759687,
      0.5971012419306395,
      0.3714693154658604
    ],
    "MATCHED_Q": [
      0.49986704468731924,
      0.5151139076719425,
      0.5693080400354765,
      0.5767171614369639,
      0.37963664704473893
    ],
    "TS_SHUFFLE": [
      0.49891294748576764,
      0.48723121124311836,
      0.5713653487222041,
      0.5712819800751973,
      0.41515204214691553
    ],
    "TS_REVERSE": [
      0.5025095357306448,
      0.5058113351128867,
      0.575973063858295
    ]
  },
  "CPTS_vs_TS_SHUFFLE_3seed": {
    "seed_deltas": [
      -0.004011972520136131,
      0.04322782490477234,
      0.014410820053764595
    ],
    "mean_delta": 0.017875557479466935,
    "wins": 2,
    "n": 3,
    "paired_bootstrap_95pct_ci": [
      -0.004011972520136131,
      0.04322782490477234
    ],
    "bootstrap_draws": 20000,
    "bootstrap_seed": 1012026
  },
  "CPTS_vs_TS_REVERSE_3seed": {
    "seed_deltas": [
      -0.007608560765013317,
      0.02464770103500402,
      0.009803104917673666
    ],
    "mean_delta": 0.00894741506255479,
    "wins": 2,
    "n": 3,
    "paired_bootstrap_95pct_ci": [
      -0.007608560765013317,
      0.02464770103500402
    ],
    "bootstrap_draws": 20000,
    "bootstrap_seed": 1012026
  },
  "CPTS_vs_MATCHED_Q": {
    "seed_deltas": [
      -0.004966069721687727,
      0.015345128475948155,
      0.016468128740492194,
      0.02038408049367557,
      -0.008167331578878556
    ],
    "mean_delta": 0.007812787281909928,
    "wins": 3,
    "n": 5,
    "paired_bootstrap_95pct_ci": [
      -0.0025999871435662403,
      0.017809909388856737
    ],
    "bootstrap_draws": 20000,
    "bootstrap_seed": 1012026
  },
  "CPTS_vs_TS_SHUFFLE": {
    "seed_deltas": [
      -0.004011972520136131,
      0.04322782490477234,
      0.014410820053764595,
      0.025819261855442255,
      -0.04368272668105516
    ],
    "mean_delta": 0.007152641522557579,
    "wins": 3,
    "n": 5,
    "paired_bootstrap_95pct_ci": [
      -0.020445307987127258,
      0.030500998714838756
    ],
    "bootstrap_draws": 20000,
    "bootstrap_seed": 1012026
  },
  "LOCAL_PAIRING_SIGNAL": true
}
```
