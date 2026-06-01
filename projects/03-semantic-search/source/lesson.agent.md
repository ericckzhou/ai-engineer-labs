# Lesson 03: Semantic Search
<!-- lesson.agent.md — Agent-optimized canonical source. Do not simplify; this is the truth layer. -->

## Metadata

| Field | Value |
|-------|-------|
| Project | 03-semantic-search |
| Core Concepts | vector databases, indexing, approximate nearest neighbor (HNSW), retrieval, distance vs similarity, re-ranking |
| Prerequisites | See PROJECT.md (Project 02 complete: embeddings + cosine from scratch; Python + numpy) |
| Difficulty | Intermediate |
| Estimated Time | See PROJECT.md (6–10 hours total) |
| Last Updated | 2026-06-01 |

---

## Learning Objectives

By completing this lesson, the learner will be able to:

1. Explain why a **brute-force cosine scan** (Project 02) does not scale, and what a **vector database** adds on top of raw embeddings.
2. Build a semantic search index with **Chroma**: create a collection, add documents (id + embedding + document + metadata), and query it.
3. Explain **approximate nearest neighbor (ANN)** search and how **HNSW** achieves roughly `O(log N)` query time instead of `O(N)` — and why it is *approximate*.
4. Convert correctly between **distance and similarity**, and avoid the silent ranking-inversion bug (Chroma returns *distances*; lower = closer).
5. Choose and justify a **distance space** (`cosine` vs `l2` vs `ip`) for text embeddings.
6. Compare ANN results against the exact brute-force baseline and **measure recall**, not just eyeball it.
7. Explain the **retrieve-then-rerank** pattern (bi-encoder retrieves, cross-encoder re-ranks) and when it is worth the cost.

---

## Prerequisite Knowledge Check

Before beginning, the learner should be able to answer:

1. From Project 02: what does `embed(text)` return, and how did you rank a small corpus against a query by cosine?
2. What is the difference between cosine *similarity* and cosine *distance*? (If unsure, revisit `sources/official-docs/scikit-learn-cosine-similarity.md`.)
3. Why is embedding dimensionality model-specific, and why must query and corpus use the **same** embedding model?

If the learner cannot rank a corpus by cosine from Project 02, complete that first — Project 03 builds directly on it.

---

## Core Concepts

| Concept | Definition | Why It Matters |
|---------|-----------|----------------|
| Vector database | A store for embeddings that indexes them for fast similarity search and supports metadata filtering | Turns "a list of vectors" into a queryable system; the operational home of embeddings. (source: `sources/official-docs/chromadb.md`) |
| Collection | A named set of records, each with an id, embedding, document, and metadata | The unit you add to and query in Chroma. (source: `sources/official-docs/chromadb.md`) |
| Approximate Nearest Neighbor (ANN) | Finding the closest vectors *without* comparing against every stored vector | Makes search sub-linear; the reason a vector DB is fast at scale. (source: `sources/papers/hnsw.md`) |
| HNSW | Hierarchical Navigable Small World graphs — the multi-layer graph index Chroma uses | Achieves ~`O(log N)` search via greedy routing through layered proximity graphs. (source: `sources/papers/hnsw.md`) |
| Distance vs. similarity | Distance: lower = closer. Similarity (cosine): higher = closer | Chroma returns **distances**; treating them as similarities silently inverts rankings. (source: `sources/official-docs/chromadb.md`) |
| Distance space | The metric the index uses: `l2` (default), `cosine`, or `ip` | Must match what your embedding model expects; text usually wants `cosine`. (source: `sources/official-docs/chromadb.md`) |
| Re-ranking | A second pass that re-scores the top-k candidates with a cross-encoder | Buys accuracy on the few results that matter, after cheap retrieval. (source: `sources/articles/sbert-retrieve-rerank.md`) |

### Concept Relationships

```
corpus → [embed each doc] → vectors → [vector DB: HNSW index + storage]   (build once)
query  → [embed] → vector → [ANN search over index] → top-k by distance    (per query)
top-k  → [optional: cross-encoder re-rank] → final ranking                 (accuracy pass)
```

Critical distinction: **the embeddings are the same as Project 02; the database is new.** A vector DB is
essentially *an HNSW index + storage + a query API* wrapped around the vectors you already know how to
produce. It solves scale and persistence, not meaning.

---

## Section 1: Motivation

### Why This Exists
In Project 02 you ranked a corpus by computing cosine against **every** document. That is an exact
`O(N)` scan: fine for 6 sentences, hopeless for 6 million. Real semantic search — over documents,
products, past messages — needs two things the brute-force loop lacks: **speed at scale** and
**persistence** (build the index once, query it forever). A **vector database** provides both.

