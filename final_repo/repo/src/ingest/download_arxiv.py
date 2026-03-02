#!/usr/bin/env python3
"""
Download arXiv papers for the Phase II corpus via keyword search.

Searches the arXiv API (free, no key required) for papers matching the
project's research domain — AI/automation impact on labor, job displacement,
UBI policy, and AI regulation — then downloads the top results as PDFs.

This script is NOT part of the main RAG pipeline. It documents how the
arXiv portion of the corpus was acquired. The remaining non-arXiv sources
were downloaded manually (see MANUAL_SOURCES below).

Usage:
    python src/ingest/download_arxiv.py [--max-per-query 5] [--total 10]

Requires: requests  (already in requirements.txt)
"""

import argparse
import hashlib
import random
import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = REPO_ROOT / "data" / "raw"

ARXIV_API = "http://export.arxiv.org/api/query"

# Keyword queries reflecting the research domain from Phase I framing brief:
# "Job policy, regulation, AI/automation, and Universal Basic Income"
SEARCH_QUERIES = [
    'all:"artificial intelligence" AND all:"job displacement"',
    'all:"automation" AND all:"labor market"',
    'all:"universal basic income" AND all:"automation"',
    'all:"AI regulation" AND all:"labor policy"',
    'all:"large language models" AND all:"employment"',
    'all:"AI" AND all:"future of work"',
    'all:"technological unemployment" AND all:"artificial intelligence"',
    'all:"AI governance" AND all:"workforce"',
]

# Non-arXiv sources that were downloaded manually
MANUAL_SOURCES = {
    "nigar_2025_ai_technological_unemployment.pdf":
        "Nigar et al. (2025) — AI and Technological Unemployment. Journal of Open Innovation.",
    "sharfuddin_2025_tax_reform_workforce.pdf":
        "Sharfuddin (2025) — Reforming the Tax Code for AI Workforce. Mercatus Center.",
    "imf_ai_global_economy.pdf":
        "IMF — AI Will Transform the Global Economy. IMF Blog.",
    "tan_2025_ubi_automation.pdf":
        "Tan (2025) — Universal Basic Income in the Age of Automation.",
    "shrm_automation_job_displacement.pdf":
        "SHRM — Automation, Generative AI, and Job Displacement Risk. SHRM Data Brief.",
}

NS = {"atom": "http://www.w3.org/2005/Atom"}


def _slug(title: str, arxiv_id: str) -> str:
    """Create a filesystem-safe slug from paper title + arxiv id."""
    clean = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")[:60]
    short_id = arxiv_id.replace("/", "_").replace(".", "")
    return f"arxiv_{short_id}_{clean}.pdf"


def search_arxiv(query: str, max_results: int = 10) -> list[dict]:
    """Query the arXiv API and return paper metadata."""
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    resp = requests.get(ARXIV_API, params=params, timeout=30)
    resp.raise_for_status()

    root = ET.fromstring(resp.text)
    papers = []
    for entry in root.findall("atom:entry", NS):
        arxiv_id_url = entry.find("atom:id", NS).text.strip()
        arxiv_id = arxiv_id_url.split("/abs/")[-1]
        # Strip version suffix (e.g. v1, v2) for the PDF URL
        arxiv_id_base = re.sub(r"v\d+$", "", arxiv_id)
        title = entry.find("atom:title", NS).text.strip().replace("\n", " ")
        title = re.sub(r"\s+", " ", title)
        summary = entry.find("atom:summary", NS).text.strip()[:200]
        authors = [a.find("atom:name", NS).text
                    for a in entry.findall("atom:author", NS)]

        papers.append({
            "arxiv_id": arxiv_id_base,
            "title": title,
            "authors": authors,
            "summary": summary,
            "pdf_url": f"https://arxiv.org/pdf/{arxiv_id_base}",
        })
    return papers


def download_papers(max_per_query: int = 5, total_target: int = 10):
    """Search arXiv with domain keywords and download unique papers."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    # Collect candidates from all queries
    seen_ids = set()
    candidates = []

    for query in SEARCH_QUERIES:
        print(f"  Searching: {query}")
        try:
            results = search_arxiv(query, max_results=max_per_query)
        except Exception as e:
            print(f"    Error: {e}")
            continue
        for paper in results:
            if paper["arxiv_id"] not in seen_ids:
                seen_ids.add(paper["arxiv_id"])
                candidates.append(paper)
        time.sleep(1)  # polite delay between API calls

    print(f"\n  Found {len(candidates)} unique papers across all queries.")

    # Shuffle to get variety across queries, then take up to total_target
    random.shuffle(candidates)
    selected = candidates[:total_target]

    print(f"  Selected {len(selected)} papers to download.\n")

    downloaded = 0
    skipped = 0
    for paper in selected:
        filename = _slug(paper["title"], paper["arxiv_id"])
        dest = RAW_DIR / filename
        if dest.exists() and dest.stat().st_size > 1000:
            print(f"  SKIP  {filename} (already exists)")
            skipped += 1
            continue

        print(f"  GET   [{paper['arxiv_id']}] {paper['title'][:70]}...")
        try:
            resp = requests.get(paper["pdf_url"], timeout=30)
            resp.raise_for_status()
            if not resp.content[:5] == b"%PDF-":
                print(f"    WARN: not a valid PDF, skipping")
                continue
            dest.write_bytes(resp.content)
            print(f"    OK  -> {filename} ({len(resp.content):,} bytes)")
            downloaded += 1
            time.sleep(1)
        except Exception as e:
            print(f"    ERR {e}")

    print(f"\nArXiv: {downloaded} downloaded, {skipped} already existed")
    return selected


def check_manual_sources():
    """Report status of non-arXiv sources."""
    print("\nManual sources (not from arXiv):")
    for filename, desc in MANUAL_SOURCES.items():
        dest = RAW_DIR / filename
        if dest.exists():
            print(f"  OK    {filename} ({dest.stat().st_size:,} bytes)")
        else:
            print(f"  MISS  {filename} — {desc}")


def main():
    parser = argparse.ArgumentParser(
        description="Download arXiv papers for the Phase II corpus.")
    parser.add_argument("--max-per-query", type=int, default=5,
                        help="Max results to fetch per keyword query (default: 5)")
    parser.add_argument("--total", type=int, default=10,
                        help="Target number of arXiv papers to download (default: 10)")
    args = parser.parse_args()

    print("=" * 60)
    print("  Phase II Corpus Acquisition — arXiv Keyword Search")
    print("=" * 60)
    print(f"\nDomain: AI/automation impact on labor, job displacement,")
    print(f"        UBI policy, and AI regulation\n")
    print(f"Config: {args.max_per_query} results/query, {args.total} total target\n")

    selected = download_papers(
        max_per_query=args.max_per_query, total_target=args.total)

    check_manual_sources()

    print(f"\nAll PDFs in {RAW_DIR}:")
    pdfs = sorted(RAW_DIR.glob("*.pdf"))
    for f in pdfs:
        print(f"  {f.name}")
    print(f"\n{len(pdfs)} sources total.")


if __name__ == "__main__":
    main()
