import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
import streamlit as st

from src.rag.retrieve import retrieve
from src.rag.generate import generate


REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_MANIFEST_PATH = REPO_ROOT / "data" / "data_manifest.csv"
THREADS_DIR = REPO_ROOT / "logs" / "threads"
OUTPUTS_DIR = REPO_ROOT / "outputs"
EVAL_RESULTS_PATH = REPO_ROOT / "src" / "eval" / "phase2_eval_results.json"


def _ensure_dirs() -> None:
    THREADS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


@st.cache_data
def load_manifest() -> pd.DataFrame:
    if not DATA_MANIFEST_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(DATA_MANIFEST_PATH)


def parse_citations(text: str) -> List[str]:
    """Extract (source_id, chunk_id) style citations from answer text."""
    pattern = r"\(([^,()]+),\s*([^,()]+)\)"
    matches = re.findall(pattern, text)
    cites = []
    for s, c in matches:
        sid = s.strip().replace("source_id:", "").replace("source_id", "").strip().strip(":")
        cid = c.strip().replace("chunk_id:", "").replace("chunk_id", "").strip().strip(":")
        cites.append(f"{sid},{cid}")
    return sorted(set(cites))


def save_thread(query: str, chunks: List[Dict[str, Any]], answer: str) -> Path:
    _ensure_dirs()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    thread = {
        "timestamp": timestamp,
        "query": query,
        "retrieved_chunks": [
            {
                "chunk_id": c["chunk_id"],
                "source_id": c["source_id"],
                "score": c.get("score"),
                "text": c.get("text", ""),
            }
            for c in chunks
        ],
        "answer": answer,
    }
    path = THREADS_DIR / f"thread_{timestamp}.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(thread, f, indent=2)
    return path


def load_threads() -> List[Dict[str, Any]]:
    if not THREADS_DIR.exists():
        return []
    items: List[Dict[str, Any]] = []
    for p in sorted(THREADS_DIR.glob("thread_*.json")):
        try:
            with p.open(encoding="utf-8") as f:
                data = json.load(f)
                data["_path"] = str(p)
                items.append(data)
        except Exception:
            continue
    return list(reversed(items))


def render_answer_with_citations(answer: str, manifest: pd.DataFrame) -> None:
    st.markdown("#### Answer")
    st.write(answer)

    cites = parse_citations(answer)
    if manifest.empty or not cites:
        return

    st.markdown("#### Citations")
    for pair in cites:
        sid, cid = pair.split(",", 1)
        row = manifest[manifest["source_id"] == sid].head(1)
        title = row["title"].iloc[0] if not row.empty else "(unknown title)"
        url = row["url_or_doi"].iloc[0] if (not row.empty and "url_or_doi" in row) else ""
        label = f"{sid} — {title}"
        if url and isinstance(url, str) and url not in ("n/a", "N/A"):
            st.markdown(f"- **{label}** — `{cid}` — [{url}]({url})")
        else:
            st.markdown(f"- **{label}** — `{cid}`")


def build_evidence_table(thread: Dict[str, Any]) -> pd.DataFrame:
    rows = []
    answer = thread.get("answer", "")
    retrieved = thread.get("retrieved_chunks", [])
    for c in retrieved:
        sid = c.get("source_id", "")
        cid = c.get("chunk_id", "")
        text = c.get("text", "").replace("\n", " ").strip()
        snippet = text[:280] + "..." if len(text) > 280 else text
        rows.append(
            {
                "Claim": f"Evidence related to: {thread.get('query', '')}",
                "Evidence snippet": snippet,
                "Citation (source_id, chunk_id)": f"({sid}, {cid})",
                "Confidence": "",
                "Notes": "",
            }
        )
    if not rows:
        rows.append(
            {
                "Claim": thread.get("query", ""),
                "Evidence snippet": "No evidence in corpus for this query.",
                "Citation (source_id, chunk_id)": "",
                "Confidence": "",
                "Notes": "",
            }
        )
    df = pd.DataFrame(rows)
    df.attrs["answer"] = answer
    return df


