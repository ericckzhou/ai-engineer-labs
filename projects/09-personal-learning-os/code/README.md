# Project 09: Personal Learning OS — Code

The **capstone**: wire the eight prior projects into one system behind a single front door. The
subsystem kernel (the memory store, the dispatch table, the four workers) and the app are
**provided** — you built each capability in P01–P08. The learning target is the **composition**: the
**router** (the front door), the **knowledge graph**, the **orchestrator**, and the **system-level
evaluation** of the router.

## Setup

```bash
# From this directory
uv venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

uv pip install -r requirements.txt

cp .env.example .env       # then put your API key(s) in .env (or set USE_OLLAMA=1)
```

## Run (one command)

```bash
# Interactive REPL — type 'remember …', then 'what did I save about …', then a synthesis request:
python os_app.py
# …or one-shot:
python os_app.py "remember the demo is June 20"
```

Until the learner cores are implemented, this raises `NotImplementedError` from the router/orchestrator.

## Test (one command)

```bash
python -m pytest          # all guiding tests are OFFLINE (no network, no provider)
```

The tests fail with `NotImplementedError` until you implement the learner cores, then pass. Build in
milestone order and re-run after each:

```bash
python -m pytest tests/test_router.py        # M1 route_query
python -m pytest tests/test_knowledge.py     # M2 KnowledgeGraph (add / related)
python -m pytest tests/test_learning_os.py   # M3 LearningOS.handle (orchestrator)
python -m pytest tests/test_evaluate_os.py   # M4 evaluate_routing
```

## Provider (swappable by key)

`config.py` picks the model from whichever API key is in `.env` — **Groq (free tier)** is preferred,
then Anthropic, then OpenAI; or set `USE_OLLAMA=1` for free local models. Override with `LLM_MODEL`.
No code change is needed to switch providers (LiteLLM routes by the model string). Only the live REPL
needs a provider; **every guiding test runs offline** with a fake `chat`.

## Build Milestones (the learner core)

| Milestone | File · symbol | What it does |
|-----------|---------------|--------------|
| M1 | `router.py` · `route_query` | The front door: classify a request into SAVE/RECALL/TASK/CHAT by precedence, with a safe default |
| M2 | `knowledge.py` · `KnowledgeGraph` | Link saved items by shared tags (incremental, symmetric, no self-edge); surface related items |
| M3 | `learning_os.py` · `LearningOS.handle` | The orchestrator: route → dispatch to ONE subsystem → `Response` with provenance |
| M4 | `evaluate_os.py` · `evaluate_routing` | Score the router: overall **and per-route** accuracy + the misroutes |
| M5 | `os_app.py` (provided) | End-to-end: a live REPL that routes real requests and prints route + provenance |
| M6 | — | Break it: mis-order precedence, drop the safe default, route everything to `TASK`, strip provenance |

## File Roles

Labeled per `OPERATING_RULES.md` §Scaffolding — `provided` (complete) · `partial` (starter +
`NotImplementedError`) · `learner` (you write the core) · `reference` (docs):

| File | Role | You... |
|------|------|--------|
| `.env.example` | `provided` | copy to `.env`, add a key (or `USE_OLLAMA=1`) |
| `config.py` | `provided` | tune `Config`; do not edit the canonical provider block |
| `requirements.txt` | `provided` | install once |
| `subsystems.py` | `provided` | reuse — the memory store + dispatch table + the four workers (P01/P03/P05/P08 stand-ins) |
| `os_app.py` | `provided` | the orchestrator app; runs once your cores work |
| `router.py` | `learner` | implement `route_query` (M1) — the precedence-ordered classifier with a safe default |
| `knowledge.py` | `partial` | implement `KnowledgeGraph.add` / `.related` (M2) |
| `learning_os.py` | `learner` | implement `LearningOS.handle` (M3) — route → dispatch → provenance |
| `evaluate_os.py` | `learner` | implement `evaluate_routing` (M4) — per-route accuracy + misroutes |
| `tests/` | `provided` | make these pass (offline) |

Search `router.py`, `knowledge.py`, `learning_os.py`, and `evaluate_os.py` for `NotImplementedError`
to find your work.

## Notes

- Fill in `../UNDERSTANDING.md` before writing any code here.
- Build in milestone order — `route_query` → `KnowledgeGraph` → `handle` → `evaluate_routing`.
- The tests are deterministic and offline: a fake `chat` stands in for the model and fake subsystems
  let the orchestrator be tested without a provider. No API key is needed to make them pass.
- This is the whole course **composed** — if a worker in `subsystems.py` is unfamiliar, revisit the
  project that built it (P01 chat, P03/P05 recall, P08 the agent behind `TASK`).
- Record your M6 ablations (mis-ordered precedence, no safe default, everything-to-`TASK`, stripped
  provenance) in `../FAILURE_ANALYSIS.md`, and your per-route routing numbers in `../EVALUATION.md`.
