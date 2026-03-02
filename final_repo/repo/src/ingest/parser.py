"""
Parse sources from data/raw/ (TXT and PDF).
Output: cleaned text per source written to data/processed/{source_id}.txt.
"""

from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


def parse_pdf(path: Path) -> str:
    """Extract text from PDF using pypdf."""
    if PdfReader is None:
        raise ImportError("pypdf is required for PDF parsing. Install with: pip install pypdf")
    reader = PdfReader(str(path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(pages).strip()


def parse_text(path: Path) -> str:
    """Read plain text file."""
    return path.read_text(encoding="utf-8", errors="replace").strip()


def parse_file(path: Path) -> str:
    """Parse a single file (dispatch by extension)."""
    ext = path.suffix.lower()
    if ext == ".pdf":
        return parse_pdf(path)
    elif ext in (".txt", ".md", ".text"):
        return parse_text(path)
    else:
        return parse_text(path)
