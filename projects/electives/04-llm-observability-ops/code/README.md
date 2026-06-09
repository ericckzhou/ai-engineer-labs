# Elective 04 — LLM Observability & Ops (code)

Instrument an agent with **standard GenAI telemetry**, then build a **per-route drift monitor**
over live traces — closing Project 07's offline→online loop. The agent, exporter, and trace
fixtures are provided; **you build `tracing.py` and `monitor.py`.**

> Brief: `../source/project.md` · Lesson: `../source/lesson.agent.md` · Rubric: `../source/rubric.md`.
> Do `../UNDERSTANDING.md` **before** coding.

## Setup (offline — no API key)

```bash
python -m venv .venv && .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m pytest
```

`test_config.py` passes; the rest fail with `NotImplementedError` until you implement, in order:

| Milestone | File / symbol | Tests |
|-----------|---------------|-------|
| M1 span | `tracing.build_span` | `tests/test_tracing.py` |
| M2 instrument | `tracing.traced` | `tests/test_tracing.py` |
| M3 aggregate | `monitor.aggregate` | `tests/test_monitor.py` |
| M4 drift | `monitor.detect_drift` | `tests/test_monitor.py` |

## Run the monitor

```bash
python evaluate_monitor.py
```

Must **flag the `search` route** (seeded error+latency regression) and report **0 false alarms**
on baseline-vs-baseline.

## File roles

| File | Role |
|------|------|
| `config.py` | provided — drift thresholds |
| `agent_backend.py` | reference — agent to instrument |
| `exporter.py` | provided — `SpanCollector` (the OTel exporter stand-in) |
| `tracing.py` | **learner** — `build_span`, `traced` |
| `monitor.py` | **learner** — `aggregate`, `detect_drift` |
| `fixtures/*.jsonl` | provided — baseline + seeded-regression spans |
| `evaluate_monitor.py` | provided — the detection scorer |
| `tests/` | provided |

## The rules that matter most

**Observability ≠ evaluation** (a trace shows latency, not quality). **Aggregate per route, not a
global mean** (a healthy average hides a dead route). **An error is a span attribute, not a
swallowed exception.**
