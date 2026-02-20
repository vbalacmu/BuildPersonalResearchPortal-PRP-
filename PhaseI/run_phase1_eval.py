#!/usr/bin/env python3
"""
Phase 1 evaluation: 16 runs = 2 tasks x 2 test cases x 2 prompt variants x 2 models.
Saves outputs to logs/phase1_runs/ as run_{task}_{case}_{prompt}_{model}.txt.
Requires OPENAI_API_KEY and ANTHROPIC_API_KEY in the environment (or set --mock to write placeholders).
"""

import os
import sys
from pathlib import Path

# Fixture text for test cases — Paper A (Nigar survey), B (SHRM empirical), C (Sharfuddin), D (Tan)
TRIAGE_CASE_A = """Title: Artificial intelligence and technological unemployment: Understanding trends, technology's adverse roles, and current mitigation guidelines (Nigar et al., 2025)

Abstract: As artificial intelligence (AI) and automation continue to reshape industries, concerns about technological unemployment are intensifying. This study employs a Systematic Literature Review (SLR) guided by the PRISMA framework to examine peer-reviewed literature from the Scopus database (2015–July 09, 2025). It identifies three core themes: (1) trends in AI-induced labor displacement, including task automation, skill polarization, and industry-specific disruptions in sectors such as healthcare, education, and creative industries; (2) the adverse roles of AI technologies, particularly in affecting white-collar professionals, gig workers, and freelancers by increasing precarity and skill mismatches; and (3) existing mitigation strategies, including responsible AI guidelines proposed by governments, institutions, and firms aimed at balancing technological advancement with employment protection. While a growing body of policy responses encourages human-AI complementarity, current measures remain fragmented and insufficient to address the structural risks of workforce displacement. This study presents a comprehensive synthesis of the evolving relationship between AI and employment, highlighting key areas for further inquiry and policy development.

Introduction (excerpt): The development of cognitive robots driven by artificial intelligence and modern information technologies has drastically changed people's lives and careers. Traditionally, economic theories and labor market dynamics have been employed to examine unemployment, with an emphasis on human adaptability, education, and skill development. However, the emergence of AI impacts the existing employment theories. Examining how AI affects employment patterns reveals a paradigm shift that reshapes the workforce, raising concerns about job displacement for workers and policymakers, as well as opportunities for innovation."""

TRIAGE_CASE_B = """Title: Automation, Generative AI, and Job Displacement Risk in U.S. Employment (SHRM Data Brief)

PURPOSE: How will advances in automation technology and generative AI reshape the world of work? As a first step toward improving our knowledge in this area, SHRM fielded a large-scale survey of U.S. workers in the spring of 2025 (SHRM 2025 Automation/AI Survey). With over 20,000 individual respondents, this survey represents a significant step forward in our understanding of current automation and generative AI use levels for individual occupations, as well as the presence of nontechnical barriers to automation displacement and worker attitudes about displacement risk. This data brief focuses on estimating the prevalence of "high" (≥ 50%) task completion via automation and generative AI in U.S. employment, as well as the prevalence of nontechnical barriers to automation displacement.

Key findings: We estimate that at least 50% of tasks are automated in 15.1% of U.S. employment (23.2 million jobs). We also find that 63.3% of jobs include at least one nontechnical barrier that would prevent automation displacement. While advances in AI create significant displacement risk for a small fraction of workers, job transformation will be much more common."""

CLAIM_CASE_C_CHUNKS = """Chunk (source_id: Sharfuddin2025, chunk_id: chunk_01):
The current tax framework creates a profound asymmetry between physical and human capital investment. Through bonus depreciation under section 168(k)—a tax provision that allows immediate write-offs of equipment costs—businesses can expense a robot or an AI server in the year it is purchased, yet they must navigate a maze of restrictions to deduct the cost of retraining the people expected to use that technology. This asymmetric treatment skews business investment decisions away from economic merit and toward tax advantages, leading to systematic underinvestment in human capital development.

Chunk (source_id: Sharfuddin2025, chunk_id: chunk_02):
Six major restrictions in the Internal Revenue Code (IRC) create bottlenecks that effectively penalize businesses for investing in human capital. These restrictions were designed for a different era and have long undermined the flexibility firms need to adapt to today's AI-driven economy. IRC section 162 and associated guidance disallow deductions for employee education when the coursework "is needed to meet the minimum educational requirements of your present trade or business." Originally intended as a safeguard against tax abuse, this provision now undermines the competitive flexibility essential in an economy reshaped by AI."""

CLAIM_CASE_D_CHUNKS = """Chunk (source_id: Tan2025, chunk_id: chunk_01):
The increasing sophistication of artificial intelligence (AI) and automation technologies has precipitated significant debate regarding their potential to cause widespread job displacement. This paper critically examines the proposition that Universal Basic Income (UBI) or other forms of guaranteed basic income (GBI) could serve as a comprehensive solution to the challenges posed by such technological unemployment. Through a synthesis of existing empirical evidence from BI/GBI pilot programs, a nuanced perspective is presented. It is argued that while basic income demonstrates considerable promise in alleviating poverty, enhancing economic security, and improving certain well-being outcomes, its efficacy as a singular panacea is limited.

Chunk (source_id: Tan2025, chunk_id: chunk_02):
The paper concludes that basic income is more appropriately viewed as a potentially crucial component within a broader, multifaceted policy framework designed to navigate the future of work. This framework should also encompass robust investments in education and skills development, active labour market policies, and strategies to ensure the equitable distribution of productivity gains from automation."""

