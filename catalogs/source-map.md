# Source Map

Maps topics to source material by tier. Navigation only — truth lives in `sources/`.

Rendered HTML for humans is generated at `catalogs/rendered/source-map.html` by
`scripts/render_sources.py`. This Markdown file remains canonical.

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

## Advanced RAG / Query Engineering (Elective 05 — Production & Hardening track)

> Extending P04's naive retrieve-then-read with a query-transformation stage — measured against
> P04's faithfulness eval. Source base for `projects/electives/05-advanced-rag-query-engineering/`.

- Tier 2: `sources/papers/query-rewriting-rag.md` — Ma et al. 2023 (EMNLP): Rewrite-Retrieve-Read; the question↔query gap; reformulate the query BEFORE retrieval (LLM rewriter or RL-trained small LM from reader feedback)
- Tier 2: `sources/papers/hyde.md` — Gao et al. 2022: Hypothetical Document Embeddings; generate a hypothetical answer, embed THAT (not the query); the dense bottleneck filters hallucinations; zero-shot
- Tier 2: `sources/papers/self-rag.md` — Asai et al. 2023: adaptive retrieve-or-NOT + self-critique (relevance + support) via reflection tokens; the advanced move is sometimes not retrieving, always critiquing what you retrieved
- Tier 2: `sources/papers/ragas.md` — the faithfulness/answer-relevance gate (already in repo) every transform is measured against
- Tier 3: `sources/articles/sbert-retrieve-rerank.md` — re-ranking (already learned in P03; PROVIDED here, not the target)

## Chunking

- Tier 3: `sources/articles/chunking-strategies.md` — Pinecone: chunk-size = precision vs context tradeoff, overlap, fixed-size (default) vs recursive vs semantic chunking, chunk expansion

## Memory Systems

- Tier 2: `sources/papers/generative-agents.md` — Park et al. 2023: memory stream; retrieval score = relevance (cosine) + recency (exponential decay `0.995^hours` from last access) + importance (LLM-rated 1–10); reflection
- Tier 2: `sources/papers/memgpt.md` — Packer et al. 2023: LLMs as operating systems; memory hierarchy (main vs external context), virtual context management, paging, self-editing memory via tools
- Tier 2: `sources/papers/memory-systems-taxonomy.md` — Tulving 1972/1985, Squire: episodic (events, dated) vs semantic (durable facts) vs procedural (skills); declarative vs non-declarative; kind-aware decay

## Tool Use / Agents

- Tier 1: `sources/official-docs/anthropic-tool-use.md` — Anthropic tool use: tool = name + description + JSON-schema input; model returns `stop_reason:"tool_use"` with `tool_use` blocks → execute → return `tool_result`; the agentic loop; `tool_choice` (auto/any/tool/none); tools as structured output
- Tier 1: `sources/articles/building-effective-agents.md` — Anthropic engineering: agent = "LLMs using tools based on environmental feedback in a loop"; workflows vs. agents; the augmented LLM (retrieval + tools + memory); the agent-computer interface (ACI)
- Tier 2: `sources/papers/react-paper.md` — Yao et al. 2022: ReAct — interleave reasoning traces and actions (Thought→Action→Observation); acting overcomes chain-of-thought hallucination; more interpretable trajectories; "reasoning traces help the model … handle exceptions" (the basis for tool-error recovery in P08)

## Agent Reliability (Project 08)

> Making an autonomous loop safe to leave running. Same agent sources as above, emphasis shifted to *when* to use an agent and *how* to bound it. No new sources — these carry over.

