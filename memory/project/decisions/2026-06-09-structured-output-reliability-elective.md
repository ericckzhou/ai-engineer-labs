# ADR: Add Elective E6 — Structured Output & Reliability

**Date:** 2026-06-09
**Status:** accepted
**Decided by:** Eric (curriculum owner), drafted with Claude

## Context

The core spine (P01–P09) and the Production & Hardening track (E2–E5) cover APIs, tokens/embeddings,
retrieval, RAG, memory, tool use, evaluation, agents, orchestration, guardrails, cost/latency,
observability, and advanced retrieval. One foundational competency is missing and is **silently
depended on** by several existing projects: getting a model to emit **reliable, schema-valid
structured output**.

- P06 (tool use) and P08 (agent) both require well-formed tool arguments, but never teach how to
  *guarantee* them — they assume the model returns valid JSON.
- P07 (evaluation) parses model verdicts; malformed output silently corrupts scores.
- Production failure rate from "the model returned almost-JSON" is high and rarely taught directly.

The gap is not "prompt engineering" (too diffuse, already woven through every project). It is the
specific engineering discipline of **constraining, validating, and repairing** model output against
a schema, and **measuring** the success rate as a first-class metric.

## Options Considered

### Option A: Add as elective E6 (off-spine), non-destructive
Create `projects/electives/06-structured-output-reliability/` mirroring E2–E5. The numbered core
spine (P01–P09) and its capstone narrative are untouched.
Pros: zero renumbering; ships independently; matches the existing "important-but-off-spine"
electives mechanism; reversible (can be promoted to core later).
Cons: a foundational skill lives in the electives, where a linear learner might skip it.

### Option B: Insert into the core spine as P6.5 (renumber P07→P10)
Place it immediately after P06 (tool use), where it is pedagogically ideal.
Pros: a linear learner hits reliability exactly when tool use makes it urgent.
Cons: renumbering P07/P08/P09 rewrites every cross-reference (catalogs, README, concept-map,
memory, the capstone's "P09" identity, internal links). High-churn, hard to reverse, and risks
breaking the validator's catalog-link checks. Disproportionate to the benefit.

### Option C: Append as core P10 (after the capstone)
Keep numbering monotonic by adding it at the end.
Pros: no renumbering; stays "core."
Cons: pedagogically wrong — a foundational reliability primitive taught *after* the P09 capstone
that already depends on it. Breaks the "primitives → composed OS" arc.

## Decision

**Option A.** Add it as **Elective E6 — Structured Output & Reliability**, authored end-to-end to
the same bar as E2–E5 (sources → `lesson.agent.md` → project/rubric/resources/reflection → labeled
code scaffolding + guiding tests → rendered HTML → root reflection stubs), with starters on `main`
(learner core = `NotImplementedError`) and the reference solution on `solns`.

In the concept map and the elective's `PROJECT.md`, mark it **"strongly recommended after P06 (tool
use); do before P08 (agent)"** so a linear learner gets the prerequisite ordering without a spine
renumber.

### Scope of E6 (so authoring is bounded)
- **Core learning target (learner-owned):** a `structured_output.py` that coerces an LLM into a
  validated schema with a **validate → repair → retry** loop, plus `coerce(...)` returning a typed
  result and a measured `success_rate` over N attempts. Offline core runs against a provided fake
  backend that emits realistic malformed outputs (trailing prose, markdown fences, single quotes,
  missing field, wrong type); the live-LLM path is the extension.
- **Provided:** `config.py` (canonical provider block), `schema.py` (the target schemas /
  validators), `fake_backend.py` (deterministic malformed-output fixtures), `evaluate.py`
  (success-rate harness), guiding tests, README, requirements, `.env.example`.
- **Milestones (M1–M5):** M1 parse-or-fail (strict), M2 tolerant extraction (strip fences/prose),
  M3 schema validation (typed, with field-level errors), M4 repair-and-retry loop with a bounded
  attempt budget, M5 measure success rate + the cost/latency of repair (ties to E3).
- **Primary sources to add (real):** Outlines / *Efficient Guided Generation for Large Language
  Models* (Willard & Louf, 2023, arXiv 2307.09702) for constrained decoding; the Anthropic tool-use
  / structured-output official docs for the JSON-mode/function-calling contract. Conform both to the
  canonical source-note schema (Type/Tier/URL/Accessed + Why This Source Matters/Key Claims/Relevant To).

## Tradeoff Accepted

A foundational reliability skill is taught off the numbered spine. We accept this rather than pay
the high, hard-to-reverse cost of renumbering P07–P09. If linear-learner skip rate proves to be a
problem, E6 can be promoted into the core spine as a deliberate, separate renumber pass.

## Consequences

- New directory `projects/electives/06-structured-output-reliability/` and two new source notes.
- `catalogs/concept-map.md`, `README.md` electives table, and `docs/curriculum/overview.md` gain E6.
- The validator's `REQUIRED_PROJECT_FILES` contract applies to E6 unchanged; `render_lessons.py`
  generates its `rendered/lesson.html`; `validate_curriculum.py` must pass.
- Establishes the precedent that **cross-cutting competencies** (reliability, and potentially future
  ones like ingestion or multi-agent) enter as electives with an explicit "recommended ordering"
  rather than via spine renumbers.

## Revisit If

- Linear learners consistently skip E6 and arrive at P08/agent without reliability skills → promote
  to core (renumber).
- A second cross-cutting competency (e.g. Document Ingestion, Multi-Agent Orchestration) is added,
  warranting a named "Foundations & Reliability" track the way E2–E5 form "Production & Hardening".
