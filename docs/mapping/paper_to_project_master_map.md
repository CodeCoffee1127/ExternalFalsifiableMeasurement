# Paper → project master map (canonical bundle)

**Authority order:** `paper_sources/paper1.tex` → appendices → figures → source-backed code in this bundle → paper-driven reconstruction.

**Status vocabulary:** **SB** source-backed | **PBR** paper-based reconstruction | **PAR** paper-aligned reconstruction | **SIM** simulation | **HCR** hardcoded replot | **DOC** documentation-only | **ART** artifact copy / bridge.

---

## Section I–II (Introduction, Related Work)

| Paper artifact | Claimed content | Required project artifact | Status | Bundle path | Notes |
|----------------|-----------------|---------------------------|--------|-------------|-------|
| Sec. I–II narrative | Positioning | — | DOC | `paper_sources/paper1.tex` | No separate code object |

---

## Section III — Theoretical framework (`sec:theory`)

| Paper artifact | Claimed content | Required project artifact | Status | Bundle path | Notes |
|----------------|-----------------|---------------------------|--------|-------------|-------|
| Sec. III-A | Information-theoretic foundations | Observable state math in code | SB | `code/state/state_calculator.py`, `code/state/parent_ablation.py` | Verifier-facing quantities |
| Sec. III-B CPFC | Protocol | CPFC compile / deps | SB | `code/cpfc/sql_cpfc.py`, `code/cpfc/dependency_extractor.py` | |
| Sec. III-C | Observable states | VSP / entropy helpers | SB | `code/state/*`, `code/verifier/vsp_verifier.py` | |
| Sec. III-D Eq.1 | Original dynamics | Dynamics variants | SB | `code/dynamics/dynamics_model.py`, `equation_variants.py`, `equation_v5_rev.py` | |
| **App. A Alg.1** | StepExtractor | Executable step JSON + buffer loop | **PBR** | `code/step_extractor/step_extractor.py`, `segmentation.py`, `schema.py`, `bridge_sql_pipeline.py` | Minimal StructureParse; see `README_RECONSTRUCTION.md` |
| App. A SQL subset | Predicate AST | Constraint rules | SB | `code/verifier/constraint_rules.py` | Partial alignment |

---

## Section IV — Measurement apparatus / VSP / EXP001 / EXP010 / EXP024 (`sec:vsp`)

| Paper artifact | Experiment | Status | Bundle path | Notes |
|----------------|------------|--------|-------------|-------|
| Table `tab:inference_permission` | Instrument permissioning | DOC | `paper1.tex` | |
| Table `tab:vsp` | VSP audit | HCR + SB modules | `scripts/run_exp001_main.py` → `generate_fig2_exp001_final.py`; `code/verifier/vsp_verifier.py` | Fig. 2 hardcoded panels |
| Fig `fig:differential_validity` | EXP010 | Mixed | `scripts/run_exp010_main.py`, `scripts/pipelines/run_exp010_figure_chain.py`, `generate_fig1_exp010_final.py` | Stats: SB+jsonl; Fig.1: HCR |
| Fig `fig:vsp_radar` | EXP001 | HCR | `run_exp001_main.py` | |
| Sec. IV-D `sec:exp024` Figs 3–5 | EXP024 | Mixed | `scripts/run_exp024_main.py` | `empirical` SB (heavy deps); `simulation` PAR; `figures` HCR |
| Two-tier reporting | Method | DOC | `paper1.tex`, `REPRODUCIBILITY.md` | |

---

## Section V — Synthetic pre-validation / EXP002 (`sec:synthetic`)

| Paper artifact | Experiment | Status | Bundle path | Notes |
|----------------|------------|--------|-------------|-------|
| Fig `fig:synthetic_validation` | EXP002 | HCR | `scripts/run_exp002_main.py` → `generate_fig6_synthetic_validation.py` | Embedded constants |
| Table `tab:synthetic` | I+/I− stats | HCR | same | |

---

## Section VI — Empirical falsification / structural failure (`sec:falsification`)

