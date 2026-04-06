#!/usr/bin/env python3
"""
Canonical bundle entry: EXP010 differential validity under calibration stress.
Paper: Section IV, Fig.~\\ref{fig:differential_validity}.

Delegates to ``exp010_vsp_calibration_corrected.py``. Prefer mounted
``data/results/exp003_v5_rev_final/exp003_full_results.jsonl`` for real H_v path.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    script = root / "scripts" / "exp010_vsp_calibration_corrected.py"
    return subprocess.call([sys.executable, str(script), *sys.argv[1:]])


if __name__ == "__main__":
    raise SystemExit(main())
