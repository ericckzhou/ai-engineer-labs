# Retrieve & Re-Rank (Sentence-Transformers)

**Type:** article (official library guide)
**Tier:** 3 (Engineering Guide)
**Author(s):** Nils Reimers / Sentence-Transformers (UKP Lab)
**Date:** accessed 2026-06-01
**URL:** https://www.sbert.net/examples/applications/retrieve_rerank/README.html
**Accessed:** 2026-06-01

## Why This Source Matters

`sentence-bert.md` introduces the bi-encoder vs. cross-encoder distinction in theory; this guide makes it an operational pattern. Project 03 builds first-stage retrieval (bi-encoder + vector DB). The natural next question — "the top result isn't always best; how do production systems fix that?" — is answered by **retrieve-then-rerank**. This source grounds the lesson's "production patterns" section and the optional re-ranking milestone.

## Key Claims

### Stage 1 — retrieve with a bi-encoder (fast)
- "The retriever has to be efficient for large document collections with millions of entries." A bi-encoder encodes query and documents **independently** into vectors, so retrieval is a fast vector similarity search (exactly the Project 02 / vector-DB path).

### Stage 2 — re-rank with a cross-encoder (accurate)
- A cross-encoder passes "the query and a possible document ... simultaneously to [a] transformer network, which then outputs a single score between 0 and 1." Attention runs *across* the query and document together, giving a more accurate relevance score than two independent embeddings compared by cosine.
- "The advantage of Cross-Encoders is the higher performance, as they perform attention across the query and the document."

### Why not cross-encoder alone
- "Scoring thousands or millions of (query, document)-pairs would be rather slow." A cross-encoder has no reusable per-item vector, so it cannot index a corpus — every query would require re-encoding against every document.

### The pipeline
- "We use the retriever to create a set of e.g. 100 possible candidates which are then re-ranked by the Cross-Encoder." Bi-encoder narrows millions → ~100 cheaply; cross-encoder reorders those ~100 precisely. Best of both: scalable *and* accurate.

## Relevant To

- concepts: [bi-encoder, cross-encoder, re-ranking, two-stage-retrieval, retrieval]
- projects: [03-semantic-search, 04-pdf-research-assistant, 07-ai-evaluation-framework]

## Notes

- The two-stage pattern is the standard production architecture for search/RAG: **retrieve broadly with the bi-encoder, re-rank narrowly with the cross-encoder.** It directly extends Project 03's single-stage retrieval.
- Trade-off framing: bi-encoder = cheap + approximate ordering; cross-encoder = expensive + sharp ordering. You apply the expensive model only to the small candidate set the cheap model already filtered. See `sources/papers/sentence-bert.md` for the underlying architecture and the 65h→5s efficiency argument.
