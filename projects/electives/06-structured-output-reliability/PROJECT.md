# Elective 06 — Structured Output & Reliability

> **Production & Hardening track** (off the 1–9 spine) — a *reliability* elective the rest of the
> curriculum depends on. Strongly recommended **after P06 (tool use), before P08 (agent)**. Teaching:
> [source/lesson.agent.md](source/lesson.agent.md) · Contracts: [source/project.md](source/project.md) ·
> Human lesson: [rendered/lesson.html](rendered/lesson.html).

## What you're building

The layer that turns a model's flaky **text** into a schema-valid **object**: `extract_json` (strip the
format noise), `validate` (enforce the contract), and a bounded `coerce` **repair loop** that hands the
model its own errors and **fails closed** when it can't produce something valid. Then you **measure** the
reliability lift per failure kind. The schema, the malformed-output backend, the eval set, and the
scorer are provided; you build `structured_output.py`.

## Why it matters

Every project after P06 assumes the model returns usable structured data — tool arguments (P06), judge
verdicts (P07), agent actions (P08), routing (P09). None taught how to *guarantee* it. A model is a text
generator, not a serializer: you get fences, prose, and — worst — valid JSON that violates your schema
and so **parses while being wrong**. This is the layer that makes that boundary trustworthy.

## The rules that matter most

**Extraction fixes format; validation enforces the contract — they're different stages.** **Repair with
the specific errors, not a blind retry.** **Bound the attempts.** **Fail closed** — never return an
object you didn't validate.

## Prerequisites
Project 06 (tool use — tools are structured output), Project 01 (model calls).

## Milestones
1. M1 `parse_strict` · 2. M2 `extract_json` · 3. M3 `validate` (incl. the bool/int trap) ·
4. M4 `build_repair_prompt` + `coerce` (bounded, fail closed) · 5. M5 measure per failure kind ·
Extension: live backend, forced tool schema (`tool_choice`), guided decoding.

## How to start
1. Read the lesson. 2. Complete [UNDERSTANDING.md](UNDERSTANDING.md) before coding. 3.
`cd code && pip install -r requirements.txt && python -m pytest` — implement until green. 4.
`python code/evaluate.py` — read success per failure kind. 5. Reflect: FAILURE_ANALYSIS → EVALUATION →
STARCALLOS_REFLECTION.

## File roles (code/)
`config.py` provided · `schema.py` provided · `fake_backend.py` reference · **`structured_output.py`
learner** · `eval_set.jsonl` provided · `evaluate.py` provided · `tests/` provided.
