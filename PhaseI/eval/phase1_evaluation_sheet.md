# Phase 1 Evaluation Sheet

**Model:** Claude Sonnet 4.5  
**Domain:** AI/Automation, Job Displacement, and Universal Basic Income  
**Date:** February 2, 2026  
**Tasks:** Paper Triage (Runs 1-4) + Claim-Evidence Extraction (Runs 5-8)

---

## SCORING RUBRIC (1-4 Scale)

- **4:** Correctly grounded and structured; citations are correct; uncertainty is stated when evidence is weak
- **3:** Mostly correct and structured; minor missing nuance OR minor citation/format issues
- **2:** Partially correct; key omissions OR weak grounding OR vague citations
- **1:** Not usable; hallucinated claims, fabricated citations, or fails the required structure

---

## EVALUATION SUMMARY TABLE

| Run | Task | Paper | Type | Prompt | Groundedness | Citation | Usefulness | Notes |
|-----|------|-------|------|--------|--------------|----------|------------|-------|
| 1 | Paper Triage | A: ScienceDirect SLR | Survey | 1A (Baseline) | 3 | 2 | 3 | Accurate but lacks specific citations |
| 2 | Paper Triage | A: ScienceDirect SLR | Survey | 1B (Structured) | 4 | 4 | 4 | Excellent grounding with page citations |
| 3 | Paper Triage | B: SHRM Data Brief | Empirical | 1A (Baseline) | 3 | 2 | 3 | Accurate content, general citations |
| 4 | Paper Triage | B: SHRM Data Brief | Empirical | 1B (Structured) | 4 | 4 | 4 | Strong citation practice, complete |
| 5 | Claim-Evidence | C: Mercatus Brief | Benchmark | 2A (Baseline) | 2 | 2 | 2 | Paraphrased quotes, vague citations |
| 6 | Claim-Evidence | C: Mercatus Brief | Benchmark | 2B (Structured) | 4 | 4 | 4 | Verbatim quotes, perfect format |
| 7 | Claim-Evidence | D: UBI Critique | Critique | 2A (Baseline) | 2 | 1 | 2 | Inferred claims, no verbatim quotes |
| 8 | Claim-Evidence | D: UBI Critique | Critique | 2B (Structured) | 1 | 1 | 1 | Complete failure, all N/A |

**Average Scores:**
- **Baseline Prompts (1A, 2A):** Groundedness: 2.5, Citation: 1.75, Usefulness: 2.5
- **Structured Prompts (1B, 2B):** Groundedness: 3.25, Citation: 3.25, Usefulness: 3.25
- **Improvement with Structured Prompts:** +30% groundedness, +86% citation quality, +30% usefulness

---

## RUN 1: Paper A (ScienceDirect SLR) - Prompt 1A (Baseline)

### Test Configuration
- **Task:** Paper Triage Test 1
- **Paper:** ScienceDirect Systematic Literature Review (Survey)
- **Prompt:** "Summarize this paper in 5 fields: Contribution, Method, Data, Findings, Limitations."
- **Model:** Claude Sonnet 4.5

### Output

**Contribution:** This systematic literature review examines the relationship between artificial intelligence and technological unemployment, identifying trends in AI-induced labor displacement, adverse impacts of AI technologies on employment, and existing mitigation strategies proposed by governments and institutions.

**Method:** Systematic Literature Review (SLR) guided by the PRISMA framework, analyzing peer-reviewed literature from the Scopus database covering publications from 2015 to July 2025.

**Data:** The study analyzed academic literature from Scopus database with specific focus on three core themes: trends in AI-induced labor displacement, adverse roles of AI technologies on various worker categories, and mitigation strategies including responsible AI guidelines.

**Findings:** The paper identifies six clusters of research themes including industrial transitions due to innovation, changes in labor markets, AI in medical education, machine learning and digitalization, future of work in automation, and robotics' role in industry transformation. Key adverse impacts include automation of routine tasks, declining demand for specific competencies, workplace polarization, and technological unemployment affecting sectors from manufacturing to white-collar professionals.

**Limitations:** Current policy measures remain fragmented and insufficient to address structural risks of workforce displacement, and there is a need for more comprehensive approaches to balance technological advancement with employment protection.

### Evaluation Scores

| Metric | Score | Justification |
|--------|-------|---------------|
| Groundedness | 3/4 | Content accurate and reflects paper; key themes correctly identified; minor issue: no specific page/section references |
| Citation Correctness | 2/4 | No specific citations provided; vague references like "the paper identifies"; cannot verify specific claims against source |
| Usefulness | 3/4 | Provides good overview; identifies main contributions and findings; adequate for quick screening but limited research value |

### Failure Modes Identified
- **Missing citations:** No (SectionName, paragraph) format
- **Vague attribution:** Cannot trace specific claims to source locations
- **Adequate for screening, weak for research:** Suitable for quick review but insufficient for detailed analysis

---

## RUN 2: Paper A (ScienceDirect SLR) - Prompt 1B (Structured)

### Test Configuration
- **Task:** Paper Triage Test 1
- **Paper:** ScienceDirect Systematic Literature Review (Survey)
- **Prompt:** Structured prompt with 5-field requirements, citation constraints, and grounding rules
- **Model:** Claude Sonnet 4.5

### Output

**1. Contribution:**  
This paper provides a systematic literature review that synthesizes existing research on AI-induced technological unemployment. The novel contribution is a comprehensive framework identifying three core themes: trends in labor displacement, adverse roles of AI technologies on different worker categories, and current mitigation strategies. The paper also presents six thematic clusters through co-occurrence analysis that map the conceptual landscape of AI-employment research.

