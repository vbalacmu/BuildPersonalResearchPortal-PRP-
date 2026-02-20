"""
Generate answer from retrieved chunks using Ollama (local SLM).
Every major claim cites (source_id, chunk_id).
If corpus does not support a claim, say so. Log every run.

Default model: llama3.2 via Ollama (local, free, no API key).
Fallback: template mode (extractive, no LLM needed).
"""

import json
import datetime
from pathlib import Path

import requests

from src.rag import REPO_ROOT

LOGS_DIR = REPO_ROOT / "logs"

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"

SYSTEM_PROMPT = (
    "You are a research assistant. Answer the question using ONLY the provided "
    "context chunks. For every claim you make, you MUST cite the source using "
    "EXACTLY this format: (source_id, chunk_id) where source_id and chunk_id "
    "are copied exactly from the chunk headers above. "
    "For example, if a chunk header says 'source_id: eloundou_2023, chunk_id: eloundou_2023_chunk_013', "
    "cite it as (eloundou_2023, eloundou_2023_chunk_013). "
    "If the context does not contain evidence for a claim, "
    "explicitly state: 'No evidence in corpus for this.' "
    "Be concise and specific. Do not invent information beyond what the chunks say."
)


def _format_chunks_for_prompt(chunks: list[dict]) -> str:
    parts = []
    for c in chunks:
        parts.append(
            f"--- Chunk (source_id: {c['source_id']}, chunk_id: {c['chunk_id']}) ---\n"
            f"{c['text']}"
        )
    return "\n\n".join(parts)


def _generate_ollama(query: str, chunks: list[dict]) -> str:
    """Generate answer using Ollama local LLM."""
    context = _format_chunks_for_prompt(chunks)
    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n\n"
        f"Answer (cite every claim with (source_id, chunk_id)):"
    )

    try:
        resp = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "num_predict": 1024,
                },
            },
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json().get("response", "").strip()
    except requests.ConnectionError:
        print("    WARN: Ollama not running. Falling back to template mode.")
        return _generate_template(query, chunks)
    except Exception as e:
        print(f"    WARN: Ollama error ({e}). Falling back to template mode.")
        return _generate_template(query, chunks)


def _generate_template(query: str, chunks: list[dict]) -> str:
    """Extractive fallback: selects relevant sentences with citations. No LLM needed."""
    lines = []
    lines.append(f"Based on the retrieved evidence, here is what the corpus says about: {query}\n")

    refs = []
    for c in chunks:
        sid = c["source_id"]
        cid = c["chunk_id"]
        text = c["text"].replace("\n", " ").strip()
        sentences = [s.strip() + "." for s in text.split(".") if len(s.strip()) > 40]
        top = sentences[:2] if len(sentences) >= 2 else sentences
        for sent in top:
            lines.append(f"- {sent} ({sid}, {cid})")
        refs.append(f"({sid}, {cid})")

    if len(lines) == 1:
        lines.append("No evidence in corpus for this query.")

    lines.append("")
    lines.append("References:")
    for r in refs:
        lines.append(f"  {r}")
    return "\n".join(lines)


def generate(query: str, chunks: list[dict], model: str = "ollama") -> str:
    """
    Generate a citation-backed answer from retrieved chunks.
    model: 'ollama' (default, local LLM) or 'template' (extractive fallback).
    """
    if model == "ollama":
        answer = _generate_ollama(query, chunks)
    else:
        answer = _generate_template(query, chunks)

    _log_run(query, chunks, answer, model)
    return answer


def _log_run(query: str, chunks: list[dict], answer: str, model: str):
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "query": query,
        "model": model,
        "prompt_version": "v1_structured_citations",
        "retrieved_chunks": [
            {"chunk_id": c["chunk_id"], "source_id": c["source_id"], "score": c.get("score")}
            for c in chunks
        ],
        "answer": answer,
    }
    log_path = LOGS_DIR / "runs.jsonl"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
