from __future__ import annotations

import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import torch
import run_v13 as runner

runner.ACTIVE_ARM = "BASELINE"
runner.PATCHED = False
runner.install_hooks()
from dcdlp.models.dcdlp import DCDLP

kwargs = dict(input_dim=8, hidden_dim=16, branch_dim=8, num_layers=2,
              dropout=0.0, backbone="gcn", hypergraph_mode="raw")
base = DCDLP(**kwargs)
base_count = sum(p.numel() for p in base.parameters() if p.requires_grad)

runner.ACTIVE_ARM = "ECR_FULL"
model = DCDLP(**kwargs)
model.train()
x = torch.randn(10, 8)
edge_index = torch.tensor([
    [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 0, 2, 1, 4],
    [1, 0, 2, 1, 3, 2, 4, 3, 5, 4, 6, 5, 7, 6, 8, 7, 9, 8, 2, 0, 4, 1],
], dtype=torch.long)
pairs = torch.tensor([[0, 1], [0, 3], [1, 5], [2, 7], [3, 9], [4, 8]], dtype=torch.long)
out = model(x, edge_index, pairs, remove_target_edges=True)
loss = torch.nn.functional.binary_cross_entropy_with_logits(
    out["logit"], torch.tensor([1., 0., 0., 1., 0., 1.])
)
loss.backward()
new_count = sum(p.numel() for p in model.parameters() if p.requires_grad) - base_count
assert new_count == 3 * 8 + 4, (base_count, new_count)
for name in ("v13_raw_coef", "v13_struct_coef", "v13_density_coef", "v13_interaction_coef"):
    grad = getattr(model, name).grad
    assert grad is not None and torch.isfinite(grad).all(), name
model.eval()
with torch.no_grad():
    check = model(x, edge_index, pairs, remove_target_edges=True)["logit"]
assert torch.isfinite(check).all()
print(json.dumps({"state":"HOOK_SMOKE_PASS","baseline_parameters":base_count,
                  "ECR_FULL_added_parameters":new_count,"train_loss":float(loss.detach()),
                  "eval_finite":bool(torch.isfinite(check).all())}))