### The Problem We're Solving
Embeddings alone are just a pile of vectors. To make them useful you must *store* them, *index* them so
search is fast, and *query* them with filters. Doing this by hand (recomputing cosine over a giant list
every query, re-embedding on every restart) is exactly the work a vector DB removes.

### Real-World Stakes
Every production search, RAG pipeline, recommendation engine, and "find related" feature runs on a
vector DB under the hood. Get the **distance-vs-similarity** direction wrong and your "most relevant"
result is actually your *least* relevant — a silent bug with no error (source:
`sources/official-docs/chromadb.md`). Pick the wrong **distance space** and rankings degrade quietly.
Misunderstand **ANN** and you will be surprised when the "nearest" neighbor is occasionally missed.

### Would Users Pay For This?
Yes — this is the first project that builds a component users actually pay for. Search quality is the
product in countless apps. The judgment built here (index design, metric choice, recall measurement,
when to re-rank) is what separates a search box that feels magic from one that feels broken.

---

## Section 2: Mental Model

### ELI12 (Explain Like I'm 12)
In Project 02 you found the closest word by checking every single house in the city, one by one. That
works for a small town. Now imagine the whole country. Instead of visiting every house, you use a
**map with zoom levels**: start zoomed all the way out, jump to the right region, zoom in, jump to the
right city, zoom in again, until you're on the right street. You only visited a handful of places, not
the whole country — but you almost always land on the right house. That zoom-map is **HNSW**, and the
filing cabinet that holds all the addresses and lets you do this is the **vector database**.

### ELI-Engineer (Explain to a Software Engineer)
- A **vector database** is an index + storage + query API over embeddings. In Chroma: a `collection`
  holds records of `(id, embedding, document, metadata)`; `collection.query(query_embeddings=...,
  n_results=k)` returns the k nearest by distance (source: `sources/official-docs/chromadb.md`).
- The index is **HNSW**: a hierarchical set of proximity graphs searched by greedy routing from the top
  layer down, giving ~`O(log N)` query time instead of the `O(N)` brute-force scan (source:
  `sources/papers/hnsw.md`). It is **approximate** — it can occasionally miss the true nearest neighbor,
  trading a little recall for a lot of speed.
- Chroma returns **distances, not similarities** — "lower distance = more similar." With `space="cosine"`,
  cosine distance ≈ `1 − cosine_similarity` (source: `sources/official-docs/chromadb.md`,
  `sources/official-docs/scikit-learn-cosine-similarity.md`).

### Real-World Analogy
A vector DB is a **library with a very good librarian**, not a pile of books. The embeddings are the
books' "meaning coordinates"; the HNSW index is the librarian who, instead of reading every spine, walks
you straight to the right shelf. Brute-force search is reading every spine in the building — correct, but
you'll be there all year.

### Intuition Diagram
```
 Build (once):
   docs ──embed──► [v1 v2 ... vN] ──add──► Chroma collection ──► HNSW index on disk

 Query (per request):
   "monetary policy"
        │ embed
        ▼
     q-vector ──► HNSW greedy routing (top layer → bottom) ──► top-k ids + DISTANCES
                                                                  (lower = closer)
        compare to brute-force exact scan ──► measure recall (did ANN find the true top-k?)
```

---

## Section 3: Technical Explanation

### Formal Definition
- **Vector search**: given a query vector `q` and a set `{v_1..v_N}`, return the `k` vectors minimizing a
  distance `d(q, v_i)` (or maximizing similarity). **Exact** search evaluates all `N` (`O(N)`).
  **Approximate (ANN)** search uses an index to evaluate far fewer (source: `sources/papers/hnsw.md`).
- **HNSW**: a "multi-layer structure consisting from hierarchical set of proximity graphs (layers) for
  nested subsets of the stored elements," with layer membership drawn from "an exponentially decaying
  probability distribution," searched greedily from the top layer down — yielding "logarithmic complexity
  scaling" (source: `sources/papers/hnsw.md`).

### How It Works (Mechanically)

**Build the index.** Embed each document once, then `collection.add(ids=, embeddings=, documents=,
metadatas=)`. Chroma inserts each vector into the HNSW graph, linking it to its nearest existing nodes
(`max_neighbors`/M controls how many links; `ef_construction` controls build-time search breadth)
(source: `sources/official-docs/chromadb.md`).

**Query.** `collection.query(query_embeddings=[q], n_results=k)` runs greedy routing through the graph
(`ef_search` controls how many candidates are explored — higher = better recall, slower) and returns
`ids`, `documents`, `distances`, `metadatas`. **Distances, not similarities** (source:
`sources/official-docs/chromadb.md`).

