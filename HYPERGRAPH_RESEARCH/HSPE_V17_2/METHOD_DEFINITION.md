# Frozen R-HSPE method

R-HSPE uses the exact V17.1 H2 model. In the training-visible raw-star hypergraph, each candidate node pair (u,v) defines tokens (w,e,f) where w is a common projected support node, e contains u,w, and f contains v,w. Identity multiplicities and token topology are preserved; the predicted training edge is removed before token construction.

Training-only ECDF F(s)=#{training-visible active hyperedges with size <=s}/#active hyperedges maps effective |e|,|f| into ranks a,b. Each token is [a+b, abs(a-b), a*b, 0,0,0]. The frozen Linear(6,8)+ReLU encoder is pooled by mean and max. Two explicit descriptors log1p(token_count), log1p(support_count) are appended; a zero-initialized Linear(18,1) residual is added to the frozen Raw-HG DCDLP logit. Added parameter count is 75.

Optimizer, learning rate 0.001, weight decay 0.0001, dimensions16/8, two GCN layers, dropout0, batch4096, QTHS25, loss, and fixed final epoch10 remain identical to V17.1. Evaluator is score_pairs(batch8192), target removal True, ranking_metrics with 20 negative candidates. Test graph features use training-visible structure, and test ECDF uses only training-visible hyperedges. All parent checkpoints and source/config hashes are recorded before test.

Primary candidate claim: candidate-specific hyperedge-pair context encoding. Secondary component: training-only rank-normalized cardinality descriptors. Mechanism: context-driven. Size causal claim: NOT_SUPPORTED. Rank normalization alone is not the primary innovation. Cross-graph scale invariance is algebraic under strictly increasing size transforms, but reduced empirical cross-graph sensitivity has not been isolated causally.
