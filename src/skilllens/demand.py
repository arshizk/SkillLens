"""Skill demand from extracted, ESCO-linked USAJOBS postings.

Demand = the share of postings that mention a skill at least once, so one long
posting that repeats a skill counts once. Shares come with a bootstrap 95%
interval because some job-series groups are small.
"""
from __future__ import annotations

import random
from collections import Counter

DATA_SERIES = {"1515", "1530", "1550", "1560"}
GROUPS = ("IT Management (2210)", "Data & analytics (1515, 1530, 1550, 1560)", "Other series")


def series_group(code: str) -> str:
    code = (code or "").strip()
    if code == "2210":
        return GROUPS[0]
    if code in DATA_SERIES:
        return GROUPS[1]
    return GROUPS[2]


def posting_skills(posting: dict, tau: float, label: str | None = None) -> set[str]:
    """ESCO skills a posting mentions (links at or above tau), optionally one span label only."""
    return {
        s["esco_label"]
        for s in posting.get("spans", [])
        if s.get("score", 0) >= tau and s.get("esco_label") and (label is None or s.get("label") == label)
    }


def unlinked_phrases(postings: list[dict], tau: float) -> Counter:
    """Phrases the model found but could not link: shows gaps in ESCO or in the linker."""
    c: Counter = Counter()
    for p in postings:
        c.update({s.get("norm") or s["text"].lower() for s in p.get("spans", []) if s.get("score", 0) < tau})
    return c


def share_ci(hits: list[int], n_boot: int = 1000, seed: int = 0) -> tuple[float, float]:
    """Percentile bootstrap 95% interval for a share of 0/1 values."""
    if not hits:
        return 0.0, 0.0
    rng = random.Random(seed)
    n = len(hits)
    stats = sorted(sum(rng.choice(hits) for _ in range(n)) / n for _ in range(n_boot))
    return stats[int(0.025 * n_boot)], stats[int(0.975 * n_boot) - 1]


def top_skills(postings: list[dict], tau: float, label: str | None = None, n: int = 15,
               with_ci: bool = False) -> list[dict]:
    """The n ESCO skills mentioned by the most postings, with counts and shares."""
    sets = [posting_skills(p, tau, label) for p in postings]
    counts: Counter = Counter()
    for s in sets:
        counts.update(s)
    out = []
    for name, k in counts.most_common(n):
        row = {"skill": name, "postings": k, "share": k / len(postings) if postings else 0.0}
        if with_ci:
            row["ci"] = share_ci([int(name in s) for s in sets])
        out.append(row)
    return out
