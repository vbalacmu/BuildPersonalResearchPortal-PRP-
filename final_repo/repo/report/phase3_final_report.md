# Phase 3 — Personal Research Portal Final Report

## 1. Introduction and Research Question

### 1.1 Domain and Motivation

This report describes the Phase 3 Personal Research Portal (PRP), a Streamlit-based application that wraps the Phase 2 RAG pipeline into a usable product for the domain of job policy, regulation, AI and automation, and Universal Basic Income. The portal supports a full research workflow over a curated corpus of 15 sources: question formulation, evidence retrieval, citation-backed synthesis, and export of research artifacts. Phase 1 established the domain framing and prompt behaviors; Phase 2 delivered ingestion, semantic retrieval, and generation with structured citations; Phase 3 adds a working interface, persistent research threads, artifact generation, and an evaluation view so that the system can be run and audited end to end.

### 1.2 Main Research Question and Sub-questions

The main research question carried forward from Phase 1 is: *How do policymakers and researchers link AI and automation to job displacement, and what role do proposals like UBI and related policies—retraining, safety nets, regulation—play in the debate?* This question decomposes into six retrievable sub-questions that drive both corpus design and the evaluation query set: how job displacement or employment impact is defined and measured; what empirical evidence exists on automation and job loss across sectors and methods; how UBI is argued for or against as a response to automation; what other policy responses are proposed and how they compare; how regulatory proposals such as the EU AI Act address AI and work; and where sources agree or disagree on the scale of impact and the best policy response. The portal is tuned for these policy- and evidence-centric questions rather than for generic AI safety or technical topics.

### 1.3 Scope

The corpus and portal are bounded by two criteria: relevance to the main question and verifiability. In scope are peer-reviewed papers, working papers, policy briefs, institutional reports, and regulatory analyses that either discuss AI and automation in relation to labor markets or propose and analyze policies such as UBI, tax reform, training, or AI regulation with explicit evidence. Out of scope are purely technical ML or LLM papers without labor or policy linkages, opinion pieces without empirical grounding, and speculative futures that cannot be grounded in existing evidence. The portal does not aim to cover the full AI ethics or macroeconomics literature; it focuses on AI-driven labor impacts and policy responses with traceable, citable evidence.

### 1.4 Continuity from Phases 1 and 2

Phase 3 reuses the domain framing and sub-questions from Phase 1 as the backbone of the corpus and query set, along with the structured prompt patterns that enforce explicit handling of unknown or missing evidence and citation constraints. The Phase 1 evaluation rubric—groundedness, citation correctness, usefulness—is operationalized in the Phase 2 automated metrics (citation precision and answer relevance) and remains visible in the Phase 3 evaluation view. From Phase 2, the portal reuses the ingestion pipeline that reads the metadata manifest, parses PDFs, chunks text, and builds the FAISS index; the RAG stack with semantic retrieval via all-MiniLM-L6-v2 and citation-backed generation via Ollama llama3.2 with a structured system prompt; and the evaluation harness over 20 queries (10 direct, 5 synthesis, 5 edge-case) with citation_precision and answer_relevance. Phase 3 adds a Streamlit interface that exposes search and ask, saves research threads, generates and exports an evidence-table artifact, and surfaces evaluation metrics and example answers so that the system functions as a single, runnable research product.

---

## 2. System Architecture

The portal follows a three-layer architecture: the Streamlit UI in `src/app/main.py` calls into the RAG layer in `src/rag/`, which in turn reads from and writes to the data layer under `data/`.

### 2.1 Data Layer

The data manifest at `data/data_manifest.csv` holds one row per source with the required schema: source_id, title, authors, year, source_type, venue, url_or_doi, raw_path, processed_path, tags, and relevance_note. Raw artifacts live under `data/raw/` as PDFs or snapshots; 10 papers were acquired via the documented script `src/ingest/download_arxiv.py`, and 5 were downloaded manually from journals and policy organizations (IMF, SHRM, Mercatus, and similar). The ingest pipeline writes plain-text extractions to `data/processed/{source_id}.txt` and produces a single chunk list in `data/processed/chunks.json`, where each chunk has source_id, chunk_id of the form `{source_id}_chunk_{NNN}`, and text. The FAISS index is stored at `data/processed/faiss.index` and is built from L2-normalized embeddings of all chunk texts.

### 2.2 Ingestion Pipeline

