"""Turn BIO tags into labelled spans (used for data exploration now, evaluation later)."""
from __future__ import annotations


def bio_to_spans(tags: list[str], label: str) -> list[tuple[int, int, str]]:
    """Return (start, end_exclusive, label) for each B-/I- run in a BIO tag list.

    An I- tag that does not follow a B- or I- tag starts a new span (common in real data).
    """
    spans: list[tuple[int, int, str]] = []
    start = None
    for i, tag in enumerate(tags):
        if tag.startswith("B") or (tag.startswith("I") and start is None):
            if start is not None:
                spans.append((start, i, label))
            start = i
        elif tag.startswith("I"):
            continue
        else:  # "O"
            if start is not None:
                spans.append((start, i, label))
                start = None
    if start is not None:
        spans.append((start, len(tags), label))
    return spans
