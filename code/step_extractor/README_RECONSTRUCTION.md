# StepExtractor — paper-driven reconstruction (Appendix A Algorithm 1)

## Classification

**Paper-based reconstruction.** This package provides:

1. **`VerifierDrivenStepExtractor`** (`step_extractor.py`) — executable control flow matching the pseudocode structure (buffer `W`, `StructureParse`, Verifier gate, accept / clear).
2. **`structure_parse`** (`segmentation.py`) — minimal syntactic heuristic (semicolon / SELECT–FROM skeleton), **not** a standards-compliant SQL parser.
3. **`StepObject`** (`schema.py`) — JSON-shaped records with `proposition`, `parent_refs`, `step_id`.
4. **`clause_records_to_step_objects`** (`bridge_sql_pipeline.py`) — maps the **source-backed** LLM clause chain (`aliyun_api.generate_step_by_step`) into the same JSON field names for reviewer traceability.

## What is not claimed

- Byte-for-byte equivalence to any lost production StepExtractor.
- Full verifier semantics inside `StructureParse`; validation is delegated to the optional Verifier callback or downstream CPFC code.

## Quick demo

```bash
python -c "from step_extractor.step_extractor import demo_run; print(demo_run('SELECT a FROM t;'))"
```

(Run from bundle root with `PYTHONPATH=code` or via `src` junction.)

## Relation to `paper_based_step_extractor_reconstruction.py`

That module retains the **gap statement** and neutral normalization helpers. The **executable** Algorithm-1-shaped loop lives in `step_extractor.py` and `segmentation.py`.
