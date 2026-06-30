# A5 Summary: CPFC Protocol Applicability Analysis

## Research Questions Answered

### Q1: Does Spider satisfy all four CPFC conditions (P1-P4)?
**Answer**: Yes. Spider satisfies all four CPFC conditions:
- **P1 (Discrete Checkpointability)**: SATISFIED - All 10 checkpoint types are discrete and independently verifiable
- **P2 (External Rule Availability)**: SATISFIED - 12 verifier rules sourced from public datasets and standards
- **P3 (Ordinal Categorical Reducibility)**: SATISFIED - Five error categories form a validated ordinal scale
- **P4 (Post-Hoc Availability)**: SATISFIED - All checkpoints evaluable on generated SQL text alone

### Q2: How does Spider instantiate each P condition concretely?
**Answer**: See `spider_instantiation_table.csv` for 16 detailed instantiations:
- P1: SQL keywords, table selection, JOIN conditions, predicates, aggregates are each discrete checkpoints
- P2: Gold queries, schema definitions, SQL-92 standard, execution results provide external rules
- P3: Error types ordered as: correct < minor_error < column_mismatch < structural_error < execution_failure
- P4: All verifiers operate on final SQL string without model access

### Q3: Which candidate domains are identified for future work, and why are they candidate-only?
**Answer**: Five candidate domains identified:
1. code_generation_with_unit_tests
2. formal_proof_fragments
3. schema_constrained_QA
4. structured_math_reasoning
5. rule_based_reasoning

All five are explicitly marked as **candidate-only** with `not_empirical_claim_flag=True`. They are NOT empirically validated in this paper because:
- No P1-P4 verification has been performed for these domains
- No ordinal validation-entropy analysis has been conducted
- No external annotator agreement data exists
- They are presented as promising directions, not empirical claims

### Q4: When does CPFC explicitly NOT apply?
**Answer**: CPFC does not apply to:
- Open-ended generation tasks (creative writing, dialogue)
- Subjective evaluation tasks (humor, aesthetics)
- Tasks requiring process-level verification
- Continuous output spaces (regression, embeddings)
- Self-referential verification scenarios
- Domains without expert-validated external rules

## Key Outputs

| Output File | Description | Rows |
|---|---|---|
| p1_p4_applicability_table.csv | Full P1-P4 applicability assessment | 4 |
| spider_instantiation_table.csv | Concrete Spider instantiations | 16 |
| candidate_future_work_map.csv | Future domain candidates (all flagged) | 5 |
| practical_workflow_summary.md | Step-by-step workflow guide | - |
| non_applicable_conditions.md | Explicit non-applicability conditions | - |
| A5_summary.md | This summary | - |

## Conclusion

Spider fully satisfies CPFC. Ordinal validation-entropy analysis is methodologically justified for Spider SQL generation tasks. All other domains are explicitly treated as candidate-only, with no empirical claims made about their CPFC status.
