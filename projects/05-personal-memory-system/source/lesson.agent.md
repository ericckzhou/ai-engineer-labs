# Lesson 05: Personal Memory System
<!-- lesson.agent.md — Agent-optimized canonical source. Do not simplify; this is the truth layer. -->

## Metadata

| Field | Value |
|-------|-------|
| Project | 05-personal-memory-system |
| Core Concepts | memory stream, retrieval scoring (relevance + recency + importance), exponential recency decay, episodic/semantic/procedural memory, memory hierarchy (main vs external context) |
| Prerequisites | See PROJECT.md (Project 02: embeddings + cosine similarity; Project 04/03: retrieval; Project 01: chat completions via LiteLLM) |
| Difficulty | Intermediate |
| Estimated Time | See PROJECT.md (10–15 hours total) |
| Last Updated | 2026-06-01 |

---

## Learning Objectives

By completing this lesson, the learner will be able to:

1. Explain why an LLM is **stateless** and why a memory system is the layer that makes an assistant *remember* across turns and sessions (source: `sources/papers/memgpt.md`).
2. Describe the **memory stream**: a growing store of natural-language memory objects, each with a creation time, a last-accessed time, and an importance score (source: `sources/papers/generative-agents.md`).
3. Implement the **retrieval score** that combines three signals — **relevance** (semantic similarity), **recency** (exponential time decay), and **importance** (salience) — into one number, and reason about what each signal contributes (source: `sources/papers/generative-agents.md`).
4. Implement **exponential recency decay**, `recency = decay_rate ^ (hours since last access)`, and explain why retrieval refreshes a memory's recency (source: `sources/papers/generative-agents.md`).
5. Distinguish **episodic** (events, dated, decaying), **semantic** (durable facts), and **procedural** (skills/instructions) memory, and explain why tagging memories by **kind** beats one flat store (source: `sources/papers/memory-systems-taxonomy.md`).
6. Explain the **memory hierarchy** — small in-prompt *main context* vs large out-of-prompt *external context* — and frame retrieval as **paging** the right memories into a limited context budget (source: `sources/papers/memgpt.md`).
7. Name and reproduce the major **failure modes** of a memory system (relevance-only recall, no decay, no importance, retrieving everything, never writing back) and say *which signal* caused each.

---

## Prerequisite Knowledge Check

Before beginning, the learner should be able to answer:

1. From Project 02: what is **cosine similarity** between two embeddings, and why must both be produced by the **same** embedding model? (Relevance scoring is exactly this.)
2. From Project 03/04: how do you embed a query and retrieve the most similar items from a store? (Memory retrieval is this, plus two more signals.)
3. From Project 01: how do you build a system + user message and send a chat completion through LiteLLM? (The orchestrator injects retrieved memories into that prompt.)

If the learner cannot compute cosine similarity between two embeddings (Project 02), revisit that first — relevance scoring is built directly on it.

---

## Core Concepts

| Concept | Definition | Why It Matters |
|---------|-----------|----------------|
| Statelessness | An LLM call has no memory of prior calls; each request is independent | The reason a memory layer must exist at all — the model won't remember unless you make it (source: `sources/papers/memgpt.md`) |
| Memory stream | A growing list of memory objects, each with text, creation time, last-accessed time, and importance | The store you retrieve from; the central data structure (source: `sources/papers/generative-agents.md`) |
| Relevance | Cosine similarity between the query embedding and a memory's embedding | Surfaces memories that are *about* the current situation (source: `sources/papers/generative-agents.md`) |
| Recency | `decay_rate ^ (hours since last access)` — an exponential decay toward 0 | Recent/recently-used memories matter more; models forgetting (source: `sources/papers/generative-agents.md`) |
| Importance | A salience score (1–10) assigned at write time — mundane vs core | Keeps a trivial-but-recent memory from outranking a pivotal one (source: `sources/papers/generative-agents.md`) |
| Retrieval score | `w_rel·relevance + w_rec·recency + w_imp·importance` | The single number that ranks memories; the lesson's learning target (source: `sources/papers/generative-agents.md`) |
| Episodic / semantic / procedural | Memory of events (dated) / facts (durable) / skills (applied) | Different `kind`s want different decay & retrieval; one flat store is worse (source: `sources/papers/memory-systems-taxonomy.md`) |
| Memory hierarchy | Small in-prompt *main context* vs large out-of-prompt *external context* | Retrieval = paging the right memories into a limited budget (source: `sources/papers/memgpt.md`) |

