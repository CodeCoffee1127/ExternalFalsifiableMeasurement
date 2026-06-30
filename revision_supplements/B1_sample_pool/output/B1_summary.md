# B1 Sample Pool Summary

## Directory: B1_sample_pool/

### Input Files (9)
| File | Rows | Description |
|------|------|-------------|
| dtest_case_manifest.csv | 369 | Full dtest case manifest |
| cpfc_outputs_dtest.csv | 369 | CPFC model outputs for all cases |
| endpoint_results_dtest.csv | 369 | Endpoint execution results |
| step_verification_logs_dtest.csv | ~1570 | Per-step verification logs |
| spider_questions.csv | 100 | Spider question texts |
| spider_schema_manifest.csv | 12 | Schema manifest for all DBs |
| codebook_labels_from_B0.json | -- | Codebook labels from B0 |
| sampling_protocol_config.yaml | -- | Stratified sampling configuration |
| random_seed_record.txt | -- | Random seed (42) |

### Output Files (8)
| File | Rows | Description |
|------|------|-------------|
| blinded_sample_pool.csv | 100 | Blinded annotation sample pool |
| sample_pool_summary.csv | 13 | Pool composition summary |
| full_candidate_pool_table.csv | 369 | All cases with pair eligibility |
| candidate_pair_inventory.csv | ~80 | Eligible pair inventory |
| selected_case_manifest.csv | 8 | Selected pairs for annotation |
| sampling_protocol.md | -- | Sampling protocol documentation |
| annotation_materials_manifest.csv | 100 | Annotation material file paths |
| B1_summary.md | -- | This summary |

### Key Metrics
- Sample size: **100 cases** from 369 dtest
- Onset distribution: t0=33, t1=26, t2=20, none=11, uncertain=10
- Pattern distribution: local=25, dep=25, burst=14, boundary=18, unverifiable=18
- Pair A eligible: **211** (target >=15) PASS
- Pair B eligible: **281** (target >=15) PASS
- Pair C eligible: **61** (target >=8) PASS
- Largest pattern share: 0.25 (target <=0.60) PASS

### Self-Check Items
- [x] Exactly 100 annotation cases selected
- [x] Onset strata distributed across t0/t1/t2/none/uncertain
- [x] Pattern strata include all 5 categories
- [x] Largest ordinary pattern class share <= 0.60
- [x] Each major onset class has sufficient representation
- [x] Each major pattern class has sufficient representation
- [x] Pair A eligible count >= 15 (actual: 211)
- [x] Pair B eligible count >= 15 (actual: 281)
- [x] Pair C eligible count >= 8 (actual: 61)
- [x] All cases properly blinded (GT SQL, CPFC labels, model source hidden)
