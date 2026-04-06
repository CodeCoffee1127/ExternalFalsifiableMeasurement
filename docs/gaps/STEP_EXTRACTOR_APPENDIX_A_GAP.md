# StepExtractor: Appendix A specification vs this repository

## Paper requirement (Appendix A)

Algorithm 1 describes a **verifier-driven** segmenter with:

- Character stream buffer of width `W`
- `StructureParse(B, R)` completion / error handling
- Accepted steps as JSON with **proposition**, **parent_refs**, **step_id**

## What this bundle now provides (paper-based reconstruction)

An **executable minimal** implementation lives under `code/step_extractor/`:

- `step_extractor.VerifierDrivenStepExtractor` — buffer loop + optional Verifier gate + tail flush for short streams.
- `segmentation.structure_parse` — **heuristic** completeness (semicolon termination or SELECT/FROM skeleton), **not** a standards-compliant SQL parser.
- `schema.StepObject` — JSON-shaped records for reviewers.
- `bridge_sql_pipeline.clause_records_to_step_objects` — maps **source-backed** LLM clause chains to the same field names (explicitly **not** Algorithm-1 equivalent).

Read **`code/step_extractor/README_RECONSTRUCTION.md`** for classification boundaries.

## Source-backed empirical path (implicit in original codebase)

1. `code/llm/aliyun_api.py` — `generate_step_by_step()` builds partial SQL per clause phase.
2. `code/pipeline/experiment_pipeline.py` — consumes that chain and runs CPFC/VSP verification.

## What remains unclaimed

- **Byte-for-byte** equivalence to any lost production StepExtractor.
- Full **StructureParse** fidelity to the paper’s rule library \(\mathcal{R}\) beyond the bundled heuristic.

## If reviewers require stricter Algorithm 1 fidelity

Extend `segmentation.py` and plug a real Verifier callback; do not rewrite read-only upstream trees outside this bundle.
