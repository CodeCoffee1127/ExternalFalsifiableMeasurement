# Project status matrix (reviewer view)

Support levels:

- **R** Runnable as-is (may need UTF-8 on Windows)
- **R+** Runnable with minimal mounted data (`docs/DATA_MOUNT_DECISIONS.md`)
- **PAR** Paper-aligned reconstruction (targets or simulators match paper method description)
- **PBR** Paper-based reconstruction (spec-shaped code; not original lost implementation)
- **HCR** Hardcoded replot / embedded paper constants
- **SIM** Simulation (explicit noise / stub)
- **ART** Asset-bridged (shipped LaTeX figures copied/synced into `figures/` for a single bundle path; **not** a full regeneration claim)
- **DOC** Documentation-only in code terms
- **BLK** Blocked without additional upstream assets (full Spider DB, API keys, etc.)

| ID | Figure / table (paper) | Support | Canonical entry | Reviewer notes |
|----|-------------------------|---------|-----------------|----------------|
| EXP001 | Fig. 2 VSP radar | HCR | `scripts/run_exp001_main.py` | Hardcoded panel values |
| EXP002 | Fig. 6 synthetic | HCR | `scripts/run_exp002_main.py` | Synthetic pre-validation layout |
| EXP003 | Rescue stats / tables | R+ / SIM-in-runner | `scripts/run_exp003_main.py` | Spider JSON required; in-runner synthesis; dual chain: `paper_aligned_reconstruction/` |
| EXP006 | Tab cross-model | SIM | `scripts/run_exp006_main.py` | Not live multi-API |
| EXP010 | Fig. 1 + diff. validity | R+ / HCR | `scripts/run_exp010_main.py`, `pipelines/run_exp010_figure_chain.py` | jsonl for real H_v; Fig.1 HCR |
| EXP021 | Tab exp021 | R | `scripts/run_exp021_main.py` | Check in-file data paths |
| EXP022 | Tab exp022 | R | `scripts/run_exp022_main.py` | Uses sqlparse |
| EXP023 | Tab exp023 | R | `scripts/run_exp023_main.py` | Identification comparison |
| EXP024 | Figs 3–5 | R / PAR / HCR | `scripts/run_exp024_main.py` | Modes: empirical (BLK likely), simulation (PAR), figures (HCR) |
| EXP025 | Figs 10–12, App. H | **R+ / SB audit + ART figures** | `scripts/run_exp025_main.py` | **Figures are asset-bridged** from `paper_sources/figures/` — **inspectable and paper-aligned**, **not fully regenerated** from one code path; **trace gap** documented. `run_exp025_v3.py` may print **non-English** legacy strings. |
| Alg.1 StepExtractor | App. A | PBR | `code/step_extractor/step_extractor.py` | Executable minimal core + gap docs |
| CPFC / Verifier | Sec. III–IV | SB | `code/cpfc/*`, `code/verifier/*` | Source-backed |
| Fig. 7 | structural failure | R | `scripts/generate_fig7_structural_failure_phase2_v32.py` | Requires `brokenaxes` |
| Protocol table | Tab diagnostic | DOC | `paper_sources/paper1.tex` | Formalized in LaTeX |

---

*Updated: Submission Polish Final Phase (EXP025 disclosure tightened).*
