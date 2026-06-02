# Assessment Rubric — Project 04: PDF Research Assistant (RAG)

> Used to evaluate the learner's completed project.
> Self-assessment first. Mentor review second.
> Dimensions and weights are the lab-standard master rubric; the **Project-04 evidence prompts**
> under each dimension are specific to this lesson (`source/lesson.agent.md`).

---

## Dimension 1: Understanding (25%)

Evaluated by reviewing UNDERSTANDING.md and UNDERSTANDING_FEEDBACK.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Explains all concepts clearly in own words. Analogy is original and accurate. No gaps in understanding. Can answer follow-up questions. | 25 |
| 3 — Good | Explains most concepts correctly. Minor gaps or oversimplifications. | 20 |
| 2 — Developing | Some correct understanding but significant gaps or misconceptions present. | 15 |
| 1 — Beginning | Surface-level understanding only. Heavy reliance on lesson language without internalization. | 10 |

**Project-04 evidence prompts — look for whether the learner can:**
- Explain RAG as **parametric + non-parametric memory** and why retrieval beats a bigger model for
  document QA (updatable, attributable) — not "it reads the PDF."
- Articulate the **chunk-size tradeoff** (small = precise/context-poor, large = rich/imprecise) and why
  **overlap** matters.
- Distinguish **faithfulness** (supported by context) from **relevance** (addresses the question), and
  why a fluent answer can still be a hallucination.
- Explain why **grounding can fail silently** (model answers from memory) and how to detect it.

**Score: ___ / 25**

**Evidence:**

---

## Dimension 2: Implementation (30%)

Evaluated by reviewing code/ and IMPLEMENTATION.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Code is correct, clean, and runnable. Architecture demonstrates understanding of the underlying concepts. No magic — learner understands every line. | 30 |
| 3 — Good | Code works correctly. Minor style or architecture issues. | 24 |
| 2 — Developing | Code partially works. Key components missing or incorrect. | 18 |
| 1 — Beginning | Code does not run or produces incorrect results. | 12 |

**Project-04 evidence prompts — look for whether the implementation:**
- `chunker.py` splits text into **overlapping, id-tagged** chunks; adjacent chunks share `overlap`
  tokens; no redundant tail chunk. (M1)
- `generator.py` `build_prompt` puts the **retrieved chunks + their ids** in the prompt and instructs
  **answer-only-from-context** with an explicit **refusal** path; `answer` returns text + cited ids. (M3, M4)
- The system **refuses** ("I don't know") on an off-document question rather than hallucinating.
- `faithfulness.py` computes `F = |V|/|S|` over decomposed claims. (M5)
- Chunks and query use the **same embedding model**; retrieval is reused, not re-derived incorrectly.
- Guiding tests in `code/tests/` pass.

**Score: ___ / 30**

**Evidence:**

---

## Dimension 3: Failure Analysis (20%)

Evaluated by reviewing FAILURE_ANALYSIS.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | 3+ intentional experiments. Each experiment correctly diagnoses why the failure occurred. Clear production implications. | 20 |
| 3 — Good | 2+ experiments with good analysis. | 16 |
| 2 — Developing | 1 experiment with shallow analysis. | 12 |
| 1 — Beginning | No intentional breakage, or breakage without analysis. | 8 |

**Project-04 evidence prompts — strong analyses typically include:**
- An **off-document question** confirming the system **refuses** — then weakening the grounding
  instruction and showing it now **hallucinates** (framed as a silent, no-error production failure).
- A **forced hallucination** (inject a false premise / weaken context) and showing the **faithfulness
  score drop** as a number.
- A **chunk-size / overlap experiment** showing a fact on a boundary becoming findable or unfindable,
  and the effect on retrieval + answer quality.
- Diagnosing a bad answer to the **right pipeline stage** (chunking vs retrieval vs generation).

**Score: ___ / 20**

**Evidence:**

---

## Dimension 4: Evaluation (15%)

Evaluated by reviewing EVALUATION.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Quantitative results for all major criteria. Honest assessment of production readiness. Cost analysis included. | 15 |
| 3 — Good | Most criteria measured quantitatively. Minor gaps. | 12 |
| 2 — Developing | Mostly qualitative ("it seemed to work"). Few numbers. | 9 |
| 1 — Beginning | No meaningful evaluation. | 6 |

**Project-04 evidence prompts — quantitative means actual numbers, e.g.:**
- **Faithfulness** `F = |V|/|S|` across several questions (grounded answers ~1.0; the forced-hallucination
  case visibly lower).
- **Retrieval hit/miss**: did the chunk containing the answer make the top-k? (per question.)
- Effect of **chunk size / overlap** on retrieval correctness; optionally **context relevance** `CR`.
- An honest production-readiness/cost note (embedding cost — local Ollama $0 vs. a cloud embedder; the
  extra LLM call faithfulness adds; latency feel).

**Score: ___ / 15**

**Evidence:**

---

## Dimension 5: StarcallOS Reflection (10%)

Evaluated by reviewing STARCALLOS_REFLECTION.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Identifies 2+ concrete, non-obvious patterns applicable to StarcallOS. Explains mechanism and implementation path. | 10 |
| 3 — Good | Identifies 1 concrete applicable pattern with good explanation. | 8 |
| 2 — Developing | Reflection is generic or surface-level. | 6 |
| 1 — Beginning | No meaningful StarcallOS connection made. | 4 |

**Project-04 evidence prompts — concrete connections include:**
- A StarcallOS feature that answers from *your* documents/notes/history framed as a **RAG pipeline** —
  naming the chunking strategy, the retrieval `k`, the grounding/refusal rule, and the citation target.
- How **faithfulness monitoring** would keep that answering trustworthy (catch hallucinations before
  the user sees them) — mechanism + implementation path, not "we could use RAG."

**Score: ___ / 10**

**Evidence:**

---

## Total Score

**___ / 100**

| Range | Level |
|-------|-------|
| 90–100 | Ready for next project |
| 75–89 | Ready with minor gaps — document them |
| 60–74 | Revisit the weak dimensions before proceeding |
| Below 60 | Return to the lesson and rebuild |

---

## Mentor Notes

**Overall assessment:**

**Strongest dimension:**

**Area most needing work:**

**Recommended next steps:**
