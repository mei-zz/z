"""Post-run report polish that preserves all machine-generated metrics."""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
RESULTS = json.loads((OUT / "results.json").read_text(encoding="utf-8"))


def write_novelty() -> None:
    text = """# Focused novelty check

Search date: 2026-10-02. Scope: exact phrases for quantile-trimmed, truncated and rank-window hard-negative selection in graph link prediction; semi-hard sampling; dynamic/self-adversarial negatives; and adjacent hyperlink/hyperedge prediction. The focused search did not confirm a paper implementing the frozen V7.1 QTHS rule. This is not an exhaustive priority review.

| Work | Relevant overlap | Distinction from frozen QTHS25 |
|---|---|---|
| [ProGCL (ICML 2022)](https://proceedings.mlr.press/v162/xia22b.html) | Studies when hardest graph-contrastive negatives are unreliable. | Contrastive node representation and reliability weighting, rather than supervised pairwise link prediction with a frozen graph teacher and fixed top-2 rule. |
| [DMNS (WWW 2024)](https://arxiv.org/abs/2403.17259) | Graph link prediction with controlled negative hardness. | Conditional diffusion generates multi-level negatives; it does not trim a fixed per-positive teacher-ranked candidate prepool. |
| [MeBNS (2023 preprint)](https://arxiv.org/abs/2312.04815) | Teacher–student learning and dynamic hard-negative handling for link prediction. | Meta-learning and sample reweighting differ from QTHS's frozen, parameter-free rank selection. |
| [RotatE (ICLR 2019)](https://arxiv.org/abs/1902.10197) | Introduces self-adversarial negative sampling. | Knowledge-graph embedding weights sampled negatives by current model scores; it is not fixed graph-teacher top-tail trimming. |
| [HeaRT (NeurIPS 2023)](https://proceedings.neurips.cc/paper_files/paper/2023/hash/0be50b4590f1c5fdf4c8feddd63c4f67-Abstract-Datasets_and_Benchmarks.html) | Establishes hard negative candidates for link-prediction evaluation. | Evaluation benchmark construction, not training-time negative selection. |
| [Negative Sampling for Hyperlink Prediction in Networks (2020)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7206280/) | Characterizes negative-sampling hardness in higher-order hyperlink prediction. | Hyperlink prediction and structural sampling, not pairwise graph LP with a frozen graph teacher and a stable-hash top-2 trim. |
| [Hard Negative Sampling in Hyperedge Prediction (2025)](https://arxiv.org/abs/2503.08743) | Direct hard-negative work for higher-order prediction. | Synthesizes hyperedge negatives in embedding space rather than selecting pairwise graph-link negatives from a fixed candidate pool. |
| [Gelato (2024 preprint)](https://arxiv.org/abs/2412.00261) | Uses graph partitioning to select hard pairs for sparse link prediction. | Partition-based candidate selection and a ranking objective differ from the fixed per-positive teacher rank trim. |

**NOVELTY_STATUS: EXACT_RULE_UNVERIFIED.** No exact-rule conflict was confirmed in this focused check. Do not claim priority; retain an exact-rule comparison in manuscript preparation.

The project source audit found no ready-to-run DNS, self-adversarial or DMNS implementation. Those methods were not recreated from scratch; the registered Random-hard and SH75 controls were run instead.
"""
    (OUT / "07_NOVELTY.md").write_text(text, encoding="utf-8")


def append_five_seed_and_transfer() -> None:
    lines = ["", "## Additional stability and transfer checks", ""]
    for dataset, block in RESULTS.get("five_seed_gate", {}).items():
        test = block["test"]
        delta = block["QTHS25_minus_GRAPH_HARD_by_seed"]
        lines.append(
            f"- {dataset.title()} 5-seed test: Graph-hard {test['GRAPH_HARD']['mean']:.6f} ± {test['GRAPH_HARD']['sample_std']:.6f}; "
            f"QTHS25 {test['QTHS25']['mean']:.6f} ± {test['QTHS25']['sample_std']:.6f}; "
            f"paired delta {block['paired_mean_delta']:+.6f}; QTHS wins {block['QTHS25_wins']}/5; "
            f"per-seed deltas {delta}."
        )
    transfer = RESULTS.get("cross_dataset_backbone_transfer", {})
    if transfer:
        lines.append(
            f"- Citeseer GraphSAGE seed 0 validation transfer: Graph-hard {transfer['GRAPH_HARD']:.6f}, "
            f"QTHS25 {transfer['QTHS25']:.6f}, delta {transfer['paired_delta']:+.6f}."
        )
    if len(lines) == 3:
        lines.append("- No additional 5-seed extension was registered after the PubMed gate.")
    path = OUT / "FINAL_REPORT.md"
    current = path.read_text(encoding="utf-8")
    marker = "## Additional stability and transfer checks"
    if marker in current:
        current = current.split(marker)[0].rstrip() + "\n"
    path.write_text(current.rstrip() + "\n" + "\n".join(lines) + "\n", encoding="utf-8")


def add_control_audit_note() -> None:
    path = OUT / "05_SEMIHARD_CONTROL.md"
    current = path.read_text(encoding="utf-8")
    note = "\n- Existing-baseline audit: no ready DNS, self-adversarial or DMNS implementation was found in the project. Those methods were not reimplemented from scratch; RANDOM_HARD50 and SH75 provide the registered matched controls.\n"
    if "Existing-baseline audit:" not in current:
        path.write_text(current.rstrip() + "\n" + note, encoding="utf-8")


def main() -> None:
    write_novelty()
    append_five_seed_and_transfer()
    add_control_audit_note()


if __name__ == "__main__":
    main()
