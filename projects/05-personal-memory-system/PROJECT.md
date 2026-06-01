# Project 5: Personal Memory System

## What We're Building

A persistent memory system that gives an AI assistant memory across conversations. It stores, retrieves, and decays memories across three memory types: episodic (what happened), semantic (what is true), and procedural (how to do things).

## Why We're Building It

The difference between a chatbot and an AI assistant is memory. Without memory, every conversation starts cold. With memory, the AI can learn your preferences, remember past conversations, and become genuinely useful over time. This is the foundation of personal AI operating systems.

## Learning Objectives

- [ ] Implement the three memory types: episodic, semantic, procedural
- [ ] Design memory storage with metadata for temporal retrieval
- [ ] Implement memory retrieval with recency and relevance scoring
- [ ] Design a memory decay function and explain why it exists
- [ ] Handle memory conflicts (new information contradicts old)
- [ ] Evaluate memory retrieval quality
- [ ] Address privacy concerns in memory system design

## Key Concepts

Episodic memory, semantic memory, procedural memory, memory decay, retrieval scoring, temporal recency, memory consolidation, privacy-first design

## Core Engineering Problem

**Problem:** LLM conversations are stateless — every call forgets everything. How do you build a system that accumulates knowledge about a user over time and retrieves the right memories at the right moment?

## Time Estimate

**Total:** 10–15 hours

## Startup Lens

Personal memory is the moat for AI assistant products. Users who've taught their AI assistant for 6 months have a high switching cost. This is why Apple Intelligence, Google Gemini, and every AI assistant company is racing to build it.

## Key Files

```
code/
  memory_types.py       — Episodic, semantic, procedural storage
  memory_store.py       — Persistence layer
  memory_retriever.py   — Relevance + recency scoring
  memory_decay.py       — Forgetting curves
  memory_manager.py     — Conflict resolution, consolidation
  chat_with_memory.py   — Integration example
  evaluate_memory.py    — Retrieval quality evaluation
  requirements.txt
  README.md
```
