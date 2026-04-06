#!/usr/bin/env python3
"""
Canonical bundle entry: EXP001 (VSP four-criteria) / Fig. 2 radar.
Paper: Section IV (Measurement Apparatus), Fig.~\\ref{fig:vsp_radar}, Table~\\ref{tab:vsp}.

Delegates to source-backed ``generate_fig2_exp001_final.py`` (hardcoded paper values for panels).
Classification: hardcoded replot (supporting implementation preserved under legacy filename).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    script = root / "scripts" / "generate_fig2_exp001_final.py"
    return subprocess.call([sys.executable, str(script), *sys.argv[1:]])


if __name__ == "__main__":
    raise SystemExit(main())
