# NHMC V16 — final execution report

**Current V16 validation outcome: Cora Stage 1 passed; PubMed transfer Stage 1 rejected.** All requested Stage 0 diagnostics and both six-arm Stage 1 screens are complete. Test evaluation remained OFF.

## Cora Stage 1

Cora is `NHMC_STAGE1_GO` on validation: H1 MRR 0.593551; B0 0.503991; B1 HRA 0.504136; B2 Native Scalar 0.532451; C1 SIZE 0.590748; C2 SHUFFLE 0.589727. H1 exceeds B0 by 0.089560, B1 by 0.089415, B2 by 0.061099, SIZE by 0.002803, and SHUFFLE by 0.003823. Train shuffle power was 0.453543, making the shuffle gate active. H1 adds 75 parameters (0.3032% of the 24,735-parameter baseline). Seed 0, five epochs; validation only.

Under the Stage 0 diagnostic-only override, Cora is interpreted as `HANDCRAFTED_SUMMARY_INSUFFICIENT_BUT_LEARNED_NHMC_EFFECTIVE` for this dataset and screen.

## Stage 0 diagnostics

No dataset met the original fixed-summary Stage 0 native-signal rule. These results are diagnostic only and did not gate neural Stage 1. Cora had Δnative +0.009334 and Δcontent −0.000097; PubMed had Δnative +0.015535 and Δcontent +0.000304; CiteSeer had Δnative +0.000595 and Δcontent +0.000415. PubMed had 4,976,014 varied native tokens and was used for transfer.

## PubMed transfer Stage 1

PubMed six-arm validation screen is complete with `NHMC_STAGE1_REJECT`. H1 MRR is 0.833945; B0 0.826532; B1 HRA 0.826108; B2 Native Scalar 0.832276; C1 SIZE 0.837051; C2 SHUFFLE 0.838108. H1−B0 is +0.007412 and H1−B1 is +0.007837, but H1−B2 is only +0.001668 (below +0.002), H1−C1 is −0.003106, and H1−C2 is −0.004163 (required +0.002). Train shuffle power is 0.439603, so the strict C2 comparison applied. H1 adds 75 parameters (0.7648% of the 9,807-parameter baseline). Seed 0, five epochs; validation only; test was not evaluated.

The PubMed result does not promote NHMC across datasets. No rescue or fallback run was triggered: PubMed had sufficient token variation, and the transfer screen itself rejected the frozen gate.

## Scope and remaining gates

Stage 0, Cora Stage 1, and the PubMed transfer Stage 1 screen are complete. Stage 2, multi-seed confirmation, and test evaluation were not run after the PubMed promotion gate failed. The current evidence supports a Cora-specific Stage 1 gain; it does not support transfer of that gain to PubMed.

## Artifacts

- Stage 0 metrics: `03_STAGE0_CROSS_DATASET.md` and raw JSON under `diagnostics/`.
- Native-token and masking checks: `02_NATIVE_STRUCTURE_AUDIT.md`.
- Cora Stage 1 metrics: `04_CORA_STAGE1.md` and `experiments/stage1_cora/results.json`.
- PubMed Stage 1 results: `05_PUBMED_STAGE1.md` and `experiments/stage1_pubmed/results.json`.
- Aggregate record: `results.json`.
- Remote experiment root: `/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/NHMC_V16`.