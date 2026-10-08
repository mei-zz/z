# Locked reproduction and environment

- Status: **PASS**.
- Runtime: `{"python": "3.11.11", "torch": "2.3.1+cu121", "torch_cuda_build": "12.1", "cuda_available": true, "gpu": "Tesla V100-PCIE-16GB", "pyg": "2.5.3", "numpy": "1.26.4", "protocol": "STRICT_TRAIN_ONLY", "checkpoint_rule": "FIXED_EPOCH_10", "environment_route": "LOCKED_TORCH_2_3_1_CUDA_12_1", "environment_repro_blocked": false}`.
- Environment route: `LOCKED_TORCH_2_3_1_CUDA_12_1`; `ENVIRONMENT_REPRO_BLOCKED=False`. Existing `mei_env` was left unchanged. The new venv isolates PyTorch/CUDA wheels; other shared base packages are read-only site packages from Python 3.11.11.
- The project environment file requests Python 3.10; this dedicated run retained the available Python 3.11.11 ABI and reports that mismatch rather than changing the active environment.
- Locked rule: STRICT_TRAIN_ONLY; training-pool exclusions use train positives/message edges only; 20 fixed candidate rows per train positive; one sampled negative per positive per epoch; exactly 10 epochs; final epoch checkpoint; fixed Graph teacher, decoder, optimizer and hidden dimensions; no validation-best checkpoint and no test-guided changes.
- Cora split hash: `c5cec7e3bf6eaad41e12ae786246bf454a1bbcd4476286c71eb7e75b0eeba71a`; train positive hash: `fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8`; candidate-pool hash: `3d1e3ea691fc19fab65d66ad278d169cf099eb831ad0e46a439510ff5d07a7ba`; validation candidate hash: `aca455fc094f2b037a812d62a4fcb79fd8d48102d021d72418aea1ab0b65b455`.
- Frozen teacher state hash: `30343bdf61b8fa38a7d9eecbd280a836ee81ef4dfeb63efeb1c74445337ad28b`; cached teacher-score hash: `a1b01e0e2ad5cd287011862d65ade0681205d11ca99dc50cf1b763faf8a82d5c`.
- Cora test candidate hash (opened once after validation freeze): `ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92`.
- Per-seed validation/test MRR, means, sample standard deviations, paired deltas and checkpoint SHA256 values are in `results.json` and `01_CORA_FULL_RESULTS.md`.
