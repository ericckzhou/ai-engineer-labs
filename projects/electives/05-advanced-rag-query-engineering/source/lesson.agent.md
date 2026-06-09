# Lesson (Agent Version): Advanced RAG — Engineering the Query, Not Just the Index

> **Canonical source of truth.** The human version (`rendered/lesson.html`) is derived from this
> file. If they conflict, this file wins.
> **Elective — Production & Hardening track.** Off the numbered 1–9 spine; recommended after P09.
> Prerequisite skills: Projects 02, 03, 04.

---

## Metadata

- **Project:** Elective 05 — Advanced RAG / Query Engineering
- **Track:** Production & Hardening (off-spine; after the P09 capstone) — a *depth* elective on retrieval
- **Estimated time:** 9–13 hours
- **Prerequisites:** Project 04 (the RAG pipeline + faithfulness eval being extended), Project 03
  (vector retrieval + **re-ranking — already built, provided here**), Project 02 (embeddings).
- **Extended capability:** the Project 04 PDF research assistant.
- **Primary sources:**
  - `sources/papers/query-rewriting-rag.md` (Ma et al. 2023 — Rewrite-Retrieve-Read)
  - `sources/papers/hyde.md` (Gao et al. 2022 — Hypothetical Document Embeddings)
  - `sources/papers/self-rag.md` (Asai et al. 2023 — adaptive retrieval + self-critique)
  - `sources/papers/ragas.md` (the faithfulness/answer-relevance gate)

---

## Learning Objectives

By the end of this elective, the learner will be able to:

1. **Name the two failure modes of naive retrieve-then-read** — paraphrased queries that miss
   lexically/semantically, and multi-hop questions a single retrieval can't satisfy.
2. **Apply query rewriting** — reformulate the user's question into a better *retrieval query*,
   and explain the question↔query gap (Rewrite-Retrieve-Read).
3. **Apply HyDE** — generate a hypothetical answer, embed *that* (not the query), and explain why
   the hypothetical lands nearer real relevant documents, and when it *hurts*.
4. **Decompose a multi-hop query and fuse results** — split into sub-questions, retrieve per
   sub-question, and **fuse** the union (dedupe + re-rank) without blowing the context budget.
5. **Measure each transform against the faithfulness eval** — prove *which* transforms help, and
   recognize that some don't (a transform that retrieves more but lowers faithfulness is a
   regression).
6. **Explain adaptive retrieval and self-critique** — that the most advanced move is sometimes
   *not to retrieve*, and always to critique relevance/support (Self-RAG).

---

## 1. Motivation

### Why this exists

Your Project 04 assistant retrieves with the user's question verbatim, then reads. It works when the
question's words match the document's words. It fails in two very common cases:

1. **Paraphrase miss.** The user asks "how do I get my money back?"; the document says "refund
   policy." A single embedding of the bare question may not land near the right passage.
