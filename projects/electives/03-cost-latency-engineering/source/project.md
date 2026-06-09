# Elective 03: Cost & Latency Engineering

# source/project.md — Detailed Project Specification

> High-level overview: root `PROJECT.md`. Teaching content: `source/lesson.agent.md`.
> This file is implementation contracts, not teaching content.
> **Elective — Production & Hardening track.** Prereq skills: Projects 01, 02, 07.

---

## The One-Sentence Brief

Take a working feature (Project 01/08) that is **correct but expensive**, add three cost levers —
**prompt caching**, a **semantic cache**, and a **model cascade** — and prove on Project 07's
**frozen eval** that you cut cost/latency **without** regressing quality.

---

## Definition of Done

- [ ] `cache.py` implements a **semantic cache**: `lookup` (embed → nearest → threshold gate) and
      `store`; same embedder for both; returns a hit only above `cfg.cache_threshold`.
- [ ] `cascade.py` implements **cheap-first routing**: call the cheap model, accept if the
      escalation signal clears `cfg.cascade_threshold`, else **escalate** to the strong model;
      returns `(text, tier, cost)` with `tier ∈ {cache, cheap, strong}`.
- [ ] `budget.py` `CostTracker` accumulates **real per-call cost** (tier price from the price
      table — no invented prices) and enforces `cfg.budget_ceiling`.
- [ ] The cache + cascade compose: a cache hit returns at ~0 cost and never calls a model.
- [ ] `evaluate_cost.py` runs the frozen eval **baseline (always-strong) vs optimized** and reports
      **quality (pass-rate), cost, latency/calls, and cache-hit rate** for both.
- [ ] Guiding tests pass offline once cores are implemented; fail with `NotImplementedError` on the
      starter.
- [ ] `UNDERSTANDING.md` (before code) states *cost and quality are separate axes* and *why the
      eval is the gate*.
- [ ] `FAILURE_ANALYSIS.md` has ≥3 experiments, **including** a semantic **false hit** (loose
      threshold → wrong cached answer) and a **cascade that never escalates** (ships cheap wrong
      answers).
- [ ] `EVALUATION.md` reports the **frontier**: quality held + cost/latency down, both numbers.
- [ ] `STARCALLOS_REFLECTION.md` names ≥1 concrete repetitive StarcallOS workload these levers make
      affordable, with a mechanism.

---

## File Specification

`code/` provides the **feature/models** and the **evaluator**; the learning target is the
**caching + routing layer**.

### `config.py` — `provided`
Canonical provider block + per-project `Config`: `cheap_model`/`strong_model` ids,
`cheap_price`/`strong_price` (per-call, from the price table), `cache_threshold` (0.83),
`cascade_threshold` (0.6), `budget_ceiling`. The learner reads these; does not hardcode.

### `feature_backend.py` — `reference`
Complete, offline, deterministic stand-ins for the thing being optimized:
- `cheap_answer(query) -> (answer, confidence)` — answers correctly on *easy* eval items, wrongly
  on *hard* ones, with a `confidence` signal the cascade can threshold.
- `strong_answer(query) -> answer` — correct on all eval items (the expensive ground truth).
- `embed(text) -> list[float]` — deterministic local embedder (so cache tests need no provider).
- `cost_of(tier) -> float` — per-call cost from `config` prices.
Does **not** do caching or routing — that's the learner's job.

### `cache.py` — `learner`
```python
class SemanticCache:
    def lookup(self, query: str, *, cfg=...) -> str | None: ...   # embed → nearest → threshold
    def store(self, query: str, answer: str, *, cfg=...) -> None: ...
```
Returns a hit only when top similarity ≥ `cfg.cache_threshold`. (M2)

### `cascade.py` — `learner`
```python
@dataclass
class CascadeResult: text: str; tier: str; cost: float; cache_hit: bool

def answer(query: str, *, cfg=..., cache: SemanticCache | None = None,
           tracker: CostTracker | None = None) -> CascadeResult: ...
```
Order: cache lookup → cheap model → escalate on low confidence → store. Track cost. (M3)

### `budget.py` — `partial`
`CostTracker` with `add(cost)`, `total`, `over_budget(ceiling)` — skeleton + TODOs (M4).

### `eval_set.jsonl` — `provided`
Frozen Project-07-style set: `{"query", "expected", "difficulty": "easy"|"hard"}`. Includes
near-duplicate queries (for cache hits) and distinct ones (to expose false hits).

### `evaluate_cost.py` — `provided`
Runs baseline vs optimized over the eval set; reports quality (pass-rate vs `expected`), total
cost, call count, and cache-hit rate. Prints the frontier side by side.

### `tests/` — `provided`
`test_config.py` (drift), `test_cache.py` (store→exact hit; near-duplicate hit; distinct miss),
`test_cascade.py` (easy→cheap tier; hard→escalate strong; cache hit→tier "cache", cost 0),
`test_budget.py` (accumulate; over-ceiling). Offline; fail with `NotImplementedError` until done.

### `pytest.ini`, `.env.example`, `README.md`, `requirements.txt` — `provided`

---

## Input / Output Contracts

| Function | Input | Output | Error/Edge |
|----------|-------|--------|------------|
| `cache.lookup(query)` | str | cached answer or `None` | below threshold → `None`; empty cache → `None` |
| `cache.store(query, answer)` | str, str | `None` | — |
| `cascade.answer(query)` | str | `CascadeResult(text, tier, cost, cache_hit)` | cache hit → tier "cache", cost 0, no model call |
| `CostTracker.add(cost)` | float | `None` | accumulates |
| `CostTracker.over_budget(ceiling)` | float | bool | total > ceiling → True |

---

## Extended Requirements
- [ ] **Real provider:** flip `feature_backend` to LiteLLM (cheap vs strong model) and re-measure.
- [ ] **Live prompt caching:** add a cached system-prefix call and read `cache_read_input_tokens`.
- [ ] **Batch API** for an offline eval run; compare cost.
- [ ] **Per-route tiering:** route by query class (Project 09 router) to a tier.

---

## Known Difficulty Spikes
1. **The false hit.** A loose `cache_threshold` returns a stored answer for a different query.
   Demonstrate it; tune it; report correctness-under-hits, not hit-rate.
2. **The escalation signal.** Defining "the cheap model wasn't sure" is the real work; a cascade
   that never escalates is just "use the cheap model."
3. **Invented prices.** Cost must trace to `anthropic-pricing.md`. No made-up numbers.
4. **One-sided wins.** A cost number without the paired quality number is incomplete (the gate).

---

## Debugging Approach
1. `python -m pytest` — implement cache → cascade → budget until green.
2. `python evaluate_cost.py` — read quality AND cost. If quality dropped, your threshold/escalation
   is too aggressive.
3. Loosen `cache_threshold` and watch a false hit appear; tighten and watch hits vanish.
4. Source: re-read `source/lesson.agent.md` §3 (the gate), §5 (false hit), §6 (escalation).

---

## Integration Notes
**Depends on:** Project 07 (the eval gate — provided here as `eval_set.jsonl` + a checker),
Project 02 (embeddings — the semantic cache), Project 01/08 (the feature). **Relates to:** Project
09 (per-route tiering), Elective 04 (cost is a telemetry signal worth tracing). Cost optimization
is only safe behind the eval — that dependency is the whole point of the ordering.
