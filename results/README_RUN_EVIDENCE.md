# Run evidence (minimal, non-misleading)

This folder holds **small, intentional** artifacts that document what was executed in this bundle. It is **not** a full historical results archive. The **submission zip** omits bulky logs and duplicate JSONL dumps that remain in the author-side archival bundle.

| Path | Chain | Classification |
|------|--------|----------------|
| `exp006_cross_model/cross_model_results.json` | EXP006 | **Simulation-based** (Gaussian noise around optional baseline). See `docs/disclosures/EXP006_simulation.md`. |
| `exp010_vsp_sensitivity/exp010_corrected_results.json` + `EXP010_Corrected_Report.md` | EXP010 | **Real H_v path** when `data/results/exp003_v5_rev_final/exp003_full_results.jsonl` is mounted; input is an **upstream pipeline artifact**. |
| `exp003_rerun_20260312/exp003_global_results.json`, `exp003_tiered_results.json`, `data_split_manifest.json`, `FREEZE_PROTOCOL_LOG.json` | EXP003 | **Honest minimal rerun** subset — global + tiered summaries and protocol metadata only; **not** shipped here: full `exp003_full_results.jsonl`, long `exp003_rerun.log`, or `discrepancy_report.md` (archival bundle only). Trajectory metrics in the empirical-style runner are **synthesized in-script** — not the paper’s final published statistic chain by itself. |

## Policy

- Do **not** treat these JSON files as proof that every paper figure recomputes from raw verifier logs.
- For gaps and hardcoded figure scripts, see `SUBMISSION_DISCLOSURE.md` and `FILE_MANIFEST.md`.
