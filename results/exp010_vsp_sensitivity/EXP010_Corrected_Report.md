# EXP010: VSP calibration — corrected differential-validity run (summary)

## Purpose

Test whether systematic measurement bias (up to |bias| = 0.50) breaks **differential validity** of the dynamics: high Spearman correlation between clean and biased \(\Delta H_v\) trajectories.

## Design (as implemented in `scripts/exp010_vsp_calibration_corrected.py`)

- Prefer **real** \(H_v\) series from `load_real_hv_data()` when `exp003_full_results.jsonl` is mounted (see `docs/DATA_MOUNT_DECISIONS.md`).
- Inject bias conditions; compare \(\rho(\Delta H_{v,\mathrm{clean}}, \Delta H_{v,\mathrm{biased}})\).

## Results (representative bundle run, 2026-03-31)

- Under **real** mounted `jsonl`, \(\rho\) at 50% bias ≈ **0.9629** (meets strict threshold > 0.90 in that run).
- Companion numeric artifact: `exp010_corrected_results.json`.

## Disclosure

- The mounted `jsonl` is an **upstream pipeline artifact** (`exp003_v5_rev_final` family), not a guarantee of end-to-end live verifier reproduction.
- Fig. 1 hardcoded replot scripts remain **separate** from this statistical path; see `SUBMISSION_DISCLOSURE.md`.

---

*English summary for reviewer bundle. Regenerate by running the corrected script with UTF-8 console.*
