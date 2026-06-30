# A7 Calibration Summary

## Cardinal Calibration Results

| N | Bias | |Bias| | Threshold (0.02) | Passes |
|---|------|------|-----------------|--------|
| 50 | 0.5000 | 0.5000 | **FAIL** |
| 200 | 0.3280 | 0.3280 | **FAIL** |
| 369 | ~0.25 | ~0.25 | **FAIL** |

**Conclusion**: Cardinal calibration is **not achieved** at any tested sample size. The |bias| = 0.328 at N=200 far exceeds the 0.02 threshold.

## Rank Order Calibration Results

| N | Spearman Rho | Threshold (0.90) | Passes |
|---|-------------:|-----------------|--------|
| 200 | 0.8820 | 0.90 | Marginal |
| 369 | 0.9100 | 0.90 | **PASS** |

## Differential Validity (Bias Injection)

| Bias Level | Spearman Rho | Passes (>=0.90) |
|------------|-------------:|----------------|
| 0% | 0.9900 | **PASS** |
| 10% | 0.9800 | **PASS** |
| 20% | 0.9700 | **PASS** |
| 30% | 0.9600 | **PASS** |
| 40% | 0.9650 | **PASS** |
| 50% | **0.9636** | **PASS** |

## Statistical Consistency Issues Found

1. **N>200 wording**: Manuscript says "N>200 required" but N=200 was explicitly tested. Clarify.
2. **Spearman rho=-1 with t=2.5**: Impossible combination. Correct to rho=0.882, t=5.89.
3. **Bias 0.33 vs 0.328**: Report full precision 0.3280 given 0.02 threshold.

## Ordinal Boundary Assessment

- **Kendall tau**: All splits show tau > 0.71 (strong ordinal agreement)
- **Interpretation**: The VSP ranking is ordinally stable even without cardinal calibration
- **Recommendation**: Use VSP for rank-order predictions, not absolute probability estimates

## Key Takeaways

1. The VSP does **not** achieve cardinal calibration (|bias| < 0.02) even at N=369
2. The VSP **does** achieve ordinal calibration (rank order preserved, bias-resistant)
3. Differential validity is confirmed: even 50% bias injection maintains rho >= 0.9636
4. All 3 flagged statistical inconsistencies have been documented with corrections
