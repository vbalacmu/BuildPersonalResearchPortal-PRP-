## EXECUTIVE SUMMARY

Structured prompts (1B, 2B) outperformed baseline prompts (1A, 2A) across all metrics: **+33% groundedness** (3.0→4.0), **+60% citation quality** (2.5→4.0), **+33% usefulness** (3.0→4.0). Citation format requirements were the highest-impact intervention, transforming outputs from screening-grade to research-grade.

---

## 1. PATTERN ANALYSIS

**Baseline prompts (1A, 2A):** Scored 3.0/2.5/3.0 avg (groundedness/citation/usefulness). Produced screening-grade outputs with general references ("the paper"), incomplete citations (no page/section), and numbered lists instead of tables.

**Structured prompts (1B, 2B):** Scored 4.0/4.0/4.0 avg. Produced research-grade outputs with field-level attribution ("Abstract", "Purpose/Key findings"), verbatim quotes, and perfect table format compliance.

**Key improvement:** Structured prompts achieved 100% perfect scores (4/4) across all runs, while baseline prompts showed more variance. ChatGPT particularly benefited from format constraints—runs 5-8 all produced verbatim quotes with correct citations, but only structured prompts enforced table format.

**Finding:** Citation format requirements drove +60% improvement in citation quality (2.5→4.0), eliminating vague attribution and enabling precise verification.

---

## 2. FAILURE MODE BREAKDOWN

**Citation incompleteness (4/8 runs - all baseline):** General references without specific page/section/paragraph citations. Example: Run 1 stated "the paper" makes claims without citing abstract, introduction, or specific sections. Structured prompts fixed this with field-level attribution.

**Format non-compliance (4/8 runs - all baseline claim-evidence):** Runs 5 and 7 used numbered lists instead of required table format. While quotes were verbatim and citations correct, lack of standardization reduces integration efficiency. Structured prompts (6, 8) enforced table format perfectly.

**No paraphrasing errors:** All 8 runs used verbatim quotes—ChatGPT maintained quote fidelity even with baseline prompts. However, baseline lacked format standardization (lists vs. tables).

**Success in structured outputs:** 100% of structured runs (2, 4, 6, 8) achieved perfect 4/4 scores across all metrics. No hallucinations detected. Models respected source boundaries when given explicit format and citation constraints.

---

## 3. PHASE 2 DESIGN DECISIONS

### Essential Elements to Carry Forward

**1. Citation format requirements** (+60% improvement)
- Triage: Field-level attribution (Abstract, Purpose, Findings sections)
- Claim-evidence: `(source_id, chunk_id)` format
- Implementation: "For each claim, provide citation: (source_id, chunk_id, page_number)"

**2. Verbatim evidence extraction** (maintained quote fidelity)
- Require exact quotes ≤20 words
- No paraphrasing for claim-evidence pairs
- Implementation: "Extract exact quote from source (≤20 words). Do NOT paraphrase."

**3. Format constraints** (100% compliance with structured prompts)
- Table format for claim-evidence extraction
- Standardized field structure for triage (5 fields)
- Implementation: "Present findings in table: | Claim | Evidence | Citation |"

**4. Grounding constraints** (zero hallucinations)
- Only use information from retrieved chunks
- No background knowledge injection
- Implementation: "ONLY use information from provided chunks. If question requires information not in chunks, state: 'Not available in retrieved sources.'"

**5. Explicit uncertainty flagging** (improved transparency)
- Standardized language: "Not specified in provided text" / "Limitations not explicitly addressed"
- Flag missing vs. stated content
- Implementation: "If data is missing, state: 'Data not available in retrieved sources'"

### Phase 2 Success Criteria

Target score: 4/4 across all dimensions
- All claims traceable to retrieved chunks with field/section attribution
- Every claim has verifiable citation format
- Table format for structured extraction tasks
- Explicit statements when information is missing
- Consistent output structure across all queries

---

## 4. KEY EXAMPLES

**Best output - Run 4 (Triage, Structured):** Perfect citation practice with field-level attribution ("Purpose/Key findings"); verbatim quote for findings section; explicit statement on limitations ("not explicitly addressed"); all 5 fields complete and grounded. Score: 4/4/4.

**Weakest baseline - Run 1 (Triage, Baseline):** Accurate content but lacks specific citations—references "the paper" without page/section/field attribution. Cannot verify where contribution/findings claims appear. Score: 3/2/3. Run 2 (same paper, structured prompt) achieved 4/4/4 with field-level citations.

**Format compliance gap - Runs 5 vs. 6:** Both used verbatim quotes and correct citations, but Run 5 (baseline) used numbered list format while Run 6 (structured) used required table format. Structured prompt eliminated format variance and achieved 4/4/4.

---

## CONCLUSION

Structured prompts with explicit constraints (citation format, table structure, grounding rules) consistently produce research-grade outputs (4.0/4 avg) compared to baseline screening-grade summaries (3.0/2.5/3.0 avg). Citation format requirements and table structure enforcement were the highest-impact interventions (+60% citation improvement, 100% format compliance with structured prompts), transforming outputs from incomplete attribution to field-level verification. For Phase 2 RAG generation: carry forward all structured prompt elements—especially mandatory field/section citations, table format for extraction tasks, and verbatim quote requirements. ChatGPT maintained quote fidelity across all runs but required explicit format constraints to achieve consistent table structure.

---

**Papers Evaluated:**  
A: ScienceDirect SLR (Survey) | B: SHRM Data Brief (Empirical) | C: Mercatus Policy Brief (Benchmark) | D: Tan UBI Critique (Critique)

**Scoring (1-4):** 4=Research-grade | 3=Minor issues | 2=Partially correct | 1=Not usable

---
