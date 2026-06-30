# Terminology Guardrails

## Version: 1.0
## Date: 2025-02-15
## Purpose: Ensure all claims about CPFC capabilities use appropriately calibrated terminology

---

## 1. Core Principle

**Always prefer ordinal/relative/diagnostic language over absolute/cardinal/truth language.**

The CPFC system provides diagnostic indicators, not truth-revealing measurements.

---

## 2. Allowed Claim Terms

| Term | Allowed Context | Required Condition | Example |
|------|----------------|-------------------|---------|
| ordinal diagnostic resolution | Describing onset localization | Kappa >= 0.60 demonstrated | "CPFC achieves ordinal diagnostic resolution with kappa=0.67" |
| protocol-defined failure-pattern differentiation | Pattern classification | Inter-annotator kappa >= 0.60 | "The protocol defines failure-pattern differentiation categories" |
| first-degradation-step localization | Onset identification | External agreement >= 0.60 exact | "First-degradation-step localization agrees with annotators at 74%" |
| independent blinded annotation reference | External validation | Blinding protocol documented | "Annotations were collected against an independent blinded annotation reference" |
| statistically meaningful external agreement | Agreement claim | Kappa >= 0.60 AND CPFC kappa >= 0.60 | "Statistically meaningful external agreement was achieved" |
| within-task-family ordinal pattern stability | Stability claims | R2 reported with caveats | "Within-task-family ordinal pattern stability observed" |
| externally checkable checkpoints | Verification method | Verification logs available | "The system uses externally checkable checkpoints" |
| post-hoc diagnostic protocol | Methodology | Protocol documented in B0 | "A post-hoc diagnostic protocol was applied" |
| population-level diagnostic summary | Results scope | Sample statistics reported | "Results represent a population-level diagnostic summary" |

---

## 3. Forbidden Claim Terms

| Term | Risk Type | Forbidden Context | Replacement |
|------|-----------|-------------------|-------------|
| absolute uncertainty | Cardinal overclaim | Any quantitative claim | ordinal diagnostic resolution |
| cardinal entropy | Cardinal overclaim | Entropy interpretation | rank-order diagnostic indicator |
| true failure mechanism | Truth claim | Pattern labels | protocol-defined failure-pattern differentiation |
| mechanism recovery | Causal overclaim | Results interpretation | pattern characterization |
| hidden causal mechanism | Causal claim | Methodology description | post-hoc diagnostic protocol |
| broad LLM reasoning validity | Generalization overclaim | Scope claims | within-task-family assessment |
| architecture-independent | Generalization overclaim | Model claims | model-specific with caveats |
| universal evaluation instrument | Universality claim | Evaluation claims | task-family-specific evaluation |
| external ground truth | Truth claim | Reference labels | independent blinded annotation reference |
| individual-chain prediction | Scope overclaim | Per-case claims | population-level diagnostic summary |

---

## 4. External Agreement Wording Rules

| Metric Condition | Allowed Wording | Forbidden Wording | Required Caveat |
|-----------------|----------------|-------------------|----------------|
| Kappa >= 0.60 AND CPFC kappa >= 0.60 | "statistically meaningful external agreement" | "external ground truth", "true labels" | "Annotation-based reference, not ground truth" |
| 0.40 <= Kappa < 0.60 | "partial external agreement" | "strong external validation" | "Moderate agreement; interpretation limited" |
| Kappa < 0.40 | "provisional labels pending further validation" | Any external agreement claim | "Insufficient agreement for validation claims" |

---

## 5. Ordinal Boundary Wording Rules

| Condition | Allowed Wording | Forbidden Wording | Manuscript Sections |
|-----------|----------------|-------------------|-------------------|
| Calibration failure | ordinal/rank-order/relative diagnostic quantity | absolute/cardinal/physical uncertainty | Methods, Results |
| Residual whiteness pass | population-level ordinal summary | individual-chain prediction | Results, Discussion |
| R2 reported | fit summary / model behavior summary | diagnostic power / mechanism recovery | Results, Discussion |

---

## 6. Consequence of Violation

Terminology violations in manuscript drafts will be flagged during internal review.
Repeated violations require revision before submission.

---

## 7. Review Authority

Terminology guardrails enforced by: senior_author + methodology_advisor
Appeals process: documented in project governance
