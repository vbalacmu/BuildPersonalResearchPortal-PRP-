# Phase 1 — Prompt the Research Domain

Personal Research Portal (PRP), Phase 1: domain framing, prompt kit, and evaluation of model behavior on research tasks.

## Quick start

```bash
cd PhaseI
pip install -r requirements.txt
export OPENAI_API_KEY="..."
export ANTHROPIC_API_KEY="..."
python run_phase1_eval.py
```

Outputs are written to `logs/phase1_runs/` (16 files). Use `--mock` to skip API calls and write placeholder files.

## Deliverables

| Item | Location |
|------|----------|
| Framing brief (1–2 pp) | `report/phase1_framing_brief.md` |
| Prompt kit | `report/phase1_prompt_kit.md` |
| Test cases | `eval/phase1_test_cases.md` |
| Evaluation sheet (16 rows) | `eval/phase1_evaluation_sheet.csv` or `eval/phase1_evaluation_sheet.md` |
| Outputs table (16 runs) | `eval/phase1_outputs_table.md` |
| Analysis memo (1–2 pp) | `report/phase1_analysis_memo.md` |
| Run outputs | `logs/phase1_runs/*.txt` |
| Plan (checklist) | `PHASE1_PLAN.md` |

## Scope

- **Domain:** Job policy, AI/automation, UBI  
- **Tasks:** Paper triage (5-field summary); Claim–evidence extraction (5 rows with citations)  
- **Runs:** 2 tasks × 2 test cases × 2 prompt variants × 2 models = 16  

**Real API runs:** If `pip install` fails (externally-managed environment), use a venv: `python3 -m venv .venv && source .venv/bin/activate`, then `pip install -r requirements.txt`, set API keys, and run `python3 run_phase1_eval.py`. Then score each output and fill `eval/phase1_evaluation_sheet.md` (and `.csv`).  

See `PHASE1_PLAN.md` for the full Phase 1 checklist and grading alignment.
