#!/usr/bin/env python3
"""
Run the full ingestion pipeline:
1. Read data_manifest.csv
2. Parse each raw source
3. Chunk each source
4. Write processed text and chunks to data/processed/
5. Save all chunks as a single JSON file for the RAG index
"""

import csv
import json
from pathlib import Path

from src.ingest import REPO_ROOT, DATA_RAW, DATA_PROCESSED, MANIFEST_PATH, CHUNK_SIZE, CHUNK_OVERLAP
from src.ingest.parser import parse_file
from src.ingest.chunking import chunk_text


def run():
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

    with open(MANIFEST_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        sources = list(reader)

    print(f"Found {len(sources)} sources in manifest.")

    all_chunks = []
    for src in sources:
        source_id = src["source_id"]
        raw_path = REPO_ROOT / src["raw_path"]
        if not raw_path.exists():
            print(f"  SKIP {source_id}: raw file not found at {raw_path}")
            continue

        text = parse_file(raw_path)
        processed_path = DATA_PROCESSED / f"{source_id}.txt"
        processed_path.write_text(text, encoding="utf-8")

        chunks = chunk_text(text, source_id, CHUNK_SIZE, CHUNK_OVERLAP)
        all_chunks.extend(chunks)
        print(f"  {source_id}: {len(text)} chars -> {len(chunks)} chunks")

    chunks_path = DATA_PROCESSED / "chunks.json"
    with open(chunks_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)
    print(f"\nTotal: {len(all_chunks)} chunks saved to {chunks_path}")


if __name__ == "__main__":
    run()
