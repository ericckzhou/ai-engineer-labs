# Project 07 — Reference Solution Notes (solns branch only)

> Exists only on `solns`. **Do not merge to `main`** — leaks answers.

## Implemented (learner surface)

| File | Function(s) | Milestone |
|---|---|---|
| `llm_judge.py` | `build_judge_prompt` (M1), `parse_judge_score` (M2) | M1/M2 |
| `metrics.py` | `summarize` (n, mean, pass_rate) | M3 |
| `regression_runner.py` | `compare_runs` (per-case delta, like-for-like means) | M4 |

`judge` orchestrator, `dataset.py`, `report.py`, `config.py` are `[provided]` — not touched.

## Offline gate — PASS

```
$ .venv/Scripts/python.exe -m pytest -q
20 passed, 1 warning   (0 skipped)
```
All pure functions, offline. `parse_judge_score` handles JSON, `Score: N`, `N/scale`,
clamps out-of-range (`Score: 9`→5), and raises `ValueError` on no-score. The live `judge`
call needs a provider (not tested here).

## Live smoke (provider-dependent) — PENDING

```
$ USE_OLLAMA=1 .venv/Scripts/python.exe regression_runner.py
# expect: judge scores the demo dataset, prints summary (mean + pass-rate)
```
