# SkillLens

**Comparing encoder fine-tuning and large language models for skill extraction and ESCO normalisation in job postings**

Data Science Capstone Project · Winter 2026/2027
**Team:** Arshi Zabeen Khan · Yashwanth Reddy Shyamakura
**Supervisor:** Dr. Humera Noor

![tests](https://github.com/arshizk/SkillLens/actions/workflows/tests.yml/badge.svg)

> **Status:** Sprint 3 (23 Nov – 6 Dec 2026). Baseline, BERT and JobSpanBERT compared on SkillSpan; 431 USAJOBS postings collected. Now: extraction on USAJOBS and ESCO linking (core MVP, 6 Dec).

## What this project does

Job postings describe required skills in free text. "ML", "machine-learning models" and "build predictive models in Python" can all mean the same skill, which makes skill demand hard to measure.

SkillLens will:

- **Extract** skill and knowledge mentions from English job postings.
- **Link** them to [ESCO](https://esco.ec.europa.eu/), the European Commission's skills taxonomy.
- **Show** skill demand across data and IT job families in an API and a dashboard.

The core question: which approach gives the best accuracy for its cost? We compare a simple dictionary baseline, fine-tuned BERT-style encoders and large language models.

## Research questions

| ID | Question |
| --- | --- |
| RQ1 | How do a dictionary baseline, fine-tuned BERT, a domain-adapted encoder (JobSpanBERT) and LLMs compare on span-level F1? |
| RQ2 | How well do models trained on one source generalise to job postings from other sources? |
| RQ3 | What are the latency and compute cost of each approach? |
| RQ4 | How accurately can extracted skills be linked to ESCO concepts? |
| RQ5 | What skill-demand differences appear across data and IT roles? |

## Data

Only real, publicly available data is used. No Kaggle or synthetic datasets. Datasets are **not** committed to this repository; scripts in `scripts/` download them.

| Dataset | Source | Use |
| --- | --- | --- |
| SkillSpan | Zhang et al., NAACL 2022 | Training and testing (expert-annotated) |
| Green et al. corpus | Green, Maynard & Lin, LREC 2022 | Second test set |
| ESCO v1.2 | European Commission | Skill taxonomy for linking |
| USAJOBS API | U.S. Office of Personnel Management | Current real postings: new test set, skill-demand analytics and demo |

## Progress

| Sprint | Dates | Done |
| --- | --- | --- |
| 0 | Oct 2026 | Proposal approved, repository and project plan set up |
| 1–2 | 26 Oct – 22 Nov | SkillSpan download and exploration ([report](reports/eda_skillspan.md)), span-level evaluation (strict and partial F1), dictionary baseline B0 ([results](reports/baseline_dev.md)), unit tests |
| 3 | 23 Nov – 6 Dec | BERT and JobSpanBERT fine-tuned on Colab ([B1](reports/results_bert-base-cased_dev.json), [M1](reports/results_jobspanbert-base-cased_dev.json)); USAJOBS collector and cleaner ([summary](reports/usajobs_summary.md)); in progress: extraction on USAJOBS, ESCO linking, first skill-demand table (core MVP) |

## Current results (SkillSpan dev set)

| Model | Strict F1: Skill | Strict F1: Knowledge | Strict F1: overall | Partial F1: overall |
| --- | --- | --- | --- | --- |
| B0 Dictionary baseline | 0.149 | 0.412 | **0.308** | 0.418 |
| B1 bert-base-cased | 0.481 | 0.579 | 0.531 | 0.735 |
| **M1 JobSpanBERT** | **0.520** | **0.588** | **0.554** | **0.757** |

Single run each (seed 42, 3 epochs). JobSpanBERT, pre-trained on job postings, is best and is used for the USAJOBS extraction.

The dictionary finds short knowledge terms ("python", "docker") reasonably well but finds under 10% of skills. Skills are longer (4.4 tokens on average vs 1.8 for knowledge) and phrased differently each time. This is the gap the fine-tuned encoders have to close.

## Approach

- **Baselines:** dictionary matching (B0), fine-tuned `bert-base-cased` (B1)
- **Models:** fine-tuned JobSpanBERT (M1), few-shot open-weight LLM (M2), optional QLoRA-fine-tuned small LLM (M3)
- **Linking:** sentence embeddings + FAISS nearest-neighbour search over ESCO skills
- **Evaluation:** strict and partial span F1, Recall@1/@5 for linking, inter-annotator agreement for our own labels

## How to run

```bash
git clone https://github.com/arshizk/SkillLens.git
cd SkillLens
python -m venv venv
venv\Scripts\activate            # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt

python scripts/download_skillspan.py   # get the data
python scripts/eda_skillspan.py        # data exploration -> reports/
python scripts/run_baseline.py         # dictionary baseline -> reports/baseline_dev.md
python -m pytest                       # unit tests
```

- **BERT training** runs on Google Colab: upload `notebooks/train_bert_colab.ipynb` and choose a T4 GPU runtime.
- **USAJOBS collection** needs a free API key in a local `.env` file (see `.env.example`), then `python scripts/collect_usajobs.py` and `python scripts/clean_usajobs.py`.
- Step-by-step setup for team members: [START_HERE.md](START_HERE.md).

## Repository structure

```
SkillLens/
├── src/skilllens/    package: data loading, spans, evaluation, extractors, USAJOBS cleaning
├── scripts/          download, exploration, baseline and USAJOBS collection scripts
├── tests/            unit tests (run automatically on every push)
├── notebooks/        Colab notebook for BERT / JobSpanBERT training
├── reports/          results and progress reports
├── configs/          experiment configuration files
├── annotations/      annotation guidelines and gold labels
├── dashboard/        Streamlit app (Sprint 4)
└── data/             local data only (git-ignored)
```

## Tech stack

Python · PyTorch · Hugging Face Transformers · sentence-transformers · FAISS · DuckDB · FastAPI · Streamlit · MLflow · pytest · GitHub Actions

## Licence

Code: MIT. Datasets keep their original licences.
