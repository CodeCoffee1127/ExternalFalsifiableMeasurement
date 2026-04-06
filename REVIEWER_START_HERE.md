# Reviewer start here

## 1. What this bundle is

A **paper-aligned supplementary code archive** for *External Falsifiable Measurement for Long-Chain Reasoning*: CPFC, verifier-gated states, VSP, synthetic pre-validation, diagnostic protocol, rescue dynamics, and tier/complex-tier analyses. It is a **single curated tree** mapped to `paper_sources/paper1.tex`, not a claim of full bitwise recovery of every historical upstream artifact.

## 2. How it relates to `paper1.tex`

- **LaTeX source** shipped under `paper_sources/` (main text + appendices + figure assets).
- **Python** implements or **labels** each major claim as **source-backed**, **paper-based reconstruction**, **paper-aligned reconstruction**, **simulation-based**, **hardcoded replot**, or **asset-bridged** (see disclosure files).
- **No** statement here implies that every table or figure recomputes from raw verifier logs inside this zip alone without extra data or credentials.

## 3. Suggested reading order (short path)

1. **`README.md`** — scope, terminology, directory map.  
2. **`QUICKSTART.md`** — environment, UTF-8, minimal data, **canonical entry scripts** table.  
3. **`SUBMISSION_DISCLOSURE.md`** — limitations, dual chains, simulation, hardcoded figures, EXP025 figure policy.  
4. **`docs/mapping/paper_to_project_master_map.md`** — section / figure / experiment → bundle path.  
5. **`docs/mapping/PROJECT_STATUS_MATRIX.md`** — support level per artifact (runnable, HCR, ART, etc.).

Then, as needed: **`REPRODUCIBILITY.md`**, **`docs/reconstruction/RECOVERY_REPORT.md`**, **`FILE_MANIFEST.md`**, **`SUBMISSION_PACKAGE_NOTE.md`**.

## 4. Shortest sanity checks (from bundle root)

```bat
set PYTHONIOENCODING=utf-8
pip install -r requirements.txt
python -c "import sys; sys.path.insert(0,'src'); import cpfc, verifier, step_extractor; print('import ok')"
python scripts\run_exp006_main.py
```

(Optional) With minimal data mounted per `docs/DATA_MOUNT_DECISIONS.md`: `python scripts\run_exp010_main.py`.

## 5. Where limitations are documented

- **`SUBMISSION_DISCLOSURE.md`** — primary honesty statement for editors/reviewers.  
- **`docs/disclosures/`** and **`docs/gaps/`** — per-topic gaps (StepExtractor, EXP003 dual chain, EXP006 simulation, EXP025 trace).  
- **`docs/reconstruction/RECOVERY_REPORT.md`** — what was missing, what was reconstructed, what stays unrecoverable.

---

*This file is the recommended entry point before running any script.*
