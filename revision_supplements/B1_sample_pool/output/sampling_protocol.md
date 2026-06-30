# Sampling Protocol Documentation

## Protocol: Stratified Random Sampling for CPFC Annotation

### Overview
- **Source Population**: 369 dtest cases
- **Target Sample Size**: 100 annotation cases
- **Sampling Method**: Stratified random sampling with dual stratification (onset + pattern)
- **Random Seed**: 42

---

## Stratification Dimensions

### Dimension 1: Onset Stratum
| Stratum | Target | Actual | Notes |
|---------|--------|--------|-------|
| t0 | ~25 | 33 | First step degradation |
| t1 | ~22 | 26 | Second step degradation |
| t2 | ~18 | 20 | Third step degradation |
| no_degradation | ~15 | 11 | No degradation detected |
| uncertain | ~10 | 10 | Uncertain onset |

### Dimension 2: Pattern Stratum
| Stratum | Target | Actual | Notes |
|---------|--------|--------|-------|
| local_verification_collapse | ~28 | 25 | Largest ordinary class |
| dependency_mediated_propagation | ~24 | 25 | Second largest |
| burst_associated_degradation | ~16 | 14 | Smaller class |
| boundary_case | ~18 | 18 | Boundary cases |
| unverifiable_or_excluded | ~14 | 18 | Excluded from primary |

---

## Constraints Verified
- Largest ordinary pattern share: 25/100 = 0.25 <= 0.60 PASS
- Each major onset class >= 15: t0=33, t1=26, t2=20 PASS (no_degradation=11 < 15 noted)
- Each major pattern class >= 15: local=25, dep=25 PASS (burst=14 < 15 noted)

---

## Pair Eligibility

### Pair A: Same Endpoint Fail, Different Onset
- Target: >= 15 eligible pairs
- Actual: 211 eligible cases, 30 pair records generated
- Selected for manifest: 3 pairs

### Pair B: Same Onset, Different Pattern
- Target: >= 15 eligible pairs
- Actual: 281 eligible cases, 30 pair records generated
- Selected for manifest: 3 pairs

### Pair C: Standard vs Deep-Nesting
- Target: >= 8 eligible pairs
- Actual: 61 eligible cases, 20 pair records generated
- Selected for manifest: 2 pairs

---

## Blinding Protocol
- Case IDs replaced with annotation_case_id (annot_001 to annot_100)
- CPFC labels hidden (cpfc_labels_hidden = true)
- Ground truth SQL hidden (ground_truth_sql_hidden_flag = true)
- Model source hidden (model_source_hidden_flag = true)
- Boundary/unverifiable/deep_nesting flags visible to annotators

---

## Exclusion Criteria
Cases excluded if:
1. Unverifiable AND no checkpoint material
2. Fewer than 2 checkpoints
3. Corrupt schema file

---

## Reproducibility
- Random seed: 42 (recorded in random_seed_record.txt)
- Sampling date: 2025-02-01
- All selection decisions documented in full_candidate_pool_table.csv
