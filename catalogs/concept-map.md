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
- Source: `sources/official-docs/` (provider tokenizer docs)
- Lesson: `projects/02-token-embedding-explorer/source/lesson.agent.md`
- Known issues: —

**Temperature**
- Source: `sources/official-docs/`
- Lesson: `projects/01-ai-chatbot/source/lesson.agent.md`
- Known issues: —

**Streaming**
- Source: `sources/official-docs/`
- Lesson: `projects/01-ai-chatbot/source/lesson.agent.md`
- Known issues: —

---

### Embeddings & Retrieval

**Embeddings**
- Source: `sources/papers/` (word2vec, sentence-transformers)
- Lesson: `projects/02-token-embedding-explorer/source/lesson.agent.md`
- Known issues: —

**Cosine Similarity**
- Source: `sources/papers/`
- Lesson: `projects/02-token-embedding-explorer/source/lesson.agent.md`
- Known issues: —

**Vector Databases**
- Source: `sources/official-docs/` (ChromaDB, Qdrant docs)
- Lesson: `projects/03-semantic-search/source/lesson.agent.md`
- Known issues: —

**Approximate Nearest Neighbor (ANN)**
- Source: `sources/papers/`
- Lesson: `projects/03-semantic-search/source/lesson.agent.md`
- Known issues: —

**Hybrid Search (BM25 + Semantic)**
- Source: `sources/articles/`
- Lesson: `projects/03-semantic-search/source/lesson.agent.md`
- Known issues: —

---

### RAG

**Retrieval-Augmented Generation (RAG)**
- Source: `sources/papers/rag-paper.md`
- Lesson: `projects/04-pdf-research-assistant/source/lesson.agent.md`
- Known issues: —

**Chunking Strategies**
- Source: `sources/articles/`
- Lesson: `projects/04-pdf-research-assistant/source/lesson.agent.md`
- Known issues: —

**Faithfulness / Hallucination Detection**
- Source: `sources/papers/` (RAGAS, TruLens)
- Lesson: `projects/04-pdf-research-assistant/source/lesson.agent.md`
- Known issues: —

---

### Memory

**Episodic Memory**
- Source: `sources/papers/`
- Lesson: `projects/05-personal-memory-system/source/lesson.agent.md`
- Known issues: —

**Semantic Memory**
- Source: `sources/papers/`
- Lesson: `projects/05-personal-memory-system/source/lesson.agent.md`
- Known issues: —

**Procedural Memory**
- Source: `sources/papers/`
- Lesson: `projects/05-personal-memory-system/source/lesson.agent.md`
- Known issues: —

**Memory Decay**
- Source: `sources/papers/`
- Lesson: `projects/05-personal-memory-system/source/lesson.agent.md`
- Known issues: —

---

### Agents

**Tool Use / Function Calling**
- Source: `sources/official-docs/anthropic-tool-use.md`
- Lesson: `projects/06-ai-coding-copilot/source/lesson.agent.md`, `projects/08-ai-agent/source/lesson.agent.md`
- Known issues: —

**ReAct Pattern**
- Source: `sources/papers/react-paper.md`
- Lesson: `projects/08-ai-agent/source/lesson.agent.md`
- Known issues: —

**Agent Loops**
- Source: `sources/articles/`
- Lesson: `projects/08-ai-agent/source/lesson.agent.md`
- Known issues: —

**Structured Output**
- Source: `sources/official-docs/`
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
