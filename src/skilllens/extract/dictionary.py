"""B0 baseline: a dictionary (gazetteer) of phrases seen as skills in the training data.

fit()     collects every gold phrase from the training split, then keeps a phrase
          only if, in training, it was labelled at least `min_precision` of the times
          it appeared at all (this drops phrases like "team" that are usually not a skill).
extract() scans a sentence left to right and takes the longest known phrase at each position.
"""
from __future__ import annotations

from collections import Counter, defaultdict

from ..data import Sentence
from ..schemas import Span

MAX_LEN = 8


def _norm(tokens: list[str]) -> tuple[str, ...]:
    return tuple(t.lower() for t in tokens)


class DictionaryExtractor:
    def __init__(self, min_precision: float = 0.5, min_count: int = 1):
        self.min_precision = min_precision
        self.min_count = min_count
        self.lexicon: dict[tuple[str, ...], str] = {}

    def fit(self, sentences: list[Sentence]) -> "DictionaryExtractor":
        as_label: dict[tuple[str, ...], Counter] = defaultdict(Counter)
        for s in sentences:
            for sp in s.gold:
                if len(sp) <= MAX_LEN:
                    as_label[_norm(s.tokens[sp.start:sp.end])][sp.label] += 1
        # how often each candidate phrase occurs anywhere in the training text
        seen = Counter()
        lengths = {len(p) for p in as_label}
        for s in sentences:
            toks = _norm(s.tokens)
            for n in lengths:
                for i in range(len(toks) - n + 1):
                    phrase = toks[i:i + n]
                    if phrase in as_label:
                        seen[phrase] += 1
        self.lexicon = {}
        for phrase, labels in as_label.items():
            label, n_lab = labels.most_common(1)[0]
            total = sum(labels.values())
            if total >= self.min_count and total / max(seen[phrase], total) >= self.min_precision:
                self.lexicon[phrase] = label
        return self

    def extract(self, tokens: list[str]) -> list[Span]:
        toks = _norm(tokens)
        spans: list[Span] = []
        i = 0
        while i < len(toks):
            for n in range(min(MAX_LEN, len(toks) - i), 0, -1):
                label = self.lexicon.get(toks[i:i + n])
                if label:
                    spans.append(Span(i, i + n, label))
                    i += n
                    break
            else:
                i += 1
        return spans
