"""Clean every downloaded USAJOBS page into one file of unique postings.

Usage:  python scripts/clean_usajobs.py
Reads:  data/raw/usajobs/*/page_*.json
Writes: data/processed/usajobs_postings.jsonl and reports/usajobs_summary.md
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from skilllens.usajobs import parse_item  # noqa: E402


def main() -> None:
    pages = sorted((ROOT / "data" / "raw" / "usajobs").glob("*/page_*.json"))
    if not pages:
        raise SystemExit("No raw pages found. Run scripts/collect_usajobs.py first.")
    records: dict[str, dict] = {}
    raw_count = 0
    seen_texts: set[str] = set()
    near_dupes = 0
    for p in pages:  # newest download wins for the same announcement
        for item in json.loads(p.read_text(encoding="utf-8"))["SearchResult"]["SearchResultItems"]:
            raw_count += 1
            rec = parse_item(item)
            if rec["usajobs_id"]:
                records[rec["usajobs_id"]] = rec
    unique = []
    for rec in records.values():
        key = rec["text"][:2000].lower()
        if not rec["sentences"]:
            continue
        if key in seen_texts:  # same text re-posted under a new ID
            near_dupes += 1
            continue
        seen_texts.add(key)
        unique.append(rec)
    out = ROOT / "data" / "processed" / "usajobs_postings.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        for rec in unique:
            f.write(json.dumps(rec) + "\n")
    series = Counter(f"{r['job_series']} {r['job_series_name']}".strip() for r in unique)
    n_sent = sum(len(r["sentences"]) for r in unique)
    lines = ["# USAJOBS collection summary", "",
             f"- Raw postings downloaded: {raw_count:,}",
             f"- Unique announcements: {len(records):,}",
             f"- Removed as duplicate text or empty: {len(records) - len(unique):,}",
             f"- Postings kept: {len(unique):,} with {n_sent:,} sentences "
             f"(average {n_sent / max(len(unique), 1):.1f} per posting)", "",
             "| Job series | Postings |", "| --- | --- |"]
    lines += [f"| {s} | {c:,} |" for s, c in series.most_common()]
    rep = ROOT / "reports" / "usajobs_summary.md"
    rep.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nSaved {out} and {rep}")


if __name__ == "__main__":
    main()
