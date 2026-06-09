# Resources — Elective 05: Advanced RAG / Query Engineering

> Curated reading. Truth lives in `sources/`. Read in order.

## Read first — the transforms
1. **Query Rewriting (Rewrite-Retrieve-Read)** — `sources/papers/query-rewriting-rag.md` (Ma et al.
   2023). The question↔query gap; rewrite before retrieval.
2. **HyDE** — `sources/papers/hyde.md` (Gao et al. 2022). Embed a hypothetical *answer*; the dense
   bottleneck filters hallucinations; when it hurts.
3. **Self-RAG** — `sources/papers/self-rag.md` (Asai et al. 2023). Retrieve-or-not + relevance/
   support self-critique. The extension; the "sometimes don't retrieve" idea.

## Read second — the gate
4. **RAGAS** — `sources/papers/ragas.md`. Faithfulness + answer-relevance: the per-transform gate.
   Every transform must justify itself here.

## Carried from prior projects
- **Project 04** — `sources/papers/rag-paper.md`: the retrieve-then-read baseline being extended.
- **Project 03** — `sources/articles/sbert-retrieve-rerank.md`: re-ranking — **provided here** for
  fusion; do not rebuild it.
- **Project 02** — embeddings: HyDE embeds a generated document; same embedder both sides.

## How sources map to code
| Source | Code |
|--------|------|
| Rewrite-Retrieve-Read | `query_transforms.rewrite` (M1) |
| HyDE | `query_transforms.hyde` (M2) |
| (decomposition) | `query_transforms.decompose` (M3) |
| re-rank (P03) | fusion in `advanced_rag.answer` (provided `rerank`) |
| RAGAS | `evaluate_rag.py` (the per-transform gate) |
| Self-RAG | retrieve-or-not + critique extension |

## Out of scope (until the extensions)
- **Training a rewriter with RL** — the paper does; the core uses a prompted/canned rewriter.
- **Full Self-RAG reflection-token training** — approximated with prompting.
- **GraphRAG / hybrid BM25+dense** — extensions, not the core.
