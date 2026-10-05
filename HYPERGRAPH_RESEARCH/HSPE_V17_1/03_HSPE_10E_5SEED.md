# Phase A

Cora/PubMed × seeds0–4 × ten epochs × B0,C0,C1,C2,C3,H1 = 60 validation-only outcomes. Fixed final epoch10, no test. Four concurrent isolated dataset/seed workers; six arms sequentially within each worker. CPU OMP/MKL4, OpenBLAS/NumExpr1 per worker.

Primary efficacy each dataset: H1>B0 in >=4/5 seeds; mean paired MRR delta>=0.005; median delta>0. Controls do not gate efficacy. Report MRR, Hits@10, Hits@20, mean positive rank and mean/std/median/min/max/per-seed deltas, parameter counts and costs.

State: PHASE_A_RUNNING; startup verified with four active workers, zero failed jobs, V100 100% utilization, 2810 MiB used. Cora seed0/1 B0 completed training epoch5/10 at the verification snapshot. See diagnostics/STARTUP_VERIFIED.json.


