#!/usr/bin/env python3
"""
EXP025 unified analysis entry (complex-tier root-cause chain).
Paper: Section IX-E, Figs.~\\ref{fig:complex_residual_by_depth},
\\ref{fig:stratified_complex_residual}, \\ref{fig:alternative_constructs_complex}.

Delegates to ``run_exp025_v3.py`` (source-backed preregistered layers + JSON/Markdown reports).
This wrapper exists so reviewers see a single paper-aligned name in ``scripts/``.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    script = root / "scripts" / "run_exp025_v3.py"
    return subprocess.call([sys.executable, str(script), *sys.argv[1:]])


if __name__ == "__main__":
    raise SystemExit(main())
