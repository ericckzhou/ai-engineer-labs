# Project 06: AI Coding Copilot — Code

A context-aware coding copilot: it injects the most relevant files as starting context, then runs
an **agentic tool loop** so the model can read and search the repository before answering. The
learning target is the **tool-use loop** — `config.py` and the file tools' plumbing are provided.

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
# Ask the copilot a question about a repository (defaults to the current dir):
python copilot.py "where is the default model configured?" --repo .
```

Until the four learner functions are implemented, this raises `NotImplementedError` from the loop.

## Test (one command)

```bash
python -m pytest          # all guiding tests are OFFLINE (no network, no provider)
```

The tests fail with `NotImplementedError` until you implement the learner cores, then pass. Build
in milestone order and re-run after each:

```bash
python -m pytest tests/test_tools.py        # M1 safe_resolve, M3 dispatch_tool
python -m pytest tests/test_agent_loop.py   # M2 parse_tool_calls, M4 run_agent
```

## Provider (swappable by key)

`config.py` picks the model from whichever API key is in `.env` — **Groq (free tier)** is preferred,
then Anthropic, then OpenAI; or set `USE_OLLAMA=1` for free local models. Override with
`LLM_MODEL` / `EMBEDDING_MODEL`. No code change is needed to switch providers (LiteLLM routes by the
model string).

## Build Milestones (the learner core)

| Milestone | File · function | What it does |
|-----------|-----------------|--------------|
| M1 | `tools.py` · `safe_resolve` | Resolve a tool path under the repo root; reject escapes (the sandbox) |
| M2 | `agent_loop.py` · `parse_tool_calls` | Extract the model's tool requests; `json.loads` the args |
| M3 | `tools.py` · `dispatch_tool` | Route a parsed call to the right file tool; return its string result |
| M4 | `agent_loop.py` · `run_agent` | The ReAct loop: call → dispatch → feed back → repeat, bounded by `max_steps` |
| M5 | `copilot.py` (provided) | End-to-end: inject context + run the loop against a real repo |
| M6 | — | Break it: drop the cap / the sandbox / the result feedback, record the failure |

## File Roles

Labeled per `OPERATING_RULES.md` §Scaffolding — `provided` (complete) · `partial` (starter +
`NotImplementedError`) · `learner` (you write the core) · `reference` (docs):

| File | Role | You... |
|------|------|--------|
| `.env.example` | `provided` | copy to `.env`, add a key (or `USE_OLLAMA=1`) |
| `config.py` | `provided` | tune `Config`; do not edit the canonical provider block |
| `requirements.txt` | `provided` | install once |
| `context_selector.py` | `provided` | reuse — Project 02/03 retrieval applied to source files |
| `copilot.py` | `provided` | the orchestrator; runs once your four functions work |
| `tools.py` | `partial` | implement `safe_resolve` (M1) and `dispatch_tool` (M3); file ops are provided |
| `agent_loop.py` | `learner` | implement `parse_tool_calls` (M2) and `run_agent` (M4) — the loop |
| `tests/` | `provided` | make these pass (offline) |

Search `tools.py` and `agent_loop.py` for `NotImplementedError` to find your work.

## Notes

- Fill in `../UNDERSTANDING.md` before writing any code here.
- Build in milestone order — `safe_resolve` → `parse_tool_calls` → `dispatch_tool` → `run_agent`.
- The tests are deterministic and offline: a fake `complete` scripts the model's turns, and a
  throwaway fixture repo backs the file tools. No API key is needed to make them pass.
- Document your process in `../IMPLEMENTATION.md`; record your M6 ablations in `../FAILURE_ANALYSIS.md`.
