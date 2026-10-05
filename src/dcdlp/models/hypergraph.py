from __future__ import annotations

"""Small, leakage-safe hypergraph branches for link-prediction ablations.

The branch deliberately uses a fixed incidence construction rather than
attention or a learned edge selector.  A star hyperedge is the closed
neighborhood of one node in the *already target-masked* message graph.  The
``complement`` mode removes the component of the hypergraph message that is
parallel to the pairwise node representation before applying the same linear
map as the raw control.  This makes the mechanism testable as an
"independent higher-order residual" hypothesis.
"""

import torch
from torch import nn
from torch.nn import functional as F
import random
from itertools import combinations
from statistics import mean, median


HYPERGRAPH_MODES = {
    "disabled",
    "raw",
    "complement",
    "pairwise",
    "shuffled",
    "random_topk",
    "global_router",
    "lchr",
    "size_calibration",
    "shuffled_cohesion",
    "sshc",
    "redundancy_calibration",
    "shuffled_redundancy",
    "hsa",
    "hsa_shuffled",
    "arhc_symmetric",
    "arhc_role",
    "arhc_full",
    "arhc_anchor_shuffled",
    "pmhe_mean",
    "pmhe_second",
    "pmhe_pair",
    "arpm_mean",
    "arpm_pair",
    "arpm_anchor_shuffled",
}

ARHC_MODES = {
    "arhc_symmetric",
    "arhc_role",
    "arhc_full",
    "arhc_anchor_shuffled",
}

PMHE_MODES = {"pmhe_mean", "pmhe_second", "pmhe_pair"}
ARPM_MODES = {"arpm_mean", "arpm_pair", "arpm_anchor_shuffled"}


def _star_members(edge_index: torch.Tensor, num_nodes: int) -> list[torch.Tensor]:
    """Build closed-neighborhood hyperedges from the supplied message graph."""
    neighbors = [set() for _ in range(num_nodes)]
    for raw_u, raw_v in edge_index.detach().cpu().t().tolist():
        u, v = int(raw_u), int(raw_v)
        if u == v:
            continue
        neighbors[u].add(v)
        neighbors[v].add(u)
    members: list[torch.Tensor] = []
    for center, values in enumerate(neighbors):
        if not values:
            continue
        members.append(
            torch.as_tensor(
                [center, *sorted(values)],
                dtype=torch.long,
                device=edge_index.device,
            )
        )
    return members


HYPERGRAPH_CONSTRUCTIONS = {
    "raw_star",
    "ecph_random",
    "ecph_degree",
    "ecph_true",
    "ecnh_random",
    "ecnh_union",
    "ecnh_true",
    "owh_random",
    "owh_closed",
    "owh_open",
}
ECNH_CONSTRUCTIONS = {"ecnh_random", "ecnh_union", "ecnh_true"}
ECNH_CN_CAP = 16
OWH_CONSTRUCTIONS = {"owh_random", "owh_closed", "owh_open"}
OWH_WEDGES_PER_CENTER = 32


def _message_neighbors(edge_index: torch.Tensor, num_nodes: int) -> list[set[int]]:
    neighbors = [set() for _ in range(num_nodes)]
    for raw_u, raw_v in edge_index.detach().cpu().t().tolist():
        u, v = int(raw_u), int(raw_v)
        if u == v:
            continue
        neighbors[u].add(v)
        neighbors[v].add(u)
    return neighbors


def _ego_components(neighbors: list[set[int]], center: int) -> list[list[int]]:
    """Connected components of G[N(center)], ordered deterministically."""
    unseen = set(neighbors[center])
    components: list[list[int]] = []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        stack = [start]
        component = [start]
        while stack:
            node = stack.pop()
            reached = neighbors[node] & unseen
            if reached:
                unseen.difference_update(reached)
                stack.extend(sorted(reached, reverse=True))
                component.extend(reached)
        components.append(sorted(component))
    return sorted(components, key=lambda group: (group[0], len(group), tuple(group)))


def _partition_groups(
    neighbors: list[set[int]], center: int, components: list[list[int]], construction: str
) -> list[list[int]]:
    sizes = sorted((len(group) for group in components if len(group) >= 2), reverse=True)
    if not sizes or construction == "raw_star":
        return []
    if construction == "ecph_true":
        return [group for group in components if len(group) >= 2]
    values = sorted(neighbors[center])
    if construction == "ecph_random":
        random.Random(12345 + center).shuffle(values)
    elif construction == "ecph_degree":
        degree = [len(row) for row in neighbors]
        values.sort(key=lambda node: (degree[node], node))
    else:
        raise ValueError(f"Unknown hypergraph_construction {construction!r}")
    groups: list[list[int]] = []
    cursor = 0
    for size in sizes:
        groups.append(sorted(values[cursor:cursor + size]))
        cursor += size
    return groups


