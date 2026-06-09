# Elective 04: LLM Observability & Ops

# source/project.md — Detailed Project Specification

> High-level overview: root `PROJECT.md`. Teaching content: `source/lesson.agent.md`.
> Implementation contracts, not teaching content.
> **Elective — Production & Hardening track.** Prereq skills: Projects 07, 08.

---

## The One-Sentence Brief

Instrument the Project 08 agent with **standard GenAI telemetry** (OpenTelemetry `gen_ai.*` spans),
then build an **online monitor** that aggregates live traces **per route** and **flags drift**
against a baseline — closing the offline→online loop Project 07 left open.

---

## Definition of Done

- [ ] `tracing.py` builds spans with the **standard** GenAI attribute names
      (`gen_ai.operation.name`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`/`output_tokens`,
      `gen_ai.response.finish_reasons`) plus latency/route/cost/error.
- [ ] A `traced` wrapper instruments model + tool calls; one agent run → a span tree; a failing
      operation records `error=true` (not a swallowed exception).
- [ ] `monitor.aggregate` rolls spans up **per route/operation** into count, error rate, avg
      latency, avg tokens, total cost — **not** a single global mean.
- [ ] `monitor.detect_drift` compares a window to the baseline **per route** and flags the regressed
      route(s) without false-alarming a healthy window.
- [ ] `evaluate_monitor.py` runs the replayable fixtures (baseline + seeded-regression window) and
      shows the monitor catches the regression and stays quiet on the baseline.
- [ ] Guiding tests pass offline once cores are implemented; fail with `NotImplementedError` on the
      starter.
- [ ] `UNDERSTANDING.md` (before code) states *observability ≠ evaluation* and *why drift is
      per-route, not a global mean*.
- [ ] `FAILURE_ANALYSIS.md` ≥3 experiments, **including** a **global-mean blind spot** (a dead route
      hidden by the average) and a **swallowed error** (a tool error not recorded → monitor blind).
- [ ] `EVALUATION.md` reports the monitor's detection on the fixtures (caught regression; no false
      alarm) and one threshold-tuning move.
- [ ] `STARCALLOS_REFLECTION.md` names ≥1 concrete capability StarcallOS must trace to run
      unattended, with the mechanism.

---

## File Specification

`code/` provides the **agent**, the **exporter**, and the **trace fixtures**; the learning target is
the **span construction** and the **drift monitor**.

### `config.py` — `provided`
Canonical provider block + `Config`: `service_name`, drift thresholds (`error_rate_delta` 0.20,
`latency_ratio` 1.5, `cost_ratio` 1.5), `sample_rate` (0.10). The cores read these.

### `agent_backend.py` — `reference`
A condensed Project-08 agent whose model/tool calls can be instrumented. Offline/deterministic;
some calls deliberately error so a span can carry `error=true`.

### `exporter.py` — `provided`
`SpanCollector`: `.add(span)`, `.spans`, `.to_jsonl(path)`, `.from_jsonl(path)`. The OTel "exporter"
stand-in — spans go here (in-memory + a local file), no collector infra needed.

### `tracing.py` — `learner`
```python
def build_span(operation, *, model, route, input_tokens, output_tokens,
               finish_reason, latency_ms, cost=0.0, error=False) -> dict:
    """Return a span dict keyed by the STANDARD gen_ai.* attribute names (+ latency/route/cost/error)."""

def traced(operation, route, *, collector): ...   # wrap a call: time it, build the span, collect it
```
(M1–M2)

### `monitor.py` — `learner`
```python
@dataclass
class RouteMetrics: count:int; error_rate:float; avg_latency_ms:float; avg_tokens:float; total_cost:float

def aggregate(spans: list[dict]) -> dict[str, RouteMetrics]:   # keyed by route (M3)

@dataclass
class Alert: route:str; metric:str; baseline:float; current:float

def detect_drift(current, baseline, *, cfg) -> list[Alert]:    # per route, vs thresholds (M4)
```

### `fixtures/baseline.jsonl`, `fixtures/window_regressed.jsonl` — `provided`
Replayable spans. Baseline = healthy across routes (`chat`, `search`, `tool`). Window = one route
(`search`) with a spiked error rate + latency. So the monitor has a known regression to catch and a
clean baseline to stay quiet on.

### `evaluate_monitor.py` — `provided`
Loads the fixtures, aggregates both, runs `detect_drift`, prints alerts; also runs
`detect_drift(baseline, baseline)` to show **no false alarm**.

### `tests/` — `provided`
`test_config.py` (drift), `test_tracing.py` (span has the standard keys; `traced` records latency +
route + error), `test_monitor.py` (aggregate per-route metrics; detect_drift flags `search`, not
`chat`; baseline-vs-baseline → no alerts). Offline; fail with `NotImplementedError` until done.

### `pytest.ini`, `.env.example`, `README.md`, `requirements.txt` — `provided`

---

## Input / Output Contracts

| Function | Input | Output | Edge |
|----------|-------|--------|------|
| `build_span(...)` | call facts | span dict with `gen_ai.*` keys | error=True sets the error attribute |
| `traced(op, route, collector)(fn)` | a callable | wrapped callable that emits a span | exception → span `error=true`, then re-raise or record |
| `aggregate(spans)` | list[span] | `{route: RouteMetrics}` | empty → `{}` |
| `detect_drift(current, baseline, cfg)` | two metric maps | `[Alert,...]` | a route only in current vs baseline handled gracefully |

---

## Extended Requirements
- [ ] Wire a **real OTel collector** / a live dashboard.
- [ ] Add an **async sampled LLM-judge** (~`cfg.sample_rate`) scoring quality drift, not just ops.
- [ ] **Distributional drift:** track input-embedding distance from the golden set.

---

## Known Difficulty Spikes
1. **Global-mean blindness.** Aggregating across routes hides the dead one. Per route, always.
2. **Standard names.** `tokens_in` instead of `gen_ai.usage.input_tokens` breaks interoperability.
3. **Swallowed errors.** A tool error not written to the span makes the monitor blind — record it.
4. **Threshold tuning.** Too tight = false alarms on the baseline; too loose = misses the regression.

---

## Debugging Approach
1. `python -m pytest` — implement tracing → aggregate → detect_drift until green.
2. `python evaluate_monitor.py` — does it flag `search` and stay quiet on baseline-vs-baseline?
3. Collapse aggregation to a global mean and watch the regression disappear (then restore).
4. Source: re-read `source/lesson.agent.md` §6 (per route), §7 (drift), §8 (async judge).

---

## Integration Notes
**Depends on:** Project 08 (the instrumented agent), Project 07 (the baseline/eval discipline).
**Relates to:** Elective 02 (a guard refusal is a traced event), Elective 03 (cost is a span
attribute), Project 09 (per-route, not global — the same anti-mean lesson). Observability records
what happened; evaluation decides if it was good — this elective builds the first and samples the
second.
