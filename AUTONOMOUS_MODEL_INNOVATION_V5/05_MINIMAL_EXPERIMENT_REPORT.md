# DCDLP V5 — Minimal Experiment Report

## Status

```text
NOT_EXECUTED
```

No Cora training, no new checkpoint, no new raw JSON, and no GPU run was performed in V5.

## Reason for non-execution

The only V4 candidate, T2WL-INC, was stopped by a direct paper/formula/source-code collision with 2-FWL and Local 2-FWL before implementation. The three post-collision candidates produced no `ELIGIBLE_FOR_MINIMAL_TEST` status: ONTM is a HOLD problem shift requiring a temporal benchmark; PTALP is a direct TMetaNet collision; EAPU-LP is an established PU formulation with no observable exposure variable in Cora HeaRT.

Running a GPU experiment after this gate would measure an implementation choice, not test a novel mechanism, and would violate the V5 stop rule.

## Experiment fields intentionally empty

| Field | V5 value |
|---|---|
| dataset | NOT APPLICABLE |
| seeds | NOT APPLICABLE |
| validation MRR | NOT APPLICABLE |
| Hits@10/20/50/100 | NOT APPLICABLE |
| AUC/AP | NOT APPLICABLE |
| Parent/control models | NOT APPLICABLE |
| checkpoint | NONE CREATED |
| parameter count | NOT APPLICABLE |
| runtime/peak GPU memory | NOT APPLICABLE |
| new script/raw log | NONE CREATED |
| test selection | NOT USED |

The complete historical Cora A–E results remain in `AUTONOMOUS_MODEL_INNOVATION_V4/raw/mechanism_cora_v4run3/` and are not copied or recomputed here. They remain the evidence for terminating CDPT, not evidence for T2WL-INC.

