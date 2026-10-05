from __future__ import annotations

import numpy as np

ARM = "BASELINE"
RUNNER = None
TRAIN_POSITIVE_INDEX = {}
TRAIN_POSITIVE_SET = set()
TRAIN_POOL = None
LAST_SETWISE = None
LAST_VIEW = None
PATCHED = False


def canonical(pair):
    a, b = int(pair[0]), int(pair[1])
    return (a, b) if a <= b else (b, a)


def configure(arm, train_pos=None, train_pool=None, runner_module=None):
    global ARM, RUNNER, TRAIN_POSITIVE_INDEX, TRAIN_POSITIVE_SET, TRAIN_POOL
    global LAST_SETWISE, LAST_VIEW
    ARM = str(arm)
    RUNNER = runner_module
    if train_pos is not None:
        keys = [canonical(pair) for pair in train_pos]
        TRAIN_POSITIVE_INDEX = {key: i for i, key in enumerate(keys)}
        TRAIN_POSITIVE_SET = set(keys)
    if train_pool is not None:
        TRAIN_POOL = np.asarray(train_pool, dtype=np.int64)
        if TRAIN_POOL.ndim != 3 or TRAIN_POOL.shape[1:] != (20, 2):
            raise RuntimeError("L1 requires the frozen 20-candidate train pool")
    LAST_SETWISE = None
    LAST_VIEW = None


def _standardize_cn(model, values, torch):
    x = values.reshape(-1, 1)

    if model.training:
        detached = x.detach()
        with torch.no_grad():
            model.v13_p1_cn_sum.add_(detached.sum(0))
            model.v13_p1_cn_square.add_(detached.square().sum(0))
            model.v13_p1_cn_count.add_(float(len(detached)))
        mean = detached.mean(0)
        variance = detached.var(0, unbiased=False)
    else:
        count = model.v13_p1_cn_count.clamp_min(1.0)
        mean = model.v13_p1_cn_sum / count
        variance = (model.v13_p1_cn_square / count - mean.square()).clamp_min(0.0)
    return (x - mean) / torch.sqrt(variance + 1e-5)


