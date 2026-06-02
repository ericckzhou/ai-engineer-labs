# Lesson 09: Personal Learning OS
<!-- lesson.agent.md — Agent-optimized canonical source. Do not simplify; this is the truth layer. -->

## Metadata

| Field | Value |
|-------|-------|
| Project | 09-personal-learning-os |
| Core Concepts | system design / composition; the augmented LLM as a system (retrieval + tools + memory); query **routing** (classify-then-dispatch); the **orchestrator** (route → dispatch → synthesize with provenance); a lightweight personal **knowledge graph** (link saved items, surface related); evaluating the *system* (routing accuracy per route), not just a component |
| Prerequisites | See PROJECT.md (Projects 05–08: memory, retrieval, the agent, evaluation — this capstone *orchestrates* them and *provides* offline stand-ins of each) |
| Difficulty | Intermediate (capstone — integration over invention) |
| Estimated Time | See PROJECT.md (15–20 hours total) |
| Last Updated | 2026-06-02 |

---

## Learning Objectives

By completing this lesson, the learner will be able to:

1. Describe a multi-capability AI app as an **augmented LLM assembled into a system** — "an LLM enhanced with augmentations such as retrieval, tools, and memory" — and explain why the eight prior projects are *subsystems* of one OS, not eight separate apps (source: `sources/articles/building-effective-agents.md`).
2. Implement **query routing**: classify an incoming request and "direct it to a specialized followup task," and explain why routing gives "separation of concerns" — each subsystem gets a narrower, more reliable job (source: `sources/articles/building-effective-agents.md`).
3. Justify a **routing precedence** and a **safe default**: order the route checks so a high-stakes intent (save) is never shadowed by a generic one (chat), and fall back to the cheapest safe route when no signal is strong — and name the silent failure each rule prevents (source: `sources/articles/building-effective-agents.md`).
4. Build an **orchestrator** (the orchestrator-workers pattern): a central component that routes a request, dispatches it to the matching subsystem, and **synthesizes a response with provenance** — *which* route handled it and *which* stored items it used (sources: `sources/articles/building-effective-agents.md`, `sources/papers/rag-paper.md`).
5. Build a lightweight personal **knowledge graph** that links saved items by shared tags/concepts and surfaces *related* items — and explain how this turns a flat memory store into a navigable structure (the "link related memories into higher-level structure" idea from reflection) (source: `sources/papers/generative-agents.md`).
6. **Evaluate the system**, not just a part: measure **routing accuracy overall and per route** on a frozen labeled set, and explain why an overall mean can hide a route that is silently 0% (source: `sources/papers/mt-bench.md`).
7. Apply **"use the simplest thing that works"** at the system level: route a simple lookup to a single retrieval, and reserve the multi-step agent for the genuinely open-ended request — and measure the cost/latency penalty of mis-routing a simple request to the agent (source: `sources/articles/building-effective-agents.md`).
8. Name the major **failure modes** of an orchestrated system (a high-stakes intent mis-routed and silently dropped; everything sent to the expensive agent; an answer with no provenance you can't audit; a router that regresses with no eval to catch it) and say which design decision prevents each.

---

## Prerequisite Knowledge Check

Before beginning, the learner should be able to answer:

1. From Project 05: what is a memory store, and what does "retrieval" return — the raw items, or a score-ranked subset? (This project **provides** an in-memory store + keyword recall so you can route *to* it; you should already understand what it does.)
2. From Project 08: what makes a request need the **agent loop** instead of a single call — and why is the agent the highest-cost, highest-blast-radius option? (Routing's whole job is to send only the requests that *need* the agent to the agent.)
3. From Project 07/08: what does it mean to **evaluate with numbers** rather than impressions, and why measure *per case* and not just the mean? (Here you apply it to the router: per-route accuracy.)
4. From Project 04: what is **provenance / citation**, and why does an answer without a pointer to its source erode trust? (The orchestrator must return which items it used.)

If routing, orchestration, and "which subsystem handles this?" feel unfamiliar, that is expected — this capstone's *new* work is the **composition**: the router, the orchestrator, the knowledge graph, and the system-level evaluation. The subsystems themselves are provided, because you already built them.

---

## Core Concepts

| Concept | Definition | Why It Matters |
|---------|-----------|----------------|
| The augmented LLM as a system | "An LLM enhanced with augmentations such as retrieval, tools, and memory" — here, the eight prior projects wired into one app | The capstone is not a ninth isolated app; it's the realization that P01–P08 were always *parts* of one system (source: `sources/articles/building-effective-agents.md`) |
| Query routing | "Routing classifies an input and directs it to a specialized followup task" | One front door, many specialists: each subsystem gets a narrower job and a more focused prompt — "separation of concerns" (source: `sources/articles/building-effective-agents.md`) |
| Routing precedence + safe default | An *ordered* set of route checks with a fallback to the cheapest safe route when no signal is strong | The order is a correctness decision: a mis-ordered router silently drops a "remember this" as small talk, or sends a trivial lookup to the costly agent (source: `sources/articles/building-effective-agents.md`) |
| Orchestrator (orchestrator-workers) | A central component that "dynamically breaks down tasks, delegates them to worker [subsystems], and synthesizes their results" | This is the OS: route → dispatch → assemble. The synthesis step is where provenance is attached (source: `sources/articles/building-effective-agents.md`) |
| Provenance | The response carries *which route* handled it and *which stored items* it used | An orchestrated answer with no trail is an unauditable black box; provenance is what makes the system trustworthy (sources: `sources/papers/rag-paper.md`, `sources/official-docs/anthropic-citations.md`) |
| Personal knowledge graph | Saved items linked by shared tags/concepts; "related" = neighbors ranked by shared-tag weight | Turns a flat list into a navigable structure — the engineering cousin of reflection's "link memories into higher-level abstractions" (source: `sources/papers/generative-agents.md`) |
| System-level evaluation | Routing accuracy **overall and per route** on a frozen labeled set | A 90%-overall router can be 0% on `save`; only per-route numbers expose the route that's silently broken (source: `sources/papers/mt-bench.md`) |

### Concept Relationships

```
   user request
        │
        ▼
   route_query(query) ──► Route(name, reason, confidence)   ◄── M1  (classify-then-dispatch)
        │   precedence: SAVE ▸ RECALL ▸ TASK ▸ (default) CHAT
        │   confidence < threshold ──────────────► CHAT (safe default)
        ▼
   LearningOS.handle  ──► dispatch to ONE subsystem (provided kernel):     ◄── M3 (orchestrator)
        ├─ SAVE   ─► store.save(item) ─► graph.add(id, tags)   ◄── M2 (knowledge graph)
        ├─ RECALL ─► store.recall(query) ─► items
        ├─ TASK   ─► bounded agent over the store (P08)
        └─ CHAT   ─► single LLM call (P01)
        │
        ▼
   Response(answer, route, reason, provenance=[item ids / sources])   ◄── synthesize WITH provenance
        │
        ▼
   evaluate_routing(cases, route_query) ─► {accuracy, per_route, misroutes}   ◄── M4 (evaluate the SYSTEM)
```

Critical framing: **Projects 01–08 each taught one capability in isolation. Project 09 is the realization that they were subsystems all along.** The new engineering is not another model technique — it is **system design**: a router that sends each request to the right specialist, an orchestrator that assembles the answer with a trail, a graph that links what you save, and an evaluation that scores the *router* the way P07/P08 scored a component. The hardest decision in the whole course is the cheapest to state: *for this request, which subsystem should run — and how do I know the router got it right?*

---

## Section 1: Motivation

### Why This Exists
By Project 08 you have eight working capabilities: a chatbot (P01), embeddings and similarity (P02), semantic search (P03), retrieval-augmented answering with citations (P04), a memory system with recency/importance scoring (P05), a tool-using copilot (P06), an evaluation harness (P07), and a reliable autonomous agent (P08). Each runs on its own. But a *person* doesn't think in projects — they say "remember this," "what did I note about X," "summarize everything I've saved on Y," or just "explain this to me." A **Personal Learning OS** is the front door that takes any of those and sends it to the right capability. The new problem is no longer *how to build a retriever or an agent* — you've done that. It's **how to compose** them: how to decide, per request, which subsystem runs, and how to return an answer you can trust and audit. That decision — routing and orchestration — is the entire lesson.

### The Problem We're Solving
Without a router, you have two bad options. **Option A: one giant prompt** that tries to do everything — save, recall, reason, and act — in a single call. It is unreliable (the model conflates "remember this" with "answer this"), unauditable (you can't tell what it did), and expensive (you pay for the agent's machinery even on a trivial lookup). **Option B: make the user pick the tool** — a "save" button, a "search" tab, an "agent" mode. That pushes your system's complexity onto the user and defeats the point of a single front door. Routing is the third option: *the system* classifies the request and dispatches it to a specialized subsystem with a focused job. The cost of getting it wrong is concrete: mis-route a "remember my doctor's appointment" to small-talk chat and the note is **silently lost**; mis-route a one-line lookup to the agent and you've spent ten steps and real money on something a single retrieval would have answered.

### Real-World Stakes
This is the shape of every "AI assistant" product: a single conversational surface backed by many specialized capabilities. ChatGPT routes between plain chat, web browsing, code execution, and image generation. A coding assistant routes between answering, editing, and running an agent. A personal-knowledge tool (Notion AI, Mem, Reflect) routes between capture, recall, and synthesis. The product is *not* any single capability — those are commodities. The product is the **orchestration**: the right specialist for the request, every time, with a trail you can inspect. A system that routes well feels like magic; one that routes badly feels broken even when every individual subsystem works perfectly.

### Would Users Pay For This?
This *is* StarcallOS in miniature. The value of a personal AI OS is that one interface quietly does the right thing — captures what you tell it, recalls what you ask for, researches when you need depth, and never makes you choose the mode. People pay for that integration, not for yet another chatbot: the capabilities are table stakes; the seamless routing and the trustworthy, auditable answers are the moat. And the discipline that protects the bill is the same one from P08, lifted to the system: route the simple request to the cheap subsystem, reserve the expensive agent for the request that genuinely needs it.

---

## Section 2: Mental Model

### ELI12 (Explain Like I'm 12)
Imagine a big help desk with one friendly person at the front and four expert rooms behind them. You walk up and say something — anything. The front-desk person's only job is to **figure out which room you need** and walk you to the right door: the **Filing Room** if you're handing them something to keep ("remember this for me"), the **Library** if you're asking for something you stored before ("what did I write about my trip?"), the **Workshop** if you want a big multi-step job done ("go through all my notes about France and make me a summary"), or the **Chat Couch** if you just want to talk something through. If the front-desk person guesses wrong, bad things happen: hand a note to the Chat Couch and it gets thrown away; send a one-second question to the Workshop and you wait an hour for what the Library could've handed you instantly. So the front desk follows simple rules — "if they're handing me something to keep, that's *always* the Filing Room first" — and when they truly can't tell, they default to the Couch, which is safe and cheap. This project is you building that front desk: the rules for picking the room, the walk to the door, and a little notebook so you can always check *which room handled it and what it used.*

### ELI-Engineer (Explain to a Software Engineer)
- The OS is the **augmented LLM as a system**: retrieval (P03/P05), tools/agent (P06/P08), and memory (P05), wired behind one entrypoint. The subsystems are **provided** (you built them); the learning target is the composition.
- **`route_query(query) -> Route`** is a classifier. Deterministic and signal-based so it's offline-testable: match intent markers, score them, and return the highest-precedence route above a confidence threshold, else the safe default (`CHAT`). Production routing "can be handled by an LLM or a more traditional classification model/algorithm" — you build the deterministic version; the live app can swap in an LLM router (extended requirement).
- **Precedence is correctness, not style.** `SAVE` is checked before `CHAT` because a dropped save is a *data-loss* failure; `TASK` (the agent) is gated so only genuinely multi-step requests reach it. The order encodes the cost of each mistake.
- **`LearningOS.handle(query) -> Response`** is the orchestrator (orchestrator-workers): `route_query` → look up the subsystem in a dispatch table → call it → wrap the result in a `Response` that carries `route`, `reason`, and `provenance` (the item ids / sources the subsystem used). On `SAVE`, it also links the new item into the knowledge graph.
- **`KnowledgeGraph`** links saved items by shared tags; `related(id)` returns neighbors ranked by shared-tag count. It's the structure that lets "recall" surface *related* notes, not just exact hits — the reflection idea (link memories into higher-level structure) at engineering scale.
- **`evaluate_routing(cases, route_fn)`** scores the router on a frozen labeled set: overall accuracy **and per-route** accuracy, plus the list of misroutes. This is P07/P08's "numbers, per case" discipline aimed at the front desk itself.

### Real-World Analogy
The OS is a **hospital triage nurse**. Every patient comes through one door and describes their problem in their own words. The nurse doesn't treat anyone — their single, high-stakes skill is **routing**: chest pain goes to cardiology *now*, a sprained wrist to orthopedics, a question about test results to records, and "I'm not sure, I just feel off" to general intake (the safe default). Triage has a strict **precedence** — life-threatening symptoms are checked first, never shadowed by a minor complaint mentioned in the same breath — because the cost of mis-triaging the emergency is catastrophic and the cost of over-triaging a sniffle to the ER is wasted, expensive capacity. And every patient gets a **chart**: which department, why, what was done — provenance, so the next clinician can audit the decision. A hospital with brilliant specialists and a bad triage nurse is a dangerous hospital. The OS is the nurse; P01–P08 are the departments.

### Intuition Diagram
```
 REQUEST: "remember that my StarcallOS demo is on June 20"
   │  route_query → matches SAVE markers ("remember that") → Route(SAVE, conf high)
   ▼
 handle → store.save(item, tags=["starcallos","demo","june"]) → graph.add(id, tags)
   ▼  Response(answer="Saved.", route="SAVE", provenance=[item#42])

 REQUEST: "what did I save about StarcallOS?"
   │  route_query → matches RECALL markers ("what did I save") → Route(RECALL)
   ▼  handle → store.recall("StarcallOS") → [item#42, item#17]
   ▼  Response(answer="You noted: demo on June 20; …", route="RECALL", provenance=[#42,#17])

 REQUEST: "go through everything I know about StarcallOS and draft a status summary"
   │  route_query → matches TASK markers ("go through everything … draft") → Route(TASK)
   ▼  handle → bounded agent over the store (P08) → multi-step synthesis
   ▼  Response(answer="<summary>", route="TASK", provenance=[#42,#17,#9])

 REQUEST: "what's the difference between recall and precision?"   (no personal data needed)
   │  route_query → no strong SAVE/RECALL/TASK signal → CHAT (safe default)
   ▼  handle → single LLM call → Response(answer="…", route="CHAT", provenance=[])

 evaluate_routing(labeled_cases, route_query)
   ─► {accuracy: 0.92, per_route: {SAVE: 1.0, RECALL: 0.9, TASK: 0.8, CHAT: 0.95},
       misroutes: [("summarize my day", expected=TASK, got=RECALL)]}
```

---

## Section 3: Technical Explanation

### Formal Definition
- **Routing** is the workflow where the system "classifies an input and directs it to a specialized followup task." It "allows for separation of concerns, and building more specialized prompts" and is the right pattern "for complex tasks where there are distinct categories that are better handled separately" (source: `sources/articles/building-effective-agents.md`).
- A **route** is one of a fixed, small set of categories `{SAVE, RECALL, TASK, CHAT}`, each bound to exactly one subsystem. `route_query` returns the chosen route plus a `reason` (why) and a `confidence` (how strong the signal was).
- The **orchestrator** follows the orchestrator-workers pattern: a central component that "dynamically breaks down tasks, delegates them to worker [subsystems], and synthesizes their results" (source: `sources/articles/building-effective-agents.md`). Here the "breakdown" is the route decision and the "synthesis" is wrapping the subsystem's output with provenance into a `Response`.
- **Provenance** is the set of identifiers (stored item ids and/or source pointers) that produced the answer — the RAG/citation principle that an answer should carry a verifiable pointer to what it was built from (sources: `sources/papers/rag-paper.md`, `sources/official-docs/anthropic-citations.md`).
- A **knowledge graph** here is an undirected weighted graph `G = (V, E)` where `V` = saved item ids and an edge `(a, b)` exists with weight = `|tags(a) ∩ tags(b)|` when the two items share at least one tag. `related(a)` returns `b`'s sorted by edge weight, descending.

### How It Works (Mechanically)

**Classify the request (routing).** `route_query` scans the text for intent markers per route, scores each route by the strength of its matched markers, and selects the **highest-precedence route whose score clears the threshold**; if none clears it, return the safe default `CHAT`. Precedence order — `SAVE`, then `RECALL`, then `TASK`, then `CHAT` — is deliberate: it ranks routes by the cost of mis-routing *to* them or *away* from them.

**Dispatch to one subsystem.** `LearningOS.handle` looks the route up in a dispatch table (`{route_name: callable}`) and calls exactly one subsystem with the query and a shared context (the store, the graph, the chat function). One request → one specialist. This is the "separation of concerns" the routing pattern buys.

**Synthesize with provenance.** Each subsystem returns a `SubsystemResult(answer, sources)`. The orchestrator wraps it into a `Response(answer, route, reason, provenance=sources)`. The `route`/`reason`/`provenance` fields are not decoration — they are what make the system auditable: you can always see which specialist ran, why the router chose it, and which stored items the answer used.

**Grow the graph on save.** When the route is `SAVE`, the store records the item and the orchestrator (or the save subsystem) calls `graph.add(item_id, tags)`, which links the new node to every existing node sharing a tag. Later, recall can call `graph.related(id)` to surface connected notes — the flat store becomes navigable.

**Evaluate the router.** `evaluate_routing` runs `route_query` over a **frozen** labeled set and computes overall accuracy, **per-route** accuracy (a confusion-style breakdown), and the explicit list of misroutes. This is the only way to know a router change improved things — and the only way to catch a route that's silently at 0%.

### The Math (When Necessary)
The capstone is system design, not math. Three small definitions matter:
- **Route confidence:** `confidence = matched_signal_strength` for the winning route (e.g. a normalized count/weight of matched markers), in `[0, 1]`. If `confidence < threshold`, fall back to `CHAT`. Raising the threshold trades routing *recall* for *precision* — fewer false routes, more requests sent to the safe default.
- **Edge weight (graph):** `w(a, b) = |tags(a) ∩ tags(b)|` — the number of shared tags. Symmetric (`w(a,b) = w(b,a)`), and there is no self-edge.
- **Routing accuracy:** overall = `correct / total`; per route `r` = `correct_r / total_r` where `total_r` counts cases whose *expected* route is `r`. Report both — the per-route vector is what exposes the silently broken route a single mean hides.

### Implementation Details
- **Precedence is the design decision.** The order in which routes are checked encodes the asymmetric cost of mistakes. `SAVE` first because a dropped save is silent data loss; `CHAT` last because it's the cheap, safe catch-all. Reordering the checks changes the system's behavior even with identical markers — this is the thing to get right.
- **The safe default must be the cheapest, least destructive route.** When the router is unsure, it should fall to `CHAT` (a single call that can't lose data and costs little), never to `TASK` (the expensive agent) and never silently to `SAVE` (which would store junk).
- **Route to the agent *sparingly*.** The whole P08 lesson — "add complexity only when it demonstrably improves outcomes" — becomes a *routing* rule here: only genuinely multi-step, synthesis-shaped requests get `TASK`. Mis-routing a one-line lookup to the agent is the system-level version of "using an agent where a call would do."
- **Provenance is part of the contract, not a log line.** `handle` must *return* the route and the sources in the `Response`, so any caller (UI, test, evaluator) can inspect them. Printing them to stdout and throwing them away is not provenance.
- **The graph links incrementally.** `add` connects the new node to existing nodes in one pass over current members — it does **not** rebuild all pairs each time (that's O(N²) per save and quadratic overall). And a node never links to itself.
- **Subsystems are injected.** `LearningOS` takes the dispatch table (and the chat function inside it) as a parameter, so the orchestrator and router are fully testable offline with fake subsystems and a fake chat — no provider, no network. The live `os_app.py` injects real ones.
- **Evaluate on a frozen set.** The labeled routing cases must not change between runs, or "the router improved" is meaningless — same discipline as P07's regression set and P08's task set.

---

## Section 4: Guided Examples

> The lab stack: the **provided** subsystem kernel (`MemoryStore`, the dispatch table, an injected `chat` fn), a deterministic signal-based router, a tiny pure-Python graph, and a pure-logic evaluator. Examples below mirror the guiding tests; all run **offline**.

### Example 1: Simple Case — classify a request (`route_query`)
```python
from router import route_query

route_query("remember that my StarcallOS demo is on June 20").name   # -> "SAVE"
route_query("what did I save about StarcallOS?").name                # -> "RECALL"
route_query("go through all my notes on France and draft a summary").name  # -> "TASK"
route_query("explain the difference between recall and precision").name    # -> "CHAT"  (safe default)

r = route_query("remember to email Sam")
print(r.name, "|", r.reason)   # SAVE | matched save markers: ['remember']
```
**What to observe:** the router maps free-text intent to a small fixed set of routes, and returns *why* (`reason`) — not just a label. The fourth request has no save/recall/task signal, so it falls to the safe default `CHAT`. The classification is the entire front door of the system.

### Example 2: Real-World Case — orchestrate a request end to end (`LearningOS.handle`)
```python
from learning_os import LearningOS
from subsystems import MemoryStore, make_subsystems
from knowledge import KnowledgeGraph

store, graph = MemoryStore(), KnowledgeGraph()
# fake chat fn so this is offline; the real app injects a LiteLLM-backed one
os_ = LearningOS(make_subsystems(store, graph, chat=lambda msgs: "(chat answer)"), graph)

r1 = os_.handle("remember that StarcallOS uses a routing front door")   # SAVE
print(r1.route, r1.provenance)        # 'SAVE' [<id of the new item>]

r2 = os_.handle("what did I save about StarcallOS?")                    # RECALL
print(r2.route, r2.provenance)        # 'RECALL' [<id of item saved above>]
print(r2.answer)                      # includes the stored note text
```
**What to observe:** one entrypoint (`handle`) routed two different requests to two different subsystems, and **every** response carries `route` and `provenance`. The save flowed into the store *and* the graph; the recall pulled it back out. The orchestrator never did any retrieval or saving itself — it routed and synthesized.

### Example 3: Edge Case — the per-route number a mean hides (`evaluate_routing`)
```python
from evaluate_os import evaluate_routing
from router import route_query

cases = [
    {"query": "remember to call mom", "expected_route": "SAVE"},
    {"query": "note: buy milk", "expected_route": "SAVE"},
    {"query": "what did I note about milk?", "expected_route": "RECALL"},
    {"query": "summarize everything I saved this week", "expected_route": "TASK"},
    {"query": "what is a vector database?", "expected_route": "CHAT"},
]
report = evaluate_routing(cases, route_query)
print(report["accuracy"])     # e.g. 0.8  (overall)
print(report["per_route"])    # e.g. {'SAVE': 1.0, 'RECALL': 1.0, 'TASK': 0.0, 'CHAT': 1.0}
print(report["misroutes"])    # [{'query': 'summarize everything I saved this week',
                              #   'expected': 'TASK', 'got': 'RECALL'}]
```
**What to observe:** overall accuracy of 0.8 looks fine — but `per_route` reveals `TASK` is **0%**: every multi-step request is being mis-routed to `RECALL`. The mean hid a completely broken route. This is exactly the P07/P08 lesson (measure per case, not just the average) applied to the system's front door, and it's how you'd find that your router needs better `TASK` markers.

---

## Section 5: Reflection Before Building

> The learner should fill UNDERSTANDING.md before proceeding to implementation.

**Questions to answer in UNDERSTANDING.md:**

1. In your own words, what is **query routing**, and why does "classify then dispatch to a specialist" give a more reliable system than one giant prompt that tries to do everything?
2. Routing **precedence** is a correctness decision. Why must `SAVE` be checked before `CHAT`, and why must the *safe default* be `CHAT` rather than `TASK` or `SAVE`? Name the concrete failure each rule prevents.
3. The orchestrator returns `route`, `reason`, and `provenance` on every response. Why is that part of the **contract** and not just logging — who needs to read them, and what breaks if `handle` only printed them?
4. Predict the four failure modes of: (a) mis-routing a `SAVE` to `CHAT`, (b) routing every request to `TASK`, (c) returning answers with no provenance, (d) shipping a router change with no evaluation. Which design decision prevents each?
5. Why does `evaluate_routing` report **per-route** accuracy and not just an overall mean? Describe a router that scores 90% overall but is dangerous.
6. The knowledge graph links saved items by shared tags. Why link **incrementally** on each save instead of rebuilding all pairs, and why must a node never be related to itself?
7. Give one request you would route to a single retrieval (`RECALL`) and one you would route to the agent (`TASK`), and justify why the first does **not** need the agent — connect this to P08's "simplest thing that works."
8. The one thing you still don't fully understand about composing subsystems into one system.

---

## Section 6: Project Assignment

See PROJECT.md and source/project.md for the full specification.

### Core Requirement
Build the **composition layer** that turns eight separate capabilities into one Personal Learning OS, in `code/`:
- **`router.py`** — `route_query` (M1) is the *learner core*: the deterministic, precedence-ordered, safe-default classifier that is the system's front door. The `Route` record and the marker tables' *shape* are *provided* scaffolding.
- **`knowledge.py`** — `KnowledgeGraph.add` / `.related` (M2) is the *learner core*: link saved items by shared tags and surface related ones, incrementally. The dataclass fields are *provided*.
- **`learning_os.py`** — `LearningOS.handle` (M3) is the *learner core*: the orchestrator — route → dispatch to one subsystem → synthesize a `Response` with provenance (and link into the graph on save). `Response` is *provided*.
- **`evaluate_os.py`** — `evaluate_routing` (M4) is the *learner core*: score the router overall and per route on a frozen set, and list the misroutes.
- **`subsystems.py`** — the provided kernel: `MemoryStore` (save/keyword-recall), `make_subsystems(store, graph, chat)` (the dispatch table), and the four subsystem callables. *(Provided — these stand in for P01/P03/P05/P08, which you already built.)*
- **`os_app.py`** — the orchestrator app: build a real LiteLLM-backed `chat`, wire the subsystems, run a REPL, and for each request print the route, the reason, the answer, and the provenance. *(Provided.)*

### Extended Requirements
- **LLM-backed router:** add an alternate `route_query_llm` that classifies via a single low-temperature model call returning a route label, and **use `evaluate_routing` to compare** it against your deterministic router on the same frozen set (source: `sources/articles/building-effective-agents.md`).
- **Provenance into the prompt:** when `RECALL`/`TASK` answer, pass the retrieved items to the model and have it cite them inline, RAG-style (sources: `sources/papers/rag-paper.md`, `sources/official-docs/anthropic-citations.md`).
- **Graph-aware recall:** after a recall hit, expand results with `graph.related(id)` so connected notes surface even without a direct keyword match (source: `sources/papers/generative-agents.md`).
- **Reflection job:** a periodic step that reads recent items and writes a higher-level summary item back into the store + graph — reflection as a synthesis subsystem (source: `sources/papers/generative-agents.md`).
- **Confidence threshold tuning:** sweep `route_threshold` and plot routing precision/recall — find the value that minimizes dangerous misroutes.

### Start Building

**Open [`code/README.md`](../code/README.md)** for setup, the milestone build order, and the file roles (which files are *provided* vs. *learner-owned*). Run `python -m pytest` to see the failing guiding tests, then implement the learner-owned functions in milestone order until they pass.

---

## Section 7: Project Milestones

| Milestone | What You Build | Validation |
|-----------|---------------|------------|
| M1: Query router | `router.route_query(query, threshold)` — classify into `{SAVE, RECALL, TASK, CHAT}` by precedence, with a safe default | save/recall/task phrasings route correctly; an unsignaled request → `CHAT` (offline test) |
| M2: Knowledge graph | `knowledge.KnowledgeGraph.add(id, tags)` + `.related(id)` — link by shared tags, incrementally; rank neighbors | items sharing tags become neighbors ranked by shared-tag count; no self-edge; symmetric (offline test) |
| M3: Orchestrator | `learning_os.LearningOS.handle(query)` — route → dispatch → `Response(answer, route, reason, provenance)`; link on save | a save then a recall round-trips through the store; every response carries route + provenance (offline test with fake subsystems) |
| M4: Evaluate routing | `evaluate_os.evaluate_routing(cases, route_fn)` — overall + per-route accuracy + misroutes | a labeled set yields correct overall/per-route numbers; a broken route shows as 0% per-route while overall stays high (offline test) |
| M5: OS end-to-end | `os_app.py` runs the REPL on a real provider, routing live requests through the subsystems | type "remember …", then "what did I save about …", then a synthesis request; see distinct routes + provenance printed |
| M6: Break / Evaluate | Mis-order precedence (CHAT first), drop the safe default, route everything to `TASK`, and strip provenance | a dropped/lost save / nonsense routes / cost+latency blow-up / unauditable answers — each recorded in FAILURE_ANALYSIS.md |

---

## Section 8: Self-Evaluation

| Criterion | Does your implementation... | Pass? |
|-----------|---------------------------|-------|
| Routing precedence | check high-stakes intents (`SAVE`) before generic ones, so a "remember this" is never shadowed by `CHAT`? | |
| Safe default | fall back to the cheapest, non-destructive route (`CHAT`) when no signal is strong — never to `TASK` or `SAVE`? | |
| One specialist per request | dispatch each request to exactly one subsystem via the table — not run several or inline their logic in `handle`? | |
| Provenance returned | put `route`, `reason`, and the used item ids/sources *in the returned `Response`*, not just print them? | |
| Graph is incremental + correct | link a new item to existing items by shared tags in one pass, with no self-edge and symmetric edges? | |
| System-level eval | report routing accuracy **per route**, not only the overall mean, and surface the misroutes? | |
| Right specialist for the job | route a simple lookup to `RECALL` and reserve `TASK` for genuinely multi-step requests — and can you name one of each? | |

**Red flags (your implementation may have problems if):**
- `CHAT` is checked first or is the highest-precedence match, so saves and recalls leak into small talk.
- Your safe default is `TASK` (every unsure request spins up the expensive agent) or `SAVE` (you store junk).
- `handle` retrieves or saves *itself* instead of dispatching to a subsystem — the orchestrator is doing a worker's job.
- `Response` has no `route`/`provenance`, so a caller can't tell what happened or audit the answer.
- `KnowledgeGraph.add` rebuilds every pair each call (O(N²)) or links a node to itself.
- Your evaluation reports a single accuracy number, so a route that's silently 0% looks fine.

---

## Section 9: Common Mistakes

| Mistake | Why It Happens | Consequence | Fix |
|---------|---------------|-------------|-----|
| Checking `CHAT` (or the broadest route) first | "Most requests are chat" | Saves/recalls get swallowed as small talk and silently lost | Order checks by the *cost of mistakes*: `SAVE` ▸ `RECALL` ▸ `TASK` ▸ `CHAT` (source: `sources/articles/building-effective-agents.md`) |
| Safe default = `TASK` | "When unsure, let the agent figure it out" | Every ambiguous request costs agent steps + money | Default to `CHAT` — the cheapest, non-destructive route; gate `TASK` behind clear multi-step signal |
| `handle` does retrieval/saving itself | "It's just one line, I'll inline it" | The orchestrator and subsystems blur; no separation of concerns; untestable | Dispatch through the table to exactly one subsystem; `handle` only routes + synthesizes |
| Provenance printed, not returned | "I can see it in the logs" | Callers/tests/evaluators can't inspect the decision; not auditable | Put `route`, `reason`, `provenance` *in the `Response`* (sources: `sources/papers/rag-paper.md`, `sources/official-docs/anthropic-citations.md`) |
| Graph rebuilt every save | "Recompute all pairs to be safe" | O(N²) per save; quadratic blow-up; slows every capture | Link the new node to current members in one pass; keep edges incremental |
| Node related to itself | forgot to skip `id == other` | "Related notes" always lists the note you're on | Skip self when adding edges and when returning `related` |
| One overall accuracy number | "90% — good enough" | A route silently at 0% is invisible; the system looks healthy and isn't | Report **per-route** accuracy + the misroute list (source: `sources/papers/mt-bench.md`) |
| Routing everything through the agent | "The agent can do anything" | Slow, costly, less reliable than a single retrieval for simple asks | Route by need; "add complexity only when it demonstrably improves outcomes" (source: `sources/articles/building-effective-agents.md`) |

---

## Section 10: Connections

### How This Connects to Previous Projects
This is **the whole course assembled into one system.** `CHAT` is Project 01 (a single completion). `RECALL` is Projects 03 and 05 (retrieval over a memory store). `SAVE` is Project 05 (capture into the store) plus the new knowledge graph. `TASK` is Project 08's reliable agent (and through it, Project 06's tools). The **provenance** the orchestrator attaches is Project 04's citation discipline. The **evaluation** of the router is Project 07/08's "numbers, per case" discipline pointed at the front door. Nothing here re-teaches a capability — every subsystem is *provided* precisely because you already built it. The new work is the one thing the prior projects deliberately left out: how to **compose** them.

### How This Connects to Future Projects
This is the terminal project of the core curriculum — but it's the *first* project of building a real product. Everything beyond here is depth on a subsystem (better retrieval, a smarter router, more tools, richer evaluation) or breadth (more routes, more capabilities behind the same front door). The pattern you build — one entrypoint, a router, a dispatch table, provenance, and a system-level eval — is the skeleton every multi-capability AI app grows on.

One concrete next step is the **MCP Interface Layer elective** (`projects/electives/01-mcp-interface-layer/`). Here the subsystems behind `route_query` are wired **in-process**; the elective shows how each (memory, retrieval, the agent) could instead be re-exposed as a **Model Context Protocol server** and the OS could *consume* them — and third-party servers — through one client. That turns the dispatch table from a hard-coded map into a **registry of interchangeable, separately-deployable capabilities**: the provider/consumer split applied to the very system you just composed. Routing and orchestration stay here in the host; the capabilities move behind a standard protocol surface.

### How This Connects to StarcallOS
**Project 09 is the smallest complete StarcallOS.** StarcallOS *is* a personal OS with one conversational surface over many capabilities — capture, recall, research, action — and its core engineering problem is exactly this lesson's: route each request to the right capability, do it with a trail the user can trust, link what the user saves into a navigable structure, and reserve the expensive autonomous machinery for the requests that truly need it. The router is StarcallOS's front door; the dispatch table is its capability registry; the provenance is its trust layer; the system-level eval is how StarcallOS knows a change to the front door didn't quietly break the "remember this" path. Build this project well and you have prototyped the spine of StarcallOS.

### Production Patterns
Real assistant systems are this skeleton plus production engineering: a router (rules, a small classifier, or an LLM) with a confidence threshold and a safe fallback; a capability/dispatch registry; per-capability prompts and budgets (P08's reliability layer on the `TASK` route); provenance and citations on every answer (P04); a frozen evaluation set for the router and for each subsystem (P07); and observability — a trace of *which route handled what* so a regression is visible. Anthropic's guidance frames the spectrum: a single augmented LLM call, then workflows (prompt chaining, **routing**, **orchestrator-workers**, evaluator-optimizer), then a full agent — reach for the simplest that works, and compose the named patterns rather than building one monolith (source: `sources/articles/building-effective-agents.md`). This project is the routing + orchestrator-workers patterns made concrete over the capabilities you already own.

---

## Assessment Rubric

See source/rubric.md for the complete grading rubric.

**Summary criteria:**
- [ ] Implementation runs correctly (router classifies by precedence with a safe default; `handle` routes → dispatches → returns a `Response` with route + provenance)
- [ ] `route_query` orders checks by the cost of mistakes and defaults to `CHAT`; never sends an unsure request to `TASK`/`SAVE`
- [ ] `LearningOS.handle` dispatches to exactly one subsystem and attaches provenance; saves flow into the store **and** the knowledge graph
- [ ] `KnowledgeGraph` links incrementally by shared tags, is symmetric, and has no self-edges
- [ ] Understanding document completed in learner's own words
- [ ] Failure analysis demonstrates intentional experimentation (mis-ordered precedence, no safe default, everything-to-`TASK`, stripped provenance)
- [ ] Evaluation is quantitative — routing accuracy **overall and per route**, with the misroutes listed — not impressionistic
- [ ] StarcallOS reflection identifies at least one concrete applicable pattern

---

## Sources

See source/resources.md for the full annotated source list.

**Required reading:**
- `sources/articles/building-effective-agents.md` — the **augmented LLM** (retrieval + tools + memory) as the building block; **routing** ("classifies an input and directs it to a specialized followup task"; "separation of concerns"); **orchestrator-workers** ("dynamically breaks down tasks, delegates … and synthesizes their results"); and "add complexity only when it demonstrably improves outcomes" as a *routing* rule. The spine of the whole capstone.
- `sources/papers/rag-paper.md` — provenance: an answer should carry a verifiable pointer to what produced it (applied here to the orchestrator's `Response`).
- `sources/papers/generative-agents.md` — reflection: linking memories into higher-level structure — the conceptual basis for the personal knowledge graph and graph-aware recall.

**Recommended reading:**
- `sources/papers/mt-bench.md` — evaluate with numbers, **per case** — applied here to the router (per-route accuracy, not just the mean).
- `sources/official-docs/anthropic-citations.md` — claim → source location; the production form of the provenance the orchestrator returns.
- `sources/official-docs/anthropic-tool-use.md` — the agentic loop behind the `TASK` route (carried from P06/P08).
- `sources/official-docs/litellm-completion.md` — the single-call interface behind the `CHAT` route and the optional LLM router (carried from P01).
- `sources/papers/knowledge-graphs-survey.md` — knowledge graphs as a data model: **entities and relations as first-class, traversable structure** — grounds the term for the lightweight tag-linked personal graph.

> **Scope of the knowledge graph:** the *lightweight, tag-linked personal graph* is grounded in the **knowledge-graphs survey** (a graph is the right structure when links between saved items are first-class and traversable) and in **Generative Agents' reflection** (linking memories into higher-level structure). It stays a modest educational construct — not a full RDF/SPARQL/ontology or KG-embedding system.

---

## Instructor Notes

<!-- Hidden context for the mentor reviewing the learner's work. -->

**Common misconceptions:**
- That the capstone is "build a ninth capability." It is not — it is **composition**. A learner who builds another retriever or another agent and stops has missed the lesson; the new work is the router, the orchestrator, the graph, and the system-level eval.
- That routing order is cosmetic. Precedence is a *correctness* decision encoding the asymmetric cost of mistakes; reordering changes behavior with identical markers.
- That the safe default is arbitrary. It must be the cheapest, least-destructive route (`CHAT`); defaulting to `TASK` burns money, defaulting to `SAVE` stores junk.
- That provenance is logging. It is part of the returned contract — the thing that makes the system auditable and testable.
- That one accuracy number evaluates a router. A high overall mean routinely hides a route that's silently 0%.
- That every request should go to the agent because "the agent is the most powerful." The most valuable routing skill is sending the *simple* request to the *cheap* subsystem.

**Diagnostic questions (reveal genuine vs. surface understanding):**
- "Your router scores 90% overall but loses every third 'remember this.' Where does that show up in your metrics, and what does it imply about precedence?" (per-route SAVE accuracy; SAVE must precede CHAT.)
- "Show me the exact line where `handle` decides which subsystem runs — and confirm it runs only one." (dispatch table lookup; one call.)
- "A caller wants to know why the OS answered the way it did. What in your `Response` lets them, and what would break if you'd only printed it?" (route/reason/provenance returned vs. logged.)
- "Give me a request you'd route to `RECALL` and one to `TASK`, and tell me why the first must *not* hit the agent." (cost/latency; simplest thing that works.)
- "Why does `related(x)` never return `x`, and why don't you rebuild the graph on every save?" (no self-edge; incremental linking, not O(N²).)

**Signs of genuine understanding:**
- The learner treats routing precedence and the safe default as correctness decisions and can name the failure each prevents.
- They keep `handle` thin — route, dispatch to one subsystem, synthesize — and put provenance in the returned `Response`.
- Their evaluation is per-route, and they can point to the route a mean would have hidden.
- They reserve `TASK` for genuinely multi-step requests and can defend "simplest thing that works" at the system level.
- They connect every design decision back to a concrete StarcallOS behavior (a lost note, a runaway bill, an unauditable answer, a silently broken front door).