### Concept Relationships

```
                              ┌─ relevance  (cosine sim: query vs memory embedding)   ── "is it about this?"
memory stream ─[score each]→  ├─ recency    (decay_rate ^ hours-since-last-access)     ── "is it fresh?"
(external context)            └─ importance (salience 1–10, set at write time)         ── "does it matter?"
        │                              │
        │                     score = w_rel·rel + w_rec·rec + w_imp·imp
        │                              │
        └──── sort desc, take top-k ───┴──→ inject into the prompt (main context) ──→ LLM answers with memory
                                                  ▲                                         │
                                                  └──────── write the new turn back ────────┘  (+ refresh last-accessed)
```

Critical framing: **a memory system is Project 04's retrieval over your *own past* instead of a PDF, but ranked by three signals instead of one.** Relevance is the embedding similarity you already know; recency and importance are the two new signals that turn "most similar" into "most worth remembering right now." MemGPT supplies the *where* (small prompt vs large store, retrieval = paging); Generative Agents supplies the *how* (the three-signal score); the taxonomy supplies the *what* (events vs facts vs skills).

---

## Section 1: Motivation

### Why This Exists
An LLM is stateless: "LLMs are constrained by limited context windows" and each call starts cold (source: `sources/papers/memgpt.md`). Project 01's chatbot only "remembered" because you replayed the entire history into every prompt — that works for one short conversation and then collapses: histories outgrow the context window, every replayed token costs money, and *nothing* survives across sessions. Close the app and the assistant forgets you. A memory system is the layer that fixes this: store experiences durably outside the prompt, and retrieve only the relevant few back in when they matter.

### The Problem We're Solving
You want an assistant that remembers — your preferences, past decisions, what you told it last week — without stuffing your entire history into every prompt. The naive fixes both fail: replay-everything blows the context window and the bill; retrieve-by-similarity-only (plain Project 04 RAG over your chat log) surfaces the *semantically* closest memory even if it's ancient and trivial, and ignores a pivotal thing you just said. The memory system answer: keep a **memory stream**, and **rank** memories by relevance **and** recency **and** importance, retrieving the top few into the prompt (source: `sources/papers/generative-agents.md`).

### Real-World Stakes
Every assistant that "remembers you" — ChatGPT's memory, coding copilots that recall your conventions, customer-support bots that know your history — is some version of this. The failure is quiet and corrosive: an assistant that forgets a standing instruction you gave it (no write-back), or that fixates on an old irrelevant detail because it scored relevance only (no recency/importance), or that contradicts a decision you made yesterday (never retrieved it). Users don't file a bug — they just stop trusting it. The engineering judgment that separates a toy from a product is: did the right memory get retrieved, did stale memory decay, and did the new turn get written back?

### Would Users Pay For This?
Memory is the difference between a stateless tool and an assistant that compounds in value the more you use it. "Perpetual" multi-session conversation is exactly what MemGPT targets (source: `sources/papers/memgpt.md`), and personalization-via-memory is a headline feature of every major assistant. Users pay for an assistant that *knows them* — and that is precisely a well-scored, well-maintained memory stream.

---

## Section 2: Mental Model

