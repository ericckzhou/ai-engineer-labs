# Curriculum Overview

Nine projects. Each one builds on the last. Each one teaches something that real AI products need.

---

## Project 1 — AI Chatbot

**Build:** A multi-turn conversational AI with streaming, system prompts, and context management.

**Core skills:** LLM APIs, message history, token limits, streaming, prompt design, cost awareness.

**Why first:** Every other project builds on understanding how to talk to an LLM. You need this foundation.

**Key question:** Why doesn't a chatbot just "remember" everything automatically?

---

## Project 2 — Token & Embedding Explorer

**Build:** An interactive tool to visualize tokenization and embedding similarity.

**Core skills:** Tokenization mechanics, embedding models, cosine similarity, vector math intuition.

**Why here:** Before you can search semantically, you need to understand what an embedding *is*. Most engineers skip this. Don't.

**Key question:** Why do two sentences with different words mean the same thing to an embedding model?

---

## Project 3 — Semantic Search

**Build:** A semantic search engine over a text corpus using vector embeddings and a vector database.

**Core skills:** Vector databases, embedding retrieval, nearest neighbor search, relevance ranking, hybrid search.

**Why here:** Semantic search is the foundation of RAG. You need to understand retrieval before you plug it into an LLM.

**Key question:** When does semantic search fail? When should you use keyword search instead?

---

## Project 4 — PDF Research Assistant

**Build:** A RAG (Retrieval-Augmented Generation) system that answers questions about uploaded PDFs.

**Core skills:** Document chunking strategies, retrieval pipelines, prompt engineering for RAG, hallucination detection.

**Why here:** RAG is the most commercially deployed AI architecture. Understanding it deeply opens up most enterprise AI work.

**Key question:** What are the five ways RAG can fail, and how do you detect each one?

---

## Project 5 — Personal Memory System

**Build:** A system that gives an AI persistent memory across conversations — episodic, semantic, and procedural.

**Core skills:** Memory taxonomy, storage architecture, retrieval strategies, memory decay, privacy considerations.

**Why here:** Memory is what separates a stateless chatbot from a true AI assistant. Every AI product eventually needs this.

**Key question:** How does human memory differ from database storage, and why does that gap matter for AI design?

---

## Project 6 — AI Coding Copilot

**Build:** A coding assistant that understands your codebase, uses tools, and generates context-aware completions.

**Core skills:** Tool use, context injection, code understanding, file system integration, prompt engineering for code.

**Why here:** Copilots are the most common AI product category. Building one teaches you tool use and structured output — essential for agents.

**Key question:** What makes a coding copilot feel smart vs. feel like autocomplete?

---

## Project 7 — AI Evaluation Framework

**Build:** An evaluation harness for measuring LLM output quality — accuracy, faithfulness, relevance, and cost.

**Core skills:** LLM-as-judge, evaluation metrics, evals design, regression testing, cost tracking.

**Why here:** You can't improve what you can't measure. Most engineers skip evals until production fails. Don't.

**Key question:** How do you measure whether your AI system is getting *better* or *worse* over time?

---

## Project 8 — AI Agent

**Build:** An autonomous agent that can use tools, plan multi-step tasks, handle failures, and produce structured output.

**Core skills:** Agent loops, tool use, planning, failure recovery, structured output, agent evaluation.

**Why here:** Agents are where AI engineering gets hard. The failure modes multiply. This project teaches you when NOT to use an agent.

**Key question:** What are the three most common ways agents fail in production, and how do you design around them?

---

## Project 9 — Personal Learning OS

**Build:** A personal AI operating system that orchestrates memory, retrieval, agents, and evaluation into a unified learning and knowledge system.

**Core skills:** System design, orchestration, multi-component AI architecture, product thinking, AI OS patterns.

**Why last:** This project synthesizes everything. It's also the most direct prototype for StarcallOS architectural patterns.

**Key question:** What does it mean to design an AI system that works *for you* — not just one that works?

---

## Optional Deepening Sources

