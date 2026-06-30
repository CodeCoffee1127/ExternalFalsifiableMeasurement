# A8 Summary: Protocol State Machine and Fallback Decisions

## Research Questions Answered

### Q1: What are the 10 protocol states, and what triggers each transition?
**Answer**: The protocol state machine defines 10 states:

1. **cardinal_rejected_ordinal_only**: Triggered when calibration bias > 0.15 threshold
2. **original_specification_rejected**: Triggered when held-out R² < 0
3. **retained_model_admissible**: Triggered when Ljung-Box p > 0.05 AND not AIC/BIC dominated
4. **retained_model_provisional**: Triggered when marginal whiteness (0.01 < p <= 0.05) OR near-dominated
5. **non_identifiable**: Triggered when residual non-white AND simpler models better
6. **scope_boundary**: Triggered when deep nesting (>3 levels) OR unverifiable elements
7. **unverifiable_excluded**: Triggered when P4 gate (post-hoc availability) fails
8. **external_agreement_supported**: Triggered when Cohen's kappa >= 0.60
9. **external_agreement_partial**: Triggered when 0.40 <= kappa < 0.60
10. **external_agreement_not_supported**: Triggered when kappa < 0.40

All 10 states are fully documented in `protocol_state_machine.csv` with trigger conditions, diagnostic inputs, allowed outputs, forbidden interpretations, next states, and manuscript locations.

### Q2: What are the fallback decision rules for each state transition?
**Answer**: 14 fallback decision rules documented in `fallback_decision_table.csv`:

Key fallback paths:
- **Calibration rejected** → restrict all claims to ordinal only
- **Specification rejected** → fall back to descriptive statistics; no model claims
- **Non-identifiable** → no model-based inference permitted
- **Scope boundary** → exclude instance; document reason
- **External not supported** → downgrade all claims to exploratory
- **External supported** → confirm validation; maintain ordinal-only caveat

Each rule specifies: current state, trigger, whether condition is met, next state, fallback action, allowed claim change, and sensitivity analysis requirement.

### Q3: What outputs are allowed in each state?
**Answer**: `allowed_outputs_by_state.csv` documents allowed outputs for all 10 states:

| State | Allowed Claim Level |
|---|---|
| cardinal_rejected_ordinal_only | ordinal population-level protocol-defined diagnostic output |
| original_specification_rejected | no model claim |
| retained_model_admissible | ordinal population-level + within-protocol comparison |
| retained_model_provisional | provisional ordinal with explicit caveat |
| non_identifiable | ordinal descriptive statistics only |
| scope_boundary | exclusion noted |
| unverifiable_excluded | none |
| external_agreement_supported | ordinal + external validation |
| external_agreement_partial | exploratory observation only |
| external_agreement_not_supported | exploratory observation only |

All states require specific caveats as documented.

### Q4: What are the termination conditions?
**Answer**: 4 terminal states defined in `termination_rule_summary.md`:

1. **cardinal_rejected_ordinal_only**: Restrict claims to ordinal interpretation
2. **non_identifiable**: Report descriptive statistics only; no model claims
3. **unverifiable_excluded**: Document exclusion; remove from analysis
4. **external_agreement_not_supported**: Downgrade all claims to exploratory

Two stable non-terminal states:
- **retained_model_admissible**: Stable pending new data
- **retained_model_provisional**: Stable with sensitivity analysis requirement

### Q5: What is the final protocol state for the retained model (M8)?
**Answer**: The final protocol state for M8_full_retained is:

**retained_model_admissible + cardinal_rejected_ordinal_only**

This composite state means:
- ✅ **Identifiability**: M8 is admissible (Ljung-Box p = 0.342 > 0.05, not AIC/BIC dominated)
- ✅ **Residual whiteness**: Pass (Ljung-Box p = 0.342)
- ✅ **External agreement**: Supported (overall kappa = 0.78 >= 0.60)
- ✅ **Scope boundary**: Within boundary (verifiable, nesting depth <= 3)
- ❌ **Calibration**: Cardinal interpretation REJECTED (calibration_bias = 0.23 > 0.15)

**Allowed claim level**: ordinal population-level protocol-defined diagnostic output

**Critical implication**: M8 can be used for ordinal population-level diagnostics, but all claims must be explicitly ordinal. Cardinal probability statements, absolute uncertainty quantification, and cross-domain generalization are forbidden.

## Key Outputs

| Output File | Description | Rows |
|---|---|---|
| protocol_state_machine.csv | 10-state protocol state machine | 10 |
| fallback_decision_table.csv | Decision rules for state transitions | 14 |
| allowed_outputs_by_state.csv | Allowed claims per state | 10 |
| termination_rule_summary.md | All termination conditions | - |
| retained_model_status_record.csv | M8 final status | 1 |
| A8_summary.md | This summary | - |

## Conclusion

The protocol state machine provides a rigorous decision framework for determining what claims are justified given diagnostic evidence. For M8, the final state permits ordinal population-level protocol-defined diagnostic output while explicitly forbidding cardinal interpretation due to calibration rejection. This ensures all manuscript claims are methodologically grounded and defensible.
