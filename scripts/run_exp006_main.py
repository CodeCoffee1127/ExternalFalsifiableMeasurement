#!/usr/bin/env python3
"""
Canonical bundle entry: EXP006 cross-model generalization (Table~\\ref{tab:cross-model}).
Paper: Section IX (Integrated Evaluation).

Delegates to ``exp006_cross_model.py``. **Simulation-based** — not live API replication.
See ``docs/disclosures/EXP006_simulation.md``.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    script = root / "scripts" / "exp006_cross_model.py"
    return subprocess.call([sys.executable, str(script), *sys.argv[1:]])


if __name__ == "__main__":
    raise SystemExit(main())
