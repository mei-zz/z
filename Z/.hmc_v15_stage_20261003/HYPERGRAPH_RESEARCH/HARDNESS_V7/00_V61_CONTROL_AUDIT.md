# V6.1 A1/A3 strict control audit

- Reproduced: True; fixed epoch 10 validation A1=0.454154, A3=0.470656, delta=+0.016502.
- Split hash: c5cec7e3bf6eaad41e12ae786246bf454a1bbcd4476286c71eb7e75b0eeba71a; pool hash: 3d1e3ea691fc19fab65d66ad278d169cf099eb831ad0e46a439510ff5d07a7ba; validation candidate hash: aca455fc094f2b037a812d62a4fcb79fd8d48102d021d72418aea1ab0b65b455.
- Teacher state hashes: Graph 30343bdf61b8fa38a7d9eecbd280a836ee81ef4dfeb63efeb1c74445337ad28b; Raw-HG 1fa029f5a0a3a6e32516907e28bd6179493eeb5429f69c97e4444acdaa9fe91e.
- All six selection hashes match V6.1 state. Checkpoint file hashes are recorded in results.json. Sampler uses only frozen train positives and the 20-candidate pool.
- V6.1 nominal veto=0.25, but it removes 1 of 2 candidates per positive (50% realized prepool trim); this is recorded for QTHS calibration.
