#!/usr/bin/env python3
"""
Canonical bundle entry: EXP003 Rescue dynamics validation (tiered / global narrative).
Paper: Section VIII--IX, abstract statistics, Table principled degradation.

Delegates to ``exp003_full_rerun.py`` (source-backed runner). Trajectory rows may be
synthesized in-script; see ``docs/disclosures/EXP003_dual_chain.md`` and ``SUBMISSION_DISCLOSURE.md``.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    script = root / "scripts" / "exp003_full_rerun.py"
    return subprocess.call([sys.executable, str(script), *sys.argv[1:]])


if __name__ == "__main__":
    raise SystemExit(main())
