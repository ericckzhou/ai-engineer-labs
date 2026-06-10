# Elective 06 — Structured Output & Reliability (code)

Turn flaky model **text** into a trustworthy, schema-valid **object**. You build the reliability core
in `structured_output.py` — `parse_strict`, `extract_json`, `validate`, `build_repair_prompt`, and the
`coerce` loop. The schema, the malformed-output backend, the eval set, and the scorer are provided.

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
| M1 strict parse | `structured_output.parse_strict` | `tests/test_structured_output.py` |
| M2 tolerant extract | `structured_output.extract_json` | `tests/test_structured_output.py` |
| M3 schema validate | `structured_output.validate` | `tests/test_structured_output.py` |
| M4 repair + coerce loop | `structured_output.build_repair_prompt`, `coerce` | `tests/test_structured_output.py` |

## Prove the reliability lift (M5)

```bash
python evaluate.py
```

Reports, **per failure kind**, naive `json.loads` success vs the full coerce loop. Robust should reach
~100% **except** the `unfixable` case — which must **fail closed** (stay 0%), never pass.

## File roles

| File | Role |
|------|------|
| `config.py` | provided — reliability params (`max_attempts`, `allow_repair`, `strict_enum`) |
| `schema.py` | provided — the `Ticket` contract (`TICKET_SCHEMA`) you validate against |
| `fake_backend.py` | reference — deterministic offline 'LLM' that emits realistic malformed output |
| `structured_output.py` | **learner** — parse / extract / validate / repair / coerce |
| `eval_set.jsonl` | provided — frozen set across the five failure kinds |
| `evaluate.py` | provided — naive-vs-robust scorer |
| `tests/` | provided |

## The rules that matter most

**Extraction fixes format noise; validation catches schema violations; only repair fixes those.**
**Fail closed** — never return an object that didn't validate. **Measure** the lift and the repair
cost; reliability you can't quantify isn't engineering. Constrained decoding (the extension) prevents
violations at the source instead of repairing them after.
