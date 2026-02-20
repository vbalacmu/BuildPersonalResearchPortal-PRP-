#!/usr/bin/env python3
"""
Phase 2 one-command entry point.

Usage:
  python run_rag.py ingest          # Parse sources, chunk, build FAISS index
  python run_rag.py query "..."     # Single RAG query (uses Ollama llama3.2)
  python run_rag.py eval [model]    # Run 20-query evaluation (model: ollama|template)
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))


def cmd_ingest():
    from src.ingest.run_ingest import run as run_ingest
    from src.rag.retrieve import build_index
    print("=== Step 1: Ingest (parse + chunk) ===")
    run_ingest()
    print("\n=== Step 2: Build FAISS index ===")
    build_index()
    print("\nIngest complete.")


def cmd_query(query_text: str, model: str = "ollama"):
    from src.rag.retrieve import retrieve
    from src.rag.generate import generate
    chunks = retrieve(query_text, k=5)
    print(f"Retrieved {len(chunks)} chunks:")
    for c in chunks:
        print(f"  [{c['chunk_id']}] (score={c.get('score', 0):.3f}) {c['text'][:80]}...")
    print()
    answer = generate(query_text, chunks, model=model)
    print("=== Answer ===")
    print(answer)


def cmd_eval(model: str = "ollama"):
    from eval.run_eval import run_eval
    print(f"=== Running 20-query evaluation (model={model}) ===\n")
    run_eval(model_name=model)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "ingest":
        cmd_ingest()
    elif cmd == "query":
        if len(sys.argv) < 3:
            print("Usage: python run_rag.py query \"Your question here\" [model]")
            sys.exit(1)
        model = sys.argv[3] if len(sys.argv) > 3 else "ollama"
        cmd_query(sys.argv[2], model)
    elif cmd == "eval":
        model = sys.argv[2] if len(sys.argv) > 2 else "ollama"
        cmd_eval(model)
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
