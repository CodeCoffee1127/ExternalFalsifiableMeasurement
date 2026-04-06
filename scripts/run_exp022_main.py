#!/usr/bin/env python3
"""
Canonical bundle entry: EXP022 semantic tier recalibration.
Paper: Section IX-C, Table~\\ref{tab:exp022}.

Delegates to ``exp022_semantic_tier_recalibration_optimized.py`` (canonical optimized branch).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    script = root / "scripts" / "exp022_semantic_tier_recalibration_optimized.py"
    return subprocess.call([sys.executable, str(script), *sys.argv[1:]])


if __name__ == "__main__":
    raise SystemExit(main())
