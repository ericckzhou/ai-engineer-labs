# Online Evaluation & Drift Monitoring for LLM Systems (industry practice)

**Type:** article (synthesized industry best-practice; multiple practitioner sources)
**Tier:** 3 (Engineering Guide)
**URL:** https://langfuse.com/blog/2025-03-04-llm-evaluation-101-best-practices-and-challenges
**Accessed:** 2026-06-09
**Primary references:**
- Langfuse — "LLM Evaluation 101: Best Practices and Challenges" — https://langfuse.com/blog/2025-03-04-llm-evaluation-101-best-practices-and-challenges
- Databricks — "Best Practices and Methods for LLM Evaluation" — https://www.databricks.com/blog/best-practices-and-methods-llm-evaluation
- VentureBeat — "Monitoring LLM behavior: Drift, retries, and refusal patterns" — https://venturebeat.com/infrastructure/monitoring-llm-behavior-drift-retries-and-refusal-patterns

> Primary source for **Elective 04 — Observability & Ops** (the online-evaluation / drift-monitor
> half). Pairs with `sources/official-docs/opentelemetry-genai-semconv.md` (the telemetry
> vocabulary) and `sources/papers/mt-bench.md` (score-with-numbers, now over a live window).
> Synthesis of converging industry practice; the linked posts are the references.

---

## The core distinction (carried from the concept map)

**Observability records what happened; evaluation decides whether it was good.** A trace tells you
latency rose and tokens grew; it does not tell you the *answers* got worse. Production needs both:
cheap telemetry on every request, plus sampled quality evaluation.

## Offline vs. online evaluation — the loop

- **Offline eval** (Project 07): a frozen set, scored before shipping, to catch regressions.
- **Online eval**: runs **continuously in production** to surface drift and failure modes the
  frozen set never anticipated. The two together are worth more than either alone — offline gates
  the release, online watches the deployment.

## How online evaluation is run in practice

- **Establish a baseline** from initial deployment, then **continuously compare** live behavior
  against it.
- **Sample, don't grade everything.** A background **LLM-judge asynchronously samples ~5–10%** of
  traffic and grades it against the *same rubric* the offline eval used. Critically, the judge
  **must not run synchronously on the request path** — that doubles latency and cost. Quality
  scoring is a background job over sampled traces, not a gate on every response.
- **Reuse offline asserts online.** The pass/fail checks from the offline suite can score sampled
  production traffic; a spike in malformed-output rate is the earliest warning of drift.

## What a trace contains (the unit of monitoring)

A trace records *everything the system did* to produce a response: the user query, retrieved
documents with relevance scores and source ids, tool calls with arguments and results, the
assembled prompt, and the model's response — plus latency, tokens, cost, and finish reason. This
is exactly what the OTel GenAI conventions standardize so tools agree on the field names.

## Drift detection strategies

- **Operational drift:** error rate, latency, token/cost per route trending off the baseline.
- **Behavioral drift:** refusal-rate spikes, retry storms, malformed-output rate.
- **Distributional drift:** the **input embedding distribution** moving away from the golden set's
  coverage — queries arriving that the system was never evaluated on — often *before* failure
  rates climb.

## The monitoring principle that mirrors P09

Aggregate **per route / per operation, not as one global mean.** A healthy overall average can
hide a single route that has silently gone to a 0% pass-rate or a 10× latency — the same trap
Project 09 names for routing accuracy. Drift detection must be per-segment.

## Why This Source Matters

It is the "decide whether it was good, continuously" half that the OTel telemetry ("record what
happened") cannot provide alone. The learner builds a monitor that aggregates spans per route and
flags the route that regressed against a baseline — the smallest real online-eval loop.

## Key Claims

- Observability records what happened; evaluation decides whether it was good — production needs both: cheap telemetry on every request plus sampled quality evaluation.
- Online evaluation runs a background LLM judge over ~5–10% sampled traffic against the *same* offline rubric; it must not run synchronously on the request path (doubles latency and cost).
- Drift is operational (error/latency/cost), behavioral (refusal spikes, retry storms, malformed output), and distributional (input-embedding shift) — and must be aggregated per route, never as one global mean that hides a regressed segment.

## Relevant To

- Elective 04 — Observability & Ops (the online-evaluation / drift-monitor half).
- Related: opentelemetry-genai-semconv.md (the telemetry vocabulary), mt-bench.md (scoring with numbers over a live window), Project 07 (offline eval), Project 09 (per-route aggregation).

## Known issues / cautions

- A synchronous production judge is an anti-pattern (latency/cost); sample asynchronously.
- Drift detection on a global mean hides per-route failure; segment it.
- An alert threshold too tight = alert fatigue; too loose = missed regressions (the same
  precision/recall dial as Electives 02/03).
