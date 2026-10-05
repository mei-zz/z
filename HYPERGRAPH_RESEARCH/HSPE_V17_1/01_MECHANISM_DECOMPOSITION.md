# Mechanism controls

B0: exact frozen strong baseline.
C0 COUNT-LINEAR: two real log counts, one zero-init Linear(2,1); 3 added parameters.
C1 COUNT-PARAM-MATCHED: pad the two log counts with four zeros; Linear(6,8), ReLU, duplicate hidden vector to width16, append two real counts, zero-init Linear(18,1). Exactly 75 added parameters, same hidden8 and final residual width as H1. Padding contains no size or degree information.
C2 CONSTANT-SET: exact V17 C3, constant [1,1,1,0,0,0] per existing token, real token/support counts, same H1 encoder/pooling/head; 75 parameters.
C3 GLOBAL SIZE-LABEL SHUFFLE: see 02_HIGH_POWER_SHUFFLE.md.
H1: exact original HSPE; 75 parameters.

Per dataset and seed report TotalGain=H1-B0, CountLinearGain=C0-B0, CountCapacityGain=C1-C0, SetPathwayGain=C2-C1, SizeContentGain=H1-C2, ShuffleAssignmentGain=H1-C3. These contrasts are empirical diagnostics, not a causal decomposition. Controls scope claims and never reject primary efficacy.

