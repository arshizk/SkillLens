"""Download current USAJOBS postings for data and IT job series.

Needs USAJOBS_API_KEY and USAJOBS_EMAIL in the .env file.
Usage:  python scripts/collect_usajobs.py
Writes: data/raw/usajobs/<today>/page_001.json, page_002.json, ...
"""
from __future__ import annotations

import json
import sys
import time
from datetime import date
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from skilllens.config import load_env, require  # noqa: E402

API = "https://data.usajobs.gov/api/search"
# OPM job series: 2210 IT Management, 1550 Computer Science, 1560 Data Science,
# 1530 Statistics, 1515 Operations Research
SERIES = "2210;1550;1560;1530;1515"
PER_PAGE = 500


def main() -> None:
    load_env()
    headers = {
        "Host": "data.usajobs.gov",
        "User-Agent": require("USAJOBS_EMAIL"),
        "Authorization-Key": require("USAJOBS_API_KEY"),
    }
    out = ROOT / "data" / "raw" / "usajobs" / date.today().isoformat()
    out.mkdir(parents=True, exist_ok=True)
    page, total, saved = 1, None, 0
    while True:
        params = {"JobCategoryCode": SERIES, "ResultsPerPage": PER_PAGE, "Page": page}
        for attempt in range(3):  # retry up to 3 times (NFR2)
            r = requests.get(API, headers=headers, params=params, timeout=60)
            if r.status_code == 200:
                break
            print(f"  page {page}: HTTP {r.status_code}, retrying ...")
            time.sleep(5 * (attempt + 1))
        else:
            raise SystemExit(f"USAJOBS kept failing on page {page}: HTTP {r.status_code} {r.text[:200]}")
        data = r.json()
        result = data.get("SearchResult", {})
        items = result.get("SearchResultItems", [])
        if total is None:
            total = int(result.get("SearchResultCountAll", 0))
            print(f"USAJOBS reports {total:,} matching postings")
        if not items:
            break
        (out / f"page_{page:03d}.json").write_text(json.dumps(data), encoding="utf-8")
        saved += len(items)
        print(f"  saved page {page}: {len(items)} postings ({saved:,} so far)")
        if saved >= total:
            break
        page += 1
        time.sleep(1)  # be polite to the API
    print(f"Done: {saved:,} postings in {out}")


if __name__ == "__main__":
    main()
