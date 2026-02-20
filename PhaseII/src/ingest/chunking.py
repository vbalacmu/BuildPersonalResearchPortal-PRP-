"""
Chunking strategy: fixed-size character-based chunks with overlap.
Output: list of dicts with keys: chunk_id, source_id, text.
"""


def chunk_text(text: str, source_id: str, chunk_size: int = 512, overlap: int = 64) -> list[dict]:
    """
    Split text into overlapping chunks by character count.
    Returns list of {"chunk_id": str, "source_id": str, "text": str}.
    """
    chunks = []
    start = 0
    idx = 0
    while start < len(text):
        end = start + chunk_size
        chunk_text_str = text[start:end]
        if chunk_text_str.strip():
            chunks.append({
                "chunk_id": f"{source_id}_chunk_{idx:03d}",
                "source_id": source_id,
                "text": chunk_text_str.strip(),
            })
            idx += 1
        start += chunk_size - overlap
    return chunks
