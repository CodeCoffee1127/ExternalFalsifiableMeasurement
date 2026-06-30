# A8_fallback Directory

## Contents

This directory contains input files and output artifacts for the protocol state machine and fallback decision analysis (A8).

### Input Files
| File | Description |
|---|---|
| diagnostic_decision_rules.yaml | YAML with all diagnostic rules (CSR, RWR, MIR, EAR, SBR) |
| model_diagnostic_results_from_A2.csv | Model diagnostics (10 rows) |
| calibration_boundary_from_A7.csv | Calibration states (3 rows) |
| scope_boundary_from_A4.csv | Scope boundary states (5 rows) |
| terminology_rules_from_B3.csv | Terminology constraints (10 rows) |
| external_annotation_status_from_B2.csv | External agreement (11 rows) |
| input_manifest.json | Input file manifest |

### Output Files
| File | Description |
|---|---|
| protocol_state_machine.csv | 10-state protocol state machine |
| fallback_decision_table.csv | Decision rules for transitions |
| allowed_outputs_by_state.csv | Allowed claims per state |
| termination_rule_summary.md | Termination conditions |
| retained_model_status_record.csv | M8 final status |
| A8_summary.md | Summary with Q1-Q5 answers |

## 10 Self-Check Items

1. [x] Protocol state machine contains all 10 required states
2. [x] State triggers match specification exactly
3. [x] Fallback decision table has rules for all transitions
4. [x] Allowed outputs documented for all 10 states
5. [x] Termination conditions cover 4 terminal states
6. [x] Retained model (M8) final state = retained_model_admissible + cardinal_rejected_ordinal_only
7. [x] Allowed claim level = ordinal population-level protocol-defined diagnostic output
8. [x] All input files referenced in state machine exist
9. [x] External agreement supported (kappa = 0.78 >= 0.60)
10. [x] A8 summary answers all 5 research questions
