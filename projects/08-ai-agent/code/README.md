# Project 08: AI Agent — Code

An autonomous, multi-step agent built by making **Project 06's tool loop reliable**. The tool layer
(sandbox, schemas, dispatch, parsing) is **provided** — you built it in P06. The learning target is
the **reliability layer**: stuck detection, a steps+tokens budget, tool-error recovery, and run
evaluation — plus the judgment of when *not* to use an agent.

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
# Give the agent a multi-step task about a repository (defaults to the current dir):
python agent_app.py "what model does this repo default to, and where is it set?" --repo .
```

Until the learner cores are implemented, this raises `NotImplementedError` from the loop.

## Test (one command)

```bash
python -m pytest          # all guiding tests are OFFLINE (no network, no provider)
```

The tests fail with `NotImplementedError` until you implement the learner cores, then pass. Build
in milestone order and re-run after each:

```bash
python -m pytest tests/test_safety.py     # M1 detect_stuck, M2 BudgetTracker
python -m pytest tests/test_agent.py      # M3 run_agent (loop + recovery + guards)
python -m pytest tests/test_evaluate.py   # M4 evaluate_run
```

## Provider (swappable by key)

`config.py` picks the model from whichever API key is in `.env` — **Groq (free tier)** is preferred,
then Anthropic, then OpenAI; or set `USE_OLLAMA=1` for free local models. Override with `LLM_MODEL`.
No code change is needed to switch providers (LiteLLM routes by the model string).

## Build Milestones (the learner core)

| Milestone | File · function | What it does |
|-----------|-----------------|--------------|
| M1 | `safety.py` · `detect_stuck` | Detect a no-progress agent: the last N actions are identical |
| M2 | `safety.py` · `BudgetTracker` | Enforce a steps **and** tokens ceiling; report *why* it stopped |
| M3 | `agent.py` · `run_agent` | The reliable loop: call → dispatch **(recover)** → feed back → guard → repeat |
| M4 | `evaluate.py` · `evaluate_run` | Score a run: completion, steps, tool calls, efficiency |
| M5 | `agent_app.py` (provided) | End-to-end: run the agent on a real multi-step task, print the trace + eval |
| M6 | — | Break it: drop the budget / stuck detection / recovery, **and** the "agent where a call would do" ablation |

## File Roles

Labeled per `OPERATING_RULES.md` §Scaffolding — `provided` (complete) · `partial` (starter +
`NotImplementedError`) · `learner` (you write the core) · `reference` (docs):

| File | Role | You... |
|------|------|--------|
| `.env.example` | `provided` | copy to `.env`, add a key (or `USE_OLLAMA=1`) |
| `config.py` | `provided` | tune `Config`; do not edit the canonical provider block |
| `requirements.txt` | `provided` | install once |
| `tools.py` | `provided` | reuse — the complete Project 06 tool layer (sandbox + file tools + dispatch) |
| `agent_app.py` | `provided` | the orchestrator; runs once your cores work |
| `safety.py` | `partial` | implement `detect_stuck` (M1) and `BudgetTracker.tick`/`over_budget` (M2) |
| `agent.py` | `learner` | implement `run_agent` (M3) — the reliable loop with recovery + guards |
| `evaluate.py` | `learner` | implement `evaluate_run` (M4) — score a run |
| `tests/` | `provided` | make these pass (offline) |

Search `safety.py`, `agent.py`, and `evaluate.py` for `NotImplementedError` to find your work.

## Notes

- Fill in `../UNDERSTANDING.md` before writing any code here.
- Build in milestone order — `detect_stuck` → `BudgetTracker` → `run_agent` → `evaluate_run`.
- The tests are deterministic and offline: a fake `complete` scripts the model's turns, a
  monkeypatched dispatch tests recovery, and a throwaway fixture repo backs the file tools. No API
  key is needed to make them pass.
- This is **Project 06 made reliable** — if the tool loop in `tools.py` is unfamiliar, revisit P06.
- Document your process in `../IMPLEMENTATION.md`; record your M6 ablations (including the
  "don't use an agent" one) in `../FAILURE_ANALYSIS.md`.
