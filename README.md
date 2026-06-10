# AI Engineering Lab

A source-grounded, test-driven AI systems engineering lab for learning how to build, evaluate, break, and reason about real AI systems.

This is not a collection of AI demos. It is a structured learning system: every project combines source reading, implementation, tests, failure analysis, evaluation, and reflection.

> **Start here:** [SETUP.md](SETUP.md) -> [Project Catalog](projects/index.html) -> [Project 1](projects/01-ai-chatbot/)

---

## Why This Repository Exists

Most AI tutorials stop at implementation.

This repository treats AI engineering as a learning system. Every project requires:

- reading primary sources
- explaining the concept in your own words
- implementing the core system
- running tests
- breaking the system intentionally
- evaluating results
- recording decisions, failures, prompts, and reflections

The goal is not to finish tutorials. The goal is to produce evidence of understanding.

## Progress Snapshot

| Metric | Status |
|---|---:|
| Core projects | 9 |
| Electives | 6 |
| Source notes | 50 |
| Rendered lessons | 15 |
| Rendered source pages | 50 |
| Test files | 58 |
| Completed implementations | TBD |
| Evaluation reports | TBD |
| Failure analyses | TBD |

## What You Build

The curriculum moves from individual AI primitives to a composed AI operating system:

```txt
Chatbot
  -> Tokens & Embeddings
  -> Semantic Search
  -> PDF RAG Assistant
  -> Personal Memory System
  -> AI Coding Copilot
  -> AI Evaluation Framework
  -> AI Agent
  -> Personal Learning OS
```

Optional elective:

```txt
MCP Interface Layer
```

## Project Map

| # | Project | What You Build | Core Skill |
|---|---|---|---|
| 1 | [AI Chatbot](projects/01-ai-chatbot/) | Multi-turn CLI chatbot with streaming and cost tracking | LLM APIs |
| 2 | [Token & Embedding Explorer](projects/02-token-embedding-explorer/) | Tokenization and embedding similarity explorer | Tokens, embeddings |
| 3 | [Semantic Search](projects/03-semantic-search/) | Vector search engine over a corpus | Retrieval |
| 4 | [PDF Research Assistant](projects/04-pdf-research-assistant/) | RAG system with citations and faithfulness checks | RAG |
| 5 | [Personal Memory System](projects/05-personal-memory-system/) | Persistent memory with relevance, recency, and importance scoring | Memory |
| 6 | [AI Coding Copilot](projects/06-ai-coding-copilot/) | Tool-using code assistant grounded in repo files | Tool use |
| 7 | [AI Evaluation Framework](projects/07-ai-evaluation-framework/) | LLM-as-judge and regression evaluation harness | Evals |
| 8 | [AI Agent](projects/08-ai-agent/) | Bounded tool-using agent with failure recovery | Agents |
| 9 | [Personal Learning OS](projects/09-personal-learning-os/) | Orchestration layer combining memory, retrieval, agents, and evals | System design |

## Electives

Electives are optional off-spine deep dives. They are not required to complete the core curriculum.

| Elective | What You Build | Why It Matters |
|---|---|---|
| [MCP Interface Layer](projects/electives/01-mcp-interface-layer/) | Wrap the memory system as an MCP server | Teaches provider/consumer protocol design |

### Production & Hardening track (recommended after the capstone)

What separates a demo from a production system — hardening, cost/latency, and operations. Off-spine; each attaches to a spine prerequisite.

| Elective | What You Build | Why It Matters |
|---|---|---|
| [Guardrails & Safety Layer](projects/electives/02-guardrails-safety-layer/) | A fail-closed input/output guard around the agent | Prompt-injection defense, PII redaction, output policy |
| [Cost & Latency Engineering](projects/electives/03-cost-latency-engineering/) | Caching + a model cascade, gated by the eval | Cut cost/latency without regressing quality |
| [LLM Observability & Ops](projects/electives/04-llm-observability-ops/) | GenAI telemetry + a per-route drift monitor | Closes the offline→online evaluation loop |
| [Advanced RAG / Query Engineering](projects/electives/05-advanced-rag-query-engineering/) | Query rewriting, HyDE, multi-hop fusion | Eval-gated retrieval beyond naive RAG |
| [Structured Output & Reliability](projects/electives/06-structured-output-reliability/) | An extract → validate → repair loop that fails closed | Make model output trustworthy data (recommended after P06, before P08) |

## Branch Policy