def export_evidence_table_csv(df: pd.DataFrame, thread: Dict[str, Any]) -> None:
    _ensure_dirs()
    ts = thread.get("timestamp", datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    out_path = OUTPUTS_DIR / f"evidence_table_{ts}.csv"
    df.to_csv(out_path, index=False)
    st.success(f"Saved CSV to {out_path}")


def export_thread_markdown(thread: Dict[str, Any], df: pd.DataFrame) -> None:
    _ensure_dirs()
    ts = thread.get("timestamp", datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    out_path = OUTPUTS_DIR / f"thread_{ts}.md"
    lines = []
    lines.append(f"# Research thread — {ts}")
    lines.append("")
    lines.append(f"**Query:** {thread.get('query', '')}")
    lines.append("")
    lines.append("## Answer")
    lines.append("")
    lines.append(thread.get("answer", ""))
    lines.append("")
    lines.append("## Evidence table")
    lines.append("")
    lines.append(df.to_markdown(index=False))
    out_path.write_text("\n".join(lines), encoding="utf-8")
    st.success(f"Saved Markdown to {out_path}")


def page_ask() -> None:
    st.header("Ask / Search")
    manifest = load_manifest()

    query = st.text_area("Enter your research question", height=80)
    model = st.selectbox("Generation mode", options=["ollama", "template"], index=0)

    if st.button("Run query", type="primary") and query.strip():
        with st.spinner("Retrieving and generating answer..."):
            chunks = retrieve(query, k=5)
            if not chunks:
                st.warning("No chunks retrieved. Did you run ingestion and build the index?")
                return
            st.markdown("#### Retrieved chunks")
            for c in chunks:
                st.markdown(
                    f"- `{c['chunk_id']}` (*{c['source_id']}*, score={c.get('score', 0):.3f}): "
                    f"{c['text'][:160]}..."
                )
            answer = generate(query, chunks, model=model)
            render_answer_with_citations(answer, manifest)
            path = save_thread(query, chunks, answer)
            st.info(f"Thread saved to: `{path}`")


def page_threads() -> None:
    st.header("Research Threads")
    manifest = load_manifest()
    threads = load_threads()
    if not threads:
        st.info("No threads saved yet. Run a query from the Ask/Search tab first.")
        return

    labels = [f"{t['timestamp']} — {t.get('query', '')[:80]}" for t in threads]
    idx = st.selectbox("Select a thread", options=list(range(len(threads))), format_func=lambda i: labels[i])
    thread = threads[idx]

    st.markdown(f"**Timestamp:** {thread['timestamp']}")
    st.markdown(f"**Query:** {thread.get('query', '')}")
    st.markdown("#### Retrieved chunks")
    for c in thread.get("retrieved_chunks", []):
        text = c.get("text", "").replace("\n", " ").strip()
        snippet = text[:200] + "..." if len(text) > 200 else text
        st.markdown(
            f"- `{c.get('chunk_id','')}` (*{c.get('source_id','')}*): {snippet}"
        )

    render_answer_with_citations(thread.get("answer", ""), manifest)

    st.markdown("### Artifacts & Export")
    df = build_evidence_table(thread)
    st.dataframe(df, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export evidence table (CSV)"):
            export_evidence_table_csv(df, thread)
    with col2:
        if st.button("Export thread summary (Markdown)"):
            export_thread_markdown(thread, df)


def page_eval() -> None:
    st.header("Evaluation")
    if not EVAL_RESULTS_PATH.exists():
        st.info(
            "No evaluation results found. Run `python -m src.eval.run_eval` "
            "from the repo root, then refresh this page."
        )
        return
    with EVAL_RESULTS_PATH.open(encoding="utf-8") as f:
        results = json.load(f)
    if not isinstance(results, list) or not results:
        st.warning("Evaluation results file is empty or malformed.")
        return

    df = pd.DataFrame(results)
    st.markdown("### Aggregate metrics")
    summary = (
        df.groupby("query_type")[["citation_precision", "answer_relevance"]]
        .mean()
        .rename_axis("query_type")
        .reset_index()
    )
    st.dataframe(summary, use_container_width=True)

    st.markdown("### Per-query results")
    st.dataframe(
        df[["query_id", "query_type", "citation_precision", "answer_relevance"]],
        use_container_width=True,
    )

    st.markdown("### Inspect example answer")
    idx = st.selectbox(
        "Select a query",
        options=list(range(len(results))),
        format_func=lambda i: f"{results[i]['query_id']} — {results[i]['query_text'][:80]}",
    )
    row = results[idx]
    st.markdown(f"**Query:** {row['query_text']}")
    st.markdown("**Answer:**")
    st.write(row["answer"])


def main() -> None:
    st.set_page_config(page_title="Personal Research Portal", layout="wide")
    st.title("Personal Research Portal")

    tab = st.sidebar.radio(
        "Navigation",
        options=["Ask / Search", "Threads & Artifacts", "Evaluation"],
    )

    if tab == "Ask / Search":
        page_ask()
    elif tab == "Threads & Artifacts":
        page_threads()
    else:
        page_eval()


if __name__ == "__main__":
    main()

