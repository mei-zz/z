# V6.1 Efficiency

- Strict pool generation cold-start: 1.2152s.
- Train-only teacher fitting: Graph 25.966s; Raw-HG 51.921s. These are one-time cold-start costs, not per-epoch selection overhead.
- Detached teacher score forward: Graph 16.3319s; Raw-HG 21.1123s (cached score reuse avoids repeated forward passes).
- Cached rank/veto selection: total 0.1975s; amortized across 10 epochs 0.019751s/epoch.
- Cached score forward repeats for same teacher/pool: 0.
- A4 selection-only overhead relative to mean strict learner training time: True under 5% target.
