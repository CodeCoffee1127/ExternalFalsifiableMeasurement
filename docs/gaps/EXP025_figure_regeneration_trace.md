# EXP025 / Main Figs 10–12 / Appendix H: regeneration traceability

## Paper expectation

- Main text Section IX-E: Figs. 10–12 (complex-tier exclusion chain).
- Appendix H: additional panels (`04_appx_figA`–`07_appx_figE` in LaTeX `figures/`).

## Source-backed assets in the upstream project

- **Canonical runner (Phase 3b):** `scripts/run_exp025_v3.py` — loads Spider `dev.json`, computes AST depth, scope-crossing flags, writes under `experiment_reports/EXP025_v3/`.
- **Visualization / wording revisions:** `experiments/EXP025/scripts/exp025_visualization_revised.py` — targets `experiments/EXP025/figures/` with IEEE-style styling (not copied in this minimal bundle).

## Gap: LaTeX figure filenames

A repository-wide string search did **not** locate Python references to the exact shipped names:

- `01_main_fig10_complex_residual_by_depth.pdf`
- `02_main_fig11_stratified_residual_distribution.pdf`
- `03_main_fig12_alternative_constructs_comparison.pdf`

Therefore one or more of the following may hold:

1. Figures were exported from a notebook or tool not indexed by name in `.py` files.
2. Figures were post-processed or renamed manually to match LaTeX `\includegraphics`.
3. Intermediate numerical results exist under `experiment_reports/EXP025*` but the final **PDF pipeline** is not fully scripted in-repo.

## Recovery status (this distribution)

- **paper-backed missing (partial):** full end-to-end regeneration of **LaTeX-named** Fig. 10–12 is **not proven** from scripts alone.
- **Action taken:** this disclosure file; run `run_exp025_v3.py` and reconcile outputs to paper figures separately.
- **Appendix H:** same caveat unless a dedicated script path is later identified.

## Type judgment

- **source-backed:** audit logic for EXP025 v3 (copied).
- **paper-backed missing:** deterministic regeneration chain → exact `01_main_*` / `04_appx_*` filenames.
