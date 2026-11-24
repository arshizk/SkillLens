"""Span-level precision, recall and F1, strict and partial.

strict  : a prediction counts only if start, end and label all match a gold span.
partial : a prediction counts if it overlaps a gold span of the same label by at
          least one token (each gold span can be matched once).
"""
from __future__ import annotations

from collections import defaultdict

from .schemas import LABELS, Span


def _prf(tp: int, n_pred: int, n_gold: int) -> dict[str, float]:
    p = tp / n_pred if n_pred else 0.0
    r = tp / n_gold if n_gold else 0.0
    f = 2 * p * r / (p + r) if p + r else 0.0
    return {"precision": p, "recall": r, "f1": f, "tp": tp, "pred": n_pred, "gold": n_gold}


def _matches(pred: list[Span], gold: list[Span], mode: str) -> int:
    if mode == "strict":
        return len(set(pred) & set(gold))
    used: set[Span] = set()
    tp = 0
    for p in pred:
        for g in gold:
            if g not in used and g.label == p.label and p.start < g.end and g.start < p.end:
                used.add(g)
                tp += 1
                break
    return tp


def evaluate(predictions: list[list[Span]], golds: list[list[Span]]) -> dict[str, dict[str, dict[str, float]]]:
    """Return {mode: {label or 'overall': metrics}} for mode in strict/partial."""
    if len(predictions) != len(golds):
        raise ValueError("predictions and golds must have the same length")
    results: dict[str, dict[str, dict[str, float]]] = {}
    for mode in ("strict", "partial"):
        counts = defaultdict(lambda: [0, 0, 0])  # tp, pred, gold
        for pred, gold in zip(predictions, golds):
            for label in LABELS:
                p = [s for s in pred if s.label == label]
                g = [s for s in gold if s.label == label]
                c = counts[label]
                c[0] += _matches(p, g, mode)
                c[1] += len(p)
                c[2] += len(g)
        res = {label: _prf(*counts[label]) for label in LABELS}
        tot = [sum(counts[l][i] for l in LABELS) for i in range(3)]
        res["overall"] = _prf(*tot)
        results[mode] = res
    return results
