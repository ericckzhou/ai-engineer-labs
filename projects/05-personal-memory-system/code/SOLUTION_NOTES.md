# Project 05 — Reference Solution Notes (solns branch only)

> Exists only on `solns`. **Do not merge to `main`** — leaks answers.

## Implemented (learner surface)

| File | Function(s) | Milestone |
|---|---|---|
| `scoring.py` | `recency_score`, `importance_score`, `relevance_score`, `retrieval_score` | M1–M3 |
| `retriever.py` | `retrieve` (score all, sort desc, take k, touch last_accessed) | M4 |

`chat_with_memory.py`, `memory_store.py`, `embedding_helpers.py`, `config.py` are
`[provided]` — not touched.

## Offline gate — PASS

```
$ .venv/Scripts/python.exe -m pytest -q
20 passed, 1 warning   (0 skipped)
```
Covers `test_scoring` (4 pure fns), `test_retriever` (relevance-tie break, k budget,
last_accessed touch), `test_config_models`. All offline (hand-built vectors + timestamps).

## Live smoke (provider-dependent) — PENDING

```
$ USE_OLLAMA=1 .venv/Scripts/python.exe chat_with_memory.py --seed
# expect: answer cites the Groq-default + StarcallOS memories over the trivial coffee one
```
