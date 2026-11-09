"""First look at SkillSpan: sentences, spans and span lengths per split.

Usage:  python scripts/eda_skillspan.py
Writes: reports/eda_skillspan.md and reports/eda_span_lengths.png
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from skilllens.spans import bio_to_spans  # noqa: E402

DATA = ROOT / "data" / "raw" / "skillspan"
REPORTS = ROOT / "reports"


def load(split: str) -> list[dict]:
    with open(DATA / f"{split}.json", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def main() -> None:
    REPORTS.mkdir(exist_ok=True)
    rows, lengths, examples = [], {"Skill": [], "Knowledge": []}, Counter()
    for split in ("train", "dev", "test"):
        data = load(split)
        n_sent = len(data)
        n_post = len({(d["source"], d["idx"]) for d in data})
        n_tok = sum(len(d["tokens"]) for d in data)
        counts = Counter()
        with_span = 0
        sources = Counter(d["source"] for d in data)
        for d in data:
            s = bio_to_spans(d["tags_skill"], "Skill")
            k = bio_to_spans(d["tags_knowledge"], "Knowledge")
            if s or k:
                with_span += 1
            for a, b, lab in s + k:
                counts[lab] += 1
                lengths[lab].append(b - a)
                if split == "train" and lab == "Knowledge":
                    examples[" ".join(d["tokens"][a:b]).lower()] += 1
        rows.append((split, n_post, n_sent, n_tok, counts["Skill"], counts["Knowledge"],
                     100 * with_span / n_sent, dict(sources)))

    def avg(xs: list[int]) -> float:
        return sum(xs) / len(xs) if xs else 0.0

    lines = ["# SkillSpan: first data exploration", "",
             "| Split | Postings | Sentences | Tokens | Skill spans | Knowledge spans | Sentences with a span | Sources |",
             "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for split, p, n, t, s, k, pct, src in rows:
        lines.append(f"| {split} | {p:,} | {n:,} | {t:,} | {s:,} | {k:,} | {pct:.0f}% | {src} |")
    tot_s = sum(r[4] for r in rows)
    tot_k = sum(r[5] for r in rows)
    lines += ["", f"Total sentences: {sum(r[2] for r in rows):,}; total spans: {tot_s + tot_k:,} "
              f"({tot_s:,} skill, {tot_k:,} knowledge).",
              f"Average span length: skill {avg(lengths['Skill']):.1f} tokens, "
              f"knowledge {avg(lengths['Knowledge']):.1f} tokens.",
              "", "Most frequent knowledge spans in train:", ""]
    lines += [f"- {txt} ({c})" for txt, c in examples.most_common(10)]
    (REPORTS / "eda_skillspan.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    fig, ax = plt.subplots(figsize=(7, 3.5))
    bins = [x - 0.5 for x in range(1, 22)]
    ax.hist([[min(x, 20) for x in lengths["Skill"]], [min(x, 20) for x in lengths["Knowledge"]]],
            bins=bins, label=["Skill", "Knowledge"])
    ax.set_xticks(range(1, 21))
    ax.set_xlabel("Span length in tokens (20 = 20 or more)")
    ax.set_ylabel("Number of spans")
    ax.set_title("SkillSpan: skill spans are much longer than knowledge spans")
    ax.legend()
    fig.tight_layout()
    fig.savefig(REPORTS / "eda_span_lengths.png", dpi=150)
    print("\n".join(lines))
    print(f"\nSaved {REPORTS / 'eda_skillspan.md'} and {REPORTS / 'eda_span_lengths.png'}")


if __name__ == "__main__":
    main()
