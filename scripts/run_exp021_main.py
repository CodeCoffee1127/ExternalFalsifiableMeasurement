#!/usr/bin/env python3
"""
Canonical bundle entry: EXP021 risk memory directionality.
Paper: Section IX-B, Table~\\ref{tab:exp021}.

Delegates to ``exp021_risk_memory_validation_optimized.py`` (canonical optimized branch).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    script = root / "scripts" / "exp021_risk_memory_validation_optimized.py"
    return subprocess.call([sys.executable, str(script), *sys.argv[1:]])


if __name__ == "__main__":
    raise SystemExit(main())