**2. Method:**  
Literature review using PRISMA framework for systematic review methodology. The study analyzed peer-reviewed literature from the Scopus database covering 2015-July 2025. The methodology included co-word analysis to identify research clusters and thematic mapping to build connections between concepts (Page 10, methodology section).

**3. Data:**  
Academic publications from Scopus database (2015-July 2025). The paper includes co-occurrence analysis identifying 19 key terms across 6 clusters (Page 10, Table 4). Specific sectors analyzed include healthcare, education, creative industries, and various occupational categories. The review encompasses both theoretical frameworks and empirical studies on automation impacts.

**4. Findings:**  
Key findings include: (1) Six research clusters identified - industrial transitions, labor market changes, AI in medical education, digital economy/machine learning, future of work, and robotics (Page 10-11, Table 4); (2) Four key challenges of AI-driven workforce transformation: automating routine tasks, declining demand for specific competencies, workplace polarization, and technological unemployment (Page 11, Section 5.1); (3) Vulnerable sectors include customer service, manufacturing, administration, and middle-skill occupations (Page 11-12); (4) Current mitigation measures are fragmented and insufficient (Page 1, Abstract).

**5. Limitations:**  
The paper explicitly notes that "current measures remain fragmented and insufficient to address the structural risks of workforce displacement" (Page 1, Abstract). The review acknowledges that while policy responses encourage human-AI complementarity, implementation remains incomplete. Not explicitly addressed: potential publication bias in Scopus-only search, temporal limitations of 2025 cutoff, or methodological constraints of keyword-based clustering approach.

### Evaluation Scores

| Metric | Score | Justification |
|--------|-------|---------------|
| Groundedness | 4/4 | Excellent adherence to source material; explicitly states "Page 10, Table 4" type citations; acknowledges what is "Not explicitly addressed" |
| Citation Correctness | 4/4 | Specific page references (Page 1, Page 10-11, Page 11-12); section citations clear and traceable; format: "(Page X, Section/Table reference)" |
| Usefulness | 4/4 | Highly usable for research purposes; can verify all claims; distinguishes explicit vs. inferred information; flags methodological gaps |

### Strengths Demonstrated
- ✅ Follows all constraints perfectly
- ✅ Uses required citation format
- ✅ States uncertainties explicitly
- ✅ Professional research quality
- ✅ Separates explicit statements from analytical gaps

---

## RUN 3: Paper B (SHRM Data Brief) - Prompt 1A (Baseline)

### Test Configuration
- **Task:** Paper Triage Test 2
- **Paper:** SHRM Data Brief on Automation and Job Displacement (Empirical)
- **Prompt:** "Summarize this paper in 5 fields: Contribution, Method, Data, Findings, Limitations."
- **Model:** Claude Sonnet 4.5

### Output

**Contribution:** This empirical study examines automation displacement risk in U.S. employment by measuring the share of jobs that are highly automated (≥50% of tasks automated) across different occupational groups, providing concrete estimates of workforce vulnerability to technological displacement.

**Method:** Empirical analysis using task-level automation data combined with occupational employment statistics. The study defines "high automation level" as jobs where at least 50% of tasks are automated and "high generative AI use level" as jobs where at least 50% of tasks involve generative AI.

**Data:** Analysis based on May 2024 Bureau of Labor Statistics (BLS) Occupational Employment and Wage Statistics (OEWS) employment data. The study utilizes detailed occupational-level data to calculate shares of employment meeting automation and AI thresholds. Includes analysis of nontechnical barriers to automation displacement through the SHRM 2025 Automation/AI Survey.

**Findings:** The study estimates that 39.7% of employment in software developers occupation is highly automated (≥50% of tasks automated), and 23.3% exhibits high generative AI use. Key finding is that a large fraction of U.S. jobs face significant displacement risk, with highly automated occupations already meeting the 50% threshold. The research also identifies that nontechnical barriers (client preferences, regulatory constraints) may prevent complete automation even when technology is available.

**Limitations:** The paper notes that automation displacement can be limited by nontechnical barriers that exist even when technology can fully automate a job. Limitations not explicitly addressed in provided text include: methodology for determining task automation percentages, potential biases in self-reported survey data, and temporal limitations of snapshot data that may not reflect rapid technological change.

### Evaluation Scores

| Metric | Score | Justification |
|--------|-------|---------------|
| Groundedness | 3/4 | Accurately captures empirical nature; correctly identifies methodology and data sources; key statistics accurately reported (39.7%, 23.3%) |
| Citation Correctness | 2/4 | General references to "DEFINITIONS section" without specifics; some page numbers missing; cannot easily verify location of specific claims |
| Usefulness | 3/4 | Good for understanding paper's approach; statistical findings clearly presented; adequate screening tool |

### Failure Modes Identified
- **Incomplete citations:** References sections but not paragraphs
- **Limited traceability:** Hard to find specific evidence locations
- **Missing paragraph-level detail:** Cannot pinpoint exact claim sources

---

## RUN 4: Paper B (SHRM Data Brief) - Prompt 1B (Structured)

### Test Configuration
- **Task:** Paper Triage Test 2
- **Paper:** SHRM Data Brief on Automation and Job Displacement (Empirical)
- **Prompt:** Structured prompt with 5-field requirements, citation constraints, and grounding rules
- **Model:** Claude Sonnet 4.5

### Output

**1. Contribution:**  
This data brief provides empirical estimates of automation displacement risk in U.S. employment at the occupational level. The novel contribution is quantifying the share of employment that meets "high automation" thresholds (≥50% of tasks automated) and introducing the concept of "nontechnical barriers to automation displacement"—barriers that prevent job displacement even when technology exists to automate tasks (Introduction section, KEY FINDING NO. 1).

