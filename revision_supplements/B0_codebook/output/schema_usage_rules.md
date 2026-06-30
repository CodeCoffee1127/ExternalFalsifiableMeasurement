# Schema Usage Rules for Annotators

## Permitted Uses of Schema Information

Annotators MAY use the database schema for the following purposes:

### 1. Table Existence Verification
- **Can use schema to**: Verify whether a table referenced in a checkpoint actually exists
- **Example**: "Checkpoint mentions 'Customers' table -- schema confirms table exists"
- **Allowed**: Confirming table presence, checking table aliases

### 2. Field Existence Verification
- **Can use schema to**: Verify whether a column referenced in a checkpoint exists in the relevant table
- **Example**: "Checkpoint uses 'cust_name' -- schema shows column is 'customer_name'"
- **Allowed**: Checking column names, data types, nullability

### 3. Join Relation Validity
- **Can use schema to**: Assess whether a proposed join uses correct foreign-key relationships
- **Example**: "Checkpoint joins Orders.customer_id to Customer.id -- schema confirms FK relation"
- **Allowed**: Validating join paths, identifying FK-PK pairs

### 4. Aggregation/Filtering/Grouping Semantic Consistency
- **Can use schema to**: Check whether aggregation functions match column data types
- **Example**: "Checkpoint applies SUM() to a VARCHAR column -- semantic inconsistency"
- **Allowed**: Checking type compatibility, semantic appropriateness

---

## Prohibited Uses of Schema Information

Annotators MUST NOT use the schema for the following:

### 1. Reverse-Inferring Ground-Truth SQL
- **Forbidden**: Constructing the correct SQL query from schema and question
- **Reason**: Would provide ground-truth knowledge that invalidates the annotation
- **Example of violation**: "From the schema, I can see the correct query should be SELECT ..."

### 2. Searching Standard Answers
- **Forbidden**: Looking up the question in reference datasets to find the correct SQL
- **Reason**: Annotations must be based on checkpoint quality, not answer correctness
- **Example of violation**: "This question is Spider entry #1234; the gold SQL is ..."

### 3. Correcting Step Labels Based on Final SQL Execution
- **Forbidden**: Using endpoint execution success/failure to override checkpoint-level evidence
- **Reason**: Onset must be localized from checkpoint evidence, not inferred from endpoint
- **Example of violation**: "The final SQL failed, so t0 must be wrong even though t0 looked fine"

### 4. Viewing CPFC Output Before Annotating
- **Forbidden**: Accessing any CPFC-generated labels, scores, or diagnostics
- **Reason**: Would introduce confirmation bias
- **Example of violation**: "The CPFC system labeled this as DMP, so I should check for propagation"

---

## Decision Framework

When uncertain whether a schema use is permitted, apply this test:

> **Would this use give me information about the CORRECT answer that is NOT available from the checkpoint sequence alone?**

- If YES -> **FORBIDDEN**
- If NO -> **PERMITTED**

---

## Examples of Permitted vs Forbidden

| Scenario | Schema Use | Verdict |
|----------|-----------|---------|
| "Checkpoint joins A.id to B.id. Schema shows FK is A.id -> B.foreign_id." | Check FK validity | PERMITTED |
| "I can write the correct SQL: SELECT * FROM ..." | Reverse-inference | FORBIDDEN |
| "The COUNT() is applied to a text column." | Type consistency check | PERMITTED |
| "Let me look up this Spider question's gold query." | Answer lookup | FORBIDDEN |
| "The schema has 3 tables; checkpoint only uses 2." | Table existence | PERMITTED |

---

## Violation Reporting

Annotators who witness or suspect schema usage rule violations should report to the annotation coordinator immediately. All annotations from violating sessions will be excluded from analysis.
