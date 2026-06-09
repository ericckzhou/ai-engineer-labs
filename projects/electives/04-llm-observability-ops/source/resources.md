# Resources — Elective 04: LLM Observability & Ops

> Curated reading. Truth lives in `sources/`. Read in order.

## Read first — the vocabulary
1. **OpenTelemetry GenAI semantic conventions** — `sources/official-docs/opentelemetry-genai-semconv.md`.
   The standard span attribute names (`gen_ai.operation.name`, `gen_ai.request.model`,
   `gen_ai.usage.*`, `gen_ai.response.finish_reasons`). Why standard names = interoperability.

## Read second — the loop
2. **Online evaluation & drift** — `sources/articles/llm-online-evaluation-drift.md`. Offline vs
   online; the **async sampled judge** (~5–10%, never synchronous); operational/behavioral/
   distributional drift; **per-route** aggregation.
3. **MT-Bench (P07)** — `sources/papers/mt-bench.md`. Score with numbers — now over a live window,
   per route, not a single answer.

## Carried from prior projects
- **Project 08** — `react-paper.md`: "the error must become an observation" — here it becomes a span
  attribute the monitor can see.
- **Project 09** — `building-effective-agents.md`: the per-route (not global mean) discipline, now
  for drift instead of routing accuracy.

## How sources map to code
| Source | Code |
|--------|------|
| OTel GenAI semconv | `tracing.build_span` (M1–M2) |
| online-eval/drift | `monitor.detect_drift` (M4), async judge (extension) |
| MT-Bench | per-route metrics / the sampled judge |

## Out of scope
- **Building a dashboard / full collector infra** — an extension; the target is the instrumentation
  + drift logic.
- **APM for non-LLM services** — real but a different discipline; here the spans are GenAI operations.
