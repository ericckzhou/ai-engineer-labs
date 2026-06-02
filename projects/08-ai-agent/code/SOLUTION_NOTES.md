# Project 08 — Reference Solution Notes (solns branch only)

> Exists only on `solns`. **Do not merge to `main`** — leaks answers.

## Implemented (learner surface)

| File | Function(s) | Milestone |
|---|---|---|
| `safety.py` | `detect_stuck` (M1), `BudgetTracker.tick` + `over_budget` (M2) | M1/M2 |
| `agent.py` | `run_agent` (reliable loop: recovery + stuck + budget guards) | M3 |
| `evaluate.py` | `evaluate_run` (completed/steps/tool_calls/efficiency/stop_reason) | M4 |

`agent_app.py`, `tools.py`, `config.py`, provided dataclasses + `parse_tool_calls` — not touched.

## Offline gate — PASS

```
$ .venv/Scripts/python.exe -m pytest -q
25 passed, 1 warning   (0 skipped)
```
All four stop-reason paths exercised offline via scripted `complete`: answered, stuck
(identical repeated action), budget (step/token ceiling), and tool-error recovery (a
raising dispatch becomes an observation, run continues). `evaluate_run` keys completion
off stop_reason AND substring (a stuck run carrying text scores `completed=False`).

## Live smoke (provider-dependent) — PENDING

```
$ USE_OLLAMA=1 .venv/Scripts/python.exe agent_app.py "what model does this repo default to?" --repo . --expect groq
# expect: ReAct trace of tool calls, final answer, stop_reason=answered, evaluate_run summary
```
