# A1 Baseline Analysis

## Directory Structure
```
A1_baseline/
├── input/                          # Input data files
│   ├── dtest_case_manifest.csv     # Case-level metadata (369 cases)
│   ├── cpfc_outputs_dtest.csv      # CPFC predictions and diagnostics
│   ├── endpoint_results_dtest.csv  # Endpoint execution results
│   ├── step_verification_logs_dtest.csv  # Step-level verification
│   ├── descriptive_error_labels_dtest.csv # Error type labels
│   ├── reduced_model_outputs_dtest.csv    # Reduced baseline predictions
│   └── input_manifest.json         # Input file inventory with hashes
│
└── output/                         # Analysis results
    ├── baseline_predictions.csv    # All baseline predictions per case
    ├── baseline_metrics_onset.csv  # Onset identification metrics
    ├── baseline_metrics_pattern.csv # Pattern classification metrics
    ├── baseline_confusion_matrix_pattern.csv # Confusion matrices
    ├── baseline_bootstrap_intervals.csv # Bootstrap CIs
    ├── baseline_nonidentifiability_table.csv # Non-identifiability analysis
    ├── endpoint_heuristic_metrics.csv # Forced heuristic results
    └── A1_summary.md               # Results summary
```

## 10-Item Self-Check

1. **Case count**: 369 cases (dtest_case_0000 to dtest_case_0368) - CONFIRMED
2. **Steps per case**: t0, t1, t2 (3 steps) - CONFIRMED
3. **Endpoint correct distribution**: ~25% true, ~75% false - CONFIRMED (26.3% true)
4. **Difficulty tiers**: easy 15%, medium 35%, hard 30%, complex 20% - CONFIRMED
5. **CPFC exact onset match >= 0.60**: actual 0.630 - PASS
6. **CPFC within-one match >= 0.80**: actual 0.840 - PASS
7. **CPFC onset MAE <= 0.50**: actual 0.420 - PASS
8. **CPFC macro F1 >= 0.55**: actual 0.580 - PASS
9. **All baselines compared**: CPFC, simple_step, descriptive_error, endpoint_only, 4 heuristics - CONFIRMED
10. **Green gate criteria documented**: Both onset and pattern gates with thresholds - CONFIRMED

## Acceptance Criteria Summary

| Criterion | Threshold | Actual | Status |
|-----------|-----------|--------|--------|
| CPFC exact match | >= 0.60 | 0.630 | PASS |
| CPFC within-one | >= 0.80 | 0.840 | PASS |
| CPFC MAE | <= 0.50 | 0.420 | PASS |
| CPFC macro F1 | >= 0.55 | 0.580 | PASS |

## Key Results

- CPFC significantly outperforms all baselines on onset identification
- CPFC pattern classification exceeds green gate threshold
- All forced endpoint heuristics fail to identify onset
- Simple step baseline is closest competitor but still below CPFC
