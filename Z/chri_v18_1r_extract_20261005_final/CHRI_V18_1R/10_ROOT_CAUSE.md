# Root cause

**Primary classification: `NUMERICAL_KERNEL_NONDETERMINISM`.** CUDA `torch_scatter.scatter_mean` atomically accumulates floating-point rows for repeated endpoint group IDs. Two isolated executions with identical initialization and first-batch inputs produced different pooled output hashes. The first different gradient and updated parameter was `decoder.4.weight`; logits/loss still matched on that first batch because the final decoder layer starts at zero. The small first-step difference then compounds through Adam over epochs. Strict `torch.use_deterministic_algorithms(True)` alone did not control the third-party scatter kernel.

The fixed-checkpoint evaluation drift is at most the score difference documented in `02_CHECKPOINT_EVAL_REPEATABILITY.json`, with CE movement around the last decimal places. It is far too small to explain PubMed training divergence, which reaches max score differences above 0.1 by epoch 5.

PubMed is larger (37,676 train pairs vs 4,488 on Cora) and its audited 256-candidate batch has 2.57x as many endpoint-pair interactions. Cora also exhibits the same first-step scatter nondeterminism; its historical one-off reproduction stayed within the former gate.

V18 did not save per-step/epoch model and optimizer hashes or its full runtime environment. The historical state sequence therefore cannot be fabricated or exactly reconstructed. The root cause is identified, and a new deterministic V18R canonical execution is available.
