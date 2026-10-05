import torch

from dcdlp.models.hypergraph import (
    _edge_centered_groups,
    _ego_components,
    _message_neighbors,
    _partition_groups,
    _star_members,
    build_hyperedges,
    construction_statistics,
)
from dcdlp.models.node_encoder import mask_pair_edges


def _edge_index():
    edges = [
        (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
        (1, 2), (2, 3), (3, 4), (5, 6),
    ]
    return torch.tensor(edges, dtype=torch.long).t().contiguous()


def _edge_sets(edge_index, construction):
    num_nodes = int(edge_index.max().item()) + 1 if edge_index.numel() else 0
    return {tuple(sorted(edge.tolist())) for edge in build_hyperedges(edge_index, num_nodes, construction)}


def test_raw_star_construction_is_unchanged_and_true_components_are_augmented():
    edge_index = _edge_index()
    raw = _star_members(edge_index, 8)
    built = build_hyperedges(edge_index, 8, "raw_star")
    assert [edge.tolist() for edge in built] == [edge.tolist() for edge in raw]

    true_edges = _edge_sets(edge_index, "ecph_true")
    assert tuple((0, 1, 2, 3, 4)) in true_edges
    assert tuple((0, 1, 2, 3, 4, 5, 6, 7)) in true_edges  # the raw star remains


def test_partition_controls_preserve_true_component_count_and_size_multiset():
    edge_index = _edge_index()
    neighbors = _message_neighbors(edge_index, 8)
    components = _ego_components(neighbors, 0)
    expected = sorted(len(group) for group in components if len(group) >= 2)
    for construction in ("ecph_random", "ecph_degree"):
        groups = _partition_groups(neighbors, 0, components, construction)
        assert sorted(map(len, groups)) == expected
        assert len(groups) == len(expected)
        assert all(set(group) <= neighbors[0] for group in groups)
    assert construction_statistics(edge_index, 8, "ecph_true")["requested_component_hyperedge_count"] > 0


def test_target_masking_precedes_ego_component_construction():
    edge_index = _edge_index()
    masked = mask_pair_edges(edge_index, torch.tensor([[2, 3]], dtype=torch.long))
    masked_edges = {tuple(sorted(pair)) for pair in masked.t().tolist()}
    assert (2, 3) not in masked_edges
    before = _edge_sets(edge_index, "ecph_true")
    after = _edge_sets(masked, "ecph_true")
    assert (0, 1, 2, 3, 4) in before
    assert (0, 1, 2, 3, 4) not in after


def test_ecnh_controls_match_group_size_and_true_uses_low_degree_common_neighbors():
    edges = [(0, 1)]
    for node in range(2, 19):
        edges.extend(((0, node), (1, node)))
    edges.extend(((2, 19), (2, 20)))
    edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
    neighbors = _message_neighbors(edge_index, 21)
    groups = {
        name: next(group for u, v, group in _edge_centered_groups(neighbors, name) if (u, v) == (0, 1))
        for name in ("ecnh_random", "ecnh_union", "ecnh_true")
    }
    assert {len(group) for group in groups.values()} == {16}
    assert len(set(groups["ecnh_true"])) == 16
    assert 2 not in groups["ecnh_true"]  # its higher degree loses the deterministic cap tie-break
    built = _edge_sets(edge_index, "ecnh_true")
    assert tuple(sorted((0, 1, *groups["ecnh_true"]))) in built
    true_stats = construction_statistics(edge_index, 21, "ecnh_true")
    assert true_stats["common_neighbor_cap"] == 16
    for control in ("ecnh_random", "ecnh_union"):
        control_stats = construction_statistics(edge_index, 21, control)
        assert control_stats["added_hyperedge_count"] == true_stats["added_hyperedge_count"]
        assert control_stats["added_hyperedge_size"] == true_stats["added_hyperedge_size"]


def test_ecnh_does_not_use_a_target_edge_as_an_edge_center():
    edge_index = _edge_index()
    masked = mask_pair_edges(edge_index, torch.tensor([[0, 1]], dtype=torch.long))
    masked_neighbors = _message_neighbors(masked, 8)
    assert all((u, v) != (0, 1) for u, v, _ in _edge_centered_groups(masked_neighbors, "ecnh_true"))


def test_owh_builds_only_open_wedges_from_the_supplied_message_graph():
    edge_index = torch.tensor(
        [(0, 1), (0, 2), (0, 3), (1, 3)], dtype=torch.long
    ).t().contiguous()
    raw = _edge_sets(edge_index, "raw_star")
    opened = _edge_sets(edge_index, "owh_open")
    closed = _edge_sets(edge_index, "owh_closed")
    assert (0, 1, 2) in opened
    assert (0, 1, 3) in raw  # Those three nodes form a closed triangle/Raw star.
    assert (0, 1, 2, 3) in raw  # Raw star remains alongside smaller wedges.
    assert (0, 1, 2) not in (closed - raw)


def test_owh_open_wedge_cap_uses_deterministic_endpoint_degree_priority():
    # A degree-10 center has 45 open wedges; endpoint degrees tie, so the
    # ascending endpoint IDs determine the first 32 pairs.
    edges = [(0, node) for node in range(1, 11)]
    edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
    stats = construction_statistics(edge_index, 11, "owh_open")
    built = _edge_sets(edge_index, "owh_open")
    wedge_additions = built - _edge_sets(edge_index, "raw_star")
    assert stats["open_wedge_candidate_count_before_cap"] == 45
    assert stats["selected_open_wedge_proposal_count"] == 32
    expected = {
        tuple(sorted((0, u, v)))
        for u, v in [(u, v) for u in range(1, 11) for v in range(u + 1, 11)][:32]
    }
    assert wedge_additions == expected


def test_owh_random_control_matches_unique_open_wedge_addition_count():
    # Path wedges that collide with degree-two Raw stars are excluded before
    # generating count-matched random triples.
    edge_index = torch.tensor(
        [(0, 1), (1, 2), (1, 3), (3, 4), (4, 5), (4, 6)],
        dtype=torch.long,
    ).t().contiguous()
    raw = _edge_sets(edge_index, "raw_star")
    opened = _edge_sets(edge_index, "owh_open")
    random = _edge_sets(edge_index, "owh_random")
    true_additions = opened - raw
    random_additions = random - raw
    assert len(random_additions) == len(true_additions)
    assert all(len(edge) == 3 for edge in random_additions)
    random_stats = construction_statistics(edge_index, 7, "owh_random")
    open_stats = construction_statistics(edge_index, 7, "owh_open")
    assert random_stats["added_hyperedge_count"] == open_stats["added_hyperedge_count"]
    assert random_stats["added_hyperedge_size"] == open_stats["added_hyperedge_size"]


def test_owh_target_pair_is_absent_before_wedge_construction():
    edge_index = torch.tensor(
        [(0, 1), (0, 2), (0, 3), (1, 3)], dtype=torch.long
    ).t().contiguous()
    masked = mask_pair_edges(edge_index, torch.tensor([[0, 1]], dtype=torch.long))
    masked_edges = {tuple(sorted(pair)) for pair in masked.t().tolist()}
    opened = _edge_sets(masked, "owh_open")
    assert (0, 1) not in masked_edges
    # Removing (0,1) removes node 0 from center 1's neighbor set, so the
    # original {0,1,2} wedge cannot be proposed on the masked graph.
    assert (0, 1, 2) not in opened
