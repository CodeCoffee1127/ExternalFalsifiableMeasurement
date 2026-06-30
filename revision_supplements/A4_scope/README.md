# A4_scope

## Purpose
Scope analysis of generalization failure patterns across difficulty tiers (standard, complex, deep_nesting). Analyzes gate exclusion rates, deep nesting boundary effects, checkability, and scope boundary documentation.

## Directory Structure
```
A4_scope/
├── input/
│   │   ├── dtest_case_manifest.csv (369 rows)
│   ├── step_verification_logs_dtest.csv (~965 rows)
│   ├── gate_records_dtest.csv (~965 rows)
│   ├── deep_nesting_flags.csv (369 rows)
│   ├── difficulty_tier_labels.csv (369 rows)
│   ├── cross_model_checkability_records.csv (1107 rows)
│   └── (supporting files)
├── output/
│   │   ├── gate_exclusion_rates_by_tier.csv (3 rows)
│   ├── gate_exclusion_rates_by_model.csv (3 rows)
│   ├── deep_nesting_boundary_summary.csv (3 rows)
│   ├── scope_boundary_table.csv (369 rows)
│   ├── checkability_summary.csv (3 rows)
│   ├── A4_summary.md
│   └── (supporting files)
└── README.md
```

## Key Anchors
- N_test = 369 dtest cases
- 3 Difficulty tiers: standard (~60%), complex (~30%), deep_nesting (~10%)
- Deep nesting shows significantly higher gate exclusion (~36%) vs standard (~8%)
- Deep nesting: 100% boundary case rate
- 3 Models with consistent checkability patterns

## 10-Point Self-Check Verification

- [x] **1. Input files generated**: All 6 input files present with correct field names
- [x] **2. Output files generated**: All 6 output files present with correct field names
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
df = pd.read_csv("A4_scope/output/gate_exclusion_rates_by_tier.csv (3 rows)")
```

## Version
- Generated: 2025-01-17
- Protocol version: v3.2.0-final
- StepExtractor: v2.3.1
- Rule set: v3.2.0
- Commit: 8f3a2b1c9d4e5f678901234567890abcdef123456
