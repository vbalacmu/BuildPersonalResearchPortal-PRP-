## Personal Research Portal

This `repo/` directory contains the code, data manifest, evaluation scripts, reports, and artifacts for the Personal Research Portal (PRP). It bundles:

- The Phase 2 ingestion pipeline and RAG system (under `src/ingest` and `src/rag`)
- The Phase 3 portal UI implemented in Streamlit (under `src/app`)
- Evaluation scripts, query set, and results (under `src/eval`)
- Generated research artifacts, run logs, and written reports

### Layout

```text
repo/
  README.md
  requirements.txt
  data/
    raw/              # downloaded PDFs / snapshots
    processed/        # parsed text, chunks, FAISS index
    data_manifest.csv # metadata for every source
  src/
    app/              # Phase 3 UI (Streamlit)
    ingest/           # parsers + chunking + optional download scripts
    rag/              # retrieval + generation
    eval/             # query sets, scripts, results
  outputs/            # artifacts, exports (filled by the app)
  logs/               # runs, prompts, research threads
  report/             # Phase 1–3 writeups + AI usage log
```

### Setup

```bash
cd final_repo/repo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Prerequisites:
- Python 3.10+ recommended
- Ollama running locally with the `llama3.2` model pulled:

```bash
ollama serve           # in another terminal
ollama pull llama3.2   # one-time
```

### 1. Ingest + Index (Phase 2)

Rebuild processed text, chunks, and the FAISS index from `data/raw/`:

```bash
cd final_repo/repo
python -m src.ingest.run_ingest
python -m src.rag.retrieve  # first call will build the FAISS index
```

After this, `data/processed/chunks.json` and `data/processed/faiss.index` are ready.

### 2. Run the Portal UI (Phase 3)

Launch the Streamlit portal:

```bash
cd final_repo/repo
streamlit run src/app/main.py
```

Portal capabilities:
- Ask/search questions over the corpus
- View retrieved evidence and citation-backed answers
- Save research threads (query + evidence + answer)
- Generate and export research artifacts (evidence tables, memos)
- View evaluation metrics and representative examples

### 3. Run Evaluation (20-query set)

To re-run the Phase 2 evaluation over the 20-query set:

```bash
cd final_repo/repo
python -m src.eval.run_eval
```

This writes `src/eval/phase2_eval_results.json` and prints aggregate metrics for:
- `citation_precision`
- `answer_relevance`

### 4. Reports and AI Usage Log

The `report/` folder in this directory contains:

- **Phase 1 (deliverables):** exported PDFs for the framing brief, prompt kit, evaluation sheet, and analysis memo (see `report/phase1_*.pdf`). For convenience, the Phase 1 source documents and additional PDFs used during Phase 1 live in `report/phase1_pdfs/`.
- **Phase 2:** `phase2_evaluation_report.md` — corpus description, chunking and retrieval design, metrics, results, and failure cases.
- **Phase 3:** `phase3_final_report_template.md` — final report describing the portal architecture, functionality, evaluation, limitations, and reproducibility.
- **AI usage log:** `AI_USAGE_LOG.md` — summary of AI tools used, what they were used for, and what was edited or verified manually.
