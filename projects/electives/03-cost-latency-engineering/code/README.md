# Elective 03 — Cost & Latency Engineering (code)

Cut the cost/latency of a working feature **without regressing quality**, gated by the Project 07
eval. The feature, models, and evaluator are provided; **you build the caching + routing layer.**

> Brief: `../source/project.md` · Lesson: `../source/lesson.agent.md` · Rubric: `../source/rubric.md`.
> Do `../UNDERSTANDING.md` **before** coding.

## Setup (offline — no API key)

```bash
python -m venv .venv && .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m pytest
```

`test_config.py` passes; the rest fail with `NotImplementedError` until you implement, in order:

| Milestone | File / symbol | Tests |
|-----------|---------------|-------|
| M2 semantic cache | `cache.SemanticCache` | `tests/test_cache.py` |
| M3 model cascade | `cascade.answer` | `tests/test_cascade.py` |
| M4 budget | `budget.CostTracker` | `tests/test_budget.py` |

(M1 prompt caching is a live-provider exercise — see the lesson §4 and the extension.)

## Prove it

```bash
python evaluate_cost.py
```

Prints the **frontier**: quality (pass-rate) **and** cost **and** calls **and** cache-hits,
baseline vs optimized. Ship only if quality held.

## File roles

| File | Role |
|------|------|
| `config.py` | provided — tiers, prices, thresholds, ceiling |
| `feature_backend.py` | reference — cheap/strong models + embedder (offline) |
| `cache.py` | **learner** — semantic cache (M2) |
| `cascade.py` | **learner** — cheap-first cascade (M3) |
| `budget.py` | partial — `CostTracker` (M4) |
| `eval_set.jsonl` | provided — frozen eval set |
| `evaluate_cost.py` | provided — the frontier scorer |
| `tests/` | provided |

## The rule that matters most

**Cost and quality are separate axes.** "10× cheaper" is half a result; the other half is "and the
eval pass-rate held." The eval is the gate.
