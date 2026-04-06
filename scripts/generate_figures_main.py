#!/usr/bin/env python3
"""
Master figure generation orchestrator (paper order, bundle canonical).

Runs emitter scripts in a fixed sequence matching main-text figure flow where possible.
Individual steps retain their own classification (HCR vs source-backed generator).

Usage:
  python scripts/generate_figures_main.py
  python scripts/generate_figures_main.py --only 7
  python scripts/generate_figures_main.py --only 1,2,345,6,7
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    p = argparse.ArgumentParser(description="Paper-ordered figure orchestrator")
    p.add_argument(
        "--only",
        type=str,
        default="all",
        help="Comma-separated: 1,2,345,6,7 or all",
    )
    ns, rest = p.parse_known_args()
    sel = {x.strip() for x in ns.only.lower().split(",") if x.strip()}
    run_all = "all" in sel or ns.only.lower().strip() == "all"

    def want(label: str) -> bool:
        return run_all or label in sel

    if want("1"):
        code = subprocess.call(
            [sys.executable, str(root / "scripts" / "generate_fig1_exp010_final.py"), *rest]
        )
        if code != 0:
            return code
    if want("2"):
        code = subprocess.call(
            [sys.executable, str(root / "scripts" / "generate_fig2_exp001_final.py"), *rest]
        )
        if code != 0:
            return code
    if want("345"):
        code = subprocess.call(
            [sys.executable, str(root / "scripts" / "run_exp024_main.py"), "figures", *rest]
        )
        if code != 0:
            return code
    if want("6"):
        code = subprocess.call(
            [sys.executable, str(root / "scripts" / "generate_fig6_synthetic_validation.py"), *rest]
        )
        if code != 0:
            return code
    if want("7"):
        code = subprocess.call(
            [
                sys.executable,
                str(root / "scripts" / "generate_fig7_structural_failure_phase2_v32.py"),
                *rest,
            ]
        )
        if code != 0:
            return code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
