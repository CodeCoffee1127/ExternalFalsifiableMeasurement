# B0 Codebook Summary

## Directory: B0_codebook/

### Input Files (5)
| File | Rows | Description |
|------|------|-------------|
| cpfc_label_definitions_from_A1.csv | 8 | Label definitions imported from A1 |
| sample_checkpoint_examples.csv | 20 | Example checkpoint sequences |
| boundary_case_examples.csv | 12 | Boundary case examples with resolution |
| spider_schema_context_examples/ | 5 files | Schema context example files |
| annotation_pilot_cases.csv | 12 | Pilot annotation cases |
| input_manifest.json | -- | Input manifest |

### Output Files (6)
| File | Description |
|------|-------------|
| annotation_codebook.md | Comprehensive annotation codebook (frozen 2025-02-01) |
| annotation_label_definitions.json | JSON label definitions with 9 labels |
| annotator_instruction_sheet.md | Annotator instructions with visible/forbidden materials |
| annotation_examples.md | 6 worked examples covering all label types |
| schema_usage_rules.md | Permitted and prohibited schema uses |
| pilot_annotation_report.md | Pilot report: 12 cases, kappa onset=0.72, pattern=0.68 |

### Key Metrics
- Pilot inter-annotator onset kappa: **0.72** (target: >=0.60)
- Pilot inter-annotator pattern kappa: **0.68** (target: >=0.60)
- Codebook revision needed: **Minor only**
- Codebook freeze date: **2025-02-01**

### Self-Check Items
- [x] All 8 labels defined with positive/negative criteria
- [x] Codebook frozen before annotation begins
- [x] Pilot kappa targets met for both onset and pattern
- [x] Annotator visible/forbidden materials clearly specified
- [x] Schema usage rules defined with examples
- [x] Worked examples cover all pattern categories
- [x] Boundary case handling specified
- [x] Unverifiable case handling specified
- [x] Ambiguous case resolution protocol defined
- [x] Pilot report documents no critical disagreements