The ingestion pipeline is implemented in `src/ingest/`. The main entry point is `run_ingest.py`, which reads `data_manifest.csv`, resolves each source's raw_path under `data/raw/`, and parses the file with `parser.py` (pypdf for PDFs). Cleaned text is written to `data/processed/{source_id}.txt`. Chunking is performed by `chunking.py` with a fixed size of 512 characters and an overlap of 64 characters; each chunk receives a unique chunk_id and all chunks are collected into `data/processed/chunks.json`. The script `download_arxiv.py` documents how the arXiv portion of the corpus was acquired via keyword search and is included for reproducibility; it is not invoked in the normal RAG run path. The pipeline is deterministic given a fixed set of PDFs under `data/raw/` and is run with `python -m src.ingest.run_ingest`.

### 2.3 Retrieval Layer

Retrieval is implemented in `src/rag/retrieve.py`. Chunks are embedded with the sentence-transformers model all-MiniLM-L6-v2 (384 dimensions). The index is a FAISS IndexFlatIP; vectors are L2-normalized so that inner product corresponds to cosine similarity. On the first invocation of retrieval after ingestion, the module builds the index from `chunks.json` and writes it to `data/processed/faiss.index`. At query time, the query string is encoded with the same model, normalized, and used to retrieve the top-k chunks (k=5 by default). The function returns a list of dictionaries, each containing chunk_id, source_id, text, and similarity score. Building the index is triggered by running `python -m src.rag.retrieve` as the main module.

### 2.4 Generation Layer

Generation is implemented in `src/rag/generate.py` with two modes. In Ollama mode the application sends a structured prompt to a local Ollama server at `http://localhost:11434/api/generate` using the model llama3.2. The system prompt requires every substantive claim to be cited using the exact format `(source_id, chunk_id)`, supplies a concrete example drawn from the chunk headers, instructs the model to state "No evidence in corpus for this." when the context does not support a claim, and forbids invention beyond the given chunks. In template mode the code performs a deterministic, extractive pass over the retrieved chunks: it selects representative sentences, formats them as bullet points with inline `(source_id, chunk_id)` citations, and appends a short reference list. Template mode requires no model server and is used both as a user-selectable baseline and as an automatic fallback when Ollama is unavailable or errors. Both modes append each run to `logs/runs.jsonl` with timestamp, query, model, prompt version, retrieved chunk IDs and scores, and the full answer text.

### 2.5 Portal UI Layer

The portal is implemented in `src/app/main.py` using Streamlit. It offers three views: Ask / Search, Threads & Artifacts, and Evaluation. The app adds the repository root to `sys.path` before importing the RAG modules so that `src.rag` resolves correctly regardless of the working directory when Streamlit is launched. The Ask / Search view is the primary entry point for running queries; Threads & Artifacts lists saved threads and allows generation and export of the evidence-table artifact; the Evaluation view reads `src/eval/phase2_eval_results.json` and displays aggregate metrics by query type, a per-query table, and a simple answer inspector.

---

## 3. Portal Functionality

### 3.1 Ask / Search Interface

The Ask / Search tab presents a text area for the research question and a dropdown to choose generation mode (ollama or template). When the user clicks "Run query," the application calls `retrieve(query, k=5)` and displays the retrieved chunks with chunk_id, source_id, a 160-character snippet, and the similarity score. It then calls `generate(query, chunks, model=selected_mode)` and renders the answer. Citations are parsed from the answer text using a regex that looks for parenthetical pairs matching `(source_id, chunk_id)`; each cited pair is resolved against the data manifest so that the UI can show source title and, when available, a clickable url_or_doi. The same query, chunk list, and answer are written to `logs/threads/thread_{timestamp}.json` so that every run becomes a reusable research thread. This flow ensures that each answer is visibly tied to specific chunks and that each citation maps back to a source in the manifest.

### 3.2 Research Threads and History

The Threads & Artifacts tab loads all JSON files under `logs/threads/` whose names match `thread_*.json`, sorts them by timestamp in reverse order, and presents a dropdown of labels of the form "timestamp — first 80 characters of query." Selecting a thread displays its timestamp and full query, the list of retrieved chunks with cleaned text snippets, and the answer with citations resolved as in the Ask / Search view. The tab thus provides a persistent history of past queries and supports inspection and reuse of prior evidence and answers without re-running retrieval or generation.

### 3.3 Artifact Generation: Evidence Table

The portal implements the evidence-table artifact schema specified in the project requirements: Claim, Evidence snippet, Citation (source_id, chunk_id), Confidence, and Notes. The function `build_evidence_table(thread)` constructs a pandas DataFrame in which each row corresponds to one retrieved chunk. The Claim column is filled with the fixed string "Evidence related to: {query}" for that thread; the Evidence snippet is a truncation of the chunk text to approximately 280 characters; the Citation column contains the literal `(source_id, chunk_id)`; Confidence and Notes are left empty for the user to complete during manual review. If the thread has no retrieved chunks, the table contains a single row with the query in the Claim column, "No evidence in corpus for this query." in the Evidence snippet column, and empty Citation. The table is shown in the UI and is the basis for both export actions.

