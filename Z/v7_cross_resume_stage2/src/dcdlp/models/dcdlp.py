from __future__ import annotations

import torch
from torch import nn

from .branches import CNBranch, DegreeBranch, ResidualBranch
from .hypergraph import (
    ARHC_MODES,
    ARPM_MODES,
    AnchorRelationalPairMoment,
    AnchorRoleHypergraph,
    HYPERGRAPH_CONSTRUCTIONS,
    HYPERGRAPH_MODES,
    HyperedgeSupportAlignment,
    IncidenceResidualComplement,
    LinkHyperedgeRouter,
    PMHE_MODES,
    PairwiseMomentHypergraph,
)
from .losses import interaction_share
from .node_encoder import NodeEncoder, mask_pair_edges


class DCDLP(nn.Module):
    def __init__(
        self, input_dim: int, hidden_dim: int = 128, branch_dim: int = 64,
        num_layers: int = 2, dropout: float = 0.3, backbone: str = "gcn",
        use_interaction: bool = True, use_aa_ra: bool = False,
        active_branches: tuple[str, ...] = ("degree", "cn", "residual"),
        decoder_mode: str = "additive",
        cn_feature_mode: str = "raw",
        cn_regressor: object | None = None,
        interaction_mode: str = "unrestricted",
        cn_input_schema: str = "selective_v1",
        hypergraph_mode: str = "disabled",
        hypergraph_construction: str = "raw_star",
        ghhr_enabled: bool = False,
        complementarity_fusion_mode: str = "none",
        fusion_gate_hidden_dim: int = 8,
        fusion_margin_graph_threshold: float = 0.0,
        fusion_margin_hypergraph_threshold: float = 0.0,
    ) -> None:
        super().__init__()
        if interaction_mode not in {"unrestricted", "audited", "disabled"}:
            raise ValueError(
                "interaction_mode must be unrestricted, audited, or disabled"
            )
        if hypergraph_mode not in HYPERGRAPH_MODES:
            raise ValueError(
                f"Unknown hypergraph_mode {hypergraph_mode!r}; expected one of "
                f"{sorted(HYPERGRAPH_MODES)}"
            )
        if hypergraph_construction not in HYPERGRAPH_CONSTRUCTIONS:
            raise ValueError(
                f"Unknown hypergraph_construction {hypergraph_construction!r}; expected one of "
                f"{sorted(HYPERGRAPH_CONSTRUCTIONS)}"
            )
        if ghhr_enabled and hypergraph_mode != "raw":
            raise ValueError("GHHR requires hypergraph_mode='raw'")
        if complementarity_fusion_mode not in {"none", "average", "global", "gate", "daf"}:
            raise ValueError(
                "complementarity_fusion_mode must be none, average, global, gate, or daf"
            )
        if complementarity_fusion_mode != "none" and hypergraph_mode != "raw":
            raise ValueError("complementarity fusion requires hypergraph_mode='raw'")
        if fusion_gate_hidden_dim < 1:
            raise ValueError("fusion_gate_hidden_dim must be positive")
        self.node_encoder = NodeEncoder(input_dim, hidden_dim, num_layers, dropout, backbone)
        self.degree_branch = DegreeBranch(branch_dim, dropout)
        self.cn_branch = CNBranch(
            hidden_dim,
            branch_dim,
            dropout,
            use_aa_ra,
            cn_feature_mode=cn_feature_mode,
            cn_regressor=cn_regressor,
            cn_input_schema=cn_input_schema,
        )
        self.residual_branch = ResidualBranch(hidden_dim, branch_dim, dropout)
        self.active_branches = set(active_branches)
        self.decoder_mode = decoder_mode
        self.cn_feature_mode = cn_feature_mode
        self.cn_input_schema = cn_input_schema
        self.hypergraph_mode = hypergraph_mode
        self.hypergraph_construction = hypergraph_construction
        self.ghhr_enabled = bool(ghhr_enabled)
        self.complementarity_fusion_mode = complementarity_fusion_mode
        self.fusion_margin_graph_threshold = float(fusion_margin_graph_threshold)
        self.fusion_margin_hypergraph_threshold = float(fusion_margin_hypergraph_threshold)
        self.hypergraph = (
            None
            if hypergraph_mode == "disabled" or hypergraph_mode in {"random_topk", "global_router", "lchr"}
            else IncidenceResidualComplement(
                hidden_dim,
                "raw" if hypergraph_mode in {"hsa", "hsa_shuffled"} | ARHC_MODES | PMHE_MODES | ARPM_MODES else hypergraph_mode,
                hypergraph_construction,
            )
        )
        self.link_router = (
            LinkHyperedgeRouter(hidden_dim, branch_dim, hypergraph_mode)
            if hypergraph_mode in {"random_topk", "global_router", "lchr"} else None
        )
        self.interaction_mode = (
            interaction_mode if use_interaction else "disabled"
        )
        self.concat_decoder = nn.Linear(branch_dim * 3, 1)
        self.interaction = nn.Parameter(torch.empty(branch_dim, branch_dim))
        nn.init.xavier_uniform_(self.interaction)
        interaction_enabled = self.interaction_mode != "disabled"
        self.interaction_scale = nn.Parameter(
            torch.tensor(0.1 if interaction_enabled else 0.0),
            requires_grad=interaction_enabled,
        )
        self.interaction.requires_grad_(interaction_enabled)
        self.bias = nn.Parameter(torch.zeros(()))
        # Initialize the auxiliary scorer after all raw-model modules so its
        # random draws cannot perturb the baseline decoder initialization.
        self.support_alignment = (
            HyperedgeSupportAlignment(hidden_dim, hypergraph_mode)
            if hypergraph_mode in {"hsa", "hsa_shuffled"} else None
        )
        # Build ARHC after all baseline modules so a fixed seed leaves the raw
        # encoder, decoder, and interaction initialization unchanged.
        self.anchor_role = (
            AnchorRoleHypergraph(hidden_dim, hypergraph_mode)
            if hypergraph_mode in ARHC_MODES else None
        )
        self.pair_moment = (
            PairwiseMomentHypergraph(hidden_dim, hypergraph_mode)
            if hypergraph_mode in PMHE_MODES else None
        )
        self.anchor_pair_moment = (
            AnchorRelationalPairMoment(hidden_dim, hypergraph_mode)
            if hypergraph_mode in ARPM_MODES else None
        )
        # A unit-initialized scalar makes the GHHR path reproduce the current
        # Raw-HG final logit before training, without changing baseline init.
        self.ghhr_beta = (
            nn.Parameter(torch.ones(())) if self.ghhr_enabled else None
        )
        self.fusion_global_logit = (
            nn.Parameter(torch.zeros(()))
            if complementarity_fusion_mode == "global" else None
        )
        self.fusion_gate = (
            nn.Sequential(
                nn.Linear(5, fusion_gate_hidden_dim),
                nn.ReLU(),
                nn.Linear(fusion_gate_hidden_dim, 1),
            )
            if complementarity_fusion_mode in {"gate", "daf"} else None
        )

    def _score_state(
        self,
        h: torch.Tensor,
        pairs: torch.Tensor,
        neighbors: list[set[int]],
        degrees: torch.Tensor,
        edge_index: torch.Tensor,
        apply_router: bool,
    ) -> dict[str, torch.Tensor]:
        z_degree, score_degree = self.degree_branch(degrees, pairs)
        z_cn, score_cn, cn_statistics = self.cn_branch(
            h, pairs, neighbors, degrees
        )
        z_residual, score_residual = self.residual_branch(h, pairs)
        if apply_router and self.link_router is not None:
            routed, _ = self.link_router(h, edge_index, pairs)
            z_residual = z_residual + routed
            score_residual = self.residual_branch.scorer(z_residual).squeeze(-1)
        if "degree" not in self.active_branches:
            z_degree, score_degree = torch.zeros_like(z_degree), torch.zeros_like(score_degree)
        if "cn" not in self.active_branches:
            z_cn, score_cn = torch.zeros_like(z_cn), torch.zeros_like(score_cn)
        if "residual" not in self.active_branches:
            z_residual, score_residual = torch.zeros_like(z_residual), torch.zeros_like(score_residual)
        projected = z_degree @ self.interaction
        raw_interaction = (
            self.interaction_scale
            * (projected * z_cn).sum(-1)
            / z_cn.shape[-1] ** 0.5
        )
        score_interaction = (
            torch.zeros_like(raw_interaction)
            if self.interaction_mode == "disabled"
            else raw_interaction
        )
        if self.decoder_mode == "concat":
            logit = self.concat_decoder(
                torch.cat([z_degree, z_cn, z_residual], dim=-1)
            ).squeeze(-1) + self.bias
        else:
            logit = score_degree + score_cn + score_residual + score_interaction + self.bias
        return {
            "logit": logit,
            "score_degree": score_degree,
            "score_cn": score_cn,
            "score_residual": score_residual,
            "score_interaction": score_interaction,
            "z_degree": z_degree,
            "z_cn": z_cn,
            "z_residual": z_residual,
            **cn_statistics,
        }

    @staticmethod
    def _structure(edge_index: torch.Tensor, num_nodes: int):
        neighbors = [set() for _ in range(num_nodes)]
        for raw_u, raw_v in edge_index.detach().cpu().t().tolist():
            u, v = int(raw_u), int(raw_v)
            neighbors[u].add(v)
            neighbors[v].add(u)
        degrees = torch.as_tensor([len(item) for item in neighbors], dtype=torch.float32, device=edge_index.device)
        return neighbors, degrees

    def forward(
        self, x: torch.Tensor, edge_index: torch.Tensor, pairs: torch.Tensor,
        remove_target_edges: bool = True,
        support_edge_index: torch.Tensor | None = None,
    ) -> dict[str, torch.Tensor]:
        message_edges = mask_pair_edges(edge_index, pairs) if remove_target_edges else edge_index
        node_state = self.node_encoder(x, message_edges)
        h = node_state
        if self.hypergraph is not None:
            h = node_state + self.hypergraph(node_state, message_edges)
        if self.anchor_role is not None:
            h = h + self.anchor_role(node_state, message_edges)
        if self.pair_moment is not None:
            h = h + self.pair_moment(node_state, message_edges)
        if self.anchor_pair_moment is not None:
            h = h + self.anchor_pair_moment(node_state, message_edges)
        neighbors, degrees = self._structure(message_edges, x.shape[0])
        fused = self._score_state(
            h, pairs, neighbors, degrees, message_edges, apply_router=True
        )
        logit = fused["logit"]
        ghhr_scores: dict[str, torch.Tensor] = {}
        graph = None
        if self.ghhr_enabled or self.complementarity_fusion_mode != "none":
            graph = self._score_state(
                node_state, pairs, neighbors, degrees, message_edges,
                apply_router=False,
            )
            residual_score = fused["logit"] - graph["logit"]
            ghhr_scores = {
                "score_graph": graph["logit"],
                "score_hg_residual": residual_score,
                "score_raw_hg": fused["logit"],
            }
            if self.ghhr_enabled:
                effective_residual = self.ghhr_beta * residual_score
                logit = graph["logit"] + effective_residual
                ghhr_scores.update({
                    "score_hg_residual_effective": effective_residual,
                    "ghhr_beta": self.ghhr_beta.expand_as(logit),
                })
        if self.complementarity_fusion_mode != "none":
            if graph is None:
                raise RuntimeError("complementarity fusion is missing the Graph score")
            score_graph = graph["logit"]
            score_raw_hg = fused["logit"]
            disagreement = (score_graph - score_raw_hg).abs()
            margin_graph = score_graph - self.fusion_margin_graph_threshold
            margin_hypergraph = score_raw_hg - self.fusion_margin_hypergraph_threshold
            if self.complementarity_fusion_mode == "average":
                alpha_h = score_graph.new_full(score_graph.shape, 0.5)
            elif self.complementarity_fusion_mode == "global":
                alpha_h = torch.sigmoid(self.fusion_global_logit).expand_as(score_graph)
            else:
                if self.complementarity_fusion_mode == "daf":
                    gate_features = torch.stack([
                        score_graph, score_raw_hg, disagreement,
                        margin_graph, margin_hypergraph,
                    ], dim=-1)
                else:
                    # Same five-input gate parameterization as DAF, with all
                    # disagreement/margin inputs removed for the control.
                    zeros = torch.zeros_like(score_graph)
                    gate_features = torch.stack([
                        score_graph, score_raw_hg, zeros, zeros, zeros,
                    ], dim=-1)
                alpha_h = torch.sigmoid(self.fusion_gate(gate_features).squeeze(-1))
            logit = score_graph + alpha_h * (score_raw_hg - score_graph)
            ghhr_scores.update({
                "fusion_alpha_h": alpha_h,
                "fusion_disagreement": disagreement,
                "fusion_margin_graph": margin_graph,
                "fusion_margin_hypergraph": margin_hypergraph,
            })
        support_aux_loss = h.new_zeros(())
        support_aux_stats = {"pairs": 0, "positive": 0, "negative": 0}
        if self.training and self.support_alignment is not None and support_edge_index is not None:
            support_aux_loss, support_aux_stats = self.support_alignment(
                h, message_edges, support_edge_index, pairs
            )
        score_interaction_share = interaction_share(
            fused["score_degree"], fused["score_cn"], fused["score_residual"], fused["score_interaction"]
        )
        result = {
            **fused,
            "logit": logit,
            "interaction_share": score_interaction_share,
            **ghhr_scores,
        }
        if self.training and self.support_alignment is not None:
            result["support_aux_loss"] = support_aux_loss
            result["support_aux_pairs"] = h.new_tensor(float(support_aux_stats["pairs"]))
        return result
