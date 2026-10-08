#!/usr/bin/env python3
"""Audit a figures/ package for required artifacts and basic export quality."""
import argparse
import json
import shutil
import subprocess
from pathlib import Path
from xml.etree import ElementTree as ET
from PIL import Image


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--root", default="figures"); args = ap.parse_args(); root = Path(args.root).resolve()
    required = ["source_data", "scripts", "pdf", "svg", "png", "captions"]
    warnings = []
    for d in required:
        if not (root / d).is_dir(): warnings.append(f"missing directory: {d}")
    ids = sorted({p.stem for d in ["pdf", "svg", "png"] if (root/d).exists() for p in (root/d).iterdir() if p.is_file()})
    for fid in ids:
        for d, ext in [("pdf", ".pdf"), ("svg", ".svg"), ("png", ".png"), ("source_data", ".csv"), ("captions", ".md")]:
            if not (root / d / f"{fid}{ext}").exists(): warnings.append(f"{fid}: missing {d}/{fid}{ext}")
        png = root / "png" / f"{fid}.png"
        if png.exists():
            with Image.open(png) as im:
                dpi = im.info.get("dpi", (0, 0))
                if min(im.size) < 1000: warnings.append(f"{fid}: PNG small ({im.size[0]}x{im.size[1]} px)")
                if dpi and min(dpi) < 590: warnings.append(f"{fid}: PNG metadata below 600 DPI ({dpi})")
        svg = root / "svg" / f"{fid}.svg"
        if svg.exists():
            try:
                tree = ET.parse(svg); texts = [e for e in tree.iter() if e.tag.endswith("text")]
                if not texts: warnings.append(f"{fid}: SVG has no editable text elements")
            except ET.ParseError as exc: warnings.append(f"{fid}: invalid SVG: {exc}")
        pdf = root / "pdf" / f"{fid}.pdf"
        if pdf.exists() and shutil.which("pdffonts"):
            proc = subprocess.run(["pdffonts", str(pdf)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            for line in proc.stdout.splitlines()[2:]:
                cols = line.split()
                if len(cols) >= 6 and cols[-3].lower() == "no": warnings.append(f"{fid}: unembedded PDF font: {line}")
    report = {"root": str(root), "figure_ids": ids, "warnings": warnings, "manual_checks": ["clipping/overlap", "legend occlusion", "minimum text size", "grayscale distinction", "deuteranopia/protanopia distinction", "axis units and uncertainty definitions"]}
    (root / "audit_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(1 if warnings else 0)


if __name__ == "__main__":
    main()
