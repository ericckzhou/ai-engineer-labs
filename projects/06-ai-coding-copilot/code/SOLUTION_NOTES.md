# Project 06 — Reference Solution Notes (solns branch only)

> Exists only on `solns`. **Do not merge to `main`** — leaks answers.

## Implemented (learner surface)

| File | Function(s) | Milestone |
|---|---|---|
| `tools.py` | `safe_resolve` (path-escape guard), `dispatch_tool` (router) | M1, M3 |
| `agent_loop.py` | `parse_tool_calls` (M2), `run_agent` (ReAct loop, M4) | M2, M4 |

`copilot.py`, `config.py`, provided file ops + `TOOL_SCHEMAS` — not touched.

## Offline gate — PASS

```
$ .venv/Scripts/python.exe -m pytest -q
18 passed, 1 warning   (0 skipped)
```
Fully offline: `safe_resolve` rejects `../../etc/passwd`; `dispatch_tool` routes/errors;
`parse_tool_calls` json.loads the args string; `run_agent` drives a scripted `complete`
(injected) through call→dispatch→feedback and hits the `max_steps` sentinel.

## Live smoke (provider-dependent) — PENDING

```
$ USE_OLLAMA=1 .venv/Scripts/python.exe copilot.py "where is safe_resolve defined?"
# expect: model issues search_code/read_file tool calls, then answers from the results
```
