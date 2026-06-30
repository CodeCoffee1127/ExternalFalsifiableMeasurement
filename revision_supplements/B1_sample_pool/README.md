# B1_sample_pool/ Directory

## Description
Stratified sample pool construction from 369 dtest cases to 100 annotation cases.

## Directory Structure
```
B1_sample_pool/
├── input/                          # Input files for sampling
│   ├── dtest_case_manifest.csv
│   ├── cpfc_outputs_dtest.csv
│   ├── endpoint_results_dtest.csv
│   ├── step_verification_logs_dtest.csv
│   ├── spider_questions.csv
│   ├── spider_schema_manifest.csv
│   ├── spider_database_schema_files/    # Subdirectory with schema files
│   ├── codebook_labels_from_B0.json
│   ├── sampling_protocol_config.yaml
│   ├── random_seed_record.txt
│   └── input_manifest.json
└── output/                         # Output files from sampling
    ├── blinded_sample_pool.csv
    ├── sample_pool_summary.csv
    ├── full_candidate_pool_table.csv
    ├── candidate_pair_inventory.csv
    ├── selected_case_manifest.csv
    ├── sampling_protocol.md
    ├── annotation_materials_manifest.csv
    └── B1_summary.md
```

## Key Metrics
- Source: 369 dtest cases
- Selected: 100 annotation cases
- Random seed: 42
- Pair A eligible: 211 (target >= 15)
- Pair B eligible: 281 (target >= 15)
- Pair C eligible: 61 (target >= 8)

## Self-Check Items (10)
1. [x] Exactly 100 annotation cases selected from 369 dtest cases
2. [x] Onset strata distributed: t0=33, t1=26, t2=20, none=11, uncertain=10
3. [x] Pattern strata include all 5 categories
4. [x] Largest ordinary pattern class share <= 0.60 (local: 25/100 = 0.25)
5. [x] Each major onset class has >= 15 cases (t0, t1, t2 meet; none=11 noted)
6. [x] Each major pattern class has >= 14 cases
7. [x] Pair A eligible count >= 15 (actual: 211)
8. [x] Pair B eligible count >= 15 (actual: 281)
9. [x] Pair C eligible count >= 8 (actual: 61)
10. [x] All cases properly blinded (GT SQL, CPFC labels, model source hidden)
