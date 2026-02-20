# Phase 1 Comprehensive Plan — No Stone Unturned

This plan maps every Phase 1 deliverable and grading criterion to concrete tasks and verification steps. Follow in order for submission-ready Phase 1.

---

## 1. Grading alignment (what graders check)

| Criterion | Points | What to deliver |
|-----------|--------|-----------------|
| **Framing quality and scope discipline** | 3 | Clear domain, main question, sub-questions, in/out scope in framing brief. |
| **Prompt kit quality** | 4 | Structured prompts, guardrails, reusable prompt cards (Appendix A1 style). |
| **Evaluation rigor and analysis** | 3 | Consistent scoring (1–4), failure tags, written justification, actionable analysis memo. |

**Phase 1 deliverables (submit together):**

1. Framing brief (1–2 pages)  
2. Prompt kit (Markdown): prompts + why each constraint exists  
3. Evaluation sheet (CSV or Markdown table): 16 rows — one per run — with scores + notes  
4. Analysis memo (1–2 pages): patterns, failures, Phase 2 design choices  

---

## 2. MVP checklist (in order)

### 2.1 Framing brief — DONE ✓

- [x] **Domain** stated (e.g. Trustworthy RAG evaluation methods).  
- [x] **Main research question** one sentence.  
- [x] **4–6 sub-questions** that break the main question into retrievable parts.  
- [x] **Scope**: what you include / exclude (in scope / out of scope).  
- [x] **Chosen tasks** (2 from task menu) and why they support citations.  
- [ ] **Verify**: File `report/phase1_framing_brief.md` is 1–2 pages; no mid-phase change to question (continuity for Phase 2).

---

### 2.2 Test cases — DONE ✓

- [x] **2 test cases per task** → 4 total.  
- [x] Each test case = one concrete input (e.g. specific paper/section or labeled chunks).  
- [x] IDs used: e.g. `triage_case_a`, `triage_case_b`, `claim_case_c`, `claim_case_d`.  
- [x] Fixture text or chunks documented (in `eval/phase1_test_cases.md` and in `run_phase1_eval.py`).  
- [ ] **Verify**: Every test case is used in the run script for both prompt variants and both models.

---

### 2.3 Prompt variants — DONE ✓

- [x] **Prompt A (baseline)** and **Prompt B (improved)** per task.  
- [x] Prompt B has: structure, guardrails, “cite chunk_id” / “say unknown when missing” where applicable.  
- [x] Prompt kit documents: intent, inputs, outputs, constraints, when to use, failure modes (Appendix A1 style).  
- [ ] **Verify**: Exact prompt text in `report/phase1_prompt_kit.md` matches strings in `run_phase1_eval.py`.

---

### 2.4 Run all 16 combinations — SCRIPT READY ✓

- [x] **2 tasks × 2 test cases × 2 prompts × 2 models = 16 runs.**  
- [x] Script: `run_phase1_eval.py`; outputs to `logs/phase1_runs/` as `run_{task}_{case}_{prompt}_{model}.txt`.  
- [ ] **Do**: Set `OPENAI_API_KEY` and `ANTHROPIC_API_KEY`; run `python run_phase1_eval.py` (no `--mock`).  
- [ ] **Verify**: 16 files in `logs/phase1_runs/`; no `ERROR:` in content; filenames follow convention.

**Run matrix (for your records):**

| # | Task   | Test case     | Prompt | Model    | Output file |
|---|--------|---------------|--------|----------|-------------|
| 1 | triage | triage_case_a | a      | openai   | run_triage_triage_case_a_a_openai.txt |
| 2 | triage | triage_case_a | a      | anthropic| run_triage_triage_case_a_a_anthropic.txt |
| 3 | triage | triage_case_a | b      | openai   | run_triage_triage_case_a_b_openai.txt |
| 4 | triage | triage_case_a | b      | anthropic| run_triage_triage_case_a_b_anthropic.txt |
| 5 | triage | triage_case_b | a      | openai   | … |
| 6 | triage | triage_case_b | a      | anthropic| … |
| 7 | triage | triage_case_b | b      | openai   | … |
| 8 | triage | triage_case_b | b      | anthropic| … |
| 9 | claim  | claim_case_c  | a      | openai   | … |
|10 | claim  | claim_case_c  | a      | anthropic| … |
|11 | claim  | claim_case_c  | b      | openai   | … |
|12 | claim  | claim_case_c  | b      | anthropic| … |
|13 | claim  | claim_case_d  | a      | openai   | … |
|14 | claim  | claim_case_d  | a      | anthropic| … |
|15 | claim  | claim_case_d  | b      | openai   | … |
|16 | claim  | claim_case_d  | b      | anthropic| … |

---

### 2.5 Evaluation sheet — TO DO