### ELI12 (Explain Like I'm 12)
Imagine a friend with a giant box of index cards. Every time something happens, they jot it on a card and toss it in the box: *"Eric likes dark mode" (Tuesday), "we decided to use Groq" (last week), "brushed teeth" (this morning).* The box is huge — they can't reread every card before answering you. So when you ask a question, they grab the handful of cards that are **(1)** actually about your question, **(2)** recent or recently-used, and **(3)** a big deal — and ignore the rest. A card you keep pulling out stays near the top; a trivial old card sinks and fades. That three-part "which cards do I grab?" rule is the whole project. Picking only by "about your question" is what a plain search does — and it would hand you the toothbrushing card if you'd worded things just right.

### ELI-Engineer (Explain to a Software Engineer)
- A **memory stream** is an append-only list of memory objects: `{text, kind, created_at, last_accessed, importance, embedding}` (source: `sources/papers/generative-agents.md`).
- The store lives in **external context** (out of the prompt — your "disk"); the prompt is **main context** ("RAM"), small and fixed. Retrieval is **paging**: select the top-k memories to load into the prompt for this turn (source: `sources/papers/memgpt.md`).
- The ranking is a weighted sum of three normalized signals:
  - **relevance** = `cosine(query_embedding, memory.embedding)` — Project 02 machinery.
  - **recency** = `decay_rate ^ hours_since(memory.last_accessed)` — exponential decay, `decay_rate≈0.995`.
  - **importance** = `memory.importance / 10` — a salience score set at write time.
  - `score = w_rel·relevance + w_rec·recency + w_imp·importance`; sort descending, take `k`.
- Retrieving a memory **refreshes** its `last_accessed`, so used memories stay warm and unused ones decay (source: `sources/papers/generative-agents.md`).
- After the model answers, **write the new turn back** into the stream (with an importance score), so the system learns. Without write-back the memory never grows.

### Real-World Analogy
A memory system is a **good executive assistant**, not a search engine. Ask "what's the plan for the Berlin trip?" and a great assistant doesn't dump every email containing "Berlin" (that's relevance-only). They surface the **relevant** threads, weighted toward the **recent** ones, and they know which were a **big deal** (the signed contract) versus noise (a lunch reservation). And every time they pull a file to help you, it stays on the top of the pile for a while. The three signals are how a person decides what to bring up — and recency-on-access is why the thing you discussed this morning is top of mind.

### Intuition Diagram
```
 WRITE (every turn / observation):
   "Eric prefers Groq for the default API"  ──embed──► vector
                                              + created_at=now, last_accessed=now, importance=7, kind=semantic
                                              └─► append to memory stream (external context)

 RETRIEVE (per query, e.g. "which API should I default to?"):
   query ──embed──► q
        for each memory m in the stream:
            rel = cosine(q, m.embedding)                 # is it about this?     [0..1]
            rec = decay_rate ** hours_since(m.last_accessed)   # is it fresh?    (0..1]
            imp = m.importance / 10                       # does it matter?       [0..1]
            score(m) = w_rel*rel + w_rec*rec + w_imp*imp
        top_k = sort(memories by score, desc)[:k]
        touch(top_k): last_accessed = now                # retrieval refreshes recency
        inject top_k into the prompt ──► LLM answers grounded in memory
```

---

## Section 3: Technical Explanation

### Formal Definition
- A **memory** is an object `m = (text, kind, created_at, last_accessed, importance, embedding)`. The **memory stream** is the list of all such objects (source: `sources/papers/generative-agents.md`).
- **Retrieval** scores every memory against a query `q` on three components and returns the top-k:
  - relevance `rel(q, m) = cos(e_q, e_m)` where `e` are embeddings (source: `sources/papers/generative-agents.md`).
  - recency `rec(m) = d^{h}` where `d` is the decay rate (paper: `0.995`) and `h` = hours since `m.last_accessed` (source: `sources/papers/generative-agents.md`).
  - importance `imp(m) = importance / 10`, a salience score rated 1–10 at creation (source: `sources/papers/generative-agents.md`).
  - `score(q, m) = w_rel·rel + w_rec·rec + w_imp·imp`; the paper min-max normalizes each component to `[0,1]` and sets all weights to 1 (source: `sources/papers/generative-agents.md`).
