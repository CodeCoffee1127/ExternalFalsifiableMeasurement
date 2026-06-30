# B3 Terminology Summary

## Directory: B3_terminology/

### Input Files (5)
| File | Rows | Description |
|------|------|-------------|
| Modification_Plan_claim_boundary.csv | 7 | Claim boundaries |
| A6_claim_replacement_log.csv | 7 | Replacement log from A6 |
| B2_external_agreement_summary.csv | 8 | B2 summary metrics |
| skeleton_C.md | -- | Reference skeleton |
| input_manifest.json | -- | Input manifest |

### Output Files (6)
| File | Rows | Description |
|------|------|-------------|
| terminology_guardrails.md | -- | Master terminology document |
| allowed_claim_terms.csv | 9 | Permitted terms with conditions |
| forbidden_claim_terms.csv | 10 | Prohibited terms with replacements |
| external_agreement_wording_rules.csv | 5 | Agreement wording rules |
| ordinal_boundary_wording_rules.csv | 5 | Ordinal wording rules |
| response_letter_phrase_bank.md | -- | Phrase bank for responses |

### Content Summary

**Allowed terms (9)**: ordinal diagnostic resolution, protocol-defined failure-pattern differentiation, first-degradation-step localization, independent blinded annotation reference, statistically meaningful external agreement, within-task-family ordinal pattern stability, externally checkable checkpoints, post-hoc diagnostic protocol, population-level diagnostic summary

**Forbidden terms (10)**: absolute uncertainty, cardinal entropy, true failure mechanism, mechanism recovery, hidden causal mechanism, broad LLM reasoning validity, architecture-independent, universal evaluation instrument, external ground truth, individual-chain prediction

**External agreement rules**: 3 tiers based on kappa thresholds
**Ordinal boundary rules**: 5 conditions with allowed/forbidden wording

### Self-Check Items
- [x] All 9 allowed terms defined with required conditions
- [x] All 10 forbidden terms have replacements
- [x] External agreement rules cover 3 kappa tiers
- [x] Ordinal boundary rules cover calibration/R2/residual/entropy/onset
- [x] Response phrase bank covers external agreement, ordinal, methodology
- [x] No absolute/cardinal claims in allowed terms
- [x] All replacements preserve intended meaning
- [x] Wording rules reference specific metric thresholds
- [x] Manuscript sections specified for each rule
- [x] Phrase bank addresses common reviewer concerns
