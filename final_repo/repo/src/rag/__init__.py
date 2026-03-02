"""
RAG: embed and index chunks (FAISS), retrieve top-k per query, generate answer with citations.
Trust: refuse to invent citations; flag missing or conflicting evidence.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
INDEX_PATH = REPO_ROOT / "data" / "processed" / "faiss.index"
CHUNKS_PATH = REPO_ROOT / "data" / "processed" / "chunks.json"

TOP_K = 5
EMBED_MODEL = "all-MiniLM-L6-v2"
