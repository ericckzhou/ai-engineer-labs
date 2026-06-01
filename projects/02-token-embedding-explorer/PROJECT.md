# Project 2: Token & Embedding Explorer

## What We're Building

An interactive tool that visualizes:
1. How text gets tokenized (before any LLM sees it)
2. How embeddings represent meaning as vectors in high-dimensional space
3. How similarity between embeddings maps to semantic meaning
4. How embedding models cluster related concepts

## Why We're Building It

Most AI engineers treat embeddings as a black box: "text goes in, magic happens, numbers come out." This causes real bugs — mismatched models, poor chunk sizes, failed similarity searches, wasted cost.

You need to see the mechanics. Once you've watched a sentence become a 1,536-dimensional vector and then computed its cosine similarity to another sentence, semantic search stops being magic and starts being engineering.

## Learning Objectives

By the end of this project, you will be able to:

- [ ] Explain what a token is and why LLMs use them instead of words or characters
- [ ] Predict roughly how many tokens a piece of text will cost before calling the API
- [ ] Explain what an embedding vector is and what the numbers mean
- [ ] Calculate cosine similarity by hand (once) and understand what it measures
- [ ] Explain why "king - man + woman = queen" works in embedding space
- [ ] Choose the right embedding model for a given task
- [ ] Identify when two texts are semantically similar even with different words
- [ ] Explain the difference between a tokenizer and an embedding model

## Prerequisites

- Project 1 complete (LLM API basics)
- Basic understanding of vectors (high school math level)
- Python with numpy is sufficient

## Key Concepts

- **Tokenizer** — converts text to a sequence of integer IDs
- **Vocabulary** — the set of all tokens a model knows
- **Embedding** — a dense vector (list of numbers) that encodes meaning
- **Cosine similarity** — a measure of angle between vectors (not distance)
- **Embedding space** — the high-dimensional space where all embeddings live
- **Semantic similarity** — two texts meaning the same thing even with different words
- **Embedding model** — a model trained to produce useful embeddings (separate from a chat model)

## Core Engineering Problem

**Problem:** Computers work with numbers, not words. Before any AI can process text, it must be converted into numerical representations. But how do you represent *meaning* numerically?

**Answer:** Embeddings. A 1,536-dimensional vector that places semantically similar texts close together in space.

## Expected Outcomes

- A visual tokenizer explorer (shows token boundaries and IDs)
- An embedding similarity calculator
- A "semantic neighborhood" explorer (find nearest neighbors in a corpus)
- Intuition for when embeddings succeed and when they fail

## Time Estimate

**Lesson reading:** 2–3 hours
**Implementation:** 3–5 hours
**Break + Evaluate:** 1–2 hours
**Total:** 6–10 hours

## Startup Lens

**Would users pay for this?** As a tool, probably not. But understanding embeddings deeply is a prerequisite for building search, recommendation, and matching products — all of which users pay for.

**Where is the value?** In knowing which embedding model to use, how to chunk text, and when embeddings fail — that judgment is worth money.

## Key Files

```
code/
  tokenizer_explorer.py    — Visualize tokenization
  embedding_explorer.py    — Generate and inspect embeddings
  similarity_calculator.py — Cosine similarity implementation
  corpus_search.py         — Find nearest neighbors in a small corpus
  requirements.txt
  README.md
```
