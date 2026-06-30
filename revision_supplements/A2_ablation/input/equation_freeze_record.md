# Equation Freeze Record

## Frozen Equations for A2 Ablation Study

All information-theoretic construction equations are frozen at their training values.
No retuning or refitting is permitted during ablation.

### Frozen Construction Equations

| Equation | Symbol | Description | Frozen Parameters | Status |
|----------|--------|-------------|-------------------|--------|
| A_t | A_t | Atomic verification score at step t | threshold=0.5, smoothing=0.1 | **FROZEN** |
| H_t | H_t | Verification entropy at step t | base=2 normalization | **FROZEN** |
| delta_H | delta_H | Entropy change: H_t - H_{t-1} | window=1 | **FROZEN** |
| I_plus | I+ | Positive information gain | gamma=0.8, epsilon=1e-6 | **FROZEN** |
| I_minus | I- | Negative information (uncertainty) | gamma=0.8, epsilon=1e-6 | **FROZEN** |
| I_nec | I_nec | Necessity information | alpha=0.5, beta=0.3 | **FROZEN** |
| burst_flag | b_t | Burst degradation indicator | min_cluster=2, max_gap=1 | **FROZEN** |
| gate_pass | g_t | Quality gate indicator | thresholds from training | **FROZEN** |

### Freeze Protocol

1. All construction parameters were fixed at values determined during model development
2. No cross-validation or grid search during ablation
3. Any NaN or undefined outputs are treated as excluded observations
4. Boundary cases flagged but not removed from estimation sample

### Verification

- [x] A_t construction frozen
- [x] H_t construction frozen  
- [x] delta_H construction frozen
- [x] I_plus construction frozen
- [x] I_minus construction frozen
- [x] I_nec construction frozen
- [x] burst_flag construction frozen
- [x] gate_pass construction frozen

Signed: ___________________ Date: 2025-01-15
