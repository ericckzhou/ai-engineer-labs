# Assessment Rubric — Elective 05: Advanced RAG / Query Engineering

> Self-assessment first, mentor review second. Grades the **query-transformation stage + fusion,
> proven per-transform against the faithfulness eval** — not rebuilding retrieval (provided) or
> re-ranking (provided, from P03).

---

## Dimension 1: Understanding (25%)

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Names the two failure modes of naive RAG (paraphrase / multi-hop), explains the question↔query gap, what HyDE embeds (a hypothetical *answer*) and when it hurts, and that **transforms must be eval-gated** (more-retrieved ≠ better). Knows re-ranking is provided. Original analogy. | 25 |
| 3 — Good | Explains the transforms + the eval gate with minor gaps. | 20 |
| 2 — Developing | Describes "rewrite the query" but assumes fancier = better, or thinks HyDE embeds the query. | 15 |
| 1 — Beginning | Surface-level; "add more retrieval". | 10 |

**Score: ___ / 25**

---

## Dimension 2: Implementation (30%)

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | `rewrite`/`hyde`/`decompose` correct; `answer` applies the transform, retrieves per (sub-)query, and **fuses = dedupe + re-rank** (uses the provided re-ranker, no duplicates, ≤ top_n); a multi-hop query's fused context contains both gold chunks. All guiding tests pass. | 30 |
| 3 — Good | Core works; minor issues (decompose misses a case, or fusion keeps a duplicate). | 24 |
| 2 — Developing | Transforms work but fusion is naive concatenation; or re-ranking rebuilt; some tests fail. | 18 |
| 1 — Beginning | Doesn't run, or no real transform stage. | 12 |

**Score: ___ / 30**

---

## Dimension 3: Failure Analysis (20%)

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | 3+ experiments **including** a transform that **didn't help / hurt** (e.g. HyDE lowering faithfulness on a factual query) and a **naive-concatenation fusion** diluting relevance. Each diagnosed with the implication. | 20 |
| 3 — Good | 2+ experiments, at least one of the two required. | 16 |
| 2 — Developing | 1 shallow experiment. | 12 |
| 1 — Beginning | No intentional breakage. | 8 |

**Score: ___ / 20**

---

## Dimension 4: Evaluation (15%)

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Reports **faithfulness + answer-relevance + retrieval-hit PER TRANSFORM** (baseline / rewrite / HyDE / decompose) on the frozen set. **Honestly** names the transforms that didn't help. Distinguishes recall from faithfulness. | 15 |
| 3 — Good | Per-transform faithfulness reported; minor gaps. | 12 |
| 2 — Developing | Reports only that "advanced RAG is better" without per-transform numbers. | 9 |
| 1 — Beginning | No real measurement. | 6 |

**Score: ___ / 15**

---

## Dimension 5: StarcallOS Reflection (10%)

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | 2+ concrete StarcallOS retrieval problems a transform fixes (messy phrasing over personal notes; multi-hop across emails/docs), with the mechanism and an implementation path. | 10 |
| 3 — Good | 1 concrete pattern, well explained. | 8 |
| 2 — Developing | Generic ("better search"). | 6 |
| 1 — Beginning | No meaningful connection. | 4 |

**Score: ___ / 10**

---

## Total Score — **___ / 100**

| Range | Level |
|-------|-------|
| 90–100 | Complete to standard |
| 75–89 | Minor gaps |
| 60–74 | Revisit weak dimensions |
| Below 60 | Return to the lesson |

---

## Elective-Specific Checks (quick pass/fail)

- [ ] `hyde` embeds a hypothetical **answer**, not the query
- [ ] Fusion **dedupes + re-ranks** the union (no duplicates, ≤ `rerank_top_n`) — not concatenation
- [ ] Re-ranking is the **provided** P03 component (not rebuilt)
- [ ] `decompose` yields ≥2 sub-questions for a multi-hop query
- [ ] EVALUATION reports faithfulness **per transform**, including ones that didn't help
- [ ] Faithfulness (not raw recall) is the gate
- [ ] All guiding tests pass offline

---

## Mentor Notes
**Overall:** · **Strongest:** · **Needs work:** · **Next steps:**
