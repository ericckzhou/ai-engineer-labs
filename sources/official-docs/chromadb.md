# Chroma (ChromaDB) — Vector Database Documentation

**Type:** official-docs
**Tier:** 1 (Official Documentation)
**Author(s):** Chroma (chromadb)
**Date:** docs accessed 2026-06-01
**URL:** https://docs.trychroma.com/
**Accessed:** 2026-06-01

## Why This Source Matters

Project 02 computed cosine similarity over a tiny in-memory corpus by hand. That does not scale: ranking a query against millions of vectors by brute-force cosine is too slow. A **vector database** solves the storage + fast-retrieval problem. Chroma is the lab's vector DB for Project 03 (Semantic Search): it is open-source, `pip install chromadb`, runs embedded in-process (no server), and exposes exactly the collection → add → query loop the project is built around. It grounds every concrete claim about how a real vector store indexes and queries embeddings.

## Key Claims

### What Chroma is and its data model
- "Chroma is the open-source data infrastructure for AI." It is a vector database for storing and retrieving embeddings.
- Data is organized into **collections**. Each record in a collection has: an **id**, an **embedding** (the vector), an optional **document** (the original text), and optional **metadata** (key/value pairs used for filtering).
- You can **bring your own embeddings** or attach an **embedding function** ("use any embedding model. OpenAI, Cohere, Hugging Face, sentence-transformers, and more"). With an embedding function attached, Chroma embeds text for you on `add` and `query`.

### Indexing — HNSW / approximate nearest neighbor
- Chroma "uses an HNSW (Hierarchical Navigable Small World) index to perform approximate nearest neighbor (ANN) search" in single-node deployments. (This is *approximate* — it trades a small amount of recall for large speedups; see `sources/papers/hnsw.md`.)
- The distance function is set by the collection's `space` parameter, with three options:
  - **`l2`** — squared L2 (Euclidean) distance. **This is the default.**
  - **`cosine`** — cosine distance; for "text embeddings or cases where you care about direction rather than scale."
  - **`ip`** — inner product.
- Key tunable HNSW parameters: `ef_construction` (candidate list size at build time, default `100`), `ef_search` (candidate list size at query time, default `100`), and `max_neighbors` (max graph connections per node, i.e. HNSW's M, default `16`). Larger values → better recall, slower/more memory.
- The chosen `space` must match what your embedding function expects (most sentence/text embedders are designed for cosine).

### Querying
- Query via `collection.query(...)`. Provide either `query_texts=["..."]` (Chroma embeds via the collection's embedding function) or `query_embeddings=[[...]]` (required if there is no embedding function; dimensions must match the stored vectors).
- `n_results` controls how many neighbors to return (default `10`).
- Returned fields: `ids`, `documents`, `distances`, `metadatas`, `embeddings`. **Chroma returns `distances`, not similarities — "lower distance = more similar."** (Mind this: it is the inverse of the cosine *similarity* from Project 02.)
- Filtering: `where` filters on metadata; `where_document` does full-text/regex filtering on the document. Filtering happens alongside the vector search (metadata pre/post-filtering).

### Persistence
- A `Client()` is in-memory (data lost on exit); a `PersistentClient(path=...)` writes the collection to disk so embeddings survive restarts. Build the index once, reuse it across runs — the "encode once, compare many" property from SBERT made operational.

## Relevant To

- concepts: [vector-database, approximate-nearest-neighbor, hnsw, retrieval, distance-vs-similarity, metadata-filtering]
- projects: [03-semantic-search, 04-pdf-research-assistant, 05-personal-memory-system]

## Notes

- **Distance vs. similarity is a classic bug source.** Project 02 ranked by cosine *similarity* (higher = closer). Chroma ranks by *distance* (lower = closer). With `space="cosine"`, Chroma's cosine distance ≈ `1 − cosine_similarity`. Mixing the two silently inverts rankings.
- **Approximate, not exact.** HNSW may miss a true nearest neighbor occasionally; for a small lab corpus the difference is invisible, but it is the price of scale. A brute-force cosine scan (Project 02) is the exact baseline to compare against.
- The default `space` is `l2`; for text embeddings you almost always want `space="cosine"` — a deliberate configuration choice, not a default.
