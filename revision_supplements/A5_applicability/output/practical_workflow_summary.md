# Practical Workflow Summary for CPFC Protocol Application

## Step 1: Task Decomposition
Decompose the target task into candidate checkpoint components. Each component should represent a discrete, independently assessable aspect of the task output.

**For Spider**: Decomposed into 10 checkpoint types: keyword correctness, table selection, JOIN conditions, WHERE predicates, aggregate functions, column selection, execution equivalence, schema linking, nesting depth, and syntax validity.

## Step 2: P1 Verification (Discrete Checkpointability)
Check that each checkpoint type has an unambiguous binary or categorical outcome.

**Tool**: Automated verifiers using string comparison, set equality, schema lookup, and parser validation.

**Result**: PASS - All 10 Spider checkpoint types have clear categorical outcomes.

## Step 3: P2 Verification (External Rule Availability)
Confirm that publicly available rule sets exist for each checkpoint type.

**Tool**: Spider gold queries, schema definitions, SQL-92 standard, foreign key constraints.

**Result**: PASS - 12 verifier rules documented, all sourced from external public datasets.

## Step 4: P3 Verification (Ordinal Categorical Reducibility)
Order failure types along a meaningful severity gradient.

**Tool**: Expert annotator validation of error type ordering.

**Result**: PASS - Five ordered categories validated: correct < minor_error < column_mismatch < structural_error < execution_failure.

## Step 5: P4 Verification (Post-Hoc Availability)
Confirm all checkpoints can be evaluated on generated output alone.

**Tool**: Verification pipeline operating on SQL text only.

**Result**: PASS - No model internal access required for any checkpoint type.

## Step 6: Protocol Eligibility Determination
If all P1-P4 are satisfied, the task is eligible for ordinal validation-entropy analysis.

**Final Result**: Spider satisfies CPFC. Ordinal validation-entropy analysis is methodologically justified.

## Practical Recommendations

1. **Document all verifier rules** in a machine-readable inventory
2. **Validate error type ordering** with multiple expert annotators
3. **Automate as much as possible** to reduce subjective judgment
4. **Version-control checkpoint schema** definitions for reproducibility
5. **Flag candidate-only domains** explicitly; never conflate with validated results
