# Elective 02: Guardrails & Safety Layer — Implementation Plan

> **Status: PLANNED — awaiting approval before authoring.**
> This is the `/plan` output (Workflow A, pre-execution). No `source/`, `code/`, or
> `rendered/` exists yet. On approval, this project is authored end-to-end like Elective 01.
> **Track:** Production & Hardening (named elective track, recommended after the P09 capstone;
> off the numbered 1–9 spine). See `memory/project/decisions/2026-06-09-production-hardening-elective-track.md`.

---

## Requirements Restatement

Build the **input/output guard layer** that wraps an existing AI feature (the Project 08 agent
and/or the Project 04 RAG assistant) and makes it *safe to expose to an untrusted user*:

- **Detect prompt injection / jailbreaks** on the way in (direct and indirect).
- **Redact PII / sensitive information** on the way out (and optionally on the way in).
- **Enforce an output policy** (schema/allow-list/refusal) and **fail closed**.

The thesis: *a feature that works is not a feature that is safe.* Every prior project assumes a
trusted user and a happy path. This elective removes that assumption.

---

## Where It Fits / Prerequisites

- **Prereqs:** Project 06 (tool sandboxing / "untrusted model input"), Project 08 (the agent
  being hardened), Project 04 (RAG — indirect injection arrives through retrieved documents).
- **Relates to:** Elective 01 (the MCP trust boundary — this generalizes it from one protocol
  surface to the whole request/response path).
- **Slot:** after Project 08. It hardens the agent the learner just built.

---

## Learning Target (the incomplete core)

The learner owns the **guard functions and the wrapper that composes them** — not the agent.

```
guards.py            (learner)
  scan_input(text)        -> InputVerdict   # injection/jailbreak heuristics (+ optional classifier)
  redact_output(text)     -> (clean, hits)  # PII detection + masking
  enforce_policy(output)  -> OutputVerdict   # schema / allow-list / refusal, fail-closed
guarded_agent.py     (partial)
  run_guarded(user_input, agent) -> Result  # compose: scan -> run -> redact -> enforce
```

Setup, the underlying agent/assistant, a **labeled attack+benign dataset**, and the eval
harness are *provided*. The detection/redaction/enforcement logic is *incomplete*.

---

## Primary Sources to Gather (Workflow A step 1 — fetch & verify before authoring)

| Source | Anchors | Status |
|--------|---------|--------|
| **OWASP Top 10 for LLM Applications (2025)** — LLM01 Prompt Injection, LLM02 Sensitive Information Disclosure | the threat taxonomy + recommended mitigations (input/output validation, redaction, human-in-the-loop) | ✅ confirmed (owasp.org PDF v2025) |
| **Llama Guard** — Inan et al. 2023 (arXiv:2312.06674) | LLM-as-classifier for input/output safety; separate prompt vs response classification | ✅ confirmed |
| **Indirect prompt injection** — Greshake et al. 2023, "Not what you've signed up for" (arXiv:2302.12173) | injection via retrieved/external content (ties to P04) | ⏳ fetch & verify |
| **Microsoft Presidio** (PII detection/redaction docs) | concrete redaction approach: recognizers → anonymizers | ⏳ fetch & verify |

→ Land in `sources/official-docs/` (OWASP, Presidio) and `sources/papers/` (Llama Guard,
Greshake). Then update `catalogs/source-map.md` and re-run `scripts/render_sources.py`.

---

## File Manifest (provided / partial / learner / reference)

| File | Role | Purpose |
|------|------|---------|
| `code/config.py` | provided | canonical provider block + guard bounds (max input len, PII entity list, refusal string, policy schema) |
| `code/agent_backend.py` | reference | the capability being wrapped (condensed P08 agent or P04 assistant), offline-capable |
| `code/guards.py` | **learner** | `scan_input`, `redact_output`, `enforce_policy` — the trust boundary |
| `code/guarded_agent.py` | partial | composition wrapper with TODOs (provided plumbing, learner wires the order + fail-closed) |
| `code/datasets/attacks.jsonl` | provided | labeled injection/jailbreak + benign prompts + PII-bearing texts |
| `code/evaluate_guards.py` | provided | scores precision/recall on the dataset (attack-catch rate, benign false-positive rate, PII leak rate) |
| `code/tests/` | provided | offline guiding tests; fail with `NotImplementedError` until cores written |
| `code/.env.example`, `pytest.ini`, `README.md` | provided | setup, one-command run + test |
| `source/lesson.agent.md` | reference | canonical lesson |
| `source/project.md`, `source/rubric.md`, `source/resources.md`, `source/reflection.template.md` | reference | contracts, 5-dim rubric, sources, reflection prompts |
| `rendered/lesson.html` | reference | derived human view (0 stubs) |
| root reflection stubs (`UNDERSTANDING.md`, `FAILURE_ANALYSIS.md`, …) | reference | learner workflow files |

---

## Milestones (4–6)

1. **M1 — Input scan:** heuristic injection/jailbreak detection (instruction-override patterns,
   role-switching, delimiter attacks); return a verdict, don't just bool.
2. **M2 — PII redaction:** detect + mask configured entities on output; preserve meaning.
3. **M3 — Output policy:** schema/allow-list enforcement + a fail-closed refusal path.
4. **M4 — Compose the wrapper:** scan → run → redact → enforce, in the right order, fail-closed.
5. **M5 — Evaluate:** run `evaluate_guards.py`; report attack-catch vs benign false-positive
   tradeoff and PII leak rate; tune the threshold.
6. **Extension:** swap the heuristic scanner for an LLM-judge classifier (Llama-Guard-style)
   and compare; add indirect-injection cases sourced from retrieved docs.

---

## Difficulty Spikes (to call out in the lesson)

1. **Fail-closed vs fail-open.** A guard that errors and passes the input through is worse than
   no guard. Every guard must default to refusal on error.
2. **The precision/recall tradeoff is the lesson.** A guard that blocks everything has 100%
   recall and is useless. The eval must surface the benign false-positive rate.
3. **Indirect injection.** The attack isn't in the user prompt — it's in the retrieved
   document. This is why scanning *only* user input is insufficient (ties back to P04).
4. **Redaction breaks structure.** Masking inside a JSON/tool argument can corrupt it; redact
   at the right layer.

---

## Risks

- **MEDIUM:** heuristic detection is inherently leaky — must be framed as defense-in-depth, not
  a solved problem, or the lesson over-promises. Mitigate by pairing heuristics with the eval
  that shows the gaps.
- **LOW:** Presidio adds a dependency; keep it optional with a regex fallback so the core runs
  offline.
- **LOW (thesis):** must not imply guardrails make a system "safe" — frame as risk reduction.

## Estimated Complexity: **MEDIUM–HIGH** (most original sourcing of the four).
