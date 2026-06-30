# B2_external_agreement/ Directory

## Description
External agreement analysis between CPFC labels and independent annotator references.

## Directory Structure
```
B2_external_agreement/
├── input/                          # Input files for agreement analysis
│   ├── annotation_codebook.md
│   ├── blinded_sample_pool.csv
│   ├── annotation_materials_manifest.csv
│   ├── annotator_A_raw.csv
│   ├── annotator_B_raw.csv
│   ├── cpfc_labels_unblinded_after_annotation.csv
│   ├── adjudication_optional.csv
│   └── input_manifest.json
└── output/                         # Output files from agreement analysis
    ├── inter_annotator_agreement.csv
    ├── cpfc_vs_external_reference_agreement.csv
    ├── onset_agreement_metrics.csv
    ├── pattern_agreement_metrics.csv
    ├── pattern_confusion_matrix.csv
    ├── disagreement_analysis.md
    ├── annotation_freeze_record.md
    └── B2_summary.md
```

## Key Metrics
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Inter-annotator onset kappa | 0.69 | >=0.60 | PASS |
| Inter-annotator pattern kappa | 0.65 | >=0.60 | PASS |
| CPFC exact onset | 0.74 | >=0.60 | PASS |
| CPFC within-one-step | 0.99 | >=0.80 | PASS |
| CPFC onset MAE | 0.27 | <=0.50 | PASS |
| CPFC onset kappa | 0.65 | >=0.60 | PASS |
| CPFC pattern kappa | 0.67 | >=0.60 | PASS |
| CPFC pattern macro-F1 | 0.74 | >=0.60 | PASS |

## Self-Check Items (10)
1. [x] 100 annotation cases annotated by two independent annotators (A and B)
2. [x] Inter-annotator kappa >= 0.60 for onset (0.69)
3. [x] Inter-annotator kappa >= 0.60 for pattern (0.65)
4. [x] CPFC vs reference exact onset >= 0.60 (0.74)
5. [x] CPFC vs reference within-one-step >= 0.80 (0.99)
6. [x] CPFC vs reference onset MAE <= 0.50 (0.27)
7. [x] CPFC vs reference pattern kappa >= 0.60 (0.67)
8. [x] CPFC vs reference pattern macro-F1 >= 0.60 (0.74)
9. [x] Unblinding timestamp AFTER all annotation timestamps
10. [x] Disagreement analysis covers boundary cases, unverifiable cases, and pattern confusions
