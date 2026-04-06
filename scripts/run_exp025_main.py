#!/usr/bin/env python3
"""
Canonical bundle entry: EXP025 complex-tier analysis + figure bridges.
Paper: Section IX-E, Appendix H figures.

Subcommands:
  analysis          — run ``exp025_main_analysis.py`` (v3 audit).
  figures-main        — run ``exp025_generate_main_figures.py``.
  figures-appendix    — run ``exp025_generate_appendix_figures.py``.
  all                 — analysis, then sync main + appendix figures.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def _call(root: Path, rel: str, args: list[str]) -> int:
    return subprocess.call([sys.executable, str(root / "scripts" / rel), *args])


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    p = argparse.ArgumentParser(description="EXP025 canonical bundle entry")
    p.add_argument(
        "command",
        choices=("analysis", "figures-main", "figures-appendix", "all"),
        nargs="?",
        default="analysis",
    )
    ns, rest = p.parse_known_args()
    cmd = ns.command

    if cmd == "analysis":
        return _call(root, "exp025_main_analysis.py", rest)
    if cmd == "figures-main":
        return _call(root, "exp025_generate_main_figures.py", rest)
    if cmd == "figures-appendix":
        return _call(root, "exp025_generate_appendix_figures.py", rest)
    if cmd == "all":
        for name, script in (
            ("analysis", "exp025_main_analysis.py"),
            ("figures-main", "exp025_generate_main_figures.py"),
            ("figures-appendix", "exp025_generate_appendix_figures.py"),
        ):
            args = rest if name == "analysis" else []
            code = _call(root, script, args)
            if code != 0:
                return code
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
