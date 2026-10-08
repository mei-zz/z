#!/usr/bin/env python3
"""Config-driven, reproducible scientific figure generator.

Supported kinds: line, grouped_bar, ablation, box, scatter, heatmap, radar,
network, and multidataset. The input config is JSON; no values are fabricated.
"""
import argparse
import json
import shutil
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

PALETTE = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9", "#000000", "#F0E442"]
MARKERS = ["o", "s", "^", "D", "v", "P", "X", "*"]
LINESTYLES = ["-", "--", "-.", ":"]
HATCHES = ["", "///", "\\\\", "xx", "..", "++", "oo", "**"]


def load_data(path, cfg):
    suffix = path.suffix.lower()
    if suffix == ".csv":
        df = pd.read_csv(path)
    elif suffix in {".xlsx", ".xls"}:
        df = pd.read_excel(path, sheet_name=cfg.get("sheet", 0))
    elif suffix in {".json", ".jsonl"}:
        if suffix == ".jsonl":
            df = pd.read_json(path, lines=True)
        else:
            obj = json.loads(path.read_text(encoding="utf-8"))
            records = obj
            for key in cfg.get("record_path", []):
                records = records[key]
            df = pd.json_normalize(records)
    elif suffix in {".log", ".txt"}:
        pattern = cfg.get("log_regex")
        if not pattern:
            raise ValueError("Structured log input requires config.log_regex with named groups")
        df = pd.Series(path.read_text(encoding="utf-8", errors="replace").splitlines(), name="line").str.extract(pattern).dropna(how="all")
    else:
        raise ValueError(f"Unsupported input type: {suffix}")
    if df.empty:
        raise ValueError("Input contains no plottable rows")
    return df


def require(df, columns):
    missing = [c for c in columns if c and c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}; available={list(df.columns)}")


def style(cfg):
    mpl.rcParams.update({
        "font.family": cfg.get("font_family", "DejaVu Sans"),
        "font.size": cfg.get("font_size", 8),
        "axes.labelsize": cfg.get("label_size", 8),
        "axes.titlesize": cfg.get("title_size", 9),
        "xtick.labelsize": cfg.get("tick_size", 7),
        "ytick.labelsize": cfg.get("tick_size", 7),
        "legend.fontsize": cfg.get("legend_size", 7),
        "axes.linewidth": 0.9,
        "lines.linewidth": 1.1,
        "lines.markersize": 4.5,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.03,
    })


def groups(df, group):
    return [("", df)] if not group else list(df.groupby(group, sort=False))


def plot_line(ax, df, cfg):
    require(df, [cfg["x"], cfg["y"], cfg.get("group"), cfg.get("error")])
    for i, (name, part) in enumerate(groups(df, cfg.get("group"))):
        part = part.sort_values(cfg["x"])
        err = part[cfg["error"]] if cfg.get("error") else None
        ax.errorbar(part[cfg["x"]], part[cfg["y"]], yerr=err, label=str(name), color=PALETTE[i % len(PALETTE)], marker=MARKERS[i % len(MARKERS)], linestyle=LINESTYLES[i % len(LINESTYLES)], capsize=2)


def plot_bar(ax, df, cfg):
    require(df, [cfg["x"], cfg["y"], cfg.get("group"), cfg.get("error")])
    gs = groups(df, cfg.get("group")); cats = list(dict.fromkeys(df[cfg["x"]].tolist()))
    width = 0.8 / len(gs); x = np.arange(len(cats))
    for i, (name, part) in enumerate(gs):
        indexed = part.set_index(cfg["x"]).reindex(cats)
        vals = indexed[cfg["y"]].to_numpy(dtype=float)
        err = indexed[cfg["error"]].to_numpy(dtype=float) if cfg.get("error") else None
        ax.bar(x - 0.4 + width / 2 + i * width, vals, width, yerr=err, label=str(name), color=PALETTE[i % len(PALETTE)], edgecolor="black", linewidth=0.55, hatch=HATCHES[i % len(HATCHES)], capsize=2)
    ax.set_xticks(x, cats)


def plot_box(ax, df, cfg):
    require(df, [cfg["x"], cfg["y"]])
    cats = list(dict.fromkeys(df[cfg["x"]].tolist()))
    vals = [df.loc[df[cfg["x"]] == c, cfg["y"]].dropna().to_numpy() for c in cats]
    bp = ax.boxplot(vals, labels=cats, patch_artist=True, showfliers=True)
    for i, box in enumerate(bp["boxes"]):
        box.set(facecolor=PALETTE[i % len(PALETTE)], alpha=0.75)


def plot_scatter(ax, df, cfg):
    require(df, [cfg["x"], cfg["y"], cfg.get("group")])
    for i, (name, part) in enumerate(groups(df, cfg.get("group"))):
        ax.scatter(part[cfg["x"]], part[cfg["y"]], label=str(name), color=PALETTE[i % len(PALETTE)], marker=MARKERS[i % len(MARKERS)], s=24, edgecolors="black", linewidths=0.35)