def install_hooks():
    global PATCHED
    if PATCHED:
        return
    import torch
    from torch import nn
    from dcdlp.models.dcdlp import DCDLP

    init0, forward0, score0 = DCDLP.__init__, DCDLP.forward, DCDLP._score_state

    def init1(self, *args, **kwargs):
        init0(self, *args, **kwargs)
        if ARM.startswith("P1_"):
            hidden = int(args[1]) if len(args) >= 2 else int(kwargs.get("hidden_dim", 128))
            input_dim = 2 * hidden + 1
            self.register_buffer("v13_p1_cn_sum", torch.zeros(1))
            self.register_buffer("v13_p1_cn_square", torch.zeros(1))
            self.register_buffer("v13_p1_cn_count", torch.zeros(()))
            if ARM == "P1_CONCAT":
                self.v13_pair_decoder = nn.Linear(input_dim, 1, bias=True)
                nn.init.zeros_(self.v13_pair_decoder.weight)
                nn.init.zeros_(self.v13_pair_decoder.bias)
            else:
                self.v13_pair_decoder = nn.Sequential(
                    nn.Linear(input_dim, 2, bias=True),
                    nn.Tanh(),
                    nn.Linear(2, 1, bias=True),
                )
                nn.init.zeros_(self.v13_pair_decoder[-1].weight)
                nn.init.zeros_(self.v13_pair_decoder[-1].bias)
        if ARM.startswith("V1_"):
            encoder_forward = self.node_encoder.forward

            def capture_graph_state(*f_args, **f_kwargs):
                state = encoder_forward(*f_args, **f_kwargs)
                self._v13_graph_node_state = state
                return state

            self.node_encoder.forward = capture_graph_state

    def score1(self, h, pairs, neighbors, degrees, edge_index, apply_router):
        global LAST_SETWISE, LAST_VIEW
        out = score0(self, h, pairs, neighbors, degrees, edge_index, apply_router)

        if ARM.startswith("P1_") and apply_router:
            hu, hv = h[pairs[:, 0]], h[pairs[:, 1]]
            cn = _standardize_cn(self, out["score_cn"], torch)
            if ARM == "P1_SYM":
                features = torch.cat([torch.abs(hu - hv), hu * hv, cn], dim=-1)
            elif ARM == "P1_GENERIC":
                features = torch.cat([hu, hv, cn], dim=-1)
            else:
                features = torch.cat([hu, hv, cn], dim=-1)
            out["logit"] = out["logit"] + self.v13_pair_decoder(features).squeeze(-1)

        if ARM.startswith("L1_") and self.training and apply_router:
            if TRAIN_POOL is None or RUNNER is None:
                raise RuntimeError("L1 candidate pool was not configured")
            positions = []
            rows = []
            for pair_i, pair in enumerate(pairs.detach().cpu().tolist()):
                row = TRAIN_POSITIVE_INDEX.get(canonical(pair))
                if row is not None:
                    positions.append(pair_i)
                    rows.append(row)
            if positions:
                candidate_pairs = TRAIN_POOL[np.asarray(rows, dtype=np.int64)].reshape(-1, 2)
                candidate_tensor = torch.as_tensor(candidate_pairs, dtype=torch.long, device=h.device)
                candidate_scores = score0(
                    self, h, candidate_tensor, neighbors, degrees, edge_index, False
                )["logit"].reshape(len(rows), 20)
                positive_scores = out["logit"][torch.as_tensor(positions, dtype=torch.long, device=h.device)]
                LAST_SETWISE = (positive_scores, candidate_scores)
            else:
                LAST_SETWISE = None

        if ARM.startswith("V1_") and apply_router:
            graph_h = getattr(self, "_v13_graph_node_state", None)
            if graph_h is None:
                raise RuntimeError("V1 graph-view state capture failed")
            graph_out = score0(self, graph_h, pairs, neighbors, degrees, edge_index, False)
            if self.training:
                pos_positions = []
                pos_pairs = []
                neg_pairs = []
                for pair_i, pair in enumerate(pairs.detach().cpu().tolist()):
                    key = canonical(pair)
                    if key not in TRAIN_POSITIVE_SET:
                        continue
                    neg_key = RUNNER.TRAIN_NEGATIVE_MAP.get(key)
                    if neg_key is None:
                        continue
                    pos_positions.append(pair_i)
                    pos_pairs.append(key)
                    neg_pairs.append(neg_key)
                if pos_positions:
                    neg_tensor = torch.as_tensor(neg_pairs, dtype=torch.long, device=h.device)
                    raw_neg = score0(self, h, neg_tensor, neighbors, degrees, edge_index, False)["logit"]
                    graph_pos = graph_out["logit"][torch.as_tensor(pos_positions, dtype=torch.long, device=h.device)]
                    graph_neg = score0(self, graph_h, neg_tensor, neighbors, degrees, edge_index, False)["logit"]
                    raw_pos = out["logit"][torch.as_tensor(pos_positions, dtype=torch.long, device=h.device)]
                    LAST_VIEW = {
                        "positive_pairs": pos_pairs,
                        "graph_margin": graph_pos - graph_neg,
                        "raw_margin": raw_pos - raw_neg,
                        "graph_h_u": graph_h[torch.as_tensor([p[0] for p in pos_pairs], dtype=torch.long, device=h.device)],
                        "graph_h_v": graph_h[torch.as_tensor([p[1] for p in pos_pairs], dtype=torch.long, device=h.device)],
                        "raw_h_u": h[torch.as_tensor([p[0] for p in pos_pairs], dtype=torch.long, device=h.device)],
                        "raw_h_v": h[torch.as_tensor([p[1] for p in pos_pairs], dtype=torch.long, device=h.device)],
                    }
                else:
                    LAST_VIEW = None
        return out

    def forward1(self, x, edge_index, pairs, remove_target_edges=True, support_edge_index=None):
        return forward0(self, x, edge_index, pairs,
                        remove_target_edges=remove_target_edges,
                        support_edge_index=support_edge_index)

    DCDLP.__init__ = init1
    DCDLP._score_state = score1
    DCDLP.forward = forward1
    PATCHED = True


def _expected_reciprocal_rank(pos, neg, temperature=0.5):
    import torch
    probabilities = torch.sigmoid((neg - pos.unsqueeze(1)) / temperature)
    batch, count = probabilities.shape
    distribution = probabilities.new_zeros((batch, count + 1))
    distribution[:, 0] = 1.0
    for j in range(count):
        p = probabilities[:, j]
        next_distribution = distribution.new_zeros(distribution.shape)
        next_distribution[:, 0] = distribution[:, 0] * (1.0 - p)
        next_distribution[:, 1:j + 2] = (
            distribution[:, 1:j + 2] * (1.0 - p.unsqueeze(1))
            + distribution[:, :j + 1] * p.unsqueeze(1)
        )
        distribution = next_distribution
    reciprocal = torch.arange(1, count + 2, dtype=pos.dtype, device=pos.device).reciprocal()
    return (distribution * reciprocal.unsqueeze(0)).sum(1)


