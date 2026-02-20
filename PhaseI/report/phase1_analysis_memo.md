# Phase 1 Analysis Memo

**1–2 pages:** patterns, failure modes, actionable takeaways, and Phase 2 design choices.

---

## 1. Patterns

- **Prompt B vs Prompt A:** [Summarize: did structured/guardrailed prompts (B) improve groundedness and citation correctness over baseline (A)? Which task showed the biggest gap?]
- **Model comparison:** [Summarize: OpenAI vs Anthropic — consistency, citation format adherence, "unknown"/"no evidence" behavior.]
- **Task:** [Triage vs claim–evidence: which was harder to score? Where did models fail more often?]

---

## 2. Failure modes (3–5 representative cases)

For each, cite run ID (e.g. run 12 = claim, claim_case_c, prompt b, anthropic) and failure tag.

1. [Example: Run 12 — wrong_citation; model cited chunk_02 but quote was from chunk_01.]
2. [Example: Run 3 — no_uncertainty; left Limitations blank instead of "not stated".]
3. [Add 1–3 more with run ID + tag + one sentence.]

---

## 3. Actionable takeaways

- **Prompts to reuse in Phase 2:** [e.g. Prompt B for both triage and claim–evidence; exact wording from prompt kit.]
- **Guardrails that worked:** [e.g. "unknown"/"not stated" for missing fields; "no evidence" for unsupported claims.]
- **What to monitor in RAG:** [e.g. citation resolution to real chunk IDs; refusing to invent citations.]

---

## 4. Phase 2 design choices

- **Generation prompt:** [Which variant (A or B) will drive RAG answer generation? Why?]
- **Evaluation:** [How will you reuse this rubric and failure tags for Phase 2 evaluation?]
- **Trust behavior:** [Refuse to invent citations; flag missing/conflicting evidence — how did Phase 1 inform this?]

---

*Fill this after completing the evaluation sheet. Keep to 1–2 pages; be specific with run IDs and tags.*
