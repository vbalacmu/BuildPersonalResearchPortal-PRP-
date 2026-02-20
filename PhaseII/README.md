# Phase II — Ground the Domain (Research-Grade RAG)

RAG pipeline over a corpus of 15 real sources on **AI/automation impact on labor, job displacement, UBI policy, and AI regulation**. Uses Ollama (llama3.2) for local LLM generation with structured citations, FAISS for retrieval, and evaluates on 20 domain-specific queries.

## Quick start

```bash
cd PhaseII
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Prerequisite: Ollama must be running with llama3.2 pulled
# ollama serve          (in another terminal)
# ollama pull llama3.2  (one-time)

# Step 1: Ingest (parse PDFs, chunk, build FAISS index)
python run_rag.py ingest

# Step 2: Single query
python run_rag.py query "What percentage of US jobs are exposed to LLMs?"

# Step 3: Run full 20-query evaluation
python run_rag.py eval
```

No API keys required. Everything runs locally using Ollama + open-weight models.

For a simpler extractive fallback (no Ollama needed):

```bash
python run_rag.py eval template
```

## Corpus acquisition

10 arXiv papers were downloaded programmatically; 5 additional sources from journals/policy orgs were downloaded manually. To re-download the arXiv papers:

```bash
python src/ingest/download_arxiv.py --total 10
```

See `src/ingest/download_arxiv.py` for the keyword queries and logic.

## Repo layout

```
PhaseII/
  README.md
  requirements.txt
  run_rag.py                  # Entry point: ingest | query | eval
  data/
    data_manifest.csv         # 15 sources with full metadata
    raw/                      # Source PDFs (15 papers/reports)
    processed/                # Parsed text, chunks.json, faiss.index
  src/
    ingest/
      parser.py               # PDF/TXT parsing (pypdf)
      chunking.py             # Fixed-size chunking with overlap
      run_ingest.py           # Orchestrates parse + chunk
      download_arxiv.py       # arXiv keyword search + PDF download
    rag/
      retrieve.py             # FAISS index + sentence-transformers
      generate.py             # Ollama (llama3.2) / template generator
  eval/
    queries_phase2.md         # 20 queries (10 direct, 5 synthesis, 5 edge)
    run_eval.py               # Evaluation (citation precision + answer relevance)
    phase2_eval_results.json  # Full results per query
  logs/
    runs.jsonl                # Machine-readable logs per run
  report/
    phase2_evaluation_report.md  # 3-5 page evaluation report
```

## Pipeline

1. **Ingest:** Parse PDFs from `data/raw/` (pypdf), chunk with fixed-size (512 chars, 64 overlap), save to `data/processed/chunks.json`.
2. **Index:** Embed chunks with `all-MiniLM-L6-v2` (sentence-transformers), build FAISS inner-product index.
3. **Retrieve:** Top-5 chunks per query via cosine similarity.
4. **Generate:** Ollama llama3.2 with structured citation prompt (or extractive template fallback).
5. **Log:** Every run saved to `logs/runs.jsonl` (query, retrieved chunk IDs, answer, model, timestamp).

## Enhancement: Structured Citations

Every answer includes inline `(source_id, chunk_id)` citations. The LLM is instructed to only cite from provided context and flag missing evidence.

## Trust behavior

- Only cites chunk IDs from the retrieved context; refuses to invent citations.
- Flags missing evidence: "No evidence in corpus for this."
- All runs logged for audit.

## Dependencies

See `requirements.txt`. Requires Ollama running locally (free, no API keys). All models are open-weight.
