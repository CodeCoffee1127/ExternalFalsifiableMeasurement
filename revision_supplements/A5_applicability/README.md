# A5_applicability Directory

## Contents

This directory contains input files and output artifacts for the CPFC protocol applicability analysis (A5).

### Input Files
| File | Description |
|---|---|
| cpfc_protocol_definition.md | Full CPFC protocol with P1-P4 definitions |
| spider_task_mapping.csv | Spider task components mapped to P conditions |
| candidate_domain_notes.md | Notes on candidate future domains (not validated) |
| checkpoint_schema_definition.json | JSON schema for checkpoint outcomes |
| verifier_rule_inventory.csv | Complete verifier rule inventory |
| input_manifest.json | Input file manifest |

### Output Files
| File | Description |
|---|---|
| p1_p4_applicability_table.csv | P1-P4 applicability assessment for Spider |
| spider_instantiation_table.csv | Concrete Spider instantiations of P conditions |
| candidate_future_work_map.csv | Candidate domains (all flagged as non-empirical) |
| practical_workflow_summary.md | Practical workflow guide |
| non_applicable_conditions.md | When CPFC does not apply |
| A5_summary.md | Summary with Q1-Q4 answers |

## 10 Self-Check Items

1. [x] P1 (discrete_checkpointability) is marked as SATISFIED for Spider
2. [x] P2 (external_rule_availability) is marked as SATISFIED for Spider
3. [x] P3 (ordinal_categorical_reducibility) is marked as SATISFIED for Spider
4. [x] P4 (posthoc_availability) is marked as SATISFIED for Spider
5. [x] All candidate_future_work domains have not_empirical_claim_flag = True
6. [x] All candidate domains include "why_candidate_only" explaining they are not empirically validated
7. [x] Non-applicable conditions are explicitly documented
8. [x] Verifier rule inventory contains at least 10 rules
9. [x] Spider task mapping contains at least 8 task components
10. [x] A5 summary answers all 4 research questions with specific evidence