| Paper artifact | Experiment | Status | Bundle path | Notes |
|----------------|------------|--------|-------------|-------|
| Fig `fig:structural_failure` | Fig. 7 | SB+PBR layout | `scripts/generate_fig7_structural_failure_phase2_v32.py` | Bundle-relative `OUTPUT_DIR`; needs `brokenaxes` |
| Fig `fig:init_sensitivity` | Sensitivity | ART | `paper_sources/figures/fig_init_sensitivity.*` | Regenerate script not bundled as canonical |

---

## Section VII — Diagnostic protocol (`sec:diagnostic`)

| Paper artifact | Content | Status | Bundle path | Notes |
|----------------|---------|--------|-------------|-------|
| Table `tab:diagnostic` | Frozen rules | DOC | `paper1.tex` | |
| Fig `fig:protocol_statemachine` | State machine | ART | `paper_sources/figures` (if present) | |

---

## Section VIII — Rescue dynamics / EXP023 (`sec:rescue`)

| Paper artifact | Experiment | Status | Bundle path | Notes |
|----------------|------------|--------|-------------|-------|
| Table `tab:principled_degradation` | Degradation disclosure | Mixed | `run_exp003_main.py`, dynamics code | |
| Table `tab:exp023_comparison` | EXP023 | SB | `scripts/run_exp023_main.py` | |
| Eq rescue | Rescue spec | SB | `code/dynamics/exp003_rescue_fixed_effects.py`, `equation_v5_rev.py` | |

---

## Section IX — Supplementary audits / EXP021–022–025 (`sec:supplementary`)

| Paper artifact | Experiment | Status | Bundle path | Notes |
|----------------|------------|--------|-------------|-------|
| Table `tab:exp021` | EXP021 | SB | `scripts/run_exp021_main.py` | Optimized canonical |
| Table `tab:exp022` | EXP022 | SB | `scripts/run_exp022_main.py` | Optimized canonical |
| Table `tab:exp023` | EXP023 revisit | SB | `run_exp023_main.py` | Same driver |
| Figs 10–12 + App. H | EXP025 | **SB audit + ART (not full regen)** | `run_exp025_main.py`, `exp025_*` | **Figures:** LaTeX assets live in `paper_sources/figures/`; `exp025_generate_*_figures.py` **asset-bridges** copies into `figures/exp025*` — **not** a proof that `run_exp025_v3.py` alone rebuilds those PDFs. **Trace gap:** `docs/gaps/EXP025_figure_regeneration_trace.md`. |
| Table `tab:tier-performance` | Tier performance | DOC / partial | `paper1.tex`; `generate_top_tier_figures` not canonical in bundle | |
| Table `tab:cross-model` | EXP006 | SIM | `scripts/run_exp006_main.py` | |

---

## Section X — Conclusion (`sec:conclusion`)

| Paper artifact | Content | Status | Bundle path |
|----------------|---------|--------|-------------|
| Integrated discussion | — | DOC | `paper1.tex` |

---

## Appendices A–H (`paper_sources/appendices/`)

| Appendix | Topic | Bundle support |
|----------|--------|----------------|
| A | Theory + Algorithm 1 + protocol detail | `appendix_A.tex`; code: `code/step_extractor/*`, `code/cpfc/*`, `code/verifier/*` |
| B–H | VSP data, synthetic validation, diagnostics, rescue tables, robustness, tier boundary, complex tier | `.tex` + many tables; figure assets under `paper_sources/figures/` |

---

## Canonical runner layer (submission-facing)

| Role | Path |
|------|------|
| EXP001–006,010,021–025 main | `scripts/run_exp*_main.py` |
| EXP025 analysis + figure bridges | `scripts/exp025_main_analysis.py`, `exp025_generate_main_figures.py`, `exp025_generate_appendix_figures.py` |
| Master figures | `scripts/generate_figures_main.py` |
| EXP010 chain | `scripts/pipelines/run_exp010_figure_chain.py` |

---

*This map is the paper-driven contract for reviewers. For honesty flags see `SUBMISSION_DISCLOSURE.md` and `docs/mapping/PROJECT_STATUS_MATRIX.md`.*
