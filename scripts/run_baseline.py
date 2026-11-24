"""Train the dictionary baseline (B0) on SkillSpan train and score it on dev.

Usage:  python scripts/run_baseline.py            (dev split, used for tuning)
        python scripts/run_baseline.py --split test   (only once, for the final table)
Writes: reports/baseline_<split>.md
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from skilllens.data import load_skillspan  # noqa: E402
from skilllens.evaluate import evaluate  # noqa: E402
from skilllens.extract.dictionary import DictionaryExtractor  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="dev", choices=["dev", "test"])
    args = ap.parse_args()

    train = load_skillspan("train")
    target = load_skillspan(args.split)
    golds = [s.gold for s in target]

    lines = [f"# Dictionary baseline (B0) on SkillSpan {args.split}", "",
             "Lexicon built from the train split only. Scores are span-level.", ""]

    # 1) tune the one setting on dev
    print("Tuning min_precision on dev ...")
    tuning = []
    for mp in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8):
        model = DictionaryExtractor(min_precision=mp).fit(train)
        r = evaluate([model.extract(s.tokens) for s in load_skillspan("dev")], [s.gold for s in load_skillspan("dev")])
        tuning.append((mp, len(model.lexicon), r["strict"]["overall"]["f1"]))
        print(f"  min_precision={mp:.1f}  lexicon={len(model.lexicon):5d}  strict F1={r['strict']['overall']['f1']:.3f}")
    best_mp = max(tuning, key=lambda t: t[2])[0]
    lines += ["## Tuning on dev", "", "| min_precision | Lexicon size | Strict F1 (dev) |", "| --- | --- | --- |"]
    lines += [f"| {mp:.1f} | {n:,} | {f:.3f} |" for mp, n, f in tuning]
    lines += ["", f"Chosen: min_precision = {best_mp:.1f}", ""]

    # 2) score the chosen setting on the requested split
    model = DictionaryExtractor(min_precision=best_mp).fit(train)
    res = evaluate([model.extract(s.tokens) for s in target], golds)
    lines += [f"## Results on {args.split}", "",
              "| Mode | Label | Precision | Recall | F1 | Predicted | Gold |",
              "| --- | --- | --- | --- | --- | --- | --- |"]
    for mode in ("strict", "partial"):
        for label in ("Skill", "Knowledge", "overall"):
            m = res[mode][label]
            lines.append(f"| {mode} | {label} | {m['precision']:.3f} | {m['recall']:.3f} | {m['f1']:.3f} | {m['pred']:,} | {m['gold']:,} |")
    out = ROOT / "reports" / f"baseline_{args.split}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[-9:]))
    print(f"\nSaved {out}")


if __name__ == "__main__":
    main()
