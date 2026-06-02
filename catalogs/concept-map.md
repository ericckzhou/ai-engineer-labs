# Concept Map

Navigation index. Pointers only — no truth lives here.

For each concept: where to find the source, which lesson teaches it, and any known learner issues.

---

## How to Use This Catalog

When reasoning about a concept:
1. Look it up here to find authoritative sources
2. Navigate to `sources/` for truth
3. Navigate to `projects/*/source/lesson.agent.md` for how it's taught
4. Check `memory/learner/misconceptions/` for known pitfalls with this learner

---

## Concepts by Domain

### LLM Fundamentals

**Chat Completions API**
- Source: `sources/official-docs/anthropic-messages-api.md`
- Lesson: `projects/01-ai-chatbot/source/lesson.agent.md`
- Known issues: —

**Context Window**
- Source: `sources/official-docs/anthropic-messages-api.md`
- Lesson: `projects/01-ai-chatbot/source/lesson.agent.md`
- Known issues: —

**Tokenization**
- Source: `sources/official-docs/tiktoken-bpe.md`, `sources/official-docs/hf-tokenization-algorithms.md`
- Lesson: `projects/02-token-embedding-explorer/source/lesson.agent.md`
- Known issues: —

**Byte Pair Encoding (BPE)**
- Source: `sources/official-docs/hf-tokenization-algorithms.md` (mechanics), `sources/official-docs/tiktoken-bpe.md` (byte-level BPE)
- Lesson: `projects/02-token-embedding-explorer/source/lesson.agent.md`
- Known issues: —

**Temperature**
- Source: `sources/official-docs/anthropic-messages-api.md`
- Lesson: `projects/01-ai-chatbot/source/lesson.agent.md`
- Known issues: —

**Streaming**
- Source: `sources/official-docs/anthropic-streaming.md`
- Lesson: `projects/01-ai-chatbot/source/lesson.agent.md`
- Known issues: —

**Stateless Multi-Turn Conversation**
- Source: `sources/official-docs/anthropic-messages-api.md`
- Lesson: `projects/01-ai-chatbot/source/lesson.agent.md`
- Known issues: —

**System Prompt**
- Source: `sources/official-docs/anthropic-messages-api.md`
- Lesson: `projects/01-ai-chatbot/source/lesson.agent.md`
- Known issues: —

**Token Cost & Pricing**
- Source: `sources/official-docs/anthropic-pricing.md`
- Lesson: `projects/01-ai-chatbot/source/lesson.agent.md`
- Known issues: —

**Provider Abstraction (LiteLLM)**
- Source: `sources/official-docs/litellm-completion.md`
- Lesson: `projects/01-ai-chatbot/source/lesson.agent.md`
- Known issues: —

---

### Embeddings & Retrieval

**Embeddings**
- Source: `sources/papers/word2vec.md` (word embeddings), `sources/papers/sentence-bert.md` (sentence embeddings)
- Lesson: `projects/02-token-embedding-explorer/source/lesson.agent.md`
- Known issues: —

**Cosine Similarity**
- Source: `sources/official-docs/scikit-learn-cosine-similarity.md`
- Lesson: `projects/02-token-embedding-explorer/source/lesson.agent.md`
- Known issues: —

**Vector Databases**
- Source: `sources/official-docs/chromadb.md` (Chroma: collections, query API, HNSW index, distance vs similarity)
- Lesson: `projects/03-semantic-search/source/lesson.agent.md`
- Known issues: —

**Approximate Nearest Neighbor (ANN) / HNSW**
- Source: `sources/papers/hnsw.md` (Malkov & Yashunin 2016: hierarchical NSW graphs, ~O(log N) search)
- Lesson: `projects/03-semantic-search/source/lesson.agent.md`
- Known issues: —

**Re-Ranking (bi-encoder → cross-encoder)**
- Source: `sources/articles/sbert-retrieve-rerank.md`, `sources/papers/sentence-bert.md`
- Lesson: `projects/03-semantic-search/source/lesson.agent.md`
- Known issues: —

