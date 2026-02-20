#!/usr/bin/env python3
"""
Run Phase 2 evaluation: 20 queries through RAG, compute metrics, save results.
Metrics: (1) citation_precision — fraction of cited chunk_ids that actually exist in the corpus.
         (2) answer_relevance — cosine similarity between query embedding and answer embedding.
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.rag.retrieve import retrieve, _load_chunks, _get_model
from src.rag.generate import generate

QUERIES = [
    # Direct queries (10)
    {"id": "direct_01", "type": "direct", "text": "What percentage of US jobs are exposed to large language models according to the literature?"},
    {"id": "direct_02", "type": "direct", "text": "How has generative AI affected freelance labor markets, particularly for writing and coding jobs?"},
    {"id": "direct_03", "type": "direct", "text": "What evidence exists that AI-exposed jobs showed wage or employment declines before ChatGPT?"},
    {"id": "direct_04", "type": "direct", "text": "What does the IMF estimate about AI's impact on global employment?"},
    {"id": "direct_05", "type": "direct", "text": "How do workers strategically adapt to AI-driven technological change?"},
    {"id": "direct_06", "type": "direct", "text": "What are the main provisions of the EU AI Act related to workforce regulation?"},
    {"id": "direct_07", "type": "direct", "text": "What arguments are made for Universal Basic Income as a response to automation?"},
    {"id": "direct_08", "type": "direct", "text": "What tax reforms have been proposed to support workers displaced by AI?"},
    {"id": "direct_09", "type": "direct", "text": "What sectors face the highest risk of job displacement from automation and generative AI?"},
    {"id": "direct_10", "type": "direct", "text": "What role does AI governance play in protecting worker rights and creativity?"},
    # Synthesis / multi-hop queries (5)
    {"id": "synth_01", "type": "synthesis", "text": "Compare the findings on AI's impact on freelance labor from Demirci et al. (2023) and Hui et al. (2023): where do they agree and disagree?"},
    {"id": "synth_02", "type": "synthesis", "text": "How do the policy recommendations from the IMF, EU AI Act, and UBI literature complement or conflict with each other?"},
    {"id": "synth_03", "type": "synthesis", "text": "Across the corpus, what evidence links AI exposure to both productivity gains and job displacement?"},
    {"id": "synth_04", "type": "synthesis", "text": "How do macroeconomic expert disagreements about AI relate to the empirical findings on labor market effects?"},
    {"id": "synth_05", "type": "synthesis", "text": "What patterns emerge across the corpus regarding whether AI primarily displaces workers or augments their capabilities?"},
    # Edge-case / ambiguity queries (5)
    {"id": "edge_01", "type": "edge", "text": "Does the corpus contain evidence that AI automation affects developed and developing economies differently?"},
    {"id": "edge_02", "type": "edge", "text": "Does the corpus support the claim that AI will create more jobs than it destroys?"},
    {"id": "edge_03", "type": "edge", "text": "Is there evidence for or against the feasibility of funding UBI through AI-related tax revenue?"},
    {"id": "edge_04", "type": "edge", "text": "Does the corpus contain conflicting evidence about whether upskilling is an effective response to AI displacement?"},
    {"id": "edge_05", "type": "edge", "text": "Does the corpus address the impact of AI on non-cognitive or creative work?"},
]


def extract_citations(answer: str, valid_chunk_ids: set = None) -> list[str]:
    """Extract (source_id, chunk_id) citations from answer text.
    Handles multiple formats the LLM might use:
      - (source_id, source_id_chunk_NNN)  — ideal format
      - (source_id, chunk_NNN)            — abbreviated, needs prefix
      - (source_id: X, chunk_id: Y)       — verbose format
    Returns chunk_ids normalized to match the corpus format."""
    cited = []
    # Pattern 1: standard (X, Y) pairs
    pattern = r'\(([^,()]+),\s*([^,()]+)\)'
    matches = re.findall(pattern, answer)
    for s, c in matches:
        sid = s.strip().replace("source_id:", "").replace("source_id", "").strip().strip(":")
        cid = c.strip().replace("chunk_id:", "").replace("chunk_id", "").strip().strip(":")
        cid = cid.strip()
        sid = sid.strip()
        # If chunk_id doesn't start with source_id prefix, try to reconstruct
        if valid_chunk_ids and cid not in valid_chunk_ids:
            # Try prefixing: e.g. "chunk_013" -> "eloundou_2023_chunk_013"
            candidate = f"{sid}_{cid}"
            if candidate in valid_chunk_ids:
                cid = candidate
        cited.append(cid)
    # Pattern 2: direct chunk_id references like source_id_chunk_NNN in text
    if valid_chunk_ids:
        for cid in valid_chunk_ids:
            if cid in answer and cid not in cited:
                cited.append(cid)
    return cited


def compute_citation_precision(answer: str, valid_chunk_ids: set) -> float:
    """Fraction of cited chunk_ids that exist in the corpus."""
    cited = extract_citations(answer, valid_chunk_ids)
    if not cited:
        return 0.0
    valid_count = sum(1 for c in cited if c in valid_chunk_ids)
    return valid_count / len(cited)


def compute_answer_relevance(query: str, answer: str) -> float:
    """Cosine similarity between query and answer embeddings."""
    import numpy as np
    model = _get_model()
    q_emb = model.encode([query], convert_to_numpy=True).astype("float32")
    a_emb = model.encode([answer[:1000]], convert_to_numpy=True).astype("float32")
    cos_sim = float(np.dot(q_emb[0], a_emb[0]) / (np.linalg.norm(q_emb[0]) * np.linalg.norm(a_emb[0]) + 1e-10))
    return cos_sim


def run_eval(model_name: str = "ollama"):
    """Run all 20 queries, compute metrics, save results."""
    chunks = _load_chunks()
    valid_chunk_ids = {c["chunk_id"] for c in chunks}

    results = []
    for q in QUERIES:
        print(f"  [{q['id']}] {q['text'][:80]}...")
        retrieved = retrieve(q["text"], k=5)
        answer = generate(q["text"], retrieved, model=model_name)
        cit_prec = compute_citation_precision(answer, valid_chunk_ids)
        ans_rel = compute_answer_relevance(q["text"], answer)
        results.append({
            "query_id": q["id"],
            "query_type": q["type"],
            "query_text": q["text"],
            "retrieved_chunk_ids": [c["chunk_id"] for c in retrieved],
            "answer": answer,
            "citation_precision": round(cit_prec, 3),
            "answer_relevance": round(ans_rel, 3),
        })
        print(f"    citation_precision={cit_prec:.3f}  answer_relevance={ans_rel:.3f}")

    out_path = REPO_ROOT / "eval" / "phase2_eval_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")
    _print_summary(results)
    return results


def _print_summary(results: list[dict]):
    """Print aggregate metrics."""
    import numpy as np
    types = ["direct", "synthesis", "edge"]
    for t in types:
        subset = [r for r in results if r["query_type"] == t]
        if not subset:
            continue
        cp = np.mean([r["citation_precision"] for r in subset])
        ar = np.mean([r["answer_relevance"] for r in subset])
        print(f"  {t:>10}: citation_precision={cp:.3f}  answer_relevance={ar:.3f}  (n={len(subset)})")
    cp_all = np.mean([r["citation_precision"] for r in results])
    ar_all = np.mean([r["answer_relevance"] for r in results])
    print(f"  {'overall':>10}: citation_precision={cp_all:.3f}  answer_relevance={ar_all:.3f}  (n={len(results)})")


if __name__ == "__main__":
    model = "ollama"
    if len(sys.argv) > 1:
        model = sys.argv[1]
    run_eval(model_name=model)
