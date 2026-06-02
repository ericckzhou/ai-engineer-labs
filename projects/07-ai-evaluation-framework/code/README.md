# Project 07: AI Evaluation Framework — Code

A reusable evaluation harness: score open-ended answers with an **LLM-as-a-judge**, aggregate into a
pass-rate, and **regression-test** a prompt/model change. The learning target is the judge (prompt +
parse) and turning scores into decisions (aggregate + regression). `config.py`, the dataset, the
judge call, and reporting are provided.

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
python regression_runner.py     # live demo: judge a sample dataset, print a summary
```

Until the four learner functions are implemented, this raises `NotImplementedError`.

## Test (one command)

```bash
python -m pytest          # all guiding tests are OFFLINE (no network, no provider)
```

Build in milestone order and re-run after each:

```bash
python -m pytest tests/test_llm_judge.py    # M1 build_judge_prompt, M2 parse_judge_score
python -m pytest tests/test_metrics.py      # M3 summarize
python -m pytest tests/test_regression.py   # M4 compare_runs
```

## Provider (swappable by key)

`config.py` picks the model from whichever API key is in `.env` — **Groq (free tier)** preferred, then
Anthropic, then OpenAI; or `USE_OLLAMA=1` for free local models. The **judge** model is `JUDGE_MODEL`
(defaults to the same resolution) — ideally set it to a *different* model than the one under test to
avoid self-enhancement bias. The judge always runs at `temperature=0` for repeatability.

## Build Milestones (the learner core)

| Milestone | File · function | What it does |
|-----------|-----------------|--------------|
| M1 | `llm_judge.py` · `build_judge_prompt` | Construct a bias-mitigated judge prompt (scale, reasoning-before-score, reference) |
| M2 | `llm_judge.py` · `parse_judge_score` | Robustly parse the judge's prose into a clamped int score |
| M3 | `metrics.py` · `summarize` | Aggregate JudgeResults into mean + pass-rate |
| M4 | `regression_runner.py` · `compare_runs` | Per-case baseline vs candidate → flag regressions |
| M5 | `regression_runner.py` (provided) | End-to-end: dataset → system → judge → summary report |
| M6 | — | Break it: reproduce a judge bias + a regression hidden in a flat mean |

## File Roles

`provided` (complete) · `partial` (starter + `NotImplementedError`) · `learner` (you write the core) ·
`reference` (docs):

| File | Role | You... |
|------|------|--------|
| `.env.example` | `provided` | copy to `.env`, add a key (or `USE_OLLAMA=1`) |
| `config.py` | `provided` | tune `Config`; do not edit the canonical provider block |
| `requirements.txt` | `provided` | install once |
| `dataset.py` | `provided` | the frozen test cases + loaders |
| `report.py` | `provided` | formats the summary / regression report |
| `llm_judge.py` | `partial` | implement `build_judge_prompt` (M1) and `parse_judge_score` (M2); `judge` is provided |
| `metrics.py` | `partial` | implement `summarize` (M3); `exact_match`/`contains` provided |
| `regression_runner.py` | `partial` | implement `compare_runs` (M4); `run_eval`/`main` provided |
| `tests/` | `provided` | make these pass (offline) |

Search `llm_judge.py`, `metrics.py`, `regression_runner.py` for `NotImplementedError` to find your work.

## Notes

- Fill in `../UNDERSTANDING.md` before writing any code here.
- Build in milestone order — judge prompt → parse → aggregate → regression.
- Tests are deterministic and offline: parsing, aggregation, and regression are pure functions; the
  live judge call (`judge`) is only exercised by the demo, not the tests.
- Record your M6 bias/regression experiments in `../FAILURE_ANALYSIS.md`.