**Hybrid Search (BM25 + Semantic)**
- Source: `sources/articles/` (deferred — not yet sourced)
- Lesson: `projects/03-semantic-search/source/lesson.agent.md`
- Known issues: not yet covered; Chroma supports keyword/regex + dense, fold in if lesson scope grows

---

### RAG

**Retrieval-Augmented Generation (RAG)**
- Source: `sources/papers/rag-paper.md` (Lewis et al. 2020: parametric + non-parametric memory, provenance, updatable knowledge)
- Lesson: `projects/04-pdf-research-assistant/source/lesson.agent.md`
- Known issues: —

**Parametric vs. Non-Parametric Memory**
- Source: `sources/papers/rag-paper.md`
- Lesson: `projects/04-pdf-research-assistant/source/lesson.agent.md`
- Known issues: —

**Chunking Strategies**
- Source: `sources/articles/chunking-strategies.md` (Pinecone: size = precision/context tradeoff, overlap, fixed/recursive/semantic)
- Lesson: `projects/04-pdf-research-assistant/source/lesson.agent.md`
- Known issues: —

**Grounding / Refusal**
- Source: `sources/papers/rag-paper.md`, `sources/papers/ragas.md`
- Lesson: `projects/04-pdf-research-assistant/source/lesson.agent.md`
- Known issues: silent failure — model answers from parametric memory while ignoring context; detect via faithfulness

**Faithfulness / Hallucination Detection**
- Source: `sources/papers/ragas.md` (Es et al. 2023: `F = |V|/|S|`, answer relevance, context relevance; reference-free LLM-as-judge)
- Lesson: `projects/04-pdf-research-assistant/source/lesson.agent.md`
- Known issues: —

**Citations / Provenance**
- Source: `sources/official-docs/anthropic-citations.md` (claim → char/page/block location; `cited_text`; verifiable pointers)
- Lesson: `projects/04-pdf-research-assistant/source/lesson.agent.md`
- Known issues: incompatible with strict Structured Outputs (interleaved citation blocks)

---

### Memory

**Memory Stream**
- Source: `sources/papers/generative-agents.md` (Park et al. 2023: append-only list of memory objects with text, creation/last-accessed times, importance)
- Lesson: `projects/05-personal-memory-system/source/lesson.agent.md`
- Known issues: —

**Retrieval Scoring (relevance + recency + importance)**
- Source: `sources/papers/generative-agents.md` (`score = w_rel·rel + w_rec·rec + w_imp·imp`; min-max normalized, equal weights)
- Lesson: `projects/05-personal-memory-system/source/lesson.agent.md`
- Known issues: relevance-only retrieval is the silent failure — it's RAG over a chat log, not a memory system

**Memory Decay (exponential recency)**
- Source: `sources/papers/generative-agents.md` (`recency = decay_rate^hours`, decay_rate 0.995, measured from last access)
- Lesson: `projects/05-personal-memory-system/source/lesson.agent.md`
- Known issues: must touch `last_accessed` on retrieval, or recency degenerates to age-since-creation

**Episodic / Semantic / Procedural Memory**
- Source: `sources/papers/memory-systems-taxonomy.md` (Tulving 1972/1985; Squire — events vs facts vs skills; declarative vs non-declarative)
- Lesson: `projects/05-personal-memory-system/source/lesson.agent.md`
- Known issues: one flat decay policy wrongly erases durable semantic/procedural memories

**Memory Hierarchy (main vs external context)**
- Source: `sources/papers/memgpt.md` (Packer et al. 2023: OS-style paging; main context = prompt, external context = store; retrieval under a budget)
- Lesson: `projects/05-personal-memory-system/source/lesson.agent.md`
- Known issues: —

---

### Agents

