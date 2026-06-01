# Assessment Rubric — Project 03: Semantic Search

> Used to evaluate the learner's completed project.
> Self-assessment first. Mentor review second.
> Dimensions and weights are the lab-standard master rubric; the **Project-03 evidence prompts**
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

**Project-03 evidence prompts — look for whether the learner can:**
- Explain what a vector DB adds **on top of** Project 02's embeddings + cosine (speed via indexing,
  persistence, filtering) — not "it makes the search smarter."
- State that **HNSW is approximate** and explain the recall/speed tradeoff (why it can miss a true neighbor).
- Predict the **distance-vs-similarity** inversion (Chroma returns distance; lower = closer) as a silent bug.
- Justify `space="cosine"` for text over the `l2` default.

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

**Project-03 evidence prompts — look for whether the implementation:**
- `indexer.py` builds a **persistent** Chroma collection with `space="cosine"`, and is **idempotent**
  (re-running does not duplicate records). (M1)
- `semantic_search.py` returns results ranked by **similarity descending** with distance correctly
  converted (`1 − distance`); a semantically-related-but-lexically-different doc ranks first. (M2, M3)
- `baseline.py` reuses cosine-from-scratch and provides a working `recall_at_k`. (M4)
- `evaluate.py` reports **recall@k of ANN vs. exact baseline** as a number across several queries. (M5)
- Corpus and query use the **same embedding model**; the corpus is indexed once, not re-embedded per query.
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

**Project-03 evidence prompts — strong analyses typically include:**
- **Forcing the inversion bug** (sort distances descending) and showing the worst results surface — then
  fixing it, framed as a silent (no-error) production failure.
- A **metric swap** (`space="cosine"` vs `l2`) on the same corpus with the ranking difference explained.
- An **`ef_search` sweep** showing recall@k change vs. (qualitative) latency.
- A **cross-model mismatch** (index with one embedding model, query with another) showing meaningless results.

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

**Project-03 evidence prompts — quantitative means actual numbers, e.g.:**
- **recall@k** of the ANN index vs. the exact brute-force baseline, across several queries (mean + per-query).
- Real **distances/similarities** for top results (showing the direction is correct).
- Effect of `ef_search` on recall; effect of `space` choice on ordering.
- An honest production-readiness/cost note (index build time, query latency feel, embedding cost — local
  Ollama $0 vs. a cloud embedder).

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

**Project-03 evidence prompts — concrete connections include:**
- A StarcallOS "find related things" feature (recall a note, surface a command, match request→capability)
  framed as a **persistent vector-DB query**, naming the collection, metric, and `k`.
- A statement of how **recall measurement and re-ranking** would keep that retrieval trustworthy as the
  store grows — mechanism + implementation path, not "we could use a vector DB."

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
