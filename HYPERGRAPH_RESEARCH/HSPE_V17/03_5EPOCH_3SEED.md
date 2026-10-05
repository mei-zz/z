# 5-epoch, 3-seed formal stage

Datasets: Cora and PubMed. Seeds: 0, 1, 2. Five arms per seed: B0 baseline, C1 histogram, C2 size-shuffle, C3 parameter-matched, and H1 HSPE-REAL. Five epochs, fixed validation candidates, test OFF. V16 pair caches are reused only after source, split/pool, sampler, feature-key, seed, epoch, result, and checkpoint checks.

Concurrency is capped at four isolated dataset/seed worker processes. Each process executes its five arms sequentially, sharing that seed’s immutable feature caches. The V100 has 16 GB; resource monitoring is used only during startup stability verification.

Per dataset, GO requires H1 to beat B0 in at least 2/3 seeds with mean gain >=0.003; beat C1 and C3 in at least 2/3 seeds with mean margins >=0.002; and, when size-shuffle power is adequate, beat C2 under the same 2/3 and +0.002 criteria. Adequacy is conservatively defined as >=30% informative changes in both train and validation in each seed. Cora and PubMed must both pass to enter 10-epoch confirmation.

Current execution state: awaiting server preflight and launch.