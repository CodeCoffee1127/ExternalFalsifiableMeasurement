# Quickstart (reviewers)

**First open:** `REVIEWER_START_HERE.md` for the one-page orientation.

## 1. Environment

- Python **3.10+** recommended.
- Install: `pip install -r requirements.txt`
- **`src` → `code` junction** (Windows) or `PYTHONPATH` pointing at `code/`.

## 2. Windows: UTF-8 (required for some drivers)

```bat
set PYTHONIOENCODING=utf-8
```

Or: `scripts\run_with_utf8.bat python scripts\run_exp006_main.py`  
Details: `docs/WINDOWS_UTF8_RUNTIME.md`

## 3. Minimal data (when needed)

See `docs/DATA_MOUNT_DECISIONS.md`:

- `spider/dev.json`, `spider/train_spider.json`
- `data/test/test.json` (EXP025 fallback)
- `data/results/exp003_v5_rev_final/exp003_full_results.jsonl` (EXP010 real H_v path)

## 4. Canonical entry scripts (primary interface)

| Entry script | Support level | Mounted data? | Expected output | Notes / disclosure |
|--------------|---------------|---------------|-----------------|---------------------|
| `run_exp001_main.py` | Hardcoded replot | No | `figures/paper/fig2_*` | EXP001 / Fig. 2 VSP radar; embedded paper-facing constants |
| `run_exp002_main.py` | Hardcoded replot | No | Fig. 6 panels | Synthetic pre-validation layout |
| `run_exp003_main.py` | Source-backed + in-runner synthesis | **Yes** — Spider JSON | `results/exp003_rerun_*` | Not guaranteed to match published R² alone; see `docs/disclosures/EXP003_dual_chain.md` |
| `run_exp006_main.py` | **Simulation-based** | No | `results/exp006_cross_model/*.json` | Not live multi-API |
| `run_exp010_main.py` | Mixed (stats + optional sim) | **Recommended** — `jsonl` | `results/exp010_vsp_sensitivity/*` | Real H_v path when `jsonl` present |
| `run_exp021_main.py` | Source-backed | Check script paths | Script-dependent | Optimized canonical driver |
| `run_exp022_main.py` | Source-backed | Check script paths | Script-dependent | Uses `sqlparse` |
| `run_exp023_main.py` | Source-backed | Check script paths | Script-dependent | Identification comparison |
| `run_exp024_main.py` | **Mode-dependent** | Empirical mode needs full stack | `figures/paper/` or experiment dirs | `figures` / `simulation` / `empirical` / `all` — see `REPRODUCIBILITY.md` |
| `run_exp025_main.py` | **Source-backed audit + asset-bridged figures** | **Yes** — Spider or D_test JSON | `experiment_reports/EXP025_v3/*`, `figures/exp025*`, `figures/exp025_appendix*` | **Not** fully regenerated from a single Python chain to LaTeX PDFs; see §5 below and `SUBMISSION_DISCLOSURE.md` |
| `generate_figures_main.py` | Orchestrator (mixed) | No for default sequence | Multiple under `figures/` | Combines HCR + generators; `--only 1,2,345,6,7` |

**Support-level glossary:** **SB** = source-backed implementation; **PBR** = paper-based reconstruction; **PAR** = paper-aligned reconstruction; **SIM** = simulation; **HCR** = hardcoded replot; **ART** = asset-bridged (shipped LaTeX figures copied into bundle output dirs); **DOC** = documentation-only.

## 5. EXP025 figures (read before judging Fig. 10–12 / Appendix H)

- **Main Figs 10–12** in the PDF are **inspectable** in `paper_sources/figures/` (LaTeX-named files).
- **`run_exp025_main.py figures-main`** / **`figures-appendix`** copy those assets into **`figures/exp025/`** and **`figures/exp025_appendix/`** — **asset-bridged**, not a claim of full regeneration from `run_exp025_v3.py` alone.
- **`run_exp025_main.py analysis`** runs the **preregistered audit script** (`run_exp025_v3.py`); console output and some legacy strings may still be **non-English** (upstream).
- A **trace gap** remains: a fully scripted rebuild of every LaTeX filename is **not** proven in-repo — `docs/gaps/EXP025_figure_regeneration_trace.md`.

## 6. Paper maps

- `docs/mapping/paper_to_project_master_map.md` — section / figure → path.  
- `docs/mapping/PROJECT_STATUS_MATRIX.md` — support level matrix.

## 7. Imports sanity

```bash
python -c "import sys; sys.path.insert(0,'src'); import cpfc, verifier, dynamics, step_extractor; print('ok')"
```

## 8. Paper LaTeX

- `paper_sources/paper1.tex`, `paper_sources/appendices/`.

---

*Full runtime detail: `REPRODUCIBILITY.md`. File inventory: `FILE_MANIFEST.md`.*
