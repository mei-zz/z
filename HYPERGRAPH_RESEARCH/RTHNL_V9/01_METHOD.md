# RTHNL method audit

For each positive p, let the selected Graph-hard negatives have logits `s_i`, unreduced negative BCE losses `softplus(s_i)`, and detached logit gradients `g_i=sigmoid(s_i)`. V9 sets `c_p=median(g_i)`, assigns raw weight 1 when `g_i<=c_p` and `2*c_p/(c_p+g_i+1e-8)` otherwise, then normalizes the weights within that positive by their mean plus `1e-8`.

Under V8's frozen `K=1`, `c_p=g_1`, so `g_1<=c_p` is always true. Thus raw and normalized weights are the same scalar for the singleton. In float32 the normalized value is exactly 1. The negative loss and gradient equal Graph-hard. Every permutation of one within-positive weight is the identity, so Shuffled-RTHNL has exactly the same loss and gradient as RTHNL. `ESS/K=1`.

The conclusion does not depend on trained weights or validation data. It follows from K and the registered formula. Increasing K or using gradients from unselected candidates would change the frozen protocol, so neither was done.