def _edge_centered_groups(
    neighbors: list[set[int]], construction: str, cap: int = ECNH_CN_CAP
) -> list[tuple[int, int, list[int]]]:
    """Build deterministic common-neighbor groups and count-matched controls.

    The true construction starts with one proposal per eligible observed edge
    and canonicalizes it later. Controls are attached one-to-one to unique
    true additions after raw-star collisions and duplicate true groups have
    been removed, so their count and size multiset match what the encoder
    actually receives.
    """
    if construction not in ECNH_CONSTRUCTIONS:
        raise ValueError(f"Unknown edge-centered construction {construction!r}")
    num_nodes = len(neighbors)
    degrees = [len(row) for row in neighbors]
    raw_keys = {
        tuple(sorted((center, *row)))
        for center, row in enumerate(neighbors) if row
    }
    groups: list[tuple[int, int, list[int]]] = []
    matched_bases: list[tuple[int, int, list[int]]] = []
    seen_true_additions: set[tuple[int, ...]] = set()
    for u in range(num_nodes):
        for v in sorted(neighbors[u]):
            if u >= v:
                continue
            common = neighbors[u] & neighbors[v]
            if not common:
                continue
            size = min(len(common), cap)
            selected_true = sorted(common, key=lambda node: (degrees[node], node))[:size]
            groups.append((u, v, selected_true))
            true_key = tuple(sorted((u, v, *selected_true)))
            if true_key not in raw_keys and true_key not in seen_true_additions:
                seen_true_additions.add(true_key)
                matched_bases.append((u, v, selected_true))
    if construction == "ecnh_true":
        return groups

    controls: list[tuple[int, int, list[int]]] = []
    seen_control: set[tuple[int, ...]] = set(raw_keys)
    for u, v, true_members in matched_bases:
        size = len(true_members)
        if construction == "ecnh_random":
            candidates = [node for node in range(num_nodes) if node not in {u, v}]
            seed = 2246822519 + u * 1000003 + v
        else:
            candidates = sorted((neighbors[u] | neighbors[v]) - {u, v})
            seed = 3266489917 + u * 1000003 + v
        chosen = None
        for attempt in range(128):
            shuffled = list(candidates)
            random.Random(seed + attempt * 104729).shuffle(shuffled)
            selected = sorted(shuffled[:size])
            key = tuple(sorted((u, v, *selected)))
            if len(selected) == size and key not in seen_control:
                chosen = selected
                seen_control.add(key)
                break
        if chosen is None:
            # A tiny or highly constrained graph may not have enough unique
            # control sets; keep the deterministic first sample and let the
            # construction audit expose the resulting collision.
            shuffled = list(candidates)
            random.Random(seed).shuffle(shuffled)
            chosen = sorted(shuffled[:size])
        controls.append((u, v, chosen))
    return controls


def _open_wedge_groups(
    neighbors: list[set[int]], cap: int = OWH_WEDGES_PER_CENTER
) -> tuple[list[tuple[int, int, int]], int, int]:
    """Return capped open wedges as (center, endpoint_u, endpoint_v)."""
    degrees = [len(row) for row in neighbors]
    groups: list[tuple[int, int, int]] = []
    candidate_count = 0
    refined_centers = 0
    for center, row in enumerate(neighbors):
        open_pairs = [
            (u, v) for u, v in combinations(sorted(row), 2)
            if v not in neighbors[u]
        ]
        candidate_count += len(open_pairs)
        if open_pairs:
            refined_centers += 1
        open_pairs.sort(key=lambda pair: (degrees[pair[0]] * degrees[pair[1]], pair[0], pair[1]))
        groups.extend((center, u, v) for u, v in open_pairs[:cap])
    return groups, candidate_count, refined_centers


def _closed_triangle_groups(neighbors: list[set[int]]) -> list[tuple[int, int, int]]:
    groups: list[tuple[int, int, int]] = []
    for center, row in enumerate(neighbors):
        for u, v in combinations(sorted(row), 2):
            if v in neighbors[u]:
                groups.append((center, u, v))
    return groups


def _random_triples(
    num_nodes: int, count: int, forbidden: set[tuple[int, ...]], seed: int = 2135587861
) -> list[tuple[int, int, int]]:
    """Deterministic unique random triples, avoiding Raw and prior triples."""
    if count <= 0 or num_nodes < 3:
        return []
    rng = random.Random(seed)
    seen = set(forbidden)
    groups: list[tuple[int, int, int]] = []
    attempts = 0
    max_attempts = max(1000, count * 32)
    while len(groups) < count and attempts < max_attempts:
        attempts += 1
        triple = tuple(sorted(rng.sample(range(num_nodes), 3)))
        if triple in seen:
            continue
        seen.add(triple)
        groups.append(triple)
    if len(groups) < count:
        for triple in combinations(range(num_nodes), 3):
            if triple in seen:
                continue
            seen.add(triple)
            groups.append(triple)
            if len(groups) == count:
                break
    return groups


def build_hyperedges(
    edge_index: torch.Tensor, num_nodes: int, construction: str = "raw_star"
) -> list[torch.Tensor]:
    """Build raw stars, optionally augmented with ECPH-style ego groups.

    ``edge_index`` is the caller's message graph. The model passes its
    already target-masked graph here, so every construction uses the same
    leakage boundary as the raw stars.
    """
    if construction not in HYPERGRAPH_CONSTRUCTIONS:
        raise ValueError(
            f"Unknown hypergraph_construction {construction!r}; expected one of "
            f"{sorted(HYPERGRAPH_CONSTRUCTIONS)}"
        )
    raw = _star_members(edge_index, num_nodes)
    if construction == "raw_star":
        return raw

    neighbors = _message_neighbors(edge_index, num_nodes)
    seen = {tuple(sorted(edge.detach().cpu().tolist())) for edge in raw}
    additions: list[torch.Tensor] = []
    if construction in ECNH_CONSTRUCTIONS:
        for u, v, selected in _edge_centered_groups(neighbors, construction):
            members = tuple(sorted((u, v, *selected)))
            if members in seen:
                continue
            seen.add(members)
            additions.append(torch.as_tensor(members, dtype=torch.long, device=edge_index.device))
        return [*raw, *additions]

    if construction in OWH_CONSTRUCTIONS:
        raw_keys = set(seen)
        open_groups, _, _ = _open_wedge_groups(neighbors)
        if construction == "owh_open":
            groups = open_groups
        elif construction == "owh_closed":
            groups = _closed_triangle_groups(neighbors)
        else:
            unique_open = {
                tuple(sorted(group)) for group in open_groups
                if tuple(sorted(group)) not in raw_keys
            }
            groups = _random_triples(num_nodes, len(unique_open), raw_keys)
        for group in groups:
            members = tuple(sorted(group))
            if members in seen:
                continue
            seen.add(members)
            additions.append(torch.as_tensor(members, dtype=torch.long, device=edge_index.device))
        return [*raw, *additions]

    for center in range(num_nodes):
        components = _ego_components(neighbors, center)
        groups = _partition_groups(neighbors, center, components, construction)
        for group in groups:
            members = tuple(sorted((center, *group)))
            if members in seen:
                continue
            seen.add(members)
            additions.append(torch.as_tensor(members, dtype=torch.long, device=edge_index.device))
    return [*raw, *additions]


