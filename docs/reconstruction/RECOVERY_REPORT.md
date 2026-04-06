# RECOVERY_REPORT.md

Honest accounting of **paper requirements** (`paper_sources/paper1.tex`) vs **bundle artifacts**. This file doubles as a **reconstruction decision log**: what was missing in the original archive, what was rebuilt (PBR/PAR), and what remains unrecoverable.  
Read-only upstream trees were **not** modified; full archival reconstruction work lives under `D:\ExternalFalsifiableMeasurementforLongChain`. **This copy** is placed at `docs/reconstruction/RECOVERY_REPORT.md` in the **reviewer submission** zip for transparency (the submission tree is a trimmed export).

---

## Summary table (high-priority items)

| ID | Paper requirement | Source status | Judgment | Evidence used | Recovery action | Code / doc / placeholder | Residual limitation |
|----|-------------------|---------------|----------|---------------|-----------------|---------------------------|---------------------|
| **C02** | Appendix A Algorithm 1 StepExtractor | Implicit LLM clause path + **PBR executable** buffer loop | **mixed**: SB empirical path + **PBR** minimal Algorithm-1-shaped code | Paper-driven phase | Add `VerifierDrivenStepExtractor`, `structure_parse`, `StepObject`, SQL bridge | `code/step_extractor/step_extractor.py`, `segmentation.py`, `schema.py`, `bridge_sql_pipeline.py`, `README_RECONSTRUCTION.md` | **Not** claimed equal to lost production; StructureParse is heuristic |
| **EXP003** | Rescue dynamics + reported test statistics | `exp003_rescue_fixed_effects.py` + runners vs `exp003_v5_rev` synthesis | **source-backed** + **paper-aligned side chain** | Script docstrings | Copy **both** chains; label roles | `code/dynamics/*`, `scripts/exp003_full_rerun.py`, `scripts/paper_aligned_reconstruction/exp003_v5_rev_final_target_matching.py` | v5_rev file matches **published numbers** by construction, not a substitute for empirical rerun |
| **EXP010** | Differential validity + Fig. 1 | `exp010_vsp_calibration_corrected.py` vs hardcoded fig scripts | **mixed**: with mounted `data/results/exp003_v5_rev_final/exp003_full_results.jsonl` + UTF-8, **stats path uses real H_v**; fig still **hardcoded** unless recomputed | Phase 4.6 mount + run | Copy one canonical `jsonl`; UTF-8 doc | `scripts/exp010_vsp_calibration_corrected.py`, `scripts/generate_fig1_exp010_final.py`, `docs/DATA_MOUNT_DECISIONS.md` | Fig 1 script still **embeds paper table**; `jsonl` is **paper-aligned upstream artifact**, not proof of live verifier pipeline |
| **EXP024** | Cardinality convergence + Fig. 3–5 | `exp024_real_data_experiment.py` vs simulation + hardcoded figs | **mixed** | Read `exp024_gold_standard_expansion_final.py`, `generate_fig3_*` | Copy real + sim + fig scripts; disclose | `scripts/exp024_*.py`, `scripts/generate_fig3/4/5_exp024_final.py` | Publication curves partly **hardcoded**; simulation runner forces monotonic bias per docstring |
| **EXP025** | Fig. 10–12 + App. H chain | `run_exp025_v3.py` + **artifact bridge** | **mixed**: SB audit + **ART** copy from `paper_sources/figures` | Paper-driven phase | `run_exp025_main.py`, `exp025_generate_*_figures.py` | Full Python regeneration still not proven; reviewers get unified paths under `figures/exp025*` |
| **C27 / EXP006** | Cross-model generalization table | `exp006_cross_model.py` uses **noise simulation** | **paper-backed missing** (true multi-API rerun) | Read `simulate_model_results` in script | Disclosure doc + copy script as-is | `scripts/exp006_cross_model.py`, `docs/disclosures/EXP006_simulation.md` | Not GPT-4 / Claude-3 online replication |
| **Fig. 7** (`fig7_structural_failure`) | Main text figure | Upstream `phase2_figures_v32.py` | **source-backed** (bundle-relative output) | LaTeX `\includegraphics{fig7_structural_failure}` | Copy as `scripts/generate_fig7_structural_failure_phase2_v32.py`; fix `OUTPUT_DIR` | script | May retain non-English inline comments; requires `brokenaxes` |
| **Fig. 2 / EXP001** | VSP radar | `generate_fig2_exp001_final.py` | **hardcoded replot** (class per Phase 3b pattern) | Filename anchor | Batch-2 copy | `scripts/generate_fig2_exp001_final.py` | Verify against `paper_sources/figures/fig2_*` |
| **EXP021 / EXP022** | Risk memory / tier recalibration | `*_optimized.py` drivers | **source-backed** | Two variants upstream; **canonical = optimized** | Batch-2 copy | `scripts/exp021_risk_memory_validation_optimized.py`, `scripts/exp022_semantic_tier_recalibration_optimized.py` | Non-English docstrings possible in upstream copy |
| **EXP023** | Gate vs step FE | `exp023_gate_vs_stepfe.py` | **source-backed** | Script header | Batch-2 copy | `scripts/exp023_gate_vs_stepfe.py` | May require data paths not mounted |

