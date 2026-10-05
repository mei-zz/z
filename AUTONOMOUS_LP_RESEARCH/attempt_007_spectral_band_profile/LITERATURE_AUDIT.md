# Attempt 007 — Literature audit

Working name: Fixed Laplacian Spectral Band Profile (FLSBP)

## Candidate object

Compute a fixed low-frequency normalized-Laplacian basis from the training graph and represent a pair by squared endpoint differences aggregated into four spectral bands, with a resistance-weighted companion profile. The basis is fixed before fitting; no learnable spectral module is introduced.

## Novelty-kill result

Spectral link prediction is an established neighboring family. Searches covered 2022–2026 spectral link prediction, diffusion distances, spectral GNNs, curvature/spectral hybrids, and recent complex-network spectral predictors. Collision is `L1`; this is only a cheap probe of a fixed bandwise object and cannot be claimed as a new spectral method without a much stronger result.

## Sources checked

- [Link prediction based on spectral analysis (2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10760775/) — direct spectral LP precedent.
- [Learnable Diffusion Distances for Link Prediction (2025)](https://doi.org/10.1109/ACCESS.2025.3590610) — recent diffusion/spectral LP precedent.
- [Spectro-Riemannian Graph Neural Networks (ICLR 2025)](https://proceedings.iclr.cc/paper_files/paper/2025/hash/915125efea950af378435518b3542e6a-Abstract-Conference.html) — recent spectral/curvature representation precedent.
- [Link predictability via second-order spectral perturbation (2026)](https://doi.org/10.1016/j.physa.2026.131838) — current spectral link-predictability direction.
