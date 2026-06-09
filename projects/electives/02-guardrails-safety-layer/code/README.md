# Elective 02 — Guardrails & Safety Layer (code)

Wrap the provided (Project 08) agent in a **fail-closed input/output guard layer**: scan
untrusted input (user **and** retrieved content) for prompt injection, redact PII from output,
enforce an output policy. The agent and the evaluator are provided; **you build `guards.py` and
wire `guarded_agent.py`.**

> Full brief: `../source/project.md` · Lesson: `../source/lesson.agent.md` · Rubric:
> `../source/rubric.md`. Do `../UNDERSTANDING.md` **before** writing code.

## Setup (offline — no API key needed)

```bash
python -m venv .venv && . .venv/Scripts/activate    # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run the tests (your progress bar)

```bash
python -m pytest
```

On the starter, `test_config.py` passes and the rest fail with `NotImplementedError`. Implement
the cores and they go green, in this order:

| Milestone | File / symbol | Test suite |
|-----------|---------------|------------|
| M1 input scan | `guards.scan_input` | `tests/test_scan_input.py` |
| M2 PII redaction | `guards.redact_output` | `tests/test_redact_output.py` |
| M3 output policy | `guards.enforce_policy` | `tests/test_enforce_policy.py` |
| M4 compose | `guarded_agent.run_guarded` | `tests/test_compose.py` |

## Evaluate (after the cores work)

```bash
python evaluate_guards.py
```

Reports **attack-catch rate**, **benign false-positive rate**, and **PII leak rate** — read all
three (lesson §8). High recall *and* high false-positive means your rules are too broad.

## File roles

| File | Role |
|------|------|
| `config.py` | provided — bounds + PII/output policy (read these; don't hardcode) |
| `agent_backend.py` | reference — the naive agent being wrapped (do not add guards here) |
| `guards.py` | **learner** — `scan_input`, `redact_output`, `enforce_policy` |
| `guarded_agent.py` | partial — compose the guards (TODOs) |
| `datasets/attacks.jsonl` | provided — labeled attack/benign/PII set (frozen) |
| `evaluate_guards.py` | provided — the three-number scorer |
| `tests/` | provided — guiding tests |

## The one rule that matters most

**Fail closed.** On any error or doubt, a guard blocks/refuses — it never passes the input
through. A guard that fails open is worse than no guard. Everything else is detail.

> Guardrails reduce risk; they do not guarantee safety (OWASP; Greshake et al.; Presidio all say
> so explicitly). Finish this project knowing what it bought you and what still gets through.
