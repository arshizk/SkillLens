"""Skill-demand report from the Colab extraction output.

Usage:  python scripts/skill_demand.py
Reads:  data/processed/usajobs_extracted.jsonl (+ reports/extraction_run.json for the threshold)
Writes: reports/skill_demand.md and reports/skill_demand_top.png
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from skilllens.demand import GROUPS, series_group, top_skills, unlinked_phrases  # noqa: E402


def table(rows: list[dict], ci: bool = False) -> list[str]:
    head = "| # | ESCO skill | Postings | Share |" + (" 95% interval |" if ci else "")
    lines = [head, "| --- | --- | --- | --- |" + (" --- |" if ci else "")]
    for i, r in enumerate(rows, 1):
        line = f"| {i} | {r['skill']} | {r['postings']} | {r['share']:.0%} |"
        if ci:
            line += f" {r['ci'][0]:.0%} to {r['ci'][1]:.0%} |"
        lines.append(line)
    return lines


def main() -> None:
    src = ROOT / "data" / "processed" / "usajobs_extracted.jsonl"
    if not src.exists():
        raise SystemExit("Put usajobs_extracted.jsonl from Colab into data/processed/ first.")
    postings = [json.loads(l) for l in src.read_text(encoding="utf-8").splitlines() if l.strip()]
    meta_path = ROOT / "reports" / "extraction_run.json"
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
    tau = float(meta.get("tau", 0.6))

    spans = [s for p in postings for s in p.get("spans", [])]
    linked = sum(1 for s in spans if s.get("score", 0) >= tau)
    out = ["# Skill demand in US federal data and IT postings", "",
           f"- Postings: {len(postings):,}; extracted phrases: {len(spans):,} "
           f"({len(spans) / max(len(postings), 1):.1f} per posting)",
           f"- Linked to ESCO at cosine >= {tau}: {linked:,} ({linked / max(len(spans), 1):.0%})",
           f"- Model: {meta.get('model', '?')}; linker: {meta.get('embed_model', '?')}",
           "- Share = postings that mention the skill at least once.", ""]

    for label, title in (("Skill", "Top skills (things people do)"), ("Knowledge", "Top knowledge (things people know)")):
        out += [f"## {title}", ""] + table(top_skills(postings, tau, label, n=15)) + [""]

    out += ["## By job-series group", ""]
    for g in GROUPS:
        sub = [p for p in postings if series_group(p.get("job_series", "")) == g]
        if not sub:
            continue
        out += [f"### {g}: {len(sub)} postings", ""] + table(top_skills(sub, tau, n=10, with_ci=True), ci=True) + [""]

    out += ["## Most common phrases without an ESCO link", "",
            "These show where ESCO or the linker has gaps (often tool names or very specific duties).", ""]
    out += [f"- {phrase} ({k})" for phrase, k in unlinked_phrases(postings, tau).most_common(15)]

    rep = ROOT / "reports" / "skill_demand.md"
    rep.write_text("\n".join(out) + "\n", encoding="utf-8")

    top = top_skills(postings, tau, n=15)[::-1]
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh([r["skill"] for r in top], [r["share"] * 100 for r in top], color="#2563eb")
    for i, r in enumerate(top):
        ax.text(r["share"] * 100 + 0.5, i, f"{r['share']:.0%}", va="center", fontsize=9)
    ax.set_xlabel("Share of postings that mention it (%)")
    ax.set_title(f"Most requested ESCO skills in {len(postings)} US federal data/IT postings")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(ROOT / "reports" / "skill_demand_top.png", dpi=150)
    print("\n".join(out[:6]))
    print(f"Saved {rep} and reports/skill_demand_top.png")


if __name__ == "__main__":
    main()
