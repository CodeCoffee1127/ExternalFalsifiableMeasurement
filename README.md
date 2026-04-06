# External Falsifiable Measurement for Long-Chain Reasoning: From Structural Hypothesis to Principled Degradation

> **Paper**: External Falsifiable Measurement for Long-Chain Reasoning: From Structural Hypothesis to Principled Degradation
> **Journal**: Information Sciences (under review)
> **Status**: Submitted
> **Code Repository**: https://github.com/CodeCoffee1127/ExternalFalsifiableMeasurement
> **Data Archive**: [figshare DOI — to be added after upload]

## Abstract

The central gap in long-chain reasoning research is not performance but the absence of externally operationalized intermediate states; without such states, degradation cannot be localized, mechanism-level comparison cannot be grounded, and revision cannot be empirically constrained. This paper establishes a falsifiable, protocol-constrained external measurement framework that renders intermediate-state degradation externally observable, testable, and revisable under declared instrument constraints, rather than advancing a stronger solver. Under the present data and instrument conditions, the original continuous realization is rejected as statistically unidentifiable, with held-out . A degraded Rescue Dynamics specification is retained only as the current identifiable implementation under the present operationalization, supported by residual whiteness (Ljung-Box ) and population-level explanatory power (), and remains admissible only in bounded diagnostic form, not as mechanism recovery. Inference remains explicitly bounded: absolute calibration is incomplete ( at ), sparse per-step support () restricts analysis to ordinal and population-level comparison, and deep-nesting complex-tier failures remain a constitutive boundary; future work requires construct redefinition under recursive scope-crossing dependencies rather than extension of the present implementation into an absolute or individual-chain model.

---

# External falsifiable measurement — paper-aligned submission project

**Reviewers:** start with **`REVIEWER_START_HERE.md`** (one page), then **`QUICKSTART.md`**. **Provenance of this zip:** **`SUBMISSION_PACKAGE_NOTE.md`**.

**Single coherent reviewer-facing package** for journal supplementary review: **strict alignment** to `paper_sources/paper1.tex`, appendices, and figures. Original upstream history may be incomplete; this tree is the **authoritative submission-facing** layout (canonical runners + classifications), not a loose patch pile.

## Project overview

The paper studies **verifier-gated falsifiable measurement** on text-to-SQL style trajectories: dynamics, tier stratification, rescue/falsification panels, and robustness narratives. This bundle packages:

- **LaTeX** main text and appendices for cross-checking claims (`paper_sources/`).
- **Python modules** that implement CPFC/VSP verification, state dynamics, and experiment drivers (`code/`, exposed also as `src/` via a directory junction on Windows).
- **Scripts** for selected experiments and figure emitters (`scripts/`).
- **Minimal data** required to run a subset of drivers without fabricating missing inputs (`spider/*.json`, `data/...` — see `docs/DATA_MOUNT_DECISIONS.md`).
- **English disclosure** of every known gap (`SUBMISSION_DISCLOSURE.md`, `docs/gaps/`, `docs/disclosures/`).

## Relation to the paper

- Anchors are **`paper_sources/paper1.tex`** and **`paper_sources/appendices/*.tex`**.
- Shipped **PDF/PNG** under `paper_sources/figures/` are **reference renders** from the LaTeX project copy; they do not automatically prove that every panel recomputes from the scripts in this zip.

## Source-backed vs paper-backed reconstruction

| Term | Meaning in this bundle |
|------|-------------------------|
| **Source-backed** | Copied from the read-only upstream code tree without editing that tree; behavior is whatever the script/module implements. |
| **Paper-based reconstruction** | Spec-shaped code where production sources are missing (e.g. **executable minimal** `VerifierDrivenStepExtractor` + minimal `StructureParse` — **not** claimed equal to lost production). |
| **Paper-aligned reconstruction** | Upstream methods that **target published statistics** (e.g. EXP003 v5_rev matcher, EXP024 gold-standard simulator per docstrings). |
| **Simulation-based** | Stochastic or synthetic drivers (e.g. EXP006). |
| **Hardcoded replot** | Figure scripts embedding paper-table constants. |
| **Asset-bridged** | Shipped LaTeX figure assets (and similar) copied into output dirs for inspection — **not** a proven full recompute chain from raw logs. |

## What is runnable now

See **`QUICKSTART.md`** and **`REPRODUCIBILITY.md`**. In short (with UTF-8 on Windows and minimal data):