- Tier 1: `sources/articles/building-effective-agents.md` — workflows vs. agents; "the most successful implementations use simple, composable patterns"; "add complexity only when it demonstrably improves outcomes" (when *not* to use an agent); orchestrator-workers, evaluator-optimizer patterns
- Tier 1: `sources/official-docs/anthropic-pricing.md` — per-MTok pricing for a real cost budget (don't invent token prices)
- Tier 2: `sources/papers/mt-bench.md` — evaluating with numbers, applied to *runs* (completion + efficiency), not single answers
- Tier 2: `sources/papers/generative-agents.md` — reflection (synthesize a higher-level judgment from raw steps) for the optional reflection/evaluator-optimizer loop

## Evaluation

- Tier 2: `sources/papers/ragas.md` — Es et al. 2023: reference-free RAG eval; faithfulness `F = |V|/|S|` (hallucination metric), answer relevance, context relevance
- Tier 2: `sources/papers/mt-bench.md` — Zheng et al. 2023: LLM-as-a-judge — ~80% human agreement; biases (position/verbosity/self-enhancement); mitigations (reasoning-before-score, reference-guided, position-swap); MT-Bench + Chatbot Arena

## System Design / Orchestration (Project 09 — capstone)

> Composing the prior subsystems into one system. No new sources — these carry over, with the emphasis on *routing*, *orchestration*, *provenance*, and *system-level evaluation*.

- Tier 1: `sources/articles/building-effective-agents.md` — the **augmented LLM** (retrieval + tools + memory) as the building block; **routing** ("classifies an input and directs it to a specialized followup task"; "separation of concerns"); **orchestrator-workers** ("dynamically breaks down tasks, delegates … and synthesizes their results"); "add complexity only when it demonstrably improves outcomes" as a *routing* rule
- Tier 1: `sources/official-docs/anthropic-citations.md` — claim → source location; the production form of the provenance the orchestrator returns (carried from Project 04)
- Tier 2: `sources/papers/rag-paper.md` — provenance: an answer should carry a verifiable pointer to what produced it (applied to the orchestrator's `Response`)
- Tier 2: `sources/papers/generative-agents.md` — reflection (linking memories into higher-level structure): the conceptual basis for linking memories into higher-order concepts
- Tier 2: `sources/papers/knowledge-graphs-survey.md` — knowledge graphs as graph-shaped representations of entities and relationships; grounds the lightweight personal graph concept without claiming a full KG implementation
- Tier 2: `sources/papers/mt-bench.md` — evaluate with numbers, **per case** — applied to the router (per-route accuracy, not just an overall mean)

## Model Context Protocol (MCP)

> Protocol surface for provider/consumer decoupling. The source base for the **MCP Interface Layer elective** (`projects/electives/01-mcp-interface-layer/`) and for comparing hand-wired tools (Projects 06/08/09) with reusable protocol-exposed capabilities.

- Tier 1: `sources/official-docs/mcp-architecture.md` — client-host-server architecture, JSON-RPC, stateful sessions, capability negotiation, composable isolated servers
- Tier 1: `sources/official-docs/mcp-tools.md` — tool discovery/calling, `inputSchema`, optional `outputSchema`, structured results, protocol vs execution errors, tool security
- Tier 1: `sources/official-docs/mcp-resources.md` — resource URIs, application-controlled context data, listing/reading resources, memory/corpus/resource surfaces
- Tier 1: `sources/official-docs/mcp-prompts.md` — reusable prompt templates with arguments, host/user-selected prompts
- Tier 1: `sources/official-docs/mcp-transports.md` — data layer vs transport layer, stdio vs Streamable HTTP, local vs remote operational constraints
- Tier 1: `sources/official-docs/mcp-security-best-practices.md` — local server execution risk, consent, sandboxing, least privilege, token/session risks
- Tier 1: `sources/official-docs/mcp-build-server.md` — practical server scaffolding, FastMCP, stdio logging caveat, host configuration

## Guardrails & Safety (Elective 02 — Production & Hardening track)

> Hardening an existing capability (P08 agent / P04 RAG) against untrusted input: prompt-injection
> detection, PII/sensitive-info redaction, and fail-closed output policy. The source base for
> `projects/electives/02-guardrails-safety-layer/`.

- Tier 1: `sources/official-docs/owasp-llm-top10-2025.md` — OWASP Top 10 for LLMs (2025): LLM01 Prompt Injection (direct vs indirect; system-prompt defenses are bypassable), LLM02 Sensitive Information Disclosure (automated detection + redaction of PII)
- Tier 1: `sources/official-docs/presidio-pii.md` — Microsoft Presidio: two-stage PII de-identification (Analyzer = regex/NER/context/checksum recognizers → Anonymizer = replace/mask/redact/hash/encrypt); "no guarantee it finds all" — risk reduction, not a fix
- Tier 2: `sources/papers/llama-guard.md` — Inan et al. 2023: LLM-as-classifier guard; separate prompt vs response classification; taxonomy-as-prompt; structured verdict (binary + violated categories), not a bare bool
- Tier 2: `sources/papers/indirect-prompt-injection.md` — Greshake et al. 2023: indirect prompt injection — hidden instructions ride in on *retrieved* content (data/instruction boundary collapse); scanning only user input is insufficient; robust mitigations are lacking (defense in depth)

## Cost & Latency (Elective 03 — Production & Hardening track)

> Cutting cost/latency of a working feature WITHOUT regressing quality, gated by the Project 07
> eval. The source base for `projects/electives/03-cost-latency-engineering/`.

- Tier 1: `sources/official-docs/anthropic-prompt-caching.md` — cache a stable prompt prefix; cache-write (~1.25×/2×) vs cache-read (~0.1×) vs base input; 5-min/1-hour TTL; stable-prefix-before-variable rule; verify via `usage.cache_read_input_tokens`
- Tier 1: `sources/official-docs/gptcache-semantic-caching.md` — semantic (embedding-similarity) cache vs exact-match; embed → ANN search → threshold = hit; too-loose threshold returns a wrong cached answer (the false hit); LRU/FIFO/LFU eviction
- Tier 1: `sources/official-docs/anthropic-pricing.md` — the per-MTok base prices all multipliers/savings apply to (don't invent prices)
- Tier 2: `sources/papers/frugalgpt.md` — Chen/Zaharia/Zou 2023: prompt adaptation, LLM approximation, LLM cascade (cheap model first → escalate on low reliability score); ~98% cost cut matching GPT-4; the escalation signal is the hard design choice

## AI Observability & Ops (Elective 04 — Production & Hardening track)

> Instrumenting an agent with standard GenAI telemetry, then monitoring live traces for
> drift/regression — closing P07's offline→online loop. Source base for
> `projects/electives/04-llm-observability-ops/`.

- Tier 1: `sources/official-docs/opentelemetry-genai-semconv.md` — standard GenAI telemetry vocabulary (`gen_ai.operation.name`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`/`output_tokens`, `gen_ai.response.finish_reasons`); standardized attribute names so tools agree; observability is separate from but supports evaluation
- Tier 3: `sources/articles/llm-online-evaluation-drift.md` — online eval vs offline; sample ~5–10% of traffic with an ASYNC LLM-judge (never synchronous on the path); operational/behavioral/distributional drift; aggregate **per route**, not a global mean
- Tier 2: `sources/papers/mt-bench.md` — score with numbers, now applied to a live window per route (not a single answer)

## Agent Self-Improvement Patterns

> Optional extensions for Project 08. These are architecture comparisons, not required base-agent behavior.

- Tier 2: `sources/papers/reflexion.md` — verbal reflection from feedback stored in memory for future attempts
- Tier 2: `sources/papers/self-refine.md` — generate, critique, revise loop without weight updates
- Tier 2: `sources/papers/tree-of-thoughts.md` — search over multiple reasoning paths with generation, evaluation, selection, and backtracking
- Tier 2: `sources/papers/rewoo.md` — plan first, execute tool calls, then solve; efficiency tradeoff versus adaptive ReAct loops

## Knowledge Graphs

- Tier 2: `sources/papers/knowledge-graphs-survey.md` — graph-shaped representation of entities and relationships; grounds Project 09's lightweight personal knowledge graph concept
