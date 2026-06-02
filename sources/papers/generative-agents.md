# Generative Agents: Interactive Simulacra of Human Behavior

**Type:** paper
**Tier:** 2 (Foundational Paper)
**Author(s):** Joon Sung Park, Joseph C. O'Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, Michael S. Bernstein
**Date:** 2023 (submitted 2023-04-07)
**URL:** https://arxiv.org/abs/2304.03442
**Accessed:** 2026-06-01

## Why This Source Matters

This is the primary source for **memory retrieval scoring** — the central learning target of Project 05. An LLM is stateless: every turn starts from zero. To make an agent that *remembers*, you need a store of past observations and a principled way to decide **which** memories to pull back into the limited context window for the current moment. Generative Agents answers that with a **memory stream** and a **retrieval function that combines three signals — relevance, recency, and importance — into a single score.** This is the architecture Project 05 implements directly: it grounds the scoring formula, the exponential recency decay, the LLM-rated importance, and the idea of *reflection* (synthesizing higher-level memories from raw ones).

## Key Claims

### The memory stream
- The agent's memory is "a long-term memory module that records, in natural language, a comprehensive list of the agent's experiences" — the **memory stream**. Each entry is a **memory object** with a natural-language description, a **creation timestamp**, and a **most-recent-access timestamp**.
- The store grows without bound, so the whole stream cannot fit in the model's context window. "The most important challenge is to retrieve [the] relevant ... most pertinent" subset for the current situation. Retrieval is the core problem, not storage.

### Retrieval = relevance + recency + importance
The retrieval function scores every memory against the agent's current situation (the query) on three components, each normalized to `[0, 1]` via min-max scaling, then summed:

- **Relevance** — semantic similarity between the memory and the current query: "the cosine similarity between the memory's embedding vector and the query memory's embedding vector." (This is the Project 02–04 embedding machinery.)
- **Recency** — "assigns a higher score to memory objects that were recently accessed ... we treat recency as an **exponential decay function** over the number of hours since the memory was last retrieved. Our decay factor is **0.995**." So `recency = decay_factor ^ (hours since last access)`; a just-accessed memory scores 1.0 and the score decays toward 0 as it ages.
- **Importance** — "distinguishes mundane from core memories" by asking the language model to rate the memory's poignancy on an **integer scale of 1 to 10** (1 = "brushing teeth", 10 = "a breakup"). This score is assigned **once, at creation**, and stored.

**Final score:** `score = α_relevance · relevance + α_recency · recency + α_importance · importance`. "In our implementation, all α's are set to 1." The top-ranked memories that fit in the context window are retrieved.

### Retrieval refreshes recency
- Recency is measured from the **last access**, not creation — so retrieving a memory updates its most-recent-access timestamp, making frequently-used memories "warm" and rarely-used ones decay. This feedback loop is what makes recency meaningful.

### Reflection — higher-level memories
- Periodically the agent **reflects**: it synthesizes "more abstract, higher-level" memories from recent observations. Reflections are themselves written back into the stream as memory objects (and can cite the observations they were drawn from), so they get retrieved like any other memory. Trigger: when the sum of importance scores of recent events crosses a threshold.

## Relevant To

- concepts: [memory-stream, retrieval-scoring, recency-decay, importance-salience, relevance-cosine, episodic-memory, reflection, stateful-agents]
- projects: [05-personal-memory-system, 08-ai-agent]

## Notes

- **The three-signal score is the whole lesson.** Relevance alone retrieves the semantically-closest memory even if it's ancient and trivial. Recency alone surfaces whatever just happened regardless of fit. Importance alone fixates on dramatic events. The *sum* is what produces human-like recall — and the weights are a design knob.
- **Recency is exponential decay over hours since last access** (`0.995 ^ hours`). This is the project's decay default. It connects "memory decay" (concept-map) to a concrete, testable formula.
- **Relevance reuses the embeddings + cosine similarity from Projects 02–04.** The query and every memory are embedded with the *same* model; relevance is their cosine similarity. The same-model rule carries over.
- **Importance is an LLM-as-judge call** (rate 1–10), assigned at write time — connects forward to Project 07's evaluation framework. In Project 05 the learner can start with a fixed importance and add LLM rating as an extension.
- **Min-max normalization before summing.** The paper scales each of the three components to `[0,1]` across the candidate set before weighting. A lab simplification: keep each component already in `[0,1]` (decay is bounded; importance/10 is bounded; cosine of normalized embeddings is ~`[0,1]`) and weight-sum — note the difference.
- Connects forward: reflection (synthesizing semantic memories from episodic ones) is the bridge to Project 09; the stateful-agent loop is Project 08.
