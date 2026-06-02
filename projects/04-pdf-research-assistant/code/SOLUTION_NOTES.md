# Project 04 — Reference Solution Notes (solns branch only)

> Exists only on `solns`. **Do not merge to `main`** — leaks answers.

## Implemented (learner surface)

| File | Function(s) | Milestone | Verified by |
|---|---|---|---|
| `chunker.py` | `chunk_text` (overlapping windows, stable ids, no tail) | M1 | offline |
| `faithfulness.py` | `faithfulness_score` (offline), `check_faithfulness` (provider) | M5 | offline (score) |
| `generator.py` | `build_prompt` (offline), `answer` (provider) | M3/M4 | offline (prompt) |

`rag.py`, `retriever.py`, `pdf_loader.py`, `config.py` are `[provided]` — not touched.

## Offline gate — PASS

```
$ .venv/Scripts/python.exe -m pytest -q
16 passed, 1 warning   (0 skipped)
```
Covers `test_chunker`, `test_faithfulness` (score), `test_generator` (build_prompt),
`test_config_models`. `check_faithfulness` and `answer` need a provider (no offline test).

## Live smoke (provider-dependent) — PENDING

```
$ USE_OLLAMA=1 .venv/Scripts/python.exe rag.py "What was Q3 revenue?"
# expect: grounded answer citing [c#], faithfulness score printed
```
