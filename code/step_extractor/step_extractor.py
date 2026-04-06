"""
VerifierDrivenStepExtractor — paper-driven executable reconstruction of Appendix A Algorithm 1.

Classification: paper-based reconstruction. Behavior follows the published control flow
(buffer size W, StructureParse, Verifier gate, accept / unverifiable) with a minimal
StructureParse. It does not claim byte-for-byte equivalence to any lost production code.
"""

from __future__ import annotations

from typing import Callable, List, Optional

from .schema import ParseStatus, RuleLibrary, StepObject
from .segmentation import structure_parse, template_step_json


VerifierFn = Callable[[StepObject, List[StepObject]], Optional[str]]
# Return None => accept; return str => reject / unverifiable reason


class VerifierDrivenStepExtractor:
    """
    CPFC StepExtractor (Verifier-Driven Segmentation) — minimal executable core.

    Feed characters from Y_{0:t-1}; when |B| == W, run StructureParse; on COMPLETE,
    build step JSON and call Verifier; accept clears buffer, else mark unverifiable.
    """

    def __init__(
        self,
        buffer_size: int = 128,
        rule_library: Optional[RuleLibrary] = None,
        verifier: Optional[VerifierFn] = None,
    ) -> None:
        self.W = max(8, int(buffer_size))
        self.R = rule_library or RuleLibrary()
        self.verifier = verifier
        self._buffer: List[str] = []
        self._accepted: List[StepObject] = []
        self._t = 0

    @property
    def history(self) -> List[StepObject]:
        return list(self._accepted)

    def reset(self) -> None:
        self._buffer.clear()
        self._accepted.clear()
        self._t = 0

    def feed(self, char: str) -> List[StepObject]:
        """Process one character; return list of newly accepted steps (0 or 1)."""

        newly: List[StepObject] = []
        self._buffer.append(char)
        if len(self._buffer) < self.W:
            return newly

        pr = structure_parse(self._buffer, self.R)
        if pr.status == ParseStatus.ERROR:
            self._buffer.clear()
            return newly

        if pr.status != ParseStatus.COMPLETE:
            return newly

        prop, parents = template_step_json(self._buffer, [s.step_id for s in self._accepted])
        self._t += 1
        sid = f"s{self._t}"
        step = StepObject(
            step_id=sid,
            proposition=prop,
            parent_refs=parents,
            meta={"structure_parse_detail": pr.detail},
        )

        if self.verifier is None:
            self._accepted.append(step)
            newly.append(step)
            self._buffer.clear()
            return newly

        verdict = self.verifier(step, self._accepted)
        if verdict is None:
            self._accepted.append(step)
            newly.append(step)
        else:
            step.meta["unverifiable_reason"] = verdict
        self._buffer.clear()
        return newly

    def feed_text(self, text: str) -> List[StepObject]:
        """Convenience: feed full stream; flush tail if COMPLETE (shorter than W)."""

        out: List[StepObject] = []
        for c in text:
            out.extend(self.feed(c))
        if self._buffer:
            pr = structure_parse(self._buffer, self.R)
            if pr.status == ParseStatus.ERROR:
                self._buffer.clear()
                return out
            if pr.status == ParseStatus.COMPLETE:
                prop, parents = template_step_json(self._buffer, [s.step_id for s in self._accepted])
                self._t += 1
                sid = f"s{self._t}"
                step = StepObject(
                    step_id=sid,
                    proposition=prop,
                    parent_refs=parents,
                    meta={"structure_parse_detail": pr.detail, "flush": "tail"},
                )
                if self.verifier is None:
                    self._accepted.append(step)
                    out.append(step)
                else:
                    verdict = self.verifier(step, self._accepted)
                    if verdict is None:
                        self._accepted.append(step)
                        out.append(step)
                    else:
                        step.meta["unverifiable_reason"] = verdict
                self._buffer.clear()
        return out


def demo_run(sql_fragment_stream: str) -> List[StepObject]:
    """Small built-in demo for reviewers (no external I/O)."""

    ex = VerifierDrivenStepExtractor(buffer_size=64)
    return ex.feed_text(sql_fragment_stream)
