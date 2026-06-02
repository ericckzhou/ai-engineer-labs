# Resources & Sources

> All sources used for this lesson, organized by tier.
> Every claim in lesson.agent.md traces back to one of these.

---

## Tier 1: Official Documentation

> Primary sources. Check these first.

- **Anthropic Citations (Messages API)** — `sources/official-docs/anthropic-citations.md`
  - URL: https://docs.anthropic.com/en/docs/build-with-claude/citations
  - What to read: how an answer span maps to a source location (`char_location`/`page_location`/`content_block_location`), `cited_text`, document chunking for citation granularity, why API citations beat prompt-asked quotes ("guaranteed to contain valid pointers").
  - Grounds: the citation/provenance section and the M4 citation milestone.

- **Chroma (ChromaDB) documentation** — `sources/official-docs/chromadb.md` (carried from Project 03)
  - URL: https://docs.trychroma.com/
  - What to read: the collection → add → query loop; `space="cosine"`; returned distances. This is the retrieval engine reused as RAG's "R".

---

## Tier 2: Foundational Papers

> Academic papers that established the concepts in this lesson.

- **RAG** — `sources/papers/rag-paper.md`
  - Title: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
  - Authors: Lewis, Perez, Piktus, Petroni, Karpukhin, Goyal, Küttler, M. Lewis, Yih, Rocktäschel, Riedel, Kiela
  - Year: 2020 (NeurIPS 2020)
  - URL: https://arxiv.org/abs/2005.11401
  - Why it matters: names and defines RAG — parametric + non-parametric memory, provenance, updatable knowledge. The architecture the whole project implements.

- **RAGAS** — `sources/papers/ragas.md`
  - Title: RAGAS: Automated Evaluation of Retrieval Augmented Generation
  - Authors: Es, James, Espinosa-Anke, Schockaert
  - Year: 2023
  - URL: https://arxiv.org/abs/2309.15217
  - Why it matters: defines **faithfulness** (`F = |V|/|S|`, the hallucination metric), answer relevance, and context relevance — reference-free, LLM-as-judge. Grounds the faithfulness/evaluation milestone.

- **Sentence-BERT (SBERT)** — `sources/papers/sentence-bert.md` (carried from Projects 02–03)
  - URL: https://arxiv.org/abs/1908.10084
  - Why it matters: the bi-encoder embeddings behind retrieval; encode-once/compare-many.

---

## Tier 3: Engineering Guides

> Practical engineering perspectives from teams who've shipped this in production.

- **Chunking Strategies for LLM Applications** — `sources/articles/chunking-strategies.md`
  - Authors: Roie Schwaber-Cohen, Arjun Patel (Pinecone), updated 2025-06-28
  - URL: https://www.pinecone.io/learn/chunking-strategies/
  - Key insight: chunk size is the precision-vs-context tradeoff; fixed-size with overlap is the default; recursive and semantic chunking are the next steps. Grounds the chunking milestone.

- **Retrieve & Re-Rank (Sentence-Transformers)** — `sources/articles/sbert-retrieve-rerank.md` (carried from Project 03)
  - URL: https://www.sbert.net/examples/applications/retrieve_rerank/README.html
  - Key insight: two-stage retrieve-then-rerank — relevant when first-stage retrieval into RAG isn't precise enough.

---

## Tier 4: Educational Sources

> Tutorials, courses, and explanatory content useful for learning.

- (None specific to this lesson. The Project 02–03 embedding/retrieval sources are the conceptual prerequisites.)

---

## Recommended Reading Order

For a learner new to this topic:

1. Start with: `sources/papers/rag-paper.md` — what RAG is and why (parametric vs non-parametric memory).
2. Then read: `sources/articles/chunking-strategies.md` — the upstream decision that caps RAG quality.
3. Then read: `sources/papers/ragas.md` — how to *measure* RAG (faithfulness = hallucination detection).
4. For depth: `sources/official-docs/anthropic-citations.md` — production-grade claim→source citations.
5. Reference: `sources/official-docs/chromadb.md` — the retrieval index (from Project 03).

---

## Further Reading

Topics adjacent to this lesson worth exploring later:

- Advanced chunking (semantic, late chunking, hierarchical / parent-document retrieval).
- Hybrid retrieval (dense + BM25) and re-ranking before generation (`sources/articles/sbert-retrieve-rerank.md`).
- RAG evaluation at scale: full RAGAS suite, faithfulness drift monitoring in production (Project 07).
- Prompt caching the document context to cut cost on repeated queries over the same PDF.
