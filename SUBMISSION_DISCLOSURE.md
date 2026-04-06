# Submission disclosure (for editors and reviewers)

This bundle is a **paper-aligned, submission-facing** code + data project: a **single coherent tree** mapped from `paper_sources/paper1.tex` (see `docs/mapping/paper_to_project_master_map.md`). It is **auditable** and **non-misleading** about what is source-backed vs reconstructed.

## 1. What this package is

- **Source-backed** copies of selected Python modules and experiment drivers from a read-only upstream tree (not modified in place).
- **Paper sources** (LaTeX) copied for cross-reference with claims.
- **Paper-based / paper-aligned reconstructions** where the formal specification or full artifact trail is missing, labeled explicitly in `docs/reconstruction/RECOVERY_REPORT.md` and `FILE_MANIFEST.md`.
- **Minimal data** mounts (Spider JSON + one canonical `exp003_full_results.jsonl`) documented in `docs/DATA_MOUNT_DECISIONS.md`.

## 2. Formal specification gaps

### StepExtractor (Appendix A Algorithm 1)

- **Paper-based reconstruction (executable):** `VerifierDrivenStepExtractor` in `code/step_extractor/step_extractor.py` with `segmentation.structure_parse`, `schema.StepObject` (JSON fields `proposition`, `parent_refs`, `step_id`). This is a **minimal** StructureParse, **not** claimed equal to lost production code. See `code/step_extractor/README_RECONSTRUCTION.md`.
- **Source-backed empirical path:** LLM clause-wise chaining in `code/llm/aliyun_api.py` + `code/pipeline/experiment_pipeline.py`.
- **Bridge:** `code/step_extractor/bridge_sql_pipeline.py` maps clause records to `StepObject` for traceability.
- **Gap statement + legacy adapter text:** `paper_based_step_extractor_reconstruction.py`, `docs/gaps/STEP_EXTRACTOR_APPENDIX_A_GAP.md`

## 3. Dual or forked experiment chains

### EXP003

- **Empirical-style runner:** `scripts/exp003_full_rerun.py` (tiered sampling + **synthetic** trajectory generation in-script when rerun — see runner code and `docs/reconstruction/RECOVERY_REPORT.md`).
- **Paper-aligned target-matching chain:** `scripts/paper_aligned_reconstruction/exp003_v5_rev_final_target_matching.py` — reproduces **published numeric targets** by construction of the upstream method, **not** interchangeable with “what the live stack printed” without disclosure.
- **Disclosure:** `docs/disclosures/EXP003_dual_chain.md`

## 4. Simulation-based chains

### EXP006 / Table cross-model

- **Canonical entry:** `scripts/run_exp006_main.py` → `scripts/exp006_cross_model.py`
- **Behavior:** `simulate_model_results` — noise around optional baseline; **no** multi-vendor API replication.
- **Disclosure:** `docs/disclosures/EXP006_simulation.md`

## 5. Hardcoded or paper-table figure scripts

- Examples include `scripts/generate_fig1_exp010_final.py`, `scripts/generate_fig3_exp024_final.py`, `scripts/generate_fig4_exp024_final.py`, `scripts/generate_fig5_exp024_final.py`, and `scripts/generate_fig6_synthetic_validation.py` (synthetic pre-validation panels with embedded publication-facing constants per upstream docstrings).
- **Meaning:** They **replot** or layout values tied to the paper; they do **not** alone prove recomputation from raw verifier logs.

## 6. EXP010 statistical path vs figure path

- **Stats:** `scripts/exp010_vsp_calibration_corrected.py` can load **real** \(H_v\) from mounted `exp003_full_results.jsonl` (v5_rev_final family artifact).
- **Fig. 1:** hardcoded table script remains a **separate** pipeline unless you rewire inputs yourself.
- **Disclosure:** `docs/reconstruction/RECOVERY_REPORT.md`, `results/README_RUN_EVIDENCE.md`

## 7. EXP025 / Main Figs 10–12 / Appendix H (explicit support levels)

**What reviewers should assume:** figures are **checkable against the paper** via shipped LaTeX assets; they are **not** claimed to be **fully regenerated** by one continuous Python pipeline from raw logs inside this zip.

