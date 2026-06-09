# Elective 04 — LLM Observability & Ops

> **Production & Hardening track** (off the 1–9 spine; after the P09 capstone).
> Teaching: [source/lesson.agent.md](source/lesson.agent.md) · Contracts:
> [source/project.md](source/project.md) · Human lesson: [rendered/lesson.html](rendered/lesson.html).

## What you're building

Instrument the Project 08 agent with **standard GenAI telemetry** (OpenTelemetry `gen_ai.*` spans),
then build an **online monitor** that aggregates live traces **per route** and **flags drift**
against a baseline — closing the offline→online loop Project 07 left open.

## Why it matters

A system you can't see is a system you can't operate. Offline eval (P07) catches what you
anticipate; production sends what you didn't. Observability + online eval are how you find out
*before* the user does.

## The rules that matter most

**Observability ≠ evaluation** (a trace shows latency, not quality). **Aggregate per route, not a
global mean** (a healthy average hides a dead route). **An error is a span attribute, not a
swallowed exception.**

## Prerequisites
Project 07 (the baseline/eval discipline), Project 08 (the agent being instrumented).

## Milestones
1. M1 emit a span · 2. M2 instrument the agent · 3. M3 aggregate per route · 4. M4 detect drift ·
5. M5 evaluate the monitor · Extension: real OTel collector, async sampled LLM-judge.

## How to start
1. Read the lesson. 2. Complete [UNDERSTANDING.md](UNDERSTANDING.md) before coding. 3.
`cd code && pip install -r requirements.txt && python -m pytest` — implement until green. 4.
`python code/evaluate_monitor.py` — flag `search`, 0 false alarms. 5. Reflect: FAILURE_ANALYSIS →
EVALUATION → STARCALLOS_REFLECTION.

## File roles (code/)
`config.py` provided · `agent_backend.py` reference · `exporter.py` provided · **`tracing.py`
learner** · **`monitor.py` learner** · `fixtures/*.jsonl` provided · `evaluate_monitor.py` provided
· `tests/` provided.
