## Personal Research Portal


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
- Ollama (optional): for LLM-backed answers, run `ollama serve` and `ollama pull llama3.2`. If Ollama is not running, use **Generation mode: template** in the portal for an extractive fallback (no LLM needed).

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

**Demo tip:** The first query may take 15–20 seconds while the embedding model loads. Use "template" mode for a quick demo without Ollama.

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

- **Phase 1** (`report/phase1/`): exported PDFs for the framing brief, prompt kit, evaluation sheet, and analysis memo.
- **Phase 2** (`report/phase2/`): `phase2_evaluation_report.md` — corpus description, chunking and retrieval design, metrics, results, and failure cases; `queries_phase2.md` — query set used for evaluation.
- **Phase 3** (`report/phase3/`): `phase3_final_report.md` — final report describing the portal architecture, functionality, evaluation, limitations, and reproducibility.
- **AI usage log** (`report/AI_USAGE_LOG.md`): summary of AI tools used, what they were used for, and what was edited or verified manually.
