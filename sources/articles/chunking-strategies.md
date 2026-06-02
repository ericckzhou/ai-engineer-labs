# Chunking Strategies for LLM Applications

**Type:** article (engineering guide)
**Tier:** 3 (Engineering Guide)
**Author(s):** Roie Schwaber-Cohen, Arjun Patel (Pinecone)
**Date:** updated 2025-06-28
**URL:** https://www.pinecone.io/learn/chunking-strategies/
**Accessed:** 2026-06-01

## Why This Source Matters

Chunking is the decision that most quietly determines RAG quality, and it is the one beginners skip. You cannot embed a whole PDF as one vector — embedding models have a context window, and a single vector for a long document is too diffuse to match a specific question. So you split the document into chunks first, and *how* you split it changes what retrieval can find. This guide is the practical primary source for the chunk-size tradeoff at the center of Project 04's chunking milestone, and for why "fixed-size with overlap" is the sane default.

## Key Claims

### Why chunk at all
- Two functions: keep input within the embedding model's context window, and keep each chunk focused enough to match a query. "Exceeding this context window may mean[] the excess tokens are truncated, or thrown away, before being processed into a vector."
- In RAG, "chunks returned from searches over databases consume context during a session, and ground the agent's responses." Bad chunks → "agents may generate hallucinations or invoke incorrect tools."

### The core tradeoff: short vs. long chunks (precision vs. context)
- **Short (sentence-level)** embeddings are "focused on specific meaning," good for precise matching — but a single sentence may lack the surrounding context needed to answer.
- **Long (paragraph/document-level)** embeddings give "a more comprehensive vector representation that captures the broader meaning and themes of the text" — but larger chunks "introduce noise and dilute significance of individual elements," making "finding precise matches when querying the index more difficult."
- This is the central design decision: too small loses context, too large loses precision.

### Fixed-size chunking (the default)
- "Fixed-sized chunking will be the best path in most cases, and we recommend starting here and iterating only after determining it insufficient." Split every N tokens/characters; simple and cheap.

### Chunk overlap
- Adjacent fixed-size chunks should overlap so a sentence split across a boundary is not lost from both chunks. Overlap preserves continuity across the cut points.

### Recursive / content-aware chunking
- LangChain's `RecursiveCharacterTextSplitter` is "a great middle ground between always splitting on a specific character and using a more semantic splitter." It splits on a priority list of separators (paragraph → line → sentence → word) so chunks respect natural boundaries where possible.

### Semantic chunking
- An emerging technique that uses embeddings to find topic boundaries: embed groups of sentences and "compare the semantic distance between each group and its predecessor" — split where meaning shifts.

### Chunk expansion (post-processing)
- You are not locked into the initial split: "chunk expansion [works] by retrieving neighboring chunks within a window for each chunk in a retrieved set" — retrieve small (precise), then widen to neighbors for context at answer time.

### Align chunking with the embedding model
- "After choosing an appropriate model for your domain, be sure to adapt your chunking strategy to align with expected document types the model has been trained on."

## Relevant To

- concepts: [chunking, fixed-size-chunking, recursive-chunking, semantic-chunking, chunk-overlap, chunk-expansion, context-vs-precision, document-parsing]
- projects: [04-pdf-research-assistant, 05-personal-memory-system]

## Notes

- **The practical default for Project 04:** fixed-size chunks (e.g. ~500 tokens) with ~10–20% overlap, then iterate. Start simple; only reach for recursive/semantic chunking if retrieval quality demands it.
- **Chunking is upstream of everything.** Bad chunks cap the ceiling: retrieval can only return chunks you created, and the generator can only ground in what retrieval returns. A faithfulness or context-relevance problem (`sources/papers/ragas.md`) is often really a chunking problem.
- Chunk size interacts with embedding dimensionality and the model's training (`sources/papers/sentence-bert.md`): a sentence-trained encoder degrades on whole-page chunks.