def construction_statistics(
    edge_index: torch.Tensor, num_nodes: int, construction: str
) -> dict[str, object]:
    """Describe the construction on one supplied message graph."""
    raw = _star_members(edge_index, num_nodes)
    neighbors = _message_neighbors(edge_index, num_nodes)
    if construction in ECNH_CONSTRUCTIONS:
        groups = _edge_centered_groups(neighbors, construction)
        eligible_edge_count = len(_edge_centered_groups(neighbors, "ecnh_true"))
        raw_keys = {tuple(sorted(edge.detach().cpu().tolist())) for edge in raw}
        unique_additions: set[tuple[int, ...]] = set()
        covered: set[int] = set()
        sizes: list[int] = []
        for u, v, selected in groups:
            members = tuple(sorted((u, v, *selected)))
            if members not in raw_keys:
                if members not in unique_additions:
                    unique_additions.add(members)
                    sizes.append(len(members))
                    covered.update(members)
        added_incidence_count = sum(len(edge) for edge in unique_additions)
        return {
            "construction": construction,
            "raw_hyperedge_count": len(raw),
            "raw_incidence_count": sum(len(edge) for edge in raw),
            "requested_edge_centered_hyperedge_count": len(groups),
            "added_hyperedge_count": len(unique_additions),
            "added_incidence_count": added_incidence_count,
            "total_hyperedge_count": len(raw) + len(unique_additions),
            "total_incidence_count": sum(len(edge) for edge in raw) + added_incidence_count,
            "edge_centered_edges_with_common_neighbors": eligible_edge_count,
            "matched_group_proposal_count": len(groups),
            "canonical_duplicate_or_raw_collision_count": len(groups) - len(unique_additions),
            "common_neighbor_cap": ECNH_CN_CAP,
            "added_hyperedge_size": {
                "count": len(sizes),
                "mean": mean(sizes) if sizes else 0.0,
                "median": median(sizes) if sizes else 0.0,
                "p90": float(torch.tensor(sorted(sizes), dtype=torch.float32).quantile(0.9).item()) if sizes else 0.0,
                "max": max(sizes) if sizes else 0,
            },
            "component_node_coverage_ratio": len(covered) / num_nodes if num_nodes else 0.0,
        }
    if construction in OWH_CONSTRUCTIONS:
        open_groups, open_candidate_count, open_center_count = _open_wedge_groups(neighbors)
        closed_groups = _closed_triangle_groups(neighbors)
        raw_keys = {tuple(sorted(edge.detach().cpu().tolist())) for edge in raw}
        true_additions = {
            tuple(sorted(group)) for group in open_groups
            if tuple(sorted(group)) not in raw_keys
        }
        if construction == "owh_open":
            groups = open_groups
        elif construction == "owh_closed":
            groups = closed_groups
        else:
            groups = _random_triples(num_nodes, len(true_additions), raw_keys)
        unique_additions: set[tuple[int, ...]] = set()
        covered: set[int] = set()
        sizes: list[int] = []
        for group in groups:
            members = tuple(sorted(group))
            if members not in raw_keys and members not in unique_additions:
                unique_additions.add(members)
                sizes.append(len(members))
                covered.update(members)
        added_incidence_count = sum(len(edge) for edge in unique_additions)
        return {
            "construction": construction,
            "raw_hyperedge_count": len(raw),
            "raw_incidence_count": sum(len(edge) for edge in raw),
            "requested_hyperedge_proposal_count": len(groups),
            "open_wedge_candidate_count_before_cap": open_candidate_count,
            "selected_open_wedge_proposal_count": len(open_groups),
            "selected_open_wedge_center_count": open_center_count,
            "per_center_wedge_cap": OWH_WEDGES_PER_CENTER,
            "priority": "endpoint_degree_product_ascending_then_node_ids",
            "closed_triangle_proposal_count": len(closed_groups),
            "matched_open_wedge_unique_addition_count": len(true_additions),
            "added_hyperedge_count": len(unique_additions),
            "added_incidence_count": added_incidence_count,
            "total_hyperedge_count": len(raw) + len(unique_additions),
            "total_incidence_count": sum(len(edge) for edge in raw) + added_incidence_count,
            "canonical_duplicate_or_raw_collision_count": len(groups) - len(unique_additions),
            "added_hyperedge_size": {
                "count": len(sizes),
                "mean": mean(sizes) if sizes else 0.0,
                "median": median(sizes) if sizes else 0.0,
                "p90": float(torch.tensor(sorted(sizes), dtype=torch.float32).quantile(0.9).item()) if sizes else 0.0,
                "max": max(sizes) if sizes else 0,
            },
            "added_node_coverage_ratio": len(covered) / num_nodes if num_nodes else 0.0,
        }
    degrees = [len(row) for row in neighbors]
    true_components = [_ego_components(neighbors, center) for center in range(num_nodes)]
    group_sizes: list[int] = []
    group_densities: list[float] = []
    refined_centers = 0
    covered: set[int] = set()
    requested_count = 0
    unique_additions: set[tuple[int, ...]] = set()
    raw_keys = {tuple(sorted(edge.detach().cpu().tolist())) for edge in raw}
    for center, components in enumerate(true_components):
        groups = _partition_groups(neighbors, center, components, construction)
        if groups:
            refined_centers += 1
        for group in groups:
            if len(group) < 2:
                continue
            requested_count += 1
            group_sizes.append(len(group))
            possible = len(group) * (len(group) - 1) // 2
            observed = sum(1 for i, u in enumerate(group) for v in group[i + 1:] if v in neighbors[u])
            group_densities.append(observed / possible if possible else 0.0)
            members = tuple(sorted((center, *group)))
            covered.update(members)
            if members not in raw_keys:
                unique_additions.add(members)
    component_count_per_center = [sum(len(group) >= 2 for group in parts) for parts in true_components]
    unique_incidence_count = sum(len(edge) for edge in unique_additions)
    sizes_sorted = sorted(group_sizes)
    return {
        "construction": construction,
        "raw_hyperedge_count": len(raw),
        "raw_incidence_count": sum(len(edge) for edge in raw),
        "requested_component_hyperedge_count": requested_count,
        "added_hyperedge_count": len(unique_additions),
        "added_incidence_count": unique_incidence_count,
        "total_hyperedge_count": len(raw) + len(unique_additions),
        "total_incidence_count": sum(len(edge) for edge in raw) + unique_incidence_count,
        "average_component_count_per_node": mean(component_count_per_center) if component_count_per_center else 0.0,
        "average_component_count_per_nonisolated_center": (
            mean(component_count_per_center[node] for node in range(num_nodes) if degrees[node])
            if any(degrees) else 0.0
        ),
        "component_size": {
            "count": len(group_sizes),
            "mean": mean(group_sizes) if group_sizes else 0.0,
            "median": median(group_sizes) if group_sizes else 0.0,
            "p90": float(torch.tensor(sizes_sorted, dtype=torch.float32).quantile(0.9).item()) if sizes_sorted else 0.0,
            "max": max(group_sizes) if group_sizes else 0,
        },
        "refined_center_count": refined_centers,
        "refined_center_ratio_all_nodes": refined_centers / num_nodes if num_nodes else 0.0,
        "refined_center_ratio_nonisolated": (
            refined_centers / sum(bool(degree) for degree in degrees) if any(degrees) else 0.0
        ),
        "component_node_coverage_ratio": len(covered) / num_nodes if num_nodes else 0.0,
        "mean_internal_density_in_group_members": mean(group_densities) if group_densities else 0.0,
        "group_internal_density_count": len(group_densities),
    }