- [ ] **Create** `eval/phase1_evaluation_sheet.csv` (or `phase1_evaluation_sheet.md`).  
- [ ] **One row per run (16 rows).** Columns (minimum):  
  - `run_id` or `task`, `test_case`, `prompt_id`, `model`  
  - `score_groundedness` (1–4)  
  - `score_citation` (1–4) — N/A or dash for triage-only runs if you don’t assess citation there; for claim–evidence, required  
  - `score_usefulness` (1–4) — optional but recommended  
  - `notes` — 1–2 sentences justification  
  - `failure_tag` — e.g. missing_evidence, wrong_citation, overconfident, fabricated_citation, wrong_structure, other  

**Rubric (1–4) to apply:**

| Score | Meaning |
|-------|--------|
| 4 | Correctly grounded and structured; citations correct; uncertainty stated when evidence weak. |
| 3 | Mostly correct and structured; minor missing nuance OR minor citation/format issues. |
| 2 | Partially correct; key omissions OR weak grounding OR vague citations. |
| 1 | Not usable; hallucinated claims, fabricated citations, or fails required structure. |

- [ ] **Fill the sheet** by reading each of the 16 output files and scoring with **written justification** (so graders see what you observed).  
- [ ] **Verify**: No row left blank; every score has a short note; failure tags used consistently.

---

### 2.6 Analysis memo — TO DO

- [ ] **Create** `report/phase1_analysis_memo.md` (1–2 pages).  
- [ ] **Include:**  
  1. **Patterns**: e.g. Prompt B vs A, model A vs B, task triage vs claim–evidence.  
  2. **Failure modes**: 3–5 representative failures with reference to run_id and failure_tag.  
  3. **Actionable takeaways**: what to reuse in Phase 2 (prompts, guardrails, output formats).  
  4. **Phase 2 design choices**: which prompt variant to use for RAG generation; what to monitor (citation correctness, “no evidence” behavior).  
- [ ] **Verify**: Memo is 1–2 pages; cites evaluation sheet and specific runs; no generic filler.

---

## 3. Deliverables checklist (submission)

| Deliverable | Location | Status |
|-------------|----------|--------|
| Framing brief (1–2 pp) | `report/phase1_framing_brief.md` | ✓ |
| Prompt kit (Markdown) | `report/phase1_prompt_kit.md` | ✓ |
| Evaluation sheet (16 rows) | `eval/phase1_evaluation_sheet.csv` or `.md` | To do |
| Analysis memo (1–2 pp) | `report/phase1_analysis_memo.md` | To do |
| 16 run outputs | `logs/phase1_runs/*.txt` | After running script |
| Run script | `run_phase1_eval.py` | ✓ |
| Dependencies | `requirements.txt` | ✓ |

---

## 4. Repo and run hygiene

- [ ] **README**: At repo root or in PhaseI, add a short “Phase 1” section: how to run `run_phase1_eval.py`, where outputs and evaluation sheet live, and where reports are.  
- [ ] **One-command run**: `python run_phase1_eval.py` from `PhaseI/` (or repo root with path).  
- [ ] **Pinned deps**: `requirements.txt` with versions (e.g. `openai>=1.0.0`, `anthropic>=0.18.0`) — already present.  
- [ ] **Folders**: `report/`, `eval/`, `logs/phase1_runs/` exist; create `logs/` and `logs/phase1_runs/` if the script will create them on first run.

---

## 5. Common mistakes to avoid (from brief)

- [ ] **Tasks that don’t force citations** — You have claim–evidence; ensure citation column and (source_id, chunk_id) are actually scored.  
- [ ] **Scoring without written justification** — Every row in the evaluation sheet must have notes so graders see what you observed.  
- [ ] **Changing the main question mid-phase** — Lock the framing brief question; Phase 2 will reuse it.

---

## 6. Stretch goals (optional)

- **3rd model**: Add one more model in `run_phase1_eval.py`; extend evaluation sheet to 24 runs (2×2×2×3).  
- **Adversarial tests**: One extra test case per task designed to stress failure (e.g. too little context, conflicting chunks).  
- **Automated checks**: Script that parses outputs and checks (e.g. triage has 5 field labels; claim–evidence has 5 rows and citation column).  
- **Uncertainty calibration**: Note when models say “unknown”/“no evidence” and compare to human expectation.

---

## 7. Execution order (summary)

1. **Confirm** framing brief, prompt kit, and test cases (sections 2.1–2.3).  
2. **Run** `python run_phase1_eval.py`; confirm 16 files in `logs/phase1_runs/`.  
3. **Create** evaluation sheet template; score all 16 runs with rubric + notes + failure tags.  
4. **Write** analysis memo (patterns, failures, takeaways, Phase 2 choices).  
5. **Add** README Phase 1 instructions and verify repo structure.  
6. **Final check**: All four deliverables present; evaluation sheet has 16 rows with justification; analysis memo 1–2 pages and specific.

---

*This plan is keyed to the Individual Project PRP brief and Phase 1 grading criteria. Use it as the single checklist for Phase 1 so no deliverable or criterion is missed.*
