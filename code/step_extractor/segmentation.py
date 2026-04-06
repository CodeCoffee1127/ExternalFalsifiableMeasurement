"""
StructureParse(B, R) — paper-driven minimal implementation.

This is NOT a full SQL parser. It approximates "complete" when the buffer
contains a verifiable clause boundary so the StepExtractor can emit a step.
"""

from __future__ import annotations

from typing import List, Sequence

from .schema import ParseResult, ParseStatus, RuleLibrary


def _balanced_single_quotes(s: str) -> bool:
    """Return True if single quotes are balanced (odd count => inside string)."""

    n = 0
    i = 0
    while i < len(s):
        if s[i] == "'":
            n += 1
            if i + 1 < len(s) and s[i + 1] == "'":
                i += 2
                continue
        i += 1
    return n % 2 == 0


def structure_parse(
    buffer_chars: Sequence[str],
    rule_library: RuleLibrary | None = None,
) -> ParseResult:
    """
    Paper Algorithm 1: T_cand <- StructureParse(B, R).

    Reconstruction rules (deterministic, documented):
      - ERROR if buffer has unbalanced single quotes.
      - COMPLETE if trimmed buffer ends with ';' and length >= 8.
      - COMPLETE if buffer contains SELECT and FROM (case-insensitive) and length >= 12.
      - Otherwise INCOMPLETE.
    """
    _ = rule_library
    text = "".join(buffer_chars).strip()
    if not text:
        return ParseResult(ParseStatus.INCOMPLETE, "empty buffer")

    if not _balanced_single_quotes(text):
        return ParseResult(ParseStatus.ERROR, "unbalanced single quotes")

    if text.endswith(";") and len(text) >= 8:
        return ParseResult(ParseStatus.COMPLETE, "terminated by semicolon")

    low = text.lower()
    if "select" in low and "from" in low and len(text) >= 12:
        return ParseResult(ParseStatus.COMPLETE, "select/from skeleton")

    return ParseResult(ParseStatus.INCOMPLETE, "need more tokens")


def template_step_json(
    buffer_chars: Sequence[str],
    history_step_ids: List[str],
) -> tuple[str, List[str]]:
    """
    Paper: s_t <- Template(B, H_{t-1}) with proposition, parent_refs, step_id.

    Returns (proposition, parent_refs) before Verifier gate; step_id assigned by caller.
    """
    proposition = "".join(buffer_chars).strip()
    parents: List[str] = []
    if history_step_ids:
        parents = [history_step_ids[-1]]
    return proposition, parents
