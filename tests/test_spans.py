from skilllens.spans import bio_to_spans


def test_simple_spans():
    tags = ["O", "B", "I", "O", "B", "O"]
    assert bio_to_spans(tags, "Skill") == [(1, 3, "Skill"), (4, 5, "Skill")]


def test_span_at_end_and_stray_i():
    tags = ["I", "I", "O", "B", "I"]
    assert bio_to_spans(tags, "Knowledge") == [(0, 2, "Knowledge"), (3, 5, "Knowledge")]


def test_no_spans():
    assert bio_to_spans(["O", "O"], "Skill") == []