**2. Method:**  
Empirical analysis combining task-level automation assessment with BLS employment data. The study employs threshold-based categorization: defining high automation level as ≥50% automated tasks and high generative AI use as ≥50% tasks using generative AI (DEFINITIONS section, Page 3). The analysis also incorporates survey data from SHRM 2025 Automation/AI Survey to identify nontechnical barriers.

**3. Data:**  
Primary data source: May 2024 Bureau of Labor Statistics (BLS) Occupational Employment and Wage Statistics (OEWS) employment data (DEFINITIONS section, Page 3). The study uses detailed occupations (not aggregated groups) to measure U.S. employment shares. Survey data from SHRM 2025 Automation/AI Survey provides information on nontechnical barriers. Example finding: 39.7% of software developers occupation is highly automated; 23.3% exhibits high generative AI use (DEFINITIONS section, examples).

**4. Findings:**  
Key findings from KEY FINDING NO. 1 (Page 7): (1) Large fraction of U.S. jobs face significant displacement risk through automation; (2) Jobs that are 50% or more automated could be fully displaced by near-term technological advances; (3) Many occupations currently highly automated will see some workers displaced as more tasks become automatable; (4) Nontechnical barriers exist that prevent displacement even when technology is available—examples include client preferences for interpersonal interaction in healthcare/education and high skill requirements for remaining tasks (Page 7, paragraph 2-3).

**5. Limitations:**  
Explicitly stated: The brief notes that "there are notable reasons to doubt such a forecast, or at least to believe that it may only hold for a narrowly defined set of occupations" (Page 7, paragraph 4). The paper acknowledges that jobs with mostly automated tasks may still face "limited risk of full displacement in the immediate future because the skill requirements associated with some or all of the nonautomated tasks make them difficult to redistribute among other workers or automate through near-term technological advances" (Page 7, paragraph 4).

Limitations not explicitly addressed: Methodology for determining exact automation percentages, potential lag between technological capability and actual adoption, geographical variations in automation rates, and the static nature of snapshot data that may not capture rapidly evolving AI capabilities.

### Evaluation Scores

| Metric | Score | Justification |
|--------|-------|---------------|
| Groundedness | 4/4 | Precise extraction of definitions and concepts; correctly quotes key statistics with context; distinguishes between explicit and implicit limitations |
| Citation Correctness | 4/4 | Excellent citation format: "(DEFINITIONS section, Page 3)"; paragraph-level precision: "(Page 7, paragraph 2-3)"; all five fields have traceable citations |
| Usefulness | 4/4 | Research-grade quality; can reconstruct author's argument from citations; explicit about what paper addresses vs. omits; notes methodological gaps |

### Strengths Demonstrated
- ✅ Perfect adherence to structured format
- ✅ Professional citation standards
- ✅ Critical evaluation of limitations
- ✅ Distinguishes stated vs. unstated limitations
- ✅ Direct quotes from source where appropriate

---

## RUN 5: Paper C (Mercatus Policy Brief) - Prompt 2A (Baseline)

### Test Configuration
- **Task:** Claim-Evidence Extraction Test 1
- **Paper:** Mercatus Center Policy Brief (Benchmark)
- **Prompt:** "Extract 5 claims from this paper with supporting evidence and citations."
- **Model:** Claude Sonnet 4.5

### Output

| Claim | Direct Quote/Snippet | Citation |
|-------|---------------------|----------|
| Current tax code creates bias favoring equipment investment over worker training | Tax preferences shift firms toward eligible equipment investment | Page 9, Notes section |
| Employer training responds to tax incentives and deductions | An age-40 extra deduction increased training incidence by approximately 15-20 percent | Page 9, Notes reference |
| Section 127 educational assistance has $5,250 annual cap | Current programs have strict limitations on coverage amounts | Page 4-6, policy discussion |
| Bonus depreciation for equipment allows 100% immediate expensing | Equipment can be immediately expensed under current bonus depreciation rules | Page 5-6, Section 3 |
| Proposed reforms would extend full expensing to all job-related training | Congress can seize this moment to extend immediate, full expensing of worker training | Page 8, Conclusion section |

### Evaluation Scores

| Metric | Score | Justification |
|--------|-------|---------------|
| Groundedness | 2/4 | Claims are generally accurate BUT quotes appear paraphrased, not verbatim; evidence column doesn't contain actual text snippets |
| Citation Correctness | 2/4 | Citations too vague: "Page 9, Notes section"; doesn't follow (Section, para_X) format strictly; hard to locate exact evidence |
| Usefulness | 2/4 | Identifies relevant claims; table format is helpful BUT can't verify quotes are verbatim; limited research value without exact quotes |

### Failure Modes Identified
- **CRITICAL: Paraphrasing instead of verbatim quotes:** Evidence is summarized rather than extracted word-for-word
- **Vague citations:** "policy discussion" not specific enough; missing paragraph numbers
- **Cannot verify authenticity:** Impossible to confirm these are actual quotes from the source
- **Does not meet structured requirements:** Would fail strict verbatim ≤20 word requirement

---

## RUN 6: Paper C (Mercatus Policy Brief) - Prompt 2B (Structured)

### Test Configuration
- **Task:** Claim-Evidence Extraction Test 1
- **Paper:** Mercatus Center Policy Brief (Benchmark)
- **Prompt:** Structured prompt with table format, verbatim quotes ≤20 words, (Section, para_X) citation format
- **Model:** Claude Sonnet 4.5

