# Project 01 — Reference Solution Notes (solns branch only)

> This file exists only on `solns`. It records how the reference implementation was
> verified. **Do not merge to `main`** — it would leak answers to learners.

## What was implemented (the learner surface)

| File | Functions filled |
|---|---|
| `context.py` | `estimate_tokens`, `within_budget`, `trim_to_budget` |
| `cost_tracker.py` | `cost_of`, `CostTracker.record`, + Groq default price in `PRICES` |
| `chatbot.py` | `stream_completion`, the one-turn block in `run_repl` |

`config.py` is `[provided]` and was **not** touched. `git diff main..solns` for this project
equals exactly the three files above.

## Offline verification (the gate) — PASS

```
$ cd projects/01-ai-chatbot/code
$ python -m venv .venv && .venv/Scripts/python.exe -m pip install -r requirements.txt
$ .venv/Scripts/python.exe -m pytest -q
13 passed, 1 warning in 0.12s
```

Covers `test_context.py` (4), `test_cost_tracker.py` (4), `test_config_models.py` (5) — no
network, no provider key required. The `asyncio_mode` warning is a pre-existing pytest.ini
config note, unrelated to the solution.

## Sourced fact

- Groq `llama-3.3-70b-versatile` price: **$0.59 / MTok input, $0.79 / MTok output**
  (source: https://groq.com/pricing, looked up 2026-06-02). Not guessed.

## Live smoke run (shape-only code) — PENDING

`stream_completion` and the `run_repl` turn need a real provider and have no offline test.
To complete the smoke run, with a provider configured:

```
$ USE_OLLAMA=1 .venv/Scripts/python.exe chatbot.py     # or set GROQ_API_KEY
you> hi
you> what did i just say?      # must remember -> proves the assistant-append memory wiring
you> /cost                     # prints accumulated turn costs
you> /quit
```

Expected: tokens stream live; the second turn references the first (memory works);
`/cost` shows non-zero accumulated spend.
