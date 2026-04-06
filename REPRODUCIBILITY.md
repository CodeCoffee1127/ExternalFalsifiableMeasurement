# Reproducibility (submission bundle)

**Orientation:** `REVIEWER_START_HERE.md` → `QUICKSTART.md` → this file.

## Runtime requirements

- **Python:** 3.10+ recommended.
- **Install:** `pip install -r requirements.txt` (includes `brokenaxes` for the Fig. 7 Phase-2 bundle script).
- **Import path:** A **`src` → `code` directory junction** at the bundle root is used so legacy `sys.path.insert(..., "src")` resolves. On non-Windows environments, set:

```bash
export PYTHONPATH="/path/to/this/bundle/code"
```

## UTF-8 on Windows (mandatory for some drivers)

Default **cp936/GBK** consoles break `print()` on Unicode (e.g. `R²`, `✓`, `✗`).

```text
set PYTHONIOENCODING=utf-8
```

See `docs/WINDOWS_UTF8_RUNTIME.md` and `scripts/run_with_utf8.bat`.

## Minimal data mount

Read-only copies documented in **`docs/DATA_MOUNT_DECISIONS.md`**:

- `spider/dev.json`, `spider/train_spider.json`
- `data/test/test.json` (EXP025 fallback)
- `data/results/exp003_v5_rev_final/exp003_full_results.jsonl` (EXP010 / loader family)

**Not shipped:** full Spider SQLite, bulk `results/`, cloud duplicate `jsonl`.

## Canonical submission entrypoints

Use **`scripts/run_exp001_main.py` … `run_exp025_main.py`** as the primary interface. They delegate to legacy script filenames without hiding classification.

Additional orchestrators:

- `scripts/generate_figures_main.py` — paper-ordered figure batch.
- `scripts/pipelines/run_exp010_figure_chain.py` — EXP010 stats → Fig. 1.
- `scripts/exp025_main_analysis.py`, `exp025_generate_main_figures.py`, `exp025_generate_appendix_figures.py` — EXP025 audit + LaTeX-named asset bridge.

## Which chains are runnable

| Chain | Canonical entry | Legacy delegate | Classification |
|-------|-----------------|-----------------|----------------|
| EXP001 | `run_exp001_main.py` | `generate_fig2_exp001_final.py` | **HCR** |
| EXP002 | `run_exp002_main.py` | `generate_fig6_synthetic_validation.py` | **HCR** |
| EXP003 | `run_exp003_main.py` | `exp003_full_rerun.py` | **Mixed** (Spider + in-runner synthesis) |
| EXP006 | `run_exp006_main.py` | `exp006_cross_model.py` | **SIM** |
| EXP010 | `run_exp010_main.py` | `exp010_vsp_calibration_corrected.py` | **Mixed** |
| EXP021–023 | `run_exp021_main.py` … | `exp021_*`, `exp022_*`, `exp023_*` | **SB** (check data paths) |
| EXP024 | `run_exp024_main.py` | `exp024_*`, `generate_fig3/4/5_*` | **empirical / PAR sim / HCR** by mode |
| EXP025 | `run_exp025_main.py` | `run_exp025_v3.py` + figure bridges | **SB audit + ART** figures |
| Fig batch | `generate_figures_main.py` | various | **Mixed** |
| StepExtractor | `import step_extractor` | — | **PBR** executable + gap docs |
| EXP003 paper table | — | `paper_aligned_reconstruction/exp003_v5_rev_final_target_matching.py` | **PAR** |

## Recommended execution order

1. Read **`docs/mapping/paper_to_project_master_map.md`**, **`docs/mapping/PROJECT_STATUS_MATRIX.md`**, **`SUBMISSION_DISCLOSURE.md`**.
2. Set UTF-8 (Windows).
3. `python scripts/run_exp006_main.py` — quick disclosed simulation smoke test.
4. `python scripts/run_exp010_main.py` — with mounted `jsonl` when available.
5. Optional: `run_exp003_main.py`, `run_exp025_main.py analysis`, `run_exp025_main.py figures-main`.
6. `python scripts/generate_figures_main.py --only 1,2` — sample HCR emitters.

## What cannot currently be claimed

- **Full** end-to-end replication of every reported number from **raw verifier logs** inside this zip alone.
- **Production** StepExtractor parity (the bundle ships a **PBR** minimal engine + heuristics).
- **Live** GPT-4 / Claude-3 runs for EXP006.
- **Proven** Python-only regeneration of all **LaTeX-named** EXP025 figures (see `docs/gaps/EXP025_figure_regeneration_trace.md`).

---

*See also: `README.md`, `QUICKSTART.md`, `docs/reconstruction/RECOVERY_REPORT.md`, `FILE_MANIFEST.md`, `SUBMISSION_PACKAGE_NOTE.md`.*