# Prompts (from report/phase1_prompt_kit.md)
PROMPT_TRIAGE_A = "Summarize this paper in 5 fields: Contribution, Method, Data, Findings, Limitations."

PROMPT_TRIAGE_B = """You are a research assistant performing paper triage for a policy analysis on AI, automation, and job displacement.

INPUT: [paste paper section below]

OUTPUT REQUIREMENTS (exactly 5 fields):
1. Contribution: What novel claim, policy proposal, or empirical finding does this paper make?
2. Method: What research approach was used? (literature review, empirical analysis, policy proposal, theoretical argument)
3. Data: What evidence, datasets, or case studies validate the claims? If none, state "No empirical data provided."
4. Findings: What are the key results or conclusions?
5. Limitations: What does the paper acknowledge as limitations, gaps, or areas for future work? If not discussed, state "Limitations not explicitly addressed."

CONSTRAINTS:
- If a field is not addressed in the provided text, write "Not specified in provided text"
- Do not infer beyond what is explicitly stated
- If the paper makes claims without evidence, note this in the Data field"""

PROMPT_CLAIM_A = "Extract 5 claims from this paper with supporting evidence and citations."

PROMPT_CLAIM_B = """You are extracting verifiable claims for a research database on AI/automation policy and job displacement.

INPUT: [paste paper section below]

OUTPUT: Table with exactly 5 rows, each containing:
| Claim | Direct Quote/Snippet | Citation (source_id, chunk_id) |

CONSTRAINTS:
- Use only the (source_id, chunk_id) labels provided with each chunk.
- Quote must be verbatim or near-verbatim from the chunks.
- If you cannot support a claim with a quote from the chunks, write "no evidence" in the Citation column.
- Do not invent citations."""


def get_run_config():
    """Yield (task, case_id, case_input, prompt_id, prompt_text) for each of 8 task/case/prompt combos."""
    # Task 1: Paper triage (2 cases, 2 prompts)
    yield ("triage", "triage_case_a", TRIAGE_CASE_A, "a", PROMPT_TRIAGE_A)
    yield ("triage", "triage_case_a", TRIAGE_CASE_A, "b", PROMPT_TRIAGE_B)
    yield ("triage", "triage_case_b", TRIAGE_CASE_B, "a", PROMPT_TRIAGE_A)
    yield ("triage", "triage_case_b", TRIAGE_CASE_B, "b", PROMPT_TRIAGE_B)
    # Task 2: Claim–evidence (2 cases, 2 prompts)
    yield ("claim", "claim_case_c", CLAIM_CASE_C_CHUNKS, "a", PROMPT_CLAIM_A)
    yield ("claim", "claim_case_c", CLAIM_CASE_C_CHUNKS, "b", PROMPT_CLAIM_B)
    yield ("claim", "claim_case_d", CLAIM_CASE_D_CHUNKS, "a", PROMPT_CLAIM_A)
    yield ("claim", "claim_case_d", CLAIM_CASE_D_CHUNKS, "b", PROMPT_CLAIM_B)


def build_message(prompt_text: str, case_input: str) -> str:
    return f"{prompt_text}\n\n---\n\n{case_input}"


def call_openai(user_message: str) -> str:
    from openai import OpenAI
    client = OpenAI()
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_message}],
        temperature=0,
    )
    return r.choices[0].message.content or ""


def call_anthropic(user_message: str) -> str:
    from anthropic import Anthropic
    client = Anthropic()
    r = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": user_message}],
    )
    return (r.content[0].text if r.content else "") or ""


def run_one(task: str, case_id: str, case_input: str, prompt_id: str, prompt_text: str, model: str, out_dir: Path, mock: bool) -> str:
    user_message = build_message(prompt_text, case_input)
    out_name = f"run_{task}_{case_id}_{prompt_id}_{model}.txt"
    out_path = out_dir / out_name

    if mock:
        out_path.write_text(f"[MOCK] Run: {task} / {case_id} / prompt_{prompt_id} / {model}\nNo API call made. Set OPENAI_API_KEY and ANTHROPIC_API_KEY and run without --mock for real outputs.", encoding="utf-8")
        return "[MOCK]"

    try:
        if model == "openai":
            output = call_openai(user_message)
        else:
            output = call_anthropic(user_message)
    except Exception as e:
        output = f"ERROR: {type(e).__name__}: {e}"
    out_path.write_text(output, encoding="utf-8")
    return output


def main():
    mock = "--mock" in sys.argv
    repo_root = Path(__file__).resolve().parent
    out_dir = repo_root / "logs" / "phase1_runs"
    out_dir.mkdir(parents=True, exist_ok=True)

    models = ["openai", "anthropic"]
    count = 0
    for task, case_id, case_input, prompt_id, prompt_text in get_run_config():
        for model in models:
            run_one(task, case_id, case_input, prompt_id, prompt_text, model, out_dir, mock)
            count += 1
    print(f"Wrote {count} runs to {out_dir}")


if __name__ == "__main__":
    main()
