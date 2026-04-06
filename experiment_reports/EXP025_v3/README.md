# EXP025 v3 run artifacts

This folder contains **timestamped outputs** from `scripts/run_exp025_v3.py` (preregistered layers, data audit, technical report).

## Disclosure

- Some legacy **non-English** strings may appear inside auto-generated Markdown/JSON from the upstream script templates. The **canonical English** traceability statement is `docs/gaps/EXP025_figure_regeneration_trace.md`.
- **LaTeX filenames** for Main Figs 10–12 are **not** proven to regenerate from these scripts alone.

## How to reproduce

From bundle root, with minimal Spider JSON mounted (`docs/DATA_MOUNT_DECISIONS.md`):

```text
set PYTHONIOENCODING=utf-8
python scripts/run_exp025_v3.py
```