### 3.4 Export Capabilities

Two export actions are available from the Threads & Artifacts tab. Export evidence table (CSV) writes the evidence table for the selected thread to `outputs/evidence_table_{timestamp}.csv`. Export thread summary (Markdown) writes a Markdown file to `outputs/thread_{timestamp}.md` containing the query, the full answer, and the evidence table rendered as a Markdown table. These two formats satisfy the MVP requirement that artifacts be exportable in Markdown or CSV; PDF export is not implemented. The outputs directory is created on demand if it does not exist.

---

## 4. Evaluation and Trust Behaviors

### 4.1 Reuse of the Phase 2 Query Set and Metrics

The portal does not re-run the 20-query evaluation set itself; that is done offline by executing `python -m src.eval.run_eval`, which loads the same RAG stack, runs each of the 20 queries (10 direct, 5 synthesis, 5 edge-case as defined in `src/eval/run_eval.py` and documented in `src/eval/queries_phase2.md`), and writes results to `src/eval/phase2_eval_results.json`. The Evaluation tab reads this file and displays an aggregate table of mean citation_precision and mean answer_relevance by query type (direct, synthesis, edge), a per-query table with query_id, query_type, citation_precision, and answer_relevance, and a dropdown to inspect the full query text and answer for any single run. Citation precision is defined as the fraction of cited chunk_ids in the generated answer that exist in the corpus; answer relevance is the cosine similarity between the query embedding and the first 1000 characters of the answer embedding using the same all-MiniLM-L6-v2 model. Thus the portal surfaces the same metrics and design used in the Phase 2 evaluation report without duplicating the evaluation logic in the UI.

### 4.2 Summary of Metrics

Under the Phase 2 evaluation (Ollama llama3.2 with the structured citation prompt), aggregate citation precision was 0.700 for direct queries, 0.600 for synthesis, and 1.000 for edge-case queries, with an overall mean of 0.750. Aggregate answer relevance was 0.867 for direct, 0.840 for synthesis, and 0.872 for edge-case, with an overall mean of 0.862. Compared to the template baseline, the Ollama setup improved answer relevance (from 0.798 to 0.862) but reduced citation precision (from 0.984 to 0.750) because the small language model sometimes omits the required citation format; when it does cite, every citation in the evaluated runs resolved to a valid chunk_id. The template baseline never emits "No evidence in corpus"; the Ollama generator did so on three queries (direct_06, synth_02, synth_04) where the retrieved chunks were insufficient for the specific question, which matches the required trust behavior of flagging missing evidence.

### 4.3 Representative Cases

For the query "What does the IMF estimate about AI's impact on global employment?," the system retrieves chunks from the IMF report (e.g. imf_ai_economy_chunk_002, imf_ai_economy_chunk_003), and the Ollama generator responds with the 40% global employment exposure figure and cites the chunks in the required format; citation precision is 1.000 and answer relevance 0.884. For the edge-case query "Does the corpus support the claim that AI will create more jobs than it destroys?," the system retrieves a mix of chunks; when the evidence does not clearly support the strong claim, the generator states that no decisive evidence exists or that sources are mixed, rather than asserting a confident yes or no, and citation precision remains 1.000. For the synthesis query "How do the policy recommendations from the IMF, EU AI Act, and UBI literature complement or conflict with each other?," the system sometimes produces a coherent synthesis but omits explicit `(source_id, chunk_id)` citations for every claim, yielding citation_precision 0.000 on some runs despite high answer relevance; this is a format-adherence failure rather than hallucination, and the portal mitigates it by offering the template mode and by exposing the evaluation metrics so users can see the tradeoff.

### 4.4 Trust Behaviors Encoded in the Portal

The system prompt and the template generator both require that substantive claims be backed by citations in the form `(source_id, chunk_id)`. The evaluation harness measures citation precision against the set of 3,068 valid chunk_ids; in practice the system either produces citations that resolve to real chunks or omits citations, and no fabricated chunk_ids were observed in the Phase 2 runs. When retrieved chunks are weakly related or absent, the generation prompt instructs the model to state "No evidence in corpus for this."; when no chunks are retrieved at all (e.g. index not built), the UI displays a warning and does not call the generator, so no answer is fabricated. Every query, retrieved chunk list, and answer is persisted as a thread, and users can export the evidence table and thread summary, so any answer can be audited against the underlying chunks and sources.

