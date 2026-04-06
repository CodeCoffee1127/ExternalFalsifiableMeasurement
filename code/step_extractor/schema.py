"""
Paper-driven data structures for Appendix A Algorithm 1 (CPFC StepExtractor).

Classification: paper-based reconstruction — JSON field names mirror the paper;
semantics are enforced only to the extent documented in README_RECONSTRUCTION.md.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class ParseStatus(str, Enum):
    """StructureParse outcome (paper Algorithm 1)."""

    INCOMPLETE = "incomplete"
    COMPLETE = "complete"
    ERROR = "error"


@dataclass
class ParseResult:
    """Result of StructureParse(B, R) in Appendix A."""

    status: ParseStatus
    detail: str = ""


@dataclass
class StepObject:
    """
    One accepted CPFC step s_t after Verifier gate (paper JSON sketch).

    Fields:
      proposition: surface string compiled from buffer (e.g., SQL fragment)
      parent_refs: directed dependency ids (paper parent_refs)
      step_id: unique id in trajectory
    """

    step_id: str
    proposition: str
    parent_refs: List[str] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_json_dict(self) -> Dict[str, Any]:
        return {
            "step_id": self.step_id,
            "proposition": self.proposition,
            "parent_refs": list(self.parent_refs),
            **{k: v for k, v in self.meta.items()},
        }


@dataclass
class RuleLibrary:
    """
    Placeholder for rule library R in Appendix A.

    Reconstruction: empty by default; callers may attach dialect flags or regex hints.
    """

    tags: Dict[str, Any] = field(default_factory=dict)
