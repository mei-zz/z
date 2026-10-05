# Experiment Ledger

## Fixed budget and execution policy

| Item | Fixed rule | Actual use |
|---|---|---|
| Problem scenes | At most three | A, B, C audited; only C executable |
| Candidates per scene | At most two | One rejected C candidate, no implementation |
| Core modifications | At most one per candidate | Zero |
| Training seeds | Seed 0 smoke, then 0–2 if candidate passes | Parent seeds 0–2; no new candidate training |
| Decision metric | Validation MRR/Hits; no test selection | Validation used for comparison; test reported descriptively |
| Compute environment | `.env` remote server, `mei_env` | Satisfied for all training and proxy runs |

## Remote commands actually executed

The Parent command was:

```bash
cd /home/ubuntu/DCDLP-main
source /home/ubuntu/anaconda3/etc/profile.d/conda.sh
conda activate mei_env
PYTHONPATH=src python -m dcdlp.cli train \
  --dataset cora --protocol heart --seed {0,1,2} --data-root data \
  --protocol-train uniform --pretrain-epochs 2 --disentangle-epochs 2 \
  --hidden-dim 64 --branch-dim 32 --batch-size 512 --device cuda:0 \
  --ablation A5 --output-dir /home/ubuntu/AFDR_V6/raw/cora_heart_baselines
```

The heuristic evaluator and validation evaluator were uploaded to the remote AFDR workspace and ran under `PYTHONPATH=/home/ubuntu/DCDLP-main/src:/home/ubuntu/AFDR_V6`. Their source copies are preserved in [`scripts`](scripts).

## Raw outputs

- Parent seed 0: [`cora_uniform_seed0_1fd9a2af2220.json`](raw/cora_heart_baselines/cora_uniform_seed0_1fd9a2af2220.json)
- Parent seed 1: [`cora_uniform_seed1_9eb82149c1c2.json`](raw/cora_heart_baselines/cora_uniform_seed1_9eb82149c1c2.json)
- Parent seed 2: [`cora_uniform_seed2_4025c6b12162.json`](raw/cora_heart_baselines/cora_uniform_seed2_4025c6b12162.json)
- Parent validation evaluations: [`valid_seed0.json`](raw/cora_heart_baselines/valid_seed0.json), [`valid_seed1.json`](raw/cora_heart_baselines/valid_seed1.json), [`valid_seed2.json`](raw/cora_heart_baselines/valid_seed2.json)
- Fixed heuristic evaluation: [`heuristics.json`](raw/cora_heart_baselines/heuristics.json)

## Resource and reproducibility notes

- Remote device: one Tesla V100 16 GB; CUDA was available.
- Parent total/trainable parameters: 112,486.
- Parent peak GPU memory: 55.46 MB in the recorded runs.
- Parent training wall time: 95.76–98.65 seconds per seed.
- Official candidate and split hashes are recorded in `BASELINE_FAILURE_EVIDENCE.md` and each raw JSON.
- The original remote project has no Git commit; historical source hashes are retained in V1–V6 reports. No V1–V6 file was overwritten.

## Not-run records

- PULL/CORE-compatible incomplete/noisy benchmark: not run because the required public data/code was not available in the remote workspace; this is not a negative model result.
- Inductive/new-node benchmark: not run because no fixed public inductive split was available in the remote workspace; NCN’s available Planetoid loader is a different random split.
- NCN/SEAL under Cora HeaRT: not run because the available official NCN loader does not consume the fixed HeaRT grouped candidates. Comparing its native Cora result to HeaRT would be invalid.
