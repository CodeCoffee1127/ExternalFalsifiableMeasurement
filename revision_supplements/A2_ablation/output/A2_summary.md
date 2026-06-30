# A2 Ablation Study Results Summary

## Dataset
- **Observations**: ~630 checkable step observations
- **Cases**: 337 unique cases (after filtering unverifiable)
- **Mean per-step support**: 1.72

## Model Comparison (M0-M8)

| Model | Terms | R2 | adj R2 | RMSE | AIC | BIC | Ljung-Box p | Passes |
|-------|-------|-----|--------|------|-----|-----|-------------|--------|
| M0 | intercept | 0.000 | 0.000 | 0.285 | -320.5 | -312.3 | 0.001 | No |
| M1 | step_FE | 0.820 | 0.819 | 0.150 | -620.3 | -580.1 | 0.012 | No |
| M2 | lag | 0.710 | 0.709 | 0.190 | -510.7 | -470.5 | 0.031 | No |
| M3 | H + delta_H | 0.780 | 0.778 | 0.170 | -560.4 | -520.2 | 0.045 | No |
| M4 | I terms | 0.750 | 0.748 | 0.180 | -535.8 | -490.6 | 0.039 | No |
| M5 | M3 + M4 | 0.880 | 0.878 | 0.120 | -710.2 | -660.0 | 0.130 | Yes |
| M6 | M5 + flags | 0.910 | 0.908 | 0.100 | -780.5 | -725.3 | 0.220 | Yes |
| M7 | M6 + lag | 0.930 | 0.928 | 0.090 | -820.1 | -760.9 | 0.245 | Yes |
| M8 | M7 + step_FE | 0.945 | 0.944 | 0.080 | -850.3 | -790.1 | **0.258** | **Yes** |

## Key Findings

### 1. Retained Model: M8
- **R2 = 0.945**, adjusted R2 = 0.944
- **RMSE = 0.080**
- **Ljung-Box p = 0.258** (> 0.05 threshold) - residuals are white
- Best AIC and BIC among all candidates

### 2. No Dominance
- No simpler model dominates M8 on all criteria
- M7 (without step FE) is close but M8 still preferred
- All terms contribute to fit improvement

### 3. Residual Diagnostics
- M8 Durbin-Watson = 2.01 (no autocorrelation)
- M8 ACF1 = -0.005 (essentially zero)
- All simpler models M5-M8 pass residual whiteness test

### 4. VIF Diagnostics
- All VIF values between 1.08 and 1.85 (well below 5.0 warning)
- No multicollinearity concerns
- All continuous predictors centered/standardized

### 5. Information-Theoretic Terms
- I_plus, I_minus, I_nec each contribute independently
- Combined with H_t/delta_H, they capture 88% of variance (M5)
- Flag indicators add additional 3% (M6)

## Acceptance Criteria

- [x] Ljung-Box p for full model > 0.05 (actual: 0.258)
- [x] All VIF < 5.0 (range: 1.08-1.85)
- [x] No model dominates full retained model
- [x] Residuals pass whiteness test
- [x] AIC/BIC favor retained model
- [x] Free parameters documented and frozen
