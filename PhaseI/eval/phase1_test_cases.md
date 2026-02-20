# Phase 1 Test Cases

Four test cases total: 2 per task. Each test case is one concrete input (a specific paper or section) used for all prompt variants and models.

---

## Task 1: Paper triage

**Required output:** 5-field summary — Contribution, Method, Data, Findings, Limitations.

### Test case 1 — Paper A (survey)

- **ID:** `triage_case_a`
- **Description:** A survey paper on RAG evaluation / faithfulness metrics.
- **Input:** Use the abstract and introduction (or full text if short) of a survey on RAG evaluation. For reproducibility, we use a concrete excerpt below.
- **Source for Phase 1:** Excerpt from a survey-style document on RAG evaluation (stored in `eval/fixtures/` or provided as inline text in the run script).

**Fixture text (Paper A — survey excerpt):**

```
Title: Evaluating Faithfulness in Retrieval-Augmented Generation

Abstract: Retrieval-augmented generation (RAG) systems combine retrieval with large language models to produce answers grounded in retrieved documents. Evaluating whether such answers are faithful to the retrieved context is critical. We survey metrics for faithfulness evaluation, including natural language inference (NLI) based approaches, answer-level overlap metrics, and claim-level decomposition. We find that NLI-based metrics correlate poorly with human judgment on adversarial examples, while claim-level metrics are more interpretable but require claim extraction. No single metric dominates across all failure modes.

Introduction (excerpt): Faithfulness in RAG means that the model's answer does not contradict and is supported by the retrieved passages. Common evaluation approaches include: (1) using NLI models to score entailment between claims and context; (2) measuring n-gram or semantic overlap between generated and source text; (3) decomposing the answer into claims and verifying each against the context. Limitations of existing work include sensitivity to claim phrasing and lack of standardized benchmarks.
```

### Test case 2 — Paper B (empirical study)

- **ID:** `triage_case_b`
- **Description:** An empirical study comparing faithfulness metrics.
- **Input:** Use the abstract and method/findings sections of an empirical paper comparing metrics.
- **Source for Phase 1:** Excerpt below.

**Fixture text (Paper B — empirical excerpt):**

```
Title: How Do Faithfulness Metrics Fail? An Empirical Study

Abstract: We compare six faithfulness metrics on three RAG benchmarks. We find that BERTScore and NLI-based metrics disagree in 30% of cases; the main failure mode is short or paraphrased answers that NLI labels as entailed but humans mark as incomplete. We release a small adversarial set where all metrics fail.

Method: We use GPT-4 to generate answers from retrieved Wikipedia passages. We evaluate with: BERTScore (precision of answer tokens in context), NLI (claim-level with DeBERTa), and two answer-level NLI variants. We collect human judgments on 500 examples for correlation.

Findings: NLI-based metrics have higher precision but miss hallucinations that preserve semantic overlap. BERTScore is sensitive to length. Combining NLI with length normalization improves correlation with humans (r=0.72). Limitations: single model, English only.
```

---

## Task 2: Claim–evidence extraction

**Required output:** 5 rows with Claim | Direct quote/snippet | Citation (source_id, chunk_id).

### Test case 1 — Paper C (benchmark)

- **ID:** `claim_case_c`
- **Description:** A benchmark paper; extract claims and evidence from the provided chunks.
- **Context chunks (for citation):** We provide 2 chunks; citations must use (source_id, chunk_id).

**Chunk C1 (source_id: Bench2024, chunk_id: chunk_01):**  
"Faithfulness benchmarks typically consist of (1) a context document, (2) a generated answer, and (3) human-annotated labels indicating whether each sentence in the answer is supported or contradicted by the context. Popular benchmarks include TRUE and FActScore."

**Chunk C2 (source_id: Bench2024, chunk_id: chunk_02):**  
"A limitation of sentence-level annotation is that it does not capture partial support or multi-hop reasoning. Some benchmarks use claim-level decomposition: the model first extracts atomic claims from the answer, then each claim is verified against the context."

**Input for model:** The above two chunks, plus instruction to output 5 rows: Claim | Direct quote/snippet | Citation (source_id, chunk_id).

### Test case 2 — Paper D (critique)

- **ID:** `claim_case_d`
- **Description:** A critique paper; extract claims and supporting quotes from the provided chunks.
- **Context chunks:**

**Chunk D1 (source_id: Critique2023, chunk_id: chunk_01):**  
"NLI-based faithfulness metrics are known to be biased toward lexical overlap. When the model paraphrases the context, NLI models often still output entailment, leading to false positives. This has been reported in the NLI literature and carries over to RAG evaluation."

**Chunk D2 (source_id: Critique2023, chunk_id: chunk_02):**  
"Recommendations for practitioners: (1) use multiple metrics and inspect disagreements; (2) prefer claim-level over answer-level when interpretability matters; (3) add human calibration on a small set before trusting automated scores."

**Input for model:** The above two chunks, plus instruction to output 5 rows: Claim | Direct quote/snippet | Citation (source_id, chunk_id).

---

## Summary

| Task              | Test case ID   | Description        |
|-------------------|----------------|--------------------|
| Paper triage      | triage_case_a  | Paper A (survey)   |
| Paper triage      | triage_case_b  | Paper B (empirical)|
| Claim–evidence    | claim_case_c   | Paper C (benchmark)|
| Claim–evidence    | claim_case_d   | Paper D (critique) |

All four test cases are run with Prompt A and Prompt B, and with both models, yielding 16 runs.