---

## Forced disclosures (also in REPRODUCIBILITY.md)

1. **C02:** Formal StepExtractor ≠ implicit SQL-clause LLM chain.
2. **EXP003:** `paper_aligned_reconstruction/exp003_v5_rev_final_target_matching.py` is **paper-aligned reconstruction**, not the empirical main chain (`docs/disclosures/EXP003_dual_chain.md`).
3. **EXP006:** **Simulation-based** cross-model table, not native third-party API runs (`docs/disclosures/EXP006_simulation.md`).
4. **Several figure scripts:** **Hardcoded paper values** for LaTeX export; not full recomputation from raw verifier logs.
5. **EXP025:** **Incomplete trace** from code to `01_main_fig10_*` / Appendix H filenames — see `docs/gaps/EXP025_figure_regeneration_trace.md`.

---

## Phase 4.6 (minimal data mount + UTF-8)

- **Mounted (read-only copy into bundle only):** `spider/dev.json`, `spider/train_spider.json`, `data/test/test.json` (fallback), `data/results/exp003_v5_rev_final/exp003_full_results.jsonl` (single canonical copy; rationale in `docs/DATA_MOUNT_DECISIONS.md`).
- **UTF-8:** `docs/WINDOWS_UTF8_RUNTIME.md`, `scripts/run_with_utf8.bat`.
- **EXP003 `exp003_full_rerun.py`:** With Spider JSON, loads **8,034** rows, stratified sample **369**, generates **1,885** trajectory rows via **in-script synthesis** (`generate_experiment_data`), **not** live LLM+DB verifier. Smoke run produced **negative R²** (~−0.62) vs paper **0.945** — **do not** conflate with publication table.
- **EXP025 v3:** No `FileNotFoundError`; may stop at **Layer 1** preregistered FAIL; still writes under `experiment_reports/EXP025_v3/`.
- **EXP010 corrected:** With mount + `PYTHONIOENCODING=utf-8`, **completed** using **real** loaded H_v from `jsonl` (ρ@50% ≈ 0.9629 in test run); disclosure: input is **v5_rev_final** pipeline artifact.
- **EXP006:** Unchanged **simulation** semantics; completes under UTF-8.

---

## Submission polish (reviewer-facing)

- **`REVIEWER_START_HERE.md`**, **`SUBMISSION_PACKAGE_NOTE.md`:** shortest path + submission-zip provenance (packaging hygiene checklists stay in the **archival** bundle only).
- **EXP025 figures:** explicitly **asset-bridged** for main Figs 10–12 and Appendix H panels (copies from `paper_sources/figures/`), **not** claimed as a single-code-path regeneration; trace gap cross-linked in `SUBMISSION_DISCLOSURE.md` §7 and `QUICKSTART.md` §5.

## Paper-driven full reconstruction phase

- **`docs/mapping/paper_to_project_master_map.md`:** section/figure/experiment → bundle path (English contract).
- **`docs/mapping/PROJECT_STATUS_MATRIX.md`:** support level per artifact (R / HCR / PBR / ART / …).
- **Canonical runners:** `scripts/run_exp001_main.py` … `run_exp025_main.py`; `generate_figures_main.py`; `scripts/pipelines/run_exp010_figure_chain.py`.
- **StepExtractor PBR:** new modules under `code/step_extractor/` (see table row C02).
- **EXP025 figure completeness:** `exp025_generate_main_figures.py` / `exp025_generate_appendix_figures.py` synchronize shipped LaTeX assets into `figures/` for a **non-fragmented** reviewer tree.

---

## Finalization phase (submission packaging)

- **Second script batch:** Fig. 2 driver, Fig. 6 synthetic validation, EXP023, EXP021/EXP022 **optimized** canonicals, Fig. 7 structural failure generator (`phase2_figures_v32` copy with bundle-relative output). Selection rationale for Fig. 7: LaTeX references `figures/fig7_structural_failure`; upstream `phase2_figures_v32.py` calls `save_figure(..., 'fig7_structural_failure')`. Alternative scripts emit `fig7_tier_wise` (different asset).
- **Documentation:** English-only reviewer set: `README.md`, `QUICKSTART.md`, `SUBMISSION_DISCLOSURE.md`; disclosures relocated under `docs/disclosures/` and `docs/gaps/`.
- **Run evidence:** `results/README_RUN_EVIDENCE.md` explains minimal JSON/JSONL artifacts; no claim of full historical `results/` recovery.

---

## What was missing vs what was reconstructed vs what stays unrecoverable

| Category | Status |
|----------|--------|
| Full original `results/` + notebooks | **Unrecoverable** in this bundle — disclose; do not fabricate. |
| StepExtractor Algorithm 1 | **Missing** — **disclosed** + neutral adapter only. |
| EXP003 published table via empirical rerun alone | **Not guaranteed** — dual chain; paper-aligned script separate. |
| EXP006 multi-API | **Missing** — simulation only. |
| EXP025 → exact main/apx figure PDF pipeline | **Partially missing** — runner + gap doc. |
| Minimal Spider + one `jsonl` | **Reconstructed** via read-only copy — see `docs/DATA_MOUNT_DECISIONS.md`. |

---

*End of RECOVERY_REPORT (through finalization).*
