# Elective 05: Advanced RAG / Query Engineering — Implementation Plan

> **Status: PLANNED — awaiting approval before authoring.**
> `/plan` output (Workflow A, pre-execution). No `source/`, `code/`, or `rendered/` yet.
> **Track:** Production & Hardening (named elective track, recommended after the P09 capstone;
> off the numbered 1–9 spine). Depth elective extending the retrieval spine (P03–P04).
> See `memory/project/decisions/2026-06-09-production-hardening-elective-track.md`.

---

## Requirements Restatement

Take Project 04's **naive retrieve-then-read** RAG and add a **query-transformation stage** that
fixes its two biggest failure modes — paraphrased queries that miss lexically, and multi-hop
questions a single retrieval can't answer. The learner adds:

- **Query rewriting** (reformulate the user question for retrieval).
- **HyDE** (generate a hypothetical answer, embed *that*, retrieve against it).
- **Multi-hop decomposition** (split a compound question, retrieve per sub-question, fuse).

…and measures each against **Project 04's faithfulness eval** to prove *which transforms
actually help* — not assume they do.

The thesis: *retrieval quality is a query problem as much as an index problem; and every
"advanced" technique must justify itself against the eval, or it's just cost.*

---

## Where It Fits / Prerequisites

- **Prereqs:** Project 03 (vector retrieval + re-ranking — re-ranking is already built there, so
  it's *provided* here), Project 04 (the RAG pipeline + faithfulness eval being extended),
  Project 02 (embeddings — HyDE embeds a generated document).
- **Slot:** after Project 04. It is the "what next" for retrieval.

---

## Learning Target (the incomplete core)

The learner owns the **query-transformation stage** — not the retriever, index, or eval (all
provided from P03/P04).

```
query_transforms.py   (learner)
  rewrite(query)            -> str                  # reformulate for retrieval
  hyde(query)               -> str                  # generate hypothetical doc to embed
  decompose(query)          -> list[str]            # split a multi-hop question
advanced_rag.py       (partial)
  answer(query) -> Result   # transform -> retrieve(per query) -> fuse -> rerank(provided) -> read
```

Provided: P04 retriever + corpus + the faithfulness/answer-relevance eval, P03 re-ranking, the
model-call plumbing. Incomplete: the three transforms and the fusion of multi-query results.

---

## Primary Sources to Gather (Workflow A step 1)

| Source | Anchors | Status |
|--------|---------|--------|
| **HyDE** — Gao et al. 2022, "Precise Zero-Shot Dense Retrieval without Relevance Labels" (arXiv:2212.10496) | generate a hypothetical document, embed it, retrieve | ⏳ fetch & verify |
| **Rewrite-Retrieve-Read** — Ma et al. 2023 (arXiv:2305.14283) | a learned/LLM query rewriter in front of retrieval | ⏳ fetch & verify |
| **Self-RAG** — Asai et al. 2023 (arXiv:2310.11511) | retrieve-on-demand + self-critique (the "should I even retrieve / did it help" decision) | ⏳ fetch & verify |
| **RAGAS** — already in repo | faithfulness / answer-relevance metrics used as the gate | ✅ in repo (`sources/papers/ragas.md`) |
| **RAG paper** — already in repo | the baseline being extended | ✅ in repo |

→ New sources land in `sources/papers/`. Update `catalogs/source-map.md` + re-render.

---

## File Manifest

| File | Role | Purpose |
|------|------|---------|
| `code/config.py` | provided | provider block + retrieval params (k, rerank top-n, transform toggles) |
| `code/rag_backend.py` | reference | condensed P04 retriever + corpus + reader, offline-capable |
| `code/rerank.py` | provided | P03 cross-encoder re-ranking (already learned — not the target here) |
| `code/query_transforms.py` | **learner** | `rewrite`, `hyde`, `decompose` |
| `code/advanced_rag.py` | partial | the multi-query orchestration + fusion, with TODOs |
| `code/eval_set.jsonl` | provided | P04's frozen QA set incl. paraphrased + multi-hop cases |
| `code/evaluate_rag.py` | provided | faithfulness + answer-relevance + retrieval-hit, **per transform** (baseline vs each) |
| `code/tests/` | provided | offline tests for each transform + fusion |
| setup files | provided | one-command run + test |
| `source/*`, `rendered/lesson.html`, root stubs | reference | lesson, contracts, rubric, HTML |

---

## Milestones (4–6)

1. **M1 — Query rewriting:** reformulate the query; measure retrieval-hit lift on the
   paraphrased cases.
2. **M2 — HyDE:** generate a hypothetical answer, embed it, retrieve; compare recall vs raw query.
3. **M3 — Multi-hop decomposition:** split a compound question, retrieve per sub-question, fuse
   (dedupe + merge) the contexts.
4. **M4 — Orchestrate + rerank:** run transforms → retrieve → fuse → re-rank (provided) → read.
5. **M5 — Prove which helped:** run `evaluate_rag.py` **per transform**; some transforms will
   *not* help (or cost more for no gain) — report that honestly.
6. **Extension:** Self-RAG-style "retrieve-or-not" gate; GraphRAG over the corpus; hybrid
   (BM25 + dense) — the hook already noted in `concept-map.md`.

---

## Difficulty Spikes

1. **Not every transform helps.** The honest result is the lesson: HyDE can *hurt* on factual
   short queries; rewriting can drift. The per-transform eval is what makes this visible.
2. **Fusion is where multi-hop breaks.** Naively concatenating per-sub-question contexts blows
   the context budget and dilutes relevance; dedupe + re-rank the union.
3. **Don't double-build re-ranking.** It's from P03 and *provided* — the target is the query
   stage, not the index stage.
4. **Faithfulness still governs.** A transform that retrieves more but lowers faithfulness (more
   distractors) is a regression — gate on P04's metric, not raw recall.

---

## Risks

- **LOW–MEDIUM:** transforms require live model calls; keep an offline deterministic path (canned
  rewrites/HyDE docs in a fixture) so tests + the demo run without a provider.
- **LOW:** overlap with P03/P04 — must be explicit in the lesson that index + re-ranking are
  *given*, so the learner doesn't rebuild them.

## Estimated Complexity: **MEDIUM** (heavy reuse of P03/P04; the transforms are the new surface).
