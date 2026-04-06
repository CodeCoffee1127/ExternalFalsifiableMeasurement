#!/usr/bin/env python3
"""
Canonical bundle entry: EXP002 synthetic pre-validation / Fig. 6.
Paper: Section V (Synthetic Pre-Validation), Fig.~\\ref{fig:synthetic_validation}.

Delegates to ``generate_fig6_synthetic_validation.py`` (embedded publication-facing constants).
Classification: hardcoded replot + synthetic panel layout.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    script = root / "scripts" / "generate_fig6_synthetic_validation.py"
    return subprocess.call([sys.executable, str(script), *sys.argv[1:]])


if __name__ == "__main__":
    raise SystemExit(main())