The source layer includes targeted material that goes **beyond** what any project requires. These
are not new projects and they gate nothing — they are *optional depth*, surfaced inside each
lesson's Sources section under **"Optional — going deeper,"** to be read only **after** the lab
works and the learner can explain their own build. The rule is deliberate: finish the essential
struggle first, then reframe it with the literature.

Where the optional depth attaches:

- **Project 6 (Coding Copilot) → MCP.** `mcp-architecture`, `mcp-tools`, `mcp-security-best-practices` — the hand-wired tool loop, restated as a reusable protocol surface (and the basis for Elective 1).
- **Project 7 (Evaluation) → observability + self-correction.** `opentelemetry-genai-semconv` (eval traces as standard telemetry) and `self-refine` (the judge's critique fed back to improve the next draft).
- **Project 8 (Agent) → self-improvement & architectures.** `reflexion`, `self-refine`, `tree-of-thoughts`, `rewoo` — design options beyond a single linear ReAct trajectory, framed as choices, not requirements.
- **Project 9 (Learning OS) → composition & provenance.** `knowledge-graphs-survey` for structured memory; `opentelemetry-genai-semconv` for observing a multi-route system.

---

## Electives (off-spine)

Electives go deeper on a focused topic. They are **optional**, not numbered into the spine,
and gate nothing — take them after their listed prerequisites.

**Elective 1 — MCP Interface Layer.** Wrap Project 5's memory system as a **Model Context
Protocol server** and consume it from two different hosts. Teaches the **provider/consumer
split** (M×N → M+N): turning a subsystem into a reusable protocol surface (tools, resources,
prompts) with a real trust boundary — *not* generic tool use. Builds on Projects 5, 6, and 8.

**Key question:** What's the difference between a *capability* and an *interface to a
capability* — and why does standardizing the interface matter more than any single tool?

---

## Production & Hardening Track (off-spine, recommended after Project 9)

A named elective track for what separates a working demo from a production system: hardening it,
making it cheap/fast, and operating it. Off the 1–9 spine; each attaches to a spine prerequisite.
(Decision record: `memory/project/decisions/2026-06-09-production-hardening-elective-track.md`.)

**Elective 2 — Guardrails & Safety Layer.** Wrap the Project 8 agent in a fail-closed input/output
guard: detect prompt injection (direct **and** indirect), redact PII, enforce an output policy —
then prove on a labeled dataset you reduced attacks/leaks without blocking real users. Builds on
Projects 4, 6, 8.
*Key question:* Why is a feature that *works* not a feature that's *safe to expose*?

**Elective 3 — Cost & Latency Engineering.** Cut a working feature's cost/latency **without**
regressing quality, gated by the Project 7 eval: prompt caching, a semantic cache, and a model
cascade (cheap-first, escalate on doubt). Builds on Projects 1, 2, 7.
*Key question:* Why can you only optimize cost *safely* once you have an eval?

**Elective 4 — LLM Observability & Ops.** Instrument the Project 8 agent with standard GenAI
telemetry (OpenTelemetry `gen_ai.*` spans), then monitor live traces for drift **per route** —
closing Project 7's offline→online loop. Builds on Projects 7, 8.
*Key question:* What does a trace tell you that an eval can't, and vice versa?

**Elective 5 — Advanced RAG / Query Engineering.** Add a query-transformation stage to Project 4's
retrieval — rewriting, HyDE, multi-hop decomposition + fusion — and prove **per transform** which
ones help (and which don't) against the faithfulness eval. Builds on Projects 2, 3, 4.
*Key question:* When does a "smarter" retrieval technique actually make answers *worse*?

---

## Curriculum Principles

**Each project is standalone.** You can do them out of order if needed. But the order is designed.

**Later projects assume earlier skills.** If you jump to Project 8 without understanding RAG (Project 4), you'll hit walls.

**Each project generates real artifacts.** Not just code — understanding, failure analysis, evaluation, decisions. These compound.

**The curriculum ends, the skills don't.** After Project 9, you have a foundation for any AI product you want to build.
