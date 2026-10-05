# Paper claim matrix

Per-positive tail detection claim requires every gate. Reverse signal operationalized as shuffle gate: >=2/3wins and mean>.002. Matched-Q clear failure: mean<-.005 or bootstrap CI wholly negative. Thresholds registered before new tests. Empirical performance does not validate a real extreme-tail regime when null detection>=90%.

```json
{
  "gates": {
    "CPTS_above_Graph_hard": true,
    "five_seed_matched_not_clear_failure": true,
    "local_shuffle_signal": true,
    "reverse_pairing_signal": true,
    "null_detector_discriminative": false,
    "cross_dataset_generalization": true
  },
  "backbone_mechanism_sanity": {
    "gcn": {
      "seed": 0,
      "CPTS": 0.4949009749656315,
      "MATCHED_Q": 0.49986704468731924,
      "delta": -0.004966069721687727
    },
    "sage": {
      "seed": 0,
      "CPTS": 0.4136664581525616,
      "MATCHED_Q": 0.40757199679023365,
      "delta": 0.006094461362327941
    },
    "gat": {
      "seed": 0,
      "CPTS": 0.5428220664581599,
      "MATCHED_Q": 0.5498069221479738,
      "delta": -0.006984855689813885
    }
  },
  "decision": "CHANGE_POINT_DETECTOR_NOT_VALIDATED"
}
```
