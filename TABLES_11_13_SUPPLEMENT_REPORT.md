# Table 11-13 Data Supplement Report

**Date**: 2026-05-01  
**Purpose**: Supplement submission package with structured data for Tables 11-13

## Summary

This report documents the addition of structured data files for Tables 11-13 from the paper "External Falsifiable Measurement for Long-Chain Reasoning: From Structural Hypothesis to Principled Degradation".

## Tables Added

### Table 11: Dynamics Equation Fit Metrics

**Source**: `tables/table_fit.tex`  
**Data Files**:
- `results/table11_fit_metrics.json` (structured JSON with metadata)
- `results/table11_fit_metrics.csv` (spreadsheet format)

**Key Findings**:
- Rescue Dynamics model achieves R² = 0.945 on test set (N=30)
- Outperforms Linear Baseline (R² = 0.42) by Δ = +0.525
- Residual diagnostics: Ljung-Box p = 0.258, Durbin-Watson = 1.99
- 100% gate coverage in [0.3, 0.7] range

**Experiment**: EXP003

---

### Table 12: Ljung-Box Test for Residual Autocorrelation

**Source**: `tables/table_ljung.tex`  
**Data Files**:
- `results/table12_ljung_box.json`
- `results/table12_ljung_box.csv`

**Key Findings**:
- All test subsets show p = 0.258 > 0.05
- Fail to reject null hypothesis: residuals are white noise
- Tier-wise analysis confirms whiteness across complexity levels

**Experiment**: EXP008

---

### Table 13a: Bootstrap 95% CI for Key Parameters

**Source**: `tables/table_sensitivity_samples.tex`  
**Data Files**:
- `results/table13a_bootstrap_ci.json`
- `results/table13a_bootstrap_ci.csv`

**Key Findings**:
- N = 1000 bootstrap resamples
- Narrow confidence intervals indicate parameter stability
- β₀: [0.524, 0.628], β₁: [0.379, 0.490], β₂: [0.312, 0.427]

**Experiment**: EXP003

---

### Table 13b: Sensitivity to Train/Test Split Ratio

**Source**: `tables/table_sensitivity_split.tex`  
**Data Files**:
- `results/table13b_split_sensitivity.json`
- `results/table13b_split_sensitivity.csv`

**Key Findings**:
- Compared 70/30 vs 80/20 splits
- 80/20 split selected for primary analysis (N_cal=120, N_test=30)
- Robust performance across splits (R²: 0.953 vs 0.945)

**Experiment**: EXP003

---

## Directory Structure

```
ExternalFalsifiableMeasurementforSubmission/
├── tables/                          [NEW]
│   ├── README.md                    [NEW] Table documentation
│   ├── table_fit.tex                [ADDED] Table 11 LaTeX
│   ├── table_ljung.tex              [ADDED] Table 12 LaTeX
│   ├── table_sensitivity_samples.tex [ADDED] Table 13a LaTeX
│   ├── table_sensitivity_split.tex  [ADDED] Table 13b LaTeX
│   ├── table_tier.tex               [ADDED] Tier analysis
│   └── table_vsp.tex                [ADDED] VSP audit
│
├── results/
│   ├── table11_fit_metrics.json     [NEW] Structured data
│   ├── table11_fit_metrics.csv      [NEW] Spreadsheet format
│   ├── table12_ljung_box.json       [NEW] Structured data
│   ├── table12_ljung_box.csv        [NEW] Spreadsheet format
│   ├── table13a_bootstrap_ci.json   [NEW] Structured data
│   ├── table13a_bootstrap_ci.csv    [NEW] Spreadsheet format
│   ├── table13b_split_sensitivity.json [NEW] Structured data
│   └── table13b_split_sensitivity.csv [NEW] Spreadsheet format
│
└── experiment_reports/
    ├── EXP003_Fit_Analysis/         [NEW]
    │   └── README.md                Detailed analysis report
    └── EXP008_LjungBox_Test/        [NEW]
        └── README.md                Detailed test report
```

## Data Integrity

### Cross-Validation

All JSON/CSV files have been cross-validated against their LaTeX sources:

✅ Table 11: All 6 metrics match `table_fit.tex`  
✅ Table 12: All 4 subsets match `table_ljung.tex`  
✅ Table 13a: All 5 parameters match `table_sensitivity_samples.tex`  
✅ Table 13b: All 5 metrics match `table_sensitivity_split.tex`

### Metadata

Each JSON file includes:
- `table_id`: Paper table identifier
- `caption`: Full table caption
- `label`: LaTeX label reference
- `source_file`: Original LaTeX file path
- `experiment`: Associated experiment ID
- `notes`: Additional context

## Usage

### For Reviewers

1. **Quick Reference**: See `tables/README.md` for table index
2. **Detailed Reports**: Check `experiment_reports/EXP003_Fit_Analysis/` and `EXP008_LjungBox_Test/`
3. **Data Files**: JSON files in `results/` for programmatic access
4. **LaTeX Sources**: Original `.tex` files in `tables/` for publication review

### For Reproducibility

```bash
# View table data in JSON
cat results/table11_fit_metrics.json | python -m json.tool

# Load in Python
import json
with open('results/table11_fit_metrics.json') as f:
    data = json.load(f)
print(data['data']['rescue_model']['R2'])  # 0.945

# Import to spreadsheet
# Open results/table11_fit_metrics.csv in Excel/Google Sheets
```

## GitHub Synchronization

To sync these files to the public repository:

```bash
# Option 1: Use the batch script (Windows)
sync_tables_to_github.bat

# Option 2: Manual git commands
git add tables/ results/table1*_*.json results/table1*_*.csv
git add experiment_reports/EXP003_Fit_Analysis/ experiment_reports/EXP008_LjungBox_Test/
git commit -m "Add Table 11-13 structured data and experiment reports"
git push origin main
```

**Repository**: https://github.com/CodeCoffee1127/ExternalFalsifiableMeasurement

## Disclosure Notes

1. **Sample Size**: Table 11 based on N=30 test samples; limited generalizability
2. **Identical p-values**: Table 12 shows p=0.258 for all tiers (conservative estimation)
3. **Bootstrap**: Table 13a uses 1000 resamples; may not capture full parameter uncertainty
4. **Single Run**: All results from canonical runs; no multi-seed averaging

See `SUBMISSION_DISCLOSURE.md` for complete disclosure statements.

## References

- Paper: Sections on Dynamics Evaluation, Residual Diagnostics, Sensitivity Analysis
- Appendices: Detailed methodology
- Code: `scripts/exp003_full_rerun.py`, Phase 4 verification pipeline

---

*Report generated: 2026-05-01*  
*Files added: 14 (6 LaTeX, 8 JSON/CSV, 2 experiment reports)*  
*Total data points: 20 metrics across 4 tables*
