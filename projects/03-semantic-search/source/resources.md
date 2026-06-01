# Resources & Sources

> All sources used for this lesson, organized by tier.
> Every claim in lesson.agent.md traces back to one of these.

---

## Tier 1: Official Documentation

> Primary sources. Check these first.

- **Chroma (ChromaDB) documentation** — `sources/official-docs/chromadb.md`
  - URL: https://docs.trychroma.com/
  - What to read: the collection → add → query loop; embedding functions; the `query()` API.
  - Key sections: collections & data model (id/embedding/document/metadata); `collection.query()` (`query_texts`/`query_embeddings`, `n_results`, returned `distances`); HNSW index & `space` (l2 default / cosine / ip); `ef_search`/`ef_construction`/`max_neighbors`; persistent vs in-memory client.

- **scikit-learn cosine similarity** — `sources/official-docs/scikit-learn-cosine-similarity.md` (carried from Project 02)
  - URL: https://scikit-learn.org/stable/modules/metrics.html#cosine-similarity
  - What to read: the cosine formula and that it measures angle. Needed to understand Chroma's *distance vs. similarity* inversion.

---

## Tier 2: Foundational Papers

> Academic papers that established the concepts in this lesson.

- **HNSW** — `sources/papers/hnsw.md`
  - Title: Efficient and Robust Approximate Nearest Neighbor Search using Hierarchical Navigable Small World Graphs
  - Authors: Yu. A. Malkov, D. A. Yashunin
  - Year: 2016 (TPAMI 2020)
  - URL: https://arxiv.org/abs/1603.09320
  - Why it matters: the index behind every vector DB. Explains how ANN search hits ~O(log N) vs O(N) brute force, and why it is *approximate*.

- **Sentence-BERT (SBERT)** — `sources/papers/sentence-bert.md` (carried from Project 02)
  - Title: Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks
  - Authors: Nils Reimers, Iryna Gurevych
  - Year: 2019
  - URL: https://arxiv.org/abs/1908.10084
  - Why it matters: the bi-encoder / encode-once-compare-many property that makes indexable retrieval possible; origin of the bi- vs cross-encoder distinction used in re-ranking.

---

## Tier 3: Engineering Blogs

> Practical engineering perspectives from teams who've shipped this in production.

- **Retrieve & Re-Rank (Sentence-Transformers)** — `sources/articles/sbert-retrieve-rerank.md`
  - Title: Retrieve & Re-Rank
  - Source (company): UKP Lab / Sentence-Transformers
  - URL: https://www.sbert.net/examples/applications/retrieve_rerank/README.html
  - Key insight: retrieve broadly with a bi-encoder (fast over millions), re-rank the top-k with a cross-encoder (accurate); cross-encoder alone can't scale.

---

## Tier 4: Educational Sources

> Tutorials, courses, and explanatory content useful for learning.

- (None specific to this lesson. The Project 02 embedding sources — `word2vec.md`, `sentence-bert.md` — are the conceptual prerequisites.)

---

## Recommended Reading Order

For a learner new to this topic:

1. Start with: `sources/official-docs/chromadb.md` — see the concrete collection/query loop you'll build.
2. Then read: `sources/papers/hnsw.md` — understand what makes the query fast (and approximate).
3. Then read: `sources/official-docs/scikit-learn-cosine-similarity.md` — reconcile cosine *similarity* with Chroma's *distance*.
4. For depth: `sources/articles/sbert-retrieve-rerank.md` + `sources/papers/sentence-bert.md` — the two-stage retrieve-then-rerank pattern.

---

## Further Reading

Topics adjacent to this lesson worth exploring later:

- Hybrid search (dense + BM25/keyword) — Chroma supports keyword/regex alongside dense vectors.
- Other vector stores (Qdrant, Weaviate, FAISS, pgvector) — all use HNSW or similar ANN indexes.
- Metadata filtering strategies (pre- vs post-filtering) and their recall implications.
