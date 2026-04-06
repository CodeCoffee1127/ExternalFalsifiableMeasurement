# EXP003: two chains in this bundle

## 1. Empirical / mechanism main chain (preferred for an honest rerun)

- **Implementation:** `code/dynamics/exp003_rescue_fixed_effects.py`, `exp003_nuclear_fix.py`
- **Runner:** `scripts/exp003_full_rerun.py`
- **Role:** Fit Rescue-style dynamics with frozen thresholds and tier counts as coded; depends on data paths and API keys as in the original project.

## 2. Paper-aligned reconstruction (published numbers)

- **File:** `scripts/paper_aligned_reconstruction/exp003_v5_rev_final_target_matching.py`  
  (copied from upstream `experiments/exp003_v5_rev/exp003_final.py`.)
- **Role:** Upstream docstring describes **direct generation** of trajectories / residuals to hit targets such as \(N=369\), \(R^2\approx 0.945\), Ljung-Box \(p\approx 0.258\).
- **Not interchangeable** with chain (1) for claims about what the live pipeline produced.

Use (2) only to **audit** or **reproduce printed statistics** under the upstream reconstruction method; disclose accordingly in any publication supplement.
