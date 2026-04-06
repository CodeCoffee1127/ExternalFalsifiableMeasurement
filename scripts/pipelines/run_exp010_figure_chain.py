#!/usr/bin/env python3
"""
EXP010 pipeline: optional statistical run, then Fig. 1 hardcoded emitter.

1. Unless ``--skip-stats``, runs ``run_exp010_main.py`` (delegates to corrected script).
2. Runs ``generate_fig1_exp010_final.py`` (hardcoded paper table values).

Classification: **mixed** — stats may be source-backed with mounted jsonl; figure script is HCR.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    p = argparse.ArgumentParser(description="EXP010 stats + Fig.1 chain")
    p.add_argument("--skip-stats", action="store_true")
    ns, rest = p.parse_known_args()

    if not ns.skip_stats:
        code = subprocess.call(
            [sys.executable, str(root / "scripts" / "run_exp010_main.py"), *rest]
        )
        if code != 0:
            return code
    return subprocess.call(
        [sys.executable, str(root / "scripts" / "generate_fig1_exp010_final.py"), *rest]
    )


if __name__ == "__main__":
    raise SystemExit(main())
