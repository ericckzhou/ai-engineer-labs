# Assessment Rubric — Elective 03: Cost & Latency Engineering

> Self-assessment first, mentor review second. Grades **cost reduction proven safe by the eval** —
> caching + cascading with quality held — not rebuilding the feature (provided) or the eval
> (provided).

---

## Dimension 1: Understanding (25%)

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Explains **cost and quality as separate axes** and why the eval is the **gate** (why this follows P07). Explains the prompt-cache write/read tradeoff, the semantic **false hit**, and the cascade **escalation signal** as the core design choice. Frames "10× cheaper" as half a result. Original analogy. | 25 |
| 3 — Good | Explains the three levers and the gate with minor gaps. | 20 |
| 2 — Developing | Describes "use a cheaper model / cache answers" but misses the quality risk or the eval's role. | 15 |
| 1 — Beginning | Surface-level; treats cost as the only axis. | 10 |

**Score: ___ / 25**

---

## Dimension 2: Implementation (30%)

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Semantic cache (embed→nearest→threshold, same embedder) with a real threshold gate; cascade routes cheap-first and **escalates on a defined signal**, returning tier + cost; `CostTracker` accumulates **real** per-call cost and enforces a ceiling; a cache hit costs ~0 and skips the model. All guiding tests pass. | 30 |
| 3 — Good | Core works; minor issues (one tier mis-priced, or threshold hardcoded). | 24 |
| 2 — Developing | Cache OR cascade works but not both; or cascade never escalates; some tests fail. | 18 |
| 1 — Beginning | Doesn't run, or no real lever (always strong / no gate). | 12 |

**Score: ___ / 30**

---

## Dimension 3: Failure Analysis (20%)

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | 3+ experiments **including** a semantic **false hit** (loose threshold → wrong cached answer) and a **never-escalating cascade** (ships cheap wrong answers). Each diagnosed with the production implication. | 20 |
| 3 — Good | 2+ experiments, at least one of false-hit / never-escalate. | 16 |
| 2 — Developing | 1 shallow experiment. | 12 |
| 1 — Beginning | No intentional breakage. | 8 |

**Score: ___ / 20**

---

## Dimension 4: Evaluation (15%)

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Reports the **frontier**: quality (pass-rate) **and** cost **and** latency/calls **and** cache-hit, baseline vs optimized, on the frozen set. Cost traces to the real price table. Honest read of any quality give-up. | 15 |
| 3 — Good | Quality + cost reported; minor gaps. | 12 |
| 2 — Developing | Cost only — no paired quality number (the metric trap). | 9 |
| 1 — Beginning | No real measurement. | 6 |

**Score: ___ / 15**

---

## Dimension 5: StarcallOS Reflection (10%)

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | 2+ concrete repetitive StarcallOS workloads these levers make affordable (background classify/summarize/route), with the mechanism (which lever, what saving) and an implementation path. | 10 |
| 3 — Good | 1 concrete applicable pattern, well explained. | 8 |
| 2 — Developing | Generic ("StarcallOS should be cheap"). | 6 |
| 1 — Beginning | No meaningful connection. | 4 |

**Score: ___ / 10**

---

## Total Score — **___ / 100**

| Range | Level |
|-------|-------|
| 90–100 | Complete to standard |
| 75–89 | Minor gaps — document them |
| 60–74 | Revisit weak dimensions |
| Below 60 | Return to the lesson |

---

## Elective-Specific Checks (quick pass/fail)

- [ ] Semantic cache uses the **same embedder** for store + lookup, with a real threshold gate
- [ ] Cascade **escalates** on a defined signal (not "always cheap" / "always strong")
- [ ] A cache hit costs ~0 and does **not** call a model
- [ ] Cost traces to the **real** per-MTok table (no invented prices)
- [ ] EVALUATION reports quality **and** cost (the frontier), baseline vs optimized
- [ ] FAILURE_ANALYSIS demonstrates a **false hit**
- [ ] All guiding tests pass offline

---

## Mentor Notes
**Overall assessment:** · **Strongest dimension:** · **Area most needing work:** · **Next steps:**
