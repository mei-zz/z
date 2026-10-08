#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT=/home/zhoulihui/lchr_v2
OUTPUT_DIR="$PROJECT_ROOT/HYPERGRAPH_RESEARCH/QTHS_V7_1"
WHEELHOUSE="$OUTPUT_DIR/wheelhouse"
BASE_PY=/home/zhoulihui/anaconda3/envs/mei_env/bin/python
REPRO_ENV=/home/zhoulihui/anaconda3/envs/mei_qths_repro

(cd "$WHEELHOUSE" && sha256sum --check "$OUTPUT_DIR/wheelhouse_sha256.txt")
if [ ! -x "$REPRO_ENV/bin/python" ]; then
  "$BASE_PY" -m venv --system-site-packages "$REPRO_ENV"
fi

"$REPRO_ENV/bin/python" -m pip install --no-index --no-deps --find-links "$WHEELHOUSE" \
  'torch==2.3.1+cu121' \
  'nvidia-cuda-nvrtc-cu12==12.1.105' \
  'nvidia-cuda-runtime-cu12==12.1.105' \
  'nvidia-cuda-cupti-cu12==12.1.105' \
  'nvidia-cudnn-cu12==8.9.2.26' \
  'nvidia-cublas-cu12==12.1.3.1' \
  'nvidia-cufft-cu12==11.0.2.54' \
  'nvidia-curand-cu12==10.3.2.106' \
  'nvidia-cusolver-cu12==11.4.5.107' \
  'nvidia-cusparse-cu12==12.1.0.106' \
  'nvidia-nccl-cu12==2.20.5' \
  'nvidia-nvtx-cu12==12.1.105' \
  'nvidia-nvjitlink-cu12==12.1.105' \
  'triton==2.3.1' \
  'torch-geometric==2.5.3'

"$REPRO_ENV/bin/python" - <<'PY'
import json
import sys
import torch
import torch_geometric
import numpy
import scipy
import sklearn
import networkx
import pandas
import pyarrow
import yaml

if not torch.cuda.is_available():
    raise RuntimeError("PyTorch 2.3.1+cu121 cannot access CUDA on the registered server")
if "V100" not in torch.cuda.get_device_name(0):
    raise RuntimeError("Expected the registered Tesla V100 GPU")
x = torch.randn((512, 512), device="cuda")
y = x @ x
conv = torch.nn.Conv2d(3, 8, 3).cuda()
image = torch.randn((2, 3, 32, 32), device="cuda")
z = conv(image)
torch.cuda.synchronize()
if not torch.isfinite(y).all() or not torch.isfinite(z).all():
    raise RuntimeError("CUDA smoke operation produced non-finite values")
report = {
    "status": "PASS",
    "python": sys.version.split()[0],
    "torch": str(torch.__version__),
    "torch_cuda_build": str(torch.version.cuda),
    "cudnn": torch.backends.cudnn.version(),
    "pyg": str(torch_geometric.__version__),
    "gpu": torch.cuda.get_device_name(0),
    "cuda_matmul": "PASS",
    "cudnn_conv2d": "PASS",
    "numpy": str(numpy.__version__),
    "scipy": str(scipy.__version__),
    "scikit_learn": str(sklearn.__version__),
    "networkx": str(networkx.__version__),
    "pandas": str(pandas.__version__),
    "pyarrow": str(pyarrow.__version__),
    "pyyaml": str(yaml.__version__),
    "environment": "/home/zhoulihui/anaconda3/envs/mei_qths_repro",
    "base_environment_modified": False,
}
print(json.dumps(report, indent=2), flush=True)
PY
