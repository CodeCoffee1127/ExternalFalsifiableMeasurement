# paper-based reconstruction helpers + gap text
# For the executable Algorithm-1-shaped loop see step_extractor.py, segmentation.py, schema.py
# and README_RECONSTRUCTION.md. This module retains neutral adapters and audit strings.

"""
Paper reference: Appendix A, ``CPFC StepExtractor (Verifier-Driven Segmentation)''.

This module keeps **gap text** and **normalization helpers**. The executable
Algorithm-1-shaped loop is in ``step_extractor.py`` / ``segmentation.py`` (PBR).

The source-backed empirical path remains LLM clause-wise SQL in ``aliyun_api.py``.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def implementation_gap_summary() -> str:
    return (
        "Formal StepExtractor (Algorithm 1): buffer size W, StructureParse, "
        "Verifier-gated boundaries, JSON with proposition/parent_refs/step_id.\n"
        "This repository: AliyunLLMAPI.generate_step_by_step → list of "
        "{step, partial_sql, candidates} per SQL-clause phase; consumed by "
        "pipeline.experiment_pipeline.ExperimentPipeline."
    )


def normalize_reasoning_step(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map one record from generate_step_by_step to a paper-neutral step dict.

    Fields are NOT equivalent to Appendix A JSON; names are chosen for traceability only.
    """
    step = int(record.get("step", -1))
    partial = record.get("partial_sql", "")
    n_cand = len(record.get("candidates") or [])
    return {
        "step_index": step,
        "partial_sql": partial,
        "n_candidates": n_cand,
        "appendix_algorithm1_equivalent": False,
        "notes": "LLM clause-wise SQL fragment; not character-buffer StepExtractor.",
    }


def chain_to_neutral_steps(chain: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [normalize_reasoning_step(r) for r in chain]
