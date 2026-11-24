from skilllens.evaluate import evaluate
from skilllens.schemas import Span


def test_perfect_match():
    gold = [[Span(0, 2, "Skill"), Span(4, 5, "Knowledge")]]
    r = evaluate(gold, gold)
    assert r["strict"]["overall"]["f1"] == 1.0


def test_boundary_error_counts_only_in_partial():
    gold = [[Span(0, 4, "Skill")]]
    pred = [[Span(0, 2, "Skill")]]
    r = evaluate(pred, gold)
    assert r["strict"]["Skill"]["f1"] == 0.0
    assert r["partial"]["Skill"]["f1"] == 1.0


def test_wrong_label_is_an_error():
    r = evaluate([[Span(0, 1, "Skill")]], [[Span(0, 1, "Knowledge")]])
    assert r["partial"]["overall"]["f1"] == 0.0


def test_precision_and_recall():
    gold = [[Span(0, 1, "Knowledge"), Span(3, 4, "Knowledge")]]
    pred = [[Span(0, 1, "Knowledge"), Span(6, 7, "Knowledge"), Span(8, 9, "Knowledge")]]
    m = evaluate(pred, gold)["strict"]["Knowledge"]
    assert (m["tp"], m["pred"], m["gold"]) == (1, 3, 2)
    assert abs(m["precision"] - 1 / 3) < 1e-9 and m["recall"] == 0.5
