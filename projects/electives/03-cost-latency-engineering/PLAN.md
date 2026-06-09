# Elective 03: Cost & Latency Engineering — Implementation Plan

> **Status: PLANNED — awaiting approval before authoring.**
> `/plan` output (Workflow A, pre-execution). No `source/`, `code/`, or `rendered/` yet.
> **Track:** Production & Hardening (named elective track, recommended after the P09 capstone;
> off the numbered 1–9 spine). See `memory/project/decisions/2026-06-09-production-hardening-elective-track.md`.

---

## Requirements Restatement

Take a working LLM feature (Project 01 chatbot or Project 08 agent) that is **correct but
expensive and slow**, and cut its cost and latency **without regressing quality** — using the
Project 07 evaluation harness as the no-regression gate. The learner adds:

- **Prompt caching** (reuse a stable prefix across calls).
- **A semantic cache** (return a stored answer for a semantically-equivalent query).
- **A model cascade** (cheap model first; escalate to a stronger model only on low confidence).

The thesis: *correctness and cost are separate axes, and you can only optimize cost safely if
you already have an eval that proves you didn't break correctness.* This is why it comes after
Project 07.

---

## Where It Fits / Prerequisites

- **Prereqs:** Project 01 (the feature), Project 07 (the eval + judge used as the gate),
  Project 02 (embeddings — the semantic cache is a similarity lookup).
- **Slot:** after Project 07. It consumes P07's frozen eval set directly.

---

## Learning Target (the incomplete core)

The learner owns the **caching + routing layer** wrapped around the model call — not the model
call or the eval.

```
cache.py            (learner)
  semantic_lookup(query, threshold) -> hit | None   # embed -> nearest -> threshold gate
  store(query, answer)
cascade.py          (learner)
  answer(query) -> (response, tier, cost)           # cheap tier -> confidence check -> escalate
budget.py           (partial)
  CostTracker        # accumulate per-call cost; enforce a ceiling (reuse P08 budget pattern)
```

Provided: the feature, P07's eval set + judge, a cost model (per-MTok from
`sources/official-docs/anthropic-pricing.md` — do **not** invent prices), and prompt-caching
plumbing. Incomplete: the cache key/threshold logic, the cascade escalation decision, and the
budget accounting.

---

## Primary Sources to Gather (Workflow A step 1)

| Source | Anchors | Status |
|--------|---------|--------|
| **Anthropic prompt caching** (official docs) | prefix caching mechanics, cache-write vs cache-read pricing, TTL | ⏳ fetch & verify (real docs) |
| **FrugalGPT** — Chen, Zaharia, Zou 2023 (arXiv:2305.05176) | LLM cascade: cheap→expensive, query-adaptive routing, cost vs accuracy frontier | ⏳ fetch & verify |
| **Semantic caching** — GPTCache (docs/paper) | embedding-similarity cache, eviction, hit/miss eval | ⏳ fetch & verify |
| **Anthropic pricing** | the cost model — **already in `sources/official-docs/anthropic-pricing.md`** | ✅ in repo |

→ New sources land in `sources/official-docs/` (prompt caching, GPTCache) and
`sources/papers/` (FrugalGPT). Update `catalogs/source-map.md` + re-render.

---

## File Manifest

| File | Role | Purpose |
|------|------|---------|
| `code/config.py` | provided | provider block + tiers (cheap/strong model ids), cache threshold, budget ceiling |
| `code/feature_backend.py` | reference | the capability being optimized (condensed P01/P08), offline-capable |
| `code/cache.py` | **learner** | semantic cache: embed → nearest → threshold gate → store |
| `code/cascade.py` | **learner** | cheap-first routing with a confidence-based escalation decision |
| `code/budget.py` | partial | `CostTracker` with TODOs (P08 pattern reused; accounting is the gap) |
| `code/eval_set.jsonl` | provided | P07's frozen eval set (the no-regression gate) |
| `code/evaluate_cost.py` | provided | runs the eval; reports quality (judge pass-rate) **and** cost/latency, baseline vs optimized |
| `code/tests/` | provided | offline tests; cache hit/miss, cascade tiering, budget enforcement |
| setup files (`.env.example`, `pytest.ini`, `README.md`) | provided | one-command run + test |
| `source/*`, `rendered/lesson.html`, root stubs | reference | lesson, contracts, rubric, HTML |

---

## Milestones (4–6)

1. **M1 — Prompt caching:** identify the stable prefix; measure cache-read savings on repeat calls.
2. **M2 — Semantic cache:** embed query → nearest stored → threshold gate; tune the threshold
   (too loose = wrong-answer hits; the failure mode).
3. **M3 — Model cascade:** answer with the cheap tier; define a confidence signal; escalate only
   when it's low.
4. **M4 — Budget:** accumulate real cost per call; enforce a ceiling.
5. **M5 — Prove it:** run `evaluate_cost.py` — quality must hold (P07 gate) while cost/latency
   drop; report the frontier.
6. **Extension:** batch API for offline workloads; cache invalidation strategy; per-route tiering.

---

## Difficulty Spikes

1. **The semantic cache's false-hit is the danger.** A too-loose threshold returns a stored
   answer for a *different* question. The eval must catch this, not just measure hit rate.
2. **Cost is meaningless without the quality gate.** "10× cheaper" is a regression if pass-rate
   dropped. The whole point of sequencing after P07.
3. **Don't invent prices.** Cost ceilings and savings use the real per-MTok table only
   (`anthropic-pricing.md`); a fabricated price invalidates the whole exercise.
4. **Confidence signals are imperfect.** Defining "the cheap model wasn't sure" is the hard
   design decision (logprobs/self-report/judge) — keep it the learner's call.

---

## Risks

- **MEDIUM:** real latency/cost numbers vary by provider and network; keep the demo offline-
  deterministic with a cost *model* so results are reproducible, and mark live numbers as
  illustrative.
- **LOW:** prompt-caching specifics are provider-dependent; teach the principle, show the
  Anthropic mechanics as the concrete instance.

## Estimated Complexity: **MEDIUM** (leans on existing P02 embeddings + P07 eval).
