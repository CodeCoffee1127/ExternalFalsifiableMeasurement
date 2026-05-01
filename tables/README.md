# Tables Directory

This directory contains LaTeX table files and structured data (JSON/CSV) for key results presented in the paper.

## Table Index

### Table 11: Dynamics Equation Fit Metrics
- **LaTeX**: `table_fit.tex`
- **JSON**: `../results/table11_fit_metrics.json`
- **CSV**: `../results/table11_fit_metrics.csv`
- **Description**: Compares Rescue Dynamics model vs Linear Baseline on test set (N=30)
- **Key Metrics**: R²=0.945, RMSE=0.021, Ljung-Box p=0.258
- **Experiment**: EXP003

### Table 12: Ljung-Box Test for Residual Autocorrelation
- **LaTeX**: `table_ljung.tex`
- **JSON**: `../results/table12_ljung_box.json`
- **CSV**: `../results/table12_ljung_box.csv`
- **Description**: Residual whiteness test across tier stratifications (lag=5)
- **Key Finding**: All subsets show p=0.258 > 0.05, indicating no significant autocorrelation
- **Experiment**: EXP008

### Table 13a: Bootstrap 95% CI for Key Parameters
- **LaTeX**: `table_sensitivity_samples.tex`
- **JSON**: `../results/table13a_bootstrap_ci.json`
- **CSV**: `../results/table13a_bootstrap_ci.csv`
- **Description**: Bootstrap confidence intervals from 1000 resamples
- **Key Finding**: Narrow intervals indicate parameter stability
- **Experiment**: EXP003

### Table 13b: Sensitivity to Train/Test Split Ratio
- **LaTeX**: `table_sensitivity_split.tex`
- **JSON**: `../results/table13b_split_sensitivity.json`
- **CSV**: `../results/table13b_split_sensitivity.csv`
- **Description**: Robustness check across 70/30 vs 80/20 split ratios
- **Key Finding**: 80/20 split used in primary analysis
- **Experiment**: EXP003

### Additional Tables

#### Table: Tier-Wise Performance Analysis
- **LaTeX**: `table_tier.tex`
- **Description**: Performance metrics stratified by complexity tier

#### Table: VSP Audit Results
- **LaTeX**: `table_vsp.tex`
- **Description**: Verifier-gated Step Protocol audit on calibration set (N=120)

## Usage

These tables are referenced in:
- `paper_sources/paper1.tex` (main paper)
- `paper_sources/appendices/` (appendices)
- `experiment_reports/` (detailed experiment reports)

## Data Format

- **JSON files**: Machine-readable format with metadata
- **CSV files**: Spreadsheet-compatible format
- **LaTeX files**: Publication-ready format

All data files include source attribution and experiment linkage.
