import networkx as nx
import numpy as np
import torch

from dcdlp.evaluation.posthoc_probe import (
    context_graph_hash,
    remove_target_edge_if_present,
)
from scripts.run_posthoc_leakage_audit import (
    _assert_context_graph,
    _extract_contextual_pairs,
    _fixed_subset,
    _sampling_seed,
)


def _toy_graph():
    graph = nx.Graph()
    graph.add_nodes_from(range(4))
    graph.add_edges_from([(0, 1), (1, 2), (2, 3)])
    return graph


def test_v2_per_pair_masking_removes_only_current_pair():
    graph = _toy_graph()
    context_a = remove_target_edge_if_present(graph, (0, 1))
    context_b = remove_target_edge_if_present(graph, (1, 2))

    assert not context_a.has_edge(0, 1)
    assert context_a.has_edge(1, 2)
    assert context_a.has_edge(2, 3)
    assert not context_b.has_edge(1, 2)
    assert context_b.has_edge(0, 1)
    assert context_b.has_edge(2, 3)
    assert graph.number_of_edges() == 3
    assert context_graph_hash(context_a) != context_graph_hash(context_b)


def test_v2_valid_test_target_removal_is_noop():
    graph = _toy_graph()
    context = remove_target_edge_if_present(graph, (0, 2))

    assert context_graph_hash(context) == context_graph_hash(graph)
    _assert_context_graph(graph, context, np.asarray([0, 2]), split="valid")
    _assert_context_graph(graph, context, np.asarray([0, 2]), split="test")


class _FakeProbeModel(torch.nn.Module):
    def forward(self, x, edge_index, pairs, *, remove_target_edges):
        assert remove_target_edges is False
        value = torch.ones((len(pairs), 2), dtype=torch.float32)
        return {
            "z_degree": value,
            "z_cn": value + 1,
            "z_residual": value + 2,
        }


class _FakeResidualizer:
    def residual(self, stats):
        expected = np.zeros(len(stats["cn"]), dtype=float)
        return expected, np.log1p(stats["cn"])


def test_v2_representation_and_target_use_same_context_hash():
    graph = _toy_graph()
    features = np.ones((4, 2), dtype=np.float32)
    x = torch.as_tensor(features)
    model = _FakeProbeModel()
    representations, stats, contexts = _extract_contextual_pairs(
        model,
        x,
        graph,
        np.asarray([[0, 1]], dtype=np.int64),
        features,
        _FakeResidualizer(),
        split="train",
    )

    assert representations["z_cn"].shape == (1, 2)
    assert stats["degree"][0] == np.log(2.0)
    assert contexts[0]["representation_context_graph_hash"] == contexts[0]["target_context_graph_hash"]
    assert contexts[0]["xy_context_hash_match"] is True
    assert contexts[0]["removed_edge_count"] == 1
    assert contexts[0]["context_edge_count"] == 2


def test_v2_probe_sampling_is_reproducible_and_seeded():
    pairs = np.asarray([[index, index + 100] for index in range(20)])
    first = _fixed_subset(pairs, 8, _sampling_seed(7, 0, 0))
    repeat = _fixed_subset(pairs, 8, _sampling_seed(7, 0, 0))
    different = _fixed_subset(pairs, 8, _sampling_seed(7, 1, 0))

    np.testing.assert_array_equal(first, repeat)
    assert not np.array_equal(first, different)
    # The seed formula has no model-label input, so model comparisons share it.
    np.testing.assert_array_equal(
        _fixed_subset(pairs, 8, _sampling_seed(7, 2, 1)),
        _fixed_subset(pairs, 8, _sampling_seed(7, 2, 1)),
    )
