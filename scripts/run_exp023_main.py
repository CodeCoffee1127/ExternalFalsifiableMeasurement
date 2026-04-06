#!/usr/bin/env python3
"""
Canonical bundle entry: EXP023 gating vs step fixed effects (identification stress).
Paper: Section VIII, Table~\\ref{tab:exp023_comparison}.

Delegates to ``exp023_gate_vs_stepfe.py``.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    script = root / "scripts" / "exp023_gate_vs_stepfe.py"
    return subprocess.call([sys.executable, str(script), *sys.argv[1:]])


if __name__ == "__main__":
    raise SystemExit(main())
