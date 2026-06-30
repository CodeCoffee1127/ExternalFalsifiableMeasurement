# B0_codebook/ Directory

## Description
Annotation codebook development, pilot annotation, and codebook freeze documentation.

## Directory Structure
```
B0_codebook/
├── input/                          # Input files for codebook development
│   ├── cpfc_label_definitions_from_A1.csv
│   ├── sample_checkpoint_examples.csv
│   ├── boundary_case_examples.csv
│   ├── spider_schema_context_examples/   # Subdirectory with schema examples
│   ├── annotation_pilot_cases.csv
│   └── input_manifest.json
└── output/                         # Output files from codebook development
    ├── annotation_codebook.md
    ├── annotation_label_definitions.json
    ├── annotator_instruction_sheet.md
    ├── annotation_examples.md
    ├── schema_usage_rules.md
    ├── pilot_annotation_report.md
    └── B0_summary.md
```

## Key Metrics
- Pilot N: 12 cases (3 per pattern category)
- Pilot inter-annotator onset kappa: 0.72
- Pilot inter-annotator pattern kappa: 0.68
- Codebook freeze date: 2025-02-01

## Self-Check Items (10)
1. [x] All 8 CPFC labels have complete definitions with positive/negative criteria
2. [x] Codebook frozen before full annotation begins (2025-02-01)
3. [x] Pilot annotation met kappa targets (onset: 0.72 >= 0.60, pattern: 0.68 >= 0.60)
4. [x] Annotator visible and forbidden materials clearly specified
5. [x] Schema usage rules documented with permitted/prohibited uses
6. [x] Worked examples cover all pattern categories (LVC, DMP, BAD, boundary, unverifiable)
7. [x] Boundary case handling specified with resolution protocol
8. [x] Unverifiable case handling specified with exclusion criteria
9. [x] Ambiguous case resolution protocol defined
10. [x] Pilot report documents no critical disagreements requiring major revision
