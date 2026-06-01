# Assessment Rubric — Project 02: Token & Embedding Explorer

> Used to evaluate the learner's completed project.
> Self-assessment first. Mentor review second.
> Dimensions and weights are the lab-standard master rubric; the **Project-02 evidence prompts**
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

**Project-02 evidence prompts — look for whether the learner can:**
- Distinguish a **tokenizer** (reversible text↔IDs, no meaning in the ID value) from an **embedding
  model** (meaning-bearing vector) — not conflate "both turn text into numbers."
- Explain why cosine measures **angle, not distance/magnitude**, and predict `cos(v,v)=1`, `cos(v,-v)=-1`.
- Predict the embed-query-with-A / embed-corpus-with-B failure as a **silent** bug (no error raised).
- State that embedding **dimensionality is model-specific** (768 vs 1536), not a quality score.

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

**Project-02 evidence prompts — look for whether the implementation:**
- `tokenizer_explorer.py` shows real `tiktoken` IDs, per-token pieces, and a **lossless round-trip**
  (`decode(encode(s)) == s`); `count(text) == len(encode(text))`. (M1)
- `embedding_explorer.py` reads the dimension from `len(vector)` — **no hardcoded 768/1536**. (M3)
- `similarity_calculator.py` implements `cosine = (a·b)/(‖a‖‖b‖)` **by hand** — no `sklearn` or other
  prebuilt cosine helper. (M4)
- `corpus_search.py` ranks a paraphrase/semantic match above a lexically-overlapping but unrelated
  text; embeds the query once rather than per-iteration. (M5)
- Tokenizer and embedding model are kept as **separate components**. The guiding tests in `tests/`
  pass (`python -m pytest`).

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

**Project-02 evidence prompts — strong analyses typically include:**
- A **failed analogy triple** (where `a − b + c` does *not* land near the expected word) with an
  explanation that this is an approximate regularity, not a law (required — see lesson §4 Example 3).
- A **cross-model dimension/space mismatch** (e.g. 768-dim vs 1536-dim) and why the scores become
  meaningless — framed as a silent retrieval bug, not a crash.
- A token-count comparison of the **same text under two encodings** explaining why counts differ.
- Each experiment ties the failure to a **production consequence** (wrong retrieval, blown budget/context).

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

**Project-02 evidence prompts — quantitative means actual numbers, e.g.:**
- Real **cosine scores** for a paraphrase pair vs. an unrelated pair (showing the gap, not "it worked").
- Real **token counts** for sample texts, and the count delta across two encodings.
- The embedding **dimension** observed, and corpus-search ranking results with their scores.
- An honest note on **production readiness / cost** (e.g. local Ollama $0 vs. a cloud embedding model's
  per-token price; latency of embed-once vs. re-embed-per-query).

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

**Project-02 evidence prompts — concrete connections include:**
- A StarcallOS "find related things" feature (recall a note, surface a command, match a request to a
  capability) framed explicitly as an **embed + cosine** lookup, with the model/dimension choice named.
- A statement of **what makes that retrieval feel intelligent vs. random** (model choice, chunking,
  when similarity lies) — mechanism and an implementation path, not just "we could use embeddings."

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