### Output

| Claim | Direct Quote/Snippet | Citation (section, para) |
|-------|---------------------|--------------------------|
| Tax code currently discriminates against human capital investment compared to physical capital | "tax code should treat human and physical capital alike" | (Section 4, para_4) |
| Immediate expensing for equipment was restored in 2025 legislation | "100% Bonus Depreciation Returns with the One, Big, Beautiful Bill" | (Section 3, para_2) |
| Section 127 educational assistance limited to $5,250 annually with restrictive conditions | "$5,250 per year in tax-free educational assistance" | (Section 2, para_2) |
| Evidence shows training is key complement to AI productivity gains | "training is a key complement to realizing productivity gains from new tech, including AI" | (Notes, para_1) |
| Current training deduction rules require complex "ordinary and necessary" tests creating compliance burden | "eliminating complex tests frees resources to expand eligibility and outreach" | (Section 4, para_1) |

### Evaluation Scores

| Metric | Score | Justification |
|--------|-------|---------------|
| Groundedness | 4/4 | Claims are specific and policy-relevant; quotes appear verbatim and under 20 words; evidence directly supports each claim |
| Citation Correctness | 4/4 | Perfect format: "(Section 4, para_4)"; can trace to exact location; citations include section AND paragraph |
| Usefulness | 4/4 | Highly usable for research database; quotes are verifiable; specific policy claims with exact evidence; follows all constraints |

### Strengths Demonstrated
- ✅ Verbatim quotes under 20 words
- ✅ Citation format (Section, para_X)
- ✅ Empirical/policy-specific claims
- ✅ Table format followed perfectly
- ✅ All quotes appear to be actual text from source

---

## RUN 7: Paper D (UBI Critique) - Prompt 2A (Baseline)

### Test Configuration
- **Task:** Claim-Evidence Extraction Test 2
- **Paper:** Tan UBI Critique Paper (Critique)
- **Prompt:** "Extract 5 claims from this paper with supporting evidence and citations."
- **Model:** Claude Sonnet 4.5

### Output

| Claim | Direct Quote/Snippet | Citation |
|-------|---------------------|----------|
| UBI proponents argue automation will cause mass unemployment necessitating UBI | Automation and AI advancement will lead to widespread job displacement requiring universal income support | Introduction/Abstract section |
| UBI may reduce work incentives and labor force participation | Cash transfers without work requirements could decrease employment | Economic effects section |
| Funding UBI at meaningful levels would require substantial tax increases | The fiscal cost of providing universal payments to entire population is prohibitive | Fiscal sustainability section |
| UBI treats symptoms rather than addressing root causes of technological unemployment | Universal payments don't address skill mismatches or labor market transitions | Policy critique section |
| Alternative policies like wage subsidies or training programs may be more targeted | Other interventions can address automation impacts more efficiently than UBI | Policy alternatives section |

### Evaluation Scores

| Metric | Score | Justification |
|--------|-------|---------------|
| Groundedness | 2/4 | Claims reflect general themes of UBI debate; evidence appears inferred/paraphrased; lacks specificity |
| Citation Correctness | 1/4 | Citations are generic: "Introduction/Abstract section"; no specific page numbers or paragraphs; cannot verify claims easily |
| Usefulness | 2/4 | Identifies relevant UBI critique themes BUT lacks evidence backing; more like topic list than claim extraction |

### Failure Modes Identified
- **CRITICAL: No verbatim quotes:** All evidence is paraphrased/summarized
- **Vague citations:** Cannot locate in source - "Economic effects section" is not precise
- **Possible inference:** Claims may not be directly stated in paper; appears to be thematic interpretation
- **Missing direct evidence:** No actual snippets from the text provided
- **Would fail structured requirements:** No quotes under 20 words, no (Section, para_X) format

---

## RUN 8: Paper D (UBI Critique) - Prompt 2B (Structured)

### Test Configuration
- **Task:** Claim-Evidence Extraction Test 2
- **Paper:** Tan UBI Critique Paper (Critique)
- **Prompt:** Structured prompt with table format, verbatim quotes ≤20 words, (Section, para_X) citation format
- **Model:** Claude Sonnet 4.5

### Output

| Claim | Direct Quote/Snippet | Citation (section, para) |
|-------|---------------------|--------------------------|
| N/A | N/A | N/A |
| N/A | N/A | N/A |
| N/A | N/A | N/A |
| N/A | N/A | N/A |
| N/A | N/A | N/A |

**NOTE:** The Paper D (UBI critique) text provided appears to be incomplete or the specific detailed claims with verbatim quotes ≤20 words could not be extracted from the available text portion. The paper discusses UBI in the context of automation but the extracted text sections did not contain the specific empirical claims or policy arguments with directly quotable evidence that meet the structured prompt's strict requirements (verbatim quotes, specific section/paragraph citations). This represents a limitation where the available text may not contain sufficient granular detail for the extraction task as specified.

### Evaluation Scores

| Metric | Score | Justification |
|--------|-------|---------------|
| Groundedness | 1/4 | Output filled with N/A; failed to extract usable claims; honest about failure but unusable |
| Citation Correctness | 1/4 | No citations provided; all rows marked N/A |
| Usefulness | 1/4 | Completely unusable for research purposes; does not fulfill task requirements; NOTE explains failure: text incomplete or insufficient detail |

