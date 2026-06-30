# Annotator Instruction Sheet

## Document Version: 1.0 (Frozen 2025-02-01)

---

## Overview
You will be annotating text-to-SQL reasoning chains to identify:
1. The **first degradation step** (when does quality first decline?)
2. The **failure pattern category** (what type of degradation occurs?)

Your annotations will be used to validate an automated diagnostic system.

---

## ANNOTATOR VISIBLE MATERIALS

The following materials are provided for EACH case and you ARE permitted to use them:

1. **Spider Question Text**: The natural language question to be translated to SQL
2. **Database Schema**: Table names, column names, data types, primary/foreign key relationships
3. **Foreign-Key Relations**: JSON file showing table join relationships
4. **Generated Checkpoint Sequence**: The step-by-step reasoning outputs from the model (3-6 checkpoints)
5. **Checkpoint-Level Verification Evidence**: For each step, whether the output passes/fails external verification against the schema
6. **Endpoint Result** (if specified by protocol): Whether the final SQL execution succeeded or failed

---

## ANNOTATOR FORBIDDEN MATERIALS

You MUST NOT access or use the following:

| Forbidden Item | Reason |
|---------------|--------|
| CPFC onset label | Would bias your onset localization |
| CPFC pattern label | Would bias your pattern classification |
| CPFC entropy score | Diagnostic signal from the system being validated |
| CPFC rank score | Derived diagnostic metric |
| CPFC internal diagnostic category | System-internal classification |
| Ground-truth SQL | Would reveal correct answer; invalidates annotation |
| Model identity | Annotations must be model-agnostic |

**Violation of forbidden material rules will result in annotation exclusion.**

---

## Annotation Workflow

### Step 1: Understand the Question (2 minutes)
- Read the Spider question text carefully
- Identify what tables and joins are likely needed
- Note any aggregation, filtering, or grouping requirements

### Step 2: Review Schema (2 minutes)
- Examine relevant tables and columns
- Check foreign key relationships for join validity
- Do NOT try to write the correct SQL

### Step 3: Examine Checkpoints (5 minutes)
- Review each checkpoint output in sequence (t0, t1, t2, ...)
- Compare each step's output against the question requirements
- Note any verification pass/fail indicators

### Step 4: Localize Onset (3 minutes)
- Determine the FIRST step where quality declines
- Consider: semantic coherence, structural correctness, verification results
- Label: t0, t1, t2, none (no degradation), or uncertain

### Step 5: Classify Pattern (3 minutes)
- Identify the degradation pattern:
  - **Local Verification Collapse**: Single-step failure, no propagation
  - **Dependency Mediated Propagation**: Error cascades through dependencies
  - **Burst Associated Degradation**: Degradation at reasoning burst point
  - **Boundary Case**: Ambiguous between categories (flag as boundary)
  - **Unverifiable/Excluded**: Cannot determine (flag as unverifiable)

### Step 6: Rate Confidence (1 minute)
- Onset confidence: 1 (very uncertain) to 5 (very certain)
- Pattern confidence: 1 (very uncertain) to 5 (very certain)

### Step 7: Record Rationale (2 minutes)
- Write brief free-text rationale for your decisions
- Note any special considerations

---

## Quality Standards

- **Minimum annotation time**: 15 minutes per case (enforced by system)
- **Confidence threshold**: If both confidences < 3, flag as boundary_case
- **Schema usage**: You may use schema to understand semantics, NOT to reverse-engineer SQL
- **Disagreement protocol**: If you find a case genuinely ambiguous, flag it and do your best

---

## Contact

For questions about annotation procedures: cpfc-annotation-team@example.org
