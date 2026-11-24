# SkillLens: fresh start, step by step

Do the stages **in order**. Each one says what it is for, what to type, and what you
should see. Type commands **one line at a time** and press Enter after each.
After every stage, message Claude with a screenshot of the result before moving on.

**Your GitHub repo stays** (github.com/arshizk/SkillLens). Its history shows the
professor that work happened over time, so we never delete it. We only replace the
folder on your laptop.

---

## Stage 0: clean slate (10 min)

**Why:** your laptop folder has a mix of old files. We throw it away and get a clean copy.

1. Close VS Code and every terminal.
2. Open File Explorer, go to `Documents`, and **delete the `SkillLens` folder**.
3. Open the Start menu, type `cmd` and open **Command Prompt**. Then type:

```
cd %USERPROFILE%\Documents
git clone https://github.com/arshizk/SkillLens.git
```

You now have a fresh `Documents\SkillLens` folder holding what is on GitHub.

4. Unzip `SkillLens_fresh_start.zip`. Open the `SkillLens` folder inside it, select
   everything (Ctrl+A), copy it (Ctrl+C), go to `Documents\SkillLens` and paste (Ctrl+V).
   If Windows asks, choose **Replace the files in the destination**.

---

## Stage 1: Python setup (10 min)

**Why:** a *virtual environment* (`venv`) is a private box of Python libraries for this
project only, so nothing clashes with other projects.

In Command Prompt:

```
cd %USERPROFILE%\Documents\SkillLens
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**You should see:** `(venv)` at the start of the line, and pip ending with
`Successfully installed ...`.

> Every time you open a new Command Prompt later, run the `cd ...` line and the
> `venv\Scripts\activate` line first.

---

## Stage 2: get the data and look at it (10 min)

**Why:** SkillSpan is a public dataset of job-posting sentences where people marked
which words are a **Skill** ("manage a team") or **Knowledge** ("Python"). We use it to
train and score our models.

```
python scripts/download_skillspan.py
python scripts/eda_skillspan.py
```

**You should see:** three files downloaded, then a table of counts. Two new files appear:
`reports/eda_skillspan.md` and `reports/eda_span_lengths.png`. Open the picture: most
skills are 1–4 words long, but some are much longer.

---

## Stage 3: run the tests (2 min)

**Why:** tests are small automatic checks that our code does what we expect. If they
pass, the building blocks work.

```
python -m pytest
```

**You should see:** `12 passed`.

---

## Stage 4: the baseline model (5 min)

**Why:** before training a smart model we need a *simple* one to beat. Ours is a
dictionary: it learns phrases that were marked as skills in the training data and
looks for them in new sentences.

```
python scripts/run_baseline.py
```

**You should see:** a results table, and `reports/baseline_dev.md` is created.
The key number is **strict overall F1 ≈ 0.308**.

What it means:
- **Precision**: of the skills we found, how many were right.
- **Recall**: of the real skills, how many we found.
- **F1**: one score combining both (0 = useless, 1 = perfect).
- **Strict**: the exact same words must be marked. **Partial**: overlapping is enough.

So the dictionary gets roughly a third right exactly. BERT should do clearly better.

---

## Stage 5: save to GitHub (5 min)

**Why:** pushing puts your work online, so Yashwanth and the professor can see it.

```
git add .
git status
git commit -m "Fresh setup: data loading, evaluation, dictionary baseline, USAJOBS collector, BERT notebook"
git push
```

`git status` lists what will be uploaded. You should **not** see `data/raw` or `.env`
in that list (`.gitignore` keeps them out).

Also add Yashwanth on GitHub: repo page, then **Settings**, **Collaborators**,
**Add people**, and enter his GitHub username.

---

## Stage 6: train BERT on Google Colab (about 1 hour, mostly waiting)

**Why:** BERT is a language model that understands context, so it can spot skills the
dictionary never saw. Training needs a GPU, which Colab gives free.

1. Open colab.research.google.com, choose **Upload**, and pick `notebooks/train_bert_colab.ipynb`.
2. Menu **Runtime**, **Change runtime type**, **T4 GPU**, **Save**.
3. Menu **Runtime**, **Run all**. Keep the tab open for about 15–25 minutes.
4. A results table prints (BERT vs the 0.308 baseline) and a `.json` file downloads.
   Screenshot the table.
5. In the first code cell change `MODEL_NAME` to `"jjzha/jobspanbert-base-cased"`
   and do **Run all** again.
6. Put both `.json` files into `Documents\SkillLens\reports`, then:

```
git add reports
git commit -m "BERT and JobSpanBERT results on SkillSpan dev"
git push
```

---

## Stage 7 (Yashwanth): real job postings from USAJOBS

**Why:** SkillSpan trains the model; USAJOBS gives us *current* US government
data/IT job postings to run it on, which is the point of the project.

1. Clone the repo (after Arshi adds him):

```
cd %USERPROFILE%\Documents
git clone https://github.com/arshizk/SkillLens.git
cd SkillLens
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. Copy `.env.example`, rename the copy to `.env`, open it in Notepad and fill in the
   API key and the registered email. **Never upload `.env`.**
3. Run:

```
python scripts/collect_usajobs.py
python scripts/clean_usajobs.py
```

The first downloads the postings. The second removes HTML, emails, phone numbers and
links, then writes `data/processed/usajobs_postings.jsonl` and
`reports/usajobs_summary.md`.
4. Read 10 postings by eye and write anything odd under "Data quality notes" in the summary.
5. Push:

```
git pull
git add .
git commit -m "USAJOBS collector, cleaner and summary"
git push
```

---

## What each folder is for

| Folder | What lives there |
| --- | --- |
| `src/skilllens/` | The real code: loading data, turning tags into spans, scoring, the dictionary model, USAJOBS cleaning |
| `scripts/` | Small programs you run: download, explore, baseline, collect, clean |
| `tests/` | Automatic checks for the code in `src/` |
| `notebooks/` | The Colab notebook for BERT training |
| `reports/` | Results and summaries that go into the progress reports |
| `data/` | Downloaded data. Stays on your laptop only, never on GitHub |
| `configs/`, `annotations/`, `dashboard/` | Empty for now; used in Sprint 4 |

## Target for 6 Dec (core MVP)

Baseline and BERT/JobSpanBERT results compared, a cleaned USAJOBS collection, and the
best model run over it to give a first table of extracted skills. The dashboard, the
LLM comparison and our own labelled postings come in Sprint 4.
