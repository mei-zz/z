# NHMC Definition and Frozen Stage-0 Features

The input hypergraph is the project's raw-star construction on the training graph: for each non-isolated center `x`, one hyperedge `e_x={x}∪N_train(x)`. For a training-positive target pair `(u,v)`, remove `(u,v)` before constructing/using any hyperedge descriptor. For a candidate negative, use the training graph as-is. Validation/test identities are not used in construction.

For shared support `w`, `E_u(w)={e:u,w∈e}` and `E_v(w)={f:v,w∈f}`. For every ordered pair `(e,f)∈E_u(w)×E_v(w)` (including `e=f` where applicable), define `A=e\{u,v,w}`, `B=f\{u,v,w}`, `o=|A∩B|`, `U=|A∪B|`, `J=o/max(1,U)`, and `O=o/max(1,min(|A|,|B|))`. The symmetric six-dimensional token is `[s_e+s_f, |s_e-s_f|, s_e*s_f, log(1+o), J, O]`, with `s_e=log(1+|e|)`.

All hyperedge-pair tokens are retained; no top-k or truncation is allowed. Target-masked local computation must match a full raw-star rebuild within `1e-6` for all raw descriptors on 100 sampled training positives per dataset. Endpoint swap must preserve the pair representation within `1e-6`.

Frozen controls and pair-level summary vectors:

- `C=|S_uv|`, support-wise HMC multiplicities `m_u(w),m_v(w)`, `MS=Σ_w log(1+m_u(w))log(1+m_v(w))`, `MAX=max_w m_u(w)m_v(w)`, and V15's exact HRA-like scalar. Let `q(x)=Σ_{e∋x}(|e|-1)` on the target-masked raw-star. `HRA(u,v)=Σ_{w∈S_uv} [sqrt(max(q(u),1)max(q(v),1)) (1+q(w))]^{-1}`.
- `Z0=[log(1+C)]`; `Z1=[HRA]`; `Z2=[log(1+C), HRA, MS, log(1+MAX)]`.
- `Z3` appends, for each of `s_e+s_f`, `|s_e-s_f|`, and `s_e*s_f`, token-wise mean, population SD, max, and p75; it also includes `log(1+token_count)`.
- `Z4` appends to Z3, separately for `log(1+o)`, `J`, and `O`, mean, population SD, max, p75, and p90, plus fractions with `o>0` and `o≥2`.
- `Z5` has the same dimensions as Z4 after shuffling `[log(1+o),J,O]` across candidate-pair tokens within frozen strata. Hyperedge-size bins are `<=2`, `3`, `4`, `5–8`, `9–16`, `17–32`, and `>=33`; shared-support-multiplicity bins use the same cut points. The pair of size bins and pair of multiplicity bins are each sorted before forming the joint stratum. Token counts, token sizes, and within-stratum overlap marginals are preserved. A fixed seed is used, and informative shuffle fraction counts candidate pairs whose token descriptors actually change.
- The single native scalar is `NS=Σ_wΣ_{e∈E_u(w)}Σ_{f∈E_v(w)} log(1+o_ef)/sqrt(max(1,(|e|-2)(|f|-2)))`.

The classifier is the frozen V15-style pipeline: five-fold `StratifiedGroupKFold` (matched negatives stay with their positive), fold-local `StandardScaler`, `LogisticRegression(C=1, solver=lbfgs, max_iter=2000, random_state=0)`, ROC-AUC and average precision, mean ± sample SD. No C tuning or feature selection.
