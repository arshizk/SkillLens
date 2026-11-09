"""Download the public SkillSpan JSON files (MIT licence) into data/raw/skillspan/.

Usage:  python scripts/download_skillspan.py
"""
from pathlib import Path
import urllib.request

BASE = "https://raw.githubusercontent.com/kris927b/SkillSpan/main/data/json/"
OUT = Path(__file__).resolve().parents[1] / "data" / "raw" / "skillspan"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for split in ("train", "dev", "test"):
        target = OUT / f"{split}.json"
        print(f"Downloading {split}.json ...")
        urllib.request.urlretrieve(BASE + f"{split}.json", target)
        print(f"  saved {target} ({target.stat().st_size / 1e6:.1f} MB)")
    print("Done.")


if __name__ == "__main__":
    main()
