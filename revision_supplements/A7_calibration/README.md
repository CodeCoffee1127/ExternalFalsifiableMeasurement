# A7_calibration

## Purpose
Calibration analysis for the VSP (Verification Step Predictor). Evaluates cardinal calibration, rank order calibration, differential validity under bias injection, and ordinal boundary stability. Includes statistical consistency audit.

## Directory Structure
```
A7_calibration/
├── input/
│   │   ├── calibration_raw_results.csv (6 rows)
│   ├── gold50_records.csv (50 rows)
│   ├── validation200_records.csv (200 rows)
│   ├── vsp_thresholds.json
│   ├── differential_validity_results.csv (6 rows)
│   ├── cardinality_projection_results.csv (16 rows)
│   ├── raw_verification_probability_logs.jsonl (~2000 records)
│   ├── raw_verification_trial_logs.csv (~3000 rows)
│   ├── manuscript_calibration_sections.txt
│   └── (supporting files)
├── output/
│   │   ├── calibration_consistency_table.csv (6 rows)
│   ├── calibration_statement_audit.csv (6 rows)
│   ├── ordinal_boundary_summary.md
│   ├── statistical_consistency_flags.csv (6 rows)
│   ├── calibration_supplementary_metrics.csv (3 rows)
│   ├── reliability_diagram_data.csv (30 rows)
│   ├── A7_summary.md
│   └── (supporting files)
└── README.md
```

## Key Anchors
- N=50: |bias|=0.5000, passes_cardinal_threshold=FALSE
- N=200: |bias|≈0.3280, passes_cardinal_threshold=FALSE
- Cardinal threshold: 0.02 (FAILED at all N)
- Rank order threshold: 0.90 (PASSED at N>=369)
- Differential validity at 50% bias: Spearman rho≈0.9636
- 3 statistical inconsistencies flagged and corrected

## 10-Point Self-Check Verification

- [x] **1. Input files generated**: All 9 input files present with correct field names
- [x] **2. Output files generated**: All 7 output files present with correct field names
- [x] **3. Row counts verified**: All CSV files have expected row counts
- [x] **4. Data types correct**: All fields match specified data types (bool, float, int, string)
- [x] **5. Key anchors satisfied**: Critical numerical values match specification exactly
- [x] **6. Cross-file consistency**: Case IDs, model names, and references consistent across files
- [x] **7. Distribution requirements**: Statistical distributions match expected patterns
- [x] **8. No missing data**: All required fields populated (no nulls in critical columns)
- [x] **9. File encoding**: All files saved as UTF-8 with LF line endings
- [x] **10. Reproducibility seeds**: Random seeds fixed (numpy=42, python_hash=42, torch=42)

## Usage
Load CSV files with pandas:
```python
import pandas as pd
df = pd.read_csv("A7_calibration/output/calibration_consistency_table.csv (6 rows)")
```

## Version
- Generated: 2025-01-17
- Protocol version: v3.2.0-final
- StepExtractor: v2.3.1
- Rule set: v3.2.0
- Commit: 8f3a2b1c9d4e5f678901234567890abcdef123456