**Tool Use / Function Calling**
- Source: `sources/official-docs/anthropic-tool-use.md` (tool = name + description + JSON-schema params; model emits a structured call → execute → feed `tool_result` back; `tool_choice` auto/any/tool/none)
- Lesson: `projects/06-ai-coding-copilot/source/lesson.agent.md`, `projects/08-ai-agent/source/lesson.agent.md`
- Known issues: LiteLLM/OpenAI shape carries `function.arguments` as a JSON **string** (must `json.loads`); raw Anthropic uses `tool_use`/`tool_result` blocks with `stop_reason:"tool_use"`

**ReAct Pattern**
- Source: `sources/papers/react-paper.md` (Yao et al. 2022: interleave Thought → Action → Observation; acting fetches ground truth → less hallucination than reasoning-only)
- Lesson: `projects/06-ai-coding-copilot/source/lesson.agent.md`, `projects/08-ai-agent/source/lesson.agent.md`
- Known issues: —

**Agent Loop (LLM + tools in a loop)**
- Source: `sources/articles/building-effective-agents.md` (Anthropic: agent = "LLMs using tools based on environmental feedback in a loop"; augmented LLM = retrieval + tools + memory)
- Lesson: `projects/06-ai-coding-copilot/source/lesson.agent.md`, `projects/08-ai-agent/source/lesson.agent.md`
- Known issues: loop must be bounded (`max_steps`) — the model drives control flow, so an unbounded loop is a runaway-cost risk

**Agent-Computer Interface (ACI) / Tool Schema Design**
- Source: `sources/articles/building-effective-agents.md` ("invest just as much effort in good agent-computer interfaces"; the model picks tools from the description alone — "the description is the API")
- Lesson: `projects/06-ai-coding-copilot/source/lesson.agent.md`
- Known issues: —

**Context Injection vs. Tool-Fetched Context**
- Source: `sources/papers/rag-paper.md`, `sources/articles/building-effective-agents.md` (retrieve obvious files up front vs. let the model pull what it needs mid-task)
- Lesson: `projects/06-ai-coding-copilot/source/lesson.agent.md`
- Known issues: —

**Tool Sandboxing (path containment)**
- Source: `sources/official-docs/anthropic-tool-use.md` (tool arguments are untrusted model input; resolve under a root and fail closed on escapes)
- Lesson: `projects/06-ai-coding-copilot/source/lesson.agent.md`
- Known issues: check containment **after** resolving — a raw `".." in path` string check is unsound (symlinks/absolute paths)

**Structured Output**
- Source: `sources/official-docs/anthropic-tool-use.md` (a `tool_use` block is schema-conforming → define a tool whose schema is the desired shape; `strict:true`)
- Lesson: `projects/06-ai-coding-copilot/source/lesson.agent.md`
- Known issues: —

---

### Evaluation

**LLM-as-Judge**
- Source: `sources/papers/` (MT-Bench, Chatbot Arena)
- Lesson: `projects/07-ai-evaluation-framework/source/lesson.agent.md`
- Known issues: —

**Faithfulness Metric**
- Source: `sources/papers/` (RAGAS)
- Lesson: `projects/07-ai-evaluation-framework/source/lesson.agent.md`
- Known issues: —

**Regression Testing for LLMs**
- Source: `sources/articles/`
- Lesson: `projects/07-ai-evaluation-framework/source/lesson.agent.md`
- Known issues: —

---

### System Design

**Query Routing**
- Source: `sources/articles/`
- Lesson: `projects/09-personal-learning-os/source/lesson.agent.md`
- Known issues: —

**Knowledge Graphs**
- Source: `sources/papers/`
- Lesson: `projects/09-personal-learning-os/source/lesson.agent.md`
- Known issues: —

---

## Adding a Concept

When a new concept is introduced in a lesson:

1. Add it here with its source, lesson link, and blank "Known issues"
2. Add the source to `sources/` in the correct tier directory
3. Update `catalogs/source-map.md`