- **Memory kinds** (source: `sources/papers/memory-systems-taxonomy.md`): *episodic* (dated events — decays), *semantic* (durable facts — should resist decay), *procedural* (skills/instructions — applied as behavior).

### How It Works (Mechanically)

**Write.** When something happens (a user turn, an observation), create a memory: embed its text once, stamp `created_at = last_accessed = now`, assign an `importance` (fixed default, or an LLM 1–10 rating), tag a `kind`, and append it to the stream.

**Score (relevance).** Embed the query with the **same** model used for memories; relevance is the cosine similarity (Project 02). Mixing embedding models makes relevance meaningless — a silent bug carried from earlier projects.

**Score (recency).** `rec = decay_rate ^ hours_since(last_accessed)`. At 0 hours this is `1.0`; it halves roughly every `ln(0.5)/ln(decay_rate)` hours. Crucially, recency is measured from **last access**, not creation — so retrieving a memory and **touching** its `last_accessed` keeps frequently-used memories warm (source: `sources/papers/generative-agents.md`).

**Score (importance).** `imp = importance / 10`. Importance is set **once at write time** — "distinguishes mundane from core memories" (source: `sources/papers/generative-agents.md`). It's why "we signed the contract" (10) outranks "brushed teeth" (1) even when both are equally recent.

**Combine & retrieve.** `score = w_rel·rel + w_rec·rec + w_imp·imp`; sort descending; take the top-k that fit the budget. Touch the returned memories' `last_accessed = now`.

**Inject & answer.** Put the retrieved memories into the prompt (main context) as context, then call the LLM (Project 01). This is MemGPT's paging step: load the relevant pages into RAM (source: `sources/papers/memgpt.md`).

**Write back.** Store the new turn as a memory so the system grows. Without this loop the assistant never learns anything new.

### The Math (When Necessary)
- Retrieval score: `score = w_rel·rel + w_rec·rec + w_imp·imp` (source: `sources/papers/generative-agents.md`).
- Exponential decay: `rec = d^h`, `d ∈ (0,1)`, `h` = hours since last access. `d=0.995`: `rec(0h)=1.0`, `rec(24h)=0.995^24≈0.887`, `rec(168h/1wk)≈0.430`. Smaller `d` forgets faster.
- Relevance: `cos(a,b) = (a·b)/(‖a‖‖b‖) ∈ [−1,1]`; for normalized embeddings of related text it sits in ~`[0,1]` (Project 02).
- Importance: `imp = importance/10 ∈ [0,1]` for a 1–10 rating.
- Note on normalization: the paper min-max scales each component across the candidate set before summing (source: `sources/papers/generative-agents.md`). The lab simplification keeps each component already bounded in `[0,1]` and weight-sums; mention the difference when reasoning about weights.

