# First divergence

Two fresh, unpatched PubMed seed0 RAW/A2 executions started from identical model and optimizer initialization, with identical first optimizer-batch input hashes. Their first-batch forward logits and loss hashes matched. The first different activation was the output of `torch_scatter.scatter_mean` in endpoint pooling; token latent and group-count hashes matched. The first different gradient and updated parameter were `decoder.4.weight`.

This is the earliest divergence reproducible from available sources: epoch 1, optimizer batch 1, first endpoint pooling. The historical V18 run did not save per-step state, so its exact first divergent step cannot be reconstructed. The V18.1 mismatch report first showed a visible heldout score discrepancy for PubMed A2 by epoch 2; that is a later symptom, not the kernel’s first divergence.

See `04_DIVERGENCE_EVIDENCE.json` and the two retained `pubmed_seed0_A2_unpatched_run*_first_step.json` traces.
