# EXP003: Dynamics Equation Fit Analysis

**Experiment ID**: EXP003  
**Date**: 2026-03-12  
**Status**: ✅ Complete  
**Related Tables**: Table 11, Table 13a, Table 13b

## Overview

This experiment evaluates the dynamics equation fit quality on the test set, comparing the Rescue Dynamics model against a Linear Baseline.

## Key Results

### Table 11: Fit Metrics (N=30)

| Metric | Rescue Model | Linear Baseline | Δ |
|--------|--------------|-----------------|---|
| R² | **0.945** | 0.42 | +0.525 |
| RMSE | 0.021 | 0.215 | -0.194 |
| MAE | 0.016 | 0.178 | -0.162 |
| Ljung-Box p-value | **0.258** | <0.001 | -- |
| Durbin-Watson | **1.99** | 0.87 | +1.12 |

### Interpretation

1. **R² = 0.945**: The Rescue Dynamics model explains 94.5% of variance in the test set
2. **Ljung-Box p = 0.258**: Residuals show no significant autocorrelation (p > 0.05)
3. **Durbin-Watson = 1.99**: Near-ideal independence of residuals (≈2.0)
4. **Gate Coverage**: 100% of samples fall within [0.3, 0.7] operating range

## Parameter Stability (Table 13a)

Bootstrap analysis (N=1000) confirms parameter stability:

- **β₀**: 95% CI [0.524, 0.628]
- **β₁**: 95% CI [0.379, 0.490]
- **β₂**: 95% CI [0.312, 0.427]

## Split Sensitivity (Table 13b)

Robustness check across train/test splits:

| Split | R² | RMSE | Ljung-Box p |
|-------|-----|------|-------------|
| 70/30 | 0.953 | 0.019 | 0.141 |
| 80/20 | 0.945 | 0.021 | 0.258 |

**Decision**: 80/20 split used in primary analysis (N_cal=120, N_test=30)

## Data Files

- **JSON**: `../../results/table11_fit_metrics.json`
- **CSV**: `../../results/table11_fit_metrics.csv`
- **Bootstrap CI**: `../../results/table13a_bootstrap_ci.json`
- **Split Sensitivity**: `../../results/table13b_split_sensitivity.json`
- **LaTeX Tables**: `../../tables/table_fit.tex`, `../../tables/table_sensitivity_*.tex`

## Disclosure

- Test set size is small (N=30), limiting generalizability
- Results are from a single canonical run; no multi-seed averaging
- See `SUBMISSION_DISCLOSURE.md` Section 3 for dual-chain disclosure

## References

- Paper: Section on Dynamics Equation Evaluation
- Appendix: Detailed methodology
- Code: `scripts/exp003_full_rerun.py`, `scripts/paper_aligned_reconstruction/exp003_v5_rev_final_target_matching.py`
