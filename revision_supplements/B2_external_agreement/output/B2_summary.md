# B2 External Agreement Summary

## Directory: B2_external_agreement/

### Input Files (7)
| File | Rows | Description |
|------|------|-------------|
| annotation_codebook.md | -- | Frozen codebook from B0 |
| blinded_sample_pool.csv | 100 | Blinded sample from B1 |
| annotation_materials_manifest.csv | 100 | Material paths from B1 |
| annotator_A_raw.csv | 100 | Annotator A annotations |
| annotator_B_raw.csv | 100 | Annotator B annotations |
| cpfc_labels_unblinded_after_annotation.csv | 100 | Unblinded CPFC labels |
| adjudication_optional.csv | 5 | Optional adjudications |
| input_manifest.json | -- | Input manifest |

### Output Files (8)
| File | Rows | Description |
|------|------|-------------|
| inter_annotator_agreement.csv | 4 | A-B agreement metrics |
| cpfc_vs_external_reference_agreement.csv | 4 | CPFC vs reference metrics |
| onset_agreement_metrics.csv | 5 | Onset by stratum |
| pattern_agreement_metrics.csv | 5 | Pattern by category |
| pattern_confusion_matrix.csv | 5x5 | Confusion matrix |
| disagreement_analysis.md | -- | Full analysis |
| annotation_freeze_record.md | -- | Freeze record |
| B2_summary.md | -- | This summary |

### Key Metrics
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Inter-annotator onset kappa | 0.69 | >=0.60 | PASS |
| Inter-annotator pattern kappa | 0.65 | >=0.60 | PASS |
| CPFC exact onset agreement | 0.74 | >=0.60 | PASS |
| CPFC within-one-step | 0.99 | >=0.80 | PASS |
| CPFC onset MAE | 0.27 | <=0.50 | PASS |
| CPFC onset kappa | 0.65 | >=0.60 | PASS |
| CPFC pattern kappa | 0.67 | >=0.60 | PASS |
| CPFC pattern macro-F1 | 0.74 | >=0.60 | PASS |

### Self-Check Items
- [x] 100 annotation cases from blinded pool
- [x] Two independent annotators (A and B)
- [x] Inter-annotator kappa >= 0.60 for onset (0.69)
- [x] Inter-annotator kappa >= 0.60 for pattern (0.65)
- [x] CPFC vs ref exact onset >= 0.60 (0.74)
- [x] CPFC vs ref within-one-step >= 0.80 (0.99)
- [x] CPFC vs ref onset MAE <= 0.50 (0.27)
- [x] CPFC vs ref pattern kappa >= 0.60 (0.67)
- [x] CPFC vs ref pattern macro-F1 >= 0.60 (0.74)
- [x] Unblinding timestamp AFTER annotation timestamps