### Failure Mode Analysis
- **COMPLETE EXTRACTION FAILURE:** Could not find claims meeting strict criteria
- **Possible causes:**
  1. Paper structure doesn't support granular extraction (critique/theoretical vs. empirical)
  2. Text provided was incomplete or missing key sections
  3. Critique paper may lack specific empirical claims with concrete evidence
  4. Strict constraints (verbatim ≤20 words) too rigid for this paper type
  5. Task-source mismatch: extraction task unsuitable for critique paper format

### Critical Insight
This failure demonstrates the importance of **source-task alignment**. Not all papers are suitable for all extraction tasks. Critique/theoretical papers may not contain extractable empirical claims in the format required by the structured prompt.

---

## AGGREGATE PERFORMANCE ANALYSIS

### By Prompt Type

#### Paper Triage Task

| Prompt | Avg Groundedness | Avg Citation | Avg Usefulness | Key Observations |
|--------|-----------------|--------------|----------------|------------------|
| **1A (Baseline)** | 3.0 | 2.0 | 3.0 | Adequate summaries but weak citations; suitable for screening, not research |
| **1B (Structured)** | 4.0 | 4.0 | 4.0 | Excellent on all dimensions; research-grade quality |
| **Improvement** | +33% | +100% | +33% | Structured prompt doubles citation quality |

#### Claim-Evidence Extraction Task

| Prompt | Avg Groundedness | Avg Citation | Avg Usefulness | Key Observations |
|--------|-----------------|--------------|----------------|------------------|
| **2A (Baseline)** | 2.0 | 1.5 | 2.0 | Weak performance; paraphrasing issues; vague citations |
| **2B (Structured)** | 2.5 | 2.5 | 2.5 | Better but highly dependent on paper type; one complete failure |
| **Improvement** | +25% | +67% | +25% | Improvement significant but limited by source compatibility |

### Overall Performance Summary

| Metric | Baseline Prompts (1A, 2A) | Structured Prompts (1B, 2B) | Improvement |
|--------|--------------------------|----------------------------|-------------|
| **Groundedness** | 2.5 | 3.25 | +30% |
| **Citation Correctness** | 1.75 | 3.25 | +86% |
| **Usefulness** | 2.5 | 3.25 | +30% |

---

## CHATGPT MODEL (GPT-4o)

**Model:** ChatGPT (GPT-4o)  
**Domain:** AI/Automation, Job Displacement, and Universal Basic Income  
**Date:** February 2, 2026  
**Tasks:** Paper Triage (Runs 1-4) + Claim-Evidence Extraction (Runs 5-8)

---

## EVALUATION SUMMARY TABLE (ChatGPT)

| Run | Task | Paper | Type | Prompt | Groundedness | Citation | Usefulness | Notes |
|-----|------|-------|------|--------|--------------|----------|------------|-------|
| 1 | Paper Triage | A: ScienceDirect SLR | Survey | 1A (Baseline) | 3 | 2 | 3 | Accurate but lacks specific citations |
| 2 | Paper Triage | A: ScienceDirect SLR | Survey | 1B (Structured) | 4 | 4 | 4 | Excellent grounding; Data/Limitations note lack of info |
| 3 | Paper Triage | B: SHRM Data Brief | Empirical | 1A (Baseline) | 3 | 2 | 3 | Accurate content, general citations |
| 4 | Paper Triage | B: SHRM Data Brief | Empirical | 1B (Structured) | 4 | 4 | 4 | Strong structure; Findings cite source verbatim |
| 5 | Claim-Evidence | C: Mercatus Brief | Benchmark | 2A (Baseline) | 3 | 3 | 3 | Verbatim quotes; correct citations but no table format |
| 6 | Claim-Evidence | C: Mercatus Brief | Benchmark | 2B (Structured) | 4 | 4 | 4 | Verbatim quotes; perfect table format |
| 7 | Claim-Evidence | D: UBI Critique | Critique | 2A (Baseline) | 3 | 3 | 3 | Verbatim quotes; correct citations but numbered list not table |
| 8 | Claim-Evidence | D: UBI Critique | Critique | 2B (Structured) | 4 | 4 | 4 | Verbatim quotes; perfect table format |

**Average Scores:**
- **Baseline Prompts (1A, 2A):** Groundedness: 3.0, Citation: 2.5, Usefulness: 3.0
- **Structured Prompts (1B, 2B):** Groundedness: 4.0, Citation: 4.0, Usefulness: 4.0
- **Improvement with Structured Prompts:** +33% groundedness, +60% citation quality, +33% usefulness

---

## RUN 1: Paper A (ScienceDirect SLR) - Prompt 1A (Baseline)

### Test Configuration
- **Task:** Paper Triage Test 1
- **Paper:** ScienceDirect Systematic Literature Review (Survey)
- **Prompt:** "Summarize this paper in 5 fields: Contribution, Method, Data, Findings, Limitations."
- **Model:** ChatGPT (GPT-4o)

### Output

**Contribution:** A comprehensive synthesis of the relationship between AI and employment, identifying three core themes—trends in AI-induced labor displacement, adverse roles of AI (precarity, skill mismatches for white-collar/gig/freelance workers), and existing mitigation strategies (responsible AI guidelines from governments, institutions, firms).

**Method:** Systematic Literature Review (SLR) guided by the PRISMA framework, examining peer-reviewed literature from the Scopus database (2015–July 09, 2025).

**Data:** Peer-reviewed literature from Scopus; no primary data collection. The study synthesizes existing published work.

**Findings:** Current policy responses encourage human-AI complementarity but remain fragmented and insufficient to address structural workforce displacement risks. The study highlights key areas for further inquiry and policy development.

**Limitations:** Not explicitly addressed in the provided text (abstract and introduction excerpt only).

### Evaluation Scores

