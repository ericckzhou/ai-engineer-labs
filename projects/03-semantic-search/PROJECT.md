# Project 3: Semantic Search

## What We're Building

A semantic search engine over a text corpus. You'll embed documents, store them in a vector database, and retrieve the most semantically relevant results for a natural language query — without any keyword matching.

## Why We're Building It

Keyword search fails when users say "what did the CEO say about layoffs" and the document says "workforce reduction announcement." Semantic search finds meaning, not just words. This is the retrieval layer underneath every RAG system, recommendation engine, and AI-powered search product.

## Learning Objectives

- [ ] Build an embedding pipeline that converts documents to vectors
- [ ] Store and query vectors in a local vector database (ChromaDB)
- [ ] Implement cosine similarity retrieval and understand ranking
- [ ] Compare semantic search vs keyword search on real failure cases
- [ ] Design and evaluate a hybrid search strategy
- [ ] Understand indexing performance vs query performance tradeoffs
- [ ] Identify the top 5 failure modes of semantic search

## Key Concepts

Embedding pipeline, vector database, approximate nearest neighbor (ANN), cosine similarity, chunking strategy, metadata filtering, hybrid search, re-ranking

## Core Engineering Problem

**Problem:** Traditional search can't find "heart attack" when the query is "myocardial infarction." How do you search by meaning, not by keywords?

## Time Estimate

**Total:** 8–12 hours

## Startup Lens

Semantic search is infrastructure for search, recommendation, personalization, and support — all multi-billion dollar categories. The retrieval quality directly determines product quality.

## Key Files

```
code/
  embed_documents.py    — Embedding pipeline
  vector_store.py       — ChromaDB interface
  search.py             — Semantic query interface
  hybrid_search.py      — BM25 + semantic fusion
  evaluate_search.py    — Precision/recall evaluation
  requirements.txt
  README.md
```