**Distance ↔ similarity.** For `space="cosine"`, convert with `similarity = 1 − distance`. Reporting the
raw distance as a "score where higher is better" is the classic inversion bug.

### The Math (When Necessary)
- Brute-force exact search cost: `O(N·d)` per query (N vectors, d dimensions).
- HNSW search cost: ~`O(d·log N)` per query — the whole point (source: `sources/papers/hnsw.md`).
- Cosine distance (Chroma `space="cosine"`): `d_cos(a,b) = 1 − (a·b)/(‖a‖‖b‖)`, so `d ∈ [0, 2]`, and
  `similarity = 1 − d ∈ [−1, 1]` (source: `sources/official-docs/scikit-learn-cosine-similarity.md`).

### Implementation Details
- **Pin one embedding model for add *and* query.** Mixing models makes distances meaningless — a silent
  bug, no error (carries from Project 02).
- **Default `space` is `l2`; for text you usually want `cosine`** — set it explicitly when creating the
  collection (source: `sources/official-docs/chromadb.md`).
- **Persist the index.** `PersistentClient(path=...)` writes the collection to disk so you embed once and
  reuse across runs (source: `sources/official-docs/chromadb.md`).
- **ANN is approximate.** Validate by comparing the top-k against a brute-force exact scan and computing
  recall@k; tune `ef_search` if recall is too low (source: `sources/papers/hnsw.md`).
- **Re-ranking is a second stage.** Retrieve ~100 candidates with the bi-encoder/vector DB, then re-score
  those with a cross-encoder for the final order — never run the cross-encoder over the whole corpus
  (source: `sources/articles/sbert-retrieve-rerank.md`).

---

## Section 4: Guided Examples

> The lab stack: `chromadb` (vector DB / HNSW), `litellm` (embeddings via `config.py`, default local
> `ollama/nomic-embed-text`, 768-dim), `numpy` (the brute-force baseline). See `code/`.

### Example 1: Simple Case — build and query a collection
```python
import chromadb
from embedding_helpers import embed_many   # wraps litellm; returns list[list[float]]

docs = [
    "The central bank raised interest rates this quarter.",
    "A young wizard attends a school of magic.",
    "Photosynthesis converts sunlight into energy in plants.",
]
client = chromadb.Client()                                  # in-memory for the demo
col = client.create_collection("demo", metadata={"hnsw:space": "cosine"})  # text → cosine
col.add(ids=["d0", "d1", "d2"], embeddings=embed_many(docs), documents=docs)

q = embed_many(["monetary policy and the economy"])[0]      # query is lexically unlike doc 0
res = col.query(query_embeddings=[q], n_results=2)
print(res["documents"][0])     # most similar first
print(res["distances"][0])     # LOWER distance = MORE similar  (not a similarity!)
```
**What to observe:** the finance sentence ranks first despite sharing no words with the query — semantic,
not lexical. And the returned numbers are *distances* (smaller is better), not the cosine *similarities*
from Project 02.

### Example 2: Real-World Case — distance → similarity, done right
```python
def to_similarity(distance: float) -> float:
    # Chroma space="cosine" returns cosine DISTANCE in [0, 2]; similarity = 1 - distance.
    return 1.0 - distance

for doc, dist in zip(res["documents"][0], res["distances"][0]):
    print(f"{to_similarity(dist):+.3f}   {doc}")   # +higher = more relevant, human-readable
```
**What to observe:** ranking by ascending distance and by descending `1 − distance` give the **same**
order. If you ever sort distances descending (thinking "higher = better"), you return the *worst*
matches first — the silent inversion bug.

### Example 3: Edge Case — ANN is approximate; measure it
```python
import numpy as np
def cosine(a, b): return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))

# Exact brute-force ranking (Project 02 style) over the same vectors:
qv = np.array(q)
vecs = [np.array(v) for v in embed_many(docs)]
exact_order = [i for i, _ in sorted(enumerate(vecs), key=lambda t: -cosine(qv, t[1]))]

# recall@k = |ANN top-k ∩ exact top-k| / k   (map Chroma's returned ids back to indices)
ann_ids = res["ids"][0]                      # e.g. ["d0", "d2"]
ann_idx = [int(i[1:]) for i in ann_ids]      # -> [0, 2]
k = len(ann_idx)
recall = len(set(ann_idx) & set(exact_order[:k])) / k
print("recall@%d = %.2f" % (k, recall))
```
**What to observe:** on a tiny corpus HNSW and brute force agree perfectly (recall@k = 1.0). The point is
the *method*: in production you confirm ANN quality by comparing against the exact baseline and watching
recall as you change `ef_search` — not by trusting that "the database is correct" (source:
`sources/papers/hnsw.md`).