2. **Multi-hop.** "Which of the founders went to the same university as the current CTO?" needs
   *two* retrievals (find the CTO's university; find founders from there) — one query can't get both.

Naive RAG treats the user's question as a fixed, perfect query. It isn't. This elective makes the
**query** a thing you engineer — rewrite it, expand it into a hypothetical answer, or split it —
before retrieval ever runs. The index and the re-ranker (Project 03) are *given*; the new surface
is the query stage.

### What breaks without it

Without query engineering, your retrieval ceiling is "the user phrased it well and the answer is in
one chunk." Real questions are messy and multi-part; you retrieve plausible-but-wrong context and
the reader confidently answers from it. And the trap on the *other* side: bolting on every fancy
transform without measuring — HyDE, rewriting, decomposition all *cost* a generation and can
*lower* faithfulness by dragging in distractors. The discipline is: add a transform only if the
eval says it helped.

> **Startup lens (StarcallOS).** A personal OS answers questions over *your* messy corpus — notes,
> emails, half-finished docs — where the phrasing never matches and questions span sources. Query
> engineering is what turns "search my stuff" from a keyword box into something that actually
> finds the multi-hop answer. And the eval is what stops you from shipping a clever transform that
> quietly made retrieval worse.

---

## 2. ELI12

Imagine a librarian. You walk up and mumble "that money-back thing." A *bad* librarian takes your
exact words to the shelf, finds nothing labeled "money-back thing," and gives up. A *good*
librarian does three smarter things:

1. **Rewrites your request** in library language — "ah, you mean the **refund policy**" — and finds
   it. (Query rewriting.)
2. **Imagines the answer first** — "a refund policy page probably says: *returns within 30 days, keep
   the receipt…*" — and looks for the shelf that has pages like *that*, not pages with your exact
   words. (HyDE.)
3. **Splits a two-part question** — "which founder went to the CTO's school?" becomes "where did the
   CTO study?" then "which founders studied there?" — two trips, then combines. (Decomposition.)

But here's the catch the good librarian knows: **fancier isn't always better.** Sometimes imagining
the answer leads you to the wrong shelf. So the good librarian *checks*: did this actually find a
better page than just using your words? That check is the eval, and it's the difference between a
clever librarian and a reliable one.

---

## 3. The Two Failure Modes of Naive Retrieve-Then-Read

Project 04's pipeline is `embed(question) → nearest chunks → read`. Two structural failures:

- **The question↔query gap.** "There is inevitably a gap between the input text and the needed
  knowledge in retrieval" (`query-rewriting-rag.md`). How a human asks ≠ how the answer is written.
  A bare-question embedding can miss the right passage entirely.
- **Single-shot retrieval can't multi-hop.** A compound question needs information from *different*
  places; one retrieval returns one neighborhood. You must split the question and retrieve per part.

Both are **query** problems, not index problems. The fix is upstream of retrieval.

---

## 4. Query Rewriting — Rewrite, Retrieve, Read

Instead of retrieving with the raw question, **reformulate it into a better retrieval query first**
(`query-rewriting-rag.md`). Prompt an LLM: "rewrite this question as a search query (or a few)."
The rewrite closes the question↔query gap — turning "how do I get my money back?" into "refund
policy return window eligibility."

The paper trains a small rewriter with RL from the reader's feedback; the cheap starting point (and
this elective's core) is an **LLM-prompted rewriter**. The risk to respect: a rewrite can **drift**
— change the meaning and retrieve the wrong thing — which is why it's gated on faithfulness.

---

## 5. HyDE — Embed a Hypothetical Answer, Not the Question

A question and its answer don't look alike in embedding space. **HyDE** (`hyde.md`) closes that gap
differently: **generate a hypothetical document** that *would* answer the query, then **embed that
document** (not the query) and retrieve its neighbors.

The hypothetical may contain wrong facts — that's fine. It "looks like" a relevant document, so its
embedding lands near genuinely relevant ones, and the encoder's **dense bottleneck filters out the
hallucinated specifics**: the hypothetical supplies the *shape* of a good answer; the real corpus
supplies the *facts*. The caution: HyDE can **hurt** on short factual lookups where the bare term
match was already good (the hypothetical adds noise). Measure it — never surface the hypothetical
itself as the answer.

---

## 6. Multi-hop Decomposition and Fusion

For a compound question, **decompose** it into sub-questions, **retrieve per sub-question**, then
**fuse** the results. Fusion is where this breaks if done naively:

- Concatenating every sub-question's chunks **blows the context budget** and **dilutes relevance**
  (more distractors → lower faithfulness).
- So **fuse = dedupe the union, then re-rank** it (Project 03's cross-encoder, *provided* here) and
  keep the top-N. The re-ranker is the tool that makes multi-query retrieval safe.

This is the transform with the most moving parts, and the one where "retrieved more" most easily
becomes "answered worse." The eval is the referee.

---

## 7. Re-Ranking the Union (Provided)

Re-ranking — retrieve broadly with the bi-encoder, then re-score the top-k with a cross-encoder — is
**Project 03's** lesson, so it is *provided* here, not rebuilt. Its role in this elective is the
**fusion stage**: it turns the noisy union of multi-query results into a clean, relevance-ordered
context. Do not re-implement it; *use* it.

---

## 8. Not Every Transform Helps — The Eval Is the Referee

This is the spine of the elective. Each transform costs a generation and can *lower* quality by
pulling in distractors. So you run **Project 04's faithfulness + answer-relevance eval**
(`ragas.md`) **per transform** — baseline vs. rewrite vs. HyDE vs. decomposition — and report which
actually helped on which queries. Expected honest findings:

- Rewriting helps the paraphrase cases, may drift on already-clear ones.
- HyDE helps conceptual queries, can hurt short factual ones.
- Decomposition helps multi-hop, costs the most and risks dilution.

A transform that raises retrieval recall but **lowers faithfulness** is a **regression**, not a win.
"More retrieved" is not the metric; "better-grounded answer" is.

---

## 9. Adaptive Retrieval and Self-Critique (Self-RAG) — The Advanced Move

The most advanced query decision is sometimes **not to retrieve at all**, and always to **critique
what you retrieved**. **Self-RAG** (`self-rag.md`) uses reflection to: (1) decide *retrieve-or-not*
before fetching, (2) judge whether each passage is *relevant*, (3) judge whether the answer is
*supported* by the passages. Always-retrieve RAG "indiscriminately incorporates a fixed number of
passages," which can drag in irrelevant context and degrade the answer.

In this elective Self-RAG is the **extension**: approximate the *behavior* with prompting — a
retrieve-or-not gate plus a relevance/support critique over the transformed pipeline — reframing
Project 04's faithfulness metric as an *inline* decision, not just a post-hoc score.

---

## Milestones

1. **M1 — Query rewriting:** reformulate the query; measure retrieval-hit lift on paraphrased cases.
2. **M2 — HyDE:** generate a hypothetical answer, embed it, retrieve; compare recall vs the raw query.
3. **M3 — Multi-hop decomposition:** split a compound question, retrieve per sub-question, fuse
   (dedupe + re-rank the union).
4. **M4 — Orchestrate:** transforms → retrieve → fuse → re-rank (provided) → read.
5. **M5 — Prove which helped:** run the faithfulness eval **per transform**; report honestly,
   including the transforms that didn't help.
6. **Extension:** Self-RAG-style retrieve-or-not gate + relevance/support critique; hybrid (BM25 +
   dense); GraphRAG over the corpus.

---

## Common Misconceptions

- **"The user's question is the query."** It's an *input to engineer*. The question↔query gap is the
  whole motivation for rewriting.
- **"HyDE embeds the question."** No — it embeds a *hypothetical answer*. And it can hurt on factual
  lookups; measure it.
- **"More retrieved context is better."** More distractors lower faithfulness. Fuse = dedupe +
  re-rank, not concatenate-everything.
- **"Advanced RAG means always retrieve more."** The advanced move is sometimes *not* retrieving, and
  always *critiquing* what you got (Self-RAG).
- **"I'll add HyDE + rewrite + decomposition because they're fancy."** Only if the eval says they
  helped. A transform that lowers faithfulness is a regression.
- **"I need to build re-ranking."** It's from Project 03 and provided — *use* it for fusion.

---

## Instructor Notes

- The **non-negotiable assessable idea** is *transforms must be eval-gated*: `EVALUATION.md` must
  report faithfulness **per transform**, including any that didn't help. A learner who adds HyDE
  and assumes it helped has missed the point.
- The **second** is the **fusion** discipline: dedupe + re-rank the union, not concatenate — or
  multi-hop *lowers* faithfulness.
- The **third** is the framing: the index + re-ranker are **given** (P03/P04); the **query stage**
  is the target. Don't let the learner rebuild retrieval.
- Keep it offline/deterministic: a provided corpus + retriever + canned rewrites/HyDE docs (a
  fixture) + the faithfulness checker make the whole thing gradeable without a provider; live LLM
  transforms are the extension.

---

## Sources

- `sources/papers/query-rewriting-rag.md` — Ma et al. 2023: Rewrite-Retrieve-Read; the
  question↔query gap; rewrite before retrieval.
- `sources/papers/hyde.md` — Gao et al. 2022: embed a hypothetical answer; the dense bottleneck
  filters hallucinations; can hurt on factual lookups.
- `sources/papers/self-rag.md` — Asai et al. 2023: adaptive retrieve-or-not + relevance/support
  self-critique; the advanced move is sometimes not retrieving.
- `sources/papers/ragas.md` — faithfulness/answer-relevance: the per-transform gate.
