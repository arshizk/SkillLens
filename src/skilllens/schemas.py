"""Shared data types. Every extraction model returns a list of Span objects."""
from __future__ import annotations

from dataclasses import dataclass

LABELS = ("Skill", "Knowledge")


@dataclass(frozen=True)
class Span:
    """A labelled phrase in a tokenised sentence. `end` is exclusive."""

    start: int
    end: int
    label: str  # "Skill" or "Knowledge"

    def __len__(self) -> int:
        return self.end - self.start
