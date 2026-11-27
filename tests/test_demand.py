from skilllens.demand import GROUPS, posting_skills, series_group, share_ci, top_skills, unlinked_phrases


def _p(series, spans):
    return {"job_series": series, "spans": spans}


def _s(label, esco, score, norm="x"):
    return {"label": label, "text": norm, "norm": norm, "esco_label": esco, "score": score}


POSTINGS = [
    _p("2210", [_s("Skill", "manage projects", 0.9), _s("Skill", "manage projects", 0.8), _s("Knowledge", "Python", 0.95)]),
    _p("1560", [_s("Knowledge", "Python", 0.9), _s("Skill", "analyse data", 0.7)]),
    _p("0801", [_s("Skill", "analyse data", 0.3, norm="crunch numbers")]),
]


def test_series_group():
    assert series_group("2210") == GROUPS[0]
    assert series_group("1560") == GROUPS[1]
    assert series_group("0801") == GROUPS[2] and series_group("") == GROUPS[2]


def test_posting_skills_uses_threshold_and_label():
    assert posting_skills(POSTINGS[2], 0.6) == set()
    assert posting_skills(POSTINGS[0], 0.6, "Knowledge") == {"Python"}


def test_top_skills_counts_each_posting_once():
    top = top_skills(POSTINGS, 0.6)
    assert top[0]["skill"] == "Python" and top[0]["postings"] == 2
    assert {r["skill"]: r["postings"] for r in top}["manage projects"] == 1
    assert abs(top[0]["share"] - 2 / 3) < 1e-9


def test_unlinked_and_ci():
    assert unlinked_phrases(POSTINGS, 0.6)["crunch numbers"] == 1
    lo, hi = share_ci([1, 0, 1, 1, 0, 1, 1, 0, 1, 1])
    assert 0 <= lo <= 0.7 <= hi <= 1
