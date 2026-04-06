# EXP025-v3: Technical Report

**Experiment:** EXP025-v3 **Generated:** 20260331_201120 **Data source:** D_test (N=457) — `data/test/test.json`

## 1. Data source declaration

- Origin: D_test JSON in bundle
- Sample count: 457 SQL items
- Synthetic data: none declared
- Cache: none declared

## 2. Sample construction protocol

- Condition A: AST depth = 1, no scope-crossing
- Condition B: AST depth ≥ 2 with scope-crossing
- Matching: nearest-neighbor (PSM-style)
- Constraint: SMD < 0.20 (SMD = 0 disallowed)

## 3. Pre-registered exclusion chain

### Layer 1: Surface complexity

- Mean SMD: 0.9468440929533608
- Status: FAILED

### Layer 2: Measurement stability

- Test–retest r: N/A
- CV: N/A
- Status: NOT REACHED

### Layer 3: Construct adequacy

- Adjusted OR: N/A
- 95% CI: N/A
- Status: NOT REACHED

## 4. Anomaly flags

- Warning: CV = 0.0000 — possible duplicate structure in inputs (script warning)

## 5. Statistical summary

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Mean SMD | 0.9468440929533608 | < 0.20 | FAIL |
| HC3 Δ (pp) | 63.99999999999999 | ≥ 25 pp | FAIL |
| Test–retest r | N/A | ≥ 0.85 | N/A |
| CV | N/A | ≤ 0.12 | N/A |
| Adjusted OR | N/A | > 3.0 | N/A |

## Validity status

- Data integrity (audit narrative): mixed — see data audit file
- Protocol compliance: FAIL
- Result validity: INVALID (chain stopped at Layer 1)

## Final diagnosis

- Surface complexity: FAILED
- Measurement boundary: NOT REACHED
- Mechanism boundary: NOT REACHED
