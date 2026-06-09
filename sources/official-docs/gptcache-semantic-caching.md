# GPTCache — Semantic Caching for LLMs

**Type:** official-docs (open-source library)
**Publisher:** Zilliz
**Link:** https://github.com/zilliztech/GPTCache

> Primary source for **Elective 03 — Cost & Latency Engineering** (the semantic-cache lever, M2).
> Reference design for an embedding-similarity cache; faithful summary.

---

## What it is

A **semantic cache**: store past (query → answer) pairs and, for a new query, return a stored
answer when a *semantically similar* query was seen before — without calling the LLM again. The
elective builds a small version of this.

## Exact-match vs. semantic cache

A traditional cache needs the **identical** key. A semantic cache hits on **meaning**: "what is
GitHub" and "can you explain GitHub" resolve to the same cached answer, so hit rates are far
higher than exact-match — the cost saving is on a *repeated kind of question*, not a repeated
string.

## Components (the design to mirror)

- **Embedding generation** — encode the query to a vector (same embedder for store and lookup —
  Project 02's rule).
- **Vector store + similarity search** — find the nearest stored query (FAISS/Milvus/etc.;
  Project 03's ANN).
- **Cache storage** — the stored answers.
- **Similarity evaluator + threshold** — decide a **hit** when nearest-neighbor similarity clears
  a configurable threshold.
- **Cache manager** — eviction policy (LRU/FIFO/LFU).

## How a hit is decided

Embed the incoming query → search the vector store → compare the top similarity to a
**threshold**. Above threshold ⇒ return the cached answer (a hit); below ⇒ miss, call the LLM,
store the result.

## The critical risk (the lesson's failure mode)

**A too-loose threshold returns a stored answer for a different question.** The cache reports a
"hit" but serves a wrong, confidently-cached answer. So the threshold is a precision/recall dial
exactly like a guard's — and the eval (Project 07's set) is what catches a false hit. Hit *rate*
alone is a vanity metric; correctness-under-hits is the real one.

## Why it anchors the elective

It connects Projects 02 (embeddings) and 03 (ANN) to a production cost lever, and it has a
quality risk (the false hit) that the eval must police — reinforcing the elective's thesis that
cost optimization is only safe behind an eval.

## Known issues / cautions

- Threshold tuning is the whole game; too loose = wrong answers, too tight = no hits (no saving).
- Reuse the **same** embedding model for store and query, or similarities are meaningless.
- A semantic cache is for *recurring* questions; on all-unique queries it only adds embedding cost.