| Item | Support level | Fully regenerated from this repo? |
|------|---------------|-----------------------------------|
| LaTeX-named PDFs/PNGs in `paper_sources/figures/` (`01_main_fig10_*`, `02_*`, `03_*`, appendix `04_*`–`07_*`) | **Asset-bridged** (shipped with LaTeX) | **No** — they are submission references bundled for alignment |
| `figures/exp025/`, `figures/exp025_appendix/` after `run_exp025_main.py figures-*` | **Asset-bridged** (copy/sync from `paper_sources/figures/`) | **No** — same pixels as shipped assets, not a recompute proof |
| `run_exp025_v3.py` audit + JSON/Markdown under `experiment_reports/EXP025_v3/` | **Source-backed** preregistered layer logic | **Partial** — statistical narrative; **does not** close the PDF filename pipeline |
| Trace from v3 numbers → exact main-text figure files | **Documentation-only gap** | **No** — see `docs/gaps/EXP025_figure_regeneration_trace.md` |

- **Canonical entry:** `scripts/run_exp025_main.py` (`analysis` | `figures-main` | `figures-appendix` | `all`).
- **Analysis path:** `exp025_main_analysis.py` → `run_exp025_v3.py` (legacy file may emit **non-English** console strings).
- **Figure path:** `exp025_generate_main_figures.py` / `exp025_generate_appendix_figures.py` — **asset-bridged** only.

## 8. Missing original artifacts (not recoverable here)

- Full historical **`results/`** trees, notebooks, and one-off exports referenced in an extended upstream workspace are **not** shipped.
- **Spider SQLite** and bulk databases are **not** copied; only **minimal JSON** splits needed for specific drivers.
- **API keys / cloud execution logs** are **not** included.

## 9. Windows runtime

- Scripts printing `R²`, `✓`, `✗` require **UTF-8** stdio (`PYTHONIOENCODING=utf-8`) on Chinese Windows defaults; see `docs/WINDOWS_UTF8_RUNTIME.md` and `scripts/run_with_utf8.bat`.

## 10. Language / non-English residuals

- **Reviewer-facing English set:** `REVIEWER_START_HERE.md`, `README.md`, `QUICKSTART.md`, this file, `docs/mapping/paper_to_project_master_map.md`, `docs/mapping/PROJECT_STATUS_MATRIX.md`, `REPRODUCIBILITY.md`, `docs/reconstruction/RECOVERY_REPORT.md`, `SUBMISSION_PACKAGE_NOTE.md`, `docs/disclosures/`, `docs/gaps/`, and `docs/DATA_MOUNT_DECISIONS.md` are maintained in **English**. (Internal packaging checklists and upstream `inventory.jsonl` live **only** in the larger archival bundle, not in this submission zip.)
- **`generate_fig7_structural_failure_phase2_v32.py`:** inline comments were translated to **English** in the submission-polish pass (logic unchanged).
- **Legacy implementation scripts** copied from upstream may still contain **Simplified Chinese** (and mixed-language `print` / template strings), including but not limited to: `exp003_full_rerun.py`, `run_exp025_v3.py`, `generate_fig1_exp010_final.py`, `generate_fig2_exp001_final.py`, `generate_fig3/4/5_exp024_final.py`, `paper_aligned_reconstruction/exp003_v5_rev_final_target_matching.py`. Treat **`run_exp*_main.py` wrappers** and the English docs above as the **primary review interface**; use legacy files as **auditable implementations**, not as language templates.

## 11. What reviewers can fairly conclude

- The package **supports inspection** of the claimed mechanisms in code, **honest** partial reruns with documented inputs, and **clear separation** between live-empirical, reconstructed, simulated, and hardcoded paths.
- It **does not support** the claim that **every** number in the PDF was recomputed from raw logs inside this zip without additional data and credentials.

---

*See also: `REVIEWER_START_HERE.md`, `README.md`, `QUICKSTART.md`, `SUBMISSION_PACKAGE_NOTE.md`, `REPRODUCIBILITY.md`, `docs/reconstruction/RECOVERY_REPORT.md`, `FILE_MANIFEST.md`.*