def _aggregate_incidence(
    h: torch.Tensor,
    hyperedges: list[torch.Tensor],
    *,
    pairwise_projection: bool,
    edge_weights: torch.Tensor | None = None,
) -> torch.Tensor:
    """Apply an unweighted incidence aggregation without materializing H."""
    output = h.new_zeros(h.shape)
    counts = h.new_zeros((h.shape[0], 1))
    for edge_id, members in enumerate(hyperedges):
        values = h[members]
        if pairwise_projection:
            if len(members) <= 1:
                continue
            # Projection control: retain the same hyperedge membership but
            # replace the set-valued message by its ordinary pairwise
            # co-membership average.
            contribution = (values.sum(dim=0, keepdim=True) - values) / (len(members) - 1)
        else:
            summary = values.mean(dim=0, keepdim=True)
            contribution = summary.expand(len(members), -1)
        if edge_weights is not None:
            contribution = contribution * edge_weights[edge_id]
        output.index_add_(0, members, contribution)
        counts.index_add_(
            0,
            members,
            h.new_ones((len(members), 1)),
        )
    return output / counts.clamp_min(1.0)


class IncidenceResidualComplement(nn.Module):
    """Standard hypergraph control plus a pairwise-complement residual mode.

    ``raw`` is the hypergraph-only control.  ``pairwise`` is a matched
    ordinary co-membership projection.  ``shuffled`` preserves the raw
    message distribution but breaks its node assignment.  ``complement``
    subtracts the per-node projection onto the pairwise encoder state before
    applying the same trainable map as ``raw``.
    """

    def __init__(
        self, hidden_dim: int, mode: str = "complement",
        construction: str = "raw_star",
    ) -> None:
        super().__init__()
        if mode not in HYPERGRAPH_MODES - {"disabled"}:
            raise ValueError(
                f"Unknown hypergraph_mode {mode!r}; expected one of "
                f"{sorted(HYPERGRAPH_MODES)}"
            )
        self.mode = mode
        if construction not in HYPERGRAPH_CONSTRUCTIONS:
            raise ValueError(
                f"Unknown hypergraph_construction {construction!r}; expected one of "
                f"{sorted(HYPERGRAPH_CONSTRUCTIONS)}"
            )
        self.construction = construction
        self.message_linear = nn.Linear(hidden_dim, hidden_dim, bias=False)
        # A near-zero sigmoid coefficient makes the calibrated modes start
        # almost exactly at the raw global hypergraph branch.
        # Candidate A's single allowed numerical stability correction:
        # a modest 4.7% initial scale keeps the branch near raw propagation
        # while providing a useful gradient at the one-epoch screen budget.
        self.calibration_logit = nn.Parameter(torch.tensor(-3.0))

    @staticmethod
    def _standardized_structure(
        edge_index: torch.Tensor, hyperedges: list[torch.Tensor], signal: str
    ) -> torch.Tensor:
        num_nodes = int(edge_index.max().item()) + 1 if edge_index.numel() else 0
        neighbors = [set() for _ in range(num_nodes)]
        for u, v in edge_index.detach().cpu().t().tolist():
            neighbors[u].add(v)
            neighbors[v].add(u)
        values = []
        if signal in {"redundancy", "shuffled_redundancy"}:
            edge_sets = [set(members.detach().cpu().tolist()) for members in hyperedges]
            incident = [[] for _ in range(num_nodes)]
            for edge_id, edge in enumerate(edge_sets):
                for node in edge:
                    incident[node].append(edge_id)
            for edge_id, edge in enumerate(edge_sets):
                nearby = set()
                for node in edge:
                    nearby.update(incident[node])
                nearby.discard(edge_id)
                overlaps = sorted(
                    (len(edge & edge_sets[other]) / len(edge | edge_sets[other])
                     for other in nearby), reverse=True
                )
                values.append(float(sum(overlaps[:3]) / min(3, len(overlaps))) if overlaps else 0.0)
            signal = "shuffled" if signal == "shuffled_redundancy" else signal
        else:
            edge_sets = None
        for members in hyperedges:
            if edge_sets is not None:
                break
            ids = members.detach().cpu().tolist()
            if signal == "size":
                values.append(float(torch.log1p(torch.tensor(float(len(ids))))))
                continue
            center, leaves = ids[0], ids[1:]
            possible = len(leaves) * (len(leaves) - 1) // 2
            closed_pairs = sum(
                1 for i, u in enumerate(leaves)
                for v in leaves[i + 1:] if v in neighbors[u]
            )
            values.append(closed_pairs / possible if possible else 0.0)
        feature = torch.as_tensor(values, dtype=torch.float32, device=edge_index.device)
        if signal == "shuffled" and len(feature) > 1:
            generator = torch.Generator(device="cpu").manual_seed(0)
            order = torch.randperm(len(feature), generator=generator).to(feature.device)
            feature = feature[order]
        return (feature - feature.mean()) / feature.std(unbiased=False).clamp_min(1e-8)

    def forward(self, h: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        hyperedges = build_hyperedges(edge_index, h.shape[0], self.construction)
        weights = None
        if self.mode in {"size_calibration", "shuffled_cohesion", "sshc",
                         "redundancy_calibration", "shuffled_redundancy"}:
            signal = {
                "size_calibration": "size",
                "shuffled_cohesion": "shuffled",
                "sshc": "cohesion",
                "redundancy_calibration": "redundancy",
                "shuffled_redundancy": "shuffled_redundancy",
            }[self.mode]
            feature = self._standardized_structure(edge_index, hyperedges, signal)
            coefficient = torch.sigmoid(self.calibration_logit)
            if self.mode in {"redundancy_calibration", "shuffled_redundancy", "size_calibration"}:
                coefficient = 0.5 * coefficient
                weights = 1.0 - coefficient * torch.tanh(feature)
            else:
                weights = 1.0 + coefficient * torch.tanh(feature)
        raw = _aggregate_incidence(
            h,
            hyperedges,
            pairwise_projection=self.mode == "pairwise",
            edge_weights=weights,
        )
        if self.mode == "complement":
            coefficient = (raw * h).sum(dim=-1, keepdim=True)
            denominator = h.square().sum(dim=-1, keepdim=True).clamp_min(1e-8)
            raw = raw - coefficient / denominator * h
        elif self.mode == "shuffled" and len(raw) > 1:
            raw = torch.roll(raw, shifts=1, dims=0)
        return self.message_linear(raw)


class LinkHyperedgeRouter(nn.Module):
    """Candidate-local star-hyperedge context from the masked message graph."""

    def __init__(self, hidden_dim: int, branch_dim: int, mode: str, topk: int = 8):
        super().__init__()
        if mode not in {"random_topk", "global_router", "lchr"}:
            raise ValueError(mode)
        self.mode, self.topk = mode, topk
        self.router = nn.Sequential(
            nn.Linear(hidden_dim * 5 + 5, hidden_dim), nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )
        self.projection = nn.Linear(hidden_dim, branch_dim, bias=False)
        self.beta = nn.Parameter(torch.tensor(0.1))
        self.last_diagnostics: dict[str, object] = {}

    def forward(self, h: torch.Tensor, edge_index: torch.Tensor,
                pairs: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        members = _star_members(edge_index, h.shape[0])
        zero = h.new_zeros((len(pairs), self.projection.out_features))
        if not members:
            self.last_diagnostics = {"pool_sizes": [0] * len(pairs), "entropy": [0.0] * len(pairs)}
            return zero, h.new_zeros(len(pairs))
        edge_repr = torch.stack([h[item].mean(0) for item in members])
        member_sets = [set(item.tolist()) for item in members]
        incident = [[] for _ in range(h.shape[0])]
        neighbors = [set() for _ in range(h.shape[0])]
        for eid, item in enumerate(member_sets):
            for node in item:
                incident[node].append(eid)
        for u, v in edge_index.detach().cpu().t().tolist():
            neighbors[u].add(v)
            neighbors[v].add(u)
        chosen, structural, pool_sizes = [], [], []
        for u, v in pairs.detach().cpu().tolist():
            pool = sorted(set(incident[u]) | set(incident[v]))
            pool_sizes.append(len(pool))
            if len(pool) > 32:
                pool = sorted(pool, key=lambda e: (-(len(member_sets[e] & neighbors[u]) +
                                                     len(member_sets[e] & neighbors[v])), e))[:32]
            if self.mode == "random_topk":
                pool = sorted(pool, key=lambda e: ((u * 73856093 ^ v * 19349663 ^ e * 83492791) & 0xffffffff))[:self.topk]
            features = []
            for eid in pool:
                group = member_sets[eid]
                features.append([float(u in group), float(v in group),
                                 len(group & neighbors[u]) / max(1, len(neighbors[u])),
                                 len(group & neighbors[v]) / max(1, len(neighbors[v])),
                                 len(group) / max(1, h.shape[0])])
            chosen.append(pool)
            structural.append(features)
        width = min(self.topk, max(map(len, chosen), default=0))
        if width == 0:
            self.last_diagnostics = {"pool_sizes": pool_sizes, "entropy": [0.0] * len(pairs)}
            return zero, h.new_zeros(len(pairs))
        ids = torch.zeros((len(pairs), width), dtype=torch.long, device=h.device)
        phi = h.new_zeros((len(pairs), width, 5))
        mask = torch.zeros((len(pairs), width), dtype=torch.bool, device=h.device)
        # Score all prefiltered candidates before choosing the learned Top-K.
        scores = []
        for i, pool in enumerate(chosen):
            if not pool:
                scores.append(h.new_empty(0))
                continue
            e = edge_repr[pool]
            u, v = pairs[i]
            q = torch.cat([h[u], h[v], h[u] * h[v], (h[u] - h[v]).abs()])
            f = h.new_tensor(structural[i])
            if self.mode == "global_router":
                q = torch.zeros_like(q)
                f = torch.zeros_like(f)
            logits = self.router(torch.cat([e, q.expand(len(pool), -1), f], -1)).squeeze(-1)
            scores.append(logits)
            selected = torch.topk(logits, min(width, len(pool))).indices if self.mode != "random_topk" else torch.arange(min(width, len(pool)), device=h.device)
            count = len(selected)
            ids[i, :count] = torch.as_tensor(pool, device=h.device)[selected]
            phi[i, :count] = f[selected]
            mask[i, :count] = True
        z = edge_repr[ids]
        rows = []
        for i, pool in enumerate(chosen):
            if not pool:
                rows.append(h.new_zeros(width))
                continue
            selected = torch.topk(scores[i], min(width, len(pool))).indices if self.mode != "random_topk" else torch.arange(min(width, len(pool)), device=h.device)
            row = h.new_full((width,), -1e9)
            row[:len(selected)] = scores[i][selected] if self.mode != "random_topk" else 0.0
            rows.append(row)
        logits = torch.stack(rows)
        alpha = torch.softmax(logits.masked_fill(~mask, -1e9), -1)
        alpha = torch.where(mask, alpha, 0.0)
        context = (alpha.unsqueeze(-1) * z).sum(1)
        entropy = -(alpha * alpha.clamp_min(1e-12).log()).sum(-1)
        self.last_diagnostics = {"pool_sizes": pool_sizes, "entropy": entropy.detach().cpu().tolist(),
                                 "top1": alpha.max(-1).values.detach().cpu().tolist(),
                                 "weights": [
                                     [[sorted(member_sets[int(ids[i, j])]),
                                       float(alpha[i, j].detach().cpu())]
                                      for j in range(width) if bool(mask[i, j])]
                                     for i in range(len(pairs))
                                 ]}
        return self.beta * self.projection(context), entropy


class HyperedgeSupportAlignment(nn.Module):
    """Small leaf-pair auxiliary scorer; center-leaf pairs are never sampled."""

    def __init__(self, hidden_dim: int, mode: str, per_class: int = 4):
        super().__init__()
        self.shuffled = mode == "hsa_shuffled"
        self.per_class = per_class
        self.scorer = nn.Sequential(
            nn.Linear(hidden_dim * 3, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(
        self,
        h: torch.Tensor,
        message_edge_index: torch.Tensor,
        support_edge_index: torch.Tensor,
        target_pairs: torch.Tensor,
    ) -> tuple[torch.Tensor, dict[str, int]]:
        hyperedges = _star_members(message_edge_index, h.shape[0])
        graph_positive = {
            tuple(sorted((int(u), int(v))))
            for u, v in support_edge_index.detach().cpu().t().tolist()
        }
        excluded = {
            tuple(sorted((int(u), int(v))))
            for u, v in target_pairs.detach().cpu().tolist()
        }
        selected_pairs, edge_ids, labels = [], [], []
        for edge_id, members in enumerate(hyperedges):
            leaves = members.detach().cpu().tolist()[1:]
            positive, negative = [], []
            for u, v in combinations(leaves, 2):
                pair = (min(u, v), max(u, v))
                if pair in excluded:
                    continue
                (positive if pair in graph_positive else negative).append(pair)
            count = min(self.per_class, len(positive), len(negative))
            if count == 0:
                continue
            chosen = random.sample(positive, count) + random.sample(negative, count)
            selected_pairs.extend(chosen)
            edge_ids.extend([edge_id] * (2 * count))
            labels.extend([1.0] * count + [0.0] * count)
        if not selected_pairs:
            return h.new_zeros(()), {"pairs": 0, "positive": 0, "negative": 0}
        if self.shuffled:
            order = torch.randperm(len(labels)).tolist()
            labels = [labels[index] for index in order]
        pair_tensor = torch.as_tensor(selected_pairs, dtype=torch.long, device=h.device)
        edge_repr = torch.stack([h[item].mean(0) for item in hyperedges])
        pair_repr = torch.cat([
            h[pair_tensor[:, 0]] * h[pair_tensor[:, 1]],
            (h[pair_tensor[:, 0]] - h[pair_tensor[:, 1]]).abs(),
        ], dim=-1)
        inputs = torch.cat([edge_repr[torch.as_tensor(edge_ids, device=h.device)], pair_repr], dim=-1)
        logits = self.scorer(inputs).squeeze(-1)
        label_tensor = torch.as_tensor(labels, dtype=h.dtype, device=h.device)
        loss = F.binary_cross_entropy_with_logits(logits, label_tensor)
        positive_count = int(sum(labels))
        return loss, {
            "pairs": len(labels), "positive": positive_count,
            "negative": len(labels) - positive_count,
        }


class AnchorRoleHypergraph(nn.Module):
    """Residual role-split operator for graph-induced star hyperedges.

    ``arhc_symmetric`` is a parameter-matched permutation-invariant control;
    ``arhc_role`` separates anchor/member inputs but keeps the return message
    symmetric; ``arhc_full`` also separates anchor/member return messages and
    adds anchor-member interactions. ``arhc_anchor_shuffled`` reassigns the
    anchor role to a deterministic random member of each unchanged edge.
    Every mode uses the same parameters and a zero-initialized residual scale.
    """

    def __init__(self, hidden_dim: int, mode: str) -> None:
        super().__init__()
        if mode not in ARHC_MODES:
            raise ValueError(f"Unknown ARHC mode {mode!r}; expected {sorted(ARHC_MODES)}")
        self.mode = mode
        self.anchor_projection = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.member_projection = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.edge_encoder = nn.Sequential(
            nn.Linear(hidden_dim * 4, hidden_dim),
            nn.GELU(),
            nn.LayerNorm(hidden_dim),
        )
        self.to_anchor = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.to_member = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.gamma = nn.Parameter(torch.zeros(()))
        self.last_diagnostics: dict[str, int] = {}

    def _role_anchors(self, hyperedges: list[torch.Tensor]) -> torch.Tensor:
        if self.mode != "arhc_anchor_shuffled":
            return torch.stack([edge[0] for edge in hyperedges])
        # Reassign the role only among the nodes already in each hyperedge.
        # This preserves each set exactly while breaking its true center ID.
        generator = torch.Generator(device="cpu").manual_seed(0)
        selected = []
        for edge in hyperedges:
            index = int(torch.randint(len(edge), (1,), generator=generator).item())
            selected.append(edge[index])
        return torch.stack(selected)

    def forward(self, h: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        hyperedges = _star_members(edge_index, h.shape[0])
        if not hyperedges:
            self.last_diagnostics = {
                "hyperedges": 0, "incidences": 0, "anchor_incidences": 0,
                "member_incidences": 0, "coverage_preserved": 1,
            }
            return torch.zeros_like(h)

        device = h.device
        edge_count = len(hyperedges)
        lengths = torch.as_tensor([len(edge) for edge in hyperedges], device=device)
        edge_ids = torch.repeat_interleave(torch.arange(edge_count, device=device), lengths)
        incidence_nodes = torch.cat(hyperedges)
        role_anchors = self._role_anchors(hyperedges).to(device)
        anchor_mask = incidence_nodes == role_anchors[edge_ids]
        leaf_nodes = incidence_nodes[~anchor_mask]
        leaf_edge_ids = edge_ids[~anchor_mask]

        # Every incidence receives exactly one role; shuffled anchors are
        # selected from the same edge, so H_anchor + H_member remains H.
        anchor_incidence_count = int(anchor_mask.sum().item())
        incidence_count = int(incidence_nodes.numel())
        self.last_diagnostics = {
            "hyperedges": edge_count,
            "incidences": incidence_count,
            "anchor_incidences": anchor_incidence_count,
            "member_incidences": int(leaf_nodes.numel()),
            "coverage_preserved": int(
                anchor_incidence_count + int(leaf_nodes.numel()) == incidence_count
            ),
        }

        zeros = h.new_zeros((edge_count, h.shape[-1]))
        if self.mode == "arhc_symmetric":
            # A1 ignores anchor identity and uses one pooled set summary in
            # both encoder slots. Averaging projections keeps full parameter
            # count matched without exposing an anchor/member distinction.
            edge_sum = h.new_zeros((edge_count, h.shape[-1]))
            edge_sum.index_add_(0, edge_ids, h[incidence_nodes])
            pooled = edge_sum / lengths.to(h.dtype).unsqueeze(-1)
            shared = 0.5 * (
                self.anchor_projection(pooled) + self.member_projection(pooled)
            )
            features = torch.cat([shared, shared, zeros, zeros], dim=-1)
        else:
            member_sum = h.new_zeros((edge_count, h.shape[-1]))
            member_sum.index_add_(0, leaf_edge_ids, h[leaf_nodes])
            member_counts = h.new_zeros((edge_count, 1))
            member_counts.index_add_(
                0, leaf_edge_ids, h.new_ones((leaf_edge_ids.numel(), 1))
            )
            member_mean = member_sum / member_counts.clamp_min(1.0)
            anchor_state = self.anchor_projection(h[role_anchors])
            member_state = self.member_projection(member_mean)
            if self.mode == "arhc_role":
                # A2 separates N->H roles but deliberately omits interactions.
                features = torch.cat([anchor_state, member_state, zeros, zeros], dim=-1)
            else:
                features = torch.cat([
                    anchor_state,
                    member_state,
                    anchor_state * member_state,
                    torch.abs(anchor_state - member_state),
                ], dim=-1)

        hyperedge_state = self.edge_encoder(features)
        if self.mode in {"arhc_symmetric", "arhc_role"}:
            # Parameter-matched symmetric H->N return for A1/A2.
            edge_message = 0.5 * (
                self.to_anchor(hyperedge_state) + self.to_member(hyperedge_state)
            )
            output = h.new_zeros(h.shape)
            output.index_add_(0, incidence_nodes, edge_message[edge_ids])
            degree = h.new_zeros((h.shape[0], 1))
            degree.index_add_(0, incidence_nodes, h.new_ones((incidence_count, 1)))
            role_message = output / degree.clamp_min(1.0)
        else:
            anchor_message = self.to_anchor(hyperedge_state)
            member_message = self.to_member(hyperedge_state)
            anchor_output = h.new_zeros(h.shape)
            anchor_output.index_add_(0, role_anchors, anchor_message)
            anchor_degree = h.new_zeros((h.shape[0], 1))
            anchor_degree.index_add_(
                0, role_anchors, h.new_ones((edge_count, 1))
            )
            member_output = h.new_zeros(h.shape)
            member_output.index_add_(0, leaf_nodes, member_message[leaf_edge_ids])
            member_degree = h.new_zeros((h.shape[0], 1))
            member_degree.index_add_(
                0, leaf_nodes, h.new_ones((leaf_nodes.numel(), 1))
            )
            # Normalize anchor and member incidence channels independently.
            role_message = (
                anchor_output / anchor_degree.clamp_min(1.0)
                + member_output / member_degree.clamp_min(1.0)
            )
        return self.gamma * role_message


class PairwiseMomentHypergraph(nn.Module):
    """Linear-time, symmetric hyperedge moment residual for PMHE controls."""

    def __init__(self, hidden_dim: int, mode: str) -> None:
        super().__init__()
        if mode not in PMHE_MODES:
            raise ValueError(f"Unknown PMHE mode {mode!r}; expected {sorted(PMHE_MODES)}")
        self.mode = mode
        # The same parameterized map is used by the mean, second-moment, and
        # pair-interaction arms so the structural statistic is the treatment.
        self.moment_projection = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.gamma = nn.Parameter(torch.zeros(()))
        self.last_diagnostics: dict[str, int] = {}

    @staticmethod
    def pairwise_moment(values: torch.Tensor) -> torch.Tensor:
        """Mean unordered Hadamard pair product in O(kd), or zero for k < 2."""
        count = values.shape[0]
        if count < 2:
            return values.new_zeros(values.shape[-1])
        first_sum = values.sum(dim=0)
        second_sum = values.square().sum(dim=0)
        return (first_sum.square() - second_sum) / (count * (count - 1))

    def forward(self, h: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        hyperedges = _star_members(edge_index, h.shape[0])
        if not hyperedges:
            self.last_diagnostics = {"hyperedges": 0, "incidences": 0}
            return torch.zeros_like(h)

        device = h.device
        edge_count = len(hyperedges)
        lengths = torch.as_tensor([len(edge) for edge in hyperedges], device=device)
        edge_ids = torch.repeat_interleave(torch.arange(edge_count, device=device), lengths)
        incidence_nodes = torch.cat(hyperedges)
        edge_sum = h.new_zeros((edge_count, h.shape[-1]))
        edge_sum.index_add_(0, edge_ids, h[incidence_nodes])
        if self.mode == "pmhe_mean":
            summaries = edge_sum / lengths.to(h.dtype).unsqueeze(-1)
        elif self.mode == "pmhe_second":
            square_sum = h.new_zeros((edge_count, h.shape[-1]))
            square_sum.index_add_(0, edge_ids, h[incidence_nodes].square())
            summaries = square_sum / lengths.to(h.dtype).unsqueeze(-1)
        else:
            square_sum = h.new_zeros((edge_count, h.shape[-1]))
            square_sum.index_add_(0, edge_ids, h[incidence_nodes].square())
            denominator = (lengths * (lengths - 1)).clamp_min(1).to(h.dtype)
            summaries = (edge_sum.square() - square_sum) / denominator.unsqueeze(-1)
            summaries = torch.where(
                (lengths >= 2).unsqueeze(-1), summaries, torch.zeros_like(summaries)
            )

        edge_message = self.moment_projection(summaries)
        node_message = h.new_zeros(h.shape)
        node_message.index_add_(0, incidence_nodes, edge_message[edge_ids])
        degree = h.new_zeros((h.shape[0], 1))
        degree.index_add_(0, incidence_nodes, h.new_ones((incidence_nodes.numel(), 1)))
        self.last_diagnostics = {
            "hyperedges": edge_count,
            "incidences": int(incidence_nodes.numel()),
            "coverage_preserved": int(incidence_nodes.numel() == sum(len(e) for e in hyperedges)),
        }
        return self.gamma * node_message / degree.clamp_min(1.0)


class AnchorRelationalPairMoment(nn.Module):
    """Anchor-conditioned mean/pair-moment residual for ARPM controls."""

    def __init__(self, hidden_dim: int, mode: str) -> None:
        super().__init__()
        if mode not in ARPM_MODES:
            raise ValueError(f"Unknown ARPM mode {mode!r}; expected {sorted(ARPM_MODES)}")
        self.mode = mode
        self.pair_projection = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.relation_encoder = nn.Sequential(
            nn.Linear(hidden_dim * 3, hidden_dim),
            nn.GELU(),
            nn.LayerNorm(hidden_dim),
        )
        self.gamma = nn.Parameter(torch.zeros(()))
        self.last_diagnostics: dict[str, int] = {}

    def _anchors(self, hyperedges: list[torch.Tensor]) -> torch.Tensor:
        if self.mode != "arpm_anchor_shuffled":
            return torch.stack([edge[0] for edge in hyperedges])
        generator = torch.Generator(device="cpu").manual_seed(0)
        return torch.stack([
            edge[int(torch.randint(len(edge), (1,), generator=generator).item())]
            for edge in hyperedges
        ])

    def forward(self, h: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        hyperedges = _star_members(edge_index, h.shape[0])
        if not hyperedges:
            self.last_diagnostics = {"hyperedges": 0, "incidences": 0}
            return torch.zeros_like(h)

        device = h.device
        edge_count = len(hyperedges)
        lengths = torch.as_tensor([len(edge) for edge in hyperedges], device=device)
        edge_ids = torch.repeat_interleave(torch.arange(edge_count, device=device), lengths)
        incidence_nodes = torch.cat(hyperedges)
        anchors = self._anchors(hyperedges).to(device)
        is_anchor = incidence_nodes == anchors[edge_ids]
        member_nodes = incidence_nodes[~is_anchor]
        member_edge_ids = edge_ids[~is_anchor]

        member_sum = h.new_zeros((edge_count, h.shape[-1]))
        member_sum.index_add_(0, member_edge_ids, h[member_nodes])
        member_count = h.new_zeros((edge_count, 1))
        member_count.index_add_(
            0, member_edge_ids, h.new_ones((member_edge_ids.numel(), 1))
        )
        mean = member_sum / member_count.clamp_min(1.0)
        summary = mean
        if self.mode != "arpm_mean":
            member_square_sum = h.new_zeros((edge_count, h.shape[-1]))
            member_square_sum.index_add_(0, member_edge_ids, h[member_nodes].square())
            denominator = (member_count.squeeze(-1) * (member_count.squeeze(-1) - 1))
            pair = (member_sum.square() - member_square_sum) / denominator.clamp_min(1).unsqueeze(-1)
            summary = torch.where(
                (member_count >= 2), pair, torch.zeros_like(pair)
            )

        anchor_state = h[anchors]
        projected = self.pair_projection(summary)
        features = torch.cat([
            summary,
            anchor_state * summary,
            torch.abs(anchor_state - projected),
        ], dim=-1)
        edge_message = self.relation_encoder(features)
        node_message = h.new_zeros(h.shape)
        node_message.index_add_(0, incidence_nodes, edge_message[edge_ids])
        degree = h.new_zeros((h.shape[0], 1))
        degree.index_add_(0, incidence_nodes, h.new_ones((incidence_nodes.numel(), 1)))
        self.last_diagnostics = {
            "hyperedges": edge_count,
            "incidences": int(incidence_nodes.numel()),
            "anchor_incidences": int(is_anchor.sum().item()),
            "member_incidences": int(member_nodes.numel()),
            "coverage_preserved": int(
                int(is_anchor.sum().item()) + int(member_nodes.numel())
                == int(incidence_nodes.numel())
            ),
        }
        return self.gamma * node_message / degree.clamp_min(1.0)
