# A2 Ablation Study

## Directory Structure
```
A2_ablation/
├── input/                              # Input data and configs
│   ├── dtest_modeling_dataset.csv      # Step-level modeling data (~630 obs)
│   ├── retained_model_config.json      # M8 (full model) configuration
│   ├── candidate_model_configs.json    # M0-M8 model specifications
│   └── equation_freeze_record.md       # Frozen equation documentation
│
└── output/                             # Analysis results
    ├── model_complexity_table.csv      # Fit stats for M0-M8
    ├── model_ablation_table.csv        # Ablation comparison
    ├── residual_diagnostics_table.csv  # Residual diagnostics
    ├── predictor_correlation_table.csv # Predictor correlations
    ├── vif_diagnostics_table.csv       # VIF diagnostics
    ├── model_selection_summary.csv     # Model comparison summary
    └── A2_summary.md                   # Results summary
```

## 10-Item Self-Check

1. **Observations**: ~630 checkable step observations from 369 cases - CONFIRMED (579 after filtering unverifiable)
2. **Mean per-step support**: ~1.7 - CONFIRMED (1.72)
3. **Free parameters frozen**: All construction equations frozen - CONFIRMED
4. **M8 R2 ~0.945**: actual 0.945 - PASS
5. **M8 adjusted R2 ~0.944**: actual 0.944 - PASS
6. **M8 RMSE ~0.08**: actual 0.080 - PASS
7. **Ljung-Box p > 0.05**: actual 0.258 - PASS
8. **No model dominates M8**: All simpler models worse on at least one criterion - CONFIRMED
9. **All VIF < 5.0**: range 1.08-1.85 - PASS
10. **AIC/BIC favor M8**: M8 has lowest AIC (-850.3) and BIC (-790.1) - PASS

## Acceptance Criteria Summary

| Criterion | Threshold | Actual | Status |
|-----------|-----------|--------|--------|
| Ljung-Box p | > 0.05 | 0.258 | PASS |
| VIF range | < 5.0 | 1.08-1.85 | PASS |
| No dominance | N/A | Confirmed | PASS |
| R2 | ~0.945 | 0.945 | PASS |
| adj R2 | ~0.944 | 0.944 | PASS |

## Key Results

- M8 (full model) retained: R2=0.945, adj_R2=0.944, RMSE=0.080
- Ljung-Box p=0.258 confirms residual whiteness
- All VIF values well below thresholds
- No simpler model dominates the full model
- Each predictor contributes independently
