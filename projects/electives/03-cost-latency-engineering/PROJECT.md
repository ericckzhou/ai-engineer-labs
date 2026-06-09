# Elective 03 — Cost & Latency Engineering

> **Production & Hardening track** (off the 1–9 spine; after the P09 capstone).
> Teaching: [source/lesson.agent.md](source/lesson.agent.md) · Contracts:
> [source/project.md](source/project.md) · Human lesson: [rendered/lesson.html](rendered/lesson.html).

## What you're building

Your Project 01/08 feature is correct but expensive. Add three cost levers — **prompt caching**, a
**semantic cache**, and a **model cascade** (cheap-first, escalate on doubt) — and prove on
Project 07's frozen eval that you cut cost/latency **without regressing quality**.

## Why it matters

At scale, the bill and the latency *are* the product. But "use a cheaper model" silently breaks
correctness unless you have an eval to catch it. You built that eval in Project 07 — this is what
it unlocks.

## The one idea that matters most

**Cost and quality are separate axes.** "10× cheaper" is half a result; the other half is "and the
eval pass-rate held." The eval is the gate.

## Prerequisites
Project 07 (the eval gate), Project 02 (embeddings — the semantic cache), Project 01/08 (the feature).

## Milestones
1. M1 prompt caching · 2. M2 semantic cache · 3. M3 model cascade · 4. M4 budget · 5. M5 prove the
frontier · Extension: live models, batch API, per-route tiering.

## How to start
1. Read the lesson. 2. Complete [UNDERSTANDING.md](UNDERSTANDING.md) before coding. 3.
`cd code && pip install -r requirements.txt && python -m pytest` — implement until green. 4.
`python code/evaluate_cost.py` — read quality AND cost. 5. Reflect: FAILURE_ANALYSIS → EVALUATION →
STARCALLOS_REFLECTION.

## File roles (code/)
`config.py` provided · `feature_backend.py` reference · **`cache.py` learner** · **`cascade.py`
learner** · `budget.py` partial · `eval_set.jsonl` provided · `evaluate_cost.py` provided ·
`tests/` provided.
