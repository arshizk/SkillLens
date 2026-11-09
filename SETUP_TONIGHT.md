# Tonight's steps (about 1 hour)

## 1. Put this into your repo (Arshi, ~15 min)
1. Copy everything in this folder into your local clone of github.com/arshizk/SkillLens
   (keep your existing README.md and LICENSE).
2. In a terminal inside the repo:
       python -m venv .venv
       source .venv/bin/activate        # Windows: .venv\Scripts\activate
       pip install -r requirements.txt

## 2. Get the data and look at it (Arshi, ~15 min)
       python scripts/download_skillspan.py
       python scripts/eda_skillspan.py
   This prints a table and writes reports/eda_skillspan.md and reports/eda_span_lengths.png.
   Read the numbers: you will be asked about them.

## 3. Run the tests (~2 min)
       pytest
   Three tests should pass.

## 4. Commit and push
       git add .
       git commit -m "Add project skeleton, SkillSpan download and first data exploration"
       git push
   data/ and .env are git-ignored on purpose: datasets and keys never go to GitHub.

## 5. Yashwanth, in parallel (~30 min)
- Request a USAJOBS API key at https://developer.usajobs.gov (it arrives by email).
  Copy .env.example to .env and put the key there. Never commit .env.
- Create a GitHub Projects board (Projects -> New project -> Board) with columns
  To do / In progress / Done, and add the Sprint 1 and Sprint 2 tasks as issues.
