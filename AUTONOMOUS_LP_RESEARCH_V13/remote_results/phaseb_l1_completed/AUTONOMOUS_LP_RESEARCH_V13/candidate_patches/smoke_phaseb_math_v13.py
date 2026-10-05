from itertools import product
import torch
import phaseb_hooks_v13 as hooks
from phaseb_hooks_v13 import _expected_reciprocal_rank
from torch.nn import functional as F

pos = torch.tensor([0.2, -0.1], dtype=torch.float64, requires_grad=True)
neg = torch.tensor([[0.4, -0.2, 0.1], [0.3, -0.4, 0.2]], dtype=torch.float64, requires_grad=True)
temperature = 0.7
actual = _expected_reciprocal_rank(pos, neg, temperature)
prob = torch.sigmoid((neg - pos[:, None]) / temperature)
brute = []
for row in range(len(pos)):
    value = pos.new_tensor(0.0)
    for outrank in product((0, 1), repeat=neg.shape[1]):
        mass = pos.new_tensor(1.0)
        rank = 1
        for j, indicator in enumerate(outrank):
            mass = mass * (prob[row, j] if indicator else 1.0 - prob[row, j])
            rank += indicator
        value = value + mass / rank
    brute.append(value)
expected = torch.stack(brute)
assert torch.allclose(actual, expected, atol=1e-12, rtol=1e-12), (actual, expected)
(1.0 - actual.mean()).backward()
assert torch.isfinite(actual).all() and torch.isfinite(pos.grad).all() and torch.isfinite(neg.grad).all()
print('EXPECTED_MRR_DP_PASS', actual.detach().tolist(), 'gradient_finite=True')

control_pos = torch.tensor([0.2, -0.1], dtype=torch.float64, requires_grad=True)
control_neg = torch.linspace(-0.5, 0.6, 40, dtype=torch.float64).reshape(2, 20).requires_grad_()
dummy_logits = torch.tensor([0.1, -0.2], dtype=torch.float64)
dummy_labels = torch.tensor([1.0, 0.0], dtype=torch.float64)
runner_stub = type('RunnerStub', (), {'LAST_PAIRS': [[0, 1], [1, 2]]})()

for arm in ('L1_EXPECTED_MRR', 'L1_INDEP_BCE', 'L1_LISTWISE',
            'L1_LISTWISE_RANDOM', 'L1_REPEAT_BCE'):
    hooks.LAST_SETWISE = (control_pos, control_neg)
    objective = hooks.loss_hook_factory(
        arm, runner_stub,
        lambda _arm: lambda logits, labels, *args, **kwargs:
            F.binary_cross_entropy_with_logits(logits, labels),
    )
    value = objective(dummy_logits, dummy_labels)
    assert value.ndim == 0 and torch.isfinite(value), (arm, value)
    value.backward(retain_graph=True)
    assert torch.isfinite(control_pos.grad).all() and torch.isfinite(control_neg.grad).all(), arm
    control_pos.grad.zero_()
    control_neg.grad.zero_()
print('L1_OBJECTIVE_CONTROLS_PASS', 'arms=5', 'all_gradients_finite=True')
