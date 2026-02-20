# logs/

Machine-readable run logs for Phase 2:

- Query ID, query text, timestamp
- Retrieved chunk IDs (and optionally scores)
- Model output (answer with citations)
- Prompt/version ID, model name

At least 20 queries (from eval query set) with retrieved chunks and outputs.
Format: JSON lines (e.g. `runs.jsonl`) or one file per run; keep citations resolvable to data manifest.
