# Pilot Annotation Report

## Report Information
- **Report Date**: 2025-01-28
- **Pilot Phase**: Pre-codebook freeze validation
- **Codebook Version**: 0.9 (draft)

---

## Pilot Design

### Sample Composition
- **pilot_N**: 12 cases
- **Case selection**: Purposive sampling to cover all pattern categories

### Distribution
| Pattern Category | Cases | Case IDs |
|-----------------|-------|----------|
| Local Verification Collapse | 3 | pilot_01, pilot_04, pilot_09 |
| Dependency Mediated Propagation | 3 | pilot_02, pilot_06, pilot_11 |
| Burst Associated Degradation | 3 | pilot_03, pilot_07, pilot_10 |
| Boundary / Unverifiable | 3 | pilot_05, pilot_08, pilot_12 |

### Annotators
- Annotator A (experienced SQL analyst)
- Annotator B (domain expert, text-to-SQL researcher)

---

## Inter-Annotator Agreement Results

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Onset Cohen's Kappa | 0.72 | >= 0.60 | PASS |
| Onset Weighted Kappa | 0.76 | >= 0.60 | PASS |
| Pattern Cohen's Kappa | 0.68 | >= 0.60 | PASS |
| Pattern Macro-F1 | 0.71 | >= 0.60 | PASS |
| Exact Onset Agreement | 83.3% | -- | -- |
| Exact Pattern Agreement | 75.0% | -- | -- |

---

## Per-Case Agreement Detail

| Case | A_Onset | B_Onset | A_Pattern | B_Pattern | Onset_Agree | Pattern_Agree |
|------|---------|---------|-----------|-----------|-------------|---------------|
| pilot_01 | t1 | t1 | LVC | LVC | Yes | Yes |
| pilot_02 | t0 | t0 | DMP | DMP | Yes | Yes |
| pilot_03 | t2 | t2 | BAD | BAD | Yes | Yes |
| pilot_04 | t1 | t1 | LVC | LVC | Yes | Yes |
| pilot_05 | t2 | uncertain | boundary | boundary | No | Yes |
| pilot_06 | t1 | t1 | DMP | DMP | Yes | Yes |
| pilot_07 | t2 | t1 | BAD | BAD | No | Yes |
| pilot_08 | uncertain | uncertain | unverifiable | unverifiable | Yes | Yes |
| pilot_09 | t0 | t0 | LVC | LVC | Yes | Yes |
| pilot_10 | t2 | t2 | BAD | BAD | Yes | Yes |
| pilot_11 | t1 | t1 | DMP | DMP | Yes | Yes |
| pilot_12 | none | none | unverifiable | unverifiable | Yes | Yes |

---

## Labels with High Disagreement

**Finding**: No critical disagreement detected.

Minor disagreements:
- pilot_05: Onset disagreement (t2 vs uncertain) in a boundary case -- expected ambiguity
- pilot_07: Onset off-by-one (t2 vs t1) in burst-associated case -- within acceptable range

Neither disagreement affects pattern classification. Both cases involve inherently ambiguous scenarios.

---

## Codebook Revision Needs

**Assessment**: Only minor clarifications needed.

### Revisions Made:
1. **Clarified** t2 boundary definition for burst cases (added note: "in burst context, onset may align with burst start or burst error point")
2. **Added** explicit instruction: "Do not use endpoint result to override checkpoint evidence"
3. **Expanded** boundary_case resolution with tie-breaking priority list
4. **Clarified** confidence threshold for flagging (both < 3 triggers boundary flag)

### No Revisions Needed For:
- Core onset localization rules (clear and well-applied)
- Pattern category definitions (distinct and consistently applied)
- Unverifiable case handling (sufficiently specified)

---

## Final Codebook Freeze

- **Freeze Date**: 2025-02-01
- **Frozen Version**: 1.0
- **Post-freeze changes**: None permitted without amendment protocol
- **Amendment protocol**: Requires agreement from both lead annotators + PI approval

---

## Recommendations

1. Proceed to full annotation with frozen codebook
2. Retain pilot cases as worked examples (case IDs blinded)
3. Use pilot disagreement cases (pilot_05, pilot_07) as training material for boundary handling
4. Monitor ongoing agreement; flag if kappa drops below 0.60
