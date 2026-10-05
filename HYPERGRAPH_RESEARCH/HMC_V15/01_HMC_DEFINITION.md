# HMC Definition — frozen before Stage 0

This test does not claim information that a weighted 2-section cannot recover. The narrower hypothesis is that a pair decoder benefits from explicit support-wise joint incidence multiplicities beyond support count, scalar summaries and independently shuffled cross-side alignment.

The fixed hypergraph is the current Raw-HG raw_star on the training message graph: each non-isolated node x contributes {x} union N(x). For target-masked graph and pair (u,v), m_u(w) counts hyperedges containing u and w; S_uv contains w distinct from u,v with both counts positive. Let a_w=log(1+m_u(w)), b_w=log(1+m_v(w)), and t_w=[a_w+b_w, |a_w-b_w|, a_w*b_w].

HMC applies ReLU(Linear(3,8)) per token, mean and max pools, appends c_uv=log(1+|S_uv|), and scores a residual Linear(17,1). Output weight and bias start at zero. Empty support yields zero pooled vectors and zero count. This adds 49 parameters: 0.1981% over the 24,735-parameter baseline.

Frozen Stage-0 features:
- C=|S_uv|; Z0 is log(1+C).
- M=sum_w m_u(w)m_v(w); E=M-C; MAX=max_w m_u(w)m_v(w); STD=std_w(log(1+m_u(w)m_v(w)); zero for empty support.
- MS=sum_w log(1+m_u(w))*log(1+m_v(w)).
- HRA-like: q(x)=sum over raw-star hyperedges containing x of (|e|-1); HRA(u,v)=sum over w in S_uv of 1/(sqrt(max(q(u),1)*max(q(v),1))*(1+q(w))). q is recomputed after target masking for training positives.
- Z1=MS; Z2=HRA; Z3=[log(1+C),log(1+M),log(1+E),log(1+MAX),STD]; Z4 uses Z3 summaries after deterministic cross-side shuffle.

HMC-FLAT preserves exact support identities and count but sets all multiplicities to (1,1). HMC-SHUFFLE canonicalizes endpoints by node ID, preserves the lower-ID side array A, and independently permutes the higher-ID array B with a deterministic pair-keyed seed. It preserves each side marginal and tests same-support alignment. An informative shuffle changes the multiset of paired multiplicities. HMC-FLAT, HMC-SHUFFLE and HMC-REAL have identical architecture and parameter count.