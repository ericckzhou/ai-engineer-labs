# Elective 02 — Guardrails & Safety Layer

> **Production & Hardening track** (off the numbered 1–9 spine; recommended after the P09 capstone).
> High-level overview. Teaching content: [source/lesson.agent.md](source/lesson.agent.md).
> Implementation contracts: [source/project.md](source/project.md). Human lesson:
> [rendered/lesson.html](rendered/lesson.html).

## What you're building

Your Project 08 agent works — but it assumes a trusted user and a happy path. This elective wraps
it in a **fail-closed input/output guard layer** that makes it safe to expose to a stranger:

- **scan input** (the user prompt **and** retrieved content) for prompt injection / jailbreaks,
- **redact PII** from the output,
- **enforce an output policy**, refusing on any violation,

and proves — on a labeled dataset — that you reduced attacks and PII leaks **without** blocking
real users.

## Why it matters

OWASP ranks Prompt Injection #1 and Sensitive Information Disclosure #2 among LLM application
risks. These are the *expected* failure modes of an exposed LLM feature, not edge cases. The guard
layer is the precondition for letting any prior project touch real users or real data.

## The one idea that matters most

**Fail closed.** On any error or doubt, a guard blocks/refuses — it never passes input through. A
guard that fails open is worse than no guard. And guardrails **reduce risk; they do not guarantee
safety** — every source says so explicitly.

## Prerequisites

Project 06 (untrusted model input / sandboxing), Project 08 (the agent being wrapped), Project 04
(RAG — where indirect injection arrives).

## Milestones

1. **M1** — input scan (user + retrieved), structured verdict.
2. **M2** — PII redaction (detect → transform).
3. **M3** — output policy enforcement (fail closed).
4. **M4** — compose the wrapper (`scan → run → redact → enforce`).
5. **M5** — evaluate (attack-catch / benign-false-positive / PII-leak).
6. **Extension** — LLM-as-classifier guard; Presidio; wrap the live agent.

## How to start

1. Read [source/lesson.agent.md](source/lesson.agent.md) (or the human version).
2. Complete [UNDERSTANDING.md](UNDERSTANDING.md) **before writing code**.
3. `cd code && pip install -r requirements.txt && python -m pytest` — implement until green.
4. `python code/evaluate_guards.py` — read all three numbers.
5. Reflect: FAILURE_ANALYSIS.md → EVALUATION.md → STARCALLOS_REFLECTION.md.

## File roles (code/)

`config.py` provided · `agent_backend.py` reference · **`guards.py` learner** ·
`guarded_agent.py` partial · `datasets/attacks.jsonl` provided · `evaluate_guards.py` provided ·
`tests/` provided.
