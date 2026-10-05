# CPTS method

For one positive, sort the M=20 frozen graph-teacher hardness scores in ascending order `h_(1) <= ... <= h_(M)`. The H0 Gaussian model has one mean and one shared variance, with `SSE1 = sum_i (h_i - mean(h))^2` and `BIC1 = M ln(SSE1/M) + 2 ln(M)`.

For each contiguous split `b=2,...,M-2`, H1 fits the lower segment `h_(1)...h_(b)` and upper segment `h_(b+1)...h_(M)` with separate means and one shared residual variance. Let `SSE2(b)` be the sum of the two within-segment SSEs. The parameter count is four: two segment means, shared variance, and discrete split location. Thus `BIC2(b) = M ln(SSE2(b)/M) + 4 ln(M)`. Select `b* = argmin_b BIC2(b)`. A float64 tiny floor is used only if the variance estimate is zero.

If `BIC2(b*) < BIC1`, an upper tail exists, its size is `M-b*`, and CPTS selects `h_(b*)`, the hardest candidate below the detected tail. Otherwise it selects `h_(M)`, exactly Graph-hard. Ties use stable original candidate order. No percentile, trim ratio, trainable parameter, or additional neural forward is used. Prefix sums make the split scan O(M) per positive after sorting; sorting is O(M log M).

The global control fits the same two-segment BIC on pooled Cora training candidate scores and applies the resulting single raw-score boundary to every positive. Matched-Q removes the rounded mean local tail count from every positive. Random-Matched removes exactly the local CPTS count, with deterministic per-seed random candidate removals, then chooses the hardest remaining candidate. These controls are training-pool-only.