---

## Section 5: Reflection Before Building

> The learner should fill UNDERSTANDING.md before proceeding to implementation.

**Questions to answer in UNDERSTANDING.md:**

1. Explain, in your own words, what a vector database adds on top of the embeddings + cosine you wrote in Project 02. What problem does it actually solve?
2. Draw the build-time vs. query-time data flow. What happens once (and is reused) vs. on every query?
3. Predict: Chroma returns `distances`. If you sort them descending to get "best first," what do you actually get, and why is there no error?
4. Why is HNSW search *approximate*? What would you measure to know whether the approximation is good enough?
5. The default `space` is `l2`. Why might `cosine` be the right choice for text embeddings — and how would you confirm it matters?
6. When is it worth adding a cross-encoder re-ranking stage, and why not just use the cross-encoder for everything?

---

## Section 6: Project Assignment

See PROJECT.md for the full project specification.

### Core Requirement
Build a semantic search engine in `code/` over a provided corpus:
- **`indexer.py`** — embed a corpus and build a **persistent** Chroma collection (`space="cosine"`),
  with document text + metadata. Idempotent: re-running does not duplicate records.
- **`semantic_search.py`** — embed a query, run `collection.query`, and return ranked
  `(document, similarity, metadata)` results with **distance correctly converted to similarity**.
