## Personal Research Portal – Demo Script

Use this as a read-aloud script while recording a **3–6 minute** demo. **Replace [your name] with your actual name** when you record; all other bracketed placeholders have been filled with example text you can use or adjust.  

**Pace tip:** Speak at a natural pace and pause briefly when you switch tabs or click; that easily fills 4–5 minutes. The extra lines added in each section give you enough to reach 5–6 minutes without rushing.

---

### 1. Intro & Goal (≈30–40 seconds)

“Hi, I’m [your name], and this is my **Personal Research Portal** for the domain of **societal and labor-market impacts of generative AI and automation**.

My **main research question** is: *How does AI affect employment, wages, and worker adaptation, and what do policymakers and researchers recommend?*

The goal of this portal is to help me go from a research question to a **grounded synthesis**. It retrieves evidence from a curated corpus, generates **citation‑backed answers**, and produces **exportable research artifacts** that I can use in my analysis and write‑up. My corpus has about **15 sources**—papers and reports on AI, labor markets, automation, and policy—so the answers are grounded in that specific literature.”

“At the top you can see the three main parts of the portal:
- **Ask / Search** – to query the corpus and get citation‑backed answers
- **Threads & Artifacts** – to review past research threads and generate artifacts
- **Evaluation** – to inspect metrics and representative examples”

---

### 2. Ask / Search Flow (≈1–1.5 minutes)

“First, I’ll show the **Ask / Search** tab.”

“At the top I can enter a research question. For this demo I’ll use:

*‘What does the IMF say about AI’s impact on global employment, and how do workers strategically adapt to AI-driven technological change?’*

Below that I select a **generation mode**. Here I’m using the default **‘ollama’** mode, which talks to a local Ollama model. If Ollama isn’t available, the system can fall back to a more template‑based generator so it still returns structured answers instead of crashing.”

“Now I’ll click **Run query**.”

“Behind the scenes, the portal runs **semantic retrieval** over my corpus using a FAISS index. It retrieves the **top‑k chunks**—here, the top five—that are most relevant to my question.  

You can see those **retrieved chunks** here: each row shows a `chunk_id`, the `source_id`, a similarity score, and a short snippet of text. This is the **evidence set** that the model sees. The chunks come from parsed PDFs in `data/processed/`, so everything is traceable back to the original sources.”

“Using those retrieved chunks, the generator produces an **answer with inline citations**.  

You can see citations like `(source_id, chunk_id)` embedded in the answer text. For example, here it might cite *(eloundou_2023, eloundou_2023_chunk_013)* or *(imf_ai_economy, imf_ai_economy_chunk_003)*—I’ll point to one on screen.”

“These `source_id`s map directly into my **data manifest** in `data/data_manifest.csv`, which contains metadata such as title, authors, year, and link/DOI. That means every citation in the answer can be traced back to a specific source and chunk in my corpus.”

“In my prompting and generation logic, I also instruct the system to **say when the corpus doesn’t support a claim** instead of guessing, which is important for trust and faithfulness.”

“Every time I run a query like this, the portal saves a **research thread** with the query, retrieved chunks, and answer, which I’ll show next.”

---

### 3. Threads & Artifacts (≈1 minute)

“Now I’ll go to the **Threads & Artifacts** tab.”

“Here I have a list of my **saved research threads**. Each thread is a full record of a past query: timestamp, query text, retrieved chunks, and the generated answer. That way I can **reproduce** what the system did and reuse it later.  

I’ll select the thread corresponding to the question I just ran.”

“Here you can see the full **thread**:
- the **timestamp**
- the **original query**
- the list of **retrieved chunks** with `source_id`, `chunk_id`, and snippets
- and the **answer**, including its inline citations

This view makes it easy to come back later, audit what the model saw, and how it answered.”

“From a thread, I can also generate a **research artifact**. In my implementation, that’s an **evidence table**.”

“The evidence table has the schema:

`Claim | Evidence snippet | Citation (source_id, chunk_id) | Confidence | Notes`

Each row ties a part of the answer back to a concrete snippet and citation. This is useful for writing up literature reviews or structured memos, because I can quickly see which evidence supports which claim.”

“I can also **export** these artifacts. For example, I’ll click **Export evidence table (CSV)** and **Export thread summary (Markdown)**.”

“These buttons save an **evidence table CSV** and a **Markdown thread summary** into the `outputs/` folder of the repo, so I can open them in a spreadsheet or text editor and include them directly in my report.”

---

### 4. Evaluation & Trust Behavior (≈1 minute)

“Finally, I’ll show the **Evaluation** tab.”

“In Phase 2, I built an evaluation set of **at least 20 queries** across different types—**direct** factual questions, **synthesis** questions that compare across sources, and **edge** questions that probe limits of the corpus—and logged results to `src/eval/phase2_eval_results.json`.  

This page loads those results and summarizes them.”

“Here you can see the **aggregate metrics** grouped by `query_type`, including **citation_precision** and **answer_relevance**. This tells me, for example, how often my citations point to the right text and how useful the answers are for different kinds of questions.”

“Below that is the **per‑query table**. Each row corresponds to a specific query in the evaluation set with its scores.”

“I can also inspect a **representative example**. I’ll select one query from the dropdown.”

“Here you see the **query text** and the **answer** that the system produced. Combined with the logs in `logs/` and the citations in the answer, this helps me debug failure modes and see where retrieval or generation needs improvement.”

“In terms of **trust behaviors**, the system is designed so that:
- every answer includes inline citations tied to `source_id` and `chunk_id`, and
- when the corpus doesn’t support a claim, the prompts instruct the model to say so rather than inventing citations.”

---

### 5. Engineering & Wrap‑Up (≈30–40 seconds)

“Under the hood, the repo follows the recommended structure:

- `data/raw/` for PDFs and snapshots  
- `data/processed/` for parsed text, chunks, and the FAISS index  
- `data/data_manifest.csv` for source metadata  
- `src/app/` for the Streamlit UI  
- `src/rag/` for retrieval and generation  
- `src/eval/` for evaluation scripts  
- `logs/` for runs and research threads  
- `outputs/` for exported artifacts  
- `report/` for the Phase 1–3 write‑ups

If a grader wants to run this from scratch, the steps are:

1. `git clone <repo_url>` and `cd BuildPersonalResearchPortal_PRP/final_repo/repo`  
2. `python3 -m venv .venv` and `source .venv/bin/activate`  
3. `pip install -r requirements.txt`  
4. `python -m src.ingest.run_ingest` and `python -m src.rag.retrieve` to build processed data and the FAISS index  
5. (Optional) `python -m src.eval.run_eval` to regenerate evaluation metrics  
6. `streamlit run src/app/main.py` to launch the portal locally at `http://localhost:8501`.”

“**Limitations and next steps:** The system depends on the quality of the corpus and the embedding model; I could extend it with more sources or a stronger LLM. For this project, the focus was on **citation faithfulness** and **exportable artifacts** so the pipeline is auditable and useful for real research.”

“To summarize: this portal turns my Phase 2 RAG pipeline into a **usable research product**. I can ask questions, get **citation‑backed answers**, generate **evidence‑table artifacts**, and inspect **evaluation metrics** and examples.  

That completes my demo for the Personal Research Portal.”