### Implementation Details
- **Same embedding model for memories and query** (carries from Projects 02–04). Mixing models makes relevance garbage — silent failure.
- **Recency from last access, and you must touch on retrieve.** If you forget to update `last_accessed` when a memory is retrieved, recency degenerates to "time since creation" and frequently-used memories wrongly decay (source: `sources/papers/generative-agents.md`).
- **Importance is set at write time, not retrieval time.** It's a stored property, not recomputed per query.
- **Weights are the design knob.** All-equal weights (the paper's default) is the start; raise `w_rec` for a chat assistant where freshness matters, raise `w_imp` to never forget pivotal facts.
- **`kind` should change decay.** Episodic memories decay; semantic facts and procedural instructions should resist decay (e.g. exclude them from the recency term or floor their recency). One flat decay policy is the easy mistake (source: `sources/papers/memory-systems-taxonomy.md`).
- **Retrieval is a budget (top-k), not all-or-nothing** — MemGPT's paging. Injecting the whole stream defeats the purpose (cost + context limit) (source: `sources/papers/memgpt.md`).
- **Write-back closes the loop.** Decide what to remember each turn; the simplest policy is "store every user turn," the agentic version is "let the model decide and rate importance."

---

## Section 4: Guided Examples

> The lab stack: `litellm` (embeddings + chat via `config.py`), an in-memory `MemoryStore`, and pure-Python scoring (cosine, decay). See `code/`. Examples below mirror the guiding tests.

### Example 1: Simple Case — exponential recency decay
```python
from scoring import recency_score

now = 1_000_000.0           # epoch seconds (any fixed "now")
hour = 3600.0
# A memory accessed right now vs 1 hour ago vs 2 hours ago, decay_rate = 0.995:
print(recency_score(now, now,          decay_rate=0.995))   # 1.0      (0 hours)
print(recency_score(now, now - hour,   decay_rate=0.995))   # 0.995    (1 hour)
print(recency_score(now, now - 2*hour, decay_rate=0.995))   # 0.990025 (2 hours)
```
**What to observe:** recency is `decay_rate ^ hours`, so a just-touched memory scores `1.0` and the score decays smoothly as the memory ages. This is why **touching `last_accessed` on retrieval** matters — it resets the clock and keeps used memories near the top.

### Example 2: Real-World Case — the three-signal score ranks memories
```python
from scoring import retrieval_score

# Three already-computed component triples (relevance, recency, importance), equal weights:
w = (1.0, 1.0, 1.0)
relevant_but_old   = retrieval_score(rel=0.9, rec=0.10, imp=0.3, weights=w)  # 1.30
fresh_but_off_topic= retrieval_score(rel=0.1, rec=1.00, imp=0.2, weights=w)  # 1.30
relevant_and_fresh = retrieval_score(rel=0.8, rec=0.90, imp=0.7, weights=w)  # 2.40  ← wins
print(relevant_and_fresh > relevant_but_old, relevant_and_fresh > fresh_but_off_topic)  # True True
```
**What to observe:** no single signal wins alone. The memory that is *about the question* **and** *fresh* **and** *matters* outranks the one that is merely very relevant but ancient, or merely fresh but off-topic. The weights `w` are the knob that tunes this (source: `sources/papers/generative-agents.md`).

### Example 3: Edge Case — relevance-only retrieval grabs the wrong memory
```python
from memory_store import Memory, MemoryStore
from retriever import retrieve

now = 1_000_000.0
store = MemoryStore()
# Same topic embedding [1,0,0]; one is trivial+old, one is important+fresh:
store.add(Memory("m0", "brushed teeth",            kind="episodic", created_at=now-1e6,
                 last_accessed=now-1e6, importance=1, embedding=[1.0, 0.0, 0.0]))
store.add(Memory("m1", "decided to default to Groq", kind="semantic", created_at=now-10,
                 last_accessed=now-10,  importance=8, embedding=[1.0, 0.0, 0.0]))

q = [1.0, 0.0, 0.0]   # query embedding — equally relevant to BOTH memories
top = retrieve(store, q, now=now, k=1, weights=(1.0, 1.0, 1.0), decay_rate=0.995)
print(top[0].id)      # 'm1'  — recency + importance break the relevance tie correctly
```
**What to observe:** relevance alone can't tell these apart (identical embeddings). Recency and importance break the tie toward the memory actually worth surfacing. A plain RAG-over-chat-log (relevance only) could just as easily return `m0`. This is *the* reason a memory system is more than Project 04 over your history (source: `sources/papers/generative-agents.md`).

---

## Section 5: Reflection Before Building

> The learner should fill UNDERSTANDING.md before proceeding to implementation.

**Questions to answer in UNDERSTANDING.md:**

1. In your own words, why is a memory system more than "Project 04 RAG over my chat history"? Use the words relevance, recency, and importance.
2. Why is an LLM stateless, and what exactly did Project 01's chatbot do to fake memory? Why does that approach break down?
3. Recency is measured from **last access**, not creation, and retrieval **touches** `last_accessed`. Predict what goes wrong if you forget to touch on retrieval.
4. Predict what each signal does *alone*: relevance-only, recency-only, importance-only. For each, give a query where it returns the wrong memory.
5. Episodic vs semantic vs procedural: give one example of each from your own use of an assistant, and say which should decay and which should not.
6. Memory hierarchy: what is "main context" vs "external context," and why is retrieval a *budget* (top-k) decision rather than "inject everything"?
7. The one thing you still don't fully understand about memory systems.

---

## Section 6: Project Assignment

See PROJECT.md and source/project.md for the full specification.

### Core Requirement
Build a personal memory system in `code/` that stores experiences and retrieves the most worth-remembering ones for a query, then a chat assistant that uses it:
- **`scoring.py`** — the three scoring signals and their combination: `recency_score` (exponential decay), `importance_score` (normalize 1–10), `relevance_score` (cosine), `retrieval_score` (weighted sum). *Learner core — the learning target.*
- **`retriever.py`** — score every memory in the store, sort, return the top-k, and **touch** their `last_accessed` (`retrieve`). *Learner core.*
- **`memory_store.py`** — the `Memory` dataclass and an in-memory `MemoryStore` (add / all / get). *(Provided — the data structure.)*
- **`embedding_helpers.py`** — embeddings glue, same model both sides. *(Provided — Project 02–04 reuse.)*
- **`chat_with_memory.py`** — the loop that embeds the query → retrieves → injects memories into the prompt → answers → writes the turn back. *(Provided orchestrator.)*

### Extended Requirements
- **LLM-rated importance:** rate each new memory's poignancy 1–10 with the model at write time, instead of a fixed default (source: `sources/papers/generative-agents.md`).
- **Kind-aware decay:** make semantic/procedural memories resist decay (floor or skip the recency term) while episodic memories decay (source: `sources/papers/memory-systems-taxonomy.md`).
- **Reflection / promotion:** periodically synthesize repeated important episodic memories into a durable semantic fact and write it back (source: `sources/papers/generative-agents.md`).
- **Persistence:** persist the stream to disk (or a Chroma collection, Project 03) so memory survives across sessions.

---

## Section 7: Project Milestones

| Milestone | What You Build | Validation |
|-----------|---------------|------------|
| M1: Recency decay | `scoring.recency_score` — `decay_rate ^ hours_since(last_accessed)` | 0h → 1.0; 1h → 0.995; older → smaller (offline test) |
| M2: Importance & relevance | `scoring.importance_score` (1–10 → [0,1]) and `scoring.relevance_score` (cosine) | identical vectors → 1.0; orthogonal → 0.0; `imp(10)=1.0` (offline test) |
| M3: Combined score | `scoring.retrieval_score` — weighted sum of the three signals | relevant+fresh+important outranks relevant-but-old and fresh-but-off-topic (offline test) |
| M4: Retrieve top-k | `retriever.retrieve` — score all, sort desc, return top-k, **touch** `last_accessed` | the important+fresh memory beats the trivial+old one on identical embeddings; returned memories' `last_accessed == now` |
| M5: Chat with memory | `chat_with_memory` wires embed → retrieve → inject → answer → write back | the assistant answers using a fact you told it earlier in the session |
| M6: Break / Evaluate | Drop a signal (relevance-only, no decay, no write-back) and watch recall degrade | each ablation surfaces the wrong memory or forgets; recorded in FAILURE_ANALYSIS.md |

---

## Section 8: Self-Evaluation

| Criterion | Does your implementation... | Pass? |
|-----------|---------------------------|-------|
| Three signals | score memories on relevance **and** recency **and** importance, not just similarity? | |
| Exponential decay | compute recency as `decay_rate ^ hours_since(last_accessed)`? | |
| Touch on retrieve | update `last_accessed = now` for the memories it returns? | |
| Top-k budget | retrieve a bounded `top_k` into the prompt, not the whole stream? | |
| Same embedding model | embed memories and queries with the one model from `config.py`? | |
| Write-back loop | store each new turn so the memory actually grows? | |
| Kinds (≥ acknowledged) | tag memories episodic/semantic/procedural (and ideally decay them differently)? | |

**Red flags (your implementation may have problems if):**
- Retrieval is cosine similarity only — you've rebuilt Project 04, not a memory system.
- Recency never changes because you never touch `last_accessed` on retrieval.
- Importance is recomputed at query time instead of stored at write time.
- You inject the entire memory stream into the prompt (no budget).
- The assistant never remembers anything new because there's no write-back.
- You report "it remembers" with no ablation showing a dropped signal breaking recall.

---

## Section 9: Common Mistakes

| Mistake | Why It Happens | Consequence | Fix |
|---------|---------------|-------------|-----|
| Relevance-only retrieval | "It's just RAG over my history" | Surfaces the semantically-closest memory even if ancient/trivial; misses what just mattered | Add recency + importance to the score (source: `sources/papers/generative-agents.md`) |
| Never touching `last_accessed` | Forgetting recency is measured from *access*, not creation | Frequently-used memories decay anyway; recency becomes "age" | Set `last_accessed = now` for every retrieved memory (source: `sources/papers/generative-agents.md`) |
| One flat decay for everything | Treating a preference like a one-off event | Durable facts (dark mode, default API) decay and get forgotten | Make semantic/procedural memories resist decay by `kind` (source: `sources/papers/memory-systems-taxonomy.md`) |
| Importance computed per query | Confusing salience with relevance | Wasted LLM calls; importance stops meaning "how big a deal was this" | Assign importance once, at write time; store it (source: `sources/papers/generative-agents.md`) |
| Injecting the whole stream | "More context is better" | Blows the context window and the bill; buries the answer | Retrieve a bounded top-k — paging, not dumping (source: `sources/papers/memgpt.md`) |
| No write-back | Treating retrieval as the whole system | The assistant never learns; same questions every session | Store the new turn (and its importance) back into the stream |
| Mixing embedding models | Memories and query embedded differently | Relevance is garbage; whole ranking fails silently | Pin one embedding model both sides (carries from Project 02) |

---

## Section 10: Connections

### How This Connects to Previous Projects
Relevance scoring **is** Project 02's cosine similarity over embeddings, and retrieving top-k from a store **is** Project 03/04's retrieval — a memory system is that retrieval with two extra signals (recency, importance) stacked on top, ranking your *own past* instead of a PDF. The prompt that consumes the retrieved memories is Project 01's system+user message construction. The "same embedding model both sides" rule is inherited wholesale.

### How This Connects to Future Projects
**Project 08 (agent)** turns write-back into a tool the model calls — MemGPT's self-editing memory, where the agent decides what to remember and when to retrieve (source: `sources/papers/memgpt.md`). **Project 09 (personal learning OS)** builds on *reflection*: synthesizing durable semantic knowledge from accumulated episodic memories (source: `sources/papers/generative-agents.md`, `sources/papers/memory-systems-taxonomy.md`). **Project 07 (evaluation)** generalizes the LLM-rated importance into a full LLM-as-judge scorer.

### How This Connects to StarcallOS
Any StarcallOS feature that "knows you" — remembers your preferences, recalls past decisions, carries context across sessions — is this memory system. The disciplines here decide whether StarcallOS feels like an assistant that *compounds* (right memory retrieved, stale memory decayed, new facts written back and promoted to durable knowledge) or a goldfish that forgets every session. The three-signal score, recency-on-access, and kind-aware decay are the concrete mechanisms; the memory stream is the data model.

### Production Patterns
Real assistant-memory systems are exactly this hierarchy plus engineering: a small in-prompt working memory and a large vector-backed store (MemGPT's main vs external context — source: `sources/papers/memgpt.md`); retrieval scored on relevance + recency + importance (Generative Agents — source: `sources/papers/generative-agents.md`); episodic observations promoted to durable semantic facts via reflection (source: `sources/papers/memory-systems-taxonomy.md`); summarization on eviction when even retrieval overflows; and the model itself deciding what to write via tools. Persistence (a real vector DB) and per-user isolation are the production add-ons.

---

## Assessment Rubric

See source/rubric.md for the complete grading rubric.

**Summary criteria:**
- [ ] Implementation runs correctly (score → retrieve top-k → inject → answer → write back)
- [ ] Retrieval combines relevance + recency + importance (not similarity alone), with exponential decay and touch-on-access
- [ ] Understanding document completed in learner's own words
- [ ] Failure analysis demonstrates intentional experimentation (drop a signal, no decay, no write-back — and the recall degradation)
- [ ] Evaluation is quantitative (which memory ranked where, score breakdowns, ablation effects), not impressionistic
- [ ] StarcallOS reflection identifies at least one concrete applicable pattern

---

## Sources

See source/resources.md for the full annotated source list.

**Required reading:**
- `sources/papers/generative-agents.md` — the memory stream and the retrieval score (relevance + recency + importance), exponential decay, importance, reflection
- `sources/papers/memgpt.md` — the memory hierarchy (main vs external context), retrieval as paging under a context budget
- `sources/papers/memory-systems-taxonomy.md` — episodic vs semantic vs procedural memory and why kind-aware storage/decay matters

**Recommended reading:**
- `sources/official-docs/scikit-learn-cosine-similarity.md` — relevance is cosine similarity (carried from Project 02)
- `sources/papers/sentence-bert.md` — the embeddings behind relevance (carried from Projects 02–04)
- `sources/official-docs/chromadb.md` — a real vector store for persisting the memory stream (carried from Project 03)

---

## Instructor Notes

<!-- Hidden context for the mentor reviewing the learner's work. -->

**Common misconceptions:**
- That a memory system is just RAG over the chat log. RAG ranks by relevance only; a memory system adds recency and importance — that's the entire point of this lesson (source: `sources/papers/generative-agents.md`).
- That recency means "time since the memory was created." It means time since **last access**, and retrieval refreshes it. Miss this and recency degenerates to age (source: `sources/papers/generative-agents.md`).
- That importance is computed when you query. It's a stored, write-time property — salience, not relevance.
- That everything should decay equally. Episodic events decay; semantic facts and procedural instructions should not (source: `sources/papers/memory-systems-taxonomy.md`).
- That you should put all memories in the prompt. The prompt is a small budget; retrieval is paging the top-k (source: `sources/papers/memgpt.md`).

**Diagnostic questions (reveal genuine vs. surface understanding):**
- "Two memories have identical embeddings — one is 'brushed teeth' from a year ago, one is 'we chose Groq' from a minute ago. Which does relevance-only retrieve, and what fixes it?" (recency + importance.)
- "You retrieve a memory but never update its timestamp. Three days later it's gone from the top results even though you use it constantly. Why?" (no touch-on-access → recency = age.)
- "Your assistant forgot a preference the user set last week, but remembered a joke from yesterday. Which signal/policy is miscalibrated?" (importance and/or kind-aware decay.)
- "Why not just inject the whole memory stream into every prompt?" (context budget + cost — paging.)

**Signs of genuine understanding:**
- The learner ablates a signal (relevance-only / no decay / no write-back) and *shows* the wrong memory being retrieved, rather than asserting it.
- They touch `last_accessed` on retrieval and can explain why, unprompted.
- They tag memories by kind and give episodic vs semantic different decay treatment.
- They can name which signal caused a bad recall (relevance vs recency vs importance) instead of "the memory was wrong."
- They keep one embedding model for memories and queries and connect it back to Project 02.
