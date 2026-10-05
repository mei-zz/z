import torch

from dcdlp.models.dcdlp import DCDLP
from dcdlp.models.hypergraph import (
    AnchorRoleHypergraph,
    AnchorRelationalPairMoment,
    IncidenceResidualComplement,
    PairwiseMomentHypergraph,
)


def test_hypergraph_modes_are_finite_and_shape_preserving():
    x = torch.randn(5, 4)
    edge_index = torch.tensor([[0, 1, 1, 2, 3], [1, 2, 3, 3, 4]])
    for mode in ("raw", "complement", "pairwise", "shuffled"):
        module = IncidenceResidualComplement(4, mode)
        output = module(x, edge_index)
        assert output.shape == x.shape
        assert torch.isfinite(output).all()


def test_disabled_hypergraph_keeps_dcdlp_output_contract():
    model = DCDLP(
        input_dim=4,
        hidden_dim=8,
        branch_dim=4,
        num_layers=1,
        dropout=0.0,
        hypergraph_mode="disabled",
    )
    x = torch.randn(5, 4)
    edge_index = torch.tensor([[0, 1, 1, 2, 3], [1, 2, 3, 3, 4]])
    pairs = torch.tensor([[0, 4], [0, 3]])
    output = model(x, edge_index, pairs)
    assert output["logit"].shape == (2,)
    assert model.hypergraph is None


def test_lchr_pool_fallback_and_gradient():
    model = DCDLP(4, 8, 4, num_layers=1, dropout=0.0, hypergraph_mode="lchr")
    x = torch.randn(5, 4)
    edges = torch.tensor([[0, 1, 1, 2], [1, 2, 3, 3]])
    pairs = torch.tensor([[0, 3], [4, 4]])
    output = model(x, edges, pairs)
    assert model.link_router.last_diagnostics["pool_sizes"][1] == 0
    assert torch.isfinite(output["logit"]).all()
    output["logit"].square().mean().backward()
    assert model.link_router.router[0].weight.grad is not None


def test_lchr_masks_target_edge_before_hypergraph_construction():
    model = DCDLP(4, 8, 4, num_layers=1, dropout=0.0, hypergraph_mode="lchr")
    x = torch.randn(2, 4)
    edges = torch.tensor([[0], [1]])
    model(x, edges, torch.tensor([[0, 1]]))
    assert model.link_router.last_diagnostics["pool_sizes"] == [0]


def test_arhc_keeps_every_incidence_and_has_finite_role_messages():
    x = torch.randn(5, 4)
    edges = torch.tensor([[0, 1, 1, 2], [1, 2, 3, 3]])
    module = AnchorRoleHypergraph(4, "arhc_full")
    output = module(x, edges)
    assert output.shape == x.shape
    assert torch.isfinite(output).all()
    diagnostics = module.last_diagnostics
    assert diagnostics["incidences"] == diagnostics["anchor_incidences"] + diagnostics["member_incidences"]
    assert diagnostics["coverage_preserved"] == 1
    assert diagnostics["hyperedges"] == diagnostics["anchor_incidences"]


def test_arhc_zero_residual_matches_raw_output_with_same_seed():
    torch.manual_seed(41)
    raw = DCDLP(4, 8, 4, num_layers=1, dropout=0.0, hypergraph_mode="raw")
    torch.manual_seed(41)
    arhc = DCDLP(4, 8, 4, num_layers=1, dropout=0.0, hypergraph_mode="arhc_full")
    raw.eval()
    arhc.eval()
    x = torch.randn(5, 4)
    edges = torch.tensor([[0, 1, 1, 2, 3], [1, 2, 3, 3, 4]])
    pairs = torch.tensor([[0, 4], [0, 3]])
    raw_output = raw(x, edges, pairs)["logit"]
    arhc_output = arhc(x, edges, pairs)["logit"]
    assert arhc.anchor_role.gamma.item() == 0.0
    assert torch.equal(raw_output, arhc_output)


def test_pairwise_moment_matches_explicit_unordered_pairs_and_handles_singleton():
    values = torch.tensor([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    expected = torch.stack([
        values[0] * values[1],
        values[0] * values[2],
        values[1] * values[2],
    ]).mean(0)
    assert torch.allclose(PairwiseMomentHypergraph.pairwise_moment(values), expected)
    assert torch.equal(
        PairwiseMomentHypergraph.pairwise_moment(values[:1]), torch.zeros(2)
    )


def test_pmhe_zero_residual_matches_raw_output_with_same_seed():
    torch.manual_seed(43)
    raw = DCDLP(4, 8, 4, num_layers=1, dropout=0.0, hypergraph_mode="raw")
    torch.manual_seed(43)
    pair = DCDLP(4, 8, 4, num_layers=1, dropout=0.0, hypergraph_mode="pmhe_pair")
    raw.eval()
    pair.eval()
    x = torch.randn(5, 4)
    edges = torch.tensor([[0, 1, 1, 2, 3], [1, 2, 3, 3, 4]])
    pairs = torch.tensor([[0, 4], [0, 3]])
    assert pair.pair_moment.gamma.item() == 0.0
    assert torch.equal(raw(x, edges, pairs)["logit"], pair(x, edges, pairs)["logit"])


def test_arpm_anchor_shuffle_preserves_incidence_and_zero_gamma_is_finite():
    x = torch.randn(5, 4)
    edges = torch.tensor([[0, 1, 1, 2], [1, 2, 3, 3]])
    module = AnchorRelationalPairMoment(4, "arpm_anchor_shuffled")
    output = module(x, edges)
    assert output.shape == x.shape
    assert torch.isfinite(output).all()
    assert module.gamma.item() == 0.0
    assert module.last_diagnostics["coverage_preserved"] == 1
    assert module.last_diagnostics["anchor_incidences"] == module.last_diagnostics["hyperedges"]


def test_arpm_zero_residual_matches_raw_output_with_same_seed():
    torch.manual_seed(47)
    raw = DCDLP(4, 8, 4, num_layers=1, dropout=0.0, hypergraph_mode="raw")
    torch.manual_seed(47)
    arpm = DCDLP(4, 8, 4, num_layers=1, dropout=0.0, hypergraph_mode="arpm_pair")
    raw.eval()
    arpm.eval()
    x = torch.randn(5, 4)
    edges = torch.tensor([[0, 1, 1, 2, 3], [1, 2, 3, 3, 4]])
    pairs = torch.tensor([[0, 4], [0, 3]])
    assert arpm.anchor_pair_moment.gamma.item() == 0.0
    assert torch.equal(raw(x, edges, pairs)["logit"], arpm(x, edges, pairs)["logit"])