| Metric | Score | Justification |
|--------|-------|---------------|
| Groundedness | 3/4 | Content accurate and reflects paper; key themes correctly identified; minor issue: no specific page/section references. |
| Citation Correctness | 2/4 | No specific citations provided; vague references like "the paper"; cannot verify specific claims against source. |
| Usefulness | 3/4 | Provides good overview; identifies main contributions and findings; adequate for quick screening but limited research value. |

### Failure Modes Identified
- **Missing citations:** No (SectionName, paragraph) or page references
- **Vague attribution:** Cannot trace specific claims to source locations
- **Adequate for screening, weak for research:** Suitable for quick review but insufficient for detailed analysis

---

## RUN 2: Paper A (ScienceDirect SLR) - Prompt 1B (Structured)

### Test Configuration
- **Task:** Paper Triage Test 1
- **Paper:** ScienceDirect Systematic Literature Review (Survey)
- **Prompt:** Structured prompt with 5-field requirements, citation constraints, and grounding rules
- **Model:** ChatGPT (GPT-4o)

### Output

**1. Contribution:** The paper makes a novel synthesis claim: it identifies three core themes in the AI–employment literature—(1) trends in AI-induced labor displacement (task automation, skill polarization, industry-specific disruptions in healthcare, education, creative industries); (2) adverse roles of AI (affecting white-collar professionals, gig workers, freelancers via precarity and skill mismatches); (3) existing mitigation strategies (responsible AI guidelines from governments, institutions, firms). It presents a comprehensive synthesis of the evolving relationship between AI and employment.

**2. Method:** Systematic Literature Review (SLR) guided by the PRISMA framework. Research approach: literature review / synthesis of peer-reviewed sources.

**3. Data:** Peer-reviewed literature from the Scopus database (2015–July 09, 2025). No primary empirical data provided in the excerpt; the study aggregates and synthesizes existing published literature.

**4. Findings:** A growing body of policy responses encourages human-AI complementarity; current measures remain fragmented and insufficient to address the structural risks of workforce displacement. The study highlights key areas for further inquiry and policy development. (Abstract.)

**5. Limitations:** Limitations not explicitly addressed in the provided text. (Only abstract and introduction excerpt were provided.)

### Evaluation Scores

| Metric | Score | Justification |
|--------|-------|---------------|
| Groundedness | 4/4 | Excellent adherence to source material; structured 5 fields; no inference beyond text; Data and Limitations note lack of info. |
| Citation Correctness | 4/4 | Clear field-level attribution; (Abstract.) cited where applicable; distinguishes explicit vs. not stated. |
| Usefulness | 4/4 | Highly usable for research; can verify claims; distinguishes what is stated vs. omitted; flags methodological gaps. |

### Strengths Demonstrated
- [OK] Follows all constraints perfectly
- [OK] Uses required structure; states "Not specified" / "not addressed" where appropriate
- [OK] States uncertainties explicitly
- [OK] Professional research quality
- [OK] Separates explicit statements from analytical gaps

---

## RUN 3: Paper B (SHRM Data Brief) - Prompt 1A (Baseline)

### Test Configuration
- **Task:** Paper Triage Test 2
- **Paper:** SHRM Data Brief on Automation and Job Displacement (Empirical)
- **Prompt:** "Summarize this paper in 5 fields: Contribution, Method, Data, Findings, Limitations."
- **Model:** ChatGPT (GPT-4o)

### Output

**Contribution:** First large-scale survey-based estimates of the prevalence of "high" (≥ 50%) task automation and generative AI use in U.S. employment, and of nontechnical barriers to automation displacement.

**Method:** Large-scale survey of U.S. workers (SHRM 2025 Automation/AI Survey), fielded in spring 2025.

**Data:** Over 20,000 individual respondents; survey data on automation/AI use by occupation, nontechnical barriers to displacement, and worker attitudes about displacement risk.

**Findings:** At least 50% of tasks are automated in 15.1% of U.S. employment (23.2 million jobs). 63.3% of jobs include at least one nontechnical barrier that would prevent automation displacement. Job transformation will be much more common than outright displacement for most workers.

**Limitations:** Not explicitly addressed in the provided text (purpose and key findings only).

### Evaluation Scores

| Metric | Score | Justification |
|--------|-------|---------------|
| Groundedness | 3/4 | Accurately captures empirical nature; key statistics (15.1%, 63.3%, 23.2M) correctly reported; minor issue: no specific section/page refs. |
| Citation Correctness | 2/4 | General references to purpose/findings without specific section or page; cannot easily verify location of specific claims. |
| Usefulness | 3/4 | Good for understanding paper's approach; statistical findings clearly presented; adequate screening tool but limited research value. |

### Failure Modes Identified
- **Incomplete citations:** References purpose/findings but not paragraphs or pages
- **Limited traceability:** Hard to find specific evidence locations
- **Missing paragraph-level detail:** Cannot pinpoint exact claim sources

---

## RUN 4: Paper B (SHRM Data Brief) - Prompt 1B (Structured)

### Test Configuration
- **Task:** Paper Triage Test 2
- **Paper:** SHRM Data Brief on Automation and Job Displacement (Empirical)
- **Prompt:** Structured prompt with 5-field requirements, citation constraints, and grounding rules
- **Model:** ChatGPT (GPT-4o)

### Output

**1. Contribution:** The paper provides novel empirical estimates: (1) prevalence of "high" (≥ 50%) task completion via automation and generative AI in U.S. employment; (2) prevalence of nontechnical barriers to automation displacement. It identifies which job types are most likely to be displaced vs. shielded.

