from __future__ import annotations

import math

import torch
from torch import nn
from torch.nn import functional as F

from dcdlp.models.dcdlp import DCDLP
from dcdlp.models.node_encoder import mask_pair_edges


class PairConditionedDynamicTransport(DCDLP):
    """DCDLP plus a pair-conditioned local message-transport path.

    The path is deliberately not an attention weight or scalar gate.  A
    symmetric endpoint-pair token generates a low-rank linear operator.  That
    operator is applied to the transformed neighbors of each endpoint and
    the two transported states are updated symmetrically before scoring.
    """

    def __init__(self, *args, transport_rank: int = 4, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        hidden_dim = self.node_encoder.layers[-1].linear.out_features
        branch_dim = self.degree_branch.scorer.in_features
        self.transport_rank = int(transport_rank)
        self.pair_token = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.LayerNorm(hidden_dim),
        )
        self.operator_generator = nn.Linear(
            hidden_dim, hidden_dim * self.transport_rank
        )
        self.neighbor_projection = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.rank_projection = nn.Linear(self.transport_rank, hidden_dim)
        self.endpoint_update = nn.Sequential(
            nn.Linear(hidden_dim * 3, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(),
        )
        self.transport_score = nn.Sequential(
            nn.Linear(hidden_dim * 3, branch_dim),
            nn.ReLU(),
            nn.Linear(branch_dim, 1),
        )
        self.transport_scale = nn.Parameter(torch.tensor(0.1))
        self.shuffle_transport = False
        self._neighbor_ids: torch.Tensor | None = None

    def set_transport_graph(self, edge_index: torch.Tensor, num_nodes: int) -> None:
        neighbors = [set() for _ in range(num_nodes)]
        for raw_u, raw_v in edge_index.detach().cpu().t().tolist():
            u, v = int(raw_u), int(raw_v)
            if u != v:
                neighbors[u].add(v)
                neighbors[v].add(u)
        max_degree = max((len(row) for row in neighbors), default=0)
        table = torch.full(
            (num_nodes, max_degree), -1, dtype=torch.long, device=edge_index.device
        )
        for node, row in enumerate(neighbors):
            if row:
                values = torch.as_tensor(sorted(row), dtype=torch.long, device=edge_index.device)
                table[node, :len(values)] = values
        self._neighbor_ids = table

    def _transport_endpoint(
        self,
        endpoint: torch.Tensor,
        other: torch.Tensor,
        h: torch.Tensor,
        operator: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        if self._neighbor_ids is None:
            raise RuntimeError("set_transport_graph must be called before forward")
        neighbor_ids = self._neighbor_ids[endpoint]
        valid = neighbor_ids >= 0
        safe_ids = neighbor_ids.clamp_min(0)
        # Remove the candidate edge itself from the local transport path.
        valid = valid & (neighbor_ids != other[:, None])
        neighbor_states = self.neighbor_projection(h[safe_ids])
        transported = torch.einsum("bdr,bkd->bkr", operator, neighbor_states)
        transported = transported * valid.unsqueeze(-1).to(transported.dtype)
        counts = valid.sum(dim=1, keepdim=True).to(h.dtype).clamp_min(1.0)
        aggregate = self.rank_projection(transported.sum(dim=1) / counts.sqrt())
        return aggregate, counts.squeeze(-1)

    def forward(
        self,
        x: torch.Tensor,
        edge_index: torch.Tensor,
        pairs: torch.Tensor,
        remove_target_edges: bool = True,
    ) -> dict[str, torch.Tensor]:
        if self._neighbor_ids is None or self._neighbor_ids.device != edge_index.device:
            self.set_transport_graph(edge_index, x.shape[0])
        message_edges = mask_pair_edges(edge_index, pairs) if remove_target_edges else edge_index
        h = self.node_encoder(x, message_edges)
        neighbors, degrees = self._structure(message_edges, x.shape[0])
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

        hu, hv = h[pairs[:, 0]], h[pairs[:, 1]]
        token = self.pair_token(torch.cat([hu + hv, torch.abs(hu - hv)], dim=-1))
        operator = self.operator_generator(token).reshape(
            len(pairs), hu.shape[-1], self.transport_rank
        )
        if self.shuffle_transport and len(pairs) > 1:
            operator = operator.roll(shifts=1, dims=0)
        aggregate_u, count_u = self._transport_endpoint(pairs[:, 0], pairs[:, 1], h, operator)
        aggregate_v, count_v = self._transport_endpoint(pairs[:, 1], pairs[:, 0], h, operator)
        updated_u = hu + self.endpoint_update(torch.cat([hu, aggregate_u, token], dim=-1))
        updated_v = hv + self.endpoint_update(torch.cat([hv, aggregate_v, token], dim=-1))
        pair_state = torch.cat([
            updated_u * updated_v,
            torch.abs(updated_u - updated_v),
            updated_u + updated_v,
        ], dim=-1)
        score_transport = self.transport_score(pair_state).squeeze(-1)
        logit = base_logit + self.transport_scale * score_transport
        return {
            "logit": logit,
            "score_degree": score_degree,
            "score_cn": score_cn,
            "score_residual": score_residual,
            "score_interaction": score_interaction,
            "score_transport": self.transport_scale * score_transport,
            "transport_norm": operator.detach().norm(dim=(1, 2)),
            "transport_neighbor_count": (count_u + count_v) / 2.0,
            "interaction_share": torch.zeros_like(logit),
            "z_degree": z_degree,
            "z_cn": z_cn,
            "z_residual": z_residual,
            **cn_statistics,
        }


class CrossDepthPairTensor(DCDLP):
    """Couple pair states from two propagation depths with a tensor operator."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        hidden_dim = self.node_encoder.layers[-1].linear.out_features
        branch_dim = self.degree_branch.scorer.in_features
        self.depth_pair_encoder = nn.Sequential(
            nn.Linear(hidden_dim * 3, branch_dim),
            nn.ReLU(),
            nn.LayerNorm(branch_dim),
        )
        self.depth_operator = nn.Parameter(torch.empty(branch_dim, branch_dim))
        nn.init.orthogonal_(self.depth_operator)
        self.depth_scale = nn.Parameter(torch.tensor(0.1))
        self.shuffle_cross = False

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
        neighbors, degrees = self._structure(message_edges, x.shape[0])
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
        early_state = self._pair_state(states[0], pairs)
        late_state = self._pair_state(states[-1], pairs)
        if self.shuffle_cross and len(pairs) > 1:
            early_state = early_state.roll(shifts=1, dims=0)
        score_cross = ((early_state @ self.depth_operator) * late_state).sum(-1) / math.sqrt(late_state.shape[-1])
        score_cross = self.depth_scale * score_cross
        return {
            "logit": base_logit + score_cross,
            "score_degree": score_degree,
            "score_cn": score_cn,
            "score_residual": score_residual,
            "score_interaction": score_interaction,
            "score_cross_depth": score_cross,
            "depth_cross_norm": (early_state - late_state).detach().norm(dim=-1),
            "interaction_share": torch.zeros_like(base_logit),
            "z_degree": z_degree,
            "z_cn": z_cn,
            "z_residual": z_residual,
            **cn_statistics,
        }
