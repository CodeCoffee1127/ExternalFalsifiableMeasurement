#!/usr/bin/env python3
"""
Canonical bundle entry: EXP024 cardinality convergence / calibration panels (Fig. 3--5).
Paper: Section IV-D--E, Figs.~\\ref{fig:calibration_convergence}, \\ref{fig:bias_distribution}, power curve.

Subcommands:
  empirical   — run ``exp024_real_data_experiment.py`` (needs full Spider / verifier stack).
  simulation  — run ``exp024_gold_standard_expansion_final.py`` (paper-aligned sim).
  figures     — run hardcoded figure emitters ``generate_fig3/4/5_exp024_final.py``.
  all         — simulation then figures (empirical not chained automatically).
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def _run(root: Path, name: str, args: list[str]) -> int:
    script = root / "scripts" / name
    return subprocess.call([sys.executable, str(script), *args])


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    p = argparse.ArgumentParser(description="EXP024 canonical bundle entry")
    p.add_argument(
        "mode",
        choices=("empirical", "simulation", "figures", "all"),
        default="figures",
        nargs="?",
    )
    ns, rest = p.parse_known_args()
    mode = ns.mode

    if mode == "empirical":
        return _run(root, "exp024_real_data_experiment.py", rest)
    if mode == "simulation":
        return _run(root, "exp024_gold_standard_expansion_final.py", rest)
    if mode == "figures":
        for s in (
            "generate_fig3_exp024_final.py",
            "generate_fig4_exp024_final.py",
            "generate_fig5_exp024_final.py",
        ):
            code = _run(root, s, rest)
            if code != 0:
                return code
        return 0
    if mode == "all":
        code = _run(root, "exp024_gold_standard_expansion_final.py", rest)
        if code != 0:
            return code
        for s in (
            "generate_fig3_exp024_final.py",
            "generate_fig4_exp024_final.py",
            "generate_fig5_exp024_final.py",
        ):
            code = _run(root, s, rest)
            if code != 0:
                return code
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
