from skilllens.data import Sentence
from skilllens.extract.dictionary import DictionaryExtractor
from skilllens.schemas import Span


def test_learns_and_finds_longest_phrase():
    train = [
        Sentence(["Experience", "with", "machine", "learning"], [Span(2, 4, "Knowledge")], "tech"),
        Sentence(["We", "use", "Python"], [Span(2, 3, "Knowledge")], "tech"),
    ]
    model = DictionaryExtractor(min_precision=0.5).fit(train)
    spans = model.extract(["Python", "and", "Machine", "Learning", "skills"])
    assert spans == [Span(0, 1, "Knowledge"), Span(2, 4, "Knowledge")]


def test_drops_phrases_usually_not_labelled():
    train = [
        Sentence(["team", "player"], [Span(0, 1, "Skill")], "house"),
        Sentence(["our", "team", "is", "great"], [], "house"),
        Sentence(["the", "team", "grows"], [], "house"),
    ]
    model = DictionaryExtractor(min_precision=0.5).fit(train)
    assert ("team",) not in model.lexicon
