"""
Bridge: implicit LLM clause-wise SQL chain -> StepObject list (linear parent_refs).

Classification: paper-aligned reconstruction for traceability — maps the
source-backed ``generate_step_by_step`` record shape to Appendix A-style JSON fields
without claiming Algorithm 1 equivalence.
"""

from __future__ import annotations

from typing import Any, Dict, List

from .schema import StepObject


def clause_records_to_step_objects(records: List[Dict[str, Any]]) -> List[StepObject]:
    """
    Convert a list of {step, partial_sql, candidates?} dicts to StepObject trajectory.

    step_id pattern: ``sql_clause_k``; parent_refs chain linearly to previous step.
    """
    out: List[StepObject] = []
    for i, r in enumerate(records):
        k = i + 1
        sid = f"sql_clause_{k}"
        partial = str(r.get("partial_sql", ""))
        parents = [out[-1].step_id] if out else []
        out.append(
            StepObject(
                step_id=sid,
                proposition=partial,
                parent_refs=parents,
                meta={
                    "n_candidates": len(r.get("candidates") or []),
                    "source": "llm_clause_chain_bridge",
                    "appendix_algorithm1_equivalent": False,
                },
            )
        )
    return out
