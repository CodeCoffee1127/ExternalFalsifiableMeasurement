#!/usr/bin/env python3
"""
EXP025 appendix-related figures (Appendix H family in ``paper_sources/figures``).

Classification: **paper-aligned reconstruction** — copies shipped LaTeX assets into
``figures/exp025_appendix/`` for a unified reviewer path.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

APX_STEMS = (
    "04_appx_figA_complex_subgroup_distribution",
    "05_appx_figB_verifier_stability_panel",
    "06_appx_figC_compile_distortion_association",
    "07_appx_figE_complex_tier_diagnostic_flow",
)
EXTENSIONS = (".pdf", ".png")


def main() -> int:
    p = argparse.ArgumentParser(description="Sync EXP025 appendix figures from paper_sources")
    p.add_argument("--out", type=Path, default=None)
    ns = p.parse_args()
    root = Path(__file__).resolve().parents[1]
    src_dir = root / "paper_sources" / "figures"
    out_dir = ns.out or (root / "figures" / "exp025_appendix")
    out_dir.mkdir(parents=True, exist_ok=True)
    copied = 0
    for stem in APX_STEMS:
        for ext in EXTENSIONS:
            src = src_dir / f"{stem}{ext}"
            if src.is_file():
                shutil.copy2(src, out_dir / src.name)
                copied += 1
    print(f"EXP025 appendix figures: copied {copied} files to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
