# Source Map

Maps topics to source material by tier. Navigation only — truth lives in `sources/`.

## Format

```
## [Topic]
Tier 1 (Official Docs): sources/official-docs/...
Tier 2 (Papers): sources/papers/...
Tier 3 (Engineering Blogs): sources/articles/...
Tier 4 (Educational): sources/videos/... or books/...
```

---

## LLM APIs & Chat Completions

- Tier 1: `sources/official-docs/anthropic-messages-api.md` — Messages API: request/response, stateless multi-turn, stop reasons, token usage
- Tier 1: `sources/official-docs/anthropic-streaming.md` — Streaming (SSE) event protocol
- Tier 1: `sources/official-docs/litellm-completion.md` — Provider-agnostic `completion()` interface
- Tier 4: `sources/videos/hf-llm-course-intro.md` — NLP vs. LLM framing
- Tier 4: `sources/articles/mlabonne-llm-course.md` — "Running LLMs" as the foundational step

## Token Cost & Pricing

- Tier 1: `sources/official-docs/anthropic-pricing.md` — Per-MTok pricing, cost formula, token estimation, prompt caching

## Tokenization

- Tier 1: `sources/official-docs/tiktoken-bpe.md` — OpenAI's BPE tokenizer: encode/decode API, token counting, byte-level BPE, ~4 bytes/token
- Tier 1: `sources/official-docs/hf-tokenization-algorithms.md` — BPE/WordPiece/Unigram mechanics, word vs char vs subword tradeoff, worked BPE merge example

## Embeddings

- Tier 2: `sources/papers/word2vec.md` — Mikolov et al. 2013: continuous word vectors, CBOW/Skip-gram, "king − man + woman ≈ queen" vector arithmetic
- Tier 2: `sources/papers/sentence-bert.md` — Reimers & Gurevych 2019: sentence embeddings via siamese BERT, encode-once/compare-many, bi- vs cross-encoder

## Cosine Similarity & Vector Math

- Tier 1: `sources/official-docs/scikit-learn-cosine-similarity.md` — formula `x·y / (‖x‖‖y‖)`, cosine of the angle, magnitude-invariance, range [−1, 1]

## Vector Databases & Approximate Nearest Neighbor

- Tier 1: `sources/official-docs/chromadb.md` — Chroma vector DB: collections/documents/embeddings/metadata/ids, `collection.query()`, HNSW index, `space` = l2 (default)/cosine/ip, returns *distances* (lower = closer), `ef_search`/`ef_construction`/`max_neighbors`, persistent vs in-memory
- Tier 2: `sources/papers/hnsw.md` — Malkov & Yashunin 2016: hierarchical navigable small-world graphs, greedy multi-layer routing, ~O(log N) ANN search vs O(N) brute force, approximate-not-exact tradeoff

## Re-Ranking / Two-Stage Retrieval

- Tier 3: `sources/articles/sbert-retrieve-rerank.md` — retrieve with bi-encoder (fast, scalable) then re-rank top-k with cross-encoder (accurate); why cross-encoder alone can't scale

## RAG (Retrieval-Augmented Generation)

- Tier 2: `sources/papers/rag-paper.md` — Original RAG paper (to be added)

## Memory Systems

- Tier 2: `sources/papers/` — Memory architecture papers (to be added)

## Tool Use / Agents

- Tier 1: `sources/official-docs/anthropic-tool-use.md` — (to be added)
- Tier 2: `sources/papers/react-paper.md` — ReAct paper (to be added)

## Evaluation

- Tier 2: `sources/papers/` — RAGAS, MT-Bench (to be added)

---

*Entries marked "to be added" need to be created in `sources/` by the Researcher agent.*
