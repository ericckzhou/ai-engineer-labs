# Project 09 — Reference Solution Notes (solns branch only)

> Exists only on `solns`. **Do not merge to `main`** — leaks answers.

## Implemented (learner surface)

| File | Function(s) | Milestone |
|---|---|---|
| `router.py` | `route_query` (precedence SAVE▸RECALL▸TASK, safe CHAT default) | M1 |
| `knowledge.py` | `KnowledgeGraph.add`, `related` (symmetric, no self-edge, incremental) | M2 |
| `learning_os.py` | `LearningOS.handle` (thin orchestrator: route→one worker→provenance) | M3 |
| `evaluate_os.py` | `evaluate_routing` (overall + per-route accuracy + misroutes) | M4 |

`os_app.py`, `subsystems.py`, `config.py` are `[provided]` — not touched.

## Offline gate — PASS

```
$ .venv/Scripts/python.exe -m pytest -q
28 passed, 1 warning   (0 skipped)
```
All offline: router precedence + safe default; graph linking/ranking; orchestrator
dispatches exactly one worker and attaches route/reason/provenance; routing evaluation
exposes per-route breakdown (the 0%-route-hidden-by-mean trap).

## Live smoke (provider-dependent) — PENDING

```
$ USE_OLLAMA=1 .venv/Scripts/python.exe os_app.py
# expect: SAVE/RECALL/TASK/CHAT routed correctly; each Response shows route + provenance
```
