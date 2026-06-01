# Lab Philosophy

## The Goal

The learner's goal is NOT to become an AI researcher.

The goal is to become an **AI Systems Engineer** capable of:
- Building AI products
- Building AI startups
- Building copilots, RAG systems, memory systems, agents
- Evaluating AI systems rigorously
- Designing AI architectures that scale
- Building a Personal AI Operating System

## Teaching Order

```
Build intuition first.
Terminology second.
Implementation third.
Optimization fourth.
```

This order matters. Most AI courses start with math or code. We start with *why it exists*.

## Every Concept Must Answer

1. Why does this exist?
2. What problem does it solve?
3. What breaks without it?
4. What are the tradeoffs?
5. How is it used in production?
6. Would users pay for this?
7. How would a startup use this?

## The Teaching Pattern

For every concept:

1. **ELI12** — Explain Like I'm 12
2. **ELI-Engineer** — Explain Like I'm A Software Engineer
3. **Real World Analogy** — A concrete parallel from outside AI
4. **Why It Exists** — The historical or engineering motivation
5. **What Problem It Solves** — Before vs. after
6. **What Breaks Without It** — The failure mode it prevents
7. **Production Usage** — How real systems use this
8. **Code Example** — Minimal working implementation
9. **Common Mistakes** — The errors most people make
10. **Production-Level Understanding** — What separates novice from expert

## What We Focus On

**Core (timeless):**
- Retrieval
- Memory
- Embeddings
- Evaluation
- Context management
- Knowledge systems
- Agents
- Product architecture
- AI system design

**Practical math only:**
- Enough to understand embeddings, similarity, attention, probability
- Not proofs. Not research derivations.

**Not focused on:**
- Frontier model research
- Training large models from scratch
- Academic proofs
- Research rabbit holes

## The Learning Flow

```
Read
  ↓
Understand (write it in your own words)
  ↓
Mentor Review (get feedback)
  ↓
Implement
  ↓
Break (intentionally break it and learn why)
  ↓
Evaluate (measure if it works)
  ↓
Record Decisions (document the tradeoffs you made)
  ↓
Reflect (what would you do differently?)
  ↓
Next Project
```

## Complexity Discipline

Avoid:
- Agent inflation (adding agents that aren't needed)
- Framework inflation (using LangChain when 50 lines of Python suffice)
- Architecture inflation (microservices for a learning project)
- Premature optimization

Always ask:
- Is this necessary?
- What breaks without it?
- Is there a simpler solution?

## Source Grounding

Never rely solely on model knowledge. Use sources.

| Tier | Type |
|------|------|
| 1 | Official Documentation |
| 2 | Foundational Papers |
| 3 | Engineering Blogs |
| 4 | Educational Sources |

Every lesson cites its sources.
