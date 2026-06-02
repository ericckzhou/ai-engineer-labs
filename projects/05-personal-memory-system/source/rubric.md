# Assessment Rubric — Project 05: Personal Memory System

> Used to evaluate the learner's completed project.
> Self-assessment first. Mentor review second.
> Dimensions and weights are the lab-standard master rubric; the **Project-05 evidence prompts**
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

**Project-05 evidence prompts — look for whether the learner can:**
- Explain why a memory system is **more than relevance-only RAG over a chat log** — naming the recency
  and importance signals and what each adds.
- Explain **exponential recency decay** and why recency is measured from **last access** (so retrieval
  must touch `last_accessed`), not creation.
- Distinguish **episodic / semantic / procedural** memory and why a single flat decay policy is wrong.
- Frame retrieval as **paging the top-k into a context budget** (main vs external context), not
  injecting everything.

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

**Project-05 evidence prompts — look for whether the implementation:**
- `scoring.py` computes recency as `decay_rate ** hours_since(last_accessed)`, importance as a
  normalized 1–10, relevance as cosine, and `retrieval_score` as the weighted sum. (M1–M3)
- `retriever.retrieve` scores **all three signals**, returns a ranked **top-k**, and **touches**
  `last_accessed = now` on the returned memories. (M4)
- The chat loop **injects retrieved memories into the prompt** and **writes each turn back**. (M5)
- Memories and queries use the **same embedding model**; relevance is real cosine similarity.
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

**Project-05 evidence prompts — strong analyses typically include:**
- A **relevance-only ablation** (weights `(1,0,0)`) showing a trivial/old memory outranking the one that
  actually matters — i.e. demonstrating it has degenerated into RAG-over-history.
- A **no-touch ablation** (skip the `last_accessed = now` update) showing a frequently-used memory
  decaying out of the top-k anyway, and explaining why.
- A **no-write-back ablation** showing the assistant failing to recall something said earlier in the
  session.
- A **weight-tuning experiment** (raise `w_recency` or `w_importance`) showing the rank order change,
  with the per-memory `(rel, rec, imp, score)` breakdown — diagnosing recall to the *signal* responsible.

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

**Project-05 evidence prompts — quantitative means actual numbers, e.g.:**
- **Score breakdowns** per candidate memory `(relevance, recency, importance, total)` for a few queries,
  showing *which* signal drove the top result.
- **Rank changes** under each ablation/weight setting (which memory moved to the top, and by how much).
- **Recall hit/miss**: across a handful of test queries, did the memory that *should* surface make the
  top-k?
- An honest production note: cost of embedding every memory + every query (local Ollama $0 vs. a cloud
  embedder), and what breaks at 10k+ memories without a real vector index (Project 03).

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

**Project-05 evidence prompts — concrete connections include:**
- A StarcallOS feature that "knows the user" framed as a **memory stream** — naming the `kind` of
  memories stored, the retrieval weights, the decay policy, and the write-back trigger.
- How **episodic → semantic promotion** (reflection) would let StarcallOS build durable knowledge about
  the user over time — mechanism + implementation path, not "we could add memory."

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
