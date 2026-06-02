# Memory Systems: Episodic, Semantic, and Procedural

**Type:** paper (cognitive-science foundation)
**Tier:** 2 (Foundational)
**Author(s):** Endel Tulving (episodic/semantic distinction); Larry R. Squire (declarative/non-declarative taxonomy)
**Date:** Tulving 1972, 1985; Squire 1992, 2004
**URL:** Tulving (1985), "How many memory systems are there?", *American Psychologist* 40(4):385–398 — https://doi.org/10.1037/0003-066X.40.4.385
**Accessed:** 2026-06-01

## Why This Source Matters

When an AI memory system stores "everything the user said" in one undifferentiated pile, retrieval gets worse, not better: a question about a *fact* ("what's my API key format?") and a question about an *event* ("what did we decide last Tuesday?") want different memories. Cognitive psychology drew these lines decades ago, and AI memory systems (Generative Agents, MemGPT, and production assistants) borrow the vocabulary directly. This source grounds Project 05's **memory types** — the distinction between remembering *events* (episodic), *facts* (semantic), and *skills* (procedural) — and why separating them improves both storage and retrieval. The names are not decoration: they determine *what you store*, *how it decays*, and *how you retrieve it*.

## Key Claims

### Episodic memory — events, time-stamped, autobiographical
- Tulving (1972) introduced **episodic memory**: memory for **specific personally-experienced events**, tied to a **time and place** ("what happened, when, where"). It is autobiographical and contextual: *"I told the assistant on Tuesday that I prefer dark mode."*
- Episodic memories are **dated** and **decay**: the value of a specific past interaction usually fades with time and is sharpened by recency of access. This is exactly what an exponential recency decay models.

### Semantic memory — general knowledge, decontextualized facts
- **Semantic memory** is "a mental thesaurus, organized knowledge a person possesses about words and other verbal symbols" — **general facts and concepts**, stripped of the episode in which they were learned. *"The user prefers dark mode"* (a standing fact) versus the dated episode of being told so.
- Semantic facts are **stable**: they should *not* decay the way a one-off event does. A good memory system **promotes** a repeated or important episodic observation into a durable semantic fact.

### Procedural memory — skills and how-to (non-declarative)
- Squire's taxonomy separates **declarative** memory (episodic + semantic — things you can *state*) from **non-declarative / procedural** memory: **skills, habits, and procedures** expressed through *performance*, not recall ("how to do something"). For an assistant, this maps to learned **workflows / standing instructions** ("how the user wants commits formatted", "the steps to deploy") — applied as behavior, not recited as a fact.

### Why the distinction matters for retrieval
- Different types want **different storage and decay policies**: episodic memories are time-keyed and decay; semantic facts are durable and should resist decay; procedural memories are applied as instructions. Tagging a memory with its **kind** lets the retriever and the decay function treat them appropriately rather than averaging everything together.

## Relevant To

- concepts: [episodic-memory, semantic-memory, procedural-memory, declarative-vs-nondeclarative, memory-types, memory-decay, fact-extraction]
- projects: [05-personal-memory-system, 09-personal-learning-os]

## Notes

- **The mapping to an AI assistant:**
  - *Episodic* → conversation turns / observations, with a timestamp. Decays (recency matters).
  - *Semantic* → extracted standing facts about the user/world. Durable (should resist decay).
  - *Procedural* → standing instructions / workflows. Applied as behavior.
- **Why not one flat store?** Mixing a dated trivial event with a permanent preference means recency decay either wrongly erases the preference or wrongly preserves the trivia. The `kind` tag lets decay and retrieval differ by type.
- **Episodic → semantic promotion** is the cognitively-motivated version of Generative Agents' *reflection* (`sources/papers/generative-agents.md`): repeated/important episodes get distilled into a durable fact. This is the Project 05 extension and the bridge to Project 09.
- These are decades-old, well-established constructs; the citation is the cognitive-science foundation, not an AI-systems claim. The AI-systems realization is in `generative-agents.md` and `memgpt.md`.