def _sample_candidate_set(neg, calls, torch):
    """Draw a deterministic-within-run 20-item multiset from each frozen pool."""
    if neg.ndim != 2 or neg.shape[1] != 20:
        raise RuntimeError(f"L1 controls require [batch,20] scores; got {tuple(neg.shape)}")
    calls["n"] += 1
    generator = torch.Generator(device=neg.device)
    generator.manual_seed(440000 + calls["n"])
    indices = torch.randint(
        0, neg.shape[1], (len(neg), 20), generator=generator, device=neg.device
    )
    return torch.gather(neg, 1, indices)


def loss_hook_factory(arm, runner_module, base_factory):
    import torch
    from torch.nn import functional as F

    calls = {"n": 0}
    baseline_loss = base_factory(arm)
    if arm.startswith("L1_"):
        def setwise_loss(logits, labels, *args, **kwargs):
            if LAST_SETWISE is None:
                raise RuntimeError("L1 setwise scores are missing for the current training batch")
            pos, neg = LAST_SETWISE
            if len(pos) == 0:
                return baseline_loss(logits, labels, *args, **kwargs)
            if arm == "L1_EXPECTED_MRR":
                per_query = 1.0 - _expected_reciprocal_rank(pos, neg)
            elif arm == "L1_INDEP_BCE":
                positive = F.binary_cross_entropy_with_logits(pos, torch.ones_like(pos), reduction="none")
                negative = F.binary_cross_entropy_with_logits(neg, torch.zeros_like(neg), reduction="none").mean(1)
                per_query = 0.5 * (positive + negative)
            elif arm == "L1_LISTWISE":
                per_query = torch.logsumexp(torch.cat([pos[:, None], neg], dim=1), dim=1) - pos
            elif arm == "L1_LISTWISE_RANDOM":
                sampled = _sample_candidate_set(neg, calls, torch)
                per_query = torch.logsumexp(
                    torch.cat([pos[:, None], sampled], dim=1), dim=1
                ) - pos
            elif arm == "L1_REPEAT_BCE":
                repeated = _sample_candidate_set(neg, calls, torch)
                positive = F.binary_cross_entropy_with_logits(
                    pos[:, None].expand_as(repeated), torch.ones_like(repeated), reduction="none"
                )
                negative = F.binary_cross_entropy_with_logits(
                    repeated, torch.zeros_like(repeated), reduction="none"
                )
                per_query = 0.5 * (positive.mean(1) + negative.mean(1))
            else:
                raise RuntimeError(f"Unknown L1 objective arm: {arm}")
            return per_query.mean()
        return setwise_loss

    if arm.startswith("V1_"):
        def distillation_loss(logits, labels, *args, **kwargs):
            base = baseline_loss(logits, labels, *args, **kwargs)
            if LAST_VIEW is None:
                return base
            teacher = LAST_VIEW["graph_margin"].detach()
            student = LAST_VIEW["raw_margin"]
            threshold = torch.quantile(teacher, 0.75)
            confident = (teacher > 0.0) & (teacher >= threshold)
            if not confident.any():
                return base
            t = teacher[confident]
            s = student[confident]
            if arm == "V1_DISTILL":
                target = torch.sigmoid(t / 0.5)
                aux = F.binary_cross_entropy_with_logits(s / 0.5, target) * 0.25
            elif arm == "V1_SHUFFLE":
                shuffled = torch.roll(teacher, shifts=1)
                target = torch.sigmoid(shuffled[confident] / 0.5)
                aux = F.binary_cross_entropy_with_logits(s / 0.5, target) * 0.25
            elif arm == "V1_MEAN":
                aux = F.mse_loss(t.mean(), s.mean())
            else:
                gu, gv = LAST_VIEW["graph_h_u"][confident], LAST_VIEW["graph_h_v"][confident]
                hu, hv = LAST_VIEW["raw_h_u"][confident], LAST_VIEW["raw_h_v"][confident]
                aux = 0.5 * (F.mse_loss(hu, gu.detach()) + F.mse_loss(hv, gv.detach()))
            return base + 0.1 * aux
        return distillation_loss

    return baseline_loss

