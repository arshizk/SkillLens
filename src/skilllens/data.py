"""Load SkillSpan sentences with their gold spans."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .schemas import Span
from .spans import bio_to_spans

DEFAULT_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "skillspan"


@dataclass
class Sentence:
    tokens: list[str]
    gold: list[Span]
    source: str


def load_skillspan(split: str, data_dir: Path = DEFAULT_DIR) -> list[Sentence]:
    """Read train/dev/test JSON lines and convert both tag columns to spans."""
    out: list[Sentence] = []
    with open(Path(data_dir) / f"{split}.json", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            d = json.loads(line)
            gold = [Span(a, b, "Skill") for a, b, _ in bio_to_spans(d["tags_skill"], "Skill")]
            gold += [Span(a, b, "Knowledge") for a, b, _ in bio_to_spans(d["tags_knowledge"], "Knowledge")]
            out.append(Sentence(tokens=d["tokens"], gold=gold, source=d["source"]))
    return out