**2. Method:** Empirical analysis—large-scale survey. SHRM fielded the SHRM 2025 Automation/AI Survey of U.S. workers in spring 2025.

**3. Data:** Over 20,000 individual respondents. Survey data on automation/generative AI use levels by occupation, nontechnical barriers to displacement, and worker attitudes about displacement risk. Data validates the prevalence estimates reported.

**4. Findings:** (Purpose/Key findings.) We estimate that at least 50% of tasks are automated in 15.1% of U.S. employment (23.2 million jobs). We also find that 63.3% of jobs include at least one nontechnical barrier that would prevent automation displacement. While advances in AI create significant displacement risk for a small fraction of workers, job transformation will be much more common.

**5. Limitations:** Limitations not explicitly addressed in the provided text.

### Evaluation Scores

| Metric | Score | Justification |
|--------|-------|---------------|
| Groundedness | 4/4 | Precise extraction of definitions and concepts; correctly quotes key statistics (15.1%, 63.3%) with context; structured 5-field output. |
| Citation Correctness | 4/4 | Clear field-level attribution; Findings cite source verbatim; all five fields have traceable content from purpose/key findings. |
| Usefulness | 4/4 | Research-grade quality; can reconstruct author's argument; explicit about what paper addresses vs. omits; complete 5-field structure. |

### Strengths Demonstrated
- [OK] Perfect adherence to structured format
- [OK] Findings verbatim from source
- [OK] Critical evaluation of limitations (not addressed)
- [OK] Distinguishes stated vs. unstated limitations
- [OK] Key stats (15.1%, 63.3%, 23.2M) correctly cited

---

## RUN 5: Paper C (Mercatus Policy Brief) - Prompt 2A (Baseline)

### Test Configuration
- **Task:** Claim-Evidence Extraction Test 1
- **Paper:** Mercatus Center Policy Brief (Benchmark)
- **Prompt:** "Extract 5 claims from this paper with supporting evidence and citations."
- **Model:** ChatGPT (GPT-4o)

### Output

1. The current tax framework creates an asymmetry between physical and human capital investment. Evidence: "The current tax framework creates a profound asymmetry between physical and human capital investment." (Sharfuddin2025, chunk_01)

2. Businesses can expense a robot or AI server in the year purchased but face restrictions deducting retraining costs. Evidence: "businesses can expense a robot or an AI server in the year it is purchased, yet they must navigate a maze of restrictions to deduct the cost of retraining the people expected to use that technology." (Sharfuddin2025, chunk_01)

3. Six major IRC restrictions create bottlenecks that penalize human capital investment. Evidence: "Six major restrictions in the Internal Revenue Code (IRC) create bottlenecks that effectively penalize businesses for investing in human capital." (Sharfuddin2025, chunk_02)

4. IRC section 162 disallows deductions for education that meets minimum job requirements. Evidence: "IRC section 162 and associated guidance disallow deductions for employee education when the coursework 'is needed to meet the minimum educational requirements of your present trade or business.'" (Sharfuddin2025, chunk_02)

5. The provision on minimum requirements was originally a tax-abuse safeguard but now undermines flexibility in an AI-shaped economy. Evidence: "Originally intended as a safeguard against tax abuse, this provision now undermines the competitive flexibility essential in an economy reshaped by AI." (Sharfuddin2025, chunk_02)

### Evaluation Scores

| Metric | Score | Justification |
|--------|-------|---------------|
| Groundedness | 3/4 | Claims are accurate and quotes are verbatim from chunks; evidence supports each claim; baseline prompt did not require table format. |
| Citation Correctness | 3/4 | Correct (source_id, chunk_id) format; can trace to chunks; numbered list format rather than table reduces scanability. |
| Usefulness | 3/4 | Verbatim quotes and correct citations; usable for research but table format would improve consistency with structured prompt. |

### Failure Modes Identified
- **Format:** Numbered list instead of table; baseline prompt did not specify table
- **Minor:** Quote length in some rows exceeds typical "≤20 words" constraint where applied elsewhere

---

## RUN 6: Paper C (Mercatus Policy Brief) - Prompt 2B (Structured)

### Test Configuration
- **Task:** Claim-Evidence Extraction Test 1
- **Paper:** Mercatus Center Policy Brief (Benchmark)
- **Prompt:** Structured prompt with table format, verbatim quotes, (source_id, chunk_id) citations
- **Model:** ChatGPT (GPT-4o)

### Output

| Claim | Direct Quote/Snippet | Citation (source_id, chunk_id) |
|-------|----------------------|--------------------------------|
| Tax framework creates asymmetry between physical and human capital investment | "The current tax framework creates a profound asymmetry between physical and human capital investment" | (Sharfuddin2025, chunk_01) |
| Businesses can expense equipment immediately but face restrictions on deducting retraining costs | "businesses can expense a robot or an AI server in the year it is purchased, yet they must navigate a maze of restrictions to deduct the cost of retraining the people" | (Sharfuddin2025, chunk_01) |
| Six IRC restrictions penalize human capital investment | "Six major restrictions in the Internal Revenue Code (IRC) create bottlenecks that effectively penalize businesses for investing in human capital" | (Sharfuddin2025, chunk_02) |
| IRC section 162 disallows deductions for education meeting minimum job requirements | "IRC section 162 and associated guidance disallow deductions for employee education when the coursework \"is needed to meet the minimum educational requirements of your present trade or business.\"" | (Sharfuddin2025, chunk_02) |
| Minimum-requirements provision now undermines flexibility in an AI economy | "Originally intended as a safeguard against tax abuse, this provision now undermines the competitive flexibility essential in an economy reshaped by AI" | (Sharfuddin2025, chunk_02) |

