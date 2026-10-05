"""Run an official LPShift script with a narrowly scoped PyTorch 2.6+ loader shim.

The LPShift/OGB code serializes PyG Data objects.  PyTorch 2.6 changed
torch.load's default to weights_only=True, which rejects those trusted data
objects.  This wrapper does not alter model code or data; it only restores the
pre-2.6 deserialization behavior for the explicitly supplied official script.
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path

import torch


_original_load = torch.load


def _trusted_load(*args, **kwargs):
    kwargs.setdefault("weights_only", False)
    return _original_load(*args, **kwargs)


torch.load = _trusted_load

if len(sys.argv) < 2:
    raise SystemExit("usage: python lpcompat_run.py SCRIPT [ARGS ...]")

script = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(script.parent))

# LPShift's 2024 utility code passes torch tensors as SciPy sparse-matrix
# indices.  SciPy 1.15 no longer accepts torch.dtype objects there.  Preserve
# the exact integer indices while adapting only their container type.
try:
    import utils as _lp_utils

    class _EdgeIndexCompat:
        """Keep torch size() while exposing NumPy values to SciPy indexing."""

        def __init__(self, tensor):
            self.tensor = tensor

        def size(self, *args):
            return self.tensor.size(*args)

        def __getitem__(self, key):
            value = self.tensor[key]
            if torch.is_tensor(value):
                return value.detach().cpu().numpy()
            return value

    for _name in ("CN", "PA", "SP"):
        if hasattr(_lp_utils, _name):
            _original_heuristic = getattr(_lp_utils, _name)

            def _wrap_heuristic(fn):
                def _compat(*args, **kwargs):
                    converted = list(args)
                    if len(converted) >= 2 and torch.is_tensor(converted[1]):
                        original = converted[1]
                        converted[1] = _EdgeIndexCompat(original)
                        result = fn(*converted, **kwargs)
                        if isinstance(result, tuple) and len(result) == 2:
                            result = (result[0], original)
                        return result
                    return fn(*converted, **kwargs)

                return _compat

            setattr(_lp_utils, _name, _wrap_heuristic(_original_heuristic))
except ImportError:
    pass

sys.argv = [str(script), *sys.argv[2:]]
runpy.run_path(str(script), run_name="__main__")
