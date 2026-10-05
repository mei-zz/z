# V9 Feature–Topology Ablation

## Scope

V9 reuses the two frozen LPShift datasets and hashes from V8. No attention, gate, new loss, wider GNN, or new message-passing rule was added. The purpose is attribution: determine whether DCDLP's behavior requires an independent feature–topology interaction or can be explained by simple feature/topology controls.

### Controls

| ID | Definition | Parameters | Training |
|---|---|---:|---|
| FeatureCosine | deterministic cosine similarity of the original node features | 0 | none |
| TopologyRA | deterministic Resource Allocation score on the message graph | 0 | none |
| FeatureMLP | 2-feature MLP on feature cosine and mean absolute feature difference | 257 | 4 epochs, AdamW |
| TopologyMLP | 8-feature MLP on degree/CN/AA/RA statistics | 641 | 4 epochs, AdamW |
| LinearFusion | one linear logit on all 10 feature/topology statistics | 11 | 4 epochs, AdamW |
| ParamMatchedFusion | `10 → 164 → 164 → 1` MLP on the same 10 statistics | 29,029 | 4 epochs, AdamW |
| DCDLP Parent | original V8 Parent, reused without modification | 28,966 | V8 locked 4 epochs |

The parameter-matched fusion differs from DCDLP by 63 parameters (`+0.217%`). It is a capacity control, not a proposed architecture.

## Metric convention

Every row uses the official average-rank tie rule. Values below are `MRR / Hits@10 / Hits@20 / Hits@50 / Hits@100`, reported as mean ± sample SD over training seeds 1–3. Fixed controls have SD zero because they are deterministic on the frozen message graph and features.

## Setting A: `ogbl-collab_CN_2_1_0_seed1`

| Model | Validation | Frozen test, descriptive only |
|---|---|---|
| DCDLP Parent | `0.5237±.0034 / .7508±.0008 / .8334±.0021 / .9236±.0023 / .9746±.0007` | `0.2352±.0067 / .5847±.0106 / .7246±.0011 / .8709±.0034 / .9586±.0019` |
| FeatureCosine | `.5270±.0000 / .8352±.0000 / .9249±.0000 / .9845±.0000 / .9984±.0000` | `.5384±.0000 / .8469±.0000 / .9286±.0000 / .9851±.0000 / .9979±.0000` |
| TopologyRA | `.4057±.0000 / .4329±.0000 / .4329±.0000 / .4329±.0000 / .4329±.0000` | `.0079±.0000 / .0000±.0000 / .0000±.0000 / .0000±.0000 / .0000±.0000` |
| FeatureMLP | `.5228±.0033 / .8312±.0018 / .9230±.0010 / .9838±.0001 / .9983±.0003` | `.5357±.0025 / .8471±.0001 / .9280±.0004 / .9855±.0004 / .9978±.0001` |
| TopologyMLP | `.1512±.0607 / .2763±.0769 / .4223±.0540 / .6776±.0109 / .8971±.0019` | `.0392±.0011 / .0754±.0052 / .1715±.0264 / .4734±.0019 / .8573±.0017` |
| LinearFusion | `.2393±.1986 / .4184±.3546 / .5142±.4343 / .6060±.4960 / .6773±.5107` | `.2516±.2126 / .4903±.4269 / .5923±.5115 / .6621±.5580 / .6853±.5426` |
| ParamMatchedFusion | `.5149±.0110 / .8271±.0127 / .9342±.0049 / .9898±.0007 / .9990±.0002` | `.2752±.0133 / .7436±.0230 / .9009±.0072 / .9849±.0017 / .9986±.0001` |

Per-seed validation MRR: DCDLP `.5255/.5198/.5258`; FeatureCosine `.5270/.5270/.5270`; FeatureMLP `.5260/.5230/.5193`; TopologyMLP `.1653/.2035/.0847`; LinearFusion `.3005/.4001/.0172`; ParamMatchedFusion `.5177/.5028/.5243`.

## Setting B: `ogbl-collab_CN_4_2_0_seed1`

| Model | Validation | Frozen test, descriptive only |
|---|---|---|
| DCDLP Parent | `.8740±.0048 / .9480±.0180 / .9622±.0154 / .9835±.0069 / .9960±.0013` | `.4118±.0650 / .5824±.1269 / .6953±.1039 / .8684±.0434 / .9664±.0140` |
| FeatureCosine | `.5565±.0000 / .8581±.0000 / .9389±.0000 / .9872±.0000 / .9985±.0000` | `.5428±.0000 / .8568±.0000 / .9374±.0000 / .9864±.0000 / .9987±.0000` |
| TopologyRA | `.8866±.0000 / .9169±.0000 / .9169±.0000 / .9169±.0000 / .9169±.0000` | `.3176±.0000 / .3409±.0000 / .3409±.0000 / .3409±.0000 / .3409±.0000` |
| FeatureMLP | `.5543±.0024 / .8569±.0015 / .9369±.0011 / .9866±.0002 / .9985±.0000` | `.5423±.0014 / .8562±.0012 / .9365±.0003 / .9863±.0002 / .9986±.0000` |
| TopologyMLP | `.4992±.1709 / .7372±.0807 / .8623±.0311 / .9682±.0022 / .9960±.0008` | `.1485±.0463 / .2675±.0416 / .4428±.0196 / .8157±.0144 / .9851±.0053` |
| LinearFusion | `.3036±.2182 / .4704±.3567 / .5667±.4142 / .6784±.4572 / .7399±.4396` | `.2536±.2085 / .4834±.4056 / .5950±.4945 / .6745±.5342 / .7059±.5070` |
| ParamMatchedFusion | `.8070±.0193 / .9580±.0075 / .9862±.0040 / .9983±.0006 / 1.0000±.0000` | `.3935±.0311 / .7684±.0124 / .9229±.0079 / .9952±.0025 / .9999±.0000` |

Per-seed validation MRR: DCDLP `.8795/.8710/.8715`; FeatureCosine `.5565/.5565/.5565`; FeatureMLP `.5561/.5551/.5515`; TopologyMLP `.6002/.5955/.3019`; LinearFusion `.3607/.4875/.0625`; ParamMatchedFusion `.8048/.8273/.7889`.

## Immediate attribution result

- A: the fixed feature-only score already exceeds DCDLP validation MRR and strongly exceeds its frozen test MRR.
- B: the fixed topology-only RA score exceeds DCDLP validation MRR; the parameter-matched fusion is below both RA and DCDLP on validation.
- In neither setting does a parameter-matched feature/topology fusion produce a stable improvement over the strongest simple control.
- The learned linear fusion is highly seed-sensitive, while the deterministic proxies are stable. This is evidence against interpreting a single learned fusion run as a mechanism result.

All per-seed JSONs, traces, prediction files, and logs are retained under `V9/raw/`; the machine-readable aggregate is `V9/raw/v9_results_summary.json`.
