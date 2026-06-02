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

- Tier 2: `sources/papers/rag-paper.md` — Lewis et al. 2020: RAG = parametric (seq2seq weights) + non-parametric (dense vector index) memory; provenance + updatable knowledge; RAG-Sequence vs RAG-Token
- Tier 1: `sources/official-docs/anthropic-citations.md` — claim → source location (`char_location`/`page_location`/`content_block_location`), `cited_text`, sentence-level citation chunking, verifiable pointers

## Chunking

- Tier 3: `sources/articles/chunking-strategies.md` — Pinecone: chunk-size = precision vs context tradeoff, overlap, fixed-size (default) vs recursive vs semantic chunking, chunk expansion

## Memory Systems

- Tier 2: `sources/papers/generative-agents.md` — Park et al. 2023: memory stream; retrieval score = relevance (cosine) + recency (exponential decay `0.995^hours` from last access) + importance (LLM-rated 1–10); reflection
- Tier 2: `sources/papers/memgpt.md` — Packer et al. 2023: LLMs as operating systems; memory hierarchy (main vs external context), virtual context management, paging, self-editing memory via tools
- Tier 2: `sources/papers/memory-systems-taxonomy.md` — Tulving 1972/1985, Squire: episodic (events, dated) vs semantic (durable facts) vs procedural (skills); declarative vs non-declarative; kind-aware decay

## Tool Use / Agents

- Tier 1: `sources/official-docs/anthropic-tool-use.md` — Anthropic tool use: tool = name + description + JSON-schema input; model returns `stop_reason:"tool_use"` with `tool_use` blocks → execute → return `tool_result`; the agentic loop; `tool_choice` (auto/any/tool/none); tools as structured output
- Tier 1: `sources/articles/building-effective-agents.md` — Anthropic engineering: agent = "LLMs using tools based on environmental feedback in a loop"; workflows vs. agents; the augmented LLM (retrieval + tools + memory); the agent-computer interface (ACI)
- Tier 2: `sources/papers/react-paper.md` — Yao et al. 2022: ReAct — interleave reasoning traces and actions (Thought→Action→Observation); acting overcomes chain-of-thought hallucination; more interpretable trajectories

## Evaluation

- Tier 2: `sources/papers/ragas.md` — Es et al. 2023: reference-free RAG eval; faithfulness `F = |V|/|S|` (hallucination metric), answer relevance, context relevance
- Tier 2: `sources/papers/` — MT-Bench (to be added)

---

*Entries marked "to be added" need to be created in `sources/` by the Researcher agent.*