The `main` branch is the learner version: lessons, setup, starter code, tests, rubrics, and TODOs. It intentionally does not include completed learner-owned core implementations.

Reference implementations belong on a separate `solutions` branch so learners can fork `main` without spoilers while reviewers can still inspect completed work.

## What Makes This Different

Most AI projects demonstrate output. This repo demonstrates learning.

It includes:

- source-grounded lessons from papers, official docs, and engineering guides
- runnable starter code and guiding tests
- rubrics and evaluation criteria
- failure-analysis workflows
- reflection and understanding artifacts
- generated HTML lessons and rendered source-map pages
- Claude-oriented agents, skills, catalogs, and operating rules
- a capstone that composes prior systems into a Personal Learning OS

## Browse The Lab

- [Project Catalog](projects/index.html)
- [Curriculum Overview](docs/curriculum/overview.md)
- [Rendered Source Map](catalogs/rendered/source-map.html)
- [Setup Guide](SETUP.md)

## How Each Project Works

```txt
Read the lesson
  -> explain it in your own words
  -> implement the core system
  -> run tests
  -> break it intentionally
  -> evaluate results
  -> reflect
```

Each project includes:

| File | Purpose |
|---|---|
| `PROJECT.md` | High-level brief |
| `source/lesson.agent.md` | Canonical lesson |
| `rendered/lesson.html` | Human-readable lesson |
| `source/project.md` | Detailed project spec |
| `source/resources.md` | Source-backed reading list |
| `source/rubric.md` | Assessment criteria |
| `source/reflection.template.md` | Reflection prompts |
| `UNDERSTANDING.md` | Learner explains the concept |
| `UNDERSTANDING_FEEDBACK.md` | Mentor feedback on the learner's understanding |
| `IMPLEMENTATION.md` | Implementation notes |
| `FAILURE_ANALYSIS.md` | What broke and why |
| `EVALUATION.md` | Measured results |
| `DECISIONS.md` | Engineering decisions |
| `PROJECT_JOURNAL.md` | Build log |
| `STARCALLOS_REFLECTION.md` | Patterns applicable to StarcallOS |
| `PROMPTS.md` | Prompt experiments and reasoning |
| `code/` | Starter code, tests, and implementation |

## Repository Intelligence Layer

This repo has a knowledge hierarchy:

```txt
PHILOSOPHY.md
  -> OPERATING_RULES.md
  -> ARCHITECTURE.md
  -> sources/
  -> docs/ + projects/
  -> evaluations/
  -> memory/
```

Sources provide truth. Catalogs route humans and agents to the right materials. Memory records learning outcomes. Agents and skills define workflows for reviewing, teaching, grading, and synthesizing documentation.

Key directories:

- `sources/` - Ground truth: papers, official docs, engineering blogs, and educational references.
- `catalogs/` - Navigation maps for sources, concepts, agents, skills, and learning objectives.
- `skills/` - Reusable reasoning methods.
- `agents/` - Named reasoning roles and responsibilities.
- `docs/` - Teaching materials derived from sources.
- `projects/` - The core labs and electives.
- `evaluations/` - Rubrics, grader prompts, and evaluation criteria.
- `memory/project/` - Decisions, retrospectives, and lessons learned.
- `memory/learner/` - Misconceptions, reflections, and skill maps.

## Stack

- Python 3.11+
- uv
- LiteLLM
- pytest
- Chroma / vector databases where needed
- Model Context Protocol for the elective
- Generated standalone HTML for lessons and sources

## Setup

See [SETUP.md](SETUP.md) for full setup.

Quick start:

```bash
uv venv
.venv\Scripts\activate
uv pip install -r requirements.txt
python scripts/validate_curriculum.py
```

Each project has its own `code/README.md` with project-specific setup, run, and test commands.

## For Resume Reviewers

This repo is designed to show:

- applied AI systems engineering
- source-backed technical learning
- test-driven implementation
- evaluation and failure analysis
- AI agent and tool workflow design
- curriculum and developer education infrastructure

The capstone, [Personal Learning OS](projects/09-personal-learning-os/), composes prompting, embeddings, search, RAG, memory, tools, evaluation, and agents into one orchestration layer.

## Inspiration

Each project includes a `STARCALLOS_REFLECTION.md` to capture patterns that could apply to StarcallOS, a personal AI operating system. This lab does not build StarcallOS directly; it builds the understanding and reusable patterns that could inform it.

---

> Build intuition first. Terminology second. Implementation third. Optimization fourth.