def plot_heatmap(ax, df, cfg):
    require(df, [cfg["row"], cfg["column"], cfg["value"]])
    matrix = df.pivot(index=cfg["row"], columns=cfg["column"], values=cfg["value"])
    im = ax.imshow(matrix.to_numpy(dtype=float), cmap=cfg.get("cmap", "viridis"), aspect="auto")
    ax.set_xticks(range(len(matrix.columns)), matrix.columns, rotation=cfg.get("x_rotation", 30), ha="right")
    ax.set_yticks(range(len(matrix.index)), matrix.index)
    plt.colorbar(im, ax=ax, label=cfg.get("colorbar_label", cfg["value"]))


def plot_radar(ax, df, cfg):
    require(df, [cfg["metric"], cfg["value"], cfg.get("group")])
    metrics = list(dict.fromkeys(df[cfg["metric"]].tolist())); angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist(); angles += angles[:1]
    for i, (name, part) in enumerate(groups(df, cfg.get("group"))):
        vals = part.set_index(cfg["metric"]).reindex(metrics)[cfg["value"]].to_numpy(dtype=float).tolist(); vals += vals[:1]
        ax.plot(angles, vals, label=str(name), color=PALETTE[i % len(PALETTE)], marker=MARKERS[i % len(MARKERS)]); ax.fill(angles, vals, color=PALETTE[i % len(PALETTE)], alpha=0.08)
    ax.set_xticks(angles[:-1], metrics)


def plot_network(ax, df, cfg):
    require(df, [cfg["source"], cfg["target"]])
    graph = nx.from_pandas_edgelist(df, cfg["source"], cfg["target"], edge_attr=cfg.get("weight"), create_using=nx.DiGraph() if cfg.get("directed", False) else nx.Graph())
    pos = nx.spring_layout(graph, seed=cfg.get("layout_seed", 42), weight=cfg.get("weight"))
    nx.draw_networkx(graph, pos, ax=ax, node_color="#56B4E9", edge_color="#666666", node_size=cfg.get("node_size", 500), font_size=cfg.get("network_font_size", 7), arrows=cfg.get("directed", False), width=1.0)
    ax.set_axis_off()


def decorate(ax, cfg):
    if cfg.get("title"): ax.set_title(cfg["title"])
    if cfg.get("xlabel"): ax.set_xlabel(cfg["xlabel"])
    if cfg.get("ylabel"): ax.set_ylabel(cfg["ylabel"])
    if "ylim" in cfg: ax.set_ylim(*cfg["ylim"])
    if "xlim" in cfg: ax.set_xlim(*cfg["xlim"])
    if cfg.get("grid", True) and cfg["kind"] not in {"heatmap", "radar", "network"}: ax.grid(axis="y", color="#D9D9D9", linewidth=0.5, zorder=0)
    if cfg.get("group") and cfg.get("legend", True): ax.legend(frameon=False, loc=cfg.get("legend_loc", "best"), ncol=cfg.get("legend_ncols", 1))
    ax.tick_params(direction="out", width=0.8, length=3)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--config", required=True); ap.add_argument("--output-root", default="figures"); args = ap.parse_args()
    cfg_path = Path(args.config).resolve(); cfg = json.loads(cfg_path.read_text(encoding="utf-8")); figure_id = cfg.get("figure_id", cfg_path.stem)
    input_path = Path(cfg["input"]); input_path = input_path if input_path.is_absolute() else (cfg_path.parent / input_path).resolve()
    df = load_data(input_path, cfg); style(cfg)
    root = Path(args.output_root).resolve()
    for sub in ["source_data", "scripts", "pdf", "svg", "png", "captions"]: (root / sub).mkdir(parents=True, exist_ok=True)
    df.to_csv(root / "source_data" / f"{figure_id}.csv", index=False)
    shutil.copy2(cfg_path, root / "scripts" / f"{figure_id}.json")
    kind = cfg["kind"]; projection = "polar" if kind == "radar" else None
    fig, ax = plt.subplots(figsize=tuple(cfg.get("figsize", [3.5, 2.6])), subplot_kw={"projection": projection} if projection else None)
    funcs = {"line": plot_line, "grouped_bar": plot_bar, "ablation": plot_bar, "multidataset": plot_bar, "box": plot_box, "scatter": plot_scatter, "heatmap": plot_heatmap, "radar": plot_radar, "network": plot_network}
    if kind not in funcs: raise ValueError(f"Unsupported kind: {kind}; choose {sorted(funcs)}")
    funcs[kind](ax, df, cfg); decorate(ax, cfg); fig.tight_layout()
    fig.savefig(root / "pdf" / f"{figure_id}.pdf")
    fig.savefig(root / "svg" / f"{figure_id}.svg")
    fig.savefig(root / "png" / f"{figure_id}.png", dpi=600)
    caption = cfg.get("caption", f"Figure X. {cfg.get('title', figure_id)}. Define panels, metrics, units, sample sizes, error bars, statistical tests, and abbreviations before submission.")
    (root / "captions" / f"{figure_id}.md").write_text(caption.strip() + "\n", encoding="utf-8")
    plt.close(fig)
    print(json.dumps({"figure_id": figure_id, "input": str(input_path), "rows": len(df), "output_root": str(root)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
