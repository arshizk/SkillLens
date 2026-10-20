SkillLens
Comparing Encoder Fine-Tuning and Large Language Models for Skill Extraction and ESCO Normalisation in Job Postings
Data Science Capstone Project · Winter 2026/2027 Team: Arshi Zabeen Khan · Yashwanth Reddy Shyamakura Supervisor: Dr. Humera Noor
Status: Proposal stage (Sprint 0). Code development starts in Sprint 1 (26 October 2026). No results yet.

What this project does
Job postings describe required skills in free text. "ML", "machine-learning models" and "build predictive models in Python" can all mean the same skill, which makes skill demand hard to measure.

SkillLens will:
Extract skill and knowledge mentions from English job postings.
Link them to ESCO, the European Commission's skills taxonomy.
Show skill demand across data and IT job families in an API and a dashboard.

The core research question: which approach gives the best accuracy for its cost — a simple dictionary baseline, fine-tuned BERT-style encoders, or large language models?

Research questions
ID	Question
RQ1	How do a dictionary baseline, fine-tuned BERT, a domain-adapted encoder (JobSpanBERT) and LLMs compare on span-level F1?
RQ2	How well do models trained on one source generalise to job postings from other sources?
RQ3	What are the latency and compute cost of each approach?
RQ4	How accurately can extracted skills be linked to ESCO concepts?
RQ5	What skill-demand differences appear across data and IT roles?


Data

Only real, publicly available data is used. No Kaggle or synthetic datasets.
Dataset	Source	Use
SkillSpan	Zhang et al., NAACL 2022	Training and testing (expert-annotated)
Green et al. corpus	Green, Maynard & Lin, LREC 2022	Second test set
ESCO v1.2	European Commission	Skill taxonomy for linking
USAJOBS API	U.S. Office of Personnel Management	Real postings: new test set (annotated by both team members), analytics and demo


Datasets are not committed to this repository. They will be downloaded by scripts in scripts/.

Planned approach
Baselines: ESCO dictionary matching (B0), fine-tuned bert-base-cased (B1)
Models: fine-tuned JobSpanBERT (M1), few-shot open-weight LLM (M2), optional QLoRA-fine-tuned small LLM (M3)
Linking: sentence embeddings + FAISS nearest-neighbour search over ESCO skills
Evaluation: strict and partial span F1 (3 seeds, mean ± std), Recall@1/@5 for linking, inter-annotator agreement for our own labels

Repository structure
skilllens/
├── configs/          experiment configuration files
├── data/             local data only (git-ignored)
├── scripts/          dataset download and collection scripts
├── src/skilllens/    package: preprocessing, extraction, linking, evaluation, API
├── dashboard/        Streamlit app
├── notebooks/        exploratory analysis
├── annotations/      annotation guidelines and gold labels
├── reports/          progress reports and final report
└── tests/            unit and integration tests

Tech stack

Python · PyTorch · Hugging Face Transformers · PEFT · sentence-transformers · FAISS · DuckDB · FastAPI · Streamlit · MLflow · pytest · GitHub Actions
