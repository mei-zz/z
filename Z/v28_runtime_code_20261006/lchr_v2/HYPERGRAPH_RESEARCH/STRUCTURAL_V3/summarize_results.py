"""Assemble and audit the archived validation-only V3 experiment outputs."""
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RAW_PARAM_COUNT = 24735


def read_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_candidate(folder, arms):
    evidence = ROOT / folder / "remote_evidence"
    data = {"F0": {}, "F1": {}}
    for stage in ("F0", "F1"):
        for arm in arms:
            data[stage][arm] = read_json(evidence / stage / arm / "metrics.json")
    status = read_json(evidence / "status.json")
    return data, status


def summarize(data, arms, branch_count):
    f0 = {arm: float(row["validation"]["mrr"]) for arm, row in data["F0"].items()}
    f1 = {arm: float(row["validation"]["mrr"]) for arm, row in data["F1"].items()}
    raw = arms[0]
    candidate = arms[-1]
    gain = f1[candidate] - f1[raw]
    raw_time = float(data["F1"][raw]["runtime"]["train_seconds"])
    candidate_time = float(data["F1"][candidate]["runtime"]["train_seconds"])
    return {
        "decision": "REJECT",
        "winner": None,
        "f0_validation_mrr": f0,
        "f1_best_validation_mrr": f1,
        "f1_validation_curve": {
            arm: data["F1"][arm]["validation_curve"] for arm in arms
        },
        "f1_best_epoch": {
            arm: int(data["F1"][arm]["best_epoch"]) + 1 for arm in arms
        },
        "candidate_gain_over_raw": {
            "absolute_mrr": gain,
            "relative_percent": 100 * gain / max(f1[raw], 1e-12),
        },
        "threshold": {"absolute_mrr": 0.003, "relative_percent": 2.0},
        "branch_parameter_count": branch_count,
        "raw_trainable_parameter_count": RAW_PARAM_COUNT,
        "parameter_overhead_percent": 100 * branch_count / RAW_PARAM_COUNT,
        "f1_runtime_seconds": {
            "raw": raw_time,
            "candidate": candidate_time,
            "candidate_over_raw_percent": 100 * (candidate_time - raw_time) / raw_time,
        },
        "candidate_gamma": next((
            data["F1"][candidate][key]
            for key in ("anchor_role_gamma", "pair_moment_gamma", "anchor_pair_moment_gamma")
            if data["F1"][candidate].get(key) is not None
        ), None),
        "test_evaluated": False,
    }


def main():
    candidates = {
        "A_ARHC": ("A_ARHC", ["A0", "A1", "A2", "A3"], 2097),
        "B_PMHE": ("B_PMHE", ["B0", "B1", "B2", "B3"], 257),
        "C_ARPM": ("C_ARPM", ["C0", "C1", "C2", "C3"], 1073),
    }
    reports = {}
    splits = set()
    all_runs = []
    all_f1_scores = []
    structural_f1_scores = []
    for key, (folder, arms, branch_count) in candidates.items():
        data, status = load_candidate(folder, arms)
        report = summarize(data, arms, branch_count)
        if key == "C_ARPM":
            c4_path = ROOT / folder / "remote_evidence" / "F1" / "C4" / "metrics.json"
            if c4_path.exists():
                c4 = read_json(c4_path)
                report["c4_shuffled_anchor_validation_mrr"] = float(c4["validation"]["mrr"])
                report["c4_validation_curve"] = c4["validation_curve"]
                report["c3_minus_c4_mrr"] = (
                    report["f1_best_validation_mrr"]["C3"]
                    - float(c4["validation"]["mrr"])
                )
                report["c4_runtime_seconds"] = float(c4["runtime"]["train_seconds"])
                all_f1_scores.append((float(c4["validation"]["mrr"]), key, "C4"))
                if c4["evaluation_candidates"]["test_evaluated"] is not False:
                    raise RuntimeError("C4 unexpectedly evaluated test")
                if c4["data_integrity"]["split_hash"] not in splits and splits:
                    raise RuntimeError("C4 changed the registered split")
                all_runs.append("C_ARPM/F1/C4")
        report["remote_status"] = status
        reports[key] = report
        all_f1_scores.extend(
            (float(row["validation"]["mrr"]), key, arm)
            for arm, row in data["F1"].items()
        )
        structural_f1_scores.append((float(data["F1"][arms[-1]]["validation"]["mrr"]), key, arms[-1]))
        for stage in ("F0", "F1"):
            for arm, row in data[stage].items():
                splits.add(row["data_integrity"]["split_hash"])
                if row["evaluation_candidates"]["test_evaluated"] is not False:
                    raise RuntimeError("A screening run unexpectedly evaluated test")
                if row["seed"] != 0 or row["protocol_eval"] != "standard" or row["protocol_train"] != "uniform":
                    raise RuntimeError("A screening run changed the registered data protocol")
                if row["dataset"] != "cora":
                    raise RuntimeError("A screening run changed the registered dataset")
                all_runs.append("%s/%s/%s" % (key, stage, arm))
    if len(splits) != 1:
        raise RuntimeError("The screening runs do not share one split hash")
    best_overall = max(all_f1_scores)
    best_candidate = max(structural_f1_scores)
    results = {
        "status": "EXECUTED",
        "final_decision": "NO_STRUCTURAL_SIGNAL",
        "winning_candidate": None,
        "best_validation_mrr": best_overall[0],
        "best_validation_arm": {"candidate": best_overall[1], "arm": best_overall[2]},
        "best_structural_candidate_validation_mrr": best_candidate[0],
        "best_structural_candidate_arm": {"candidate": best_candidate[1], "arm": best_candidate[2]},
        "best_raw_validation_mrr": 0.4876775417205556,
        "raw_hypergraph": {
            "construction": "one target-masked closed-neighborhood star {c} union N(c) per non-isolated center",
            "anchor_id": "hyperedges[e][0]",
            "matched_f1_validation_mrr": 0.4876775417205556,
        },
        "registered_protocol": {
            "dataset": "cora", "protocol": "standard", "training_negatives": "uniform",
            "seed": 0, "evaluation_negatives_per_positive": 20,
            "hidden_dim": 16, "branch_dim": 8, "layers": 2, "dropout": 0,
            "batch_size": 4096, "ablation": "A5",
            "stages_epochs": {"F0": 1, "F1": 5},
            "test_policy": "test only after a candidate meets GO",
        },
        "integrity_audit": {
            "screening_run_count": len(all_runs),
            "unique_split_hash_count": len(splits),
            "split_hash": next(iter(splits)),
            "test_evaluated_screening_runs": 0,
            "all_screening_test_flags_false": True,
        },
        "candidates": reports,
        "novelty_status": {
            "broad_ARHC_PMHE_ARPM_families": "NOVELTY_CONFLICT",
            "exact_graph_induced_star_operator_claims": "NOVELTY_UNVERIFIED",
            "guarantee": "focused literature search only; no novelty guarantee",
        },
        "next_expected_step": "shift the next research cycle to hypergraph-construction innovation; do not extend these rejected operator variants",
    }
    with (ROOT / "results.json").open("w", encoding="utf-8") as handle:
        json.dump(results, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


if __name__ == "__main__":
    main()
