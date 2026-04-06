# FILE_MANIFEST.md — submission package (trimmed)

This manifest describes **this reviewer-facing zip**, not the full archival reconstruction tree.

**Legend:** **SB** source-backed | **PBR** paper-based reconstruction | **PAR** paper-aligned | **SIM** simulation | **HCR** hardcoded replot | **ART** asset-bridged | **DOC** documentation.

## Root (reviewer core)

| Path | Role |
|------|------|
| `README.md` | Scope, terminology, entry commands |
| `REVIEWER_START_HERE.md` | One-page orientation |
| `QUICKSTART.md` | UTF-8, data, **canonical `run_exp*_main.py` table** |
| `SUBMISSION_DISCLOSURE.md` | Limitations and classifications |
| `REPRODUCIBILITY.md` | Runtime and chain detail |
| `FILE_MANIFEST.md` | This file |
| `SUBMISSION_PACKAGE_NOTE.md` | Provenance of this export |
| `requirements.txt`, `.gitignore` | Environment |

## `docs/`

| Path | Role |
|------|------|
| `docs/DATA_MOUNT_DECISIONS.md` | Minimal mounted data provenance |
| `docs/WINDOWS_UTF8_RUNTIME.md` | Windows console encoding |
| `docs/disclosures/*.md` | EXP003 / EXP006 disclosures |
| `docs/gaps/*.md` | StepExtractor, EXP025 trace gap |
| `docs/mapping/paper_to_project_master_map.md` | Paper section → artifact map |
| `docs/mapping/PROJECT_STATUS_MATRIX.md` | Support level matrix |

## `docs/reconstruction/`

| Path | Role |
|------|------|
| `docs/reconstruction/RECOVERY_REPORT.md` | Missing vs reconstructed vs unrecoverable (optional deep read) |

## Code and scripts

| Path | Role |
|------|------|
| `code/` | CPFC, verifier, state, dynamics, step_extractor (PBR core), … |
| `src` | Junction → `code` (Windows) |
| `scripts/run_exp001_main.py` … `run_exp025_main.py` | Canonical experiment entry layer |
| `scripts/generate_figures_main.py` | Figure orchestrator |
| `scripts/pipelines/run_exp010_figure_chain.py` | EXP010 stats → Fig.1 |
| `scripts/exp025_*`, `run_exp025_v3.py`, … | Supporting implementation (legacy language possible) |
| `scripts/run_with_utf8.bat` | UTF-8 helper |

## Data and results (minimal)

| Path | Role |
|------|------|
| `spider/*.json`, `data/**` | Minimal mount for EXP003 / EXP025 / EXP010 paths |
| `results/README_RUN_EVIDENCE.md` | Explains retained JSON evidence |
| `results/exp006_cross_model/`, `exp010_vsp_sensitivity/` | Small runnable evidence |
| `results/exp003_rerun_20260312/` | **Subset only** (global/tiered JSON + manifest + freeze log; no full log/jsonl duplicate here) |

## Figures and paper

| Path | Role |
|------|------|
| `paper_sources/` | `paper1.tex`, appendices, LaTeX figure assets |
| `figures/` | Regenerated panels (partial set) + `paper/` |

## Not included here (still in archival bundle)

`ACTION_LOG.md`, `BUNDLE_CLEAN_CHECK.md`, `inventory.jsonl`, `phase3b_summary.json`, `canonical_conflicts_phase3b.md`, `component_mapping_phase3.md`, `docs/PATH_SELF_CHECK.md`, `docs/MINIMAL_RUN_BLOCKERS.md`, duplicate EXP025 reports, full EXP003 rerun logs, and other internal-only artifacts.

---

*Submission export — trimmed for reviewers.*
