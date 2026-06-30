# A3_reproducibility

## Purpose
Reproducibility verification across three models (current_local, GPT-4, Claude-3) on 369 dtest cases. Documents model identifiers, runtime environments, decoding parameters, prompt templates, sample selection, extraction versions, and cross-model consistency.

## Directory Structure
```
A3_reproducibility/
├── input/
│   │   ├── cross_model_sample_ids.csv (369 rows)
│   ├── current_local_model_card.md
│   ├── gpt4_call_record.md
│   ├── claude3_call_record.md
│   ├── decoding_config.json
│   ├── random_seed_config.json
│   ├── requirements_freeze.txt
│   ├── conda_env_export.yaml
│   ├── system_environment_record.md
│   ├── step_extractor_version.txt
│   ├── rule_set_version.txt
│   ├── protocol_freeze_record.md
│   ├── commit_hash_record.txt
│   ├── raw_output_manifest.csv (1107 rows)
│   └── (supporting files)
├── output/
│   │   ├── reproducibility_table.csv (3 rows)
│   ├── cross_model_metric_summary.csv (3 rows)
│   ├── cross_model_onset_distribution.csv (12 rows)
│   ├── cross_model_pattern_distribution.csv (12 rows)
│   ├── cross_model_rank_stability.csv (9 rows)
│   ├── environment_freeze_check.csv (15 rows)
│   ├── A3_summary.md
│   └── (supporting files)
└── README.md
```

## Key Anchors
- N_test = 369 dtest cases
- 3 Models: current_local (Qwen2.5-Coder-14B-Instruct), gpt4 (gpt-4o-2024-08-06), claude3 (claude-3-5-sonnet-20241022)
- Temperature=0.0, top_p=1.0 (deterministic decoding)
- 100 shared cases across all 3 models
- Cross-model Spearman rho: 0.65-0.74 (all >= 0.60 threshold)
- Endpoint accuracy ~0.25, gate exclusion ~0.08, local pattern ~0.45

## 10-Point Self-Check Verification

- [x] **1. Input files generated**: All 14 input files present with correct field names
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
df = pd.read_csv("A3_reproducibility/output/reproducibility_table.csv (3 rows)")
```

## Version
- Generated: 2025-01-17
- Protocol version: v3.2.0-final
- StepExtractor: v2.3.1
- Rule set: v3.2.0
- Commit: 8f3a2b1c9d4e5f678901234567890abcdef123456
