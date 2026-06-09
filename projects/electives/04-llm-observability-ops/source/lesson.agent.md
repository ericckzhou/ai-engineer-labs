# Lesson (Agent Version): Observability & Ops — Watching a System You've Already Shipped

> **Canonical source of truth.** The human version (`rendered/lesson.html`) is derived from this
> file. If they conflict, this file wins.
> **Elective — Production & Hardening track.** Off the numbered 1–9 spine; recommended after P09.
> Prerequisite skills: Projects 07, 08.

---

## Metadata

- **Project:** Elective 04 — LLM Observability & Ops
- **Track:** Production & Hardening (off-spine; after the P09 capstone)
- **Estimated time:** 9–12 hours
- **Prerequisites:** Project 07 (offline eval — the baseline you compare against), Project 08 (the
  agent that emits traces).
- **Instrumented capability:** the Project 08 agent.
- **Primary sources:**
  - `sources/official-docs/opentelemetry-genai-semconv.md` (standard GenAI span attributes)
  - `sources/articles/llm-online-evaluation-drift.md` (online eval; async sampled judge; per-route drift)
  - `sources/papers/mt-bench.md` (score with numbers — now over a live window)

---

## Learning Objectives

By the end of this elective, the learner will be able to:

1. **Distinguish observability from evaluation** — telemetry records *what happened*; evaluation
   decides *whether it was good*; production needs both, continuously.
2. **Emit standard GenAI spans** — instrument a model/tool call with the OpenTelemetry GenAI
   attribute names (`gen_ai.operation.name`, `gen_ai.request.model`, `gen_ai.usage.*`,
   `gen_ai.response.finish_reasons`) and explain why standard names matter.
3. **Instrument an agent run** — wrap model + tool calls so one run produces a span tree with
   latency, tokens, cost, route, and errors.
4. **Aggregate traces into metrics** — roll spans up **per route/operation** (count, error rate,
   latency, tokens, cost).
5. **Detect drift** — compare a live window to a baseline and flag the route/metric that regressed,
   **per segment, not on a global mean**.
6. **Explain the online-eval loop** — why a production LLM-judge samples ~5–10% of traffic
   **asynchronously** and never runs synchronously on the request path; how offline + online evals
   combine.

---

## 1. Motivation

### Why this exists

In Project 07 you evaluated your system **offline**, before shipping: a frozen set, a judge, a
pass-rate. That catches the regressions you can anticipate. Then you ship — and the real world
sends queries your frozen set never imagined, a provider silently changes a model, a retrieved
corpus drifts, and one route quietly starts failing. Your offline eval, run last Tuesday, says
nothing about *right now*.

This elective builds the missing half: **observability** (record what the live system did, in a
standard format) plus **online evaluation** (continuously judge whether it's still good). It
closes the loop Project 07 left open — offline → online.

### What breaks without it

Without it, your first sign of a production regression is an angry user, not a dashboard. You can't
answer "is it slower than last week?", "which route is failing?", or "did quality drift after the
model update?" — because you never recorded the run in a queryable way, and nothing is scoring live
traffic. A system you can't see is a system you can't operate.

> **Startup lens (StarcallOS).** A personal OS runs unattended, all day. The only way to trust an
> unattended system is to instrument it: every model call, tool call, route, cost, and error as a
> standard span, plus a background judge sampling quality. Observability is how StarcallOS earns
> the right to run without you watching.

---

## 2. ELI12

Imagine a restaurant kitchen. **Observability** is the camera over every station: it records who
cooked what, how long each dish took, and which orders came back. It tells you *exactly what
happened* — but a camera can't taste the food. So you also send a **food critic** to taste a few
random plates each night (not every plate — that would jam the kitchen). The critic tells you
*whether the food is still good.* You need both: the cameras to see the speed and the mistakes, the
critic to judge the taste.

And the golden rule of the cameras: **a single average lies.** "Average dish time: 8 minutes"
looks fine even if the dessert station is secretly taking 40. You have to watch **each station**,
not just the kitchen's average. That per-station view is the whole trick of drift detection.

---

## 3. Observability vs. Evaluation

These are different jobs and the lesson hinges on not conflating them
(`opentelemetry-genai-semconv.md`):

- **Observability** = *what happened*. Latency, tokens, cost, route, error, finish reason — recorded
  on every request, cheaply, as structured **traces**.
- **Evaluation** = *was it good*. A judged quality score — expensive, so run on a **sample**, not
  every request.

A trace can tell you latency doubled; it cannot tell you the answers got worse. A judge can tell you
quality dropped; it's too costly to run on everything. Production needs both, and they share fields:
the trace preserves the context (prompt, retrieved docs, response) the judge needs to score.

---

## 4. GenAI Telemetry — Spans with Standard Names

A **span** is a record of one operation (a model call, a tool call) with a start, a duration, and
**attributes**. OpenTelemetry's GenAI semantic conventions standardize the attribute *names* so any
tool can read any system's traces (`opentelemetry-genai-semconv.md`). The ones that matter here:

| Attribute | Meaning |
|-----------|---------|
| `gen_ai.operation.name` | the operation (e.g. `chat`, `execute_tool`) |
| `gen_ai.request.model` | the model requested |
| `gen_ai.usage.input_tokens` / `gen_ai.usage.output_tokens` | token usage |
| `gen_ai.response.finish_reasons` | why generation stopped |

The point of using the **standard** names (not `my_model` or `tokens_in`) is interoperability: a
trace written to the convention can be read by any conforming backend, compared across models,
prompts, and deployments. Inventing your own names throws that away — the whole reason the
convention exists.

---

## 5. Instrumenting the Agent

Instrumentation wraps each operation so it emits a span. A `traced` wrapper around a model/tool call
records the **duration** (wall-clock), pulls **tokens/cost** from the result, tags the **route** and
**operation**, captures any **error**, and appends the span to a collector/exporter. One agent run →
a **tree of spans** (the top-level run, each model call, each tool call). The learner owns building
the span with the correct attributes; the exporter (where spans go) is provided.

A key discipline: an **error is a span attribute, not a swallowed exception.** A tool that fails
records `error=true` on its span — that's how the monitor later sees the error-rate rise. (This is
the telemetry echo of Project 08's "the error must become an observation.")

---

## 6. Aggregating Traces into Metrics — Per Route

Raw spans are noise; **metrics** are signal. Aggregation rolls spans up **per route/operation** into:
count, **error rate**, average **latency**, average **tokens**, total **cost**. The non-negotiable
design choice is the *grouping*: per route, **not** one global average. A global mean is where a
dead route hides — "overall error rate 3%" can conceal a `search` route at 60%. (Same trap Project
09 names for routing accuracy; same fix — segment it.)

---

## 7. Drift Detection — Baseline vs. Live Window

**Drift** is the live system moving away from a known-good **baseline**. The monitor compares a
recent **window** of metrics to the baseline, per route, and **flags** a route whose error rate rose
beyond a threshold, or whose latency rose beyond a ratio, or whose cost/tokens spiked
(`llm-online-evaluation-drift.md`). Three flavors:

- **Operational drift** — error rate, latency, cost per route.
- **Behavioral drift** — refusal-rate spikes, retry storms, malformed-output rate.
- **Distributional drift** — the *input* distribution moving off the golden set's coverage (queries
  you never evaluated) — often the earliest warning, *before* failures climb.

