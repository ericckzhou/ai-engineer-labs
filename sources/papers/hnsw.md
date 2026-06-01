# HNSW: Efficient and Robust Approximate Nearest Neighbor Search using Hierarchical Navigable Small World Graphs

**Type:** paper
**Tier:** 2 (Foundational Paper)
**Author(s):** Yu. A. Malkov, D. A. Yashunin
**Date:** 2016 (submitted 2016-03-30; final revision 2018-08-14; published IEEE TPAMI 2020)
**URL:** https://arxiv.org/abs/1603.09320
**Accessed:** 2026-06-01

## Why This Source Matters

A vector database's speed is not magic — it is an algorithm. HNSW is the index that powers Chroma (and Qdrant, Weaviate, FAISS, pgvector, and most others). This paper is the primary source for *why* semantic search can rank a query against millions of vectors in milliseconds instead of doing a brute-force scan. It grounds the lesson's core scaling claim and the "approximate, not exact" tradeoff a learner must understand before trusting a vector DB's results.

## Key Claims

### The problem
- **Approximate K-nearest-neighbor (ANN) search**: find the vectors closest to a query without comparing against every stored vector. Exact (brute-force) search is `O(N)` per query — linear in corpus size — which becomes prohibitive at scale.

### What HNSW is
- A method that is "fully graph-based, without any need for additional search structures" — it builds proximity graphs and searches them, rather than partitioning space with trees.
- It constructs "a multi-layer structure consisting from hierarchical set of proximity graphs (layers) for nested subsets of the stored elements."

### How it works (intuition)
- Elements are assigned to layers "with an exponentially decaying probability distribution" — most elements live only in the bottom layer; few reach the top. This creates **scale separation**: upper layers have long-range links, lower layers short-range.
- Search starts at the top layer and **greedily routes** toward the query, descending layer by layer — like zooming in. The result is "graphs similar to the previously studied Navigable Small World (NSW) structures while additionally having the links separated by their characteristic distance scales."

### The payoff
- The structure "allows a logarithmic complexity scaling" of search — roughly `O(log N)` instead of `O(N)`.
- Empirically it "is able to strongly outperform previous opensource state-of-the-art vector-only approaches," making it the de facto standard ANN index.

## Relevant To

- concepts: [approximate-nearest-neighbor, hnsw, vector-database, retrieval, navigable-small-world, search-complexity]
- projects: [03-semantic-search, 04-pdf-research-assistant]

## Notes

- **Approximate is a feature, not a bug.** HNSW trades exact recall for `O(log N)` speed. Tunable knobs (`ef_search`, `ef_construction`, `M`/`max_neighbors`) move the recall-vs-speed/memory point. Higher `ef_search` → more candidates explored → higher recall, slower query.
- The exact baseline is the brute-force cosine scan from Project 02. Comparing HNSW results against that brute-force ranking on a small corpus is the way to *see* the approximation (and confirm it is near-perfect at small scale).
- This is why the vector DB matters: the database is essentially "an HNSW index + storage + a query API" around the embeddings Project 02 produced.
