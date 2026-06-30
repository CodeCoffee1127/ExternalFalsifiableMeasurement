# A6_claim_audit Directory

## Contents

This directory contains input files and output artifacts for the claim audit and forbidden phrase review (A6).

### Input Files
| File | Description |
|---|---|
| manuscript_original.tex | Original manuscript with forbidden phrases |
| manuscript_revised_draft.tex | Revised manuscript after replacements |
| sections/introduction.tex | Introduction section file |
| sections/methodology.tex | Methodology section file |
| sections/results.tex | Results section file |
| appendices/math_derivations.tex | Math derivations appendix |
| tables/checkpoint_breakdown.tex | Checkpoint breakdown table |
| claim_forbidden_phrases.txt | List of 11 forbidden phrases |
| claim_allowed_replacements.csv | Allowed replacements (18 rows) |
| input_manifest.json | Input file manifest |

### Output Files
| File | Description |
|---|---|
| claim_audit_hits.csv | All audit hits (44 rows) |
| claim_replacement_log.csv | Replacement log (44 rows) |
| abstract_highlights_claim_check.csv | Abstract/Highlights check (12 rows) |
| contribution_claim_check.csv | Contributions check (8 rows) |
| residual_risk_phrases.csv | Post-revision risk phrases (7 rows) |
| A6_summary.md | Summary with Q1-Q4 answers |

## 10 Self-Check Items

1. [x] All 11 forbidden phrases from claim_forbidden_phrases.txt were detected
2. [x] At least 30 audit hits generated (actual: 44)
3. [x] All audit hits have reviewer T-codes assigned
4. [x] Abstract section fully cleared of forbidden phrases
5. [x] Contributions section fully cleared of forbidden phrases
6. [x] claim_replacement_log.csv has matching row count with audit hits
7. [x] All replacements are from claim_allowed_replacements.csv
8. [x] Residual risk phrases documented (7 items)
9. [x] Risk types include forbidden, overclaim, and ambiguous
10. [x] A6 summary answers all 4 research questions
