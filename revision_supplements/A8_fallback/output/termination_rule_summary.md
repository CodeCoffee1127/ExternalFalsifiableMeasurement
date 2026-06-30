# Termination Rule Summary

## Overview

This document summarizes all termination conditions in the CPFC protocol state machine. Termination occurs when no further state transitions are possible or when the protocol reaches a definitive end-state.

## Terminal States

### 1. TERMINAL: Cardinal Rejected + Ordinal Only
- **Trigger**: Calibration bias exceeds threshold (0.15)
- **Final State**: cardinal_rejected_ordinal_only
- **Allowed Claims**: Ordinal population-level protocol-defined diagnostic output only
- **Forbidden Claims**: Cardinal probability, absolute uncertainty, cross-domain generalization
- **Manuscript Location**: Section 5.2
- **Action**: Restrict all claims to ordinal interpretation

### 2. TERMINAL: Non-Identifiable
- **Trigger**: Residual non-white AND simpler models better (AIC/BIC)
- **Final State**: non_identifiable
- **Allowed Claims**: Ordinal descriptive statistics only
- **Forbidden Claims**: Any model-based inference, population-level generalization
- **Manuscript Location**: Section 5.6
- **Action**: Report descriptive statistics; no model claims

### 3. TERMINAL: Unverifiable Excluded
- **Trigger**: P4 gate fails (post-hoc availability violated)
- **Final State**: unverifiable_excluded
- **Allowed Claims**: None for excluded instances
- **Forbidden Claims**: Any inference about excluded instances
- **Manuscript Location**: Section 5.8
- **Action**: Document exclusion reason; remove from analysis

### 4. TERMINAL: External Agreement Not Supported (Downgrade)
- **Trigger**: Cohen's kappa < 0.40
- **Final State**: external_agreement_not_supported
- **Allowed Claims**: Exploratory observation only
- **Forbidden Claims**: Validated diagnostic claim, externally confirmed pattern
- **Manuscript Location**: Section 6.3
- **Action**: Downgrade all claims to exploratory status

## Non-Terminal but Stable States

### 5. Stable: Retained Model Admissible
- **Condition**: Ljung-Box p > 0.05 AND not dominated AND external agreement supported
- **Stability**: Stable pending new data
- **Next Possible Transitions**: None under current data; re-evaluation required if new data arrives
- **Manuscript Location**: Section 5.4

### 6. Stable: Retained Model Provisional
- **Condition**: Marginal whiteness or near-dominated
- **Stability**: Conditionally stable; requires sensitivity analysis
- **Next Possible Transitions**: S03 (if sensitivity confirms) or S05 (if sensitivity fails)
- **Manuscript Location**: Section 5.5

## Termination Rules Summary Table

| Terminal State | Trigger | Allowed Claims | Action |
|---|---|---|---|
| cardinal_rejected_ordinal_only | calibration_bias > 0.15 | Ordinal only | Restrict claims |
| non_identifiable | residual non-white + simpler better | Descriptive only | No model claims |
| unverifiable_excluded | P4 gate fails | None (excluded) | Document exclusion |
| external_agreement_not_supported | kappa < 0.40 | Exploratory only | Downgrade claims |

## Composite Termination Logic

The final protocol state is the **conjunction** of all individual state assessments:

```
final_state = cardinal_rejected_ordinal_only 
              AND retained_model_admissible 
              AND scope_boundary (within)
              AND external_agreement_supported
```

For M8_full_retained, the composite state is:
- **calibration**: cardinal_rejected_ordinal_only (calibration_bias = 0.23 > 0.15)
- **identifiability**: retained_model_admissible (Ljung-Box p = 0.342 > 0.05, not dominated)
- **residual_whiteness**: pass (Ljung-Box p = 0.342 > 0.05)
- **external_annotation**: supported (overall kappa = 0.78 >= 0.60)
- **scope_boundary**: within_boundary (nesting_depth <= 3, verifiable)

**Final Protocol State**: retained_model_admissible + cardinal_rejected_ordinal_only

This means M8 is admissible, but all claims must be **ordinal only** due to calibration rejection.
