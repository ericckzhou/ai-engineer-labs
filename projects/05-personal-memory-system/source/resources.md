# Resources & Sources

> All sources used for this lesson, organized by tier.
> Every claim in lesson.agent.md traces back to one of these.

---

## Tier 1: Official Documentation

> Primary sources. Check these first.

- **scikit-learn — Cosine Similarity** — `sources/official-docs/scikit-learn-cosine-similarity.md` (carried from Project 02)
  - URL: https://scikit-learn.org/stable/modules/metrics.html#cosine-similarity
  - What to read: `x·y / (‖x‖‖y‖)`, cosine of the angle, magnitude-invariance, range `[−1, 1]`. This is the **relevance** signal.

- **Chroma (ChromaDB) documentation** — `sources/official-docs/chromadb.md` (carried from Project 03)
  - URL: https://docs.trychroma.com/
  - What to read: the collection → add → query loop. A real vector store for **persisting the memory stream** (extension).

---

## Tier 2: Foundational Papers

> Academic papers that established the concepts in this lesson.

- **Generative Agents** — `sources/papers/generative-agents.md`
  - Title: Generative Agents: Interactive Simulacra of Human Behavior
  - Authors: Park, O'Brien, Cai, Morris, Liang, Bernstein
  - Year: 2023
  - URL: https://arxiv.org/abs/2304.03442
  - Why it matters: the **memory stream** and the **retrieval score** — relevance + recency + importance,
    exponential recency decay (`0.995 ^ hours`), LLM-rated importance, and reflection. The architecture
    the whole project implements.

- **MemGPT** — `sources/papers/memgpt.md`
  - Title: MemGPT: Towards LLMs as Operating Systems
  - Authors: Packer, Wooders, Lin, Fang, Patil, Stoica, Gonzalez
  - Year: 2023
  - URL: https://arxiv.org/abs/2310.08560
  - Why it matters: the **memory hierarchy** — small in-prompt *main context* vs large out-of-prompt
    *external context* — and retrieval as **paging** under a context budget; self-editing memory via tools.

- **Memory Systems Taxonomy** — `sources/papers/memory-systems-taxonomy.md`
  - Title: Episodic and semantic memory (Tulving 1972, 1985); declarative/non-declarative (Squire)
  - URL: https://doi.org/10.1037/0003-066X.40.4.385 (Tulving 1985)
  - Why it matters: **episodic vs semantic vs procedural** memory — the cognitive foundation for tagging
    memories by `kind` and giving them different decay/retrieval treatment.

- **Sentence-BERT (SBERT)** — `sources/papers/sentence-bert.md` (carried from Projects 02–04)
  - URL: https://arxiv.org/abs/1908.10084
  - Why it matters: the bi-encoder embeddings behind the relevance signal; encode-once/compare-many.

---

## Tier 3: Engineering Guides

> Practical engineering perspectives.

- (None specific to this lesson. The Generative Agents and MemGPT papers are themselves the
  engineering blueprints; the Project 02–04 embedding/retrieval sources are the prerequisites.)

---

## Tier 4: Educational Sources

> Tutorials, courses, and explanatory content useful for learning.

- (None specific to this lesson. The Project 02–03 embedding/retrieval sources are the conceptual
  prerequisites.)

---

## Recommended Reading Order

For a learner new to this topic:

1. Start with: `sources/papers/generative-agents.md` — the memory stream and the three-signal retrieval
   score (this *is* the project).
2. Then read: `sources/papers/memgpt.md` — where memory lives (main vs external context) and why
   retrieval is a budgeted paging decision.
3. Then read: `sources/papers/memory-systems-taxonomy.md` — episodic vs semantic vs procedural, and why
   `kind` should change decay.
4. Reference: `sources/official-docs/scikit-learn-cosine-similarity.md` — the relevance math (Project 02).
5. Reference: `sources/official-docs/chromadb.md` — a real store for persisting the stream (Project 03).

---

## Further Reading

Topics adjacent to this lesson worth exploring later:

- Reflection / memory consolidation: synthesizing durable semantic knowledge from episodic streams
  (Generative Agents; bridge to Project 09).
- Self-editing memory as tool use: letting the model decide what to remember and when to retrieve
  (MemGPT; bridge to Project 08).
- Summarization-on-eviction and recursive context compression when even retrieval overflows the window.
- Persisting and isolating memory per user with a real vector DB (Chroma, Project 03) at scale.
