# Annotation Worked Examples

## Example 1: Local Verification Collapse (LVC)

**Case**: annot_005
**Question**: "What are the names of students who scored above 90 in Mathematics?"

### Checkpoint Sequence:
- **t0**: Identifies need for Student table and Score table. Proposes join on student_id. VERIFIED.
- **t1**: Adds filter condition "score > 90" and subject = 'Mathematics'. VERIFIED.
- **t2**: Incorrectly groups by student_name instead of selecting distinct names. VERIFICATION FAIL.
- **t3**: Final SQL has GROUP BY error but produces correct result by coincidence.

### Annotation:
- **Onset**: t2
- **Pattern**: local_verification_collapse
- **Rationale**: t2 is the first step with a verification failure. The error is isolated to t2 (GROUP BY misuse); t0 and t1 were correct. The error does not propagate because t3 happens to recover.

---

## Example 2: Dependency Mediated Propagation (DMP)

**Case**: annot_008
**Question**: "Find the average salary of employees in departments with more than 10 employees."

### Checkpoint Sequence:
- **t0**: Correctly identifies Employee and Department tables. Proposes join. VERIFIED.
- **t1**: Incorrectly joins Employee.department_id to Department.dept_id (wrong column name). VERIFICATION FAIL.
- **t2**: Uses the incorrect join to calculate averages. Propagates the wrong join condition. VERIFICATION FAIL.
- **t3**: Final SQL fails execution due to the join error.

### Annotation:
- **Onset**: t1
- **Pattern**: dependency_mediated_propagation
- **Rationale**: The t1 join error propagates through t2 and t3. Each subsequent step depends on the incorrect join, causing cascading failures. The dependency chain is clear.

---

## Example 3: Burst Associated Degradation (BAD)

**Case**: annot_011
**Question**: "List the top 3 most expensive products in each category, including category name and product count."

### Checkpoint Sequence:
- **t0**: Basic identification of Product and Category tables. VERIFIED.
- **t1-t4**: Rapid burst of reasoning -- window function proposed, then modified, then subquery added, then ranking changed. Multiple complex steps in quick succession.
- **t3** (within burst): Incorrectly uses ROW_NUMBER() instead of RANK() for top-N. VERIFICATION FAIL at t3.
- **t5**: Final SQL executes but returns wrong top-3 ordering.

### Annotation:
- **Onset**: t3
- **Pattern**: burst_associated_degradation
- **Rationale**: The degradation occurs during a reasoning burst (t1-t4). The burst complexity exceeds baseline (5 steps with complex window functions). t3's error is characteristic of burst-induced degradation.

---

## Example 4: No Degradation

**Case**: annot_003
**Question**: "How many customers are from Germany?"

### Checkpoint Sequence:
- **t0**: Identifies Customer table, country column. Proposes COUNT(*). VERIFIED.
- **t1**: Adds WHERE country = 'Germany' filter. VERIFIED.
- **t2**: Final SQL is correct. VERIFIED.

### Annotation:
- **Onset**: none
- **Pattern**: (none applicable)
- **Rationale**: All checkpoints pass verification. No semantic drift. No degradation detected.

---

## Example 5: Boundary Case

**Case**: annot_014
**Question**: "Find employees who manage departments with budgets exceeding $1M."

### Checkpoint Sequence:
- **t0**: Correct table identification. VERIFIED.
- **t1**: Proposes join Employee.manager_id = Department.manager_id. VERIFIED.
- **t2**: Adds budget filter. But also changes the join condition. Could be LVC (just the filter change) or DMP (join change propagates).

### Annotation:
- **Onset**: t2
- **Pattern**: boundary_case (between LVC and DMP)
- **Confidence**: onset=2, pattern=2
- **Rationale**: Evidence supports both LVC (single-step change) and DMP (join modification propagates). Both interpretations are defensible. Flagged as boundary.

---

## Example 6: Uncertain Onset

**Case**: annot_007
**Question**: "List all flights from JFK to LAX."

### Checkpoint Sequence:
- **t0**: Partial output (truncated). Cannot assess full quality.
- **t1**: Appears acceptable but builds on incomplete t0.
- **t2**: Final SQL fails verification. Cannot determine if root cause is t0 or t1.

### Annotation:
- **Onset**: uncertain
- **Pattern**: unverifiable_or_excluded
- **Rationale**: t0 output is truncated. Cannot reliably determine if degradation started at t0 or t1. Insufficient evidence.

---

## Summary Table

| Case ID | Onset | Pattern | Key Characteristic |
|---------|-------|---------|-------------------|
| annot_005 | t2 | LVC | Single-step failure, isolated |
| annot_008 | t1 | DMP | Cascading dependency error |
| annot_011 | t3 | BAD | Degradation during reasoning burst |
| annot_003 | none | -- | All steps acceptable |
| annot_014 | t2 | boundary | Ambiguous LVC vs DMP |
| annot_007 | uncertain | unverifiable | Insufficient evidence |