- **EXP006** — completes; **simulation** (`docs/disclosures/EXP006_simulation.md`).
- **EXP010 corrected** — completes with mounted `exp003_full_results.jsonl`; **real H_v path** relative to that artifact (`SUBMISSION_DISCLOSURE.md`).
- **EXP003 full_rerun** — completes with Spider JSON; **synthetic** trajectory metrics in-runner; **not** the paper’s final statistic chain by itself.
- **EXP025 v3** — runs; may **FAIL** preregistered layers; figure filename regeneration **not fully traced** (`docs/gaps/EXP025_figure_regeneration_trace.md`).
- **Hardcoded figure scripts** — e.g. Fig. 1, Fig. 3–6 emitters — run with matplotlib; they **replot embedded values**.

## What is not fully recoverable

- Full upstream **`results/`** history, notebooks, and ad-hoc exports.
- **Production** StepExtractor as deployed in the lost workspace (superseded for review by **PBR** `code/step_extractor/*`).
- **End-to-end** regeneration proven for every LaTeX figure filename from Python alone (EXP025 main Figs 10–12 use **artifact bridge** + gap disclosure).
- **Live multi-vendor LLM** reruns for EXP006.

**Do not** claim full empirical replication without adding data, credentials, and missing drivers. See **`docs/reconstruction/RECOVERY_REPORT.md`** (optional deep read).

## Directory structure

```text
SUBMISSION_PACKAGE_NOTE.md   # How this submission zip relates to the archival bundle
paper_sources/               # paper1.tex, appendices/, figures/
docs/mapping/                # paper_to_project_master_map.md, PROJECT_STATUS_MATRIX.md
docs/reconstruction/         # RECOVERY_REPORT.md (optional)
code/                        # cpfc, verifier, state, dynamics, step_extractor, …
src/                         # Junction → code (Windows)
scripts/
  run_exp001_main.py … run_exp025_main.py   # Canonical paper-facing entrypoints
  exp025_main_analysis.py                   # EXP025 v3 delegate
  exp025_generate_main_figures.py           # Fig 10–12 asset bridge
  exp025_generate_appendix_figures.py       # Appendix H figure bridge
  generate_figures_main.py                  # Paper-ordered figure orchestrator
  pipelines/run_exp010_figure_chain.py      # EXP010 stats → Fig.1
  paper_aligned_reconstruction/
configs/  data/  spider/  results/  figures/  experiment_reports/
docs/disclosures/  docs/gaps/  docs/DATA_MOUNT_DECISIONS.md  docs/WINDOWS_UTF8_RUNTIME.md
```

## Minimal execution entry points

1. `pip install -r requirements.txt`
2. `set PYTHONIOENCODING=utf-8` (Windows)
3. `python scripts/run_exp006_main.py` — canonical **disclosed** simulation chain
4. `python scripts/generate_figures_main.py --only 1,2` — sample figure orchestration
5. Read **`docs/mapping/paper_to_project_master_map.md`**, **`docs/mapping/PROJECT_STATUS_MATRIX.md`**, and **`SUBMISSION_DISCLOSURE.md`** before citing numbers.

## Benchmark Datasets

The following benchmark datasets are **not included** in this repository. Download them separately from their official sources:

- **Spider**: Text-to-SQL benchmark. Official repository: https://yale-lily.github.io/spider
- **BIRD**: Large-scale text-to-SQL benchmark. Official repository: https://bird-bench.github.io

Download these datasets separately and place them according to `docs/DATA_MOUNT_DECISIONS.md`.

## Disclosure summary

Consolidated for editors/reviewers in **`SUBMISSION_DISCLOSURE.md`**. Per-component notes in **`docs/disclosures/`** and **`docs/gaps/`**.

---

*Read-only sources `D:\ExternalFalsifiableMeasurement` and `D:\Latex\Paper1_2.0` were not modified. This reviewer-facing tree is a **selective export**; see **`SUBMISSION_PACKAGE_NOTE.md`**.*


## Citation

If you use this code or data, please cite our paper:

```bibtex
@article{TODO_citation,
  title   = {External Falsifiable Measurement for Long-Chain Reasoning: From Structural Hypothesis to Principled Degradation},
  journal = {Information Sciences},
  year    = {2025},
  note    = {Under review. DOI to be updated upon publication.}
}
```

## License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.

> **Note**: The LaTeX manuscript source (`paper_sources/`) is not included in this public repository
> while the paper is under review. It will be made available upon acceptance.
