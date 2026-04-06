#!/usr/bin/env python3
"""
EXP025 main-text figures (Fig. 10--12) — result-to-artifact bridge.

Classification: **paper-aligned reconstruction** when full recompute is unavailable.
Copies LaTeX-named assets from ``paper_sources/figures/`` into ``figures/exp025/``
so the bundle exposes a single reviewer path: generated outputs + shipped PDFs.

This does **not** claim the v3 audit script alone reproduces these PDFs bitwise.
See ``docs/gaps/EXP025_figure_regeneration_trace.md``.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

MAIN_PATTERNS = (
    "01_main_fig10_complex_residual_by_depth",
    "02_main_fig11_stratified_residual_distribution",
    "03_main_fig12_alternative_constructs_comparison",
)
EXTENSIONS = (".pdf", ".png")


def main() -> int:
    p = argparse.ArgumentParser(description="Sync EXP025 main figures from paper_sources")
    p.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output directory (default: <bundle>/figures/exp025)",
    )
    ns = p.parse_args()
    root = Path(__file__).resolve().parents[1]
    src_dir = root / "paper_sources" / "figures"
    out_dir = ns.out or (root / "figures" / "exp025")
    out_dir.mkdir(parents=True, exist_ok=True)

    copied = 0
    for stem in MAIN_PATTERNS:
        for ext in EXTENSIONS:
            src = src_dir / f"{stem}{ext}"
            if src.is_file():
                shutil.copy2(src, out_dir / src.name)
                copied += 1
    print(f"EXP025 main figures: copied {copied} files to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
