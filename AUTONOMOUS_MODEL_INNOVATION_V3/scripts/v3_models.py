from __future__ import annotations

import math

import torch
from torch import nn
from torch.nn import functional as F

from dcdlp.models.dcdlp import DCDLP
from dcdlp.models.node_encoder import mask_pair_edges


class _DepthPairModel(DCDLP):
    """Shared V3 scaffold for exactly one changed pair-decoder mechanism."""

    def __init__(self, *args, pair_mode: str = "cross", **kwargs) -> None:
        super().__init__(*args, **kwargs)
        hidden_dim = self.node_encoder.layers[-1].linear.out_features
        branch_dim = self.degree_branch.scorer.in_features
        self.pair_mode = pair_mode
        self.depth_pair_encoder = nn.Sequential(
            nn.Linear(hidden_dim * 3, branch_dim),
            nn.ReLU(),
            nn.LayerNorm(branch_dim),
        )
        self.depth_operator = nn.Parameter(torch.empty(branch_dim, branch_dim))
        nn.init.orthogonal_(self.depth_operator)
        self.depth_scale = nn.Parameter(torch.tensor(0.1))
        self.shuffle_depth = False

    def _encode_states(self, x: torch.Tensor, edge_index: torch.Tensor) -> list[torch.Tensor]:
        states = []
        for layer, norm in zip(self.node_encoder.layers, self.node_encoder.norms):
            x = norm(layer(x, edge_index))
            x = F.relu(x)
            x = F.dropout(x, p=self.node_encoder.dropout, training=self.training)
            states.append(x)
        return states

    def _pair_state(self, h: torch.Tensor, pairs: torch.Tensor) -> torch.Tensor:
        hu, hv = h[pairs[:, 0]], h[pairs[:, 1]]
        return self.depth_pair_encoder(torch.cat([
            hu * hv, torch.abs(hu - hv), hu + hv,
        ], dim=-1))

    def _base_scores(self, h: torch.Tensor, message_edges: torch.Tensor, pairs: torch.Tensor):
        neighbors, degrees = self._structure(message_edges, h.shape[0])
        z_degree, score_degree = self.degree_branch(degrees, pairs)
        z_cn, score_cn, cn_statistics = self.cn_branch(h, pairs, neighbors, degrees)
        z_residual, score_residual = self.residual_branch(h, pairs)
        if "degree" not in self.active_branches:
            z_degree, score_degree = torch.zeros_like(z_degree), torch.zeros_like(score_degree)
        if "cn" not in self.active_branches:
            z_cn, score_cn = torch.zeros_like(z_cn), torch.zeros_like(score_cn)
        if "residual" not in self.active_branches:
            z_residual, score_residual = torch.zeros_like(z_residual), torch.zeros_like(score_residual)
        projected = z_degree @ self.interaction
        raw_interaction = (
            self.interaction_scale * (projected * z_cn).sum(-1) / z_cn.shape[-1] ** 0.5
        )
        score_interaction = (
            torch.zeros_like(raw_interaction)
            if self.interaction_mode == "disabled" else raw_interaction
        )
        base_logit = score_degree + score_cn + score_residual + score_interaction + self.bias
        return base_logit, {
            "score_degree": score_degree,
            "score_cn": score_cn,
            "score_residual": score_residual,
            "score_interaction": score_interaction,
            "z_degree": z_degree,
            "z_cn": z_cn,
            "z_residual": z_residual,
            **cn_statistics,
        }

    def _changed_score(self, early_state: torch.Tensor, late_state: torch.Tensor) -> torch.Tensor:
        if self.shuffle_depth and len(early_state) > 1:
            early_state = early_state.roll(shifts=1, dims=0)
        if self.pair_mode == "late":
            raw = ((late_state @ self.depth_operator) * late_state).sum(-1)
        elif self.pair_mode == "concat":
            raw = self.concat_head(torch.cat([early_state, late_state], dim=-1)).squeeze(-1)
        else:
            raw = ((early_state @ self.depth_operator) * late_state).sum(-1)
        return self.depth_scale * raw / math.sqrt(late_state.shape[-1])

    def forward(
        self,
        x: torch.Tensor,
        edge_index: torch.Tensor,
        pairs: torch.Tensor,
        remove_target_edges: bool = True,
    ) -> dict[str, torch.Tensor]:
        message_edges = mask_pair_edges(edge_index, pairs) if remove_target_edges else edge_index
        states = self._encode_states(x, message_edges)
        h = states[-1]
        base_logit, outputs = self._base_scores(h, message_edges, pairs)
        early_state = self._pair_state(states[0], pairs)
        late_state = self._pair_state(states[-1], pairs)
        score_cross = self._changed_score(early_state, late_state)
        outputs.update({
            "logit": base_logit + score_cross,
            "score_cross_depth": score_cross,
            "depth_cross_norm": (early_state - late_state).detach().norm(dim=-1),
            "depth_operator_norm": (
                self.depth_operator.detach().norm().expand(len(pairs))
                if hasattr(self, "depth_operator")
                else torch.zeros_like(base_logit)
            ),
            "interaction_share": torch.zeros_like(base_logit),
        })
        return outputs


class CDPT(_DepthPairModel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, pair_mode="cross", **kwargs)


class LateOnly(_DepthPairModel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, pair_mode="late", **kwargs)


class ConcatMLP(_DepthPairModel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, pair_mode="concat", **kwargs)
        # Remove the CDPT-only tensor parameter and replace it with a small
        # concatenation MLP.  The resulting parameter count differs from CDPT
        # by only 33 at the audited 64/32 dimensions.
        del self.depth_operator
        self.concat_head = nn.Sequential(
            nn.Linear(64, 15),
            nn.ReLU(),
            nn.Linear(15, 1),
        )

    def _changed_score(self, early_state: torch.Tensor, late_state: torch.Tensor) -> torch.Tensor:
        if self.shuffle_depth and len(early_state) > 1:
            early_state = early_state.roll(shifts=1, dims=0)
        raw = self.concat_head(torch.cat([early_state, late_state], dim=-1)).squeeze(-1)
        return self.depth_scale * raw / math.sqrt(late_state.shape[-1])

    def forward(self, *args, **kwargs):
        output = super().forward(*args, **kwargs)
        output["depth_operator_norm"] = torch.zeros_like(output["logit"])
        return output


class FixedRandomOperator(_DepthPairModel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, pair_mode="cross", **kwargs)
        with torch.no_grad():
            branch_dim = self.depth_operator.shape[0]
            self.depth_operator.normal_(mean=0.0, std=1.0 / math.sqrt(branch_dim))
        self.depth_operator.requires_grad_(False)


MODEL_CLASSES = {
    "B1_CDPT": CDPT,
    "B2_LateOnly": LateOnly,
    "B3_ConcatMLP": ConcatMLP,
    "B4_FixedRandom": FixedRandomOperator,
}
