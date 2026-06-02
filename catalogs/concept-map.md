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

**Workflow vs. Agent**
- Source: `sources/articles/building-effective-agents.md` (workflow = LLMs/tools on "predefined code paths"; agent = the LLM "dynamically direct[s] [its] own processes and tool usage")
- Lesson: `projects/08-ai-agent/source/lesson.agent.md`
- Known issues: the agent is the highest-capability *and* highest-blast-radius pattern — reach for it last; "add complexity only when it demonstrably improves outcomes"

**Loop / Stuck Detection**
- Source: `sources/papers/react-paper.md` (a reasoning step lets the loop decide it's done instead of thrashing; the no-progress failure)
- Lesson: `projects/08-ai-agent/source/lesson.agent.md`
- Known issues: compare the *whole* action (tool **and** arguments), not just the tool name — else a productive multi-file read is wrongly killed as "stuck"

**Agent Budget / Resource Management (steps + tokens + cost)**
- Source: `sources/official-docs/anthropic-tool-use.md` (the loop must be bounded), `sources/official-docs/anthropic-pricing.md` (per-MTok cost)
- Lesson: `projects/08-ai-agent/source/lesson.agent.md`
- Known issues: a `max_steps` cap misses a few huge steps — track tokens too; don't invent token prices for the cost ceiling

**Tool-Error Recovery**
- Source: `sources/papers/react-paper.md` ("reasoning traces help the model … handle exceptions" — feed the error back as an observation)
- Lesson: `projects/08-ai-agent/source/lesson.agent.md`
- Known issues: `except: pass` is worse than crashing — the model never sees the error and repeats it (→ stuck); the error must become an observation

**Agent Evaluation (run-level: completion + efficiency + cost)**
- Source: `sources/papers/mt-bench.md` (score with numbers — applied to a *run*, not a single answer)
- Lesson: `projects/08-ai-agent/source/lesson.agent.md`
- Known issues: a bare "did it answer?" bool hides a low-efficiency (wandering) run; key completion off the `stop_reason` AND the expected outcome

---

**Reflexion**
- Source: `sources/papers/reflexion.md` (verbal feedback converted into a reflection memory for future attempts)
- Lesson: optional extension for `projects/08-ai-agent/source/lesson.agent.md`
- Known issues: reflection quality depends on feedback quality; not a guarantee of autonomous learning

**Self-Refine**
- Source: `sources/papers/self-refine.md` (generate, feedback, revise loop using an LLM)
- Lesson: optional extension for `projects/07-ai-evaluation-framework/source/lesson.agent.md`, `projects/08-ai-agent/source/lesson.agent.md`
- Known issues: self-feedback can become vague or self-confirming without external tests

**Tree of Thoughts**
- Source: `sources/papers/tree-of-thoughts.md` (search over multiple reasoning paths with evaluation and backtracking)
- Lesson: optional extension for `projects/08-ai-agent/source/lesson.agent.md`
- Known issues: costs more inference and orchestration; reserve for tasks where search matters

**ReWOO / Plan-Execute**
- Source: `sources/papers/rewoo.md` (decouple planning from observation-heavy tool execution)
- Lesson: optional extension for `projects/08-ai-agent/source/lesson.agent.md`
- Known issues: a bad initial plan needs replanning; efficiency trades off against ReAct-style adaptability

---

### Model Context Protocol

**MCP Provider/Consumer Split**
- Source: `sources/official-docs/mcp-architecture.md`
- Lesson: `projects/electives/01-mcp-interface-layer/source/lesson.agent.md`; related to `projects/06-ai-coding-copilot/source/lesson.agent.md`, `projects/08-ai-agent/source/lesson.agent.md`, `projects/09-personal-learning-os/source/lesson.agent.md`
- Known issues: MCP is an interface protocol, not another agent loop

**MCP Tools**
- Source: `sources/official-docs/mcp-tools.md`
- Lesson: `projects/electives/01-mcp-interface-layer/source/lesson.agent.md`
- Known issues: tool schemas cross a trust boundary; validate inputs and distinguish protocol errors from tool execution errors

**MCP Resources**
- Source: `sources/official-docs/mcp-resources.md`
- Lesson: `projects/electives/01-mcp-interface-layer/source/lesson.agent.md`
- Known issues: resources are context data, not actions; hosts decide how to include them

**MCP Prompts**
- Source: `sources/official-docs/mcp-prompts.md`
- Lesson: `projects/electives/01-mcp-interface-layer/source/lesson.agent.md`
- Known issues: prompts are reusable templates exposed by a server, not private app strings

**MCP Transports**
- Source: `sources/official-docs/mcp-transports.md`
- Lesson: `projects/electives/01-mcp-interface-layer/source/lesson.agent.md`
- Known issues: stdio logging to stdout can corrupt protocol messages; remote HTTP needs stronger auth

**MCP Security**
- Source: `sources/official-docs/mcp-security-best-practices.md`
- Lesson: `projects/electives/01-mcp-interface-layer/source/lesson.agent.md`; related to Project 06 sandboxing
- Known issues: local servers run with host privileges unless sandboxed; use least privilege and explicit consent

---

### Evaluation

**LLM-as-Judge**
- Source: `sources/papers/mt-bench.md` (Zheng et al. 2023: strong LLM judge ~80% human agreement; single-answer grading vs pairwise; reasoning-before-score / reference-guided mitigations)
- Lesson: `projects/07-ai-evaluation-framework/source/lesson.agent.md`
- Known issues: judge biases — position, verbosity, self-enhancement, weak math grading; judge is not ground truth (spot-check the ~20%)

**Judge Biases (position / verbosity / self-enhancement)**
- Source: `sources/papers/mt-bench.md` (named failure modes of an LLM judge + mitigations: position-swap, watch length, different judge model)
- Lesson: `projects/07-ai-evaluation-framework/source/lesson.agent.md`
- Known issues: verbosity bias makes a wordier-but-not-better answer score higher — a metric trap

**Faithfulness Metric**
- Source: `sources/papers/ragas.md` (reference-free; `F = |V|/|S|` — supported claims / total claims; the hallucination metric)
- Lesson: `projects/07-ai-evaluation-framework/source/lesson.agent.md`, `projects/04-pdf-research-assistant/source/lesson.agent.md`
- Known issues: —

**Score Aggregation & Pass-Rate**
- Source: `sources/papers/mt-bench.md` (turning per-case scores into a ship/no-ship decision)
- Lesson: `projects/07-ai-evaluation-framework/source/lesson.agent.md`
- Known issues: a flat mean can hide a per-case regression — compare per case

**Regression Testing for LLMs**
- Source: `sources/papers/mt-bench.md` (engineering application: freeze a dataset, score baseline vs candidate, flag per-case drops)
- Lesson: `projects/07-ai-evaluation-framework/source/lesson.agent.md`
- Known issues: dataset must be frozen between runs; `temperature=0` judge or the gate is flaky

---

**Agent Observability / GenAI Telemetry**
- Source: `sources/official-docs/opentelemetry-genai-semconv.md` (standard GenAI telemetry attributes and spans)
- Lesson: `projects/07-ai-evaluation-framework/source/lesson.agent.md`, `projects/08-ai-agent/source/lesson.agent.md`, `projects/09-personal-learning-os/source/lesson.agent.md`
- Known issues: observability records what happened; evaluation decides whether it was good

---

### System Design (Project 09 — capstone)

**Augmented LLM as a System**
- Source: `sources/articles/building-effective-agents.md` (the building block: an LLM "enhanced with augmentations such as retrieval, tools, and memory")
- Lesson: `projects/09-personal-learning-os/source/lesson.agent.md`
- Known issues: the capstone is composition, not a ninth capability — the subsystems (P01/P03/P05/P08) are provided

**Query Routing**
- Source: `sources/articles/building-effective-agents.md` (routing: "classifies an input and directs it to a specialized followup task"; "separation of concerns"; routing can be an LLM or a traditional classifier)
- Lesson: `projects/09-personal-learning-os/source/lesson.agent.md`
- Known issues: precedence is a *correctness* decision (check `SAVE` before `CHAT`) and the safe default must be the cheapest, non-destructive route (`CHAT`, never `TASK`/`SAVE`); a mis-ordered router silently drops a "remember this"

**Orchestrator-Workers (Orchestration)**
- Source: `sources/articles/building-effective-agents.md` (a central LLM "dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results")
- Lesson: `projects/09-personal-learning-os/source/lesson.agent.md`
- Known issues: the orchestrator must dispatch to exactly one subsystem and only synthesize — if `handle` retrieves/saves itself it has taken on a worker's job (loses separation of concerns)

**Provenance (orchestrated answers)**
- Source: `sources/papers/rag-paper.md` (verifiable pointer to what produced the answer), `sources/official-docs/anthropic-citations.md` (claim → source location)
- Lesson: `projects/09-personal-learning-os/source/lesson.agent.md`, `projects/04-pdf-research-assistant/source/lesson.agent.md`
- Known issues: provenance must be *returned* in the `Response`, not printed — a printed trail is invisible to callers, tests, and the evaluator

**Knowledge Graphs (personal, tag-linked)**
- Source: `sources/papers/knowledge-graphs-survey.md` (graph-shaped representation of entities and relationships), `sources/papers/generative-agents.md` (reflection as a memory-linking behavior)
- Lesson: `projects/09-personal-learning-os/source/lesson.agent.md`
- Known issues: Project 09 is a lightweight tag-linked personal graph, not a full ontology/RDF/SPARQL system; link **incrementally** (not O(N²) full-rebuild), keep edges **symmetric**, and never link a node to itself

**System-Level Evaluation (per-route routing accuracy)**
- Source: `sources/papers/mt-bench.md` (score with numbers, **per case** — applied to the router, not a single answer)
- Lesson: `projects/09-personal-learning-os/source/lesson.agent.md`
- Known issues: an overall accuracy mean hides a route that is silently 0% — report per-route accuracy + the misroute list on a frozen labeled set

---

## Adding a Concept

When a new concept is introduced in a lesson:

1. Add it here with its source, lesson link, and blank "Known issues"
2. Add the source to `sources/` in the correct tier directory
3. Update `catalogs/source-map.md`
