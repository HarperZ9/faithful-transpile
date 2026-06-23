"""Grounding check — the rigor-not-relativism guardrail against the over-build failure mode.

The live demonstration found that a reconciliation can ADD claims not supported by the subject
(it "over-builds" — completeness bought with invention). This penalizes the `grounded` dimension when
a candidate asserts tokens the subject's perceptible forms do not contain. Minimal + honest: it flags
unsupported salient tokens, not a semantic proof — a real witness does deeper, behind the same call.
"""
from __future__ import annotations
import re

_WORD = re.compile(r"[A-Za-z][A-Za-z0-9_-]{3,}")


def _salient(text: str) -> set[str]:
    return {w.lower() for w in _WORD.findall(text)}


def unsupported_tokens(candidate: str, subject_views: dict[str, str]) -> set[str]:
    """Salient tokens in the candidate not present in ANY of the subject's perceptible forms,
    minus the scaffolding words the minds add (channel/reconcile markers)."""
    corpus = _salient(" ".join(subject_views.values()))
    scaffold = {"text", "diagram", "from", "reconciled", "mine", "theirs", "this", "that",
                "with", "into", "toward", "telos", "proposal", "channel"}
    return {t for t in _salient(candidate) if t not in corpus and t not in scaffold}


def grounding_penalty(candidate: str, subject_views: dict[str, str]) -> float:
    """0.0 (fully grounded) → up to ~0.6 penalty as unsupported salient tokens accumulate.
    Subtract from the candidate's `grounded` score; record the offenders as evidence."""
    bad = unsupported_tokens(candidate, subject_views)
    return min(0.6, 0.15 * len(bad))
