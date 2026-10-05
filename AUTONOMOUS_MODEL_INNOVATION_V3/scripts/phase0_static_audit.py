from __future__ import annotations

import json
import sys
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dcdlp.models.dcdlp import DCDLP
from v3_models import MODEL_CLASSES


def common():
    return dict(
        hidden_dim=64,
        branch_dim=32,
        num_layers=2,
        dropout=0.0,
        backbone="gcn",
        use_interaction=True,
        active_branches=("degree", "cn", "residual"),
        decoder_mode="additive",
        interaction_mode="unrestricted",
        cn_input_schema="selective_v1",
    )


def main() -> None:
    torch.manual_seed(0)
    x = torch.randn(31, 7)
    edges = torch.tensor([
        [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        [1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    ], dtype=torch.long)
    pairs = torch.tensor([[0, 6], [2, 8], [10, 16], [20, 21]], dtype=torch.long)
    kwargs = common()
    parent = DCDLP(7, **kwargs)
    parent_state = {key: value.detach().clone() for key, value in parent.state_dict().items()}
    records = []
    for model_id, model_class in [("B0_Parent", None), *MODEL_CLASSES.items()]:
        torch.manual_seed(0)
        model = DCDLP(7, **kwargs) if model_class is None else model_class(7, **kwargs)
        model.load_state_dict(parent_state, strict=False)
        model.eval()
        if model_class is not None and hasattr(model, "depth_scale"):
            model.depth_scale.data.zero_()
        parent_output = parent(x, edges, pairs)["logit"]
        zero_output = model(x, edges, pairs)["logit"]
        equivalence = float((zero_output - parent_output).abs().max())
        exchange = float((model(x, edges, pairs)["logit"] - model(x, edges, pairs.flip(1))["logit"]).abs().max())
        if model_class is not None:
            if hasattr(model, "depth_scale"):
                model.depth_scale.data.fill_(0.1)
            model.zero_grad(set_to_none=True)
            model(x, edges, pairs)["logit"].sum().backward()
            prefixes = ("depth_pair_encoder", "depth_operator", "depth_scale", "concat_head")
            gradient_tensors = sum(
                int(parameter.grad is not None and torch.isfinite(parameter.grad).all() and parameter.grad.abs().sum() > 0)
                for name, parameter in model.named_parameters() if name.startswith(prefixes)
            )
        else:
            gradient_tensors = 0
        records.append({
            "model_id": model_id,
            "total_parameters": sum(value.numel() for value in model.parameters()),
            "trainable_parameters": sum(value.numel() for value in model.parameters() if value.requires_grad),
            "zero_scale_parent_equivalence_error": equivalence,
            "exchange_error": exchange,
            "finite": bool(torch.isfinite(zero_output).all()),
            "changed_path_gradient_tensors": gradient_tensors,
            "operator_trainable": bool(hasattr(model, "depth_operator") and model.depth_operator.requires_grad),
        })
    status = all(row["zero_scale_parent_equivalence_error"] < 1e-6 and row["exchange_error"] < 1e-6 and row["finite"] for row in records)
    print(json.dumps({"status": "PASS" if status else "FAIL", "records": records}, indent=2))


if __name__ == "__main__":
    main()
