# Elective 06: Structured Output & Reliability

# source/project.md — Detailed Project Specification

> High-level overview: root `PROJECT.md`. Teaching content: `source/lesson.agent.md`.
> Implementation contracts, not teaching content.
> **Elective — Production & Hardening track** (reliability elective). Recommended after P06, before P08.

---

## The One-Sentence Brief

Build the layer that turns a model's flaky **text** into a schema-valid **object** — `extract_json`,
`validate`, and a bounded `coerce` repair loop that **fails closed** — then **measure** the reliability
lift per failure kind against a provided malformed-output backend.

---

## Definition of Done

- [ ] `parse_strict(text)` strictly `json.loads` (M1, the baseline).
- [ ] `extract_json(text)` strips fences/prose and returns the first balanced JSON object; raises
      `ValueError` when there is none (M2).
- [ ] `validate(obj, schema)` returns a list of error strings (`[]` = valid), covering
      missing/required, type (including the `bool`-as-`int` trap), enum, and min/max (M3).
- [ ] `build_repair_prompt(message, bad_output, errors)` includes the message and the specific errors.
- [ ] `coerce(message)` runs extract → validate → repair → retry within `cfg.max_attempts`, repairs with
      the errors, and **raises `StructuredOutputError`** when it can't produce a valid object (M4).
- [ ] Guiding tests pass offline once cores are implemented; fail with `NotImplementedError` on the
      starter.
- [ ] `UNDERSTANDING.md` (before code) names the three failure modes and why extraction ≠ validation,
      and why the layer must fail closed.
- [ ] `FAILURE_ANALYSIS.md` ≥3 experiments, **including** (a) a blind retry (no errors) that fails to
      converge, and (b) the `bool`/`int` trap letting an invalid object through a naive check.
- [ ] `EVALUATION.md` reports success **per failure kind** (clean/fenced/prose/schema/unfixable) and the
      repair cost — including that the unfixable case correctly stays failed.
- [ ] `STARCALLOS_REFLECTION.md` names ≥1 concrete StarcallOS chain where one unreliable hop poisons the
      rest, and how coerce contains it.

---

## File Specification

`code/` provides the **schema, the malformed-output backend, the eval set, and the scorer**; the
learning target is the **reliability core** (`structured_output.py`).

### `config.py` — `provided`
Canonical provider block + `Config`: `max_attempts` (3), `allow_repair` (True), `strict_enum` (True).
Cores read these — do not hardcode the budget.

### `schema.py` — `provided`
The `Ticket` contract as data: `TICKET_SCHEMA` (category enum, priority int 1–5, needs_human bool,
summary str) + the `Ticket` dataclass and `to_ticket`. You validate against this; you don't change it.

### `fake_backend.py` — `reference`
A deterministic offline 'LLM'. `generate(prompt)` returns a case's raw (often malformed) output on the
first call and its repaired output on a later (repair) call — unless the case is `unfixable`. Five
shapes: clean / fenced / prose / schema / unfixable. `reset()` clears per-case counters. The live model
is the extension.

### `structured_output.py` — `learner`
```python
def parse_strict(text) -> dict: ...                              # M1 strict json.loads
def extract_json(text) -> dict: ...                              # M2 strip fences/prose, first {...}
def validate(obj, schema=TICKET_SCHEMA, *, cfg=...) -> list[str] # M3 errors ([] = valid)
def build_repair_prompt(message, bad_output, errors) -> str: ... # M4a
def coerce(message, *, backend=..., schema=..., cfg=...) -> dict # M4 loop, fail closed
class StructuredOutputError(Exception): ...
```

### `eval_set.jsonl` — `provided`
Frozen set: `{"id", "text", "kind", "fixable", "expect_valid"}` across the five failure kinds.

### `evaluate.py` — `provided`
Runs the set; reports, per kind, naive baseline (parses **and** validates) vs the robust coerce loop —
so "how much did the loop actually help" is visible, not assumed.

### `tests/` — `provided`
`test_config.py` (drift), `test_structured_output.py` (M1–M4: extraction strips fences, validation flags
each violation class incl. bool-as-int, coerce repairs a schema violation and fails closed on the
unfixable case). Offline; fail with `NotImplementedError` until done.

### `pytest.ini`, `.env.example`, `README.md`, `requirements.txt` — `provided`

---

## Input / Output Contracts

| Function | Input | Output | Edge |
|----------|-------|--------|------|
| `parse_strict(text)` | str | dict | non-JSON → raises `json.JSONDecodeError` |
| `extract_json(text)` | str | dict (first balanced object) | no object → raises `ValueError` |
| `validate(obj, schema)` | dict, spec | `list[str]` errors (`[]` = valid) | bool where int → an error |
| `coerce(message)` | str | schema-valid dict | budget exhausted → raises `StructuredOutputError` |

---

## Extended Requirements
- [ ] **Live backend:** swap `fake_backend` for a real model (litellm); keep the same loop.
- [ ] **Forced tool schema:** request a tool call with `tool_choice` so the provider returns
      schema-shaped arguments; compare the repair rate.
- [ ] **Guided decoding:** constrain generation to the JSON schema (Outlines-style) so invalid output is
      impossible; measure the drop in repairs.
- [ ] **Streaming + partial validation:** validate as tokens arrive (ties to a streaming elective).

---

## Known Difficulty Spikes
1. **Extraction vs validation.** Keep them separate — a regex never fixes a missing field.
2. **The `bool`/`int` trap.** `isinstance(True, int)` is `True`; check bool before int or invalid
   objects slip through.
3. **Fail closed.** Returning the least-bad object instead of raising inverts the whole point.
4. **Repair with the errors.** Blind retry repeats the mistake; the repair prompt must carry the errors.
5. **Bounded budget.** Cap attempts; unbounded retry is a runaway cost.

---

## Debugging Approach
1. `python -m pytest` — implement M1→M4 until green.
2. `python evaluate.py` — read success **per failure kind**. fenced/prose should be fixed by extraction
   (0 repairs); schema needs one repair; unfixable must stay failed.
3. Disable error feedback in `build_repair_prompt` (return a generic "try again") and watch the schema
   case stop converging — then restore it.
4. Source: re-read `source/lesson.agent.md` §5 (validation/the bool trap), §6 (fail closed).

---

## Integration Notes
**Depends on:** Project 06 (tool use — tools are structured output), Project 01 (model calls).
**Hardens:** P06 (tool arguments), P07 (LLM-judge verdicts), P08 (agent actions), P09 (routing).
**Relates to:** Elective 02 (a validated object is a smaller attack surface than free text), Elective 03
(every repair is a generation — cost/latency), Elective 04 (emit the repair rate as telemetry). The
model is probabilistic; the code that acts on it is deterministic — this layer is the contract between.