---

## 5. Limitations and Future Work

### 5.1 Technical Limitations

The system relies on a small local model (llama3.2 via Ollama, 3B parameters). It performs adequately on structured citation tasks but may miss subtle cross-document relationships or nuanced policy arguments that larger models capture. The embedding model all-MiniLM-L6-v2 and the FAISS inner-product index are robust and reproducible but not state of the art; hybrid retrieval (e.g. BM25 plus dense) or cross-encoder reranking could improve recall and precision, especially on synthesis and policy-specific queries. Chunking is fixed-size (512 characters, 64-character overlap) and does not use section boundaries; pypdf does not reliably preserve section structure across diverse PDFs, so section-aware chunking would require a different parser or manual markup. The corpus is deliberately small (15 sources, 3,068 chunks) and focused on English-language policy and labor literature; it does not cover non-English sources, global South perspectives, or older automation literature in depth.

### 5.2 UX Limitations

Threads are stored as JSON files under `logs/threads/` with no database or multi-user support; the design is appropriate for a personal portal but not for shared or collaborative use. The portal implements only the evidence-table artifact; annotated bibliography and synthesis-memo generators are not implemented, though the manifest and chunk structure would support them. The UI does not expose filters by year, venue, source type, or tags; that metadata exists in the manifest but is not yet queryable from the interface.

### 5.3 Future Work

Concrete next steps include an agentic research loop that decomposes complex questions into sub-queries, runs retrieval and generation iteratively, and aggregates results; a knowledge-graph or concept view that links entities such as UBI, EU AI Act, and technological unemployment to supporting chunks and sources; and the addition of BM25 or sparse retrieval plus reranking to improve relevance on keyword-heavy policy queries. Richer artifacts could include an annotated bibliography view over the manifest and selected chunks and a synthesis-memo generator that produces an 800–1200 word memo with inline citations and a reference list. The Phase 2 report already identified query rewriting and stripping of bibliography sections during parsing as design choices that would address specific failure modes (e.g. direct_06, direct_07); implementing those in the pipeline would improve citation coverage and reduce spurious citations to sources outside the corpus.

---

## 6. Engineering and Reproducibility

### 6.1 End-to-End Run Path

A grader can run the system from a clean clone as follows. From the repository root (e.g. `final_repo/repo`), create a virtual environment, activate it, and install dependencies with `pip install -r requirements.txt`. Ensure the corpus is present: either place PDFs under `data/raw/` so that the paths in `data_manifest.csv` resolve, or run `src/ingest/download_arxiv.py` to obtain the arXiv subset (the manifest also references manually acquired sources that must be added separately). Run `python -m src.ingest.run_ingest` to produce `data/processed/*.txt` and `data/processed/chunks.json`. Run `python -m src.rag.retrieve` once to build `data/processed/faiss.index`. Optionally run `python -m src.eval.run_eval` to refresh `src/eval/phase2_eval_results.json`. Start the portal with `streamlit run src/app/main.py` and open the URL printed in the terminal (e.g. http://localhost:8501). For full RAG functionality Ollama must be running with the llama3.2 model; if Ollama is not available, the user can select template mode in the UI and still run queries with citation-backed, extractive answers.

### 6.2 Configuration Choices

Embedding model is all-MiniLM-L6-v2 (sentence-transformers). The vector index is FAISS IndexFlatIP with L2-normalized vectors. Top-k is 5 and is defined in `src/rag/__init__.py` as TOP_K. Generation uses Ollama model llama3.2 with temperature 0.1 and num_predict 1024; the template fallback is selected by passing `model="template"` to `generate()`. Chunk size and overlap are 512 and 64 characters and are set in `src/ingest/__init__.py`. Logs are appended to `logs/runs.jsonl` in JSONL form; each thread is written to `logs/threads/thread_{ISO8601}.json`.

### 6.3 Implementation Details Relevant to Graders

The Streamlit app and the evaluation script both insert the repository root into `sys.path` before importing `src.rag` and `src.ingest`, so that running `streamlit run src/app/main.py` or `python -m src.eval.run_eval` from the repo root works without installing the package. Citation extraction in the UI and in the evaluation script normalizes several formats: the standard `(source_id, chunk_id)` parenthetical, the verbose `(source_id: X, chunk_id: Y)` form, and bare chunk_id strings that appear in the text; normalization is used both for computing citation precision and for resolving citations to titles and URLs in the manifest. If the Ollama server is unreachable or returns an error, `generate()` catches the exception and falls back to template mode for that request while still logging the run, so that evaluation and the UI continue to function without a running model server.
