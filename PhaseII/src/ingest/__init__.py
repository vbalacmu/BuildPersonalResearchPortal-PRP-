"""
Ingestion pipeline: parse and clean text, chunk, store text + metadata.
Produces data/processed/ and updates data_manifest.csv (processed_path).
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = REPO_ROOT / "data" / "raw"
DATA_PROCESSED = REPO_ROOT / "data" / "processed"
MANIFEST_PATH = REPO_ROOT / "data" / "data_manifest.csv"

CHUNK_SIZE = 512
CHUNK_OVERLAP = 64