The alert threshold is the familiar precision/recall dial: too tight ⇒ alert fatigue; too loose ⇒
missed regressions. The monitor's job is to catch the seeded regression **without** crying wolf on a
healthy window.

---

## 8. Online Evaluation — The Async Sampled Judge

Telemetry is cheap and runs on everything. *Quality* scoring is expensive, so online evaluation
**samples** — a background LLM-judge grades ~5–10% of traffic against the **same rubric** the
offline eval used (`llm-online-evaluation-drift.md`). The load-bearing rule:

> **A production judge must NOT run synchronously on the request path.** That doubles latency and
> cost for every user. It runs **asynchronously**, over sampled traces, feeding a quality dashboard.

This is how offline and online evals combine: offline gates the release (Project 07); online watches
the deployment (this elective). Together they're worth more than either alone.

---

## Milestones

1. **M1 — Emit a span:** wrap a model call in a GenAI span with the standard attributes; verify via
   the exporter.
2. **M2 — Instrument the agent:** `traced` across model + tool calls; one run → a span tree;
   errors recorded as attributes.
3. **M3 — Aggregate:** roll spans up into **per-route** metrics (count, error rate, latency, tokens,
   cost).
4. **M4 — Detect drift:** compare a window to the baseline per route; flag the regressed route
   without false-alarming the healthy one.
5. **M5 — Evaluate the monitor:** run the fixtures; catch the seeded regression, no false alarm on
   the baseline.
6. **Extension:** wire a real OTel collector / dashboard; add an async sampled LLM-judge for quality
   drift.

---

## Common Misconceptions

- **"Observability is evaluation."** No — a trace says latency rose; it doesn't say quality dropped.
  You need a judge for that.
- **"I'll name the attributes whatever."** Then no standard tool can read your traces. Use the
  `gen_ai.*` names; interoperability is the point.
- **"Watch the overall average."** A global mean hides a single dead route. Aggregate per route.
- **"Score every request for quality."** A synchronous production judge doubles latency/cost. Sample
  ~5–10% asynchronously.
- **"Swallow the tool error so the run continues."** Then the monitor never sees it. The error is a
  span attribute.

---

## Instructor Notes

- The **non-negotiable assessable idea** is *observability ≠ evaluation* — and that drift is detected
  **per route, not on a global mean**. A monitor that only reports an overall average has missed the
  point.
- The **second** is *standard attribute names*: inventing field names defeats interoperability.
- The **third** is the *async sampled judge*: a synchronous production judge is the named
  anti-pattern.
- Keep it offline/deterministic: a provided exporter stub + replayable trace fixtures (a baseline +
  a seeded-regression window) make the monitor a gradeable artifact with no live system.
- Scope guard: the target is the instrumentation + the drift monitor, **not** building a dashboard
  (that's an extension).

---

## Sources

- `sources/official-docs/opentelemetry-genai-semconv.md` — standard GenAI span attributes; tools
  agree on field names; observability supports but is separate from evaluation.
- `sources/articles/llm-online-evaluation-drift.md` — online vs offline eval; async sampled judge
  (~5–10%, never synchronous); operational/behavioral/distributional drift; per-route aggregation.
- `sources/papers/mt-bench.md` — scoring with numbers, applied to a live window per route.
