# Experiment Ledger — V2

The following runs are retained as raw JSON under the attempt directories.

## Locked protocols

- Parent and candidate use the same data artifact, split, negative candidates, seed, epochs, batch size, backbone, hidden/branch dimensions, optimizer, and early-selection rule.
- Test candidates are not used for idea selection. The official test ranking is read only after the candidate is locked for the stage.
- Primary metrics: MRR, Hits@10, Hits@20, Hits@50, Hits@100. AUC/AP are diagnostics only.
- Required controls: shuffled structural transport where applicable; a simple proxy; parameter-count and randomized-path controls when feasible.
- Stage 2 kill rule: mean ΔMRR must be positive, seed-wise behavior must not show ranking collapse, and Hits must not be systematically lower.
- Stage 3 promising rule: mean ΔMRR > 0, at least 2/3 seeds improve MRR, and Hits are not systematically down.

## Runs

| Attempt | Candidate | Stage | Dataset/seed(s) | Parent | Candidate | Controls | Status |
|---|---|---|---|---|---|---|---|
| 001 | V2-001 PCDT | Stage 0 | Cora HeaRT seed 0, 8192 candidates | 112,486 params; 43.22 MB peak | 177,512 params; 631.13 MB peak | exact parent equivalence at scale 0; exchange error 0 | PASS |
| 001 | V2-001 PCDT | Stage 1 | Cora HeaRT seed 0, 2 epochs | MRR 0.09491 | MRR 0.11374 | shuffled-eval MRR 0.12120; CN proxy 0.09777 | STOP: aligned path lost shuffled control |
| 002 | V2-002 CDPT | Stage 0 | Cora HeaRT seed 0, 8192 candidates | 112,486 params; 42.99 MB peak | 119,751 params; 46.75 MB peak | exact parent equivalence at scale 0; exchange error 0 | PASS |
| 002 | V2-002 CDPT | Stage 1 | Cora HeaRT seed 0, 2 epochs | MRR 0.09491 | MRR 0.10299 | shuffled-eval MRR 0.09247; CN proxy 0.09777 | PASS |
| 002 | V2-002 CDPT | Stage 2 | Cora HeaRT seed 0, 4 epochs | MRR 0.09987 | MRR 0.10787 | trained shuffled MRR 0.10756; CN proxy 0.09777 | PASS |
| 002 | V2-002 CDPT | Stage 3 | Cora HeaRT seeds 0--2, 4 epochs | ΔMRR: +0.00800, -0.00565, +0.02385 | mean ΔMRR +0.00873; 2/3 improved | mean ΔHits10/20/50/100: +0.02277/+0.02720/+0.03605/+0.02910 | FOUND_PROMISING_INNOVATION |
