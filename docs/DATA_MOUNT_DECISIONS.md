# DATA_MOUNT_DECISIONS.md (Phase 4.6)

All copies are **read-only pull** from `D:\ExternalFalsifiableMeasurement` into this bundle. **No edits** were made to the source tree.

## Files copied

| Bundle path | Source path | Size (approx) | Reason |
|-------------|-------------|---------------|--------|
| `spider/dev.json` | `D:\ExternalFalsifiableMeasurement\spider\dev.json` | Spider dev split | EXP003 tier/load; EXP025 primary loader |
| `spider/train_spider.json` | `D:\ExternalFalsifiableMeasurement\spider\train_spider.json` | Train split | EXP003 `load_and_prepare_data` requires both dev+train |
| `data/test/test.json` | `D:\ExternalFalsifiableMeasurement\data\test\test.json` | Fallback | EXP025 v3 if `spider/dev.json` absent (now redundant but kept for parity) |
| `data/results/exp003_v5_rev_final/exp003_full_results.jsonl` | `D:\ExternalFalsifiableMeasurement\data\results\exp003_v5_rev_final\exp003_full_results.jsonl` | 58,206 bytes | **Single canonical H_v input** for EXP010 / EXP024-style loaders |

## Why this `jsonl` copy (and not the duplicate under `clouds_outputs/`)

- Two byte-identical copies existed:
  - `clouds_outputs\exp003_v5_rev_final\exp003_full_results.jsonl`
  - `data\results\exp003_v5_rev_final\exp003_full_results.jsonl`
- Same length (58,206 bytes). **Chose `data/results/...`** as canonical mount path because it matches conventional repo layout and is the **second** candidate in `load_real_hv_data()` / EXP024 loaders—scripts try `clouds_outputs` first, then **`data/results`** (which now hits in this bundle).
- **Did not copy** the `clouds_outputs` duplicate to avoid two identical artifacts.

## Experiments enabled / advanced

| Chain | Effect of mount |
|-------|------------------|
| EXP003 `full_rerun` | Loads **8,034** SQL rows; stratified **369** samples; **no longer** empty-DataFrame crash. **Note:** trajectory rows are still **synthesized** inside the script (`generate_experiment_data`), not produced by live LLM + DB verifier. |
| EXP025 v3 | Loads Spider dev; completes pipeline to **Layer 1** (may FAIL preregistered checks but **no FileNotFoundError**); writes reports under `experiment_reports/EXP025_v3/`. |
| EXP010 corrected | With UTF-8 console, loads **real** `H_v` series from mounted `jsonl`; run **completed** (ρ@50% ≈ 0.9629 in test run). |
| EXP006 | Unchanged data need; still **simulation**; UTF-8 required for stdout. |

## Deliberately NOT copied (Phase 4.6)

- Entire `spider/database/` SQLite files — not required for the scripts exercised above (they only need JSON question/SQL metadata for tiering and EXP025 logic).
- Bulk `results/` trees (except the one `jsonl` above).
- Full `experiment_reports/` archive.
- `clouds_outputs/` duplicate `jsonl`.

## Honesty flags

1. **Mounted `jsonl`** originates from upstream **`exp003_v5_rev_final`** — **paper-aligned / reconstruction** context per `docs/reconstruction/RECOVERY_REPORT.md`; using it for EXP010 is **real input** relative to that pipeline, not proof of end-to-end live measurement.
2. **EXP003 `full_rerun`** after mount still generates **synthetic** per-step metrics from sampled questions; **negative R²** in smoke run is expected and **not** the paper’s reported 0.945.

---

*Phase 4.6.*