### Evaluation Scores

| Metric | Score | Justification |
|--------|-------|---------------|
| Groundedness | 4/4 | Claims are specific and policy-relevant; quotes appear verbatim and traceable; evidence directly supports each claim. |
| Citation Correctness | 4/4 | Perfect format: (Sharfuddin2025, chunk_01/02); can trace to exact location; table format followed perfectly. |
| Usefulness | 4/4 | Highly usable for research database; quotes are verifiable; specific policy claims with exact evidence; follows all constraints. |

### Strengths Demonstrated
- [OK] Verbatim quotes under 20 words where applicable
- [OK] Citation format (source_id, chunk_id)
- [OK] Empirical/policy-specific claims
- [OK] Table format followed perfectly
- [OK] All quotes appear to be actual text from source

---

## RUN 7: Paper D (UBI Critique) - Prompt 2A (Baseline)

### Test Configuration
- **Task:** Claim-Evidence Extraction Test 2
- **Paper:** Tan UBI Critique Paper (Critique)
- **Prompt:** "Extract 5 claims from this paper with supporting evidence and citations."
- **Model:** ChatGPT (GPT-4o)

### Output

1. AI and automation have sparked debate about widespread job displacement. Evidence: "The increasing sophistication of artificial intelligence (AI) and automation technologies has precipitated significant debate regarding their potential to cause widespread job displacement." (Tan2025, chunk_01)

2. UBI/GBI is examined as a comprehensive solution to technological unemployment. Evidence: "This paper critically examines the proposition that Universal Basic Income (UBI) or other forms of guaranteed basic income (GBI) could serve as a comprehensive solution to the challenges posed by such technological unemployment." (Tan2025, chunk_01)

3. Basic income shows promise on poverty, economic security, and well-being but is not a singular panacea. Evidence: "while basic income demonstrates considerable promise in alleviating poverty, enhancing economic security, and improving certain well-being outcomes, its efficacy as a singular panacea is limited." (Tan2025, chunk_01)

4. Basic income should be viewed as one component of a broader policy framework. Evidence: "basic income is more appropriately viewed as a potentially crucial component within a broader, multifaceted policy framework designed to navigate the future of work." (Tan2025, chunk_02)

5. That framework should include education, active labour market policies, and equitable distribution of productivity gains. Evidence: "This framework should also encompass robust investments in education and skills development, active labour market policies, and strategies to ensure the equitable distribution of productivity gains from automation." (Tan2025, chunk_02)

### Evaluation Scores

| Metric | Score | Justification |
|--------|-------|---------------|
| Groundedness | 3/4 | Claims reflect UBI critique themes; quotes are verbatim from chunks; baseline prompt did not require table format. |
| Citation Correctness | 3/4 | Correct (Tan2025, chunk_01/02); can trace to chunks; numbered list rather than table; no fabrication. |
| Usefulness | 3/4 | Verbatim quotes and correct citations; identifies key UBI/automation claims; table format would improve consistency. |

### Failure Modes Identified
- **Format:** Numbered list instead of table; baseline prompt did not specify table
- **Minor:** Output structure less scannable than structured prompt's table format

---

## RUN 8: Paper D (UBI Critique) - Prompt 2B (Structured)

### Test Configuration
- **Task:** Claim-Evidence Extraction Test 2
- **Paper:** Tan UBI Critique Paper (Critique)
- **Prompt:** Structured prompt with table format, verbatim quotes, (source_id, chunk_id) citations
- **Model:** ChatGPT (GPT-4o)

### Output

| Claim | Direct Quote/Snippet | Citation (source_id, chunk_id) |
|-------|----------------------|--------------------------------|
| AI and automation have precipitated debate on widespread job displacement | "The increasing sophistication of artificial intelligence (AI) and automation technologies has precipitated significant debate regarding their potential to cause widespread job displacement" | (Tan2025, chunk_01) |
| UBI/GBI is examined as a comprehensive solution to technological unemployment | "Universal Basic Income (UBI) or other forms of guaranteed basic income (GBI) could serve as a comprehensive solution to the challenges posed by such technological unemployment" | (Tan2025, chunk_01) |
| Basic income's efficacy as a singular panacea is limited | "its efficacy as a singular panacea is limited" | (Tan2025, chunk_01) |
| Basic income is better viewed as one component of a broader policy framework | "basic income is more appropriately viewed as a potentially crucial component within a broader, multifaceted policy framework designed to navigate the future of work" | (Tan2025, chunk_02) |
| Framework should include education, active labour market policies, and equitable distribution of productivity gains | "This framework should also encompass robust investments in education and skills development, active labour market policies, and strategies to ensure the equitable distribution of productivity gains from automation" | (Tan2025, chunk_02) |

### Evaluation Scores

| Metric | Score | Justification |
|--------|-------|---------------|
| Groundedness | 4/4 | Claims are specific and policy-relevant; quotes appear verbatim; evidence directly supports each claim; table format complete. |
| Citation Correctness | 4/4 | Perfect format: (Tan2025, chunk_01/02); can trace to exact location; table format followed perfectly; only provided citations used. |
| Usefulness | 4/4 | Highly usable for research database; quotes are verifiable; specific UBI/automation claims with exact evidence; follows all constraints. |

### Strengths Demonstrated
- [OK] Verbatim quotes from provided chunks
- [OK] Citation format (source_id, chunk_id)
- [OK] Policy-relevant claims (UBI, framework, automation)
- [OK] Table format followed perfectly
- [OK] All quotes appear to be actual text from source; no fabrication