- **`baseline.py`** — an exact brute-force cosine ranking (reuse Project 02's cosine) used to validate
  the vector DB, plus a `recall_at_k(...)` helper.
- **`evaluate.py`** — run a set of queries through both paths and report **recall@k** of the ANN index
  vs. the exact baseline.

### Extended Requirements
- Add a **cross-encoder re-ranking** stage (`rerank.py`): retrieve top-k with the vector DB, re-order with
  a cross-encoder, and report how the top result changed (source: `sources/articles/sbert-retrieve-rerank.md`).
- Compare `space="cosine"` vs `space="l2"` on the same corpus and explain the ranking differences.
- Sweep `ef_search` and record recall vs. (qualitative) latency.

---

## Section 7: Project Milestones

| Milestone | What You Build | Validation |
|-----------|---------------|------------|
| M1: Index | `indexer.py` builds a persistent Chroma collection from the corpus | Collection count == number of docs; re-running does not duplicate |
| M2: Query | `semantic_search.py` returns top-k for a query | A semantically-related-but-lexically-different doc ranks first |
| M3: Distance→similarity | Convert Chroma distances to similarities correctly | Ascending-distance order == descending-similarity order (no inversion) |
| M4: Baseline | `baseline.py` reproduces exact cosine ranking from Project 02 | On the corpus, baseline top-1 matches your hand-checked expectation |
| M5: Recall | `evaluate.py` computes recall@k of ANN vs. exact baseline | recall@k reported as a number across several queries |
| M6: Break/Extend | Re-ranking and/or `space`/`ef_search` experiments documented | At least one surprising result recorded in FAILURE_ANALYSIS.md |

---

## Section 8: Self-Evaluation

| Criterion | Does your implementation... | Pass? |
|-----------|---------------------------|-------|
| Real index | build and persist an actual Chroma collection (not an in-memory list)? | |
| Semantic win | rank a paraphrase/related doc above a keyword-overlapping but unrelated one? | |
| Direction correct | convert distance→similarity so higher = more relevant, with no inversion? | |
| Metric choice | set `space="cosine"` deliberately for text, not rely on the `l2` default? | |
| Measured, not eyeballed | report recall@k vs. the exact baseline as a number? | |
| Same model both sides | embed corpus and query with the identical model? | |

**Red flags (your implementation may have problems if):**
- You sort Chroma `distances` descending and call the top result "best."
- You re-embed the entire corpus on every query instead of indexing once.
- You compare embeddings produced by different models across add and query.
- You claim the search "works" with no recall number or baseline comparison.
- You run a cross-encoder over the whole corpus instead of re-ranking a small candidate set.

---

## Section 9: Common Mistakes

| Mistake | Why It Happens | Consequence | Fix |
|---------|---------------|-------------|-----|
| Treating distance as similarity | Project 02 returned similarity; Chroma returns distance | Rankings silently inverted (worst shown as best) | `similarity = 1 − distance`; sort by ascending distance (source: `sources/official-docs/chromadb.md`) |
| Leaving `space` at default `l2` for text | Default is `l2`; text wants `cosine` | Subtly worse rankings, no error | Set `metadata={"hnsw:space": "cosine"}` (source: `sources/official-docs/chromadb.md`) |
| Re-embedding the corpus every query | Forgetting the index is built once | Slow, expensive; defeats the vector DB | Index once with a `PersistentClient`; query many |
| Expecting ANN to be exact | "It's a database, it must be right" | Surprise when a true neighbor is missed | ANN is approximate; measure recall@k, tune `ef_search` (source: `sources/papers/hnsw.md`) |
| Mixing embedding models | Corpus and query embedded at different times/models | Meaningless distances, silent garbage | Pin one model for both sides |
| Cross-encoder over the whole corpus | "It's more accurate" | Far too slow at scale | Retrieve top-k cheaply, then re-rank those (source: `sources/articles/sbert-retrieve-rerank.md`) |

---

## Section 10: Connections

### How This Connects to Previous Projects
Project 02 produced embeddings and ranked them by cosine **by hand** over a tiny corpus. Project 03 keeps
the exact same embeddings and cosine intuition but moves storage and search into a **vector database** so
it scales and persists. Your Project 02 `cosine_similarity` becomes the **exact baseline** you validate
the database against.

### How This Connects to Future Projects
This is the retrieval engine of **Project 04 (RAG / PDF assistant)** — RAG = *this* search step feeding
retrieved chunks to an LLM. **Project 05 (memory)** stores and recalls past items by the same vector-DB
lookup. The re-ranking pattern reappears wherever first-stage retrieval isn't precise enough.

### How This Connects to StarcallOS
Any StarcallOS "find related things" feature — recall a note, surface a command, match a request to a
capability — is a vector-DB query underneath. The judgment built here (index once, choose the metric,
measure recall, re-rank when it matters) decides whether that recall feels instant and right or slow and
wrong.

### Production Patterns
The standard architecture is **two-stage retrieval**: a bi-encoder + ANN index retrieves a broad
candidate set fast; a cross-encoder re-ranks the top-k precisely (source:
`sources/articles/sbert-retrieve-rerank.md`, `sources/papers/sentence-bert.md`). Add metadata filtering
(`where`) for hard constraints, and persist the index so it survives restarts.

---

## Assessment Rubric

See source/rubric.md for the complete grading rubric.

**Summary criteria:**
- [ ] Implementation runs correctly (persistent index, semantic query, baseline, recall eval)
- [ ] Understanding document completed in learner's own words
- [ ] Failure analysis demonstrates intentional experimentation (metric swap, ef_search, re-ranking, inversion)
- [ ] Evaluation is quantitative (recall@k vs. exact baseline; real distances/similarities)
- [ ] StarcallOS reflection identifies at least one concrete applicable pattern

---

## Sources

See source/resources.md for the full annotated source list.

**Required reading:**
- `sources/official-docs/chromadb.md` — vector DB data model, query API, HNSW, distance vs similarity, `space`
- `sources/papers/hnsw.md` — why ANN search is ~O(log N) and approximate
- `sources/official-docs/scikit-learn-cosine-similarity.md` — cosine, to reconcile similarity with Chroma's distance

**Recommended reading:**
- `sources/articles/sbert-retrieve-rerank.md` — retrieve-then-rerank two-stage pattern
- `sources/papers/sentence-bert.md` — bi- vs cross-encoder; encode-once/compare-many

---

## Instructor Notes

<!-- Hidden context for the mentor reviewing the learner's work. -->

**Common misconceptions:**
- That a vector database "does something to the meaning." It does not — it stores and indexes the same embeddings; it adds speed, persistence, and filtering.
- That distances are similarities. Chroma returns distances; lower is closer. This is the single most common bug in the project.
- That ANN/HNSW returns the exact nearest neighbors. It is approximate by design.
- That higher embedding dimension or a bigger index is automatically "better."

**Diagnostic questions (reveal genuine vs. surface understanding):**
- "Chroma returned distance 0.12 and 0.40 for two docs — which is more relevant, and why?" (distance direction)
- "Your search and your Project-02 brute force disagree on rank 5. Is that a bug?" (ANN approximation + recall thinking)
- "Why set `space='cosine'` when `l2` is the default?" (metric choice for text)
- "When would you add a cross-encoder, and why not use it for the whole corpus?" (two-stage retrieval economics)

**Signs of genuine understanding:**
- The learner indexes once and queries many, with a persistent client, unprompted.
- They report recall@k against a brute-force baseline rather than asserting "it works."
- They catch the distance-vs-similarity direction without being told.
- Their Failure Analysis includes a deliberate metric or `ef_search` change with a measured effect.
