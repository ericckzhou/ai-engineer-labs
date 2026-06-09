# Elective 04: LLM Observability & Ops — Implementation Plan

> **Status: PLANNED — awaiting approval before authoring.**
> `/plan` output (Workflow A, pre-execution). No `source/`, `code/`, or `rendered/` yet.
> **Track:** Production & Hardening (named elective track, recommended after the P09 capstone;
> off the numbered 1–9 spine). See `memory/project/decisions/2026-06-09-production-hardening-elective-track.md`.

---

## Requirements Restatement

Instrument an existing agent (Project 08) with **standardized GenAI telemetry** (OpenTelemetry
GenAI semantic conventions — spans + attributes per call/tool/run), then build an **online
monitor** that detects **drift / regression over live traces** against a baseline. This closes
the loop Project 07 left open: P07 evaluates **offline** before ship; this evaluates the system
**online** after ship.

The thesis: *observability records what happened; evaluation decides whether it was good — and
in production you need both, continuously, not once.* (This distinction is already stated in
`catalogs/concept-map.md` under Agent Observability.)

---

## Where It Fits / Prerequisites

- **Prereqs:** Project 07 (offline eval — the baseline being compared against), Project 08 (the
  agent emitting traces).
- **Slot:** after Project 08, alongside Project 07. The repo already anchors this with
  `sources/official-docs/opentelemetry-genai-semconv.md` — the elective makes it concrete.

---

## Learning Target (the incomplete core)

The learner owns the **instrumentation + the online monitor** — not the agent.

```
tracing.py          (learner)
  trace_call(span_kind, attrs)        # emit GenAI spans: gen_ai.request.model, usage tokens, tool name…
  @traced                              # decorator wrapping a model/tool call into a span
monitor.py          (learner)
  aggregate(traces) -> Metrics         # per-route/per-tool: latency, tokens, cost, error rate
  detect_drift(window, baseline) -> Alerts   # flag a metric/route that regressed vs baseline
```

Provided: the agent, an OTel exporter/collector stub (writes spans to a local file/in-memory),
a **replayable trace fixture** (so the monitor is testable offline), and P07's baseline. The
span-attribute mapping and the drift logic are incomplete.

---

## Primary Sources to Gather (Workflow A step 1)

| Source | Anchors | Status |
|--------|---------|--------|
| **OpenTelemetry GenAI semantic conventions** | the standard span/attribute names (`gen_ai.*`), what to record per call/tool | ✅ **already in `sources/official-docs/opentelemetry-genai-semconv.md`** |
| **Online evaluation / production monitoring** reference (e.g. an LLM-ops guide on drift + online eval) | continuous eval over live traffic, drift detection, sampling | ⏳ fetch & verify |
| **MT-Bench** — already in repo | scoring-with-numbers, now applied to a live window, per-route | ✅ in repo (`sources/papers/mt-bench.md`) |

→ One new source likely in `sources/articles/`. Update `catalogs/source-map.md` + re-render.

---

## File Manifest

| File | Role | Purpose |
|------|------|---------|
| `code/config.py` | provided | provider block + telemetry settings (service name, exporter path, sampling) |
| `code/agent_backend.py` | reference | condensed P08 agent that will be instrumented |
| `code/tracing.py` | **learner** | GenAI span emission + the `@traced` wrapper |
| `code/monitor.py` | **learner** | aggregate traces → metrics; detect per-route/per-metric drift |
| `code/exporter.py` | provided | OTel exporter/collector stub → local spans file (offline) |
| `code/fixtures/traces.jsonl` | provided | replayable baseline + a regressed window for the monitor to catch |
| `code/evaluate_monitor.py` | provided | scores the monitor: does it flag the seeded regression without false alarms on the baseline? |
| `code/tests/` | provided | offline tests for span attributes + drift detection |
| setup files | provided | one-command run + test |
| `source/*`, `rendered/lesson.html`, root stubs | reference | lesson, contracts, rubric, HTML |

---

## Milestones (4–6)

1. **M1 — Emit spans:** wrap a model call in a GenAI span with the standard attributes
   (model, input/output tokens, latency); verify via the exporter file.
2. **M2 — Instrument the agent:** `@traced` across model + tool calls; one run → a span tree.
3. **M3 — Aggregate:** roll spans up into per-route/per-tool metrics (latency, tokens, cost,
   error rate).
4. **M4 — Detect drift:** compare a window to the baseline; flag the regressed route/metric
   (per-route, not a single mean — mirrors P09's "an overall mean hides a 0% route").
5. **M5 — Evaluate the monitor:** run `evaluate_monitor.py` on the fixtures; catch the seeded
   regression, no false alarm on the baseline.
6. **Extension:** wire to a real OTel collector / a live dashboard; add online LLM-judge sampling.

---

## Difficulty Spikes

1. **Observability ≠ evaluation.** A trace tells you latency went up; it doesn't tell you the
   answers got worse. The monitor must combine telemetry (cheap, every request) with sampled
   eval (expensive, a subset).
2. **A mean hides a dead route.** Drift must be per-route/per-tool, not a global average — the
   same trap called out in Project 09.
3. **Standard attribute names matter.** Inventing `my_model_field` instead of
   `gen_ai.request.model` defeats interoperability — the point of using the semconv.
4. **Testability.** Online systems are hard to test; the replayable trace fixture is what makes
   the monitor an offline, gradeable artifact.

---

## Risks

- **MEDIUM:** scope creep toward "build a dashboard." Keep the learning target the
  instrumentation + drift logic; a dashboard is an extension, not the core.
- **LOW:** OTel SDK surface is large; provide the exporter stub so the learner writes attributes,
  not collector plumbing.

## Estimated Complexity: **MEDIUM** (one source already in repo; strong reuse of P07/P08).
