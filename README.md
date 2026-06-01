# AI Engineering Lab

A project-based learning lab for building AI systems — not AI researchers, but **AI Systems Engineers** capable of shipping products, agents, RAG pipelines, memory systems, and personal AI operating systems.

> **Start here if you're new:** [SETUP.md](SETUP.md) → [docs/curriculum/overview.md](docs/curriculum/overview.md) → Project 1

---

## Repository Architecture

```
PHILOSOPHY.md       ← What we believe
OPERATING_RULES.md  ← How Claude reasons in this repo
ARCHITECTURE.md     ← Repo structure and why
```

**Layer hierarchy (higher overrides lower):**
```
sources/ → docs/+projects/ → evaluations/ → memory/learner/
```

- **`sources/`** — Ground truth. Primary papers, official docs, engineering blogs.
- **`catalogs/`** — Navigation maps. How to find anything quickly.
- **`skills/`** — Reusable reasoning methods (how to do things).
- **`agents/`** — Named reasoning roles (who does what).
- **`docs/`** — Teaching materials derived from sources.
- **`projects/`** — The 9 learning projects.
- **`evaluations/`** — Rubrics, grader prompts, project criteria.
- **`memory/project/`** — Decisions, retrospectives, cross-project insights.
- **`memory/learner/`** — Misconceptions, reflections, skill map.

---

## What You'll Build

| # | Project | Core Skills |
|---|---------|-------------|
| 1 | [AI Chatbot](projects/01-ai-chatbot/) | LLM APIs, context windows, prompt design, streaming |
| 2 | [Token & Embedding Explorer](projects/02-token-embedding-explorer/) | Tokenization, embeddings, vector math, similarity |
| 3 | [Semantic Search](projects/03-semantic-search/) | Vector databases, retrieval, relevance, ranking |
| 4 | [PDF Research Assistant](projects/04-pdf-research-assistant/) | RAG architecture, chunking, retrieval pipelines |
| 5 | [Personal Memory System](projects/05-personal-memory-system/) | Memory types, storage, retrieval, decay |
| 6 | [AI Coding Copilot](projects/06-ai-coding-copilot/) | Tool use, context injection, code understanding |
| 7 | [AI Evaluation Framework](projects/07-ai-evaluation-framework/) | LLM-as-judge, evals, reliability metrics |
| 8 | [AI Agent](projects/08-ai-agent/) | Agents, planning, tool loops, failure modes |
| 9 | [Personal Learning OS](projects/09-personal-learning-os/) | System design, orchestration, AI product architecture |

## Learning Philosophy

Every concept is introduced because it **solves a real engineering problem**.

For every concept, ask:
- Why does this exist?
- What breaks without it?
- Would users pay for this?
- How would a startup use this?

## How To Use This Lab

```
Read the lesson → Write your understanding → Implement → Break it → Evaluate → Reflect
```

Each project folder contains:

| File | Purpose |
|------|---------|
| `PROJECT.md` | What you're building and why |
| `LESSON.md` | The full lesson with intuition → implementation |
| `UNDERSTANDING.md` | You write this — prove you understand |
| `IMPLEMENTATION.md` | You document your implementation process |
| `FAILURE_ANALYSIS.md` | You document what you broke and learned |
| `EVALUATION.md` | You evaluate if the system works |
| `DECISIONS.md` | Engineering decisions you made |
| `PROJECT_JOURNAL.md` | Running notes as you build |
| `STARCALLOS_REFLECTION.md` | Patterns applicable to StarcallOS |
| `PROMPTS.md` | Prompts you designed and why |
| `SOURCES.md` | Sources used — documentation, papers, blogs |
| `UNDERSTANDING_FEEDBACK.md` | Mentor feedback on your understanding |
| `code/` | Your working implementation |

## Stack

- **Language:** Python 3.11+
- **Package Manager:** uv
- **LLM Abstraction:** LiteLLM (provider-agnostic)
- **Default Provider:** Anthropic Claude (swap freely)

## Setup

See [SETUP.md](SETUP.md) for step-by-step environment setup.

## Primary Inspiration

Every project reflects on [StarcallOS](../StarcallOS/) — a personal AI operating system. The goal is not to build StarcallOS directly, but to discover reusable patterns, architectures, and ideas through independent projects.

---

> "Build intuition first. Terminology second. Implementation third. Optimization fourth."
