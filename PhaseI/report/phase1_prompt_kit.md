**Domain:** Job policy, regulation, AI/automation, and Universal Basic Income  
**Tasks:** Paper Triage + Claim-Evidence Extraction

---

## TASK 1: PAPER TRIAGE

### Prompt 1A (Baseline)

```
Summarize this paper in 5 fields: Contribution, Method, Data, Findings, Limitations.
```

---

### Prompt 1B (Structured)

```
You are a research assistant performing paper triage for a policy analysis on AI, automation, and job displacement.

INPUT: [paste paper section below]

OUTPUT REQUIREMENTS (exactly 5 fields):
1. Contribution: What novel claim, policy proposal, or empirical finding does this paper make?
2. Method: What research approach was used? (literature review, empirical analysis, policy proposal, theoretical argument)
3. Data: What evidence, datasets, or case studies validate the claims? If none, state "No empirical data provided."
4. Findings: What are the key results or conclusions? Cite specific sections or paragraph numbers.
5. Limitations: What does the paper acknowledge as limitations, gaps, or areas for future work? If not discussed, state "Limitations not explicitly addressed."

CONSTRAINTS:
- Cite specific sections using (SectionName, paragraph_number) format
- If a field is not addressed in the provided text, write "Not specified in provided text"
- Do not infer beyond what is explicitly stated
- If the paper makes claims without evidence, note this in the Data field
- Flag any instance where policy recommendations lack empirical grounding
```

**Why each constraint exists:**

- **"Cite specific sections using (SectionName, paragraph_number) format"** → Forces traceable citations; prevents vague "the paper says..." references; enables verification against source
- **"Write 'Not specified in provided text'"** → Prevents hallucination when information is missing; trains model to acknowledge gaps rather than invent content
- **"Do not infer beyond what is explicitly stated"** → Ensures groundedness; stops models from making logical leaps or assumptions not supported by text
- **"Note when claims lack evidence"** → Flags methodological weakness; critical for policy analysis where unsupported claims are common
- **"Flag policy recommendations lacking empirical grounding"** → Directly addresses domain concern (policy debates often cite ideology not evidence)

---

## TASK 2: CLAIM-EVIDENCE EXTRACTION

### Prompt 2A (Baseline)

```
Extract 5 claims from this paper with supporting evidence and citations.
```

---

### Prompt 2B (Structured)

```
You are extracting verifiable claims for a research database on AI/automation policy and job displacement.

INPUT: [paste paper section below]

OUTPUT: Table with exactly 5 rows, each containing:
| Claim | Direct Quote/Snippet | Citation (section, para) |

CLAIM DEFINITION: A claim must be:
- Empirical (testable/verifiable with data) OR
- A specific policy argument with stated reasoning

CONSTRAINTS:
- Quote must be <= 20 words, verbatim from text
- Citation format: (SectionName, para_X) where X is paragraph number within that section
- If fewer than 5 verifiable claims exist, fill remaining rows with "N/A | N/A | N/A"
- Never paraphrase the evidence quote—it must be word-for-word from source
- Do NOT extract vague claims like "AI will affect jobs"—be specific (sectors, timelines, magnitudes)
- Flag claims that lack supporting evidence in the "Direct Quote/Snippet" column by writing "[NO EVIDENCE PROVIDED]"

EXAMPLE ROW:
| 76,440 positions eliminated by AI in 2025 | "76,440 positions already eliminated in 2025" | (Introduction, para_3) |

```

**Why each constraint exists:**

- **"Quote must be <= 20 words, verbatim from text"** → Prevents paraphrasing errors; ensures evidence is directly traceable; forces extraction not interpretation
- **"Citation format: (SectionName, para_X)"** → Standardizes citations for Phase 2 RAG use; enables automated verification; matches research database requirements
- **"Fill remaining rows with N/A"** → Handles edge case where papers make <5 claims; prevents model from inventing claims to reach quota
- **"Never paraphrase—word-for-word from source"** → Critical anti-hallucination measure; paraphrasing introduces interpretation errors and untraceable modifications
- **"Do NOT extract vague claims—be specific"** → Domain-specific filter; policy debates full of platitudes ("AI changes everything"); we need measurable, testable claims
- **"Flag claims lacking evidence with [NO EVIDENCE PROVIDED]"** → Identifies argumentative vs. empirical claims; critical for assessing source quality in policy analysis
- **"CLAIM DEFINITION: Empirical OR specific policy argument"** → Scopes extraction to useful claim types; excludes opinions, background info, transitions
