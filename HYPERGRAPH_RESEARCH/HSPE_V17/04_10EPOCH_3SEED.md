# 10-epoch, 3-seed confirmation

Conditional stage. It starts automatically only if both Cora and PubMed pass the 5-epoch, 3-seed gate. It repeats the same five arms, seeds, splits, sampler, and method definitions for ten epochs, validation only; test remains OFF.

GO requires H1 to beat B0 in at least 2/3 seeds with mean gain >=0.003 and beat C1/C3 in at least 2/3 seeds with mean margins >0.002. If shuffle is adequate, the same strict >0.002 mean margin applies to C2. Five- and ten-epoch directions and seed-level delta correlations are recorded. Current state: conditional, not started.