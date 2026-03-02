"""
Embed chunks, build FAISS index, retrieve top-k chunks per query.
"""

import json
import numpy as np

try:
    import faiss
except ImportError:
    faiss = None

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

from src.rag import INDEX_PATH, CHUNKS_PATH, TOP_K, EMBED_MODEL

_model = None
_index = None
_chunks = None


def _get_model():
    global _model
    if _model is None:
        if SentenceTransformer is None:
            raise ImportError("sentence-transformers required. pip install sentence-transformers")
        _model = SentenceTransformer(EMBED_MODEL)
    return _model


def _load_chunks():
    global _chunks
    if _chunks is None:
        with open(CHUNKS_PATH, encoding="utf-8") as f:
            _chunks = json.load(f)
    return _chunks


def build_index():
    """Embed all chunks and build a FAISS index. Save to disk."""
    if faiss is None:
        raise ImportError("faiss-cpu required. pip install faiss-cpu")
    model = _get_model()
    chunks = _load_chunks()
    texts = [c["text"] for c in chunks]
    print(f"Embedding {len(texts)} chunks with {EMBED_MODEL}...")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    embeddings = embeddings.astype("float32")
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    faiss.write_index(index, str(INDEX_PATH))
    print(f"Index saved to {INDEX_PATH} ({index.ntotal} vectors, dim={dim})")


def load_index():
    """Load FAISS index from disk."""
    global _index
    if _index is None:
        if faiss is None:
            raise ImportError("faiss-cpu required. pip install faiss-cpu")
        _index = faiss.read_index(str(INDEX_PATH))
    return _index


def retrieve(query: str, k: int = TOP_K) -> list[dict]:
    """Return top-k chunks for query. Each dict: chunk_id, source_id, text, score."""
    model = _get_model()
    index = load_index()
    chunks = _load_chunks()
    q_emb = model.encode([query], convert_to_numpy=True).astype("float32")
    faiss.normalize_L2(q_emb)
    scores, indices = index.search(q_emb, k)
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0 or idx >= len(chunks):
            continue
        c = chunks[idx].copy()
        c["score"] = float(score)
        results.append(c)
    return results


if __name__ == "__main__":
    # Convenience CLI: build the FAISS index from data/processed/chunks.json
    build_index()
