# CPFC Annotation Codebook v1.0

## Document Information
- **Version**: 1.0 (Frozen)
- **Freeze Date**: 2025-02-01
- **Codebook Authors**: CPFC Research Team
- **Last Revised**: 2025-01-28

---

## 1. First Degradation Step Definition

The **first degradation step** is the earliest checkpoint step (t0, t1, or t2) at which the chain's reasoning quality demonstrably declines relative to the immediately preceding step. 

### Criteria:
- **Verification failure**: The step produces output that fails external verification against the database schema or question requirements
- **Semantic drift**: The step's output departs measurably from the semantic intent of the question
- **Structural incoherence**: The step introduces a structural pattern (join, aggregation, filter) that is inconsistent with prior steps

### Degradation must be:
- **Observable**: Visible in the checkpoint output without access to ground-truth SQL
- **Persistent**: Not self-correcting in subsequent steps (unless burst-associated)
- **Categorizable**: Assignable to one of the defined pattern categories

---

## 2. Onset Localization Rules

| Step | Description | Localization Criteria |
|------|-------------|----------------------|
| **t0** | Initial reasoning step | First checkpoint shows degraded quality relative to question requirements |
| **t1** | Second reasoning step | Degradation appears at the second checkpoint; t0 was acceptable |
| **t2** | Third reasoning step | Degradation appears at third checkpoint; t0 and t1 were acceptable |
| **none** | No degradation | All checkpoints maintain acceptable quality |
| **uncertain** | Cannot determine | Insufficient evidence to localize onset |

### Decision Priority:
1. Check t0 first -- is initial reasoning already degraded?
2. If t0 acceptable, check t1
3. If t0 and t1 acceptable, check t2
4. If all steps acceptable -> label "none"
5. If evidence is contradictory or missing -> label "uncertain"

---

## 3. Pattern Categories Definition

### 3.1 Local Verification Collapse (LVC)
- **Definition**: Verification fails at a single isolated step without causing downstream propagation
- **Positive criteria**: One step fails verification; subsequent steps are acceptable or independent
- **Negative criteria**: Error visibly propagates to subsequent steps
- **Visible evidence**: Single-step verification failure, no dependency chain effects

### 3.2 Dependency Mediated Propagation (DMP)
- **Definition**: An error at one step propagates to subsequent steps through logical or structural dependencies
- **Positive criteria**: Early step error causes cascading failures in later steps; dependency chain is traceable
- **Negative criteria**: Steps are independent; error is isolated
- **Visible evidence**: Multiple consecutive degraded steps with clear dependency linkage

### 3.3 Burst Associated Degradation (BAD)
- **Definition**: Degradation coincides with a reasoning burst (multiple rapid steps or complex sub-structure)
- **Positive criteria**: Degradation occurs during or immediately after a reasoning burst; burst complexity exceeds baseline
- **Negative criteria**: Degradation occurs in simple, non-burst steps
- **Visible evidence**: Elevated step count or complexity at degradation point

### 3.4 Boundary Case
- **Definition**: Case falls at the boundary between two or more categories
- **Positive criteria**: Evidence supports multiple category assignments equally; annotator confidence < 3
- **Resolution**: Flag as boundary_case; assign best-fit category with lowest confidence

### 3.5 Unverifiable or Excluded
- **Definition**: Case cannot be reliably verified or meets exclusion criteria
- **Positive criteria**: Missing checkpoint data; schema inaccessible; question malformed
- **Action**: Exclude from primary analysis; document reason

---

## 4. Boundary Case Handling

When a case exhibits characteristics of multiple categories:
1. **Review all evidence** against each candidate category
2. **Check confidence**: If onset confidence < 3 AND pattern confidence < 3, flag as boundary
3. **Apply tie-breaking**:
   - Prefer pattern with more supporting evidence
   - Prefer pattern with earlier onset in evidence sequence
   - If still tied, mark as boundary_case and exclude from ordinary agreement calculations
4. **Document rationale** in free_text field

---

## 5. Unverifiable Case Handling

Exclusion criteria (mark as unverifiable_or_excluded):
- Missing checkpoint material
- Schema file unreadable or corrupt
- Question text is empty or non-sensical
- Fewer than 2 checkpoints available
- Endpoint result data missing AND no verification evidence available

---

## 6. Ambiguous Case Resolution

For cases labeled ambiguous_case:
1. Both annotators must independently flag ambiguity
2. If one annotator flags and the other does not, the non-flagging annotator's label takes precedence
3. Adjudication is triggered when both flag AND labels disagree
4. Default resolution: assign "uncertain" onset and exclude from pattern agreement

---

## Appendix: Annotation Workflow Summary

```
Step 1: Read question text and schema (VISIBLE evidence)
Step 2: Review checkpoint sequence
Step 3: Review verification evidence per checkpoint
Step 4: Localize first degradation step (t0/t1/t2/none/uncertain)
Step 5: Classify pattern (LVC/DMP/BAD/boundary/unverifiable)
Step 6: Rate confidence (1-5) for both onset and pattern
Step 7: Flag boundary/unverifiable/ambiguous if applicable
Step 8: Record rationale
Step 9: Submit annotation
```
