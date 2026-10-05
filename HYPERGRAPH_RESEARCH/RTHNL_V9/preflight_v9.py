"""Check V9's frozen training K before spending a training budget."""
import json
from pathlib import Path
import torch
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
samples = ROOT / 'HYPERGRAPH_RESEARCH/QTHS_V7_1/RUNS/CORA/C1_GRAPH_HARD/seed0/negative_samples_by_epoch.npz'
with np.load(samples, allow_pickle=False) as archive:
    shape = list(archive['negatives'].shape)
assert shape == [10, 4488, 2], shape
device = 'cuda' if torch.cuda.is_available() else 'cpu'
checks = []
for dtype in (torch.float32, torch.float64):
    logits = torch.linspace(-20, 20, 10001, device=device, dtype=dtype).reshape(-1, 1).requires_grad_()
    g = logits.detach().sigmoid()
    c = g.median(dim=1, keepdim=True).values
    raw = torch.where(g <= c, torch.ones_like(g), 2*c/(c+g+1e-8))
    weight = (raw/(raw.mean(dim=1, keepdim=True)+1e-8)).detach()
    # Every within-positive permutation of a singleton is the identity.
    shuffled = weight.flip(dims=[1])
    base_loss = torch.nn.functional.softplus(logits).mean()
    robust_loss = (weight*torch.nn.functional.softplus(logits)).mean()
    control_loss = (shuffled*torch.nn.functional.softplus(logits)).mean()
    base_grad = torch.autograd.grad(base_loss, logits, retain_graph=True)[0]
    robust_grad = torch.autograd.grad(robust_loss, logits, retain_graph=True)[0]
    control_grad = torch.autograd.grad(control_loss, logits)[0]
    checks.append({
        'dtype': str(dtype), 'raw_weights_all_one': bool(torch.equal(raw, torch.ones_like(raw))),
        'normalized_weight_min': weight.min().item(), 'normalized_weight_max': weight.max().item(),
        'rthnl_equals_shuffled_loss': bool(torch.equal(robust_loss, control_loss)),
        'rthnl_equals_shuffled_gradient': bool(torch.equal(robust_grad, control_grad)),
        'max_gradient_difference_from_baseline': (robust_grad-base_grad).abs().max().item(),
        'ess_over_k': ((weight.sum(dim=1)**2)/(weight.square().sum(dim=1))).mean().item(),
    })
assert all(c['rthnl_equals_shuffled_gradient'] and c['raw_weights_all_one'] for c in checks)
result = {
    'state': 'PREFLIGHT_BLOCKED', 'reason': 'FROZEN_K1_DEGENERACY',
    'training_negative_count_per_positive': 1, 'candidate_pool_per_positive': 20,
    'recorded_negative_shape': shape, 'device': device,
    'gpu': torch.cuda.get_device_name(0) if device == 'cuda' else None,
    'torch_version': torch.__version__, 'checks': checks,
    'training_jobs_launched': 0, 'test_evaluations': 0,
    'performance_decision': 'NOT_EVALUATED',
    'mechanism_status': 'INOPERATIVE_UNDER_FROZEN_K1',
    'requires_user_decision': 'Keep frozen K=1 or explicitly authorize a new matched multi-negative protocol.',
}
(OUT/'results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2), flush=True)
