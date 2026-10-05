#!/usr/bin/env bash
set -eu
cd /home/zhoulihui/lchr_v2
out=HYPERGRAPH_RESEARCH/CPTS_V10_1_AUDIT
export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 PYTHONUNBUFFERED=1
nohup setsid /home/zhoulihui/anaconda3/envs/mei_qths_repro/bin/python -u "$out/run_audit.py" > "$out/supervisor.log" 2>&1 < /dev/null &
printf 'DETACHED_LAUNCH_PID=%s\n' "$!"
